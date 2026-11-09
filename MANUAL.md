# Simulation Manual

This manual describes how `src/simulation.py` works **in its current version**: what it reads, what it calculates, what it writes, and what it does not do yet.

---

## 1. Overview

Before these steps, the script loads its own settings from `config/override_config.yaml` and the calendar-bench experiment that file points at (see section 2a). The script then runs in four steps:

```
.ics calendar ──► 1. Load events ──► 2. Generate Poisson arrivals ──► 3. Calculate metrics ──► 4. Export to Excel
```

| Step | Function | Input | Output |
|---|---|---|---|
| 1 | `load_calendar()` | path to `.ics` file, experiment | planned tasks and context annotations |
| 2 | `generate_triggers()` | tasks, horizon, experiment, arrival rate, seed | list of arrivals |
| 3 | `calculate_metrics()` | tasks, context, arrivals, horizon, rate, experiment | list of (metric, value) pairs |
| 4 | `export_to_excel()` | tasks, context, arrivals, metrics, persona, output path | `.xlsx` file |

`main()` runs these four steps in order and prints the key metrics to the console.

The arrivals generated in step 2 are meant to trigger override events later on. **In the current version they do not change the calendar yet.** See section 7.

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
python src/simulation.py path/to/calendar.ics --config path/to/override_config.yaml
```

If you leave out the path, the script uses `DEFAULT_ICS_FILE` at the top of `simulation.py`. If you leave out `--config`, it uses `config/override_config.yaml`.

### Output

- An Excel file named `calendar_simulation_metrics.xlsx`, saved **in the same folder as the `.ics` file**.
- A summary of all metrics printed in the console.

If the output file already exists, it is overwritten. On Windows, close the file in Excel before running, or saving fails with a `PermissionError`.

### Parameters

The parameters are set in `config/override_config.yaml`:

| Parameter | Default | Meaning |
|---|---|---|
| `experiment_dir` | `../calendar_bench_configs/experiments/healthy_lifestyle_promotion` | calendar-bench experiment that generated the calendar; relative to the config file |
| `horizon_source` | `experiment` | `experiment`: horizon from `environment.yaml`; `calendar`: first to last planned task |
| `arrivals.rate_per_hour` | `0.4` | Expected number of arrivals per hour (λ of the Poisson process) |
| `arrivals.seed` | `42` | Random seed. The same seed and calendar always give the same arrivals. |

---

## 2a. Link with calendar-bench (`src/calendar_bench_link.py`)

The `.ics` calendars come from a calendar-bench experiment. That experiment is described by the YAML files in `calendar_bench_configs/experiments/<experiment>/` (field reference: `calendar_bench_configs/CONFIG.md`). The simulation reads three of them:

| File | What the simulation uses |
|---|---|
| `environment.yaml` | `horizon` (start date + weeks) as the simulation horizon, `time_windows` (morning, evening, ...) and `daily_window` (waking hours) to label tasks and arrivals |
| `event_config.yaml` | the event catalog: category (eat, work, sports, ...), `is_concurrent`, `is_dividable` and `intensity` of every event |
| `persona_config.yaml` | the persona of the person in the calendar and its characteristics (Big Five, age, ...) |

`temporal_relation_rules.yaml` and `scenarios.yaml` are not used yet. They become relevant when the plan is updated (rules a changed plan must keep) and when task completion is measured (scenario tasks).

How a calendar event is matched to the catalog: calendar-bench writes `SUMMARY:<label> (Person <person id>)` and `DESCRIPTION:Generated event for <label> (<catalog event>), ...`. The label is what the calendar shows (for example `doing research`); the catalog event is the name in `event_config.yaml` (for example `office_work`). `wake_up` and `go_to_bed` are markers derived from `sleep`. The persona is the person id without its number (`diligent_anxious_active_0000` → `diligent_anxious_active`).

---

## 3. Step 1: Loading the calendar (`load_calendar`)

The script reads every `VEVENT` in the `.ics` file. calendar-bench writes two kinds of events:

- **Planned tasks**, such as `breakfast`, `meeting` or `sleep`. These are the *tasks*.
- **Context annotations**, whose summary starts with `[ctx:<category>]` (for example `[ctx:location] home`). These are kept apart as *context events* with their category and value, and are not counted as tasks. They are input for the *task context* model later.

Each event is stored with these fields:

| Field | Source in ICS | Notes |
|---|---|---|
| `uid` | `UID` | calendar-bench files have no `UID`, so a synthetic id `evt-<number>` is used |
| `summary` | `SUMMARY` | `"Untitled event"` if missing |
| `start` | `DTSTART` | Events **without** `DTSTART` are skipped |
| `end` | `DTEND`, or `DTSTART + DURATION` | `None` if neither is present |
| `duration_hours` | `DTEND − DTSTART`, or `DURATION` | `None` if neither is present; never negative |
| `status` | `STATUS` | e.g. `CONFIRMED`, `TENTATIVE`; empty if missing |
| `all_day` | type of `DTSTART` | `True` if `DTSTART` is a date with no time |

Tasks also get the fields from section 2a: `person_id`, `persona`, `label`, `event` (catalog name), `in_catalog`, `is_marker` (`wake_up`/`go_to_bed`), `category`, `is_concurrent`, `is_dividable`, `intensity` and `time_window`.

Tasks and context events are then sorted by start time.

### How dates and times are handled (`normalize_datetime`)

- **Times with a timezone** (e.g. `...Z` or with `TZID`) are converted to the **local time of the computer running the script**, and the timezone is then removed. The same file can therefore give different times on computers in different timezones.
- **Times without a timezone** ("floating" times) are used as they are.
- **All-day events** (date only) start at 00:00. Because `DTEND` of an all-day event is the next day in the ICS standard, a one-day all-day event counts as **24 hours**. Such events are included in all duration metrics.

---

## 4. Step 2: Generating arrivals (`generate_triggers`)

### Simulation horizon

- With `horizon_source: experiment` (default): **start** = `horizon.start_date` 00:00 from `environment.yaml`, **end** = start + `horizon.weeks` weeks.
- With `horizon_source: calendar`: **start** = the earliest `start` of all planned tasks, **end** = the latest `end` (context annotations are not used).

### Poisson process

Arrivals follow a Poisson process with rate λ = `rate_per_hour`. Because the times between arrivals in a Poisson process are exponentially distributed with mean 1/λ, the script works like this:

1. Start at the simulation start.
2. Draw a time gap from an exponential distribution, `rng.expovariate(λ)`, in hours. `rng` is a separate `random.Random(seed)` stream, so later random draws (such as override draws) do not shift the arrivals.
3. Add it to the current time.
4. If the new time is before the simulation end, record an arrival and go back to step 2. Otherwise stop.

With λ = 0.4, the average gap between arrivals is 2.5 hours. The expected number of arrivals is λ × (horizon length in hours).

Each arrival is stored as:

```python
{"time": <datetime>, "type": "POISSON_ARRIVAL", "summary": "Calendar-wide arrival",
 "time_window": "morning", "in_daily_window": True, "active_tasks": "meeting, drink_water"}
