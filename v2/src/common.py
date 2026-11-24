"""
Shared setup and output helpers for the v2 scripts.

Loading the calendar, the calendar-bench experiment and the temporal rules
is done with the unchanged v1 functions (../../src).
"""

import statistics
import sys
from datetime import datetime
from pathlib import Path

V1_SRC = Path(__file__).resolve().parents[2] / "src"
if str(V1_SRC) not in sys.path:
    sys.path.insert(0, str(V1_SRC))

from icalendar import Calendar, Event  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

from calendar_bench_link import load_experiment  # noqa: E402  (v1)
from rules import parse_rules  # noqa: E402  (v1)
from simulation import load_calendar, calendar_horizon  # noqa: E402  (v1)
from calendar_bench_export import write_calendar_bench_json  # noqa: E402  (v1)
from override_simulation import summarise_kpis, t_quantile_975  # noqa: E402  (v1)

from model_v2 import parameters_for  # noqa: E402


def mean_ci(values):
    """Mean and 95% confidence interval (t distribution) over replications."""
    values = [v for v in values if v is not None]
    if not values:
        return None, None, None
    m = statistics.mean(values)
    if len(values) < 2:
        return m, None, None
    half = t_quantile_975(len(values) - 1) * statistics.stdev(values) / len(values) ** 0.5
    return m, m - half, m + half


def load_setup(config, ics_file):
    """Everything one simulation run needs, from the config and a calendar."""
    experiment = load_experiment(config["experiment_dir"])
    rules = parse_rules(experiment["temporal_rules"])
    tasks, context_events = load_calendar(Path(ics_file), experiment)
    if not tasks:
        raise ValueError(f"No planned tasks found in {ics_file}")
    if config.get("horizon_source", "experiment") == "experiment":
        horizon = experiment["horizon"]
    else:
        horizon = calendar_horizon(tasks)
    persona_ids = sorted({t["persona"] for t in tasks if t.get("persona")})
    persona_id = persona_ids[0] if len(persona_ids) == 1 else None
    person_ids = sorted({t["person_id"] for t in tasks if t.get("person_id")})
    params, params_source = parameters_for(config, persona_id)
    return {
        "experiment": experiment, "rules": rules, "tasks": tasks,
        "context_events": context_events, "horizon": horizon,
        "persona_id": persona_id,
        "persona": experiment["personas"].get(persona_id) if persona_id else None,
        "person_id": person_ids[0] if len(person_ids) == 1 else Path(ics_file).stem,
        "params": params, "params_source": params_source,
    }


def triggers_of(config):
    return {
        "rate_per_hour": config["triggers"]["rate_per_hour"],
        "task_start": config["triggers"]["task_start"],
    }


def summarise(per_replication):
    """v1's mean / sd / 95% CI per KPI, over the union of KPI names."""
    names = []
    for kpis in per_replication:
        for name in kpis:
            if name not in names:
                names.append(name)
    filled = [{n: k.get(n, 0 if n.startswith("Replacements:") else None)
               for n in names} for k in per_replication]
    return summarise_kpis(filled)


# ============================================================
# EXCEL
# ============================================================

def write_workbook(path, sheets):
    """sheets: list of (title, header, rows)."""
    workbook = Workbook()
    first = True
    for title, header, rows in sheets:
        ws = workbook.active if first else workbook.create_sheet()
        first = False
        ws.title = title[:31]
        ws.append(list(header))
        for row in rows:
            ws.append(list(row))
    fill = PatternFill(fill_type="solid", fgColor="1F4E78")
    for ws in workbook.worksheets:
        ws.freeze_panes = "A2"
        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = fill
            cell.alignment = Alignment(horizontal="center")
        for col in ws.columns:
            width = max((len(str(c.value)) for c in col if c.value is not None),
                        default=0)
            ws.column_dimensions[get_column_letter(col[0].column)].width = min(width + 2, 45)
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                if isinstance(cell.value, datetime):
                    cell.number_format = "yyyy-mm-dd hh:mm"
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)
    return path


# ============================================================
# EXECUTED CALENDAR: .ics AND calendar-bench JSON
# ============================================================

def write_executed_ics(result, context_events, path, replication):
    """Executed calendar; replacement blocks get the activity as title."""
    cal = Calendar()
    cal.add("prodid", "-//BEP override simulation v2//executed calendar//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", f"Executed calendar v2 (replication {replication})")
    blocks = sorted(result["calendar"].blocks, key=lambda b: b["start"])
    for i, block in enumerate(blocks):
        person = block.get("person_id")
        suffix = f" (Person {person})" if person else ""
        ev = Event()
        ev.add("uid", f"exec-v2-r{replication}-{i:05d}")
        ev.add("dtstart", block["start"])
        ev.add("dtend", block["end"])
        if block["kind"] == "replacement":
            ev.add("summary", f"{block['label']} [replacement]{suffix}")
            ev.add("description", f"Replacement activity; {block['note']}")
            ev.add("x-override", "replace")
        else:
            ev.add("summary", block.get("summary") or block["label"])
            desc = block.get("description", "")
            if block.get("note"):
                desc = f"{desc}; {block['note']}".lstrip("; ")
                ev.add("x-override", "postpone"
                       if block["note"].startswith("postponed") else "interrupted")
            if desc:
                ev.add("description", desc)
        cal.add_component(ev)
    for i, item in enumerate(context_events):
        ev = Event()
        ev.add("uid", f"ctx-{i:05d}")
        ev.add("summary", item["summary"])
        ev.add("dtstart", item["start"])
        ev.add("dtend", item["end"])
        ev.add("categories", [item["context_category"]])
        cal.add_component(ev)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(cal.to_ical())
    return path


def calendar_bench_blocks(blocks):
    """
    Blocks for the calendar-bench persona JSON: planned catalog events, and
    replacement activities that are catalog events (e.g. napping). Health
    tasks and non-catalog replacements are left out.
    """
    out = []
    for b in blocks:
        if b.get("category") == "health":
            continue
        if b.get("kind") == "replacement":
            if not b.get("catalog_event"):
                continue
            b = dict(b, kind="task", event=b["catalog_event"],
                     label=b["catalog_event"])
        out.append(b)
    return out


def write_cb_json(blocks, setup, path):
    return write_calendar_bench_json(
        calendar_bench_blocks(blocks), setup["context_events"],
        setup["horizon"], setup["person_id"], setup["persona_id"] or "", path)
