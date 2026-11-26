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

# Calendar of week 6 (10 Aug - 16 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-08-10 (planned busy time 11.2 h)
Free windows: 06:39-06:55, 08:25-08:50, 09:20-09:55, 11:25-12:21, 12:41-13:30, 14:00-14:40, 16:10-16:30, 18:34-19:40, 20:10-21:30
Observed context: 07:51-09:51 physical behavioural opportunity; 12:00-13:00 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 17:30-18:30 social behavioural opportunity; 17:30-18:30 suitable for outdoor; 17:30-19:30 habitual behaviour; 21:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-08-11 (planned busy time 10.2 h)
Free windows: 06:39-06:55, 08:25-09:55, 11:25-12:21, 12:41-13:40, 14:10-14:40, 16:10-17:00, 18:34-19:20, 20:50-21:30, 21:40-22:00
Observed context: 12:00-14:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-19:30 suitable for outdoor; 20:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-08-12 (planned busy time 10.6 h)
Free windows: 06:00-06:29, 06:39-06:55, 09:20-09:55, 11:25-12:21, 12:41-13:30, 14:00-15:00, 18:34-19:40, 21:40-22:00
Observed context: 07:51-09:51 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 17:30-18:30 social behavioural opportunity; 17:30-19:00 habitual behaviour; 20:30-22:00 low physical opportunity to enact a behaviour

### Thursday 2026-08-13 (planned busy time 13.2 h)
Free windows: 06:39-06:55, 08:25-09:08, 11:08-12:21, 12:41-13:40, 14:40-15:00, 18:34-18:50, 19:20-20:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 17:30-18:30 social behavioural opportunity; 17:30-19:30 habitual behaviour; 17:30-20:30 suitable for outdoor; 20:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-08-14 (planned busy time 10.8 h)
Free windows: 06:00-06:29, 06:39-06:55, 08:25-08:50, 11:25-12:21, 13:20-14:00, 15:30-16:20, 18:34-18:50, 20:50-21:30, 21:40-22:00
Observed context: 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-18:30 social behavioural opportunity; 17:30-18:30 suitable for outdoor; 17:30-19:30 habitual behaviour; 18:30-20:00 raining or snowing; 19:30-22:00 low physical opportunity to enact a behaviour

### Saturday 2026-08-15 (planned busy time 12.2 h)
Free windows: 06:00-06:29, 06:39-06:50, 07:20-07:50, 12:50-13:20, 16:20-16:30, 16:50-17:00, 18:34-19:20, 20:50-21:30, 21:40-22:00
Observed context: 07:19-10:19 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-18:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 21:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-08-16 (planned busy time 12.4 h)
Free windows: 06:39-06:55, 11:08-12:21, 14:50-15:20, 16:50-17:00, 19:10-19:20, 19:50-21:30, 21:40-22:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:30 social behavioural opportunity; 18:30-20:00 raining or snowing; 19:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 6
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W6T01 | Ask One Person for Support 💬 | 20 min | 1 | MentalWellbeing | alongside |
| W6T02 | Eat Dinner Earlier 🗓️ | 15 min | 1 | MentalWellbeing | alongside |
| W6T03 | Log Afternoon Caffeine ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W6T04 | Message One New Contact 💬 | 30 min | 1 | MentalWellbeing | standalone |
| W6T05 | Move in the Afternoon 🚶 | 15 min | 2 | MentalWellbeing | alongside |
| W6T06 | Plan a Low-Cost Outing 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W6T07 | Play a Guided Meditation 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W6T08 | Schedule One Enjoyable Activity 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W6T09 | Set a Podcast Sleep Timer 🎙️ | 15 min | 1 | MentalWellbeing | alongside |
| W6T10 | Write One Difficult Thought ✍️ | 15 min | 1 | MentalWellbeing | alongside |
| W6T11 | Write One Kind No ✍️ | 10 min | 1 | MentalWellbeing | standalone |
| W6T12 | Write One Meaningful Action ✍️ | 15 min | 1 | MentalWellbeing | standalone |
| W6T13 | Write Tomorrow's List ✍️ | 10 min | 1 | MentalWellbeing | alongside |
| W6T14 | Share a Meal 🌮 | 30 min | 1 | Nutrition | standalone |
| W6T15 | Add Five Walk Minutes 🚶 | 15 min | 2 | PhysicalActivity | standalone |
| W6T16 | Clean Actively for 10 Minutes 🧹 | 10 min | 2 | PhysicalActivity | standalone |
| W6T17 | Clean Actively for 20 Minutes 🧹 | 20 min | 2 | PhysicalActivity | standalone |
| W6T18 | Do 20 Minutes of Cardio 💪 | 20 min | 3 | PhysicalActivity | standalone |
| W6T19 | Do 30 Minutes of Cardio 💪 | 30 min | 3 | PhysicalActivity | standalone |
| W6T20 | Plan Sitting Breaks 🗓️ | 5 min | 1 | PhysicalActivity | standalone |
| W6T21 | Schedule a 30-Minute Walk 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W6T22 | Try Walk-Run Intervals 🏃 | 30 min | 3 | PhysicalActivity | standalone |
| W6T23 | Walk 4,000 to 6,000 Steps 🚶 | 60 min | 2 | PhysicalActivity | standalone |
| W6T24 | Walk 6,000 to 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |
| W6T25 | Walk One Routine Route 🚶 | 25 min | 2 | PhysicalActivity | standalone |
| W6T26 | Plan a Coffee Chat ☕ | 30 min | 1 | Unknown | standalone |

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\unemployed_family_caregiver_0000\static\week_6_plan.json`
