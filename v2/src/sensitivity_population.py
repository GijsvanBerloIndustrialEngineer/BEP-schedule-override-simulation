"""
Sensitivity analysis of the v2 simulation over the whole calendar-bench
population (30 planned calendars, three personas).

For every person:
  - the person's own sampled Big Five traits (calendar_bench_population/
    persons/<person>.json) replace the persona means;
  - base setting, the one-at-a-time (OAT) low/high settings of sensitivity.py,
    and the context/persona ablation, each with R replications and the same
    seeds (common random numbers).

    python v2/src/sensitivity_population.py [--replications 10] [--workers 10]
    python v2/src/sensitivity_population.py --plot-only     # redraw from the CSV

Output (default docs/sensitivity_30_calendars/):
  results_per_person.csv   one row per person x setting (mean over replications)
  summary.xlsx             aggregated tables
  fig_*.png                charts
"""

import argparse
import copy
import csv
import json
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

SRC = Path(__file__).resolve().parent
REPO = SRC.parents[1]
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

BIG_FIVE = ("openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism")
KPIS = ["Completion rate (eligible tasks)", "Plan-execution deviation (hours)",
        "Share postponed", "Share skipped", "Share replaced",
        "Share of postponements to a later day"]
PERSONAS = ["diligent_anxious_active", "free_spirited_social_student", "unemployed_family_caregiver"]
SHORT = {"diligent_anxious_active": "Diligent, anxious, active",
         "free_spirited_social_student": "Free-spirited social student",
         "unemployed_family_caregiver": "Unemployed family caregiver"}


def person_traits(person_file):
    c = json.loads(Path(person_file).read_text(encoding="utf-8"))["persona"]["characteristics"]
    return {t: float(c[t]) for t in BIG_FIVE if t in c}


def persona_from_traits(traits):
    """A persona dict that persona_traits(..., 'mean') turns into these exact values."""
    return {"characteristics": {t: {"type": "norm", "params": {"loc": v, "scale": 0.0}}
                                for t, v in traits.items()}}


def run_person(ics, person_file, reps):
    """All settings for one person; returns a list of result rows."""
    from common import load_setup, triggers_of
    from model_v2 import load_config, validate_parameters
    from sensitivity import PARAMETERS, ABLATION, _scale
    from simulation_v2 import run_replication, replication_kpis

    config = load_config()
    setup = load_setup(config, ics)
    traits = person_traits(person_file)
    persona = persona_from_traits(traits)
    base_params, base_triggers = setup["params"], triggers_of(config)
    seed0 = config["replications"]["base_seed"]

    def run(params, triggers):
        vals = {k: [] for k in KPIS}
        for r in range(reps):
            res = run_replication(setup["tasks"], setup["context_events"], setup["experiment"],
                                  params, setup["rules"], setup["horizon"], triggers,
                                  seed0 + r, persona, config["persona"])
            k = replication_kpis(res)
            for name in KPIS:
                if k.get(name) is not None:
                    vals[name].append(k[name])
        return {name: (statistics.mean(v) if v else None) for name, v in vals.items()}

    meta = {"person": setup["person_id"], "persona": setup["persona_id"], **traits}
    rows = [dict(meta, analysis="base", parameter="base", level="base", value="",
                 **run(base_params, base_triggers))]
    for name, (path, low, high, apply) in PARAMETERS.items():
        for level, value in (("low", low), ("high", high)):
            params, triggers = copy.deepcopy(base_params), dict(base_triggers)
            apply(params, triggers, value)
            validate_parameters(params)
            rows.append(dict(meta, analysis="oat", parameter=name, level=level, value=value,
                             **run(params, triggers)))
    for name, switch in ABLATION.items():
        params, triggers = copy.deepcopy(base_params), dict(base_triggers)
        _scale("context_coefficients", None)(params, triggers, switch["context"])
        if not switch["context"]:
            params["intensity_slope"] = {}
        _scale("trait_coefficients", None)(params, triggers, switch["persona"])
        rows.append(dict(meta, analysis="ablation", parameter=name, level="", value="",
                         **run(params, triggers)))
    return rows


def simulate(args, out):
    ics_files = sorted(Path(args.ics_dir).glob("*.ics"))
    jobs = []
    for ics in ics_files:
        pf = Path(args.persons_dir) / f"{ics.stem}.json"
        if not pf.exists():
            print(f"  no person file for {ics.stem}; skipped")
            continue
        jobs.append((str(ics), str(pf)))
    print(f"{len(jobs)} calendars, {args.replications} replications per setting, {args.workers} workers")
    rows, t0 = [], time.time()
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_person, ics, pf, args.replications): ics for ics, pf in jobs}
        for i, f in enumerate(as_completed(futs), start=1):
            rows.extend(f.result())
            print(f"  [{i}/{len(jobs)}] {Path(futs[f]).stem} done ({time.time() - t0:.0f} s)")
    rows.sort(key=lambda r: (r["person"], r["analysis"] != "base", r["analysis"], r["parameter"], r["level"]))
    fields = ["person", "persona", *BIG_FIVE, "analysis", "parameter", "level", "value", *KPIS]
    with (out / "results_per_person.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return rows


def load_rows(out):
    rows = []
    with (out / "results_per_person.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            for k in (*BIG_FIVE, *KPIS):
                r[k] = float(r[k]) if r.get(k) not in (None, "") else None
            rows.append(r)
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--ics-dir", default=str(REPO / "calendar_bench_population" / "ics"))
    ap.add_argument("--persons-dir", default=str(REPO / "calendar_bench_population" / "persons"))
    ap.add_argument("--out", default=str(REPO / "docs" / "sensitivity_30_calendars"))
    ap.add_argument("--replications", type=int, default=10)
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--plot-only", action="store_true")
    args = ap.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = load_rows(out) if args.plot_only else simulate(args, out)
    if args.plot_only:
        print(f"{len(rows)} rows read from {out / 'results_per_person.csv'}")
    from sensitivity_population_report import make_report
    make_report(rows, out, args.replications)


if __name__ == "__main__":
    main()
