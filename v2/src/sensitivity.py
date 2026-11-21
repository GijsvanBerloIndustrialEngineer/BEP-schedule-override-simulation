"""
Sensitivity analysis of the v2 override simulation.

Two parts:

1. One-at-a-time (OAT): every parameter group is set to a low and a high
   value while the rest stays at the config value; R replications per
   setting with the same seeds (common random numbers). Output: a table and
   a tornado chart of the change in the completion rate.
2. Ablation (the slide's question "how strongly do context and persona make
   execution deviate from the plan?"): the model without context and persona
   inputs (v1 logic), with only context, with only persona, and with both.

    python v2/src/sensitivity.py [calendar.ics] [--replications 10] [--skip-oat] [--skip-ablation]
    python v2/src/sensitivity.py --health-method human_coach   # include the health tasks

Output (output.dir): <calendar>_sensitivity.xlsx / .csv and
<calendar>_sensitivity_tornado.png
"""

import argparse
import copy
import csv
import statistics
from pathlib import Path

from common import load_setup, triggers_of, write_workbook
from compare_planning_methods import mean_ci
from health_tasks import (
    build_method, load_catalog, load_solution, placements_from_solution,
    task_batch_from_solution,
)
from model_v2 import DEFAULT_CONFIG, load_config, validate_parameters
from simulation_v2 import run_replication, replication_kpis

KPIS = ["Completion rate (eligible tasks)", "Plan-execution deviation (hours)",
        "Share postponed", "Share skipped", "Share replaced",
        "Share of postponements to a later day"]


# ------------------------------------------------------------------
# Parameter groups: name -> (description, low, high, apply(params, triggers, value))
# ------------------------------------------------------------------

def _scale(group, factor):
    def apply(params, triggers, value):
        for action, coefs in (params.get(group) or {}).items():
            for k in coefs:
                coefs[k] *= value
    return apply


def _scale_one(name, factor=None):
    def apply(params, triggers, value):
        for action in params["coefficients"]:
            params["coefficients"][action][name] *= value
    return apply


def _base(params, triggers, value):
    for a in params["base_probabilities"]:
        params["base_probabilities"][a] *= value


def _lambda(params, triggers, value):
    triggers["rate_per_hour"] = value


def _q(params, triggers, value):
    params["notification_share"] = value


def _slope(params, triggers, value):
    params["intensity_slope"] = {"tired": value}


def _window(params, triggers, value):
    params["postpone_window"] = {"mode": "rolling", "days": value}


def _task_start(params, triggers, value):
    triggers["task_start"] = bool(value)


PARAMETERS = {
    "lambda (arrivals per hour)": ("triggers.rate_per_hour", 0.2, 0.8, _lambda),
    "base probabilities (x factor)": ("override_model.base_probabilities", 0.5, 1.5, _base),
    "beta fill (x factor)": ("coefficients.*.fill", 0.0, 2.0, _scale_one("fill")),
    "beta earlier overrides (x factor)": ("coefficients.*.earlier_overrides", 0.0, 2.0, _scale_one("earlier_overrides")),
    "beta notified (x factor)": ("coefficients.*.notified", 0.0, 2.0, _scale_one("notified")),
    "q notification share": ("notification_share", 0.0, 1.0, _q),
    "beta context (x factor)": ("context_coefficients", 0.0, 2.0, _scale("context_coefficients", None)),
    "beta persona traits (x factor)": ("trait_coefficients", 0.0, 2.0, _scale("trait_coefficients", None)),
    "beta tired x intensity": ("intensity_slope.tired", 0.0, 0.30, _slope),
    "replanning window (days)": ("postpone_window.days", 1, 14, _window),
    "task-start trigger (off/on)": ("triggers.task_start", 0, 1, _task_start),
}

