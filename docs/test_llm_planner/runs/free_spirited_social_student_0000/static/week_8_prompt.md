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

# Calendar of week 8 (24 Aug - 30 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-08-24 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-20:30 suitable for outdoor; 17:49-19:49 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity

### Tuesday 2026-08-25 (planned busy time 11.3 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:10, 17:10-17:40, 19:10-19:29, 19:39-19:50
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 15:30-21:30 physical behavioural opportunity; 16:00-20:30 social behavioural opportunity; 17:30-18:30 habitual behaviour

### Wednesday 2026-08-26 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 12:00-13:30 social behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:30 physical behavioural opportunity; 18:30-19:30 raining or snowing; 18:30-21:30 social behavioural opportunity

### Thursday 2026-08-27 (planned busy time 11.8 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:10, 17:40-17:50, 19:39-19:50
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-13:30 social behavioural opportunity; 12:00-14:00 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-20:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity; 20:30-22:00 raining or snowing

### Friday 2026-08-28 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 14:30-20:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-20:30 suitable for outdoor; 17:49-19:49 physical behavioural opportunity; 20:30-21:30 raining or snowing

### Saturday 2026-08-29 (planned busy time 9.8 h)
Free windows: 06:00-07:49, 10:00-12:00, 13:58-14:11, 15:01-17:10, 17:30-17:40, 21:10-21:26, 21:36-21:50
Observed context: 12:00-13:30 social behavioural opportunity; 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 15:30-21:30 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-20:30 suitable for outdoor; 18:30-21:30 social behavioural opportunity

### Sunday 2026-08-30 (planned busy time 10.3 h)
Free windows: 06:00-07:49, 07:59-12:15, 19:30-19:40, 21:10-21:26
Observed context: 06:30-08:30 suitable for outdoor; 10:00-14:00 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 12:00-13:00 suitable for outdoor; 16:00-17:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-21:30 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity

# Health tasks of week 8
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W8T01 | Ask One Person for Support 💬 | 20 min | 1 | MentalWellbeing | alongside |
| W8T02 | Block Distractions 📵 | 5 min | 1 | MentalWellbeing | alongside |
| W8T03 | Care for One Friendship 🫂 | 10 min | 1 | MentalWellbeing | standalone |
| W8T04 | Eat A Lighter Dinner 🍽️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T05 | Eat Dinner Earlier 🗓️ | 15 min | 1 | MentalWellbeing | alongside |
| W8T06 | Log Afternoon Caffeine ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W8T07 | Message One New Contact 💬 | 30 min | 1 | MentalWellbeing | standalone |
| W8T08 | Move in the Afternoon 🚶 | 15 min | 1 | MentalWellbeing | alongside |
| W8T09 | Plan Three Recharge Activities 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T10 | Play a Guided Meditation 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W8T11 | Play Calm Sleep Sounds 🎶 | 10 min | 1 | MentalWellbeing | alongside |
| W8T12 | Schedule a Short Rest Break 🗓️ | 10 min | 1 | MentalWellbeing | alongside |
| W8T13 | Schedule One Enjoyable Activity 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T14 | Send a Friend Check-In 💬 | 10 min | 1 | MentalWellbeing | alongside |
| W8T15 | Set a Podcast Sleep Timer 🎙️ | 15 min | 1 | MentalWellbeing | alongside |
| W8T16 | Set a Repeatable Bedtime 😴 | 10 min | 1 | MentalWellbeing | alongside |
| W8T17 | Set Up a Calm Spot 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W8T18 | Write About Stressors ⚡ | 15 min | 1 | MentalWellbeing | alongside |
| W8T19 | Write One Meaningful Action ✍️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T20 | Write Tomorrow's List ✍️ | 10 min | 1 | MentalWellbeing | alongside |
| W8T21 | Batch-Cook Healthy Meal 🍲 | 120 min | 2 | Nutrition | standalone |
| W8T22 | Eat One Screen-Free Meal 😌 | 20 min | 1 | Nutrition | standalone |
| W8T23 | Infuse a Water Bottle 🥒 | 15 min | 1 | Nutrition | standalone |
| W8T24 | Make a Calming Drink ☕ | 10 min | 1 | Nutrition | alongside |
| W8T25 | Share a Meal 🌮 | 30 min | 1 | Nutrition | standalone |
| W8T26 | Swap A Meaty Meal for Legumes 🍲 | 30 min | 2 | Nutrition | standalone |
| W8T27 | Try a Different Fruit 🥝 | 30 min | 1 | Nutrition | standalone |
| W8T28 | Try a Veggie Recipe 🧑‍🍳 | 30 min | 2 | Nutrition | standalone |
| W8T29 | Do 30 Minutes of Cardio 💪 | 30 min | 3 | PhysicalActivity | standalone |
| W8T30 | Do 45 Minutes of Cardio 💪 | 45 min | 3 | PhysicalActivity | standalone |
| W8T31 | Make One Trip Car-Free 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W8T32 | Try Walk-Run Intervals 🏃 | 30 min | 3 | PhysicalActivity | standalone |
| W8T33 | Walk 6,000 to 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |
| W8T34 | Walk Over 10,000 Steps 🚶 | 85 min | 3 | PhysicalActivity | standalone |
| W8T35 | Walk Over 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |
| W8T36 | Write One Difficult Thought ✍️ | 15 min | 1 | Unknown | alongside |

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\free_spirited_social_student_0000\static\week_8_plan.json`
