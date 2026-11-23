"""
Simulate the calendar-bench health scenario (healthy_lifestyle_promotion)
and compare task completion per planning method.

For every planning method, the health tasks it placed are added to the
person's base calendar, the v2 override simulation runs R replications
(same seeds for every method: common random numbers), and the completion
of the health tasks is compared.

    python v2/src/compare_planning_methods.py [path/to/calendar.ics] [--replications N]
    python v2/src/compare_planning_methods.py --solutions ptime=path/to/ptime/persons

Methods:
  - every folder in health_scenario.solutions of the config, plus any
    --solutions name=folder (calendar-bench solution files <person_id>.json)
  - the built-in v2 methods in health_scenario.builtin_methods, which place
    the task batch of the FIRST solution source (see health_tasks.py)

Output (output.dir): <calendar>_planning_methods.xlsx / .csv / .png
"""

import argparse
import csv
import statistics
import sys
from pathlib import Path

from common import load_setup, triggers_of, write_workbook
from health_tasks import (
    build_method, load_catalog, load_solution, placements_from_solution,
    task_batch_from_solution,
)
from model_v2 import DEFAULT_CONFIG, load_config
from simulation_v2 import run_replication, replication_kpis

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from override_simulation import t_quantile_975  # noqa: E402  (v1)


def mean_ci(values):
    values = [v for v in values if v is not None]
    if not values:
        return None, None, None
    m = statistics.mean(values)
    if len(values) < 2:
        return m, None, None
    half = t_quantile_975(len(values) - 1) * statistics.stdev(values) / len(values) ** 0.5
    return m, m - half, m + half


def health_kpis(result, health_blocks, batch_size, unscheduled):
    """Completion of health tasks; a task counts when all its pieces are done."""
    group_of = {b["uid"]: b["health_group"] for b in health_blocks}
    meta = {b["health_group"]: b for b in health_blocks}
    groups = {}
    acts = {}
    for o in result["outcomes"]:
        g = group_of.get(o["uid"])
        if g is None:
            continue
        groups.setdefault(g, []).append(o["completed"])
        acts.setdefault(g, set()).update(a for a in o["actions"].split(", ") if a)
    done = {g: all(v) for g, v in groups.items()}
    n = len(done)

    def rate(pred):
        sel = [g for g in done if pred(meta[g])]
        return sum(done[g] for g in sel) / len(sel) if sel else None

    k = {
        "Health tasks placed": n,
        "Health tasks unscheduled by planner": len(unscheduled),
        "Health completion (placed tasks)": sum(done.values()) / n if n else None,
        "Health completion (whole batch)": sum(done.values()) / batch_size if batch_size else None,
        "Health share postponed": sum("postpone" in a for a in acts.values()) / n if n else None,
        "Health share skipped": sum("skip" in a for a in acts.values()) / n if n else None,
        "Health share replaced": sum("replace" in a for a in acts.values()) / n if n else None,
    }
    for domain in ("PhysicalActivity", "Nutrition", "MentalWellbeing"):
        k[f"Health completion: {domain}"] = rate(lambda b, d=domain: b["health_domain"] == d)
    k["Health completion: intensity 1"] = rate(lambda b: b["intensity"] <= 1)
    k["Health completion: intensity >= 2"] = rate(lambda b: b["intensity"] >= 2)
    base = replication_kpis(result)
    k["Base-calendar completion (eligible, incl. health)"] = base["Completion rate (eligible tasks)"]
    k["Plan-execution deviation (hours)"] = base["Plan-execution deviation (hours)"]
    return k