ABLATION = {
    "v1 inputs only (no context, no persona)": {"context": 0.0, "persona": 0.0},
    "+ context": {"context": 1.0, "persona": 0.0},
    "+ persona": {"context": 0.0, "persona": 1.0},
    "+ context + persona (v2)": {"context": 1.0, "persona": 1.0},
}


def run_setting(tasks, setup, params, triggers, config, reps, extra_kpis=None):
    base_seed = config["replications"]["base_seed"]
    out = []
    for r in range(reps):
        res = run_replication(tasks, setup["context_events"], setup["experiment"],
                              params, setup["rules"], setup["horizon"], triggers,
                              base_seed + r, setup["persona"], config["persona"])
        k = replication_kpis(res)
        row = {name: k.get(name) for name in KPIS}
        if extra_kpis:
            row.update(extra_kpis(res))
        out.append(row)
    return out


def health_tasks_for(config, setup, method):
    hs = config["health_scenario"]
    catalog = load_catalog(hs.get("health_task_catalog"))
    start = setup["horizon"][0].date()
    first = next(iter(hs["solutions"].items()))
    sol = load_solution(first[1], setup["person_id"])
    batch = task_batch_from_solution(sol, catalog, start)
    if method in hs["solutions"]:
        sol = load_solution(hs["solutions"][method], setup["person_id"])
        return placements_from_solution(sol, batch, setup["person_id"],
                                        setup["persona_id"], method, start)
    batch.sort(key=lambda t: (t["week"], t["slug"]))
    return build_method(method, batch, setup, setup["params"], config["persona"],
                        hs.get("seed", 0))[0]


