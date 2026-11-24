# Version 3: two-stage execution model

Version 2 had **one decision** about a planned task, taken at the moment it is due (plus random interruptions). In daily life there are two different moments:

1. **Revising the plan in advance.** In the morning, or the evening before, a person looks at the day and keeps, moves or drops tasks. At that moment they know how full the day is and how heavy a task is, but not yet how tired or anxious they will be at 18:00.
2. **Executing at the planned time.** When the moment comes, they start or not, depending on their energy, mood, location and reminders. Once started, they finish the task or stop part-way.

Version 3 models these as separate stages. Versions 1 (`../src`) and 2 (`../v2`) are not changed; v3 imports their code and uses the v2 config as its base.

| Stage | When | Decision | Inputs |
|---|---|---|---|
| 1. Review (new) | 07:00 on the day (or 21:00 the evening before) | keep / move to a later day / drop | Planned hours of the day, task intensity, persona traits; **no** momentary context |
| 2a. Start | Planned start of the task | none / postpone / skip / replace (v2 model) | As v2: day load, earlier overrides, notification, momentary context, traits |
| 2b. Progress (new) | After a task starts | finish / stop part-way | Context at the start (tired, stress, anxious, energetic), intensity, traits |

Poisson interruptions during a task are off by default: the progress model now produces partial execution. Set `triggers.rate_per_hour` > 0 to add them back.

## Execution states

Every planned task ends in one of the states of the plan of work (SRQ2):

| State | Meaning |
|---|---|
| completed | Executed in full (possibly after a move or a postponement) |
| partial | Started, but stopped part-way |
| rejected | Dropped at the review |
| missed | Skipped at the planned time (or a postponement without a free slot) |
| replaced | Replaced at the planned time by another activity |

Two flags record what happened on the way: *moved at review* and *postponed at start*.

## Run it

From the repository root:

```bash
python v3/src/run_simulation.py
```

```bash
python v3/src/stage_ablation.py --replications 10
```

| Script | Output (in `v3/output/`, not in git) |
|---|---|
| `run_simulation.py` | `<calendar>_v3_simulation.xlsx` (KPIs with 95% CI, execution states, review and start decisions, changes, tasks), executed `.ics`, calendar-bench JSON |
| `stage_ablation.py` | Contribution of each stage: execution only, + review, + progress, full v3 |

## New parameters

All in [`config/v3_config.yaml`](config/v3_config.yaml); the rest comes from `../v2/config/v2_config.yaml` (see `../v2/PARAMETERS.md`).

| Parameter | Value | Status |
|---|---|---|
| Review time and mode | 07:00, same morning | Assumption |
| Review base probabilities (move, drop) on a typical day of 8 planned hours | 0.06, 0.04 | Assumption |
| Effect of day load per hour above 8 (move, drop) | +0.08, +0.10 | Direction: planning fallacy (Buehler et al., 1994); size assumed |
| Effect of intensity per level (move, drop) | +0.15, +0.20 | Assumption |
| Trait effects at review: conscientiousness (move, drop) | −1.0, −2.0 | Direction: Steel (2007); size assumed |
| Trait effects at review: neuroticism | +0.5 | Direction: Steel (2007); size assumed |
| Moves: max per task, window | 1, 7 days | Assumption |
| Base probability that a started task is finished | 0.92 | Assumption. [CITE] a source for task completion once started |
| Progress: tired, stress, anxious, energetic | −0.6, −0.4, −0.3, +0.3 | Direction: Liao et al. (2015); size assumed |
| Progress: intensity per level | −0.3 | Assumption |
| Progress: conscientiousness, neuroticism | +1.5, −0.3 | Direction: Claessens et al. (2010); Steel (2007); size assumed |
| Stop point of an unfinished task | uniform 25–85% of its duration | Assumption |

## Limitations

- As in v2, no parameter is fitted to data.
- Tasks that start before the review time (before 07:00) are not reviewed.
- The review does not know the momentary context. A variant where the person anticipates their context (a forecast) is a natural extension.
- An unfinished task leaves free time; it is not followed by a replacement activity.
