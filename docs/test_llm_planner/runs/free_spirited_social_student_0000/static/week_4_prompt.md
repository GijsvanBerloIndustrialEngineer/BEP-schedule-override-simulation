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

# Calendar of week 4 (27 Jul - 02 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-07-27 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-13:30 social behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 17:49-19:49 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity; 19:30-21:00 raining or snowing

### Tuesday 2026-07-28 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 16:00-17:30, 19:39-19:50
Observed context: 08:00-12:00 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 16:00-17:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-21:30 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity

### Wednesday 2026-07-29 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-17:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:30 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity

### Thursday 2026-07-30 (planned busy time 11.3 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-14:20, 16:20-17:40, 19:10-19:29, 19:39-19:50
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-13:30 social behavioural opportunity; 14:30-19:00 social behavioural opportunity; 15:30-21:30 physical behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 19:30-20:30 raining or snowing

### Friday 2026-07-31 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 12:00-13:30 social behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:49-19:49 physical behavioural opportunity; 18:30-20:00 raining or snowing; 18:30-21:30 social behavioural opportunity

### Saturday 2026-08-01 (planned busy time 9.8 h)
Free windows: 06:00-07:49, 10:00-12:00, 13:58-14:11, 15:01-17:10, 17:30-17:40, 21:10-21:26, 21:36-21:50
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 14:30-17:30 social behavioural opportunity; 15:30-21:30 physical behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-18:30 suitable for outdoor; 18:30-19:30 raining or snowing; 18:30-21:30 social behavioural opportunity

### Sunday 2026-08-02 (planned busy time 10.3 h)
Free windows: 06:00-07:49, 07:59-12:15, 19:30-19:40, 21:10-21:26
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-13:30 social behavioural opportunity; 12:00-16:00 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 18:30-19:00 raining or snowing; 18:30-21:30 social behavioural opportunity

# Health tasks of week 4
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W4T01 | Set Up a Calm Spot 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W4T02 | Clean Actively for 10 Minutes 🧹 | 10 min | 2 | PhysicalActivity | standalone |
| W4T03 | Move for 10 Minutes 💪 | 10 min | 1 | PhysicalActivity | alongside |
| W4T04 | Move in the Afternoon 🚶 | 15 min | 1 | PhysicalActivity | alongside |
| W4T05 | Plan Sitting Breaks 🗓️ | 5 min | 1 | PhysicalActivity | standalone |
| W4T06 | Plan This Week's Exercises 🗓️ | 30 min | 1 | PhysicalActivity | standalone |
| W4T07 | Walk One Routine Route 🚶 | 25 min | 2 | PhysicalActivity | standalone |
| W4T08 | Walk Somewhere Nearby 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W4T09 | Write One Movement Step ✍️ | 5 min | 1 | PhysicalActivity | alongside |
| W4T10 | 7-Minute Workout 💪 | 7 min | 3 | Unknown | alongside |
| W4T11 | Write About Stressors ⚡ | 15 min | 1 | Unknown | alongside |

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\free_spirited_social_student_0000\static\week_4_plan.json`
