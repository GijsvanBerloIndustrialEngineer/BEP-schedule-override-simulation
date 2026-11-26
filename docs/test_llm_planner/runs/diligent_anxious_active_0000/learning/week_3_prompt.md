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

# Calendar of week 3 (20 Jul - 26 Jul 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-07-20 (planned busy time 12.0 h)
Free windows: 07:00-07:50, 12:30-13:09, 18:00-18:50, 19:55-20:10, 20:20-20:54, 21:14-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:49-07:51 social behavioural opportunity; 08:09-10:41 social behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:00-12:15 low self efficacy; 12:41-15:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-20:30 suitable for outdoor; 20:30-21:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-07-21 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 06:30-07:30 social behavioural opportunity; 06:30-08:17 psychological behavioural capability; 07:11-07:31 intention to enact a behaviour; 07:51-10:51 social behavioural opportunity; 11:00-12:00 social behavioural opportunity; 12:00-12:15 low self efficacy; 12:00-16:00 physical behavioural opportunity; 12:41-14:41 psychological behavioural capability; 17:30-18:30 suitable for outdoor; 17:30-19:00 habitual behaviour; 17:30-21:30 physical behavioural opportunity; 18:30-20:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-07-22 (planned busy time 13.2 h)
Free windows: 06:00-06:50, 12:40-13:09, 17:43-18:20, 19:55-20:20, 21:30-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 07:09-11:41 social behavioural opportunity; 12:00-12:10 disposition to attend to one s goals; 12:00-12:30 low self efficacy; 12:41-14:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-19:30 suitable for outdoor

### Thursday 2026-07-23 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 06:30-07:30 social behavioural opportunity; 07:11-07:41 intention to enact a behaviour; 09:51-10:51 social behavioural opportunity; 11:00-12:00 social behavioural opportunity; 12:00-12:15 low self efficacy; 12:41-14:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 19:30-20:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-07-24 (planned busy time 11.9 h)
Free windows: 06:00-06:40, 07:00-07:40, 10:46-11:00, 17:24-17:40, 18:10-18:40, 19:55-20:54, 21:14-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:30-11:09 social behavioural opportunity; 12:00-12:10 disposition to attend to one s goals; 12:00-12:15 low self efficacy; 12:00-14:00 physical behavioural opportunity; 12:41-15:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-19:30 suitable for outdoor

### Saturday 2026-07-25 (planned busy time 11.0 h)
Free windows: 06:00-06:50, 07:00-11:12, 12:42-13:09, 18:10-18:21
Observed context: 06:30-07:00 intention to enact a behaviour; 12:00-12:05 disposition to attend to one s goals; 12:00-12:30 low self efficacy; 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-17:50 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 17:30-20:30 social behavioural opportunity; 17:30-21:30 physical behavioural opportunity; 19:30-21:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-07-26 (planned busy time 7.8 h)
Free windows: 06:00-06:50, 07:00-09:04, 10:54-13:09, 13:39-15:30, 19:30-19:50, 20:10-20:50, 21:10-21:20
Observed context: 06:30-06:50 intention to enact a behaviour; 12:00-12:05 disposition to attend to one s goals; 12:00-12:30 low self efficacy; 12:00-15:00 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-20:30 social behavioural opportunity; 17:30-21:30 physical behavioural opportunity

