"""
Write the executed calendar as an .ics file (REPORT D12).

The file uses the same layout as the calendar-bench plan, so the two can be
opened side by side in a calendar app or compared with a script:

- planned tasks keep SUMMARY "<label> (Person <id>)" and DESCRIPTION;
- shortened, postponed and replacing blocks get an X-OVERRIDE property and
  a note in the DESCRIPTION;
- replaced parts become "UNPLANNED (Person <id>)" blocks;
- the [ctx:...] context annotations are copied unchanged.
"""

from pathlib import Path

from icalendar import Calendar, Event


def _event(summary, start, end, description, uid, categories=None,
           override=None):
    event = Event()
    event.add("uid", uid)
    event.add("summary", summary)
    event.add("dtstart", start)
    event.add("dtend", end)
    if description:
        event.add("description", description)
    if categories:
        event.add("categories", [categories])
    if override:
        event.add("x-override", override)
    return event


def write_executed_ics(result, context_events, output_path, replication):
    calendar = Calendar()
    calendar.add("prodid", "-//BEP override simulation//executed calendar//EN")
    calendar.add("version", "2.0")
    calendar.add("x-wr-calname", f"Executed calendar (replication {replication})")

    blocks = sorted(result["calendar"].blocks, key=lambda b: b["start"])
    for index, block in enumerate(blocks):
        person = block.get("person_id")
        suffix = f" (Person {person})" if person else ""
        uid = f"exec-r{replication}-{index:05d}"
        if block["kind"] == "unplanned":
            calendar.add_component(_event(
                f"UNPLANNED{suffix}", block["start"], block["end"],
                f"Unplanned activity; {block['note']}", uid,
                override="replace",
            ))
            continue
        description = block.get("description", "")
        override = None
        if block.get("note"):
            description = f"{description}; {block['note']}".lstrip("; ")
            override = "postpone" if block["note"].startswith("postponed") else (
                "interrupted"
            )
        calendar.add_component(_event(
            block["summary"], block["start"], block["end"], description, uid,
            override=override,
        ))

    for index, item in enumerate(context_events):
        calendar.add_component(_event(
            item["summary"], item["start"], item["end"], item["description"],
            f"ctx-{index:05d}", categories=item["context_category"],
        ))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(calendar.to_ical())
    return output_path