def tornado(path, rows, kpi):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    data = sorted(rows, key=lambda r: abs(r["high"] - r["low"]))
    fig, ax = plt.subplots(figsize=(9, 0.45 * len(data) + 1.5))
    for i, r in enumerate(data):
        ax.barh(i, r["low"] - r["base"], color="#2a6f97", height=0.6,
                label="low value" if i == 0 else None)
        ax.barh(i, r["high"] - r["base"], color="#e07a5f", height=0.6,
                label="high value" if i == 0 else None)
        ax.text(min(r["low"], r["high"]) - r["base"], i,
                f"{r['low_value']} / {r['high_value']}  ", va="center",
                ha="right", fontsize=7, color="#555555")
    ax.axvline(0, color="#333333", linewidth=0.8)
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels([r["parameter"] for r in data], fontsize=8)
    ax.set_xlabel(f"Change in {kpi.lower()} vs. base (base = {data[0]['base']:.3f})")
    ax.set_title("One-at-a-time sensitivity (mean over replications)")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Sensitivity analysis of the v2 simulation")
    parser.add_argument("ics_file", nargs="?", type=Path, default=None)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--replications", type=int, default=10)
    parser.add_argument("--health-method", default=None,
                        help="add the health tasks of this planning method")
    parser.add_argument("--skip-oat", action="store_true")
    parser.add_argument("--skip-ablation", action="store_true")
    args = parser.parse_args(argv)

    config = load_config(args.config)
    ics_file = args.ics_file or config["default_calendar"]
    setup = load_setup(config, ics_file)
    tasks = setup["tasks"]
    extra = None
    if args.health_method:
        hblocks = health_tasks_for(config, setup, args.health_method)
        tasks = sorted(tasks + hblocks, key=lambda t: t["start"])
        hgroups = {b["uid"]: b["health_group"] for b in hblocks}

        def extra(res):
            groups = {}
            for o in res["outcomes"]:
                if o["uid"] in hgroups:
                    groups.setdefault(hgroups[o["uid"]], []).append(o["completed"])
            return {"Health completion": (sum(all(v) for v in groups.values())
                                          / len(groups)) if groups else None}
        if "Health completion" not in KPIS:
            KPIS.append("Health completion")
    reps = args.replications
    base_params = setup["params"]
    base_triggers = triggers_of(config)

    print(f"Base setting ({reps} replications)...")
    base_rows = run_setting(tasks, setup, base_params, base_triggers, config, reps, extra)
    base = {k: mean_ci([r[k] for r in base_rows]) for k in KPIS}

    long_rows = [["base", "", ""] + [k] + list(base[k]) for k in KPIS]
    oat = []
    if not args.skip_oat:
        for name, (path, low, high, apply) in PARAMETERS.items():
            res = {}
            for label, value in (("low", low), ("high", high)):
                params = copy.deepcopy(base_params)
                triggers = dict(base_triggers)
                apply(params, triggers, value)
                validate_parameters(params)
                rows = run_setting(tasks, setup, params, triggers, config, reps, extra)
                res[label] = {k: mean_ci([r[k] for r in rows]) for k in KPIS}
                for k in KPIS:
                    long_rows.append([name, label, value, k, *res[label][k]])
            main_kpi = KPIS[0]
            oat.append({
                "parameter": name, "config_path": path,
                "low_value": low, "high_value": high,
                "base": base[main_kpi][0],
                "low": res["low"][main_kpi][0], "high": res["high"][main_kpi][0],
                "low_dev": res["low"][KPIS[1]][0], "high_dev": res["high"][KPIS[1]][0],
            })
            print(f"  {name:36s} completion {oat[-1]['low']:.3f} / {oat[-1]['high']:.3f} "
                  f"(base {oat[-1]['base']:.3f})")

    ablation = []
    if not args.skip_ablation:
        print("Ablation: context and persona inputs")
        for name, switch in ABLATION.items():
            params = copy.deepcopy(base_params)
            triggers = dict(base_triggers)
            _scale("context_coefficients", None)(params, triggers, switch["context"])
            if not switch["context"]:
                params["intensity_slope"] = {}
            _scale("trait_coefficients", None)(params, triggers, switch["persona"])
            rows = run_setting(tasks, setup, params, triggers, config, reps, extra)
            stats = {k: mean_ci([r[k] for r in rows]) for k in KPIS}
            ablation.append((name, stats))
            print(f"  {name:42s} completion {stats[KPIS[0]][0]:.3f}  "
                  f"deviation {stats[KPIS[1]][0]:.1f} h")
            for k in KPIS:
                long_rows.append(["ablation: " + name, "", "", k, *stats[k]])

    out_dir = Path(config["output"]["dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(ics_file).stem + (f"_{args.health_method}" if args.health_method else "")
    header = ["Parameter", "Level", "Value", "KPI", "Mean", "95% CI low", "95% CI high"]
    with (out_dir / f"{stem}_sensitivity.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(long_rows)
    ref = ablation[0][1] if ablation else None
    sheets = [
        ("OAT (completion)", ["Parameter", "Config path", "Low value", "High value",
                              "Base completion", "Completion at low", "Completion at high",
                              "Swing (high - low)", "Deviation h at low", "Deviation h at high"],
         [[o["parameter"], o["config_path"], o["low_value"], o["high_value"],
           o["base"], o["low"], o["high"], o["high"] - o["low"],
           o["low_dev"], o["high_dev"]] for o in oat]),
        ("Ablation", ["Model inputs"] + [f"{k} (mean)" for k in KPIS]
         + ["Completion change vs v1 inputs", "Deviation change vs v1 inputs (h)"],
         [[n] + [s[k][0] for k in KPIS]
          + [s[KPIS[0]][0] - ref[KPIS[0]][0], s[KPIS[1]][0] - ref[KPIS[1]][0]]
          for n, s in ablation]),
        ("All results", header, long_rows),
    ]
    xlsx = write_workbook(out_dir / f"{stem}_sensitivity.xlsx", sheets)
    png = tornado(out_dir / f"{stem}_sensitivity_tornado.png", oat, KPIS[0]) if oat else None
    print("\nFiles written:")
    for p in (xlsx, out_dir / f"{stem}_sensitivity.csv", png):
        if p:
            print(f"  {Path(p).resolve()}")


if __name__ == "__main__":
    main()
