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
age 37, female, occupation: unemployed, has children, aims for about 0 workouts a week.

# Calendar of week 2 (13 Jul - 19 Jul 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-07-13 (planned busy time 12.2 h)
Free windows: 06:39-06:55, 08:25-08:40, 09:10-09:55, 11:25-12:21, 13:20-13:30, 15:00-15:10, 16:40-17:00, 18:34-19:40, 20:10-21:30
Observed context: 06:30-07:30 suitable for outdoor; 07:41-09:41 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 17:30-19:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 20:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-07-14 (planned busy time 11.2 h)
Free windows: 06:39-06:55, 08:25-09:55, 11:25-12:21, 15:50-17:00, 18:34-19:30, 21:00-21:30
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 17:30-18:30 suitable for outdoor; 17:30-19:00 habitual behaviour; 17:30-19:30 social behavioural opportunity; 18:30-19:00 raining or snowing; 19:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-07-15 (planned busy time 10.6 h)
Free windows: 06:30-06:55, 09:20-09:55, 11:25-12:21, 12:41-13:40, 14:10-15:00, 18:34-20:00, 21:40-22:00
Observed context: 07:51-10:51 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-18:30 social behavioural opportunity; 17:30-19:30 habitual behaviour; 17:30-20:30 suitable for outdoor; 20:30-21:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Thursday 2026-07-16 (planned busy time 12.2 h)
Free windows: 08:25-09:08, 11:08-12:21, 12:41-13:10, 16:10-17:00, 17:30-18:04, 18:34-20:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-18:30 social behavioural opportunity; 17:30-19:00 habitual behaviour; 21:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-07-17 (planned busy time 12.2 h)
Free windows: 06:39-06:55, 08:25-08:50, 11:25-12:21, 12:41-13:10, 13:40-14:10, 16:40-17:00, 18:34-20:00, 21:40-22:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-18:30 social behavioural opportunity; 17:30-19:30 habitual behaviour; 17:30-20:30 suitable for outdoor; 20:30-21:30 raining or snowing; 20:30-22:00 low physical opportunity to enact a behaviour

### Saturday 2026-07-18 (planned busy time 10.7 h)
Free windows: 06:39-06:55, 08:25-08:50, 11:20-12:21, 12:41-13:20, 13:30-14:20, 14:50-17:20, 17:50-18:04, 18:34-19:20
Observed context: 09:51-11:51 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 17:30-18:30 suitable for outdoor; 17:30-19:30 social behavioural opportunity; 18:30-19:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-07-19 (planned busy time 11.7 h)
Free windows: 06:39-07:10, 07:40-09:08, 11:08-12:21, 12:41-13:00, 14:40-15:10, 16:40-17:10, 21:00-21:30, 21:40-22:00
Observed context: 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-18:30 social behavioural opportunity; 17:30-19:30 suitable for outdoor; 19:30-20:30 raining or snowing; 20:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 2
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W2T01 | Add One Personal Touch 🪴 | 15 min | 1 | MentalWellbeing | standalone |
| W2T02 | Care for One Friendship 🫂 | 10 min | 1 | MentalWellbeing | standalone |
| W2T03 | Get Morning Light ☀️ | 5 min | 1 | MentalWellbeing | alongside |
| W2T04 | Prepare a Sleep-Friendly Room 😴 | 5 min | 1 | MentalWellbeing | standalone |
| W2T05 | Schedule a Short Rest Break 🗓️ | 10 min | 1 | MentalWellbeing | alongside |
| W2T06 | Schedule One Social Moment 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W2T07 | Step Outside for Fresh Air 🌬️ | 5 min | 1 | MentalWellbeing | alongside |
| W2T08 | Write About Stressors ⚡ | 15 min | 1 | MentalWellbeing | alongside |
| W2T09 | Write Control Table ✍️ | 15 min | 1 | MentalWellbeing | alongside |
| W2T10 | Drink A Glass of Water 🫗 | 5 min | 1 | Nutrition | alongside |
| W2T11 | Try a Different Fruit 🥝 | 30 min | 1 | Nutrition | standalone |
| W2T12 | Add Five Walk Minutes 🚶 | 15 min | 2 | PhysicalActivity | standalone |
| W2T13 | Log How Movement Felt ✍️ | 5 min | 1 | PhysicalActivity | alongside |
| W2T14 | Walk Over 2,000 Steps 🚶 | 30 min | 2 | PhysicalActivity | standalone |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 1
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Log Fruit Servings 📒 | Mon 06 Jul 12:00 | 11.2 h | psychological behavioural capability | done |
| Log Veggie Servings 📒 | Tue 07 Jul 18:40 | 10.4 h | habitual behaviour | done |
| Plan This Week's Meals 🗓️ | Mon 06 Jul 12:50 | 11.2 h | psychological behavioural capability | postponed, done later |
| Prepare One Better Snack 🍎 | Thu 09 Jul 12:50 | 12.5 h | physical behavioural opportunity, psychological behavioural capability | done |
| Swap A Meaty Meal for Legumes 🍲 | Wed 08 Jul 12:50 | 11.2 h | physical behavioural opportunity, psychological behavioural capability | postponed, done later |
| Clean Actively for 10 Minutes 🧹 | Mon 06 Jul 09:00 | 11.2 h | physical behavioural opportunity | done |
| Do 10 Minutes of Cardio 💪 | Wed 08 Jul 09:10 | 11.2 h | physical behavioural opportunity | postponed, done later |
| Write One Movement Step ✍️ | Wed 08 Jul 09:30 | 11.2 h | physical behavioural opportunity | done |
| Tea Time ☕ | Fri 10 Jul 14:30 | 11.0 h | physical behavioural opportunity | done |
| Write a Grocery List 🛒 | Tue 07 Jul 13:00 | 10.4 h | physical behavioural opportunity | done |

## Memory: completion rate of your placements so far (weeks 1-1)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | afternoon | 6 / 6 | 100% |
| time of day | morning | 3 / 3 | 100% |
| day type | weekday | 10 / 10 | 100% |
| day load | heavy (>9 h) | 10 / 10 | 100% |
| intensity | intensity 1 | 7 / 7 | 100% |
| intensity | intensity 2 | 3 / 3 | 100% |
| observed context at the planned time | physical behavioural opportunity | 7 / 7 | 100% |
| observed context at the planned time | psychological behavioural capability | 4 / 4 | 100% |

## Your lessons from last week
Assumes a caregiver with fragmented days who follows through best in quiet midday windows (12:00-14:00 marked as psychological capability) and morning slots after the school run flagged as physical opportunity. Light, short tasks are anchored to habitual routines (lunch, early evening). Tasks are spread across days to avoid overload, with no evening placements during low-opportunity periods.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\unemployed_family_caregiver_0000\learning\week_2_plan.json`
