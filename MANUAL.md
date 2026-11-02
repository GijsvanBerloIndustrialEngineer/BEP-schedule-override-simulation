# Simulation Manual

This manual describes how `src/simulation.py` works **in its current version**: what it reads, what it calculates, what it writes, and what it does not do yet.

---

## 1. Overview

The script runs in four steps:

```
.ics calendar ──► 1. Load events ──► 2. Generate Poisson arrivals ──► 3. Calculate metrics ──► 4. Export to Excel
```

| Step | Function | Input | Output |
|---|---|---|---|
| 1 | `load_calendar()` | path to `.ics` file | list of tasks (events) |
| 2 | `generate_triggers()` | tasks, arrival rate, seed | list of arrivals, simulation start and end |
| 3 | `calculate_metrics()` | tasks, arrivals, horizon, rate | list of (metric, value) pairs |
| 4 | `export_to_excel()` | tasks, arrivals, metrics, output path | `.xlsx` file |

`main()` runs these four steps in order and prints the key metrics to the console.

The arrivals generated in step 2 are meant to trigger override events later on. **In the current version they do not change the calendar yet.** See section 7.

---

## 2. Running the simulation

### Requirements

- Python 3.9 or newer
- Packages: `icalendar`, `openpyxl`

```bash
pip install -r requirements.txt
```

### Command

```bash
python src/simulation.py path/to/calendar.ics
```

If you leave out the path, the script uses `DEFAULT_ICS_FILE` at the top of `simulation.py`.

### Output

- An Excel file named `calendar_simulation_metrics.xlsx`, saved **in the same folder as the `.ics` file**.
- A summary of all metrics printed in the console.

If the output file already exists, it is overwritten. On Windows, close the file in Excel before running, or saving fails with a `PermissionError`.

### Parameters

The parameters are set in `main()`:

| Parameter | Default | Meaning |
|---|---|---|
| `rate_per_hour` | `0.4` | Expected number of arrivals per hour (λ of the Poisson process) |
| `seed` | `42` | Random seed. The same seed and calendar always give the same arrivals. |

---

## 3. Step 1: Loading the calendar (`load_calendar`)

The script reads every `VEVENT` in the `.ics` file and stores it as a *task* with these fields:

| Field | Source in ICS | Notes |
|---|---|---|
| `uid` | `UID` | Empty string if missing |
| `summary` | `SUMMARY` | `"Untitled event"` if missing |
| `start` | `DTSTART` | Events **without** `DTSTART` are skipped |
| `end` | `DTEND`, or `DTSTART + DURATION` | `None` if neither is present |
| `duration_hours` | `DTEND − DTSTART`, or `DURATION` | `None` if neither is present; never negative |
| `status` | `STATUS` | e.g. `CONFIRMED`, `TENTATIVE`; empty if missing |
| `all_day` | type of `DTSTART` | `True` if `DTSTART` is a date with no time |

The tasks are then sorted by start time.

### How dates and times are handled (`normalize_datetime`)

- **Times with a timezone** (e.g. `...Z` or with `TZID`) are converted to the **local time of the computer running the script**, and the timezone is then removed. The same file can therefore give different times on computers in different timezones.
- **Times without a timezone** ("floating" times) are used as they are.
- **All-day events** (date only) start at 00:00. Because `DTEND` of an all-day event is the next day in the ICS standard, a one-day all-day event counts as **24 hours**. Such events are included in all duration metrics.

---

## 4. Step 2: Generating arrivals (`generate_triggers`)

### Simulation horizon

- **Start** = the earliest `start` of all tasks
- **End** = the latest `end` of all tasks

### Poisson process

Arrivals follow a Poisson process with rate λ = `rate_per_hour`. Because the times between arrivals in a Poisson process are exponentially distributed with mean 1/λ, the script works like this:

