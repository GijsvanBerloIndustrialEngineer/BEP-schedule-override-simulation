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

# Calendar of week 2 (13 Jul - 19 Jul 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-07-13 (planned busy time 12.0 h)
Free windows: 07:00-07:50, 12:30-13:09, 18:00-18:50, 19:55-20:10, 20:20-20:54, 21:14-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:49-07:51 social behavioural opportunity; 08:09-10:41 social behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:41-15:41 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-20:30 suitable for outdoor; 21:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-07-14 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 06:30-07:30 social behavioural opportunity; 06:30-08:17 psychological behavioural capability; 07:11-07:31 intention to enact a behaviour; 07:51-10:51 social behavioural opportunity; 11:00-12:00 social behavioural opportunity; 12:00-12:10 disposition to attend to one s goals; 12:00-12:30 low self efficacy; 12:00-16:00 physical behavioural opportunity; 12:41-14:41 psychological behavioural capability; 17:30-17:50 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-20:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 20:30-21:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-07-15 (planned busy time 13.2 h)
Free windows: 06:00-06:50, 12:40-13:09, 17:43-18:20, 19:55-20:20, 21:30-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:30-10:51 social behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 12:00-12:10 disposition to attend to one s goals; 12:41-14:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Thursday 2026-07-16 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 06:30-08:30 suitable for outdoor; 07:19-11:11 social behavioural opportunity; 07:29-07:49 intention to enact a behaviour; 10:00-12:00 physical behavioural opportunity; 12:41-15:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 19:30-21:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-07-17 (planned busy time 11.9 h)
Free windows: 06:00-06:40, 07:00-07:40, 10:46-11:00, 17:24-17:40, 18:10-18:40, 19:55-20:54, 21:14-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:30-08:30 suitable for outdoor; 06:49-07:49 social behavioural opportunity; 08:09-09:09 social behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 12:00-12:30 low self efficacy; 12:00-13:00 suitable for outdoor; 12:41-14:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Saturday 2026-07-18 (planned busy time 11.0 h)
Free windows: 06:00-06:50, 07:00-11:12, 12:42-13:09, 18:10-18:21
Observed context: 06:30-07:00 intention to enact a behaviour; 12:00-12:05 disposition to attend to one s goals; 12:00-12:15 low self efficacy; 12:00-14:00 psychological behavioural capability; 12:00-16:00 physical behavioural opportunity; 17:30-17:50 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-19:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 19:30-20:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-07-19 (planned busy time 7.8 h)
Free windows: 06:00-06:50, 07:00-09:04, 10:54-13:20, 14:20-14:30, 15:00-15:40, 18:40-19:15, 19:55-20:30, 20:50-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 12:00-12:05 disposition to attend to one s goals; 12:00-12:30 low self efficacy; 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-20:30 social behavioural opportunity; 17:30-21:30 physical behavioural opportunity; 18:30-20:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 2
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W2T01 | Care for One Friendship 🫂 | 10 min | 1 | MentalWellbeing | standalone |
| W2T02 | Eat A Lighter Dinner 🍽️ | 15 min | 1 | MentalWellbeing | standalone |
| W2T03 | Get Morning Light ☀️ | 5 min | 1 | MentalWellbeing | alongside |
| W2T04 | Schedule a Short Rest Break 🗓️ | 10 min | 1 | MentalWellbeing | alongside |
| W2T05 | Step Outside for Fresh Air 🌬️ | 5 min | 1 | MentalWellbeing | alongside |
| W2T06 | Write About Stressors ⚡ | 15 min | 1 | MentalWellbeing | alongside |
| W2T07 | Write Control Table ✍️ | 15 min | 1 | MentalWellbeing | alongside |
| W2T08 | Log Veggie Servings 📒 | 5 min | 1 | Nutrition | alongside |
| W2T09 | Swap A Meaty Meal for Legumes 🍲 | 30 min | 2 | Nutrition | standalone |
| W2T10 | Tea Time ☕ | 15 min | 1 | Nutrition | alongside |
| W2T11 | Write a Grocery List 🛒 | 30 min | 1 | Nutrition | standalone |
| W2T12 | Add Five Walk Minutes 🚶 | 15 min | 2 | PhysicalActivity | standalone |
| W2T13 | Log How Movement Felt ✍️ | 5 min | 1 | PhysicalActivity | alongside |
| W2T14 | Prepare Your Workout Clothes 👟 | 10 min | 1 | PhysicalActivity | alongside |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 1
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Drink A Glass of Water 🫗 | Mon 06 Jul 10:00 | 12.0 h | physical behavioural opportunity, psychological behavioural capability | done |
| Log Fruit Servings 📒 | Tue 07 Jul 12:50 | 13.3 h | physical behavioural opportunity, psychological behavioural capability | replaced by snack |
| Prepare One Better Snack 🍎 | Tue 07 Jul 07:00 | 13.3 h | social behavioural opportunity | postponed, done later |
| Try a Veggie Recipe 🧑‍🍳 | Sun 12 Jul 18:00 | 7.8 h | habitual behaviour, physical behavioural opportunity, social behavioural opportunity, suitable for outdoor | done |
| Clean Actively for 20 Minutes 🧹 | Sat 11 Jul 09:00 | 11.0 h | - | done |
| Do 10 Minutes of Cardio 💪 | Wed 08 Jul 06:30 | 13.2 h | intention to enact a behaviour, physical behavioural opportunity | skipped |
| Log Each Walk 📒 | Mon 06 Jul 19:00 | 12.0 h | physical behavioural opportunity, suitable for outdoor | done |
| Schedule a 30-Minute Walk 🚶 | Mon 06 Jul 17:50 | 12.0 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | postponed, done later |
| Walk a New Route 🚶 | Mon 06 Jul 18:30 | 12.0 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |
| Walk Over 2,000 Steps 🚶 | Fri 10 Jul 18:10 | 11.9 h | habitual behaviour, physical behavioural opportunity, suitable for outdoor | done |

## Memory: completion rate of your placements so far (weeks 1-1)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | evening | 5 / 5 | 100% |
| time of day | morning | 3 / 4 | 75% |
| day type | weekday | 6 / 8 | 75% |
| day type | weekend | 2 / 2 | 100% |
| day load | heavy (>9 h) | 7 / 9 | 78% |
| intensity | intensity 2 | 5 / 5 | 100% |
| intensity | intensity 1 | 3 / 4 | 75% |
| observed context at the planned time | physical behavioural opportunity | 6 / 8 | 75% |
| observed context at the planned time | suitable for outdoor | 5 / 5 | 100% |
| observed context at the planned time | habitual behaviour | 4 / 4 | 100% |
| observed context at the planned time | psychological behavioural capability | 1 / 2 | 50% |
| observed context at the planned time | social behavioural opportunity | 2 / 2 | 100% |

## Your lessons from last week
She seems most likely to follow through in the early morning slot around 06:30, where intention to act is observed, and in the 17:30-19:00 habitual evening window, which is also suitable for outdoor activity. Walks go in the dry evenings. Cardio goes in the morning intention window. Weekend mornings and Sunday evening have more room for longer tasks. Low self-efficacy around midday and rain in late evening make those times poor choices.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\diligent_anxious_active_0000\learning\week_2_plan.json`
