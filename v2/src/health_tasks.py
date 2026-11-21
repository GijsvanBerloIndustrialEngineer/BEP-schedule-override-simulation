"""
Health tasks of the calendar-bench healthy_lifestyle_promotion scenario and
the planning methods that place them into a person's calendar.

Two sources of placements:

1. calendar-bench solution files (<person_id>.json with a "scheduled" list),
   one folder per planning method. The human coach schedules are published
   in calendar-bench; other methods' output can be added the same way.
2. Planning methods built into v2 that place the SAME task batch:
   - fcfs_greedy_v2  : re-implementation of calendar-bench's documented FCFS
                       greedy (earliest untouched free gap that fits).
                       Not calendar-bench's own code or output.
   - random_slot_v2  : a uniformly random free slot in the task's week
                       (context-blind baseline).
   - context_aware_v2: the free slot in the task's week with the highest
                       probability of "no override" under the v2 model at
                       the planned start (context- and persona-informed).
"""

import json
import random
import re
from datetime import date, datetime, timedelta
from pathlib import Path

from model_v2 import (
    action_probabilities,
    active_contexts,
    context_covariates,
    persona_traits,
    NO_OVERRIDE,
)

DOMAIN_KEYWORDS = {
    "PhysicalActivity": ["walk", "step", "run", "cardio", "stretch", "clean",
                         "exercise", "squat", "yoga", "cycle", "bike", "stairs",
                         "dance", "move", "strength", "push"],
    "Nutrition": ["eat", "cook", "meal", "drink", "water", "fruit", "veg",
                  "snack", "breakfast", "lunch", "dinner", "sugar", "protein"],
    "MentalWellbeing": ["breath", "mindful", "journal", "gratitude", "calm",
                        "rest", "relax", "meditat", "reflect", "sleep", "screen"],
}
LEVEL_RE = re.compile(r"Level(\d)")


def load_catalog(path):
    if path is None or not Path(path).exists():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8")).get("tasks", {})


def domain_of(slug, entry):
    if entry and entry.get("domain"):
        return entry["domain"], "ontology"
    text = slug.replace("_", "-").lower()
    for domain, words in DOMAIN_KEYWORDS.items():
        if any(w in text for w in words):
            return domain, "keyword"
    return "Unknown", "none"


def week_of(day, start_date):
    return (day - start_date).days // 7 + 1


# ============================================================
# 1. SOLUTION FILES -> TASK BATCH AND PLACEMENTS
# ============================================================

def load_solution(folder, person_id):
    path = Path(folder) / f"{person_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def task_batch_from_solution(solution, catalog, start_date):
    """
    The recommended tasks of one person: one per (task slug, week), with
    duration_min, intensity and flags, as calendar-bench generated them.
    """
    batch = {}
    for item in solution.get("scheduled", []) + solution.get("unscheduled", []):
        day = date.fromisoformat(item["date"]) if item.get("date") else None
        slug = item.get("parent_task_label") or item["label"]
        week = week_of(day, start_date) if day else item.get("week")
        key = (slug, week)
        if key in batch:
            continue
        entry = catalog.get(slug)
        domain, domain_source = domain_of(slug, entry)
        batch[key] = {
            "slug": slug, "week": week,
            "display_name": item.get("display_name") or slug,
            "duration_min": item.get("duration_min") or 10,
            "intensity": item.get("intensity") or 1,
            "is_concurrent": bool(item.get("is_concurrent")),
            "is_dividable": bool(item.get("is_dividable")),
            "domain": domain, "domain_source": domain_source,
            "subclass": (entry or {}).get("subclass"),
            "location_links": (entry or {}).get("location_links"),
        }
    return list(batch.values())


