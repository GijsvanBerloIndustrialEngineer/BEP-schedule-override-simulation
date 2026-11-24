"""
Health tasks of the calendar-bench healthy_lifestyle_promotion scenario.

The placements come from calendar-bench solution files (<person_id>.json
with a "scheduled" list). The human coach schedules are published in
calendar-bench. Comparing planning methods is left to calendar-bench itself.
"""

import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path

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
