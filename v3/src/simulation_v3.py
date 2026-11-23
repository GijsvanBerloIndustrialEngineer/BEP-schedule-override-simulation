"""
Event-driven execution simulation, version 3 (two stages).

Events in time order (at equal times: review, then start, then arrival):

  review   once per day, before the day: every eligible task of that day is
           kept, moved to a later day, or dropped (stage 1, model_v3).
  start    at the planned (or new) start of an eligible task: the version 2
           decision none / postpone / skip / replace with the momentary
           context (stage 2). If the task starts, a progress draw decides
           whether it is finished or stopped part-way (partial).
  arrival  optional Poisson interruption during a task (off by default).

Execution states per planned task: rejected (dropped at review), missed
(skipped), replaced, partial, completed; with the flags moved at review
and postponed at start. Versions 1 and 2 are imported and not changed.
"""

import heapq
import random
import statistics
import sys
from datetime import datetime, timedelta
from pathlib import Path

V3_DIR = Path(__file__).resolve().parent.parent
V2_SRC = V3_DIR.parent / "v2" / "src"
V1_SRC = V3_DIR.parent / "src"
for p in (V2_SRC, V1_SRC):
    if str(p) not in sys.path:
        sys.path.append(str(p))

from override_simulation import (  # noqa: E402  (v1)
    ExecutedCalendar, remaining_planned_hours, earlier_overrides,
    generate_arrivals, task_outcomes, _hours, _midnight, _is_sleep,
)
from override_model import is_eligible  # noqa: E402  (v1)
from model_v2 import (  # noqa: E402
    ACTIONS, NO_OVERRIDE, action_probabilities, active_contexts,
    choose_replacement, context_covariates, draw_action, persona_traits,
)
from simulation_v2 import find_slot_across_days  # noqa: E402
from model_v3 import KEEP, draw, finish_probability, review_probabilities  # noqa: E402

PRIORITY = {"review": 0, "start": 1, "arrival": 2}
STATES = ("completed", "partial", "rejected", "missed", "replaced")


def _parse_time(text):
    h, m = (int(x) for x in str(text).split(":"))
    return timedelta(hours=h, minutes=m)


