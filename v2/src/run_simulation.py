"""
Run the v2 override simulation on one planned calendar.

    python v2/src/run_simulation.py [path/to/calendar.ics] [--config ...] [--replications N]

Writes to output.dir of the config (default v2/output/):
  <calendar>_v2_simulation.xlsx      KPI summary, replications, changes,
                                     decisions, tasks, parameters, traits
  <calendar>_v2_executed_run1.ics    executed calendar of replication 1
  <calendar>_v2_calendar_bench/      plan + executed run(s) as calendar-bench JSON
"""

import argparse
import sys
from pathlib import Path

from common import (
    load_setup, triggers_of, summarise, write_workbook, write_executed_ics,
    write_cb_json,
)
from model_v2 import DEFAULT_CONFIG, intercepts, load_config
from simulation_v2 import run_replication, replication_kpis


def parameter_rows(params, settings):
    rows = [("postpone_window", str(params.get("postpone_window"))),
            ("trait_source", settings["trait_source"]),
            ("trait centre", settings["centre"])]
    for action, p in params["base_probabilities"].items():
        rows.append((f"base probability {action}", p))
    for action, b0 in intercepts(params).items():
        rows.append((f"intercept beta0 {action}", b0))
    for group in ("coefficients", "context_coefficients", "trait_coefficients"):
        for action, coefs in (params.get(group) or {}).items():
            for name, value in coefs.items():
                rows.append((f"{group} {action} {name}", value))
    for name, value in (params.get("intensity_slope") or {}).items():
        rows.append((f"intensity_slope {name}", value))
    for key in ("notification_share", "max_postpones_per_task",
                "postpone_respect_weekdays",
                "check_temporal_rules", "earlier_overrides_window",
                "earlier_overrides_cap"):
        rows.append((key, params.get(key)))
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description="v2 override simulation")
    parser.add_argument("ics_file", nargs="?", type=Path, default=None)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--replications", type=int, default=None)
    args = parser.parse_args(argv)

    config = load_config(args.config)
    ics_file = args.ics_file or config.get("default_calendar")
    if ics_file is None or not Path(ics_file).exists():
        sys.exit(f"Calendar not found: {ics_file}. Pass a .ics path.")
    setup = load_setup(config, ics_file)
    triggers = triggers_of(config)
    reps = args.replications or config["replications"]["count"]
    base_seed = config["replications"]["base_seed"]
    print(f"Calendar: {ics_file}")
    print(f"Persona: {setup['persona_id']} (parameters: {setup['params_source']})")
    print(f"Tasks: {len(setup['tasks'])}, context episodes: {len(setup['context_events'])}")

    results, per_rep = [], []
    for r in range(reps):
        res = run_replication(
            setup["tasks"], setup["context_events"], setup["experiment"],
            setup["params"], setup["rules"], setup["horizon"], triggers,
            base_seed + r, setup["persona"], config["persona"])
        results.append(res)
        per_rep.append(replication_kpis(res))
        print(f"  replication {r + 1}/{reps}: {len(res['changes'])} overrides, "
              f"completion {per_rep[-1]['Completion rate (eligible tasks)']:.3f}")

    summary = summarise(per_rep)
    out_dir = Path(config["output"]["dir"])
    stem = Path(ics_file).stem
    first = results[0]
    names = [row[0] for row in summary]
    outcomes = {o["uid"]: o for o in first["outcomes"]}
    sheets = [
        ("KPI summary", ["KPI", "Mean", "Std. dev.", "95% CI low", "95% CI high", "N"], summary),
        ("Replications", ["Replication", "Seed"] + names,
         [[i + 1, res["seed"]] + [k.get(n) for n in names]
          for i, (res, k) in enumerate(zip(results, per_rep))]),
        ("Changes", ["Replication", "Time", "Trigger", "Task", "Event", "Drawn",
                     "Applied", "Planned start", "Planned end", "Affected h",
                     "New start", "New end", "Delay h", "Days moved",
                     "Replacement", "Active context", "p none", "p postpone",
                     "p skip", "p replace", "Note"],
         [[i + 1, c["time"], c["trigger"], c["label"], c["event"],
           c["drawn_action"], c["action"], c["planned_start"], c["planned_end"],
           c["affected_hours"], c["new_start"], c["new_end"], c["delay_hours"],
           c["days_moved"], c["replacement"], c["active_context_covariates"],
           c["p_none"], c["p_postpone"], c["p_skip"], c["p_replace"], c["note"]]
          for i, res in enumerate(results) for c in res["changes"]]),
        ("Decisions (run 1)", ["Time", "Trigger", "Outcome", "Task",
                               "Active context", "eta context (postpone)",
                               "eta persona (postpone)", "p none", "p postpone",
                               "p skip", "p replace"],
         [[d["time"], d["trigger"], d["outcome"], d.get("task"),
           d.get("active_context_covariates"), d.get("eta_context_postpone"),
           d.get("eta_persona_postpone"), d.get("p_none"), d.get("p_postpone"),
           d.get("p_skip"), d.get("p_replace")] for d in first["decisions"]]),
        ("Tasks (run 1)", ["UID", "Label", "Event", "Start", "End", "Planned h",
                           "Executed h", "Eligible", "Notified", "Completed",
                           "Actions", "Deviation h"],
         [[t["uid"], t["label"], t["event"], t["start"], t["end"],
           outcomes[t["uid"]]["planned_hours"], outcomes[t["uid"]]["executed_hours"],
           outcomes[t["uid"]]["eligible"], outcomes[t["uid"]]["notified"],
           outcomes[t["uid"]]["completed"], outcomes[t["uid"]]["actions"],
           outcomes[t["uid"]]["deviation_hours"]] for t in setup["tasks"]]),
        ("Persona traits", ["Replication", "Trait", "Value"],
         [[i + 1, t, v] for i, res in enumerate(results)
          for t, v in res["traits"].items()]),
        ("Parameters", ["Parameter", "Value"],
         parameter_rows(setup["params"], config["persona"])),
    ]
    xlsx = write_workbook(out_dir / f"{stem}_v2_simulation.xlsx", sheets)
    written = [xlsx]
    n_ics = min(config["output"]["executed_ics_replications"], reps)
    for r in range(n_ics):
        written.append(write_executed_ics(
            results[r], setup["context_events"],
            out_dir / f"{stem}_v2_executed_run{r + 1}.ics", r + 1))
    if config["output"].get("calendar_bench_json"):
        jdir = out_dir / f"{stem}_v2_calendar_bench"
        pid = setup["person_id"]
        written.append(write_cb_json(setup["tasks"], setup, jdir / "plan" / f"{pid}.json"))
        for r in range(n_ics):
            written.append(write_cb_json(results[r]["calendar"].blocks, setup,
                                         jdir / f"executed_run{r + 1}" / f"{pid}.json"))

    print("\nFiles written:")
    for p in written:
        print(f"  {Path(p).resolve()}")
    print(f"\nKPIs over {reps} replications (mean [95% CI]):")
    for name, mean, sd, low, high, n in summary:
        if mean is None:
            print(f"  {name}: n/a")
        elif low is None:
            print(f"  {name}: {mean:.4g}")
        else:
            print(f"  {name}: {mean:.4g} [{low:.4g}, {high:.4g}]")


if __name__ == "__main__":
    main()
