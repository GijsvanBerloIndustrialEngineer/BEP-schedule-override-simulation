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

# Calendar of week 1 (06 Jul - 12 Jul 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-07-06 (planned busy time 11.2 h)
Free windows: 06:00-06:29, 06:39-06:55, 09:00-09:55, 11:25-12:21, 12:41-15:00, 16:30-17:00, 18:34-19:10, 21:10-21:30, 21:40-22:00
Observed context: 07:31-09:31 physical behavioural opportunity; 11:00-12:00 suitable for outdoor; 12:00-14:00 psychological behavioural capability; 17:30-18:30 social behavioural opportunity; 17:30-19:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 19:30-20:30 raining or snowing; 20:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-07-07 (planned busy time 10.4 h)
Free windows: 06:39-06:55, 08:40-09:55, 11:25-12:21, 12:41-14:30, 16:00-17:00, 18:34-19:30, 21:00-21:30, 21:40-22:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 17:30-18:30 social behavioural opportunity; 17:30-19:30 habitual behaviour; 20:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-07-08 (planned busy time 11.2 h)
Free windows: 06:39-06:55, 08:25-10:00, 10:30-11:20, 11:50-12:21, 12:41-14:00, 16:00-16:40, 19:40-20:10, 20:40-21:30
Observed context: 09:01-11:01 physical behavioural opportunity; 12:00-13:00 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-18:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 19:30-22:00 low physical opportunity to enact a behaviour; 20:30-21:30 raining or snowing

### Thursday 2026-07-09 (planned busy time 12.5 h)
Free windows: 06:39-06:55, 08:25-08:50, 10:20-10:50, 12:41-13:10, 15:00-15:10, 16:40-17:10, 19:10-20:10, 20:40-21:30, 21:40-22:00
Observed context: 06:30-07:30 habitual behaviour; 11:00-12:00 habitual behaviour; 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 17:30-18:30 social behavioural opportunity; 17:30-18:30 suitable for outdoor; 18:30-19:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-07-10 (planned busy time 11.0 h)
Free windows: 06:39-06:55, 08:25-09:55, 11:25-12:21, 12:41-13:50, 14:20-15:10, 18:34-19:40, 21:10-21:30, 21:40-22:00
Observed context: 12:00-14:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-19:00 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 20:30-21:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Saturday 2026-07-11 (planned busy time 11.3 h)
Free windows: 06:39-06:55, 08:25-09:55, 12:00-12:21, 12:41-14:10, 16:20-17:00, 18:34-18:50, 20:20-21:00, 21:40-22:00
Observed context: 10:31-11:31 physical behavioural opportunity; 12:00-13:00 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 17:30-19:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-07-12 (planned busy time 12.2 h)
Free windows: 08:00-09:50, 10:20-11:50, 12:00-12:21, 12:41-13:10, 18:30-19:00, 21:40-22:00
Observed context: 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-18:30 social behavioural opportunity; 17:30-18:30 suitable for outdoor; 17:30-19:30 habitual behaviour; 18:30-19:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 1
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W1T01 | Log Fruit Servings 📒 | 15 min | 1 | Nutrition | alongside |
| W1T02 | Log Veggie Servings 📒 | 5 min | 1 | Nutrition | alongside |
| W1T03 | Plan This Week's Meals 🗓️ | 45 min | 1 | Nutrition | standalone |
| W1T04 | Prepare One Better Snack 🍎 | 5 min | 1 | Nutrition | standalone |
| W1T05 | Swap A Meaty Meal for Legumes 🍲 | 30 min | 2 | Nutrition | standalone |
| W1T06 | Clean Actively for 10 Minutes 🧹 | 10 min | 2 | PhysicalActivity | standalone |
| W1T07 | Do 10 Minutes of Cardio 💪 | 10 min | 2 | PhysicalActivity | standalone |
| W1T08 | Write One Movement Step ✍️ | 5 min | 1 | PhysicalActivity | alongside |
| W1T09 | Tea Time ☕ | 15 min | 1 | Unknown | alongside |
| W1T10 | Write a Grocery List 🛒 | 30 min | 1 | Unknown | standalone |

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\unemployed_family_caregiver_0000\shared\week_1_plan.json`
