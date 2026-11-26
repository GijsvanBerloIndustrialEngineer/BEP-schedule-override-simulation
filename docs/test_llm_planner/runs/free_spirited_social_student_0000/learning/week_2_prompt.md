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

# Calendar of week 2 (13 Jul - 19 Jul 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-07-13 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 16:00-17:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 12:00-13:30 social behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 18:30-21:30 social behavioural opportunity; 19:19-21:19 physical behavioural opportunity

### Tuesday 2026-07-14 (planned busy time 11.3 h)
Free windows: 06:00-07:49, 12:04-13:38, 16:00-17:50, 19:39-19:50
Observed context: 12:00-14:00 psychological behavioural capability; 15:30-21:30 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 18:30-21:30 social behavioural opportunity; 19:30-20:30 raining or snowing

### Wednesday 2026-07-15 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 15:30-17:30 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:49-19:49 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity

### Thursday 2026-07-16 (planned busy time 11.8 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:10, 17:40-17:50, 19:39-19:50
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-16:00 physical behavioural opportunity; 16:00-20:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-21:30 physical behavioural opportunity

### Friday 2026-07-17 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 16:00-20:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-20:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 20:30-21:00 raining or snowing

### Saturday 2026-07-18 (planned busy time 9.8 h)
Free windows: 06:00-07:49, 10:00-12:00, 13:58-14:11, 15:01-17:10, 17:30-17:40, 21:10-21:26, 21:36-21:50
Observed context: 12:00-14:00 psychological behavioural capability; 15:30-21:30 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 18:30-19:00 raining or snowing; 18:30-21:30 social behavioural opportunity

### Sunday 2026-07-19 (planned busy time 10.5 h)
Free windows: 06:00-07:49, 07:59-12:15, 19:30-19:40
Observed context: 12:00-13:30 social behavioural opportunity; 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 15:30-21:30 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-19:30 suitable for outdoor; 18:30-21:30 social behavioural opportunity; 19:30-20:30 raining or snowing

# Health tasks of week 2
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W2T01 | Add One Personal Touch 🪴 | 15 min | 1 | MentalWellbeing | standalone |
| W2T02 | Care for One Friendship 🫂 | 10 min | 1 | MentalWellbeing | standalone |
| W2T03 | Eat A Lighter Dinner 🍽️ | 15 min | 1 | MentalWellbeing | standalone |
| W2T04 | Get Morning Light ☀️ | 5 min | 1 | MentalWellbeing | alongside |
| W2T05 | Plan Three Recharge Activities 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W2T06 | Prepare a Sleep-Friendly Room 😴 | 5 min | 1 | MentalWellbeing | standalone |
| W2T07 | Schedule a Short Rest Break 🗓️ | 10 min | 1 | MentalWellbeing | alongside |
| W2T08 | Step Outside for Fresh Air 🌬️ | 5 min | 1 | MentalWellbeing | alongside |
| W2T09 | Write Control Table ✍️ | 15 min | 1 | MentalWellbeing | alongside |
| W2T10 | Log Veggie Servings 📒 | 5 min | 1 | Nutrition | alongside |
| W2T11 | Swap A Meaty Meal for Legumes 🍲 | 30 min | 1 | Nutrition | standalone |
| W2T12 | Try a Veggie Recipe 🧑‍🍳 | 30 min | 1 | Nutrition | standalone |
| W2T13 | Write a Grocery List 🛒 | 30 min | 1 | Nutrition | standalone |
| W2T14 | Log Run Wins 🏅 | 5 min | 1 | PhysicalActivity | alongside |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 1
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Drink A Glass of Water 🫗 | Tue 07 Jul 10:00 | 11.8 h | - | done |
| Eat One Screen-Free Meal 😌 | Mon 06 Jul 12:30 | 11.7 h | psychological behavioural capability, social behavioural opportunity | replaced by rest |
| Log Fruit Servings 📒 | Wed 08 Jul 14:00 | 11.7 h | - | done |
| Prepare One Better Snack 🍎 | Tue 07 Jul 12:10 | 11.8 h | physical behavioural opportunity, psychological behavioural capability | done |
| Try a Different Fruit 🥝 | Sat 11 Jul 10:00 | 9.8 h | - | done |
| Do 10 Minutes of Cardio 💪 | Fri 10 Jul 07:00 | 11.7 h | physical behavioural opportunity | postponed, done later |
| Log Each Walk 📒 | Wed 08 Jul 13:10 | 11.7 h | physical behavioural opportunity | done |
| Schedule a 30-Minute Walk 🚶 | Wed 08 Jul 12:30 | 11.7 h | physical behavioural opportunity, psychological behavioural capability | done |
| Walk Over 2,000 Steps 🚶 | Sun 12 Jul 10:00 | 10.3 h | - | postponed, done later |
| Tidy Up for 5 Minutes 🧹 | Sat 11 Jul 15:10 | 9.8 h | - | done |

## Memory: completion rate of your placements so far (weeks 1-1)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | afternoon | 5 / 6 | 83% |
| time of day | morning | 4 / 4 | 100% |
| day type | weekday | 6 / 7 | 86% |
| day type | weekend | 3 / 3 | 100% |
| day load | heavy (>9 h) | 9 / 10 | 90% |
| intensity | intensity 1 | 5 / 6 | 83% |
| intensity | intensity 2 | 3 / 3 | 100% |
| observed context at the planned time | physical behavioural opportunity | 4 / 4 | 100% |
| observed context at the planned time | psychological behavioural capability | 2 / 3 | 67% |

## Your lessons from last week
Assumes a free-spirited, social student follows through best on low-effort tasks tied to existing routines (lunch, midday breaks) and on weekend mornings with long free windows. Intense or early workouts are kept few, placed in observed physical-opportunity windows. Evenings are social and unreliable, so they are avoided. Tasks are spread across days rather than stacked.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\free_spirited_social_student_0000\learning\week_2_plan.json`
