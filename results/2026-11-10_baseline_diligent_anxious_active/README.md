# Baseline experiment: diligent_anxious_active_0000

Run on 2026-11-10 with simulation code at commit `a4893c3` and the unchanged config (copied here as `override_config_used.yaml`).

- **Input calendar:** `diligent_anxious_active_0000.ics` from calendar-bench (experiment `healthy_lifestyle_promotion`; not stored here, see `data/`)
- **Persona:** `diligent_anxious_active` (default parameters + persona set)
- **Arrivals:** Poisson, λ = 0.4 per hour
- **Replications:** 30 (seeds 42–71), 95% confidence intervals
- **Command:** `python src/simulation.py data/diligent_anxious_active_0000.ics`

All override probabilities and coefficients are version-1 assumptions, not fitted values.

## KPIs (mean [95% CI] over 30 replications)

| KPI | Value |
|---|---|
| Completion rate (eligible tasks) | 0.953 [0.950, 0.956] |
| Completion rate (all tasks) | 0.985 [0.985, 0.986] |
| Share postponed | 0.0165 [0.0147, 0.0183] |
| Share skipped | 0.0393 [0.0364, 0.0422] |
| Share replaced | 0.0081 [0.0064, 0.0097] |
| Mean postponement delay (hours) | 1.68 [1.39, 1.97] |
| Plan–execution deviation (hours) | 30.2 [28.0, 32.3] |
| Planned task hours | 1102 |
| Executed task hours | 1077 [1075, 1079] |
| Eligible tasks | 480 |
| Arrivals | 551.4 [544.5, 558.2] |
| Override checks | 140.0 [136.1, 143.9] |
| Overrides | 30.7 [29.1, 32.2] |
| Failed postponements (became skip) | 10.5 [9.5, 11.4] |
| Arrivals ignored: free time | 138.5 [133.5, 143.6] |
| Arrivals ignored: sleep | 139.7 [135.4, 143.9] |
| Arrivals ignored: excluded task | 131.8 [126.7, 136.9] |
| Arrivals ignored: unplanned block | 1.4 [0.7, 2.1] |

## Observations

- Only about 25% of arrivals (140 of 551) reach an eligible task; the rest fall in free time, sleep or excluded tasks.
- About a third of postponement attempts fail (10.5 failed vs. ~7.9 successful), because no free slot was left on the same day, so they become skips. This pushes the skip share above the postpone share.

## Files

- `diligent_anxious_active_0000_override_simulation.xlsx`: KPI summary, replications, changes, decisions, tasks, executed calendar, parameters
- `diligent_anxious_active_0000_executed_run1.ics`: executed calendar of replication 1
- `diligent_anxious_active_0000_calendar_bench/`: plan and executed run 1 in calendar-bench JSON, for `tools/validate_with_calendar_bench.py`
- `override_config_used.yaml`: the config used for this run