# Health tasks of week 3
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W3T01 | Log Afternoon Caffeine ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W3T02 | Move in the Afternoon 🚶 | 15 min | 1 | MentalWellbeing | alongside |
| W3T03 | Plan Three Recharge Activities 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W3T04 | Play a Guided Meditation 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W3T05 | Read Something Calm 📖 | 20 min | 1 | MentalWellbeing | standalone |
| W3T06 | Schedule One Social Moment 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W3T07 | Set a Repeatable Bedtime 😴 | 10 min | 1 | MentalWellbeing | alongside |
| W3T08 | Write One Difficult Thought ✍️ | 15 min | 1 | MentalWellbeing | alongside |
| W3T09 | Write One Meaningful Action ✍️ | 15 min | 1 | MentalWellbeing | standalone |
| W3T10 | Write Tomorrow's List ✍️ | 10 min | 1 | MentalWellbeing | alongside |
| W3T11 | Eat One Screen-Free Meal 😌 | 20 min | 1 | Nutrition | standalone |
| W3T12 | Do 15 Minutes of Cardio 💪 | 15 min | 3 | PhysicalActivity | standalone |
| W3T13 | Log Run Wins 🏅 | 5 min | 1 | PhysicalActivity | alongside |
| W3T14 | Tidy Up for 5 Minutes 🧹 | 5 min | 1 | PhysicalActivity | standalone |
| W3T15 | Walk Somewhere Nearby 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W3T16 | Write a Backup Plan 🗓️ | 5 min | 1 | PhysicalActivity | standalone |
| W3T17 | Plan a Coffee Chat ☕ | 30 min | 1 | Unknown | standalone |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 2
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Care for One Friendship 🫂 | Sun 19 Jul 18:40 | 7.8 h | physical behavioural opportunity, raining or snowing, social behavioural opportunity | done |
| Eat A Lighter Dinner 🍽️ | Fri 17 Jul 18:10 | 11.9 h | habitual behaviour, physical behavioural opportunity | done |
| Get Morning Light ☀️ | Mon 13 Jul 06:30 | 12.0 h | intention to enact a behaviour, physical behavioural opportunity | done |
| Schedule a Short Rest Break 🗓️ | Wed 15 Jul 10:00 | 13.2 h | physical behavioural opportunity, social behavioural opportunity | done |
| Step Outside for Fresh Air 🌬️ | Thu 16 Jul 07:50 | 13.5 h | social behavioural opportunity, suitable for outdoor | skipped |
| Write About Stressors ⚡ | Tue 14 Jul 19:00 | 13.5 h | physical behavioural opportunity, suitable for outdoor | done |
| Write Control Table ✍️ | Sat 18 Jul 08:00 | 11.0 h | - | done |
| Log Veggie Servings 📒 | Mon 13 Jul 12:30 | 12.0 h | - | done |
| Swap A Meaty Meal for Legumes 🍲 | Mon 13 Jul 18:20 | 12.0 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Tea Time ☕ | Sun 19 Jul 15:00 | 7.8 h | - | postponed, done later |
| Write a Grocery List 🛒 | Wed 15 Jul 17:50 | 13.2 h | habitual behaviour, physical behavioural opportunity | done |
| Add Five Walk Minutes 🚶 | Mon 13 Jul 18:00 | 12.0 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Log How Movement Felt ✍️ | Fri 17 Jul 17:20 | 11.9 h | - | done |
| Prepare Your Workout Clothes 👟 | Tue 14 Jul 06:30 | 13.5 h | psychological behavioural capability, social behavioural opportunity | skipped |

## Memory: completion rate of your placements so far (weeks 1-2)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | evening | 11 / 11 | 100% |
| time of day | morning | 6 / 9 | 67% |
| time of day | afternoon | 3 / 4 | 75% |
| day type | weekday | 15 / 19 | 79% |
| day type | weekend | 5 / 5 | 100% |
| day load | heavy (>9 h) | 17 / 21 | 81% |
| day load | medium (6-9 h) | 3 / 3 | 100% |
| intensity | intensity 1 | 13 / 16 | 81% |
| intensity | intensity 2 | 7 / 7 | 100% |
| observed context at the planned time | physical behavioural opportunity | 14 / 16 | 88% |
| observed context at the planned time | suitable for outdoor | 8 / 9 | 89% |
| observed context at the planned time | habitual behaviour | 8 / 8 | 100% |
| observed context at the planned time | social behavioural opportunity | 4 / 6 | 67% |
| observed context at the planned time | psychological behavioural capability | 1 / 3 | 33% |
| observed context at the planned time | intention to enact a behaviour | 1 / 2 | 50% |

## Your lessons from last week
She follows through best in the 17:30-19:00 habitual evening window and when outdoor suitability or physical opportunity is observed; weekends are reliable. Early morning around 06:30 is less certain (cardio skipped), so only light alongside tasks go there. Avoid midday low self-efficacy and rainy late evenings. Walks and standalone tasks are placed in dry early evenings; short logging tasks follow the activities they relate to.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\diligent_anxious_active_0000\learning\week_3_plan.json`
