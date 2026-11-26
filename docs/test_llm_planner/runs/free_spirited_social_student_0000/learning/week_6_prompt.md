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
age 21, female, occupation: student, no children, aims for about 2 workouts a week.

# Calendar of week 6 (10 Aug - 16 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-08-10 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:49-19:49 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity

### Tuesday 2026-08-11 (planned busy time 11.3 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:40, 19:10-19:29, 21:10-21:26
Observed context: 12:00-14:00 psychological behavioural capability; 12:00-16:00 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity

### Wednesday 2026-08-12 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-13:30 social behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-19:30 suitable for outdoor; 18:30-21:30 social behavioural opportunity

### Thursday 2026-08-13 (planned busy time 11.3 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:00, 17:00-17:50, 21:10-21:26
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 14:30-19:00 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-21:30 physical behavioural opportunity; 20:00-21:30 social behavioural opportunity

### Friday 2026-08-14 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-20:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-19:30 suitable for outdoor; 19:30-20:00 raining or snowing

### Saturday 2026-08-15 (planned busy time 9.8 h)
Free windows: 06:00-07:49, 10:00-12:00, 13:58-14:11, 15:01-17:10, 17:30-17:40, 21:10-21:26, 21:36-21:50
Observed context: 12:00-13:30 social behavioural opportunity; 12:00-14:00 psychological behavioural capability; 15:30-21:30 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-18:30 suitable for outdoor; 18:30-19:00 raining or snowing; 18:30-21:30 social behavioural opportunity

### Sunday 2026-08-16 (planned busy time 10.3 h)
Free windows: 06:00-07:49, 07:59-12:15, 19:30-19:40, 21:10-21:26
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-16:00 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity; 19:30-21:00 raining or snowing

