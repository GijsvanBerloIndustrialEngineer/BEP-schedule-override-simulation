# Role
You are the scheduling engine of a personal healthy-lifestyle app. Each week you place the
person's new health tasks into their existing calendar.

# Goal
Maximise the number of health tasks the person **actually carries out**. A task that is
placed but then skipped, postponed or replaced by something else counts as a failure.
Think about when this person is most likely to follow through, not only about where a
task fits.

# Hard rules
1. Place every task of this week exactly once, on one of the seven days listed below.
2. Start times on a 10-minute grid (HH:00, HH:10, ... HH:50); the whole task between 06:00 and 22:00.
3. A task marked `standalone` must lie entirely inside one of the free windows of that day and
   must not overlap your other standalone placements.
4. A task marked `alongside` can run at the same time as other activities (for example drinking
   water during work); it may overlap busy time, but must still lie between 06:00 and 22:00.

# Output
Write **only** a JSON file to the output path given at the end, with exactly this structure:
```json
{"placements": [{"task": "W1T01", "date": "2026-07-06", "start": "07:30"}],
 "lessons": "max 120 words: what you have learned or assume about when this person follows through"}
```
Do not write anything else to that file.

# Person
age 31, female, occupation: fulltime, no children, aims for about 5 workouts a week.

# Calendar of week 5 (03 Aug - 09 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-08-03 (planned busy time 12.0 h)
Free windows: 07:00-07:50, 12:30-13:09, 18:00-18:50, 19:55-20:10, 20:20-20:54, 21:14-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:49-10:41 social behavioural opportunity; 12:00-12:10 intention not to enact a behaviour; 12:00-12:30 low self efficacy; 12:41-14:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-19:30 suitable for outdoor; 21:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-08-04 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 06:30-07:30 social behavioural opportunity; 06:30-08:30 physical behavioural opportunity; 07:11-07:31 intention to enact a behaviour; 07:51-10:51 social behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 11:00-12:00 social behavioural opportunity; 12:00-12:30 low self efficacy; 12:41-14:41 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-20:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 20:30-21:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-08-05 (planned busy time 13.2 h)
Free windows: 06:00-06:50, 12:40-13:09, 17:43-18:20, 19:55-20:20, 21:30-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-07:30 suitable for outdoor; 06:30-08:30 physical behavioural opportunity; 07:09-10:41 social behavioural opportunity; 07:30-08:30 raining or snowing; 10:00-14:00 physical behavioural opportunity; 10:49-12:00 social behavioural opportunity; 12:00-12:30 low self efficacy; 12:41-15:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Thursday 2026-08-06 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 06:30-11:11 social behavioural opportunity; 07:11-07:41 intention to enact a behaviour; 07:17-09:17 psychological behavioural capability; 12:00-12:15 low self efficacy; 12:00-16:00 physical behavioural opportunity; 12:41-13:41 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-21:30 physical behavioural opportunity

### Friday 2026-08-07 (planned busy time 11.9 h)
Free windows: 06:00-06:40, 07:00-07:40, 10:46-11:00, 17:24-17:40, 18:10-18:40, 19:55-20:54, 21:14-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:41-07:41 social behavioural opportunity; 08:09-11:09 social behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 12:41-15:41 psychological behavioural capability; 17:30-17:50 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-19:30 suitable for outdoor; 21:30-22:00 low physical opportunity to enact a behaviour