```

Arrivals are still **calendar-wide**: they are also generated at night and outside planned events. Each one is labelled with the experiment's time window (`None` outside all windows), whether it falls in the waking window (`daily_window`), and the planned tasks running at that moment (sleep markers excluded). This prepares the choice of how an arrival is linked to a task (REPORT, D1/D2).

If `rate_per_hour <= 0`, the script stops with a `ValueError`.

---

## 5. Step 3: Metrics (`calculate_metrics`)

| Metric | Calculation |
|---|---|
| calendar-bench experiment, Experiment folder | from `override_config.yaml` / `environment.yaml` |
| Person, Persona | from the event summaries, matched to `persona_config.yaml` |
| Planned tasks | number of loaded tasks (context annotations not included) |
| Context annotations | number of `[ctx:...]` events |
| Tasks with known duration | tasks where `duration_hours` is not `None` |
| Task events not found in event_config.yaml | catalog names that could not be matched; should be `none` |
| Total task duration (hours / days) | sum of known durations; days = hours / 24 |
| Average task duration (hours) | total duration / tasks with known duration |
| Shortest / longest task (+ duration) | task with the smallest (non-zero, no marker) / largest duration; on a tie, the first one in time order |
| Horizon source | `experiment` or `calendar` |
| Simulation start / end | see section 4 |
| Simulation duration (hours / days) | end − start |
| Configured arrival rate (per hour) | `rate_per_hour` |
| Number of Poisson arrivals | number of generated arrivals |
| Arrivals inside waking window | arrivals within `daily_window` of `environment.yaml` |
| Arrivals during a planned task | arrivals with at least one active task |
| Observed arrival rate (per hour) | number of arrivals / simulation hours |
| Average time between arrivals (hours) | simulation hours / number of arrivals |
| Total task-hours / simulation-hours | total task duration / simulation duration |

Notes:
- The **observed rate** should be close to the configured rate for long horizons. Differences come from randomness.
- **Task-hours / simulation-hours** is a measure of how full the calendar is. It can be **greater than 1** when events overlap, and all-day events (24 h each) raise it strongly.

---

## 6. Step 4: Excel output (`export_to_excel`)

The workbook has five sheets:

| Sheet | Contents |
|---|---|
| **Metrics** | one row per metric: `Metric`, `Value` |
| **Tasks** | one row per planned task: UID, Summary, Start, End, Duration (hours), Status, All-day event, Person, Persona, Label, Catalog event, Category, In event_config, Sleep marker, Concurrent, Dividable, Intensity, Time window |
| **Context** | one row per context annotation: UID, Context category, Value, Start, End, Duration (hours) |
| **Arrivals** | one row per arrival: Arrival number, Arrival time, Arrival type, Description, Time window, In waking window, Active tasks |
| **Persona** | the persona's characteristics from `persona_config.yaml`: Characteristic, Distribution, Parameters. These are the distributions of the persona, not the values sampled for this person (the `.ics` does not contain those) |

Formatting: blue header row, frozen top row, filters on all columns, column widths fitted to the content (max 45), and date/time columns shown as `yyyy-mm-dd hh:mm:ss`.

After saving, the script checks that the file exists and is not empty. Otherwise it raises a `RuntimeError`.

---

## 7. Current limitations

What the simulation **does not do yet** (planned for the BEP):

- **No override logic.** Arrivals are generated but do not change any events. Persona, catalog and context information is loaded and exported, but not yet used in an override probability.
- **No plan update or executed calendar.** The output only describes the planned calendar plus the arrivals. No new `.ics` file of the executed schedule is written.
- **Only one run.** Each run uses one seed. Multiple replications have to be done by changing the seed by hand.

Technical points to keep in mind:

- **Recurring events (`RRULE`) are not expanded.** Only the first occurrence of a repeating event is read, so calendars with recurring events are undercounted.
- **Timezone conversion depends on the computer** (see section 3).
- **Events without an end or duration** are loaded but left out of all duration metrics and of the horizon end.
- `temporal_relation_rules.yaml` and `scenarios.yaml` are copied but not read yet.

---

## 8. Troubleshooting

| Message | Cause / fix |
|---|---|
| `FileNotFoundError: Calendar file not found` | Check the path to the `.ics` file, or pass it as an argument |
| `ValueError: No planned tasks were found` | The file has no planned `VEVENT` with a `DTSTART` (only `[ctx:...]` events or none) |
| `FileNotFoundError: Config file not found` | Check `--config` and `experiment_dir` in `override_config.yaml` |
| `ModuleNotFoundError: No module named 'yaml'` | Run `pip install -r requirements.txt` |
| Metric *Task events not found in event_config.yaml* is not `none` | The calendar comes from a different experiment than `experiment_dir`; point it at the right experiment |
| `ModuleNotFoundError: No module named 'icalendar'` | Run `pip install -r requirements.txt` |
| `PermissionError` when saving | The Excel file is still open. Close it and run again. |
| Number of arrivals is 0 | The horizon is very short or empty |
