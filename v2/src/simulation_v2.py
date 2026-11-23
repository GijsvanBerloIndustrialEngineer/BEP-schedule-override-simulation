"""
Event-driven override simulation, version 2.

The loop is the same as v1 (docs/CONCEPTUAL_MODEL.md): a trigger looks at the
*executed* calendar, picks the active task, draws an action and updates the
calendar. What changed:

- Triggers: Poisson arrivals (v1) plus, optionally, one decision at the
  start of every eligible task (also at the new start of a postponed task).
- Probability: context covariates and persona traits (model_v2.py).
- Postpone: the next free slot may be on a later day (postpone_max_days_ahead).
- Replace: a concrete activity chosen from the context (rest, snack,
  socialise, ...) instead of a generic UNPLANNED block.

v1 code is imported from ../../src and not changed.
"""

import heapq
import random
import sys
from datetime import timedelta
from pathlib import Path

V1_SRC = Path(__file__).resolve().parents[2] / "src"
if str(V1_SRC) not in sys.path:
    sys.path.insert(0, str(V1_SRC))

from override_simulation import (  # noqa: E402  (v1, unchanged)
    ExecutedCalendar,
    find_free_slot,
    remaining_planned_hours,
    earlier_overrides,
    generate_arrivals,
    task_outcomes,
    replication_kpis as v1_replication_kpis,
    _hours,
    _midnight,
    _is_sleep,
)
from override_model import is_eligible  # noqa: E402  (v1 eligibility rule)

from model_v2 import (  # noqa: E402
    ACTIONS,
    NO_OVERRIDE,
    action_probabilities,
    active_contexts,
    choose_replacement,
    context_covariates,
    draw_action,
    persona_traits,
)

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# ============================================================
# 1. POSTPONE ACROSS DAYS
# ============================================================

def find_slot_across_days(calendar, block, earliest, duration, experiment,
                          rules, params, horizon_end):
    """
    Earliest feasible slot from `earliest` on within the replanning window
    (v1's find_free_slot per day). The window spans a week:
      rolling       : `days` days from the interruption (default 7)
      calendar_week : until the end of the same Mon-Sun week
      same_day      : only the same day (v1)
    """
    window = params.get("postpone_window") or {"mode": "rolling", "days": 7}
    mode = window.get("mode", "rolling")
    if mode == "same_day":
        max_days = 0
    elif mode == "calendar_week":
        max_days = 6 - earliest.weekday()
    elif mode == "rolling":
        # `days` days counted from the interruption: offsets 0 .. days-1
        max_days = max(0, int(window.get("days", 7)) - 1)
    else:
        raise ValueError(f"Unknown postpone_window.mode '{mode}'")
    use_rules = params.get("check_temporal_rules", True)
    allowed_days = None
    if params.get("postpone_respect_weekdays"):
        entry = experiment["event_catalog"].get(block.get("event")) or {}
        if entry.get("weekdays"):
            allowed_days = set(entry["weekdays"])
    for offset in range(max_days + 1):
        if offset == 0:
            start_from = earliest
        else:
            start_from = _midnight(earliest) + timedelta(days=offset)
        if horizon_end is not None and start_from >= horizon_end:
            break
        if allowed_days and WEEKDAYS[start_from.weekday()] not in allowed_days:
            continue
        slot = find_free_slot(calendar, block, start_from, duration,
                              experiment, rules, use_rules)
        if slot is not None:
            return slot
    return None


# ============================================================
# 2. ONE REPLICATION
# ============================================================

