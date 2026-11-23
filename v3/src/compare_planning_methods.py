"""
Health scenario with the v3 model: the same planning methods as v2, now
reporting the execution state of every health task (completed, partial,
rejected at review, missed, replaced).

    python v3/src/compare_planning_methods.py [calendar.ics] [--replications N]
    python v3/src/compare_planning_methods.py --solutions ptime=path/to/persons

Output: v3/output/<calendar>_v3_planning_methods.xlsx / .csv
"""

import argparse
import csv
import statistics
import sys
from pathlib import Path

from model_v3 import DEFAULT_CONFIG, load_config
from run_simulation import run
from simulation_v3 import STATES

from common import load_setup, write_workbook  # v2
from health_tasks import (  # v2
    build_method, load_catalog, load_solution, placements_from_solution,
    task_batch_from_solution,
)
from stage_ablation import mean_ci


def health_kpis_factory(blocks, batch_size):
    group = {b["uid"]: b["health_group"] for b in blocks}
    meta = {b["health_group"]: b for b in blocks}

    def kpis(res):
        per = {}
        for o in res["outcomes"]:
            g = group.get(o["uid"])
            if g is not None:
                per.setdefault(g, []).append(o["state"])
        # a task is completed only if all its pieces are; otherwise it takes
        # the "worst" state of its pieces in this order
        rank = ["rejected", "missed", "replaced", "partial", "completed"]
        state = {g: min(v, key=rank.index) for g, v in per.items()}
        n = len(state)
        out = {f"Health {s}": (sum(1 for x in state.values() if x == s) / batch_size)
               for s in STATES}
        out["Health completion (whole batch)"] = out["Health completed"]
        for d in ("PhysicalActivity", "Nutrition", "MentalWellbeing"):
            sel = [g for g in state if meta[g]["health_domain"] == d]
            out[f"Health completion: {d}"] = (sum(state[g] == "completed" for g in sel) / len(sel)) if sel else None
        out["Health tasks placed"] = n
        return out
    return kpis


def main(argv=None):
    ap = argparse.ArgumentParser(description="v3 planning-method comparison")
    ap.add_argument("ics_file", nargs="?", type=Path, default=None)
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--replications", type=int, default=None)
    ap.add_argument("--solutions", nargs="*", default=[])
    args = ap.parse_args(argv)
    config = load_config(args.config)
    ics = args.ics_file or config["default_calendar"]
    setup = load_setup(config, ics)
    hs = config["health_scenario"]
    sources = dict(hs["solutions"])
    for item in args.solutions:
        n, _, folder = item.partition("=")
        sources[n] = Path(folder).resolve()
    catalog = load_catalog(hs.get("health_task_catalog"))
    start = setup["horizon"][0].date(); pid = setup["person_id"]

    plans, batch = {}, None
    for name, folder in sources.items():
        sol = load_solution(folder, pid)
        if sol is None:
            print(f"  {name}: no solution for {pid}; skipped"); continue
        own = task_batch_from_solution(sol, catalog, start)
        batch = batch or own
        plans[name] = (placements_from_solution(sol, own, pid, setup["persona_id"], name, start), len(own))
    if batch is None:
        sys.exit("No solution file found; run v2/tools/import_calendar_bench.py first.")
    batch.sort(key=lambda t: (t["week"], t["slug"]))
    for name in hs.get("builtin_methods") or []:
        blocks, _ = build_method(name, batch, setup, setup["params"], config["persona"], hs.get("seed", 0))
        plans[name] = (blocks, len(batch))

    reps = args.replications or config["replications"]["count"]
    rows, per_method = [], {}
    for name, (blocks, size) in plans.items():
        tasks = sorted(setup["tasks"] + blocks, key=lambda t: t["start"])
        _, per_rep = run(config, setup, reps, tasks=tasks, extra=health_kpis_factory(blocks, size))
        per_method[name] = per_rep
        m = mean_ci([r["Health completion (whole batch)"] for r in per_rep])
        print(f"  {name:18s} health completion {m[0]:.3f} [{m[1]:.3f}, {m[2]:.3f}]  "
              f"rejected {statistics.mean(r['Health rejected'] for r in per_rep):.3f}  "
              f"partial {statistics.mean(r['Health partial'] for r in per_rep):.3f}")
    keys = [k for k in per_method[next(iter(per_method))][0] if k.startswith("Health")]
    for name, per_rep in per_method.items():
        for k in keys:
            rows.append([name, k, *mean_ci([r[k] for r in per_rep])])
    out = Path(config["output"]["dir"]); out.mkdir(parents=True, exist_ok=True)
    stem = Path(ics).stem
    with (out / f"{stem}_v3_planning_methods.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["Method", "KPI", "Mean", "95% CI low", "95% CI high"]); w.writerows(rows)
    write_workbook(out / f"{stem}_v3_planning_methods.xlsx", [
        ("Comparison", ["Method", "KPI", "Mean", "95% CI low", "95% CI high"], rows)])
    print(f"Files written to {out.resolve()}")


if __name__ == "__main__":
    main()