def plot(path, rows, methods):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    kpis = ["Health completion (whole batch)", "Health completion: PhysicalActivity",
            "Health completion: Nutrition", "Health completion: MentalWellbeing"]
    fig, ax = plt.subplots(figsize=(10, 4.8))
    width = 0.8 / len(methods)
    colors = ["#2a6f97", "#e07a5f", "#81b29a", "#9a7aa0", "#f2cc8f", "#3d405b"]
    for i, m in enumerate(methods):
        means, errs = [], [[], []]
        for kpi in kpis:
            mean, lo, hi = rows[(m, kpi)]
            means.append(mean or 0)
            errs[0].append((mean - lo) if lo is not None else 0)
            errs[1].append((hi - mean) if hi is not None else 0)
        xs = [j + (i - (len(methods) - 1) / 2) * width for j in range(len(kpis))]
        ax.bar(xs, means, width, yerr=errs, capsize=3, label=m,
               color=colors[i % len(colors)])
    ax.set_xticks(range(len(kpis)))
    ax.set_xticklabels([k.replace("Health completion", "Completion").replace(": ", "\n")
                        for k in kpis])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Share of health tasks completed")
    ax.set_title("Health-task completion per planning method (mean, 95% CI)")
    ax.legend(frameon=False, fontsize=8, ncol=len(methods))
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compare planning methods on the health scenario")
    parser.add_argument("ics_file", nargs="?", type=Path, default=None)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--replications", type=int, default=None)
    parser.add_argument("--solutions", nargs="*", default=[],
                        help="extra methods as name=folder with <person_id>.json files")
    args = parser.parse_args(argv)

    config = load_config(args.config)
    ics_file = args.ics_file or config["default_calendar"]
    setup = load_setup(config, ics_file)
    hs = config["health_scenario"]
    sources = dict(hs["solutions"])
    for item in args.solutions:
        name, _, folder = item.partition("=")
        sources[name] = Path(folder).resolve()
    catalog = load_catalog(hs.get("health_task_catalog"))
    start_date = setup["horizon"][0].date()
    pid = setup["person_id"]

    plans = {}   # method -> (health blocks, unscheduled, batch size)
    batch = None
    for name, folder in sources.items():
        solution = load_solution(folder, pid)
        if solution is None:
            print(f"  {name}: no solution file for {pid} in {folder}; skipped")
            continue
        own_batch = task_batch_from_solution(solution, catalog, start_date)
        batch = batch or own_batch
        blocks = placements_from_solution(solution, own_batch, pid,
                                          setup["persona_id"], name, start_date)
        unscheduled = solution.get("unscheduled", [])
        plans[name] = (blocks, unscheduled, len(own_batch))
    if batch is None:
        sys.exit("No solution file found; run v2/tools/import_calendar_bench.py first.")
    batch.sort(key=lambda t: (t["week"], t["slug"]))
    for name in hs.get("builtin_methods") or []:
        blocks, unscheduled = build_method(name, batch, setup, setup["params"],
                                           config["persona"], hs.get("seed", 0))
        plans[name] = (blocks, unscheduled, len(batch))

    reps = args.replications or config["replications"]["count"]
    base_seed = config["replications"]["base_seed"]
    triggers = triggers_of(config)
    print(f"Person {pid}: task batch {len(batch)} health tasks over "
          f"{len({t['week'] for t in batch})} weeks; {reps} replications per method")

    per_rep = {}
    for name, (blocks, unscheduled, size) in plans.items():
        tasks = sorted(setup["tasks"] + blocks, key=lambda t: t["start"])
        per_rep[name] = []
        for r in range(reps):
            res = run_replication(tasks, setup["context_events"], setup["experiment"],
                                  setup["params"], setup["rules"], setup["horizon"],
                                  triggers, base_seed + r, setup["persona"],
                                  config["persona"])
            per_rep[name].append(health_kpis(res, blocks, size, unscheduled))
        m, lo, hi = mean_ci([k["Health completion (whole batch)"] for k in per_rep[name]])
        print(f"  {name:18s} placed {len({b['health_group'] for b in blocks}):3d}  "
              f"health completion {m:.3f} [{lo:.3f}, {hi:.3f}]")

    methods = list(plans)
    kpi_names = list(next(iter(per_rep.values()))[0])
    rows = {(m, k): mean_ci([x[k] for x in per_rep[m]]) for m in methods for k in kpi_names}

    out_dir = Path(config["output"]["dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(ics_file).stem
    summary = [[m, k, *rows[(m, k)]] for k in kpi_names for m in methods]
    with (out_dir / f"{stem}_planning_methods.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Method", "KPI", "Mean", "95% CI low", "95% CI high"])
        w.writerows(summary)
    wide = [[k] + [rows[(m, k)][0] for m in methods] for k in kpi_names]
    placements = [[m, b["health_slug"], b["health_week"], b["health_domain"],
                   b["intensity"], b["is_concurrent"], b["start"], b["end"]]
                  for m, (blocks, _, _) in plans.items() for b in blocks]
    xlsx = write_workbook(out_dir / f"{stem}_planning_methods.xlsx", [
        ("Comparison (means)", ["KPI"] + methods, wide),
        ("Comparison (CI)", ["Method", "KPI", "Mean", "95% CI low", "95% CI high"], summary),
        ("Replications", ["Method", "Replication"] + kpi_names,
         [[m, r + 1] + [x[k] for k in kpi_names]
          for m in methods for r, x in enumerate(per_rep[m])]),
        ("Placements", ["Method", "Task", "Week", "Domain", "Intensity",
                        "Concurrent", "Start", "End"], placements),
        ("Task batch", ["Task", "Week", "Domain", "Domain source", "Sub-class",
                        "Duration min", "Intensity", "Concurrent", "Dividable"],
         [[t["slug"], t["week"], t["domain"], t["domain_source"], t["subclass"],
           t["duration_min"], t["intensity"], t["is_concurrent"], t["is_dividable"]]
          for t in batch]),
    ])
    png = plot(out_dir / f"{stem}_planning_methods.png", rows, methods)
    print("\nFiles written:")
    for p in (xlsx, out_dir / f"{stem}_planning_methods.csv", png):
        if p:
            print(f"  {Path(p).resolve()}")


if __name__ == "__main__":
    main()
