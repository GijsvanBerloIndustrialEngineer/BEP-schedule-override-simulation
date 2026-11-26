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

# Calendar of week 4 (27 Jul - 02 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-07-27 (planned busy time 12.0 h)
Free windows: 07:00-07:50, 12:30-13:09, 18:00-18:50, 19:55-20:10, 20:20-20:54, 21:14-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:49-07:51 social behavioural opportunity; 08:09-10:41 social behavioural opportunity; 10:00-16:00 physical behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:00-12:15 low self efficacy; 12:41-15:41 psychological behavioural capability; 17:30-17:50 intention not to enact a behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 18:30-19:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-07-28 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 07:11-07:41 intention to enact a behaviour; 07:19-08:19 social behavioural opportunity; 11:00-12:00 social behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:00-12:15 low self efficacy; 12:41-15:41 psychological behavioural capability; 15:30-21:30 physical behavioural opportunity; 17:30-17:50 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor

### Wednesday 2026-07-29 (planned busy time 13.2 h)
Free windows: 06:00-06:50, 12:40-13:09, 17:43-18:20, 19:55-20:20, 21:30-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:30-10:51 social behavioural opportunity; 12:00-12:10 disposition to attend to one s goals; 12:00-12:15 low self efficacy; 12:41-14:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Thursday 2026-07-30 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 07:11-07:31 intention to enact a behaviour; 07:19-08:19 social behavioural opportunity; 11:00-12:00 social behavioural opportunity; 12:00-12:15 low self efficacy; 12:00-14:00 physical behavioural opportunity; 12:41-15:41 psychological behavioural capability; 17:30-19:00 habitual behaviour; 17:30-20:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-07-31 (planned busy time 11.9 h)
Free windows: 06:00-06:40, 07:00-07:40, 10:46-11:00, 17:24-17:40, 18:10-18:40, 19:55-20:54, 21:14-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 06:49-07:49 social behavioural opportunity; 08:09-11:09 social behavioural opportunity; 12:00-12:10 disposition to attend to one s goals; 12:00-14:00 physical behavioural opportunity; 12:41-14:41 psychological behavioural capability; 15:30-19:30 physical behavioural opportunity; 17:30-17:40 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-20:30 suitable for outdoor; 20:30-21:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Saturday 2026-08-01 (planned busy time 11.0 h)
Free windows: 06:00-06:50, 07:00-11:12, 12:42-13:09, 18:10-18:21
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:30-09:30 suitable for outdoor; 09:30-10:00 raining or snowing; 10:00-12:00 physical behavioural opportunity; 12:00-12:10 disposition to attend to one s goals; 12:00-12:30 low self efficacy; 12:00-14:00 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 social behavioural opportunity; 19:30-21:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-08-02 (planned busy time 7.3 h)
Free windows: 06:00-06:50, 07:00-09:20, 09:50-11:30, 12:50-13:09, 13:39-14:40, 16:10-18:00, 20:40-21:20
Observed context: 06:30-07:00 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-12:15 low self efficacy; 12:00-14:00 psychological behavioural capability; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-20:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 20:30-21:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 4
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W4T01 | Add One Personal Touch 🪴 | 15 min | 1 | MentalWellbeing | standalone |
| W4T02 | Ask One Person for Support 💬 | 20 min | 1 | MentalWellbeing | alongside |
| W4T03 | Set Up a Calm Spot 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W4T04 | Share a Meal 🌮 | 30 min | 1 | Nutrition | standalone |
| W4T05 | Clean Actively for 10 Minutes 🧹 | 10 min | 1 | PhysicalActivity | standalone |
| W4T06 | Do 20 Minutes of Cardio 💪 | 20 min | 3 | PhysicalActivity | standalone |
| W4T07 | Plan Sitting Breaks 🗓️ | 5 min | 1 | PhysicalActivity | standalone |
| W4T08 | Plan This Week's Exercises 🗓️ | 30 min | 2 | PhysicalActivity | standalone |
| W4T09 | Tell Someone Your Plan 💬 | 10 min | 1 | PhysicalActivity | alongside |
| W4T10 | Walk 4,000 to 6,000 Steps 🚶 | 60 min | 2 | PhysicalActivity | standalone |
| W4T11 | Write One Movement Step ✍️ | 5 min | 1 | PhysicalActivity | alongside |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 3
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Log Afternoon Caffeine ☕ | Mon 20 Jul 15:00 | 12.0 h | psychological behavioural capability | done |
| Move in the Afternoon 🚶 | Tue 21 Jul 15:00 | 13.5 h | physical behavioural opportunity | done |
| Plan Three Recharge Activities 🗓️ | Wed 22 Jul 18:00 | 13.2 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Play a Guided Meditation 🧘 | Fri 24 Jul 20:00 | 11.9 h | - | replaced by snack |
| Read Something Calm 📖 | Sun 26 Jul 11:00 | 7.8 h | - | done |
| Schedule One Social Moment 🗓️ | Fri 24 Jul 20:20 | 11.9 h | - | postponed, done later |
| Set a Repeatable Bedtime 😴 | Sun 26 Jul 21:00 | 7.8 h | physical behavioural opportunity | done |
| Write One Difficult Thought ✍️ | Thu 23 Jul 19:00 | 13.5 h | physical behavioural opportunity, suitable for outdoor | done |
| Write One Meaningful Action ✍️ | Sat 25 Jul 10:40 | 11.0 h | - | postponed, done later |
| Write Tomorrow's List ✍️ | Wed 22 Jul 21:30 | 13.2 h | - | done |
| Eat One Screen-Free Meal 😌 | Fri 24 Jul 18:10 | 11.9 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Do 15 Minutes of Cardio 💪 | Wed 22 Jul 20:00 | 13.2 h | - | done |
| Log Run Wins 🏅 | Wed 22 Jul 18:20 | 13.2 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Tidy Up for 5 Minutes 🧹 | Mon 20 Jul 18:40 | 12.0 h | physical behavioural opportunity, suitable for outdoor | done |
| Walk Somewhere Nearby 🚶 | Mon 20 Jul 18:00 | 12.0 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Write a Backup Plan 🗓️ | Mon 20 Jul 18:30 | 12.0 h | physical behavioural opportunity, suitable for outdoor | done |
| Plan a Coffee Chat ☕ | Sat 25 Jul 10:00 | 11.0 h | - | done |