1. Start at the simulation start.
2. Draw a time gap from an exponential distribution, `random.expovariate(λ)`, in hours.
3. Add it to the current time.
4. If the new time is before the simulation end, record an arrival and go back to step 2. Otherwise stop.

With λ = 0.4, the average gap between arrivals is 2.5 hours. The expected number of arrivals is λ × (horizon length in hours).

Each arrival is stored as:

```python
{"time": <datetime>, "type": "POISSON_ARRIVAL", "summary": "Calendar-wide arrival"}
```

Arrivals are **calendar-wide**: they are not linked to a specific task. They are also generated at night and outside planned events.

If `rate_per_hour <= 0`, the script stops with a `ValueError`. If no task has a known end, no arrivals are generated.

---

## 5. Step 3: Metrics (`calculate_metrics`)

| Metric | Calculation |
|---|---|
| Total calendar events | number of loaded tasks |
| Events with known duration | tasks where `duration_hours` is not `None` |
| Total event duration (hours / days) | sum of known durations; days = hours / 24 |
| Average event duration (hours) | total duration / events with known duration |
| Shortest / longest event (+ duration) | task with the smallest / largest duration; on a tie, the first one in time order |
| Simulation start / end | see section 4 |
| Simulation duration (hours / days) | end − start |
| Configured arrival rate (per hour) | `rate_per_hour` |
| Number of Poisson arrivals | number of generated arrivals |
| Observed arrival rate (per hour) | number of arrivals / simulation hours |
| Average time between arrivals (hours) | simulation hours / number of arrivals |
| Total event-hours / simulation-hours | total event duration / simulation duration |

Notes:
- The **observed rate** should be close to the configured rate for long horizons. Differences come from randomness.
- **Event-hours / simulation-hours** is a measure of how full the calendar is. It can be **greater than 1** when events overlap, and all-day events (24 h each) raise it strongly.

---

## 6. Step 4: Excel output (`export_to_excel`)

The workbook has three sheets:

| Sheet | Contents |
|---|---|
| **Metrics** | one row per metric: `Metric`, `Value` |
| **Tasks** | one row per event: UID, Summary, Start, End, Duration (hours), Status, All-day event |
| **Arrivals** | one row per arrival: Arrival number, Arrival time, Arrival type, Description |

Formatting: blue header row, frozen top row, filters on all columns, column widths fitted to the content (max 45), and date/time columns shown as `yyyy-mm-dd hh:mm:ss`.

After saving, the script checks that the file exists and is not empty. Otherwise it raises a `RuntimeError`.

---

## 7. Current limitations

What the simulation **does not do yet** (planned for the BEP):

- **No override logic.** Arrivals are generated but do not change any events. There is no link yet to personas, notifications or task context.
- **No plan update or executed calendar.** The output only describes the planned calendar plus the arrivals. No new `.ics` file of the executed schedule is written.
- **Only one run.** Each run uses one seed. Multiple replications have to be done by changing the seed by hand.

Technical points to keep in mind:

- **Recurring events (`RRULE`) are not expanded.** Only the first occurrence of a repeating event is read, so calendars with recurring events are undercounted.
- **Timezone conversion depends on the computer** (see section 3).
- **Events without an end or duration** are loaded but left out of all duration metrics and of the horizon end.
- Parameters are set in the code, not on the command line (except for the `.ics` path).
- The function `get_duration_hours()` and the `math` import are not used by the current code.

---

## 8. Troubleshooting

| Message | Cause / fix |
|---|---|
| `FileNotFoundError: Calendar file not found` | Check the path to the `.ics` file, or pass it as an argument |
| `ValueError: No calendar events were found` | The file has no `VEVENT` with a `DTSTART` |
| `ModuleNotFoundError: No module named 'icalendar'` | Run `pip install -r requirements.txt` |
| `PermissionError` when saving | The Excel file is still open. Close it and run again. |
| Number of arrivals is 0 | The calendar has no events with an end time, or the horizon is very short |
