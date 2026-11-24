# Simulation Manual

This manual describes how the override simulation works: what it reads, how it decides on overrides, how it builds the executed calendar, and what it writes. The design decisions D1–D15 it refers to are listed in [docs/REPORT.md](docs/REPORT.md), section 4.

The simulation has three versions. Each later version imports the code of the earlier ones and changes nothing in them, so the base described in sections 1–12 still applies to all three.

| Part | Sections | Version |
|---|---|---|
| A | 1–12 | **Version 1**: the base mechanism, its inputs, output and scoring with calendar-bench |
| B | 13 | **Version 2** (`v2/`): context and persona in the decision, replacement activities, week-long replanning, task-start trigger, health scenario, sensitivity analysis |
| C | 14 | **Version 3** (`v3/`): review of the day in advance and partial execution |
| D | 15 | **Input calendars**: the 30 calendars of the calendar-bench population (`calendar_bench_population/`) |

---

## 1. Overview

```
override_config.yaml ──┐
calendar-bench configs ┼─► load ─► R replications of the override loop ─► KPIs + CI ─► Excel + executed .ics
planned .ics ──────────┘
```

One replication works as follows (see also [docs/CONCEPTUAL_MODEL.md](docs/CONCEPTUAL_MODEL.md)):

```
for each Poisson arrival t, in time order:                       (D1)
    look at the EXECUTED calendar at t
    no task, sleep, or only excluded tasks → ignore              (D2, D9)
    pick the active task
    fill   ← planned hours left today                            (D6)
    k      ← overrides earlier today                             (D5)
    n      ← task notified? (0/1)                                (D10)
    p      ← multinomial logit(fill, k, n)                       (D3, D4)
    action ← draw from {none, postpone, skip, replace} with p
    update the executed calendar                                 (D7, D8)
compute KPIs                                                     (D13)
```

| Module | Role |
|---|---|
| `src/simulation.py` | Entry point: loads everything, runs the replications, writes Excel and `.ics` |
| `src/calendar_bench_link.py` | Reads the calendar-bench configs and matches calendar events to them |
| `src/override_model.py` | Parameter sets per persona, eligibility, multinomial logit |
| `src/override_simulation.py` | Arrivals, executed calendar, the override loop, KPIs, confidence intervals |
| `src/rules.py` | Temporal rules that a postponed task must respect |
| `src/executed_calendar.py` | Writes the executed calendar as `.ics` |
| `src/calendar_bench_export.py` | Writes the plan and executed calendars in calendar-bench's JSON format |
| `tools/validate_with_calendar_bench.py` | Scores those JSON files with calendar-bench's own validation (section 12) |

---

## 2. Running the simulation

### Requirements

- Python 3.9 or newer
- Packages: `icalendar`, `openpyxl`, `PyYAML`

```bash
pip install -r requirements.txt
```

### Command

```bash
python src/simulation.py path/to/calendar.ics
python src/simulation.py path/to/calendar.ics --replications 5
python src/simulation.py path/to/calendar.ics --config path/to/override_config.yaml
```

- No calendar path: the script uses `DEFAULT_ICS_FILE` at the top of `simulation.py`.
- No `--config`: the script uses `config/override_config.yaml`.
- `--replications` overrides `replications.count` from the config, handy for a quick test.

30 replications of an 8-week calendar take about 10 seconds.

### Output

Written next to the `.ics` file, or in `output.dir` of the config:

| File | Contents |
|---|---|
| `<calendar>_override_simulation.xlsx` | KPI summary, replications, all changes, details of run 1, parameters (section 9) |
| `<calendar>_executed_run1.ics` | The executed calendar of replication 1 (section 8). `output.executed_ics_replications` sets how many runs get an `.ics` |
| `<calendar>_calendar_bench/plan/<person>.json`, `.../executed_runN/<person>.json` | The plan and the executed calendars in calendar-bench's JSON format (section 12); switch off with `output.calendar_bench_json: false` |

Existing files with the same name are overwritten. On Windows, close the Excel file before running, or saving fails with a `PermissionError`.

---

## 3. Configuration (`config/override_config.yaml`)