def health_block(task, start, end, person_id, persona_id, index, method):
    """A health task placement as a planned-task dict for the simulation."""
    return {
        "uid": f"health-{method}-{index:04d}",
        "summary": f"{task['display_name']} (Person {person_id})",
        "description": f"Health task {task['slug']} (week {task['week']}, {method})",
        "start": start, "end": end,
        "duration_hours": (end - start).total_seconds() / 3600,
        "status": "", "all_day": False,
        "person_id": person_id, "persona": persona_id,
        "label": task["display_name"], "event": "health_task",
        "in_catalog": False, "is_marker": False, "category": "health",
        "is_concurrent": task["is_concurrent"], "is_dividable": task["is_dividable"],
        "intensity": task["intensity"], "time_window": None,
        "force_eligible": True,
        "health_slug": task["slug"], "health_week": task["week"],
        "health_group": f"{task['slug']}|w{task['week']}",
        "health_domain": task["domain"], "health_subclass": task["subclass"],
        "location_links": task["location_links"],
    }


def placements_from_solution(solution, batch, person_id, persona_id, method,
                             start_date):
    """
    Health blocks exactly as the solution file placed them. Pieces of a
    divided task share the task's (slug, week) group.
    """
    by_key = {(t["slug"], t["week"]): t for t in batch}
    blocks = []
    for i, item in enumerate(solution.get("scheduled", [])):
        day = date.fromisoformat(item["date"])
        midnight = datetime.combine(day, datetime.min.time())
        start = midnight + timedelta(minutes=item["start_minutes"])
        end = midnight + timedelta(minutes=item["end_minutes"])
        if end <= start:
            continue
        slug = item.get("parent_task_label") or item["label"]
        task = by_key.get((slug, week_of(day, start_date)))
        if task is None:      # task of another person's batch: keep it as is
            task = task_batch_from_solution({"scheduled": [item]}, {}, start_date)[0]
        blocks.append(health_block(task, start, end, person_id, persona_id, i, method))
    return blocks


# ============================================================
# 2. BUILT-IN PLANNING METHODS
# ============================================================

class FreeTime:
    """Busy intervals per day of the base calendar, for placing tasks."""

    def __init__(self, base_tasks, daily_window, step_minutes):
        self.busy = {}
        self.wake = daily_window.get("wake_minutes", 360)
        self.sleep = daily_window.get("sleep_minutes", 1320)
        self.step = step_minutes or 10
        for t in base_tasks:
            if t.get("is_marker") or t.get("is_concurrent"):
                continue
            self.add(t["start"], t["end"])

    def add(self, start, end):
        day = start.date()
        while day <= (end - timedelta(microseconds=1)).date():
            self.busy.setdefault(day, []).append((start, end))
            day += timedelta(days=1)

    def is_free(self, start, end):
        return all(not (s < end and start < e)
                   for s, e in self.busy.get(start.date(), []))

    def gaps(self, day):
        """Free [start, end) intervals inside the waking window."""
        midnight = datetime.combine(day, datetime.min.time())
        lo = midnight + timedelta(minutes=self.wake)
        hi = midnight + timedelta(minutes=self.sleep)
        out, cursor = [], lo
        for s, e in sorted(self.busy.get(day, [])):
            if e <= cursor or s >= hi:
                continue
            if s > cursor:
                out.append((cursor, min(s, hi)))
            cursor = max(cursor, e)
        if cursor < hi:
            out.append((cursor, hi))
        return out

    def candidate_starts(self, day, minutes):
        midnight = datetime.combine(day, datetime.min.time())
        dur = timedelta(minutes=minutes)
        t = midnight + timedelta(minutes=self.wake)
        last = midnight + timedelta(minutes=self.sleep) - dur
        while t <= last:
            if self.is_free(t, t + dur):
                yield t
            t += timedelta(minutes=self.step)


def _week_days(start_date, week):
    first = start_date + timedelta(days=7 * (week - 1))
    return [first + timedelta(days=i) for i in range(7)]


def plan_fcfs_greedy(batch, free, start_date, rng):
    """calendar-bench's documented FCFS greedy, re-implemented (see module doc)."""
    used_gaps = set()
    placed, unscheduled = [], []
    for task in batch:
        dur = timedelta(minutes=task["duration_min"])
        choice = None
        fallback = []
        for day in _week_days(start_date, task["week"]):
            for gap in free.gaps(day):
                if gap[1] - gap[0] < dur:
                    continue
                if (day, gap[0]) not in used_gaps:
                    choice = gap[0]
                    used_gaps.add((day, gap[0]))
                    break
                fallback.append(gap[0])
            if choice:
                break
        if choice is None and fallback:
            earliest = min(fallback)
            ties = [f for f in fallback if f == earliest]
            choice = rng.choice(ties)
        if choice is None:
            unscheduled.append(task)
            continue
        free.add(choice, choice + dur)
        placed.append((task, choice, choice + dur))
    return placed, unscheduled


