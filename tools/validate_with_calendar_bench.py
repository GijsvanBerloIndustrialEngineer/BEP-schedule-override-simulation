"""
Score the plan and the executed calendars with calendar-bench's own
per-person validation, and compare them.

calendar-bench is NOT changed: the script imports its validation code from a
local checkout (read-only) and runs it on the JSON files that
src/simulation.py writes to <calendar>_calendar_bench/.

Usage (run with a Python that has calendar-bench's packages installed:
pyyaml, pydantic>=2, z3-solver, icalendar, numpy, scipy):

    python tools/validate_with_calendar_bench.py \
        --calendar-bench path/to/calendar-bench \
        path/to/<calendar>_calendar_bench

Why not calendar-bench's `persona validate` command:
- its loader drops the context episodes when it reads JSON back, so the
  context rules (e.g. no_office_when_tired) would never fire;
- it pairs files with sampled persons by list position, which only works
  for a full population;
- its load_config() connects to Neo4j for experiments with contexts.
This script calls the same check functions directly instead.

Checks used (per person): persona stage cadence, event constraints
(per-event duration, per-day totals and episodes, weekdays), LTL rules
from temporal_relation_rules.yaml (with contexts) and day-to-day
continuity. Population-level checks (instance counts, characteristic and
context distributions) need all persons and are skipped.
"""

import argparse
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from calendar_bench_link import DEFAULT_OVERRIDE_CONFIG, load_override_config  # noqa: E402

STREAMS = ("persona", "event", "ltl", "continuity")


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "inputs", nargs="+", type=Path,
        help="<calendar>_calendar_bench folder(s) or person JSON file(s)",
    )
    parser.add_argument(
        "--calendar-bench", required=True, type=Path,
        help="local checkout of calendar-bench (read-only)",
    )
    parser.add_argument(
        "--config", type=Path, default=DEFAULT_OVERRIDE_CONFIG,
        help="override_config.yaml (for experiment_dir)",
    )
    parser.add_argument(
        "--out", type=Path, default=None,
        help="folder for the report (default: next to the first input)",
    )
    return parser.parse_args(argv)


def collect_inputs(paths):
    """{run name: JSON file}. A folder holds plan/ and executed_runN/."""
    found = {}
    for path in paths:
        if path.is_file():
            found[path.parent.name] = path
            continue
        for sub in sorted(p for p in path.iterdir() if p.is_dir()):
            files = sorted(sub.glob("*.json"))
            if files:
                found[sub.name] = files[0]
    if "plan" in found:          # plan first, then the runs
        found = {"plan": found.pop("plan"), **found}
    return found


def load_calendar_bench(cb_root, experiment_dir):
    sys.path.insert(0, str(cb_root))
    from src.scripts.persona.config.loader import (
        load_environment, load_persona, load_event, load_rules,
    )
    from src.scripts.persona.domain.event import Catalog
    from src.scripts.persona.sampling.persona_sampler import sample_population
    from src.scripts.persona.validation.parallel import _per_person_task
    from src.scripts.persona.validation.loader import schedule_from_dict
    from src.scripts.persona.domain.schedule import PersonSchedule
    from src.scripts.persona.context.schema import ContextEpisode

    environment = load_environment(experiment_dir / "environment.yaml")
    persona_cfg = load_persona(experiment_dir / "persona_config.yaml")
    event_cfg = load_event(experiment_dir / "event_config.yaml")
    rules = load_rules(experiment_dir / "temporal_relation_rules.yaml")

    return {
        "environment": environment,
        "catalog": Catalog.from_event_config(event_cfg),
        "rules": rules.rules,
        "persons": {
            p.person_id: p
            for p in sample_population(persona_cfg, environment.seed)
        },
        "check": _per_person_task,
        "schedule_from_dict": schedule_from_dict,
        "PersonSchedule": PersonSchedule,
        "ContextEpisode": ContextEpisode,
    }


def build_schedule(cb, payload, person):
    base = cb["schedule_from_dict"](payload)
    contexts = [
        cb["ContextEpisode"](
            name=c["name"],
            category=c["category"],
            date=dt.date.fromisoformat(c["date"]),
            start_minutes=int(c["start_minutes"]),
            end_minutes=int(c["end_minutes"]),
        )
        for c in payload.get("contexts", [])
    ]
    return cb["PersonSchedule"](
        person_id=base.person_id,
        persona_id=person.persona_id,
        person_seed=person.person_seed,
        days=base.days,
        contexts=contexts,
    )