| Key | Default | Meaning |
|---|---|---|
| `experiment_dir` | `../calendar_bench_configs/experiments/healthy_lifestyle_promotion` | calendar-bench experiment that generated the calendar; relative to the config file |
| `horizon_source` | `experiment` | `experiment`: horizon from `environment.yaml`; `calendar`: first to last planned task |
| `arrivals.rate_per_hour` | `0.4` | λ of the Poisson process (D1) |
| `replications.count` | `30` | Number of replications R (D14) |
| `replications.base_seed` | `42` | Replication r uses seed `base_seed + r` |
| `output.dir` | `null` | Output folder; `null` = next to the `.ics` |
| `output.executed_ics_replications` | `1` | Number of runs that get an executed `.ics` (and calendar-bench JSON) |
| `output.calendar_bench_json` | `true` | Also write calendar-bench JSON files (section 12) |
| `override_model.default` | see below | The parameter set used for every persona |
| `override_model.personas.<persona id>` | see below | Values that differ for one persona (D15) |

### The parameter set

| Key | Default | Decision |
|---|---|---|
| `base_probabilities.postpone / skip / replace` | `0.12 / 0.08 / 0.05` | D3/D4: probabilities when fill = 0, no earlier overrides and no notification. `p_none = 1 − sum` |
| `coefficients.<action>.fill` | `0.10 / 0.08 / 0.05` | D6: effect per planned hour left in the day |
| `coefficients.<action>.earlier_overrides` | `−0.40` | D5: effect per earlier override; negative = lowers the next override chance |
| `coefficients.<action>.notified` | `−0.30 / −0.50 / −0.20` | D10: effect of a notification |
| `earlier_overrides_window` | `day` | D5: which overrides count: `day`, `run` or a number of hours |
| `earlier_overrides_cap` | `3` | D5: higher counts are treated as 3 |
| `notification_share` | `0.5` | D10: share q of tasks that are notified |
| `max_postpones_per_task` | `1` | D7: after this, postpone is no longer possible for the task |
| `check_temporal_rules` | `true` | D7: a new slot must respect the temporal rules |
| `excluded.events / labels / categories` | see config | D9: tasks that never get an override |

**All values are assumptions for version 1.** They are not fitted to data. Report them as assumptions and run a sensitivity analysis.

### Parameter sets per persona (D15)

The persona is read from the calendar: the person id `diligent_anxious_active_0000` gives the persona `diligent_anxious_active`. If `override_model.personas` has an entry for that persona, its values are merged over `default`; keys that are not listed keep the default value. The persona and the parameter set used appear in the **Plan metrics** sheet; the effective values appear in the **Parameters** sheet.

| Persona | Base probabilities (postpone / skip / replace) | Other |
|---|---|---|
| default | 0.12 / 0.08 / 0.05 | q = 0.5 |
| `diligent_anxious_active` | 0.10 / 0.05 / 0.03 | |
| `free_spirited_social_student` | 0.15 / 0.12 / 0.10 | q = 0.3 |
| `unemployed_family_caregiver` | 0.12 / 0.10 / 0.08 | |

---

## 4. Loading the calendar and the experiment

### The calendar-bench experiment

The simulation reads four files from `experiment_dir` (field reference: `calendar_bench_configs/CONFIG.md`):

| File | Used for |
|---|---|
| `environment.yaml` | Horizon (`start_date` + `weeks`), `time_windows`, waking window `daily_window` (06:00–22:00), slot grid `solver.step_minutes` (10 min) |
| `event_config.yaml` | Per event: category, `is_concurrent`, `is_dividable`, `intensity` |
| `persona_config.yaml` | Persona characteristics (exported to the Persona sheet) |
| `temporal_relation_rules.yaml` | Rules a postponed task must respect (section 7) |

`scenarios.yaml` is not used in version 1.

### The planned calendar (`load_calendar`)

calendar-bench writes two kinds of events into one `.ics` file (D11):

- **Planned tasks**, for example `breakfast (Person diligent_anxious_active_0000)`.
- **Context annotations**, whose summary starts with `[ctx:<category>]`, for example `[ctx:energy_state] tired`. They are kept apart, are not tasks, and are not overridden. They are used by the temporal rules (section 7) and are kept as input for the task-context model of version 2.

Every planned task is matched to the experiment:

| Field | Source |
|---|---|
| `uid` | `UID`, or a synthetic `evt-<number>` (calendar-bench files have no `UID`) |
| `label` | what the calendar shows, e.g. `doing research` |
| `event` | the name in `event_config.yaml`, e.g. `office_work`, taken from `DESCRIPTION:Generated event for <label> (<event>)` |
| `category`, `is_concurrent`, `is_dividable`, `intensity` | `event_config.yaml` |
| `person_id`, `persona` | `(Person <id>)` in the summary; persona = id without its number |
| `is_marker` | `wake_up` and `go_to_bed`, zero-length markers derived from `sleep` |
| `time_window` | the `time_windows` entry the start falls in |

Events without `DTSTART`, and planned events without an end or duration, are skipped.

### Dates and times

Times with a timezone are converted to the local time of the computer and the timezone is removed. Times without a timezone (calendar-bench uses these) are used as they are.

---

## 5. Arrivals and the active task (D1, D2, D9)

**Arrivals (D1).** A homogeneous Poisson process with rate λ: exponential gaps with mean 1/λ hours, from the start to the end of the horizon. With λ = 0.4 and an 8-week horizon (1,344 h) that is about 538 arrivals per replication.

**Which task (D2).** Each arrival looks at the executed calendar at that moment, so it sees the result of earlier overrides:

| Situation at the arrival | Result |
|---|---|
| No planned task running | ignored: *free time* |
| Only an `UNPLANNED` block running | ignored: *unplanned block* |
| A sleep task running (`sleep`, `napping`) | ignored: *sleep* |
| Only excluded tasks running (D9) | ignored: *excluded task* |
| One or more eligible tasks running | override decision on one of them |

When several eligible tasks run at the same time, a time-blocking task (`is_concurrent: false`) is chosen before a concurrent one; between equals the choice is random.

**Eligibility (D9).** The explicit exclusion list in the config:

- events: `sleep`, `napping`, `wake_up`, `go_to_bed`, `breakfast`, `lunch`, `dinner`, `snacking`, `drink_water`, `meeting`;
- labels: `standup`, `external meeting` (the `office_work` labels that are meetings).

All other tasks can get an override: office work, sports, chores, reading, socialising, etc. With the test calendar, 480 of the 1,536 planned tasks are eligible.

---

## 6. The override decision (D3–D6, D10)

### Multinomial logit (D3, D4)

For each action k ∈ {postpone, skip, replace}, with *no override* as the reference:

```
η_k = β0_k + β_fill,k · fill + β_over,k · earlier_overrides + β_notif,k · notified

p_k    = exp(η_k) / (1 + Σ_j exp(η_j))
p_none = 1        / (1 + Σ_j exp(η_j))
```

The intercepts follow from the base probabilities: `β0_k = ln(p_k / p_none)`. With the default set (0.12 / 0.08 / 0.05, so p_none = 0.75), β0 = −1.83 / −2.24 / −2.71.

The inputs:

| Input | Definition |
|---|---|
| `fill` (D6) | Planned task hours left in the day, from the arrival to midnight: union of the time-blocking tasks in the executed calendar, without sleep and without concurrent tasks |
| `earlier_overrides` (D5) | Number of overrides earlier in the window (default: the same day), capped at `earlier_overrides_cap`. The negative coefficient makes a later override **less** likely |
| `notified` (D10) | 1 if the task is notified. Each replication draws per task whether it is notified, with probability q (`notification_share`). The test data has no alarms (E3) |

### The rule-based part (D4)

- Only eligible tasks during waking activity get a decision (section 5).
- A task that was already postponed `max_postpones_per_task` times cannot be postponed again: `postpone` gets probability 0 and the other probabilities are rescaled.
- A postponement without a free slot becomes a skip (section 7).

The action is drawn with one uniform random number per decision.

---

## 7. Updating the calendar (D7, D8)

An override acts on the **remaining part** of the active task, from the arrival time t to the planned end. The part before t has already been executed and stays in the calendar.

| Action | Effect |
|---|---|
| No override | Nothing changes |
| **Skip** | The task ends at t; the remaining part is not executed |
| **Replace** (D8) | The task ends at t; an `UNPLANNED` block fills the remaining part, so it has the same length |
| **Postpone** (D7) | The task ends at t; the remaining part moves to the next free slot on the same day. Without a free slot the task is skipped (the Changes sheet shows *postpone failed: no free slot today*) |

### Finding the next free slot (D7)

The slot search starts at the **planned end** of the task (postponing means later, not now) and steps through the day on the `step_minutes` grid (10 min). A slot is free when:

