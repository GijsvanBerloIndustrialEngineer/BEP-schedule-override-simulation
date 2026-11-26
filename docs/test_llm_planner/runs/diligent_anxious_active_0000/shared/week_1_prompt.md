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

# Calendar of week 1 (06 Jul - 12 Jul 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-07-06 (planned busy time 12.0 h)
Free windows: 06:00-06:50, 12:50-13:09, 13:39-17:23, 17:43-19:15, 20:20-20:54, 21:14-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:51-09:51 social behavioural opportunity; 07:17-10:17 psychological behavioural capability; 10:00-12:00 physical behavioural opportunity; 12:00-12:10 disposition to attend to one s goals; 12:00-12:30 low self efficacy; 17:30-17:40 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 19:30-20:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-07-07 (planned busy time 13.3 h)
Free windows: 06:10-06:30, 07:00-07:10, 07:30-07:50, 12:40-13:09, 17:24-17:40, 19:55-20:54
Observed context: 06:30-07:51 social behavioural opportunity; 07:01-07:21 intention to enact a behaviour; 08:09-10:51 social behavioural opportunity; 12:00-14:00 physical behavioural opportunity; 12:41-14:41 psychological behavioural capability; 17:30-18:30 suitable for outdoor; 17:30-19:00 habitual behaviour; 17:30-21:30 physical behavioural opportunity; 18:30-20:00 raining or snowing

### Wednesday 2026-07-08 (planned busy time 13.2 h)
Free windows: 06:00-06:50, 12:40-13:09, 17:43-18:20, 19:55-20:20, 21:30-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 07:09-10:41 social behavioural opportunity; 07:17-09:17 psychological behavioural capability; 10:00-12:00 physical behavioural opportunity; 10:49-12:00 social behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:00-13:00 suitable for outdoor; 12:41-13:41 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 18:39-20:39 physical behavioural opportunity

### Thursday 2026-07-09 (planned busy time 13.3 h)
Free windows: 06:10-06:30, 07:00-07:10, 07:30-07:50, 12:40-13:09, 17:24-17:40, 19:55-20:54
Observed context: 06:49-10:51 social behavioural opportunity; 07:01-07:21 intention to enact a behaviour; 12:00-12:15 low self efficacy; 12:41-15:41 psychological behavioural capability; 17:30-18:30 suitable for outdoor; 17:30-19:00 habitual behaviour; 17:30-21:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-07-10 (planned busy time 11.9 h)
Free windows: 06:00-06:40, 07:00-07:40, 10:46-11:00, 17:24-17:40, 18:10-18:40, 19:55-20:54, 21:14-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:49-08:49 social behavioural opportunity; 07:17-09:17 psychological behavioural capability; 12:00-12:10 disposition to attend to one s goals; 12:00-12:30 low self efficacy; 17:30-18:30 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-19:30 suitable for outdoor; 19:30-20:30 raining or snowing

### Saturday 2026-07-11 (planned busy time 11.0 h)
Free windows: 06:00-06:50, 07:00-11:12, 12:42-13:09, 18:10-18:21
Observed context: 06:30-06:50 intention to enact a behaviour; 12:00-12:10 intention not to enact a behaviour; 12:00-15:00 psychological behavioural capability; 12:00-16:00 physical behavioural opportunity; 17:30-17:40 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-20:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 20:30-21:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-07-12 (planned busy time 7.8 h)
Free windows: 06:10-06:50, 07:50-09:04, 10:54-13:09, 13:39-16:00, 17:50-19:15, 19:55-20:10, 21:10-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-12:30 low self efficacy; 12:00-15:00 psychological behavioural capability; 17:30-19:00 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 1
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W1T01 | Drink A Glass of Water 🫗 | 5 min | 1 | Nutrition | alongside |
| W1T02 | Log Fruit Servings 📒 | 15 min | 1 | Nutrition | alongside |
| W1T03 | Prepare One Better Snack 🍎 | 5 min | 1 | Nutrition | standalone |
| W1T04 | Try a Veggie Recipe 🧑‍🍳 | 30 min | 2 | Nutrition | standalone |
| W1T05 | Clean Actively for 20 Minutes 🧹 | 20 min | 2 | PhysicalActivity | standalone |
| W1T06 | Do 10 Minutes of Cardio 💪 | 10 min | 3 | PhysicalActivity | standalone |
| W1T07 | Log Each Walk 📒 | 15 min | 1 | PhysicalActivity | alongside |
| W1T08 | Schedule a 30-Minute Walk 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W1T09 | Walk a New Route 🚶 | 15 min | 2 | PhysicalActivity | standalone |
| W1T10 | Walk Over 2,000 Steps 🚶 | 30 min | 2 | PhysicalActivity | standalone |

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\diligent_anxious_active_0000\shared\week_1_plan.json`
