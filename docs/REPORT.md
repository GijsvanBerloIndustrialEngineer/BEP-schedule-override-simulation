# Report: Simulation Logic, Current Errors and Open Design Choices

This report reviews `src/simulation.py` as of commit `03c11fc` (`main`). It covers three things:

1. how the simulation logic currently works,
2. the errors and incorrect behaviour the simulation shows today,
3. the parts that still have to be decided and improved.

> **Update (version 1, branch `feature/override-simulation`).** Sections 1–3 describe the code as of commit `03c11fc` and are kept as the starting point. Section 4 lists the design decisions taken for version 1, how they are implemented, and which errors from section 2 are now solved.

All claims about the code refer to `src/simulation.py` with line numbers. The figures about the input data come from the test calendar `diligent_anxious_active_0000.ics`, which is the default input (lines 19–21). Python was not available on the machine used for this review, so the figures were counted directly from the `.ics` file rather than from a script run. Arrival counts are therefore given as expected values, not as observed ones.

---

## 1. Simulation logic

### 1.1 Pipeline

`main()` (lines 389–435) runs four steps in a fixed order:

```
.ics file ─► load_calendar() ─► generate_triggers() ─► calculate_metrics() ─► export_to_excel()
```

No step feeds back into an earlier one. The calendar is read once and never changed, so the current program is a *calendar analysis plus arrival generator*, not yet a discrete-event simulation.

### 1.2 Loading the calendar (`load_calendar`, lines 73–122)

- Every `VEVENT` is read (line 86). Events without `DTSTART` are skipped (lines 87–89).
- `normalize_datetime()` (lines 33–45) converts timezone-aware times to the local time of the computer running the script and then strips the timezone (lines 38–39). It turns date-only values into midnight datetimes (lines 42–43).
- The end is taken from `DTEND`. If there is no `DTEND`, it is computed as `DTSTART + DURATION`. Otherwise it is `None` (lines 96–108).
- The duration is clamped at zero with `max(0, …)` (lines 98–100, 102–104).
- Each event becomes a dict with `uid`, `summary`, `start`, `end`, `duration_hours`, `status` and `all_day` (lines 110–119).
- The tasks are sorted by start time (line 121).

### 1.3 Generating triggers (`generate_triggers`, lines 129–170)

- The horizon runs from the earliest `start` to the latest `end` of **all** loaded events (lines 139–146).
- `random.seed(seed)` seeds Python's global random generator (line 151).
- Arrivals follow a homogeneous Poisson process. Exponential inter-arrival times are drawn with `random.expovariate(rate_per_hour)` and added to the clock until the clock passes the horizon end (lines 156–162).
- Each arrival is a dict `{time, type="POISSON_ARRIVAL", summary="Calendar-wide arrival"}` (lines 164–168). It is not linked to any task.

Defaults: λ = 0.4 per hour and seed 42, both hard-coded in `main()` (lines 390 and 404–408).

### 1.4 Metrics (`calculate_metrics`, lines 177–265)

The function computes 18 summary values: event counts, total, average, shortest and longest duration, horizon, configured and observed arrival rate, mean time between arrivals, and the occupancy ratio `total event-hours / horizon-hours` (lines 227–230).

### 1.5 Export (`export_to_excel`, lines 272–382)

The workbook has three sheets: **Metrics**, **Tasks** and **Arrivals**. It is saved next to the input `.ics` file (line 26) and then checked for existence and a non-zero size (lines 377–380).

### 1.6 Comparison with the conceptual model

`docs/CONCEPTUAL_MODEL.md` describes a five-step loop: read calendar → pick task or trigger → override probability → action (none / postpone / skip / replace) → update calendar → repeat. Only step 1 exists in code, and step 2 exists only in part. Steps 3–5 and the loop itself do not exist yet. As a result the **Poisson arrivals have no effect on any output except their own sheet and two metrics**.

---

## 2. Current errors and incorrect behaviour

The issues are ordered by their impact on the results.

### E1. Context annotations are counted as tasks (high impact)

The test calendar has 4,344 `VEVENT`s. Only **1,536** are planned activities, such as `breakfast`, `meeting` or `sleep`. The other **2,808** are context annotations whose summary starts with `[ctx:…]`, such as `[ctx:energy_state] tired` or `[ctx:location] home`, and which carry a `CATEGORIES` field. `load_calendar()` treats every `VEVENT` the same way (lines 86–119), so these annotations are counted as tasks.

Effect on the metrics:

| Metric | All events (current) | Tasks only |
|---|---|---|
| Total calendar events | 4,344 | 1,536 |
| Total event duration | ≈ 3,370 h | ≈ 1,102 h |
| Event-hours / simulation-hours | ≈ **2.50** | ≈ 0.82 |

An occupancy of 2.5 suggests a calendar that is overbooked two and a half times. That figure is an artefact of mixing in the context annotations. The averages and the shortest/longest event are distorted in the same way. The simulation horizon also starts at a context annotation (`2026-07-06 00:00`) instead of at the first task.

**Fix:** split the events into *tasks* and *context* when loading, for example on the `[ctx:` prefix or on `CATEGORIES`. Compute the task metrics on tasks only. Keep the context events as a separate input, because they are exactly what the later *task context* model needs.

### E2. Arrivals fall in free time and during sleep (high impact for the next step)

Arrivals are spread uniformly over the whole horizon (lines 156–168). With λ = 0.4 per hour over a horizon of about 1,348 h, about **539** arrivals are expected. `sleep` takes 6 h a day, so roughly a quarter of those land while the persona is asleep, and many more land in gaps between tasks. The conceptual model states that free time has **no override chance**, yet nothing in the code links an arrival to a task. Once the override logic is added, most arrivals will either do nothing or need a rule to map them to a task.

### E3. Notifications cannot be modelled from the input

The conceptual model uses *notifications* as an input in the first version. The test calendar contains **no `VALARM` components** and no other notification field, and the loader does not read alarms. As things stand, the notification input cannot be taken from the data.

### E4. Fields stored as empty values

The test calendar has **no `UID` and no `STATUS`** on any event. Both columns in the Tasks sheet are therefore empty (lines 111 and 116). This matters once the plan is updated: without a unique id, a postponed or replaced task cannot be traced back to its original. A synthetic id is needed, such as the event index or a hash of summary and start.

### E5. Overlapping events inflate occupancy

Even among the planned tasks alone, about 410 tasks start before the previous task has ended. The occupancy ratio adds up durations (line 187) instead of measuring the union of busy time, so overlaps are counted twice. The same applies to all-day events, which count as 24 h each because `DTEND` is the next day (lines 42–43 and 96–100).

### E6. Invalid data is silently hidden

`max(0, …)` (lines 98–104) turns an event whose end lies before its start into a 0-hour event without any warning. The `end` field still holds the earlier time, so `start` and `end` disagree with `duration_hours`. Such events should be reported or rejected.

### E7. Recurring events are not expanded

`RRULE`, `EXDATE` and `RECURRENCE-ID` are ignored. A recurring event counts once, at its first occurrence. The current test file has no recurring events, but real calendars exported from Outlook or Google do.

### E8. Results depend on the machine's timezone

Timezone-aware times are converted to the *computer's* local timezone (line 39). The same `.ics` file can therefore give different times and horizons on different machines. The test file uses floating times, so it is not affected today.

### E9. Smaller code issues

| # | Location | Issue |
|---|---|---|
| a | lines 48–66 | `get_duration_hours()` duplicates logic from `load_calendar()` and is never called. |
| b | line 3 | `import math` is unused. |
| c | lines 19–21 | The default input is an absolute path into a personal OneDrive folder, so the script fails on any other machine unless a path is passed in. |
| d | line 151 | `random.seed()` seeds the **global** generator. Any later random call, such as the override draws, shares and shifts that stream, so adding one draw changes every arrival after it. Use a dedicated `random.Random(seed)` instance per random stream. |
| e | lines 203–206 | "Average time between arrivals" is computed as `horizon / N`, not as the mean of the gaps. It includes the tail after the last arrival and is slightly biased upwards. |
| f | lines 390, 404–408 | λ and the seed are hard-coded in `main()`. There are no command-line options and no support for replications. |
| g | lines 441–444 | The error is printed and then raised again, so it appears twice in the console. |
| h | line 236 | "Total event duration (days)" is hours / 24. That figure means little when events overlap or when it includes context annotations. |

---

## 3. Open choices and improvements

### 3.1 Design decisions you still have to make

These choices decide the shape of the model. Each comes with options and a suggested default.