def run_replication(tasks, context_events, experiment, params, rules, horizon,
                    config, seed, persona=None, persona_settings=None):
    persona_settings = persona_settings or {"trait_source": "mean", "centre": 0.5}
    stages = config.get("stages") or {}
    review = stages.get("review") or {}
    progress = stages.get("progress") or {}
    triggers = config["triggers"]

    rng = {k: random.Random(f"{k}-{seed}") for k in
           ("arrivals", "notifications", "decisions", "replacements", "traits",
            "review", "progress")}
    traits = persona_traits(persona, persona_settings.get("trait_source", "mean"), rng["traits"])
    centre = persona_settings.get("centre", 0.5)
    calendar = ExecutedCalendar(tasks, context_events)

    q = params.get("notification_share", 0)
    eligible, notified = {}, {}
    for b in calendar.blocks:
        eligible[b["uid"]] = bool(b.get("force_eligible") or is_eligible(b, params))
        notified[b["uid"]] = 1 if rng["notifications"].random() < q else 0
        b.update(eligible=eligible[b["uid"]], notified=notified[b["uid"]], moves=0,
                 reviewed_day=None)

    events = {uid: [] for uid in eligible}
    changes, exec_changes, decisions = [], [], []
    queue, order = [], [0]

    def push(t, kind, payload):
        heapq.heappush(queue, (t, PRIORITY[kind], order[0], kind, payload))
        order[0] += 1

    start, end = horizon
    if review.get("enabled"):
        offset = _parse_time(review.get("time", "07:00"))
        day = start.date()
        while datetime.combine(day, datetime.min.time()) < end:
            midnight = datetime.combine(day, datetime.min.time())
            moment = (midnight + offset if review.get("mode", "same_morning") == "same_morning"
                      else midnight - timedelta(days=1) + offset)
            push(moment, "review", day)
            day += timedelta(days=1)
    if triggers.get("task_start", True):
        for b in calendar.blocks:
            if b["eligible"] and not b.get("is_marker"):
                push(b["start"], "start", b)
    rate = triggers.get("rate_per_hour", 0) or 0
    if rate > 0:
        for t in generate_arrivals(start, end, rate, rng["arrivals"]):
            push(t, "arrival", None)

    max_postpones = params.get("max_postpones_per_task", 1)
    window = params.get("earlier_overrides_window", "day")
    move_params = dict(params, postpone_window={"mode": "rolling",
                                                "days": review.get("move_window_days", 7)})

    # ---------------------------------------------------------- stage 1
    def do_review(day, moment):
        midnight = datetime.combine(day, datetime.min.time())
        todays = sorted((b for b in calendar.on_day(day)
                         if b["kind"] == "task" and b["eligible"] and not b.get("is_marker")
                         and b["start"].date() == day and b["start"] >= moment
                         and b.get("reviewed_day") != day),
                        key=lambda b: b["start"])
        day_load = remaining_planned_hours(calendar, max(moment, midnight))
        for b in todays:
            b["reviewed_day"] = day
            probs = review_probabilities(review, day_load, b.get("intensity"), traits, centre)
            action = draw(probs, rng["review"], (KEEP, "move", "drop"))
            if action == "move" and b["moves"] >= review.get("max_moves_per_task", 1):
                action = KEEP
            rec = {"time": moment, "stage": "review", "task": b["label"],
                   "task_uid": b["origin_uid"], "day_load": day_load,
                   "p_keep": probs[KEEP], "p_move": probs["move"], "p_drop": probs["drop"],
                   "outcome": action}
            decisions.append(rec)
            if action == KEEP:
                events[b["origin_uid"]].append("kept")
                continue
            dur = b["end"] - b["start"]
            if action == "move":
                slot = find_slot_across_days(calendar, b, midnight + timedelta(days=1), dur,
                                             experiment, rules, move_params, end)
                if slot is None:
                    rec["outcome"] = "keep (no slot to move to)"
                    events[b["origin_uid"]].append("kept")
                    continue
                calendar.remove(b)
                moved = dict(b, start=slot, end=slot + dur, moves=b["moves"] + 1,
                             reviewed_day=None, note=f"moved at review on {day:%Y-%m-%d}")
                calendar.add(moved)
                push(slot, "start", moved)
                events[b["origin_uid"]].append("moved")
                changes.append(_change(moment, b, "move", "review", slot, slot + dur,
                                       _hours(slot - b["start"])))
            else:
                calendar.remove(b)
                events[b["origin_uid"]].append("dropped")
                changes.append(_change(moment, b, "drop", "review"))

    # ---------------------------------------------------------- stage 2
    def decide(block, moment, kind):
        contexts = active_contexts(calendar.context_by_day, moment)
        ctx_values = context_covariates(block, contexts, params)
        fill = remaining_planned_hours(calendar, moment)
        earlier = earlier_overrides(exec_changes, moment, window)
        allowed = tuple(a for a in ACTIONS if a != "postpone" or block["postpones"] < max_postpones)
        probs, _ = action_probabilities(params, fill, earlier, block["notified"], ctx_values,
                                        traits, centre, block.get("intensity") or 1, allowed)
        action = draw_action(probs, rng["decisions"])
        rec = {"time": moment, "stage": kind, "task": block["label"],
               "task_uid": block["origin_uid"], "fill_hours": fill,
               "earlier_overrides": earlier, "notified": block["notified"],
               "active_context": ", ".join(k for k, v in ctx_values.items() if v),
               **{f"p_{a}": probs[a] for a in (NO_OVERRIDE,) + ACTIONS}, "outcome": action}
        decisions.append(rec)
        return action, contexts, ctx_values, rec

    def apply_override(block, moment, action, contexts, rec):
        cut = max(moment, block["start"])
        remaining = block["end"] - cut
        uid = block["origin_uid"]
        planned = (block["start"], block["end"])   # before shorten() changes the block
        if action == "postpone":
            slot = find_slot_across_days(calendar, block, block["end"], remaining,
                                         experiment, rules, params, end)
            if slot is None:
                action = "skip"
                rec["outcome"] = "skip (postpone failed)"
            else:
                calendar.shorten(block, cut)
                moved = dict(block, start=slot, end=slot + remaining,
                             postpones=block["postpones"] + 1,
                             note=f"postponed from {moment:%Y-%m-%d %H:%M}")
                calendar.add(moved)
                push(slot, "start", moved)
                events[uid].append("postponed")
                c = _change(moment, block, "postpone", "execution", slot, slot + remaining,
                            _hours(slot - cut), planned=planned)
                changes.append(c); exec_changes.append(c)
                return
        if action == "skip":
            calendar.shorten(block, cut)
            events[uid].append("skipped")
        if action == "replace":
            calendar.shorten(block, cut)
            name, _ = choose_replacement(params, contexts, traits, centre, rng["replacements"])
            spec = (params.get("replacements") or {}).get(name) or {}
            stop = min(cut + remaining,
                       cut + timedelta(minutes=spec.get("max_minutes") or 10 ** 6))
            calendar.add({
                "kind": "replacement", "uid": f"{uid}-repl-{len(changes)}", "origin_uid": uid,
                "label": name or "replacement", "summary": name or "replacement",
                "event": spec.get("event") or name, "catalog_event": spec.get("event"),
                "category": "replacement", "intensity": None, "is_concurrent": False,
                "is_marker": False, "eligible": False, "person_id": block.get("person_id"),
                "start": cut, "end": stop, "postpones": 0, "note": f"replaces {block['label']}",
            })
            events[uid].append("replaced")
            rec["replacement"] = name
        c = _change(moment, block, action, "execution", planned=planned)
        changes.append(c); exec_changes.append(c)

    def do_start(block, moment):
        if block not in calendar.blocks or block["start"] != moment:
            return
        action, contexts, ctx_values, rec = decide(block, moment, "start")
        if action != NO_OVERRIDE:
            apply_override(block, moment, action, contexts, rec)
            return
        events[block["origin_uid"]].append("started")
        if not progress.get("enabled"):
            return
        p_fin = finish_probability(progress, ctx_values, block.get("intensity"), traits, centre)
        rec["p_finish"] = p_fin
        if rng["progress"].random() < p_fin:
            return
        lo, hi = progress.get("stop_fraction", [0.25, 0.85])
        share = rng["progress"].uniform(lo, hi)
        dur = block["end"] - block["start"]
        stop = block["start"] + timedelta(minutes=max(1, round(_hours(dur) * 60 * share)))
        planned = (block["start"], block["end"])
        calendar.shorten(block, stop)
        block["note"] = f"stopped after {100 * share:.0f}% (partial)"
        events[block["origin_uid"]].append("partial")
        rec["outcome"] = "started, partial"
        changes.append(_change(stop, block, "partial", "progress", planned=planned))

    def do_arrival(moment):
        active = [b for b in calendar.active_at(moment)
                  if b["kind"] == "task" and not b.get("is_marker")]
        if not active or any(_is_sleep(b) for b in active):
            return
        cands = [b for b in active if b["eligible"]]
        if not cands:
            return
        main = [b for b in cands if not b.get("is_concurrent")]
        block = rng["decisions"].choice(main or cands)
        action, contexts, _, rec = decide(block, moment, "interruption")
        if action != NO_OVERRIDE:
            apply_override(block, moment, action, contexts, rec)

    while queue:
        moment, _, _, kind, payload = heapq.heappop(queue)
        if kind == "review":
            do_review(payload, moment)
        elif kind == "start":
            do_start(payload, moment)
        else:
            do_arrival(moment)

    outcomes = task_outcomes(tasks, calendar, changes, eligible, notified)
    for o in outcomes:
        o["state"] = final_state(events.get(o["uid"], []), o)
        o["moved_at_review"] = "moved" in events.get(o["uid"], [])
        o["postponed_at_start"] = "postponed" in events.get(o["uid"], [])
    return {"seed": seed, "calendar": calendar, "decisions": decisions,
            "changes": changes, "outcomes": outcomes, "traits": traits}