def plan_random(batch, free, start_date, rng):
    placed, unscheduled = [], []
    for task in batch:
        dur = timedelta(minutes=task["duration_min"])
        options = [s for d in _week_days(start_date, task["week"])
                   for s in free.candidate_starts(d, task["duration_min"])]
        if not options:
            unscheduled.append(task)
            continue
        start = rng.choice(options)
        free.add(start, start + dur)
        placed.append((task, start, start + dur))
    return placed, unscheduled


def plan_context_aware(batch, free, start_date, rng, context_by_day, params,
                       persona, centre, base_tasks, day_penalty=0.02):
    """Free slot in the task's week with the highest predicted p(no override)."""
    traits = persona_traits(persona, "mean")
    placed, unscheduled = [], []
    per_day = {}
    # Planned hours left in the day (the v1 `fill` covariate), from the base
    # calendar plus the health tasks placed so far.
    from override_simulation import ExecutedCalendar, remaining_planned_hours
    plan = ExecutedCalendar(base_tasks, [])
    for task in batch:
        dur = timedelta(minutes=task["duration_min"])
        probe = {"event": "health_task", "health_subclass": task["subclass"],
                 "location_links": task["location_links"]}
        best, best_score = None, None
        for day in _week_days(start_date, task["week"]):
            for start in free.candidate_starts(day, task["duration_min"]):
                ctx = active_contexts(context_by_day, start)
                x = context_covariates(probe, ctx, params)
                fill = remaining_planned_hours(plan, start)
                p, _ = action_probabilities(params, fill, 0, 0, x, traits,
                                            centre, task["intensity"])
                score = p[NO_OVERRIDE] - day_penalty * per_day.get(day, 0)
                if best_score is None or score > best_score + 1e-12:
                    best, best_score = start, score
        if best is None:
            unscheduled.append(task)
            continue
        free.add(best, best + dur)
        plan.add({"kind": "task", "start": best, "end": best + dur,
                  "category": "health", "is_concurrent": False,
                  "is_marker": False})
        per_day[best.date()] = per_day.get(best.date(), 0) + 1
        placed.append((task, best, best + dur))
    return placed, unscheduled


def context_by_day_of(context_events):
    out = {}
    for item in context_events:
        ctx = {"context_category": item["context_category"],
               "event": item["context_value"],
               "start": item["start"], "end": item["end"]}
        day = item["start"].date()
        while day <= (item["end"] - timedelta(microseconds=1)).date():
            out.setdefault(day, []).append(ctx)
            day += timedelta(days=1)
    return out


def build_method(name, batch, setup, params, persona_settings, seed):
    """Health blocks + unscheduled tasks for a built-in planning method."""
    exp = setup["experiment"]
    start_date = setup["horizon"][0].date()
    free = FreeTime(setup["tasks"], exp["daily_window"], exp.get("step_minutes"))
    rng = random.Random(f"{name}-{seed}")
    if name == "fcfs_greedy_v2":
        placed, unscheduled = plan_fcfs_greedy(batch, free, start_date, rng)
    elif name == "random_slot_v2":
        placed, unscheduled = plan_random(batch, free, start_date, rng)
    elif name == "context_aware_v2":
        placed, unscheduled = plan_context_aware(
            batch, free, start_date, rng, context_by_day_of(setup["context_events"]),
            params, setup["persona"], persona_settings.get("centre", 0.5),
            setup["tasks"])
    else:
        raise ValueError(f"Unknown built-in planning method '{name}'")
    blocks = [health_block(t, s, e, setup["person_id"], setup["persona_id"], i, name)
              for i, (t, s, e) in enumerate(placed)]
    return blocks, unscheduled
