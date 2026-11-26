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

# Calendar of week 3 (20 Jul - 26 Jul 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-07-20 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-20:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-20:30 suitable for outdoor; 17:49-19:49 physical behavioural opportunity; 20:30-21:00 raining or snowing

### Tuesday 2026-07-21 (planned busy time 11.3 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:20, 17:20-17:40, 19:10-19:29, 19:39-19:50
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 16:00-20:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-20:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity

### Wednesday 2026-07-22 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-13:30 social behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-17:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:30 physical behavioural opportunity; 18:30-19:30 raining or snowing; 18:30-21:30 social behavioural opportunity

### Thursday 2026-07-23 (planned busy time 11.8 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:10, 17:40-17:50, 19:39-19:50
Observed context: 12:00-14:00 psychological behavioural capability; 12:00-16:00 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-21:30 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity

### Friday 2026-07-24 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-13:00 suitable for outdoor; 12:00-13:30 social behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-17:30 social behavioural opportunity; 16:30-18:30 suitable for outdoor; 17:30-18:30 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 18:30-20:00 raining or snowing; 18:30-21:30 social behavioural opportunity

### Saturday 2026-07-25 (planned busy time 9.8 h)
Free windows: 06:00-07:49, 10:00-12:00, 13:58-14:11, 15:01-17:10, 17:30-17:40, 21:10-21:26, 21:36-21:50
Observed context: 12:00-14:00 psychological behavioural capability; 15:30-21:30 physical behavioural opportunity; 16:00-20:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 18:30-19:00 raining or snowing

### Sunday 2026-07-26 (planned busy time 10.3 h)
Free windows: 06:00-07:49, 07:59-12:15, 19:30-19:40, 21:10-21:26
Observed context: 12:00-13:30 social behavioural opportunity; 12:00-14:00 psychological behavioural capability; 15:30-21:30 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-20:30 suitable for outdoor; 18:30-21:30 social behavioural opportunity; 20:30-21:30 raining or snowing

# Health tasks of week 3
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W3T01 | Log Afternoon Caffeine ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W3T02 | Play a Guided Meditation 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W3T03 | Read Something Calm 📖 | 20 min | 1 | MentalWellbeing | standalone |
| W3T04 | Schedule One Social Moment 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W3T05 | Set a Repeatable Bedtime 😴 | 10 min | 1 | MentalWellbeing | alongside |
| W3T06 | Write One Meaningful Action ✍️ | 15 min | 1 | MentalWellbeing | standalone |
| W3T07 | Write Tomorrow's List ✍️ | 10 min | 1 | MentalWellbeing | alongside |
| W3T08 | Add Five Walk Minutes 🚶 | 15 min | 2 | PhysicalActivity | standalone |
| W3T09 | Do 15 Minutes of Cardio 💪 | 15 min | 2 | PhysicalActivity | standalone |
| W3T10 | Do 20 Minutes of Cardio 💪 | 20 min | 2 | PhysicalActivity | standalone |
| W3T11 | Log How Movement Felt ✍️ | 5 min | 1 | PhysicalActivity | alongside |
| W3T12 | Prepare Your Workout Clothes 👟 | 10 min | 1 | PhysicalActivity | alongside |
| W3T13 | Walk 4,000 to 6,000 Steps 🚶 | 60 min | 2 | PhysicalActivity | standalone |
| W3T14 | Walk a New Route 🚶 | 15 min | 2 | PhysicalActivity | standalone |
| W3T15 | Write a Backup Plan 🗓️ | 5 min | 1 | PhysicalActivity | standalone |
| W3T16 | Plan a Coffee Chat ☕ | 30 min | 1 | Unknown | standalone |
| W3T17 | Write One Difficult Thought ✍️ | 15 min | 1 | Unknown | alongside |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 2
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Add One Personal Touch 🪴 | Mon 13 Jul 12:10 | 11.7 h | physical behavioural opportunity, psychological behavioural capability, social behavioural opportunity | done |
| Care for One Friendship 🫂 | Tue 14 Jul 12:10 | 11.3 h | psychological behavioural capability | done |
| Eat A Lighter Dinner 🍽️ | Tue 14 Jul 17:10 | 11.3 h | physical behavioural opportunity, social behavioural opportunity | done |
| Get Morning Light ☀️ | Mon 13 Jul 07:00 | 11.7 h | physical behavioural opportunity | skipped |
| Plan Three Recharge Activities 🗓️ | Sat 18 Jul 10:00 | 9.8 h | - | done |
| Prepare a Sleep-Friendly Room 😴 | Sun 19 Jul 10:00 | 10.5 h | - | done |
| Schedule a Short Rest Break 🗓️ | Wed 15 Jul 10:00 | 11.7 h | - | postponed, done later |
| Step Outside for Fresh Air 🌬️ | Thu 16 Jul 12:30 | 11.8 h | physical behavioural opportunity, psychological behavioural capability | done |
| Write Control Table ✍️ | Fri 17 Jul 12:10 | 11.7 h | physical behavioural opportunity, psychological behavioural capability | replaced by snack |
| Log Veggie Servings 📒 | Wed 15 Jul 13:00 | 11.7 h | physical behavioural opportunity, psychological behavioural capability | done |
| Swap A Meaty Meal for Legumes 🍲 | Sat 18 Jul 10:30 | 9.8 h | - | done |
| Try a Veggie Recipe 🧑‍🍳 | Sun 19 Jul 10:30 | 10.5 h | - | done |
| Write a Grocery List 🛒 | Wed 15 Jul 12:10 | 11.7 h | physical behavioural opportunity, psychological behavioural capability | done |
| Log Run Wins 🏅 | Fri 17 Jul 14:00 | 11.7 h | - | done |

## Memory: completion rate of your placements so far (weeks 1-2)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | afternoon | 12 / 14 | 86% |
| time of day | morning | 9 / 10 | 90% |
| day type | weekday | 14 / 17 | 82% |
| day type | weekend | 7 / 7 | 100% |
| day load | heavy (>9 h) | 21 / 24 | 88% |
| intensity | intensity 1 | 17 / 20 | 85% |
| intensity | intensity 2 | 3 / 3 | 100% |
| observed context at the planned time | physical behavioural opportunity | 9 / 11 | 82% |
| observed context at the planned time | psychological behavioural capability | 7 / 9 | 78% |
| observed context at the planned time | social behavioural opportunity | 2 / 3 | 67% |

## Your lessons from last week
Low-effort intensity-1 tasks are done reliably; midday free windows (12:00-13:30) and weekend mornings with long free windows work best. Evenings are social and unreliable, so only one short task sits near 17:00. Tasks are spread over the week with at most two or three per day, and alongside tasks sit at routine moments such as lunch and morning.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\free_spirited_social_student_0000\learning\week_3_plan.json`