| # | Decision | Options | Suggested default for version 1 |
|---|---|---|---|
| D1 | **What triggers an override check?** | (a) Poisson arrivals (current); (b) the start of every planned task; (c) both | (b) the task start. Every task gets exactly one check, which matches "no override chance in free time". Keep Poisson arrivals for *external* disruptions in a later version. |
| D2 | **If Poisson arrivals stay, how is an arrival mapped to a task?** | the active task at that time; the next upcoming task; ignore it if no task is active | The active task; ignore the arrival in free time and during sleep. |
| D3 | **Structure of the override probability** | one *p(override)* followed by a choice of action; or a separate probability per action (multinomial) | Two stages: *p(override)*, then a categorical draw over {postpone, skip, replace}. This is easier to calibrate and to explain. |
| D4 | **Functional form of *p(override)*** | constant; logistic in (fill rate, earlier overrides, notification); rule-based | Logistic: `p = σ(β0 + β1·fill + β2·overrides + β3·notified)`. It stays within [0, 1] and each β can be read on its own. |
| D5 | **Effect of earlier overrides** | raises *p* (procrastination spiral); lowers it (catch-up); none | Decide from the literature. Also fix the **window**: the same day, the last *N* hours, or the whole run. |
| D6 | **"Total task duration" state** | planned hours per day; remaining hours in the day; share of the day that is busy | Remaining planned hours in the current day, as the measure of how full the rest of the day is. |
| D7 | **Postpone rule** | next free slot of at least the task's duration; fixed delay; the next day at the same time; rule per task type | Next free slot on the same day, otherwise skip. Cap the number of postponements per task. |
| D8 | **Replace rule** | a generic "unplanned activity"; a draw from the persona's activity set; leisure only | A generic `UNPLANNED` block of the same length, to keep version 1 simple. |
| D9 | **Which events can be overridden?** | all events; only discretionary tasks (not `sleep` or `wake_up`); rule per category | Exclude fixed and physiological events such as `sleep`, `wake_up`, `meeting`, and the meals if you decide so. Write this down as an explicit list. |
| D10 | **Notification source** | the `VALARM` components in the `.ics`; a parameter (all tasks or a share of them notified); a lead-time model | A parameter: a share *q* of tasks is notified, drawn at random. The test data has no alarms (E3). |
| D11 | **Use of the `[ctx:…]` events** | ignore them; use them as *task context* covariates later; drop them | Separate them now (E1) and keep them for version 2, when task context and personas are added. |
| D12 | **Output of the executed calendar** | `.ics`; a sheet in the Excel workbook; both | Both: an `.ics` that can be compared with the plan, and a sheet listing each change. |
| D13 | **KPIs** | completion rate; share of postponed, skipped or replaced tasks; mean postponement delay; plan–execution deviation in hours | All of these, per run and over replications. |
| D14 | **Replications and seeds** | a single run; *R* replications with seeds `base + r`; common random numbers across scenarios | *R* replications, with confidence intervals on the KPIs. |
| D15 | **Personas (version 2)** | parameters per persona, such as `diligent`, `anxious` and `active` in the file name; parameters derived from the context events | Parameter sets per persona, read from the file name or a configuration file. |

### 3.2 Improvement list

**Fix now (correctness):**

1. Split tasks from `[ctx:…]` context events in `load_calendar()` and compute the metrics on tasks only (E1).
2. Give every task a synthetic id when `UID` is missing (E4).
3. Compute occupancy as the union of busy intervals, not the sum of durations. Report the overlap separately (E5).
4. Warn about, or reject, events whose end lies before their start instead of clamping them silently (E6).
5. Replace `random.seed()` with `rng = random.Random(seed)` and pass `rng` around (E9-d).
6. Remove `get_duration_hours()` and `import math` (E9-a, E9-b).

**Build next (the simulation itself):**

7. An event queue, such as a `heapq` of (time, event), that processes triggers in time order according to D1 and D2.
8. `override_probability(task, state, params)` according to D3–D6.
9. `apply_action()` for postpone, skip and replace according to D7–D9, with an override counter in the state.
10. An executed calendar as output, plus a change log (D12).
11. KPIs and replications (D13, D14).

**Make it robust and reusable:**

12. Command-line options or a configuration file for λ, seed, number of replications and parameters, instead of hard-coded values (E9-f).
13. A relative default input path, such as `data/`, instead of the OneDrive path (E9-c).
14. Expand recurring events, for example with the `recurring-ical-events` package (E7).
15. Choose and document one timezone policy, for example converting to `Europe/Amsterdam` explicitly (E8).
16. Unit tests for loading, Poisson arrivals (observed rate close to λ over long horizons), the override draw and calendar updates.
17. Validation: compare the simulated override rates with values from the literature, or with real plan-versus-actual data if it becomes available.

---

## 4. Decisions taken and status (version 1)

### 4.1 Design decisions D1–D15

