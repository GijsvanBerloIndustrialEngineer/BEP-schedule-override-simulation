"""
Run the v3 simulation (review + execution + progress) on one planned calendar.

    python v3/src/run_simulation.py [path/to/calendar.ics] [--config ...] [--replications N]

Writes to v3/output/:
  <calendar>_v3_simulation.xlsx    KPI summary, execution states, replications,
                                   decisions (review and start), changes, tasks
  <calendar>_v3_executed_run1.ics  executed calendar of replication 1
  <calendar>_v3_calendar_bench/    plan + executed run as calendar-bench JSON
"""

import argparse
import sys
from pathlib import Path

from model_v3 import DEFAULT_CONFIG, load_config
from simulation_v3 import run_replication, replication_kpis, STATES

from common import load_setup, summarise, write_workbook, write_executed_ics, write_cb_json  # v2


def run(config, setup, reps, tasks=None, extra=None):
    """R replications; returns results and per-replication KPIs."""
    base_seed = config["replications"]["base_seed"]
    results, per_rep = [], []
    for r in range(reps):
        res = run_replication(tasks or setup["tasks"], setup["context_events"],
                              setup["experiment"], setup["params"], setup["rules"],
                              setup["horizon"], config, base_seed + r, setup["persona"],
                              config["persona"])
        k = replication_kpis(res)
        if extra:
            k.update(extra(res))
        results.append(res)
        per_rep.append(k)
    return results, per_rep


def main(argv=None):
    ap = argparse.ArgumentParser(description="v3 two-stage execution simulation")
    ap.add_argument("ics_file", nargs="?", type=Path, default=None)
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--replications", type=int, default=None)
    args = ap.parse_args(argv)

    config = load_config(args.config)
    ics = args.ics_file or config.get("default_calendar")
    if ics is None or not Path(ics).exists():
        sys.exit(f"Calendar not found: {ics}. Pass a .ics path.")
    setup = load_setup(config, ics)
    reps = args.replications or config["replications"]["count"]
    print(f"Calendar: {ics}\nPersona: {setup['persona_id']}; {len(setup['tasks'])} tasks")

    results, per_rep = run(config, setup, reps)
    for i, k in enumerate(per_rep):
        print(f"  replication {i + 1}/{reps}: completion {k['Completion rate (eligible tasks)']:.3f}")
    summary = summarise(per_rep)

    out = Path(config["output"]["dir"]); stem = Path(ics).stem
    names = [r[0] for r in summary]
    first = results[0]
    sheets = [
        ("KPI summary", ["KPI", "Mean", "Std. dev.", "95% CI low", "95% CI high", "N"], summary),
        ("Replications", ["Replication", "Seed"] + names,
         [[i + 1, res["seed"]] + [k.get(n) for n in names] for i, (res, k) in enumerate(zip(results, per_rep))]),
        ("Decisions (run 1)", ["Time", "Stage", "Task", "Outcome", "Day load", "Fill",
                               "Active context", "p keep", "p move", "p drop", "p none",
                               "p postpone", "p skip", "p replace", "p finish", "Replacement"],
         [[d["time"], d["stage"], d["task"], d["outcome"], d.get("day_load"), d.get("fill_hours"),
           d.get("active_context"), d.get("p_keep"), d.get("p_move"), d.get("p_drop"),
           d.get("p_none"), d.get("p_postpone"), d.get("p_skip"), d.get("p_replace"),
           d.get("p_finish"), d.get("replacement")] for d in first["decisions"]]),
        ("Changes", ["Replication", "Time", "Stage", "Action", "Task", "Planned start",
                     "Planned end", "New start", "New end", "Delay h", "Days moved"],
         [[i + 1, c["time"], c["stage"], c["action"], c["label"], c["planned_start"],
           c["planned_end"], c["new_start"], c["new_end"], c["delay_hours"], c["days_moved"]]
          for i, res in enumerate(results) for c in res["changes"]]),
        ("Tasks (run 1)", ["UID", "Label", "Event", "Planned h", "Executed h", "Eligible",
                           "State", "Moved at review", "Postponed at start", "Deviation h"],
         [[o["uid"], o["label"], o["event"], o["planned_hours"], o["executed_hours"],
           o["eligible"], o["state"], o["moved_at_review"], o["postponed_at_start"],
           o["deviation_hours"]] for o in first["outcomes"]]),
    ]
    written = [write_workbook(out / f"{stem}_v3_simulation.xlsx", sheets)]
    written.append(write_executed_ics(first, setup["context_events"], out / f"{stem}_v3_executed_run1.ics", 1))
    if config["output"].get("calendar_bench_json"):
        jdir = out / f"{stem}_v3_calendar_bench"; pid = setup["person_id"]
        written.append(write_cb_json(setup["tasks"], setup, jdir / "plan" / f"{pid}.json"))
        written.append(write_cb_json(first["calendar"].blocks, setup, jdir / "executed_run1" / f"{pid}.json"))
    print("\nFiles written:")
    for p in written:
        print(f"  {Path(p).resolve()}")
    print(f"\nKPIs over {reps} replications (mean [95% CI]):")
    for name, mean, sd, lo, hi, n in summary:
        if mean is None:
            print(f"  {name}: n/a")
        elif lo is None:
            print(f"  {name}: {mean:.4g}")
        else:
            print(f"  {name}: {mean:.4g} [{lo:.4g}, {hi:.4g}]")


if __name__ == "__main__":
    main()