1. it is on the same day, starts after `wake_minutes` and ends before `sleep_minutes` of `daily_window` (06:00–22:00);
2. it does not overlap sleep, and, for a time-blocking task, does not overlap another time-blocking task or `UNPLANNED` block (concurrent tasks such as `drink_water` may overlap);
3. it does not break a temporal rule (if `check_temporal_rules: true`).

### Temporal rules used (`src/rules.py`)

Only rules that a single placement can break are used. From the PHLC experiment that is 22 rules:

- **LTL `G ¬(A ∧ B)`**: A and B never at the same time, for events and contexts. Examples: `no_overlap_sleep_running`, `no_overlap_lunch_work`, `no_office_when_tired` (office work not during a `[ctx:energy_state] tired` period), `no_running_when_tired`, `no_gym_when_tired`.
- **Allen pair rules with only separation relations** (`p`, `P`, `m`, `M`): the two must be apart by at least `buffer` minutes. Examples: `intensive_far_from_intensive` (no two intensity-3/4 events back to back), `lunch_far_from_intensive` (60 minutes after lunch), `sleep_separates_from_running`.

Not used: rules with `applies_to`, LTL shapes with `F` or `→` and `weekly_count` (they describe the whole horizon, not one placement), and Allen rules on `kind: task` (those are about calendar-bench scenario health tasks).

---

## 8. KPIs, replications and the executed calendar (D12–D14)

### KPIs per replication (D13)

Shares and the completion rate are computed over the **eligible** tasks of the plan, unless stated otherwise.

| KPI | Definition |
|---|---|
| Completion rate (eligible tasks) | Share of eligible tasks whose executed hours (all pieces, including a postponed part) reach the planned hours (1 min tolerance) |
| Completion rate (all tasks) | The same over all planned tasks |
| Share postponed | Share of eligible tasks with at least one successful postponement |
| Share skipped | Share with at least one skip, including failed postponements |
| Share replaced | Share with at least one replacement |
| Mean postponement delay (hours) | Mean of (new start − arrival time) over successful postponements |
| Plan–execution deviation (hours) | Sum over all tasks of the symmetric difference between the planned interval and the executed pieces: planned + executed − 2 × overlap |
| Planned / executed task hours | Totals |
| Arrivals, override checks, overrides, failed postponements, ignored arrivals per reason | Counts that explain the KPIs |

A task can get more than one override, for example first postponed and later skipped. It then counts in both shares.

### Replications and confidence intervals (D14)

Replication r (0 … R−1) uses seed `base_seed + r`. Each replication has three separate random streams (arrivals, notifications, decisions), so changing the model does not shift the arrivals. For each KPI the KPI summary sheet gives the mean, the standard deviation and the 95% confidence interval `mean ± t(0.975, R−1) · sd / √R`.

### The executed calendar (D12)

`<calendar>_executed_run1.ics` has the same layout as the plan, so the two can be opened side by side:

- unchanged tasks keep their `SUMMARY` and `DESCRIPTION`;
- interrupted tasks end at the override time; their `DESCRIPTION` ends with `interrupted at HH:MM (<action>)` and they have `X-OVERRIDE:interrupted`;
- postponed parts have `X-OVERRIDE:postpone` and `postponed from <time>` in the `DESCRIPTION`;
- replaced parts are `UNPLANNED (Person <id>)` blocks with `X-OVERRIDE:replace`;
- the `[ctx:...]` context annotations are copied unchanged.

The executed `.ics` can be read again by `load_calendar`.

---

## 9. Excel output

| Sheet | Contents |
|---|---|
| **KPI summary** | Per KPI: mean, standard deviation, 95% CI, N (D13, D14) |
| **Replications** | One row per replication: seed and all KPIs |
| **Changes** | Every override in every replication (D12): time, task, drawn and applied action, old block, new slot, delay, inputs (fill, earlier overrides, notified) and the four probabilities |
| **Decisions (run 1)** | Every arrival of replication 1 with its outcome and probabilities |
| **Tasks (run 1)** | Every planned task with planned and executed hours, eligibility, notification, actions, final outcome and deviation |
| **Executed calendar (run 1)** | Every block of the executed calendar, including `UNPLANNED` blocks |
| **Plan metrics** | Experiment, person, persona, parameter set, task counts, horizon, λ, R |
| **Parameters** | The effective parameter set, including the intercepts |
| **Context** | The `[ctx:...]` annotations (D11) |
| **Persona** | The persona's characteristics from `persona_config.yaml` (distributions, not the values of this person) |