## Memory: completion rate of your placements so far (weeks 1-3)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | evening | 21 / 22 | 95% |
| time of day | morning | 9 / 12 | 75% |
| time of day | afternoon | 5 / 6 | 83% |
| day type | weekday | 27 / 32 | 84% |
| day type | weekend | 9 / 9 | 100% |
| day load | heavy (>9 h) | 31 / 36 | 86% |
| day load | medium (6-9 h) | 5 / 5 | 100% |
| intensity | intensity 1 | 27 / 31 | 87% |
| intensity | intensity 2 | 8 / 8 | 100% |
| intensity | intensity 3 | 1 / 2 | 50% |
| observed context at the planned time | physical behavioural opportunity | 23 / 25 | 92% |
| observed context at the planned time | suitable for outdoor | 15 / 16 | 94% |
| observed context at the planned time | habitual behaviour | 12 / 12 | 100% |
| observed context at the planned time | social behavioural opportunity | 4 / 6 | 67% |
| observed context at the planned time | psychological behavioural capability | 2 / 4 | 50% |
| observed context at the planned time | intention to enact a behaviour | 1 / 2 | 50% |

## Your lessons from last week
She completes tasks best in the 17:30-19:00 habitual evening window, on weekends, and when physical or outdoor opportunity is observed; intensity 2 tasks were always done. Early mornings and midday low self-efficacy are weaker, and social or psychological-capability contexts are less reliable. Placed cardio and walk in dry early evenings, calm standalone tasks in dry evening or weekend slots, and short alongside logs right after related activities.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\diligent_anxious_active_0000\learning\week_4_plan.json`
