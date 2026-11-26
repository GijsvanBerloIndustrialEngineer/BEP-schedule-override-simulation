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

# Calendar of week 8 (24 Aug - 30 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-08-24 (planned busy time 12.0 h)
Free windows: 07:00-07:50, 12:30-13:09, 18:00-18:50, 19:55-20:10, 20:20-20:54, 21:14-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:49-07:51 social behavioural opportunity; 08:09-10:41 social behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-12:10 disposition to attend to one s goals; 12:00-12:15 low self efficacy; 12:41-15:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-19:30 suitable for outdoor; 19:09-21:09 physical behavioural opportunity

### Tuesday 2026-08-25 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 07:11-07:31 intention to enact a behaviour; 07:17-08:17 psychological behavioural capability; 07:19-12:00 social behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:00-12:15 low self efficacy; 12:41-14:41 psychological behavioural capability; 17:30-19:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 19:30-20:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-08-26 (planned busy time 13.2 h)
Free windows: 06:00-06:50, 12:40-13:09, 17:43-18:20, 19:55-20:20, 21:30-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 08:09-11:41 social behavioural opportunity; 12:00-12:10 disposition to attend to one s goals; 12:41-15:41 psychological behavioural capability; 17:30-17:50 intention not to enact a behaviour; 17:30-18:30 social behavioural opportunity; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Thursday 2026-08-27 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 06:30-07:30 social behavioural opportunity; 06:30-08:30 physical behavioural opportunity; 07:11-07:31 intention to enact a behaviour; 10:00-12:00 physical behavioural opportunity; 10:00-12:00 social behavioural opportunity; 12:00-12:10 disposition to attend to one s goals; 12:41-15:41 psychological behavioural capability; 17:30-17:40 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-20:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-08-28 (planned busy time 11.9 h)
Free windows: 06:00-06:40, 07:00-07:40, 10:46-11:00, 17:24-17:40, 18:10-18:40, 19:55-20:54, 21:14-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:49-11:09 social behavioural opportunity; 10:00-16:00 physical behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:41-15:41 psychological behavioural capability; 17:30-17:50 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-19:30 suitable for outdoor; 19:30-20:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Saturday 2026-08-29 (planned busy time 11.0 h)
Free windows: 06:00-06:50, 07:00-11:12, 12:42-13:09, 18:10-18:21
Observed context: 06:30-06:35 disposition to attend to one s goals; 06:30-07:00 intention to enact a behaviour; 12:00-12:30 low self efficacy; 12:00-14:00 psychological behavioural capability; 12:00-16:00 physical behavioural opportunity; 17:30-17:40 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-21:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-08-30 (planned busy time 8.5 h)
Free windows: 06:00-06:50, 07:00-09:04, 10:54-12:00, 12:30-13:09, 16:50-17:40, 18:40-19:15, 20:20-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 12:00-12:10 disposition to attend to one s goals; 12:00-12:15 low self efficacy; 12:00-14:00 psychological behavioural capability; 12:00-16:00 physical behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-20:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 20:30-21:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 8
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W8T01 | Add One Personal Touch 🪴 | 15 min | 1 | MentalWellbeing | standalone |
| W8T02 | Block Distractions 📵 | 5 min | 1 | MentalWellbeing | alongside |
| W8T03 | Care for One Friendship 🫂 | 10 min | 1 | MentalWellbeing | standalone |
| W8T04 | Eat A Lighter Dinner 🍽️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T05 | Eat Dinner Earlier 🗓️ | 15 min | 1 | MentalWellbeing | alongside |
| W8T06 | Log Afternoon Caffeine ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W8T07 | Make a Calming Drink ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W8T08 | Message One New Contact 💬 | 30 min | 1 | MentalWellbeing | standalone |
| W8T09 | Move in the Afternoon 🚶 | 15 min | 2 | MentalWellbeing | alongside |
| W8T10 | Mute Non-Essential Notifications 🔕 | 5 min | 1 | MentalWellbeing | alongside |
| W8T11 | Plan a Coffee Chat ☕ | 30 min | 1 | MentalWellbeing | standalone |
| W8T12 | Plan Three Recharge Activities 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T13 | Play a Guided Meditation 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W8T14 | Play Calm Sleep Sounds 🎶 | 10 min | 1 | MentalWellbeing | alongside |
| W8T15 | Schedule a Short Rest Break 🗓️ | 10 min | 1 | MentalWellbeing | alongside |
| W8T16 | Schedule One Enjoyable Activity 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T17 | Schedule One Social Moment 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T18 | Send a Friend Check-In 💬 | 10 min | 1 | MentalWellbeing | alongside |
| W8T19 | Set a Podcast Sleep Timer 🎙️ | 15 min | 1 | MentalWellbeing | alongside |
| W8T20 | Set a Repeatable Bedtime 😴 | 10 min | 1 | MentalWellbeing | alongside |
| W8T21 | Set Up a Calm Spot 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W8T22 | Step Outside for Fresh Air 🌬️ | 5 min | 1 | MentalWellbeing | alongside |
| W8T23 | Write One Kind No ✍️ | 10 min | 1 | MentalWellbeing | standalone |
| W8T24 | Write One Meaningful Action ✍️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T25 | Write Tomorrow's List ✍️ | 10 min | 1 | MentalWellbeing | alongside |
| W8T26 | Batch-Cook Healthy Meal 🍲 | 120 min | 3 | Nutrition | standalone |
| W8T27 | Eat One Screen-Free Meal 😌 | 20 min | 1 | Nutrition | standalone |
| W8T28 | Swap A Meaty Meal for Legumes 🍲 | 30 min | 2 | Nutrition | standalone |
| W8T29 | Try a Different Fruit 🥝 | 30 min | 1 | Nutrition | standalone |
| W8T30 | Try a Veggie Recipe 🧑‍🍳 | 30 min | 2 | Nutrition | standalone |
| W8T31 | Write a Grocery List 🛒 | 30 min | 1 | Nutrition | standalone |
| W8T32 | Do 30 Minutes of Cardio 💪 | 30 min | 3 | PhysicalActivity | standalone |
| W8T33 | Do 45 Minutes of Cardio 💪 | 45 min | 3 | PhysicalActivity | standalone |
| W8T34 | Make One Trip Car-Free 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W8T35 | Try Walk-Run Intervals 🏃 | 30 min | 3 | PhysicalActivity | standalone |
| W8T36 | Walk 6,000 to 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |
| W8T37 | Walk Over 10,000 Steps 🚶 | 85 min | 3 | PhysicalActivity | standalone |
| W8T38 | Walk Over 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\diligent_anxious_active_0000\static\week_8_plan.json`
