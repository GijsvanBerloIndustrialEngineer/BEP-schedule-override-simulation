"""
Event-driven override simulation (docs/CONCEPTUAL_MODEL.md, REPORT D1-D14).

One replication walks through Poisson arrivals in time order. Each arrival
looks at the *executed* calendar at that moment (so earlier overrides are
visible), picks the active task, draws an action from the override model
and updates the calendar. The result is the executed calendar, a list of
changes and the KPIs of the run.
"""

import math
import random
import statistics
from datetime import datetime, timedelta

from override_model import (
    ACTIONS,
    NO_OVERRIDE,
    action_probabilities,
    draw_action,
    is_eligible,
)
from rules import violated_rules

UNPLANNED_LABEL = "UNPLANNED"
EPSILON_HOURS = 1 / 60          # one minute tolerance for "fully executed"


# ============================================================
# 1. HELPERS
# ============================================================

def _hours(delta):
    return delta.total_seconds() / 3600


def _midnight(moment):
    return datetime.combine(moment.date(), datetime.min.time())


def _days_covered(start, end):
    """Dates an interval [start, end) touches."""
    day = start.date()
    last = (end - timedelta(microseconds=1)).date() if end > start else day
    days = []
    while day <= last:
        days.append(day)
        day += timedelta(days=1)
    return days


def _overlap_hours(start_a, end_a, start_b, end_b):
    return max(0.0, _hours(min(end_a, end_b) - max(start_a, start_b)))


def _union_hours(intervals):
    total = 0.0
    current_start = current_end = None
    for start, end in sorted(intervals):
        if current_end is None or start > current_end:
            if current_end is not None:
                total += _hours(current_end - current_start)
            current_start, current_end = start, end
        else:
            current_end = max(current_end, end)
    if current_end is not None:
        total += _hours(current_end - current_start)
    return total


def generate_arrivals(start, end, rate_per_hour, rng):
    """Poisson arrivals (D1): exponential gaps with mean 1 / rate."""
    if rate_per_hour <= 0:
        raise ValueError("rate_per_hour must be greater than zero.")
    arrivals = []
    if start is None or end is None or end <= start:
        return arrivals
    current = start
    while True:
        current += timedelta(hours=rng.expovariate(rate_per_hour))
        if current >= end:
            return arrivals
        arrivals.append(current)


# ============================================================
# 2. THE EXECUTED CALENDAR
# ============================================================

class ExecutedCalendar:
    """Executed blocks plus a per-day index for fast lookups."""

    def __init__(self, tasks, context_events):
        self.blocks = []
        self.by_day = {}
        self.context_by_day = {}
        for task in tasks:
            block = dict(task)
            block.update({
                "kind": "task",
                "origin_uid": task["uid"],
                "postpones": 0,
                "note": "",
            })
            self.add(block)
        for item in context_events:
            ctx = {
                "kind": "context",
                "event": item["context_value"],
                "context_category": item["context_category"],
                "start": item["start"],
                "end": item["end"],
            }
            for day in _days_covered(ctx["start"], ctx["end"]):
                self.context_by_day.setdefault(day, []).append(ctx)

    def add(self, block):
        self.blocks.append(block)
        for day in _days_covered(block["start"], block["end"]):
            self.by_day.setdefault(day, []).append(block)

    def remove(self, block):
        self.blocks.remove(block)
        for day_blocks in self.by_day.values():
            if block in day_blocks:
                day_blocks.remove(block)

    def shorten(self, block, new_end):
        """End a block earlier; drop it if nothing is left."""
        self.remove(block)
        if new_end > block["start"]:
            block["end"] = new_end
            self.add(block)

    def on_day(self, day):
        return self.by_day.get(day, [])

    def active_at(self, moment):
        return [
            b for b in self.on_day(moment.date())
            if b["start"] <= moment < b["end"]
        ]


def _is_sleep(block):
    return block.get("category") == "sleep" and not block.get("is_marker")


def _blocks_time(block):
    """Does this block occupy time for non-concurrent tasks?"""
    if block["kind"] == "unplanned":
        return True
    if block.get("is_marker"):
        return False
    return not block.get("is_concurrent")


# ============================================================
# 3. ONE DECISION STEP
# ============================================================