| # | Decision taken | Implementation |
|---|---|---|
| D1 | Poisson arrivals trigger override events | `generate_arrivals()`; λ in `override_config.yaml` (`arrivals.rate_per_hour`, 0.4) |
| D2 | The arrival acts on the active task; arrivals in free time and during sleep are ignored | `run_replication()`; ignored arrivals are counted per reason |
| D3 | Multinomial probability per action | Multinomial logit over {none, postpone, skip, replace}, "none" as reference (`action_probabilities()`) |
| D4 | Logistic, with a small rule-based part | Rules: exclusion list, postponement cap (1 per task), postponement without a free slot becomes a skip |
| D5 | Earlier overrides **lower** the chance of a next override | Coefficient −0.40 per earlier override, counted over the same day, capped at 3 |
| D6 | Planned hours left in the day as the fill measure | Union of time-blocking task hours from the arrival to midnight, without sleep |
| D7 | Postpone to the next free slot on the same day | Search from the planned end on the 10-min grid, within 06:00–22:00, no overlap, respecting 22 temporal rules from `temporal_relation_rules.yaml`; otherwise skip |
| D8 | Replace with a generic `UNPLANNED` block of the same length | The remaining part of the task becomes `UNPLANNED` |
| D9 | Explicit exclusion list | Events `sleep`, `napping`, `wake_up`, `go_to_bed`, `breakfast`, `lunch`, `dinner`, `snacking`, `drink_water`, `meeting`; labels `standup`, `external meeting`. The meals are excluded. |
| D10 | A share q of tasks is notified, drawn at random | `notification_share` (0.5), drawn per task per replication |
| D11 | Separate `[ctx:...]` events now, use them in version 2 | Kept as context events; used by the temporal rules and exported to the Context sheet |
| D12 | Both an executed `.ics` and a change list | `<calendar>_executed_run1.ics` and the Changes sheet |
| D13 | Completion rate; shares postponed / skipped / replaced; mean postponement delay; plan–execution deviation | `replication_kpis()`; definitions in the manual, section 8 |
| D14 | R replications with confidence intervals | R = 30, seeds `base_seed + r`, 95% t-interval per KPI |
| D15 | Parameter sets per persona | `override_model.personas` in the config; persona read from the person id |

All probabilities and coefficients are **assumptions** and are listed in `config/override_config.yaml`. They still have to be supported by literature or a sensitivity analysis.

### 4.2 Status of the errors from section 2

| # | Status in version 1 |
|---|---|
| E1 | **Solved.** Context annotations are separated from tasks; metrics use tasks only |
| E2 | **Solved by D2.** Arrivals in free time, during sleep or during excluded tasks are ignored and counted |
| E3 | **Worked around by D10.** Notifications are a parameter; the data still has no alarms |
| E4 | **Solved.** Synthetic ids `evt-<number>`; every executed block keeps its origin task id |
| E5 | **Partly.** The fill measure (D6) uses the union of busy time; the plan metric *task-hours / simulation-hours* is still a sum |
| E6 | Open. Negative durations are still clamped to 0 without a warning |
| E7 | Open. Recurring events are not expanded (calendar-bench files have none) |
| E8 | Open. Timezone conversion depends on the computer (calendar-bench files use floating times) |
| E9 | a, b, d, f, g, h **solved** (unused code removed, separate random streams, config file and command-line options, error shown once, metrics redefined); e solved by removing the metric; c open (default input path) |

### 4.3 First results (test calendar)

`diligent_anxious_active_0000.ics`, default parameters with the `diligent_anxious_active` set, λ = 0.4, R = 30:

| KPI | Mean | 95% CI |
|---|---|---|
| Completion rate (eligible tasks) | 0.953 | [0.950, 0.956] |
| Share postponed | 0.017 | [0.015, 0.018] |
| Share skipped | 0.039 | [0.036, 0.042] |
| Share replaced | 0.008 | [0.006, 0.010] |
| Mean postponement delay (hours) | 1.68 | [1.39, 1.97] |
| Plan–execution deviation (hours) | 30.2 | [28.0, 32.3] |

More than half of the drawn postponements (on average 10.5 per run, against about 8 successful ones) find no free slot on the same day and become a skip. Of the ~551 arrivals per run, about 140 lead to an override decision; the rest fall in free time, sleep or excluded tasks. These numbers follow directly from the assumed parameters and are only a check that the model works, not a result.

### 4.4 Next steps

1. Support the parameters with literature and run a sensitivity analysis (λ, base probabilities, coefficients, q).
2. Version 2: task context (`[ctx:...]` energy state, mood, location) and persona characteristics as inputs of the probability.
3. Simulate the scenario (health) tasks from calendar-bench `scenarios.yaml`, for example the `human_coach` schedules, and compare completion per planning method.

