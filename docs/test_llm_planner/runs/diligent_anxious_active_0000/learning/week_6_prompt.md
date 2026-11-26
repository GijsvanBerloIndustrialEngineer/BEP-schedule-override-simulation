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

# Calendar of week 6 (10 Aug - 16 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-08-10 (planned busy time 12.0 h)
Free windows: 07:00-07:50, 12:30-13:09, 18:00-18:50, 19:55-20:10, 20:20-20:54, 21:14-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:49-10:41 social behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 11:00-12:00 social behavioural opportunity; 12:00-12:30 low self efficacy; 12:41-14:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 18:30-20:00 raining or snowing

### Tuesday 2026-08-11 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 06:30-07:30 social behavioural opportunity; 07:11-07:41 intention to enact a behaviour; 07:17-09:17 psychological behavioural capability; 10:11-11:11 social behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:00-12:30 low self efficacy; 12:00-14:00 physical behavioural opportunity; 12:41-13:41 psychological behavioural capability; 15:30-21:30 physical behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-20:30 suitable for outdoor; 20:30-22:00 raining or snowing

### Wednesday 2026-08-12 (planned busy time 13.2 h)
Free windows: 06:00-06:50, 12:40-13:09, 17:43-18:20, 19:55-20:20, 21:30-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:30-10:51 social behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:41-14:41 psychological behavioural capability; 17:30-17:50 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:30 physical behavioural opportunity; 18:30-19:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Thursday 2026-08-13 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 06:30-07:30 social behavioural opportunity; 06:30-08:30 physical behavioural opportunity; 07:11-07:31 intention to enact a behaviour; 10:00-12:00 physical behavioural opportunity; 10:11-11:11 social behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:00-12:30 low self efficacy; 12:41-14:41 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-21:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-08-14 (planned busy time 12.5 h)
Free windows: 06:00-06:50, 07:00-07:20, 10:56-11:10, 13:39-13:50, 18:10-18:20, 18:50-19:00, 19:20-19:50, 20:40-20:54, 21:14-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 07:09-09:09 social behavioural opportunity; 11:00-12:00 social behavioural opportunity; 12:00-12:30 low self efficacy; 12:51-14:51 psychological behavioural capability; 17:30-17:50 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Saturday 2026-08-15 (planned busy time 10.2 h)
Free windows: 06:00-06:50, 07:00-08:50, 09:20-11:12, 12:42-13:09, 13:39-14:10, 18:10-18:21
Observed context: 06:30-06:50 intention to enact a behaviour; 10:00-12:00 physical behavioural opportunity; 12:00-12:15 low self efficacy; 12:00-14:00 psychological behavioural capability; 17:30-19:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 17:30-20:30 social behavioural opportunity; 18:21-20:21 physical behavioural opportunity