---

## 10. Limitations of version 1

Version 2 (section 13) addresses the context and persona inputs, the scenario tasks, replacement activities and the same-day postponement. Version 3 (section 14) adds partial execution and the review in advance.

- **All parameters are assumptions.** Calibrate them against literature or data, or report a sensitivity analysis.
- **Task context and persona characteristics** (energy state, Big Five, ...) do not yet enter the probability. Personas only change the parameter set (D15).
- **Scenario tasks** from calendar-bench (`scenarios.yaml`, health tasks) are not simulated yet; the simulation works on the persona calendar.
- **Replace** always inserts a generic `UNPLANNED` block (D8).
- **Postpone** only looks at the same day (D7). Many postponements fail late in the day; they are counted as skips.
- **Recurring events (`RRULE`) are not expanded**, and timezone conversion depends on the computer (calendar-bench files are not affected).
- Overlapping tasks in the plan itself are left as they are; calendar-bench sometimes plans tasks at night (e.g. `writing` 00:20–03:50 on 6 July).

---

## 11. Troubleshooting

| Message | Cause / fix |
|---|---|
| `FileNotFoundError: Calendar file not found` | Check the path to the `.ics` file, or pass it as an argument |
| `FileNotFoundError: Config file not found` | Check `--config` and `experiment_dir` in `override_config.yaml` |
| `ValueError: No planned tasks were found` | The file has no planned `VEVENT` with a start and end |
| `ValueError: base_probabilities ...` | The three base probabilities must be > 0 and sum to less than 1 |
| `ModuleNotFoundError: No module named 'yaml'` | Run `pip install -r requirements.txt` |
| `PermissionError` when saving | The Excel file is still open. Close it and run again |
| Persona shows `unknown` | The person id does not match a persona in `persona_config.yaml`; the `default` parameter set is used |
| Metric *Task events not found in event_config.yaml* is not `none` | The calendar comes from a different experiment than `experiment_dir` |
| `ModuleNotFoundError: No module named 'pydantic'` / `'z3'` (validation script) | Run the script with the separate environment from section 12 |
| Validation: *person ... is not in the sampled population* | The calendar comes from a different experiment than `experiment_dir`, or the persona config was changed |

---

## 12. Scoring with calendar-bench (`tools/validate_with_calendar_bench.py`)

calendar-bench has its own validation of a person's calendar. This script runs it on the **plan** and on the **executed calendar(s)** and compares the two. The difference shows how much the overrides damage the qualities the planner guaranteed.

calendar-bench is **not changed**: the script imports its check functions from a local checkout and only reads it.

### What is checked

| Check | What it counts |
|---|---|
| `event` | Event constraints from `event_config.yaml`: duration of one episode (`per_event_duration`), total per day and number of episodes per day (`per_day`), allowed weekdays (`weekday`) |
| `ltl` | LTL rules from `temporal_relation_rules.yaml`, **including the context rules** (e.g. `no_office_when_tired`, `walking_overlaps_physical_opportunity`) |
| `continuity` | Sleep and other events that cross midnight line up with the next day |
| `persona` | Stage cadence of the persona |

Not checked: the population-level checks (instance counts, distributions of characteristics and contexts), because they need all 30 persons, and the Allen pair rules, which calendar-bench only uses in its scenario evaluation.

Many violations in the executed calendar are **intended** by the overrides: a skipped or cut-off workout is shorter than its minimum duration. Report the difference between plan and execution, not the absolute count.

### Why not calendar-bench's `persona validate` command

- Its JSON loader drops the context episodes, so context rules would never fire.
- It pairs files with sampled persons by list position, which only works for a full population.
- Its `load_config()` connects to Neo4j for experiments with contexts.

The script calls the same check functions directly, loads the contexts, and matches the person by id.

### Setup (once)

```bash
git clone https://github.com/MaaniBeigy/calendar-bench path/to/calendar-bench
python -m venv .venv-calendar-bench
.venv-calendar-bench/Scripts/python -m pip install -r tools/requirements-calendar-bench.txt
```

(On macOS/Linux: `.venv-calendar-bench/bin/python`.)

### Run