def remaining_planned_hours(calendar, moment):
    """D6: planned task hours left today from `moment` (union, no sleep)."""
    day_end = _midnight(moment) + timedelta(days=1)
    intervals = []
    for block in calendar.on_day(moment.date()):
        if block["kind"] != "task" or _is_sleep(block):
            continue
        if not _blocks_time(block):
            continue
        start, end = max(block["start"], moment), min(block["end"], day_end)
        if end > start:
            intervals.append((start, end))
    return _union_hours(intervals)


def earlier_overrides(changes, moment, window):
    """D5: number of overrides before `moment` inside the window."""
    if window == "day":
        return sum(
            1 for c in changes
            if c["time"] < moment and c["time"].date() == moment.date()
        )
    if window == "run":
        return sum(1 for c in changes if c["time"] < moment)
    hours = float(window)
    return sum(
        1 for c in changes
        if moment - timedelta(hours=hours) <= c["time"] < moment
    )


def find_free_slot(calendar, block, earliest, duration, experiment,
                   rules, use_rules):
    """
    D7: earliest start >= `earliest` on the same day, on the step grid and
    inside the waking window, where the block fits without overlapping
    time-blocking blocks and without breaking a temporal rule.
    """
    day_start = _midnight(earliest)
    window = experiment["daily_window"]
    wake = day_start + timedelta(minutes=window.get("wake_minutes", 0))
    latest_end = day_start + timedelta(
        minutes=window.get("sleep_minutes", 24 * 60)
    )
    step = timedelta(minutes=experiment.get("step_minutes") or 10)

    start = max(earliest, wake)
    offset = start - day_start
    steps = math.ceil(offset / step)
    start = day_start + steps * step

    day_blocks = calendar.on_day(earliest.date())
    neighbours = None
    if use_rules:
        # The task's own (interrupted) block is not a neighbour of itself
        neighbours = [b for b in day_blocks if b is not block]
        neighbours += calendar.context_by_day.get(
            earliest.date(), []
        )

    candidate = dict(block)
    candidate["kind"] = "task"
    while start + duration <= latest_end:
        end = start + duration
        clash = False
        for other in day_blocks:
            if other is block:
                continue
            if other["start"] < end and start < other["end"]:
                if _is_sleep(other) or (
                    not block.get("is_concurrent") and _blocks_time(other)
                ):
                    clash = True
                    break
        if not clash and use_rules:
            if violated_rules(candidate, start, end, neighbours, rules):
                clash = True
        if not clash:
            return start
        start += step
    return None


# ============================================================
# 4. ONE REPLICATION
# ============================================================

