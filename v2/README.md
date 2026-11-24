# Version 2 of the override simulation

Version 1 (`../src`, `../config`) shows that the mechanism works. Version 2 has to show **how strongly context and persona make execution deviate from the plan**. Version 1 is not changed. v2 imports its calendar loading, slot search, temporal rules and KPI code from `../src` and adds everything new in this folder.

## What changed compared with v1

| v1 limitation | v2 |
|---|---|
| Probabilities and β's are assumptions, not fitted | Still not fitted (there is no execution data). Every parameter is now documented with its source status and literature for its direction in [PARAMETERS.md](PARAMETERS.md), and covered by a sensitivity analysis (`src/sensitivity.py`). |
| Context (`[ctx]`) and persona traits are not inputs | The logit has context covariates (energy, mood, stress, location, weather, self-efficacy, intention) read from the `[ctx:...]` episodes at the decision moment, a tired × intensity term, and the Big Five traits of the persona from `persona_config.yaml` (`src/model_v2.py`). |
| Replacing always gives a generic `UNPLANNED` block | A concrete activity (rest, snack, socialise, read, screen time, walk outside) is drawn with weights that depend on the active context and the traits. Most map onto calendar-bench catalog events, so they appear in the calendar-bench JSON export. |
| Postponing only within the same day | **Replanning looks at a week**: the next feasible slot is searched over a rolling 7-day window (`postpone_window`; `calendar_week` = until Sunday, `same_day` = v1). |

Also new:

- **Task-start trigger**: besides the Poisson arrivals (v1), every eligible task gets one decision at its planned start, and again at its new start after a postponement. Without it, a 10-minute health task is hit by an arrival only ~6% of the time. Set `triggers.task_start: false` for v1 behaviour.
- **Health tasks**: the calendar-bench `healthy_lifestyle_promotion` health tasks can be added to the calendar as the human coach placed them (`sensitivity.py --health-method human_coach`).
- v1's per-persona base probabilities are dropped: persona differences now come from the traits.

## Run it

From the repository root (Python 3.9+):

```bash
pip install -r v2/requirements.txt
```

```bash
python v2/src/run_simulation.py
```

```bash
python v2/src/sensitivity.py --replications 10
```

Without a calendar argument, the scripts use `default_calendar` from [`config/v2_config.yaml`](config/v2_config.yaml) (`data/diligent_anxious_active_0000.ics`, which is not in git; pass another `.ics` as the first argument). Output goes to `v2/output/` (not in git). Run times on a laptop: about 1 min and 9 min.

| Script | Output |
|---|---|
| `run_simulation.py` | `<calendar>_v2_simulation.xlsx` (KPIs with 95% CI, changes incl. replacement activity and days moved, decisions with active context, persona traits, parameters), executed `.ics`, calendar-bench JSON |
| `sensitivity.py` | `<calendar>_sensitivity.xlsx/.csv`, `_sensitivity_tornado.png`: one-at-a-time low/high per parameter group, plus the **ablation** (v1 inputs → + context → + persona → both) |

`sensitivity.py --health-method human_coach` runs the same analysis with the health tasks in the calendar and adds *Health completion* as a KPI.

## Health tasks

calendar-bench publishes the output of the **human coach** (`human_coach_schedules/`) for all 30 persons; they are in `data/scenario_solutions/human_coach/`. `sensitivity.py --health-method human_coach` adds those health tasks to the calendar and reports *Health completion*.

Comparing planning methods is not done in this repository: the plan is to run the override simulation inside calendar-bench, so each calendar-bench planner gets execution KPIs there.

## Files

```
v2/
├── README.md
├── PARAMETERS.md                 # every parameter: value, source status, literature, sensitivity range
├── requirements.txt
├── config/v2_config.yaml
├── data/                         # copied from calendar-bench (MIT), see data/README.md
│   ├── scenario_solutions/human_coach/diligent_anxious_active_0000.json
│   └── health_task_catalog.json
├── src/
│   ├── model_v2.py               # logit with context + persona, replacement choice
│   ├── simulation_v2.py          # event loop: triggers, week-long replanning, replacements
│   ├── health_tasks.py           # health tasks from calendar-bench solution files
│   ├── common.py                 # setup, Excel/.ics/JSON output
│   ├── run_simulation.py         # entry: one calendar
│   └── sensitivity.py            # OAT + ablation
└── tools/import_calendar_bench.py   # copies inputs from a calendar-bench checkout (read-only)
```

## Known limitations of v2

- Still no fitted parameters: the sensitivity analysis shows which ones matter most and should get data or literature first.
- Persona traits are the persona mean by default (`persona.trait_source: sample` draws one person per replication); calendar-bench's sampled values per person are not in the `.ics`.
- Some context covariates hardly occur during tasks for this persona (`tired` only at night), so their coefficients have no effect on this calendar.
- `fill` and the earlier-overrides window are still per day; only replanning looks a week ahead.
- Sensitivity is one-at-a-time (no interactions). A Morris screening or Sobol indices are the next step (see PARAMETERS.md).