```bash
python src/simulation.py path/to/calendar.ics
.venv-calendar-bench/Scripts/python tools/validate_with_calendar_bench.py --calendar-bench path/to/calendar-bench path/to/<calendar>_calendar_bench
```

Set `output.executed_ics_replications` higher to score more replications; every `executed_runN` folder becomes a column.

### Output

In the `<calendar>_calendar_bench` folder:

- `validation_report.md`: violations per check, per event/kind and per rule, for the plan, every run, and the difference with the plan;
- `validation_report.json`: the same numbers plus every single violation.

### Check of the conversion

The exported **plan** of `diligent_anxious_active_0000` gives 0 violations, as a calendar generated by calendar-bench should. A test calendar with an office-work block placed on a `tired` context episode gives `no_office_when_tired` violations, so the context rules are active.


---

# Part B: Version 2

## 13. Version 2 (`v2/`)

Version 2 keeps the loop of section 1 and the code of `src/` (calendar loading, slot search, temporal rules, KPIs, calendar-bench export) and changes what goes into the decision and what comes out of it. Every parameter, with its value, source status (`CB`, `LIT-DIR`, `ASSUMPTION`, `[CITE]`) and sensitivity range, is listed in [v2/PARAMETERS.md](v2/PARAMETERS.md). The settings are in `v2/config/v2_config.yaml`; the version 1 config is not read.

### 13.1 Running

```bash
pip install -r v2/requirements.txt
python v2/src/run_simulation.py [calendar.ics]
python v2/src/compare_planning_methods.py [calendar.ics] [--solutions name=folder ...]
python v2/src/sensitivity.py [calendar.ics] [--replications 10] [--health-method human_coach] [--skip-oat] [--skip-ablation]
```

Without a calendar, `default_calendar` from the config is used (`data/diligent_anxious_active_0000.ics`). Output goes to `v2/output/`. Run times on a laptop: about 1, 4 and 9 minutes.

### 13.2 Triggers

| Trigger | Key | Default |
|---|---|---|
| Poisson arrivals during a task (as D1) | `triggers.rate_per_hour` | 0.4 /h |
| One decision at the planned start of every eligible task, and again at the new start after a postponement | `triggers.task_start` | `true` |

Without the task-start trigger a 10-minute (health) task is hit by an arrival only about 6% of the time, so short tasks almost always count as completed. `task_start: false` gives the trigger logic of version 1.

### 13.3 The decision

The multinomial logit of section 6 gets two extra blocks in η_k:

```
η_k = β0_k + β_fill·fill + β_over·earlier_overrides + β_notif·notified        (as v1)
          + Σ_c β_c,k · context_c                                             (context)
          + Σ_t β_t,k · (trait_t − 0.5)                                       (persona)
```

- **Context.** A covariate is 1 when the matching `[ctx:...]` episode is active at the decision moment: `tired` (plus `tired × (intensity − 1)`), `energetic`, `negative_mood` (anxious), `positive_mood` (happy, calm), `stress`, `low_self_efficacy`, `intention_not_to_act`, `intention_to_act`, `bad_weather_outdoor` (only for outdoor tasks) and `location_mismatch` (the current location does not fit the task).
- **Persona.** The Big Five traits from `persona_config.yaml`, centred at `persona.centre` (0.5). `persona.trait_source: mean` uses the persona mean (`loc`); `sample` draws one person per replication from `norm(loc, scale)`. Conscientiousness lowers, neuroticism raises the override probabilities.
- The per-persona base probabilities of version 1 (D15) are dropped: persona differences now come from the traits only.

The **Decisions** sheet shows, per decision, the active context covariates and the context and persona parts of η.

### 13.4 Updating the calendar

| Action | Version 2 |
|---|---|
| Postpone | Next feasible slot in a rolling 7-day window (`postpone_window`; `calendar_week` = until Sunday, `same_day` = version 1). Same feasibility rules as section 7; `postpone_respect_weekdays: true` also respects the allowed weekdays of the event |
| Replace | A concrete activity instead of `UNPLANNED`: rest (`napping`), snack (`snacking`), socialise, read, screen time or walk outside. Weight = base weight × multipliers of the active contexts × trait multipliers. All except screen time are calendar-bench catalog events, so they are scored in the calendar-bench JSON |
| Skip | As version 1 |

### 13.5 Health scenario and planning methods (`compare_planning_methods.py`)