def validate_file(cb, path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    person_id = payload["person_id"]
    person = cb["persons"].get(person_id)
    if person is None:
        raise ValueError(
            f"{path}: person {person_id!r} is not in the sampled population "
            "of this experiment"
        )
    schedule = build_schedule(cb, payload, person)
    result = cb["check"](
        person, schedule, cb["catalog"], cb["rules"],
        cb["environment"].horizon.start_date,
    )
    return {stream: list(getattr(result, stream)) for stream in STREAMS}


def summarise(violations):
    summary = {"total": sum(len(v) for v in violations.values())}
    for stream in STREAMS:
        summary[stream] = len(violations[stream])
    summary["event_by_kind"] = Counter(
        f"{v.event_name} / {v.kind}" for v in violations["event"]
    )
    summary["ltl_by_rule"] = Counter(v.rule_id for v in violations["ltl"])
    summary["continuity_by_kind"] = Counter(v.kind for v in violations["continuity"])
    summary["persona_by_kind"] = Counter(
        getattr(v, "kind", type(v).__name__) for v in violations["persona"]
    )
    return summary


def _table(rows, header):
    lines = ["| " + " | ".join(header) + " |",
             "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def write_report(summaries, details, out_dir, person_id):
    out_dir.mkdir(parents=True, exist_ok=True)
    names = list(summaries)
    plan = summaries.get("plan")

    lines = [
        f"# calendar-bench validation: {person_id}",
        "",
        "Per-person checks of calendar-bench (stage cadence, event "
        "constraints, LTL rules with contexts, continuity) on the plan and "
        "the executed calendars. Population-level checks are skipped.",
        "",
        "## Violations per check",
        "",
    ]
    header = ["Check"] + names + (
        [f"Δ {n} − plan" for n in names if n != "plan"] if plan else []
    )
    rows = []
    for key in ("total",) + STREAMS:
        row = [key] + [summaries[n][key] for n in names]
        if plan:
            row += [summaries[n][key] - plan[key] for n in names if n != "plan"]
        rows.append(row)
    lines += [_table(rows, header), ""]

    for title, field in (
        ("Event constraints (event / kind)", "event_by_kind"),
        ("LTL rules", "ltl_by_rule"),
        ("Continuity", "continuity_by_kind"),
        ("Persona", "persona_by_kind"),
    ):
        keys = sorted(set().union(*(summaries[n][field] for n in names)))
        if not keys:
            continue
        rows = []
        for key in keys:
            row = [key] + [summaries[n][field].get(key, 0) for n in names]
            if plan:
                row += [summaries[n][field].get(key, 0) - plan[field].get(key, 0)
                        for n in names if n != "plan"]
            rows.append(row)
        lines += [f"## {title}", "", _table(rows, ["Item"] + header[1:]), ""]

    report_md = out_dir / "validation_report.md"
    report_md.write_text("\n".join(lines), encoding="utf-8")

    report_json = out_dir / "validation_report.json"
    report_json.write_text(json.dumps({
        "person_id": person_id,
        "summaries": {
            n: {k: (dict(v) if isinstance(v, Counter) else v)
                for k, v in s.items()}
            for n, s in summaries.items()
        },
        "violations": {
            n: {stream: [
                {k: getattr(v, k) for k in v.__slots__} if hasattr(v, "__slots__")
                else str(v)
                for v in vs
            ] for stream, vs in d.items()}
            for n, d in details.items()
        },
    }, indent=2, default=str), encoding="utf-8")
    return report_md, report_json


def main(argv=None):
    args = parse_arguments(argv)
    config = load_override_config(args.config)
    cb = load_calendar_bench(args.calendar_bench.resolve(),
                             Path(config["experiment_dir"]))

    inputs = collect_inputs(args.inputs)
    if not inputs:
        raise ValueError("No calendar-bench JSON files found in the inputs.")

    summaries, details, person_ids = {}, {}, set()
    for name, path in inputs.items():
        violations = validate_file(cb, path)
        details[name] = violations
        summaries[name] = summarise(violations)
        person_ids.add(json.loads(path.read_text(encoding="utf-8"))["person_id"])
        print(f"{name}: {summaries[name]['total']} violations "
              + ", ".join(f"{s} {summaries[name][s]}" for s in STREAMS))

    out_dir = args.out or args.inputs[0]
    if out_dir.is_file():
        out_dir = out_dir.parent
    md, js = write_report(summaries, details, out_dir, ", ".join(sorted(person_ids)))
    print(f"\nReport: {md.resolve()}\nDetails: {js.resolve()}")


if __name__ == "__main__":
    main()
