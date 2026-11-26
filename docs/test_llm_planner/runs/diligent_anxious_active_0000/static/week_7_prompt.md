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

# Calendar of week 7 (17 Aug - 23 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-08-17 (planned busy time 12.0 h)
Free windows: 07:00-07:50, 12:30-13:09, 18:00-18:50, 19:55-20:10, 20:20-20:54, 21:14-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:49-07:51 social behavioural opportunity; 08:09-10:41 social behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:41-14:41 psychological behavioural capability; 17:30-17:50 intention not to enact a behaviour; 17:30-19:00 habitual behaviour; 19:09-21:09 physical behavioural opportunity

### Tuesday 2026-08-18 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 06:30-07:30 social behavioural opportunity; 07:11-07:41 intention to enact a behaviour; 09:51-11:51 social behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:00-12:30 low self efficacy; 12:00-14:00 physical behavioural opportunity; 12:41-15:41 psychological behavioural capability; 15:00-16:00 suitable for outdoor; 16:00-16:30 raining or snowing; 16:30-18:30 suitable for outdoor; 17:30-19:00 habitual behaviour; 17:30-21:30 physical behavioural opportunity; 18:30-19:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-08-19 (planned busy time 13.2 h)
Free windows: 06:00-06:50, 12:40-13:09, 17:43-18:20, 19:55-20:20, 21:30-21:42
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 07:09-10:41 social behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 10:49-12:00 social behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:41-14:41 psychological behavioural capability; 17:30-17:50 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:30 physical behavioural opportunity

### Thursday 2026-08-20 (planned busy time 13.5 h)
Free windows: 06:20-06:50, 07:40-08:16, 19:00-19:15, 20:30-20:54, 21:14-21:42
Observed context: 06:30-07:30 social behavioural opportunity; 06:30-08:30 physical behavioural opportunity; 06:36-07:21 intention to enact a behaviour; 07:39-08:24 intention to enact a behaviour; 08:11-11:11 social behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:00-12:15 low self efficacy; 12:41-14:41 psychological behavioural capability; 17:30-17:50 intention not to enact a behaviour; 17:30-18:30 habitual behaviour; 18:11-20:11 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-08-21 (planned busy time 11.9 h)
Free windows: 06:00-06:40, 07:00-07:40, 10:46-11:00, 17:24-17:40, 18:10-18:40, 19:55-20:54, 21:14-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 06:49-11:11 social behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:41-15:41 psychological behavioural capability; 17:30-17:50 intention not to enact a behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:00 habitual behaviour; 17:30-21:30 physical behavioural opportunity; 18:30-20:00 raining or snowing

### Saturday 2026-08-22 (planned busy time 11.0 h)
Free windows: 06:00-06:50, 07:00-11:12, 12:42-13:09, 18:10-18:21
Observed context: 06:30-06:50 intention to enact a behaviour; 06:30-07:30 suitable for outdoor; 07:30-08:30 raining or snowing; 12:00-12:10 disposition to attend to one s goals; 12:00-12:30 low self efficacy; 12:00-14:00 physical behavioural opportunity; 12:00-15:00 psychological behavioural capability; 17:30-19:00 habitual behaviour; 17:30-20:30 social behavioural opportunity; 17:30-21:30 physical behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-08-23 (planned busy time 7.8 h)
Free windows: 06:00-06:30, 07:30-09:04, 10:54-11:50, 12:20-13:09, 13:39-15:50, 17:20-17:50, 19:55-21:42
Observed context: 06:30-07:00 intention to enact a behaviour; 06:30-08:30 physical behavioural opportunity; 12:00-12:05 disposition to attend to one s goals; 12:00-15:00 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-19:30 social behavioural opportunity; 17:30-19:30 suitable for outdoor; 19:30-20:00 raining or snowing

# Health tasks of week 7
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W7T01 | Add One Personal Touch 🪴 | 15 min | 1 | MentalWellbeing | standalone |
| W7T02 | Ask One Person for Support 💬 | 20 min | 1 | MentalWellbeing | alongside |
| W7T03 | Block Distractions 📵 | 5 min | 1 | MentalWellbeing | alongside |
| W7T04 | Care for One Friendship 🫂 | 10 min | 1 | MentalWellbeing | standalone |
| W7T05 | Eat A Lighter Dinner 🍽️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T06 | Eat Dinner Earlier 🗓️ | 15 min | 1 | MentalWellbeing | alongside |
| W7T07 | Log Afternoon Caffeine ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W7T08 | Message One New Contact 💬 | 30 min | 1 | MentalWellbeing | standalone |
| W7T09 | Mute Non-Essential Notifications 🔕 | 5 min | 1 | MentalWellbeing | alongside |
| W7T10 | Plan a Low-Cost Outing 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T11 | Plan Three Recharge Activities 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T12 | Play a Guided Meditation 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W7T13 | Play Calm Sleep Sounds 🎶 | 10 min | 1 | MentalWellbeing | alongside |
| W7T14 | Schedule a Short Rest Break 🗓️ | 10 min | 1 | MentalWellbeing | alongside |
| W7T15 | Schedule One Social Moment 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T16 | Set a Podcast Sleep Timer 🎙️ | 15 min | 1 | MentalWellbeing | alongside |
| W7T17 | Set a Repeatable Bedtime 😴 | 10 min | 1 | MentalWellbeing | alongside |
| W7T18 | Set Up a Calm Spot 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W7T19 | Step Outside for Fresh Air 🌬️ | 5 min | 1 | MentalWellbeing | alongside |
| W7T20 | Write About Stressors ⚡ | 15 min | 1 | MentalWellbeing | alongside |
| W7T21 | Write One Meaningful Action ✍️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T22 | Write Tomorrow's List ✍️ | 10 min | 1 | MentalWellbeing | alongside |
| W7T23 | Eat One Screen-Free Meal 😌 | 20 min | 1 | Nutrition | standalone |
| W7T24 | Share a Meal 🌮 | 30 min | 1 | Nutrition | standalone |
| W7T25 | Swap A Meaty Meal for Legumes 🍲 | 30 min | 2 | Nutrition | standalone |
| W7T26 | Try a Different Fruit 🥝 | 30 min | 1 | Nutrition | standalone |
| W7T27 | Try a Veggie Recipe 🧑‍🍳 | 30 min | 2 | Nutrition | standalone |
| W7T28 | Write a Grocery List 🛒 | 30 min | 1 | Nutrition | standalone |
| W7T29 | Do 30 Minutes of Cardio 💪 | 30 min | 3 | PhysicalActivity | standalone |
| W7T30 | Do 45 Minutes of Cardio 💪 | 45 min | 4 | PhysicalActivity | standalone |
| W7T31 | Make One Trip Car-Free 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W7T32 | Try Walk-Run Intervals 🏃 | 30 min | 3 | PhysicalActivity | standalone |
| W7T33 | Walk Over 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\diligent_anxious_active_0000\static\week_7_plan.json`