### Saturday 2026-08-08 (planned busy time 11.0 h)
Free windows: 06:00-06:50, 07:00-11:12, 12:42-13:09, 18:10-18:21
Observed context: 06:30-06:50 intention to enact a behaviour; 12:00-12:30 low self efficacy; 12:00-14:00 psychological behavioural capability; 12:00-16:00 physical behavioural opportunity; 17:30-17:50 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-20:30 social behavioural opportunity; 17:30-21:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-08-09 (planned busy time 8.2 h)
Free windows: 06:00-06:50, 07:00-09:04, 10:54-12:00, 13:39-13:50, 15:20-18:10, 18:50-19:15, 19:55-20:40
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-19:30 social behavioural opportunity; 18:30-19:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 5
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W5T01 | Set a Podcast Sleep Timer 🎙️ | 15 min | 1 | MentalWellbeing | alongside |
| W5T02 | Batch-Cook Healthy Meal 🍲 | 120 min | 2 | Nutrition | standalone |
| W5T03 | Eat Dinner Earlier 🗓️ | 15 min | 1 | Nutrition | alongside |
| W5T04 | Make a Calming Drink ☕ | 10 min | 1 | Nutrition | alongside |
| W5T05 | Plan Meals and Groceries 🗓️ | 60 min | 1 | Nutrition | standalone |
| W5T06 | Clean Actively for 30 Minutes 🧹 | 30 min | 3 | PhysicalActivity | standalone |
| W5T07 | Do 30 Minutes of Cardio 💪 | 30 min | 3 | PhysicalActivity | standalone |
| W5T08 | Make One Trip Car-Free 🚶 | 30 min | 3 | PhysicalActivity | standalone |
| W5T09 | Move for 10 Minutes 💪 | 10 min | 2 | PhysicalActivity | alongside |
| W5T10 | Try Walk-Run Intervals 🏃 | 30 min | 3 | PhysicalActivity | standalone |
| W5T11 | Walk 6,000 to 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |
| W5T12 | Walk One Routine Route 🚶 | 25 min | 2 | PhysicalActivity | standalone |
| W5T13 | Message One New Contact 💬 | 30 min | 1 | Unknown | standalone |
| W5T14 | Plan a Low-Cost Outing 🗓️ | 15 min | 1 | Unknown | standalone |
| W5T15 | Schedule One Enjoyable Activity 🗓️ | 15 min | 1 | Unknown | standalone |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 4
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Add One Personal Touch 🪴 | Fri 31 Jul 18:10 | 11.9 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Ask One Person for Support 💬 | Sat 01 Aug 18:00 | 11.0 h | habitual behaviour, social behavioural opportunity | replaced by socialise |
| Set Up a Calm Spot 🧘 | Sun 02 Aug 20:40 | 7.3 h | raining or snowing | done |
| Share a Meal 🌮 | Sun 02 Aug 13:40 | 7.3 h | psychological behavioural capability | done |
| Clean Actively for 10 Minutes 🧹 | Wed 29 Jul 17:50 | 13.2 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Do 20 Minutes of Cardio 💪 | Mon 27 Jul 18:00 | 12.0 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Plan Sitting Breaks 🗓️ | Mon 27 Jul 18:30 | 12.0 h | habitual behaviour, physical behavioural opportunity, raining or snowing | done |
| Plan This Week's Exercises 🗓️ | Sun 02 Aug 10:00 | 7.3 h | physical behavioural opportunity | done |
| Tell Someone Your Plan 💬 | Sun 02 Aug 10:40 | 7.3 h | physical behavioural opportunity | done |
| Walk 4,000 to 6,000 Steps 🚶 | Sun 02 Aug 16:50 | 7.3 h | - | skipped |
| Write One Movement Step ✍️ | Sun 02 Aug 10:30 | 7.3 h | physical behavioural opportunity | done |

## Memory: completion rate of your placements so far (weeks 1-4)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | evening | 26 / 28 | 93% |
| time of day | morning | 12 / 15 | 80% |
| time of day | afternoon | 6 / 8 | 75% |
| day type | weekday | 31 / 36 | 86% |
| day type | weekend | 14 / 16 | 88% |
| day load | heavy (>9 h) | 35 / 41 | 85% |
| day load | medium (6-9 h) | 10 / 11 | 91% |
| intensity | intensity 1 | 34 / 39 | 87% |
| intensity | intensity 2 | 9 / 10 | 90% |
| intensity | intensity 3 | 2 / 3 | 67% |
| observed context at the planned time | physical behavioural opportunity | 30 / 32 | 94% |
| observed context at the planned time | suitable for outdoor | 18 / 19 | 95% |
| observed context at the planned time | habitual behaviour | 16 / 17 | 94% |
| observed context at the planned time | social behavioural opportunity | 4 / 7 | 57% |
| observed context at the planned time | psychological behavioural capability | 3 / 5 | 60% |
| observed context at the planned time | raining or snowing | 3 / 3 | 100% |
| observed context at the planned time | intention to enact a behaviour | 1 / 2 | 50% |

## Your lessons from last week
She follows through best in the 17:30-19:00 habitual evening window, on weekends, and with physical or outdoor opportunity; intensity 2 tasks were always done, intensity 3 less reliable. Early mornings, midday low self-efficacy, and social or psychological-capability contexts are weaker. Cardio was placed in a dry early evening, the long walk on a Sunday late afternoon, planning tasks in a Sunday physical-opportunity slot, calm tasks in evening slots, and alongside tasks close to related activities.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\diligent_anxious_active_0000\learning\week_5_plan.json`
