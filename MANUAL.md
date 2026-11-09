# Simulation Manual

This manual describes how the override simulation works **in version 1**: what it reads, how it decides on overrides, how it builds the executed calendar, and what it writes. The design decisions D1–D15 it refers to are listed in [docs/REPORT.md](docs/REPORT.md), section 4.

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
| `output.executed_ics_replications` | `1` | Number of runs that get an executed `.ics` |
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