The health tasks of the calendar-bench `healthy_lifestyle_promotion` scenario are added to the person's calendar by several planning methods, and their completion is compared under the same seeds.

| Method | Source |
|---|---|
| `human_coach` | calendar-bench output: `v2/data/scenario_solutions/human_coach/<person>.json` |
| `fcfs_greedy_v2` | Re-implementation of calendar-bench's documented FCFS greedy (earliest free gap that fits) |
| `random_slot_v2` | Random free slot in the task's week |
| `context_aware_v2` | Free slot in the task's week with the highest predicted p(no override); an upper bound, because it plans with the model it is evaluated with |

All methods place the same task batch, taken from the human coach file. A health task counts as completed when all its pieces are executed in full. Domain and sub-class come from `v2/data/health_task_catalog.json` (HealthTasks ontology). Output: `<calendar>_planning_methods.xlsx/.csv/.png`, with completion per method, per domain and per intensity.

To add another method's output: put its `<person_id>.json` files in a folder and pass `--solutions name=path/to/folder`, or add the folder under `health_scenario.solutions` in the config. To add the human coach file of other persons: `python v2/tools/import_calendar_bench.py --calendar-bench path/to/calendar-bench --persons <person_id> ...` (reads calendar-bench, does not change it).

### 13.6 Sensitivity analysis (`sensitivity.py`)

- **One-at-a-time (OAT):** every parameter group is set to its low and high value from PARAMETERS.md, the rest stays at the default. Output: `<calendar>_sensitivity.xlsx/.csv` and the tornado chart `<calendar>_sensitivity_tornado.png`.
- **Ablation:** version 1 inputs → + context → + persona → both, to show how much each block contributes.
- `--health-method human_coach` runs it with the health tasks in the calendar and adds *Health completion* as a KPI.

### 13.7 Limitations of version 2

- No parameter is fitted to data.
- The traits are the persona mean by default; calendar-bench's sampled values per person are not in the `.ics`.
- Some context covariates hardly occur during tasks for `diligent_anxious_active` (`tired` only at night).
- `fill` and the earlier-overrides window are still per day; only replanning looks a week ahead.
- The sensitivity analysis is one-at-a-time (no interactions).

---

# Part C: Version 3

## 14. Version 3 (`v3/`)

Version 2 had one decision about a planned task, at the moment it is due. Version 3 separates the two moments at which a plan is abandoned in daily life: **revising the plan in advance** (the person knows how full the day is, but not how they will feel later) and **executing at the planned time** (starting or not, then finishing or stopping part-way). Versions 1 and 2 are not changed; `v3/config/v3_config.yaml` holds only the new parameters and reads the rest from `v2/config/v2_config.yaml` (`base_config`).

### 14.1 Running

```bash
python v3/src/run_simulation.py [calendar.ics]
python v3/src/stage_ablation.py [calendar.ics] [--replications 10]
python v3/src/compare_planning_methods.py [calendar.ics] [--solutions name=folder ...]
```

Output goes to `v3/output/`.

### 14.2 The stages

| Stage | When | Decision | Inputs |
|---|---|---|---|
| 1. Review | `stages.review.time` (07:00) on the day, or the evening before (`mode: evening_before`) | keep / move to a later day / drop | Planned hours left in the day (centred at 8 h), task intensity, conscientiousness and neuroticism; **no** momentary context |
| 2a. Start | Planned start of the task | none / postpone / skip / replace | The version 2 model (section 13.3) |
| 2b. Progress | Once a task has started | finish / stop part-way | Context at the start (tired, stress, negative mood, energetic), intensity, conscientiousness and neuroticism |

- **Review.** Move and drop are logits against keep, with base probabilities 0.06 / 0.04 on a typical day. A moved task goes to the first feasible slot from the next day on, within `move_window_days` (7), at most `max_moves_per_task` (1) times. Tasks that start before the review time are not reviewed.
- **Progress.** A started task is finished with base probability 0.92. A task that is not finished stops after a uniform 25–85% of its duration (`stop_fraction`); the rest of the slot stays free.
- **Poisson interruptions** are off (`triggers.rate_per_hour: 0.0`), because the progress stage now produces partial execution. A rate > 0 adds them back as in version 2.

The values and their status are listed in [v3/README.md](v3/README.md), section *New parameters*.

### 14.3 Execution states

Every planned task ends in one state:

| State | Meaning |
|---|---|
| completed | Executed in full (possibly after a move or a postponement) |
| partial | Started, but stopped part-way |
| rejected | Dropped at the review |
| missed | Skipped at the planned time, or a postponement without a free slot |
| replaced | Replaced at the planned time by another activity |

Two flags record what happened on the way: *moved at review* and *postponed at start*.

### 14.4 Output

| File / sheet | Contents |
|---|---|
| `<calendar>_v3_simulation.xlsx` → **KPI summary**, **Replications** | Completion rate, share per state, share moved at review, share postponed at start, deviation, postponement delay, decision counts, with 95% CI |
| → **Decisions (run 1)** | Every review, start and progress decision with day load, fill, active context and all probabilities |
| → **Changes** | Every change in every replication, with stage, action, planned and new times, delay and days moved. The planned times are recorded before the task is cut |
| → **Tasks (run 1)** | Every planned task with planned and executed hours, state and the two flags |
| `<calendar>_v3_executed_run1.ics`, `<calendar>_v3_calendar_bench/` | Executed calendar and calendar-bench JSON; score them with section 12 |
| `<calendar>_v3_stage_ablation.xlsx/.csv` | Contribution of each stage: execution only, + review, + progress, full v3 |
| `<calendar>_v3_planning_methods.xlsx/.csv` | Health-task execution states per planning method (same methods as section 13.5) |

### 14.5 Limitations of version 3

- As in version 2, no parameter is fitted to data.
- Tasks that start before the review time are not reviewed.
- The review does not know the momentary context; a variant where the person anticipates their context is a natural extension.
- An unfinished task leaves free time; it is not followed by a replacement activity.

---

# Part D: Input calendars

## 15. The calendar-bench population (`calendar_bench_population/`)

The folder holds the planned calendars of all 30 persons of the calendar-bench experiment `healthy_lifestyle_promotion`, 10 per persona, copied unchanged from calendar-bench's output. The person used for all results so far, `diligent_anxious_active_0000`, is one of them (its `.ics` is identical to `data/diligent_anxious_active_0000.ics`). Details of the files: [calendar_bench_population/README.md](calendar_bench_population/README.md).

| File | Used by |
|---|---|
| `ics/<person_id>.ics` | Input of every version: planned events and `[ctx:...]` context episodes (section 4) |
| `persons/<person_id>.json` | calendar-bench's own person file, including the **sampled characteristics of the person** (Big Five, age, occupation, weekly workouts). Not read by the simulation yet |
| `persons/<person_id>_timeline.tsv` | The same calendar as one table, for inspection in Excel or pandas. Not read by the simulation |

### Running other persons

Pass the calendar as the first argument:

```bash
python src/simulation.py calendar_bench_population/ics/unemployed_family_caregiver_0005.ics
python v3/src/run_simulation.py calendar_bench_population/ics/free_spirited_social_student_0003.ics
```

- The persona is read from the person id, so the persona parameter set (version 1) or the persona traits (versions 2 and 3) follow automatically.
- Version 1 writes its output next to the `.ics`, inside `calendar_bench_population/ics/`. Those files are ignored by git. Keep the repository in a short path on Windows: the output path of version 1 must stay under 260 characters.
- Versions 2 and 3 use the persona **mean** traits (`persona.trait_source: mean`), not the sampled values in `persons/<person_id>.json`.
- The health-scenario comparison (sections 13.5, 14.1) needs the human coach file of the person in `v2/data/scenario_solutions/human_coach/`. The files of all 30 persons are there (imported from calendar-bench commit `2c823c2` with `v2/tools/import_calendar_bench.py`), so the comparison runs for every population calendar.

### Scenario output of the other planning methods

The scenario definitions (`scenarios.yaml`: the weekly ramp of the Progressive Healthy Lifestyle Challenge, the LLM augmenters, greedy, PTIME and DQN) are in `calendar_bench_configs/experiments/healthy_lifestyle_promotion/` and are identical to the calendar-bench repository. calendar-bench publishes only the output of the **human coach**; the output of the other methods needs a calendar-bench run of its own (LLM API keys, Neo4j). When those solution files are available, add them as described in section 13.5.

To run the whole population, loop over the folder, for example in PowerShell:

```powershell
Get-ChildItem calendar_bench_population/ics/*.ics | ForEach-Object { python v3/src/run_simulation.py $_.FullName }
```