def run_replication(tasks, context_events, experiment, params, rules,
                    horizon, triggers, seed, persona=None,
                    persona_settings=None, notified_override=None):
    """
    Run the v2 override loop once.

    tasks             : planned tasks (base calendar, plus health tasks if any)
    triggers          : {"rate_per_hour": float, "task_start": bool}
    persona           : persona dict from persona_config.yaml (or None)
    persona_settings  : {"trait_source": mean|sample, "centre": 0.5}
    notified_override : optional {uid: 0/1}, to fix notifications per task
    """
    persona_settings = persona_settings or {"trait_source": "mean", "centre": 0.5}
    arrival_rng = random.Random(f"arrivals-{seed}")
    notify_rng = random.Random(f"notifications-{seed}")
    decision_rng = random.Random(f"decisions-{seed}")
    replace_rng = random.Random(f"replacements-{seed}")
    trait_rng = random.Random(f"traits-{seed}")

    traits = persona_traits(persona, persona_settings.get("trait_source", "mean"),
                            trait_rng)
    centre = persona_settings.get("centre", 0.5)

    calendar = ExecutedCalendar(tasks, context_events)

    q = params.get("notification_share", 0)
    eligible, notified = {}, {}
    for block in calendar.blocks:
        uid = block["uid"]
        eligible[uid] = block.get("force_eligible") or is_eligible(block, params)
        if notified_override and uid in notified_override:
            notified[uid] = notified_override[uid]
        else:
            notified[uid] = 1 if notify_rng.random() < q else 0
        block["eligible"] = eligible[uid]
        block["notified"] = notified[uid]

    max_postpones = params.get("max_postpones_per_task", 1)
    window = params.get("earlier_overrides_window", "day")
    horizon_end = horizon[1]

    # Trigger queue: (time, order, kind, block). kind "arrival" or "start".
    queue = []
    order = 0
    for moment in generate_arrivals(horizon[0], horizon[1],
                                    triggers["rate_per_hour"], arrival_rng):
        queue.append((moment, order, "arrival", None))
        order += 1
    if triggers.get("task_start"):
        for block in calendar.blocks:
            if block["eligible"] and not block.get("is_marker"):
                queue.append((block["start"], order, "start", block))
                order += 1
    heapq.heapify(queue)

    decisions, changes = [], []

    while queue:
        moment, _, kind, target = heapq.heappop(queue)
        record = {"time": moment, "trigger": kind, "outcome": None, "task": None}
        decisions.append(record)

        if kind == "start":
            # The block may have been shortened, moved or removed meanwhile
            if target not in calendar.blocks or target["start"] != moment:
                record["outcome"] = "ignored: start of changed task"
                continue
            block = target
        else:
            active = [b for b in calendar.active_at(moment)
                      if b["kind"] == "task" and not b.get("is_marker")]
            if not active:
                in_repl = any(b["kind"] == "replacement"
                              for b in calendar.active_at(moment))
                record["outcome"] = ("ignored: replacement activity" if in_repl
                                     else "ignored: free time")
                continue
            if any(_is_sleep(b) for b in active):
                record["outcome"] = "ignored: sleep"
                continue
            candidates = [b for b in active if b["eligible"]]
            if not candidates:
                record["outcome"] = "ignored: excluded task"
                continue
            main = [b for b in candidates if not b.get("is_concurrent")]
            block = decision_rng.choice(main or candidates)

        contexts = active_contexts(calendar.context_by_day, moment)
        ctx_values = context_covariates(block, contexts, params)
        fill = remaining_planned_hours(calendar, moment)
        earlier = earlier_overrides(changes, moment, window)
        allowed = tuple(a for a in ACTIONS
                        if a != "postpone" or block["postpones"] < max_postpones)
        probabilities, parts = action_probabilities(
            params, fill, earlier, block["notified"], ctx_values, traits,
            centre, block.get("intensity") or 1, allowed,
        )
        action = draw_action(probabilities, decision_rng)

        record.update({
            "task": block["label"], "task_uid": block["origin_uid"],
            "category": block.get("category"),
            "fill_hours": fill, "earlier_overrides": earlier,
            "notified": block["notified"],
            "active_context_covariates": ", ".join(
                k for k, v in ctx_values.items() if v),
            "eta_context_postpone": parts["postpone"]["context"],
            "eta_persona_postpone": parts["postpone"]["persona"],
            **{f"p_{a}": probabilities[a] for a in (NO_OVERRIDE,) + ACTIONS},
            "action": action,
        })
        if action == NO_OVERRIDE:
            record["outcome"] = "no override"
            continue

        old_start, old_end = block["start"], block["end"]
        cut = max(moment, old_start)
        remaining = old_end - cut
        change = {
            "time": moment, "trigger": kind,
            "task_uid": block["origin_uid"], "label": block["label"],
            "event": block["event"], "category": block.get("category"),
            "drawn_action": action, "action": action,
            "planned_start": old_start, "planned_end": old_end,
            "affected_hours": _hours(remaining),
            "new_start": None, "new_end": None, "delay_hours": None,
            "days_moved": None, "replacement": None,
            "fill_hours": fill, "earlier_overrides": earlier,
            "notified": block["notified"],
            "active_context_covariates": record["active_context_covariates"],
            **{f"p_{a}": probabilities[a] for a in (NO_OVERRIDE,) + ACTIONS},
            "note": "",
        }

        if action == "postpone":
            new_start = find_slot_across_days(
                calendar, block, old_end, remaining, experiment, rules,
                params, horizon_end,
            )
            if new_start is None:
                action = "skip"
                change["action"] = "skip"
                change["note"] = "postpone failed: no free slot in the search window"
            else:
                calendar.shorten(block, cut)
                moved = dict(block)
                moved.update({
                    "start": new_start, "end": new_start + remaining,
                    "postpones": block["postpones"] + 1,
                    "note": f"postponed from {moment:%Y-%m-%d %H:%M}",
                })
                calendar.add(moved)
                if triggers.get("task_start"):
                    heapq.heappush(queue, (new_start, order, "start", moved))
                    order += 1
                change.update({
                    "new_start": moved["start"], "new_end": moved["end"],
                    "delay_hours": _hours(new_start - cut),
                    "days_moved": (new_start.date() - cut.date()).days,
                })

        if action == "skip":
            calendar.shorten(block, cut)

        if action == "replace":
            calendar.shorten(block, cut)
            name, _ = choose_replacement(params, contexts, traits, centre,
                                         replace_rng)
            spec = (params.get("replacements") or {}).get(name) or {}
            cap = timedelta(minutes=spec.get("max_minutes") or 10 ** 6)
            end = min(old_end, cut + cap)
            calendar.add({
                "kind": "replacement",
                "uid": f"{block['origin_uid']}-repl-{len(changes)}",
                "origin_uid": block["origin_uid"],
                "label": name or "replacement",
                "summary": name or "replacement",
                "event": spec.get("event") or name,
                "catalog_event": spec.get("event"),
                "category": "replacement",
                "intensity": None, "is_concurrent": False, "is_marker": False,
                "eligible": False, "person_id": block.get("person_id"),
                "start": cut, "end": end, "postpones": 0,
                "note": f"replaces {block['label']}",
            })
            change.update({"new_start": cut, "new_end": end,
                           "replacement": name})

        if block["start"] < cut:
            block["note"] = f"interrupted at {cut:%H:%M} ({change['action']})"
        record["outcome"] = change["action"]
        changes.append(change)

    outcomes = task_outcomes(tasks, calendar, changes, eligible, notified)
    return {
        "seed": seed, "calendar": calendar, "decisions": decisions,
        "changes": changes, "outcomes": outcomes, "traits": traits,
    }