### Sunday 2026-08-16 (planned busy time 8.2 h)
Free windows: 06:10-06:50, 07:00-09:04, 10:54-11:50, 12:50-13:09, 13:39-14:10, 15:40-18:10, 18:50-19:15, 19:55-20:30, 21:30-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 12:00-12:10 disposition to attend to one s goals; 12:00-12:15 low self efficacy; 12:00-14:00 physical behavioural opportunity; 12:00-15:00 psychological behavioural capability; 15:30-19:30 physical behavioural opportunity; 17:30-17:50 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:30 social behavioural opportunity; 18:30-20:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 6
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W6T01 | Ask One Person for Support 💬 | 20 min | 1 | MentalWellbeing | alongside |
| W6T02 | Block Distractions 📵 | 5 min | 1 | MentalWellbeing | alongside |
| W6T03 | Eat Dinner Earlier 🗓️ | 15 min | 1 | MentalWellbeing | alongside |
| W6T04 | Log Afternoon Caffeine ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W6T05 | Make a Calming Drink ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W6T06 | Message One New Contact 💬 | 30 min | 1 | MentalWellbeing | standalone |
| W6T07 | Move in the Afternoon 🚶 | 15 min | 2 | MentalWellbeing | alongside |
| W6T08 | Plan a Low-Cost Outing 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W6T09 | Play a Guided Meditation 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W6T10 | Schedule One Enjoyable Activity 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W6T11 | Set a Podcast Sleep Timer 🎙️ | 15 min | 1 | MentalWellbeing | alongside |
| W6T12 | Write One Kind No ✍️ | 10 min | 1 | MentalWellbeing | standalone |
| W6T13 | Write One Meaningful Action ✍️ | 15 min | 1 | MentalWellbeing | standalone |
| W6T14 | Write Tomorrow's List ✍️ | 10 min | 1 | MentalWellbeing | alongside |
| W6T15 | Batch-Cook Healthy Meal 🍲 | 120 min | 2 | Nutrition | standalone |
| W6T16 | Share a Meal 🌮 | 30 min | 1 | Nutrition | standalone |
| W6T17 | Clean Actively for 10 Minutes 🧹 | 10 min | 2 | PhysicalActivity | standalone |
| W6T18 | Clean Actively for 20 Minutes 🧹 | 20 min | 2 | PhysicalActivity | standalone |
| W6T19 | Do 20 Minutes of Cardio 💪 | 20 min | 3 | PhysicalActivity | standalone |
| W6T20 | Do 30 Minutes of Cardio 💪 | 30 min | 3 | PhysicalActivity | standalone |
| W6T21 | Make One Trip Car-Free 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W6T22 | Schedule a 30-Minute Walk 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W6T23 | Try Walk-Run Intervals 🏃 | 30 min | 3 | PhysicalActivity | standalone |
| W6T24 | Walk 4,000 to 6,000 Steps 🚶 | 60 min | 2 | PhysicalActivity | standalone |
| W6T25 | Walk 6,000 to 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |
| W6T26 | Write One Difficult Thought ✍️ | 15 min | 1 | Unknown | alongside |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 5
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Set a Podcast Sleep Timer 🎙️ | Mon 03 Aug 21:20 | 12.0 h | - | done |
| Batch-Cook Healthy Meal 🍲 | Sat 08 Aug 09:00 | 11.0 h | - | done |
| Eat Dinner Earlier 🗓️ | Tue 04 Aug 17:40 | 13.5 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Make a Calming Drink ☕ | Wed 05 Aug 20:00 | 13.2 h | - | done |
| Plan Meals and Groceries 🗓️ | Sun 09 Aug 16:30 | 8.2 h | - | done |
| Clean Actively for 30 Minutes 🧹 | Sun 09 Aug 17:30 | 8.2 h | habitual behaviour, intention not to enact a behaviour, physical behavioural opportunity, social behavioural opportunity, suitable for outdoor | done |
| Do 30 Minutes of Cardio 💪 | Mon 03 Aug 18:00 | 12.0 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Make One Trip Car-Free 🚶 | Fri 07 Aug 18:10 | 11.9 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | skipped |
| Move for 10 Minutes 💪 | Tue 04 Aug 18:00 | 13.5 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Try Walk-Run Intervals 🏃 | Wed 05 Aug 17:50 | 13.2 h | habitual behaviour, physical behavioural opportunity | skipped |
| Walk 6,000 to 8,000 Steps 🚶 | Sun 09 Aug 15:20 | 8.2 h | - | done |
| Walk One Routine Route 🚶 | Sun 09 Aug 18:50 | 8.2 h | habitual behaviour, physical behavioural opportunity, raining or snowing, social behavioural opportunity | done |
| Message One New Contact 💬 | Fri 07 Aug 20:00 | 11.9 h | - | done |
| Plan a Low-Cost Outing 🗓️ | Mon 03 Aug 18:30 | 12.0 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Schedule One Enjoyable Activity 🗓️ | Thu 06 Aug 19:00 | 13.5 h | physical behavioural opportunity | done |

## Memory: completion rate of your placements so far (weeks 1-5)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | evening | 36 / 40 | 90% |
| time of day | morning | 13 / 16 | 81% |
| time of day | afternoon | 8 / 10 | 80% |
| day type | weekday | 39 / 46 | 85% |
| day type | weekend | 19 / 21 | 90% |
| day load | heavy (>9 h) | 44 / 52 | 85% |
| day load | medium (6-9 h) | 14 / 15 | 93% |
| intensity | intensity 1 | 41 / 46 | 89% |
| intensity | intensity 2 | 13 / 14 | 93% |
| intensity | intensity 3 | 4 / 7 | 57% |
| observed context at the planned time | physical behavioural opportunity | 37 / 41 | 90% |
| observed context at the planned time | habitual behaviour | 22 / 25 | 88% |
| observed context at the planned time | suitable for outdoor | 23 / 25 | 92% |
| observed context at the planned time | social behavioural opportunity | 6 / 9 | 67% |
| observed context at the planned time | psychological behavioural capability | 3 / 5 | 60% |
| observed context at the planned time | raining or snowing | 4 / 4 | 100% |
| observed context at the planned time | intention to enact a behaviour | 1 / 2 | 50% |

## Your lessons from last week
She follows through best in the 17:30-19:00 habitual evening window and on weekends, with physical or outdoor opportunity. Evenings had 93% completion; mornings and afternoons were weaker, as were social and psychological-capability contexts. Intensity 3 is less reliable, so I spread those tasks across separate evenings. Long tasks go in large weekend windows, planning tasks in evening slots, and alongside tasks near related activities.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\diligent_anxious_active_0000\learning\week_6_plan.json`