def run_replication(tasks, context_events, experiment, params, rules,
                    horizon, rate_per_hour, seed):
    """
    Run the override loop once. Returns a dict with the executed calendar,
    the decisions, the changes and the per-task outcomes.
    """
    arrival_rng = random.Random(f"arrivals-{seed}")
    notify_rng = random.Random(f"notifications-{seed}")
    decision_rng = random.Random(f"decisions-{seed}")

    calendar = ExecutedCalendar(tasks, context_events)

    # D9 eligibility and D10 notifications, per original task
    q = params.get("notification_share", 0)
    eligible = {}
    notified = {}
    for block in calendar.blocks:
        eligible[block["uid"]] = is_eligible(block, params)
        notified[block["uid"]] = 1 if notify_rng.random() < q else 0
    for block in calendar.blocks:
        block["eligible"] = eligible[block["uid"]]
        block["notified"] = notified[block["uid"]]

    max_postpones = params.get("max_postpones_per_task", 1)
    window = params.get("earlier_overrides_window", "day")
    use_rules = params.get("check_temporal_rules", True)

    arrivals = generate_arrivals(horizon[0], horizon[1], rate_per_hour,
                                 arrival_rng)
    decisions = []
    changes = []

    for moment in arrivals:
        active = [b for b in calendar.active_at(moment)
                  if b["kind"] == "task" and not b.get("is_marker")]
        record = {"time": moment, "outcome": None, "task": None}
        decisions.append(record)

        # D2: ignore the arrival in free time and during sleep
        if not active:
            in_unplanned = any(b["kind"] == "unplanned"
                               for b in calendar.active_at(moment))
            record["outcome"] = (
                "ignored: unplanned block" if in_unplanned
                else "ignored: free time"
            )
            continue
        if any(_is_sleep(b) for b in active):
            record["outcome"] = "ignored: sleep"
            continue
        candidates = [b for b in active if b["eligible"]]
        if not candidates:
            record["outcome"] = "ignored: excluded task"
            record["task"] = ", ".join(b["label"] for b in active)
            continue

        # The active task: a time-blocking task first, then a random one
        main = [b for b in candidates if not b.get("is_concurrent")]
        block = decision_rng.choice(main or candidates)

        fill = remaining_planned_hours(calendar, moment)
        earlier = earlier_overrides(changes, moment, window)
        allowed = tuple(
            a for a in ACTIONS
            if a != "postpone" or block["postpones"] < max_postpones
        )
        probabilities, _ = action_probabilities(
            params, fill, earlier, block["notified"], allowed
        )
        action = draw_action(probabilities, decision_rng)

        record.update({
            "task": block["label"],
            "task_uid": block["origin_uid"],
            "fill_hours": fill,
            "earlier_overrides": earlier,
            "notified": block["notified"],
            "p_none": probabilities[NO_OVERRIDE],
            "p_postpone": probabilities["postpone"],
            "p_skip": probabilities["skip"],
            "p_replace": probabilities["replace"],
            "action": action,
        })

        if action == NO_OVERRIDE:
            record["outcome"] = "no override"
            continue

        old_start, old_end = block["start"], block["end"]
        remaining = old_end - moment
        change = {
            "time": moment,
            "task_uid": block["origin_uid"],
            "label": block["label"],
            "event": block["event"],
            "drawn_action": action,
            "action": action,
            "planned_start": old_start,
            "planned_end": old_end,
            "affected_hours": _hours(remaining),
            "new_start": None,
            "new_end": None,
            "delay_hours": None,
            "fill_hours": fill,
            "earlier_overrides": earlier,
            "notified": block["notified"],
            "p_none": probabilities[NO_OVERRIDE],
            "p_postpone": probabilities["postpone"],
            "p_skip": probabilities["skip"],
            "p_replace": probabilities["replace"],
            "note": "",
        }

        if action == "postpone":
            new_start = find_free_slot(
                calendar, block, old_end, remaining, experiment, rules,
                use_rules,
            )
            if new_start is None:
                # D7 rule: no free slot left today -> the task is skipped
                action = "skip"
                change["action"] = "skip"
                change["note"] = "postpone failed: no free slot today"
            else:
                calendar.shorten(block, moment)
                moved = dict(block)
                moved.update({
                    "start": new_start,
                    "end": new_start + remaining,
                    "postpones": block["postpones"] + 1,
                    "note": f"postponed from {moment:%Y-%m-%d %H:%M}",
                })
                calendar.add(moved)
                change.update({
                    "new_start": moved["start"],
                    "new_end": moved["end"],
                    "delay_hours": _hours(new_start - moment),
                })

        if action == "skip":
            calendar.shorten(block, moment)

        if action == "replace":
            calendar.shorten(block, moment)
            calendar.add({
                "kind": "unplanned",
                "uid": f"{block['origin_uid']}-unplanned-{len(changes)}",
                "origin_uid": block["origin_uid"],
                "label": UNPLANNED_LABEL,
                "event": UNPLANNED_LABEL,
                "category": None,
                "intensity": None,
                "is_concurrent": False,
                "is_marker": False,
                "eligible": False,
                "person_id": block.get("person_id"),
                "start": moment,
                "end": old_end,
                "postpones": 0,
                "note": f"replaces {block['label']}",
            })
            change.update({"new_start": moment, "new_end": old_end})

        if block["start"] < moment:
            block["note"] = f"interrupted at {moment:%H:%M} ({change['action']})"
        record["outcome"] = change["action"]
        changes.append(change)

    outcomes = task_outcomes(tasks, calendar, changes, eligible, notified)
    return {
        "seed": seed,
        "calendar": calendar,
        "arrivals": arrivals,
        "decisions": decisions,
        "changes": changes,
        "outcomes": outcomes,
    }


# ============================================================
# 5. OUTCOMES AND KPIS (D13)
# ============================================================

