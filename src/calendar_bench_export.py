"""
Export a calendar (the plan or an executed calendar) as a calendar-bench
per-person JSON file, the format calendar-bench's own validation reads
(src/scripts/persona/export/json_writer.py in calendar-bench).

Layout of the file:

    {
      "person_id": "...", "persona_id": "...", "person_seed": 0,
      "days": [
        {"day_index": 0, "date": "2026-07-06", "weekday": "Mon",
         "events": {"office_work": [{"start": 510, "duration": 120,
                                      "label": "writing"}], ...},
         "spillovers": [{"type": "sleep", "start": 0, "duration": 390,
                         "orig_start": 1350, "orig_duration": 480,
                         "event_idx": 0}]},
        ...
      ],
      "contexts": [{"name": "tired", "category": "energy_state",
                    "date": "2026-07-06", "start_minutes": 0,
                    "end_minutes": 120, ...}]
    }

- Events are keyed by their catalog name (event_config.yaml); the label the
  calendar shows is kept in "label" when it differs from the name.
- start and duration are minutes; an event that crosses midnight stays on
  its start day and gets a spillover entry on the next day, exactly as
  calendar-bench does.
- wake_up / go_to_bed are left out (calendar-bench derives them from sleep).
- UNPLANNED blocks are left out: they are not catalog events.
- person_seed is not stored in the .ics; it is written as 0 and filled in
  by tools/validate_with_calendar_bench.py from the sampled population.

This module has no dependency on calendar-bench itself.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

DAY_MINUTES = 24 * 60
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _minutes_from(day_start, moment):
    return int(round((moment - day_start).total_seconds() / 60))


def to_calendar_bench_dict(blocks, context_events, horizon, person_id,
                           persona_id):
    """
    blocks         : planned tasks or executed blocks (dicts with kind,
                     event, label, start, end, is_marker)
    context_events : [ctx:...] events from load_calendar()
    horizon        : (start, end) datetimes of the experiment
    """
    start, end = horizon
    first_day = start.date()
    n_days = (end.date() - first_day).days

    days = []
    for index in range(n_days):
        date = first_day + timedelta(days=index)
        days.append({
            "day_index": index,
            "date": date.isoformat(),
            "weekday": WEEKDAYS[date.weekday()],
            "events": {},
            "spillovers": [],
        })

    usable = [
        b for b in blocks
        if b.get("kind", "task") == "task"
        and not b.get("is_marker")
        and b["end"] > b["start"]
    ]
    usable.sort(key=lambda b: b["start"])

    for block in usable:
        index = (block["start"].date() - first_day).days
        if not 0 <= index < n_days:
            continue
        day_start = datetime.combine(block["start"].date(), datetime.min.time())
        entry = {
            "start": _minutes_from(day_start, block["start"]),
            "duration": _minutes_from(block["start"], block["end"]),
        }
        if block.get("label") and block["label"] != block["event"]:
            entry["label"] = block["label"]
        days[index]["events"].setdefault(block["event"], []).append(entry)

    # Spillovers: the part of an event past midnight, listed on the next day
    for index in range(n_days - 1):
        for name, events in days[index]["events"].items():
            for event_idx, event in enumerate(events):
                overflow = event["start"] + event["duration"] - DAY_MINUTES
                if overflow > 0:
                    days[index + 1]["spillovers"].append({
                        "type": name,
                        "start": 0,
                        "duration": overflow,
                        "orig_start": event["start"],
                        "orig_duration": event["duration"],
                        "event_idx": event_idx,
                    })

    contexts = []
    for item in context_events:
        day_start = datetime.combine(item["start"].date(), datetime.min.time())
        contexts.append({
            "name": item["context_value"],
            "category": item["context_category"],
            "date": item["start"].date().isoformat(),
            "start_minutes": _minutes_from(day_start, item["start"]),
            "end_minutes": _minutes_from(day_start, item["end"]),
            "ontology_uri": None,
            "dimension": None,
            "polarity": None,
            "instrument": None,
            "theory_mappings": None,
        })

    return {
        "person_id": person_id,
        "persona_id": persona_id,
        "person_seed": 0,
        "days": days,
        "contexts": contexts,
    }


def write_calendar_bench_json(blocks, context_events, horizon, person_id,
                              persona_id, output_path):
    payload = to_calendar_bench_dict(
        blocks, context_events, horizon, person_id, persona_id
    )
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return output_path
