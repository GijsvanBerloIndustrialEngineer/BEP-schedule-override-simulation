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

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\free_spirited_social_student_0000\static\week_2_plan.json`