def _change(t, block, action, stage, new_start=None, new_end=None, delay=None, planned=None):
    """One change; `planned` = (start, end) of the block before it was cut."""
    p_start, p_end = planned or (block["start"], block["end"])
    return {"time": t, "task_uid": block["origin_uid"], "label": block["label"],
            "event": block.get("event"), "category": block.get("category"),
            "action": action, "stage": stage, "planned_start": p_start,
            "planned_end": p_end, "new_start": new_start, "new_end": new_end,
            "delay_hours": delay, "days_moved": ((new_start.date() - t.date()).days
                                                 if new_start else None), "note": ""}


def final_state(ev, outcome):
    """Execution state of one planned task (plan of work, SRQ2)."""
    if not outcome["eligible"]:
        return "not eligible"
    if "dropped" in ev:
        return "rejected"
    if "skipped" in ev:
        return "missed"
    if "replaced" in ev:
        return "replaced"
    if "partial" in ev:
        return "partial"
    return "completed" if outcome["completed"] else "partial"


def replication_kpis(result, predicate=None):
    outs = [o for o in result["outcomes"] if o["eligible"] and (predicate is None or predicate(o))]
    n = len(outs)
    share = (lambda f: sum(1 for o in outs if f(o)) / n) if n else (lambda f: None)
    dec = result["decisions"]
    reviews = [d for d in dec if d["stage"] == "review"]
    starts = [d for d in dec if d["stage"] == "start"]
    delays = [c["delay_hours"] for c in result["changes"]
              if c["action"] == "postpone" and c["delay_hours"] is not None]
    kpis = {"Completion rate (eligible tasks)": share(lambda o: o["state"] == "completed")}
    for s in STATES:
        kpis[f"Share {s}"] = share(lambda o, s=s: o["state"] == s)
    kpis.update({
        "Share moved at review": share(lambda o: o["moved_at_review"]),
        "Share postponed at start": share(lambda o: o["postponed_at_start"]),
        "Plan-execution deviation (hours)": sum(o["deviation_hours"] for o in result["outcomes"]),
        "Mean postponement delay (hours)": statistics.mean(delays) if delays else None,
        "Review decisions": len(reviews),
        "Start decisions": len(starts),
        "Started tasks that end partial": (
            sum(1 for d in starts if d["outcome"] == "started, partial")
            / max(1, sum(1 for d in starts if str(d["outcome"]).startswith("none")
                         or d["outcome"] == "started, partial"))),
        "Eligible tasks": n,
    })
    return kpis