def task_outcomes(tasks, calendar, changes, eligible, notified):
    """Per original task: planned vs executed hours and what happened."""
    pieces = {}
    for block in calendar.blocks:
        if block["kind"] == "task":
            pieces.setdefault(block["origin_uid"], []).append(block)
    actions = {}
    for change in changes:
        actions.setdefault(change["task_uid"], []).append(change["action"])

    outcomes = []
    for task in tasks:
        planned = task["duration_hours"] or 0.0
        own = pieces.get(task["uid"], [])
        executed = sum(_hours(b["end"] - b["start"]) for b in own)
        on_plan = sum(
            _overlap_hours(b["start"], b["end"], task["start"], task["end"])
            for b in own
        ) if task["end"] else 0.0
        task_actions = actions.get(task["uid"], [])
        if not task_actions:
            final = "as planned"
        else:
            final = task_actions[-1]
        outcomes.append({
            "uid": task["uid"],
            "label": task["label"],
            "event": task["event"],
            "eligible": eligible[task["uid"]],
            "notified": notified[task["uid"]],
            "planned_hours": planned,
            "executed_hours": executed,
            "completed": executed >= planned - EPSILON_HOURS,
            "postponed": "postpone" in task_actions,
            "skipped": "skip" in task_actions,
            "replaced": "replace" in task_actions,
            "actions": ", ".join(task_actions),
            "final": final,
            # plan-execution deviation: symmetric difference in hours
            "deviation_hours": planned + executed - 2 * on_plan,
        })
    return outcomes


def replication_kpis(result):
    outcomes = result["outcomes"]
    eligible = [o for o in outcomes if o["eligible"]]
    n = len(eligible)
    decisions = result["decisions"]
    delays = [c["delay_hours"] for c in result["changes"]
              if c["delay_hours"] is not None]

    def share(flag):
        return sum(1 for o in eligible if o[flag]) / n if n else None

    def count(outcome):
        return sum(1 for d in decisions if d["outcome"] == outcome)

    return {
        "Completion rate (eligible tasks)": share("completed"),
        "Completion rate (all tasks)": (
            sum(1 for o in outcomes if o["completed"]) / len(outcomes)
            if outcomes else None
        ),
        "Share postponed": share("postponed"),
        "Share skipped": share("skipped"),
        "Share replaced": share("replaced"),
        "Mean postponement delay (hours)": (
            statistics.mean(delays) if delays else None
        ),
        "Plan-execution deviation (hours)": sum(
            o["deviation_hours"] for o in outcomes
        ),
        "Planned task hours": sum(o["planned_hours"] for o in outcomes),
        "Executed task hours": sum(o["executed_hours"] for o in outcomes),
        "Eligible tasks": n,
        "Arrivals": len(decisions),
        "Override checks": sum(1 for d in decisions if "action" in d),
        "Overrides": len(result["changes"]),
        "Failed postponements (became skip)": sum(
            1 for c in result["changes"] if c["note"].startswith("postpone failed")
        ),
        "Arrivals ignored: free time": count("ignored: free time"),
        "Arrivals ignored: sleep": count("ignored: sleep"),
        "Arrivals ignored: excluded task": count("ignored: excluded task"),
        "Arrivals ignored: unplanned block": count("ignored: unplanned block"),
    }


# Two-sided 95% t quantiles for df = 1..30; normal value above.
_T975 = [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262,
         2.228, 2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101,
         2.093, 2.086, 2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052,
         2.048, 2.045, 2.042]


def t_quantile_975(df):
    if df < 1:
        return None
    if df <= len(_T975):
        return _T975[df - 1]
    if df <= 60:
        return 2.000
    if df <= 120:
        return 1.980
    return 1.960


def summarise_kpis(per_replication):
    """D14: mean, standard deviation and 95% confidence interval per KPI."""
    if not per_replication:
        return []
    rows = []
    for name in per_replication[0]:
        values = [kpis[name] for kpis in per_replication
                  if kpis[name] is not None]
        if not values:
            rows.append((name, None, None, None, None, 0))
            continue
        mean = statistics.mean(values)
        if len(values) > 1:
            sd = statistics.stdev(values)
            half = t_quantile_975(len(values) - 1) * sd / math.sqrt(len(values))
            rows.append((name, mean, sd, mean - half, mean + half, len(values)))
        else:
            rows.append((name, mean, None, None, None, 1))
    return rows
