# calendar-bench configuration files

This folder holds the experiment configuration files of
[calendar-bench](https://github.com/MaaniBeigy/calendar-bench), copied unchanged from commit
[`2c823c2`](https://github.com/MaaniBeigy/calendar-bench/tree/2c823c234d7c25bae7f603d74eb8fd7d522b7243).
They are here so the override simulation can use the same experiment setup (horizon, time windows,
event catalog, personas, temporal rules and scenarios) that calendar-bench uses to generate the
planned calendars. The override simulation is meant to become an extra step in calendar-bench that
works on these configs.

calendar-bench is MIT-licensed; its licence is kept in [`LICENSE`](LICENSE).

## What is in here

| Path | Origin in calendar-bench | Contents |
| --- | --- | --- |
| [`CONFIG.md`](CONFIG.md) | `CONFIG.md` | Full reference for every field in the five YAML files |
| [`experiments/example_experiment/`](experiments/example_experiment/) | `src/experiments/persona/example_experiment/` | Small working example experiment |
| [`experiments/healthy_lifestyle_promotion/`](experiments/healthy_lifestyle_promotion/) | `src/experiments/persona/healthy_lifestyle_promotion/` | PHLC-2026 benchmark experiment (3 personas). Calendars such as `diligent_anxious_active_0000.ics` are generated from this experiment |
| [`templates/persona/`](templates/persona/) | `src/scripts/persona/config/examples/` | Template persona-generation configs |
| [`templates/scenarios/`](templates/scenarios/) | `src/scripts/scenarios/config/examples/` | Template scenario configs |

The `human_coach_schedules/` JSON data of the PHLC-2026 experiment is not copied; only the configs are.

## The five files of an experiment

| File | Purpose | Relevance for the override simulation |
| --- | --- | --- |
| `environment.yaml` | Seed, horizon, solver, named time windows, daily waking window | Simulation horizon, seed and time windows to reuse |
| `event_config.yaml` | Catalog of events with population-wide bounds | Which events exist and how flexible they are (duration, frequency, windows) |
| `persona_config.yaml` | Persona templates and their characteristics | Persona characteristics that should drive override probabilities |
| `temporal_relation_rules.yaml` | LTL and Allen rules between events | Rules an overridden/rescheduled plan must still satisfy |
| `scenarios.yaml` | Task-scheduling scenarios on top of the calendars | The tasks whose completion the override simulation measures |

Note: paths inside `CONFIG.md` refer to the calendar-bench layout
(`src/experiments/persona/<experiment>/`). In this repository the same files live under
`calendar_bench_configs/experiments/<experiment>/`.
