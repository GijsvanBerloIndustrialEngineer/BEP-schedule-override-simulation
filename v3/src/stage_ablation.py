"""
Contribution of the two v3 stages: the same calendar and seeds with the
review stage and the progress model switched off and on.

    python v3/src/stage_ablation.py [calendar.ics] [--replications 10]

Variants:
  execution only       decision at the task start (v2 model), no review,
                       no progress model, no Poisson interruptions
  + review             stage 1 added
  + progress           progress model added
  full v3              both

Output: v3/output/<calendar>_v3_stage_ablation.xlsx / .csv
"""

import argparse
import copy
import csv
import statistics
import sys
from pathlib import Path

from model_v3 import DEFAULT_CONFIG, load_config
from run_simulation import run

from common import load_setup, write_workbook  # v2

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from override_simulation import t_quantile_975  # noqa: E402  (v1)

VARIANTS = {
    "execution only": (False, False),
    "+ review": (True, False),
    "+ progress": (False, True),
    "full v3": (True, True),
}
KPIS = ["Completion rate (eligible tasks)", "Share completed", "Share partial",
        "Share rejected", "Share missed", "Share replaced", "Share moved at review",
        "Share postponed at start", "Plan-execution deviation (hours)"]


def mean_ci(values):
    values = [v for v in values if v is not None]
    m = statistics.mean(values)
    if len(values) < 2:
        return m, None, None
    h = t_quantile_975(len(values) - 1) * statistics.stdev(values) / len(values) ** 0.5
    return m, m - h, m + h


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("ics_file", nargs="?", type=Path, default=None)
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--replications", type=int, default=10)
    args = ap.parse_args(argv)
    base = load_config(args.config)
    ics = args.ics_file or base["default_calendar"]
    setup = load_setup(base, ics)

    rows = []
    for name, (rev, prog) in VARIANTS.items():
        cfg = copy.deepcopy(base)
        cfg["stages"]["review"]["enabled"] = rev
        cfg["stages"]["progress"]["enabled"] = prog
        _, per_rep = run(cfg, setup, args.replications)
        stats = {k: mean_ci([r[k] for r in per_rep]) for k in KPIS}
        rows.append((name, stats))
        print(f"  {name:16s} completion {stats[KPIS[0]][0]:.3f}  partial {stats['Share partial'][0]:.3f}  "
              f"rejected {stats['Share rejected'][0]:.3f}  deviation {stats[KPIS[-1]][0]:.1f} h")

    out = Path(base["output"]["dir"]); out.mkdir(parents=True, exist_ok=True)
    stem = Path(ics).stem
    with (out / f"{stem}_v3_stage_ablation.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Variant", "KPI", "Mean", "95% CI low", "95% CI high"])
        for name, stats in rows:
            for k in KPIS:
                w.writerow([name, k, *stats[k]])
    write_workbook(out / f"{stem}_v3_stage_ablation.xlsx", [
        ("Stage ablation", ["Variant"] + KPIS, [[n] + [s[k][0] for k in KPIS] for n, s in rows]),
    ])
    print(f"Files written to {out.resolve()}")


if __name__ == "__main__":
    main()