# ============================================================
# 3. KPIS
# ============================================================

def replication_kpis(result, category_filter=None):
    """v1 KPIs plus the new v2 ones."""
    kpis = v1_replication_kpis(result)
    kpis.pop("Arrivals ignored: unplanned block", None)
    # v1 counts every decision moment as an arrival; v2 also has task starts
    triggers = kpis.pop("Arrivals")
    kpis["Triggers (Poisson arrivals + task starts)"] = triggers
    kpis["Task-start triggers"] = sum(
        1 for d in result["decisions"] if d["trigger"] == "start")
    changes = result["changes"]
    postponed = [c for c in changes if c["days_moved"] is not None]
    kpis["Share of postponements to a later day"] = (
        sum(1 for c in postponed if c["days_moved"] > 0) / len(postponed)
        if postponed else None)
    kpis["Replaced hours"] = sum(
        _hours(c["new_end"] - c["new_start"]) for c in changes
        if c["action"] == "replace")
    checks = [d for d in result["decisions"] if "action" in d]
    kpis["Decisions with an active context covariate"] = (
        sum(1 for d in checks if d["active_context_covariates"]) / len(checks)
        if checks else None)
    for name in sorted({c["replacement"] for c in changes if c["replacement"]}):
        kpis[f"Replacements: {name}"] = sum(
            1 for c in changes if c["replacement"] == name)
    return kpis


def group_completion(result, predicate):
    """Completion rate of the original tasks for which predicate(uid) is true."""
    outs = [o for o in result["outcomes"] if predicate(o)]
    if not outs:
        return None
    return sum(1 for o in outs if o["completed"]) / len(outs)
