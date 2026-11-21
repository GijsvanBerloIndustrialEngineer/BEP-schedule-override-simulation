"""
Copy the inputs version 2 needs from a local calendar-bench checkout.

calendar-bench (https://github.com/MaaniBeigy/calendar-bench, MIT licence)
is only READ, never changed. This script

1. copies the human coach schedules of the healthy-lifestyle experiment
   (src/experiments/persona/healthy_lifestyle_promotion/human_coach_schedules)
   to v2/data/scenario_solutions/human_coach/, and
2. extracts, for every health task that appears in those schedules, its
   domain, sub-class, difficulty level and ontology context links from
   src/assets/ontologies/HealthTasks_*.json into
   v2/data/health_task_catalog.json.

Usage:
    python v2/tools/import_calendar_bench.py --calendar-bench path/to/calendar-bench
    python v2/tools/import_calendar_bench.py --calendar-bench ... --persons diligent_anxious_active_0000
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

V2_DIR = Path(__file__).resolve().parent.parent
EXPERIMENT = Path("src/experiments/persona/healthy_lifestyle_promotion")


def walk_ontology(node, path, out):
    """Collect {slug: entry} with path = [domain, subclass, level]."""
    if not isinstance(node, dict):
        return
    for key, value in node.items():
        if isinstance(value, dict) and "title" in value and "estimatedDuration" in value:
            out[key] = (path, value)
        elif isinstance(value, dict):
            walk_ontology(value, path + [key], out)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--calendar-bench", type=Path, required=True,
                        help="local checkout of calendar-bench (read only)")
    parser.add_argument("--persons", nargs="*", default=None,
                        help="person ids to copy (default: all 30)")
    args = parser.parse_args(argv)

    root = args.calendar_bench.resolve()
    schedules = root / EXPERIMENT / "human_coach_schedules"
    ontologies = sorted((root / "src/assets/ontologies").glob("HealthTasks_*.json"))
    if not schedules.is_dir() or not ontologies:
        sys.exit(f"Not a calendar-bench checkout: {root}")

    target = V2_DIR / "data" / "scenario_solutions" / "human_coach"
    target.mkdir(parents=True, exist_ok=True)
    files = sorted(schedules.glob("*.json"))
    if args.persons:
        files = [f for f in files if f.stem in set(args.persons)]
    slugs = set()
    for file in files:
        shutil.copy2(file, target / file.name)
        data = json.loads(file.read_text(encoding="utf-8"))
        for item in data.get("scheduled", []):
            slugs.add(item.get("parent_task_label") or item["label"])
    print(f"Copied {len(files)} human coach schedule(s) to {target}")

    ontology_file = ontologies[-1]
    entries = {}
    walk_ontology(json.loads(ontology_file.read_text(encoding="utf-8")), [], entries)
    catalog = {}
    for slug in sorted(slugs):
        if slug not in entries:
            continue
        path, entry = entries[slug]
        links = entry.get("context_links") or {}
        catalog[slug] = {
            "domain": path[0] if path else None,
            "subclass": path[1] if len(path) > 1 else None,
            "level": path[2] if len(path) > 2 else None,
            "title": entry.get("title"),
            "estimated_duration": entry.get("estimatedDuration"),
            "location_links": links.get("location", []),
            "energy_links": links.get("energy_state", []),
        }
    out = V2_DIR / "data" / "health_task_catalog.json"
    out.write_text(json.dumps({
        "source": f"calendar-bench {ontology_file.relative_to(root).as_posix()} (MIT licence)",
        "tasks": catalog,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    missing = sorted(slugs - set(catalog))
    print(f"Wrote {len(catalog)} health tasks to {out}"
          + (f" ({len(missing)} not in ontology: {missing[:5]})" if missing else ""))


if __name__ == "__main__":
    main()