# Health tasks of week 6
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W6T01 | Ask One Person for Support 💬 | 20 min | 1 | MentalWellbeing | alongside |
| W6T02 | Block Distractions 📵 | 5 min | 1 | MentalWellbeing | alongside |
| W6T03 | Log Afternoon Caffeine ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W6T04 | Move in the Afternoon 🚶 | 15 min | 1 | MentalWellbeing | alongside |
| W6T05 | Plan a Coffee Chat ☕ | 30 min | 1 | MentalWellbeing | standalone |
| W6T06 | Play a Guided Meditation 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W6T07 | Schedule One Enjoyable Activity 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W6T08 | Set a Podcast Sleep Timer 🎙️ | 15 min | 1 | MentalWellbeing | alongside |
| W6T09 | Write Tomorrow's List ✍️ | 10 min | 1 | MentalWellbeing | alongside |
| W6T10 | Batch-Cook Healthy Meal 🍲 | 120 min | 2 | Nutrition | standalone |
| W6T11 | Eat Dinner Earlier 🗓️ | 15 min | 1 | Nutrition | alongside |
| W6T12 | Make a Calming Drink ☕ | 10 min | 1 | Nutrition | alongside |
| W6T13 | Share a Meal 🌮 | 30 min | 1 | Nutrition | standalone |
| W6T14 | Add Five Walk Minutes 🚶 | 15 min | 2 | PhysicalActivity | standalone |
| W6T15 | Clean Actively for 10 Minutes 🧹 | 10 min | 2 | PhysicalActivity | standalone |
| W6T16 | Clean Actively for 20 Minutes 🧹 | 20 min | 2 | PhysicalActivity | standalone |
| W6T17 | Do 20 Minutes of Cardio 💪 | 20 min | 2 | PhysicalActivity | standalone |
| W6T18 | Do 30 Minutes of Cardio 💪 | 30 min | 2 | PhysicalActivity | standalone |
| W6T19 | Make One Trip Car-Free 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W6T20 | Try Walk-Run Intervals 🏃 | 30 min | 2 | PhysicalActivity | standalone |
| W6T21 | Walk 4,000 to 6,000 Steps 🚶 | 60 min | 2 | PhysicalActivity | standalone |
| W6T22 | Walk 6,000 to 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |
| W6T23 | Walk One Routine Route 🚶 | 25 min | 2 | PhysicalActivity | standalone |
| W6T24 | Message One New Contact 💬 | 30 min | 1 | Unknown | standalone |
| W6T25 | Write One Kind No ✍️ | 10 min | 1 | Unknown | standalone |
| W6T26 | Write One Meaningful Action ✍️ | 15 min | 1 | Unknown | standalone |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 5
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Plan Meals and Groceries 🗓️ | Mon 03 Aug 12:10 | 11.7 h | physical behavioural opportunity, psychological behavioural capability | done |
| Plan a Low-Cost Outing 🗓️ | Mon 03 Aug 13:10 | 11.7 h | physical behavioural opportunity | done |
| Do 30 Minutes of Cardio 💪 | Tue 04 Aug 12:10 | 11.8 h | physical behavioural opportunity, psychological behavioural capability | skipped |
| Write One Kind No ✍️ | Tue 04 Aug 12:40 | 11.8 h | physical behavioural opportunity, psychological behavioural capability | done |
| Walk 6,000 to 8,000 Steps 🚶 | Wed 05 Aug 12:10 | 11.7 h | physical behavioural opportunity, psychological behavioural capability | done |
| Try Walk-Run Intervals 🏃 | Thu 06 Aug 12:10 | 11.8 h | physical behavioural opportunity, psychological behavioural capability | skipped |
| Message One New Contact 💬 | Thu 06 Aug 12:40 | 11.8 h | physical behavioural opportunity, psychological behavioural capability | done |
| Clean Actively for 20 Minutes 🧹 | Fri 07 Aug 12:10 | 11.7 h | physical behavioural opportunity, psychological behavioural capability | done |
| Make One Trip Car-Free 🚶 | Fri 07 Aug 12:30 | 11.7 h | physical behavioural opportunity, psychological behavioural capability | done |
| Schedule One Enjoyable Activity 🗓️ | Fri 07 Aug 13:00 | 11.7 h | physical behavioural opportunity | done |
| Batch-Cook Healthy Meal 🍲 | Sat 08 Aug 10:00 | 9.8 h | - | done |
| Set a Podcast Sleep Timer 🎙️ | Sat 08 Aug 21:30 | 9.8 h | - | done |
| Eat Dinner Earlier 🗓️ | Tue 04 Aug 18:00 | 11.8 h | habitual behaviour, physical behavioural opportunity, social behavioural opportunity, suitable for outdoor | done |
| Make a Calming Drink ☕ | Wed 05 Aug 15:00 | 11.7 h | - | done |

## Memory: completion rate of your placements so far (weeks 1-5)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | afternoon | 37 / 45 | 82% |
| time of day | morning | 14 / 17 | 82% |
| time of day | evening | 3 / 3 | 100% |
| day type | weekday | 41 / 51 | 80% |
| day type | weekend | 14 / 15 | 93% |
| day load | heavy (>9 h) | 55 / 66 | 83% |
| intensity | intensity 1 | 38 / 46 | 83% |
| intensity | intensity 2 | 15 / 16 | 94% |
| intensity | intensity 3 | 2 / 4 | 50% |
| observed context at the planned time | psychological behavioural capability | 28 / 36 | 78% |
| observed context at the planned time | physical behavioural opportunity | 28 / 32 | 88% |
| observed context at the planned time | social behavioural opportunity | 11 / 15 | 73% |
| observed context at the planned time | suitable for outdoor | 2 / 2 | 100% |

## Your lessons from last week
Follows through best at weekday lunch (12:00-13:30) and weekend mornings; intensity 2-3 tasks are done reliably, intensity 1 slightly less. Evenings and early mornings are riskier due to social plans, so standalone tasks go at lunch or Saturday morning, with alongside tasks in the afternoon or evening. Keep two or three tasks per day and walks or cardio at midday.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\free_spirited_social_student_0000\learning\week_6_plan.json`
