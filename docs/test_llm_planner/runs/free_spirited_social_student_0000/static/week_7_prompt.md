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

# Calendar of week 7 (17 Aug - 23 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-08-17 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-12:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-20:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-20:30 suitable for outdoor; 20:30-22:00 raining or snowing

### Tuesday 2026-08-18 (planned busy time 11.8 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:10, 17:40-17:50, 19:39-19:50
Observed context: 12:00-14:00 psychological behavioural capability; 12:00-16:30 social behavioural opportunity; 15:30-21:30 physical behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-19:00 social behavioural opportunity; 17:30-19:30 suitable for outdoor; 19:30-20:30 raining or snowing

### Wednesday 2026-08-19 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-10:30 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 12:00-13:30 social behavioural opportunity; 12:00-14:00 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 17:30-19:30 suitable for outdoor; 18:30-21:30 social behavioural opportunity; 19:30-20:00 raining or snowing

### Thursday 2026-08-20 (planned busy time 11.8 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:10, 17:40-17:50, 19:39-19:50
Observed context: 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-20:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-19:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 19:30-20:30 raining or snowing

### Friday 2026-08-21 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 12:00-13:30 social behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-17:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:49-19:49 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity

### Saturday 2026-08-22 (planned busy time 9.8 h)
Free windows: 06:00-07:49, 10:00-12:00, 13:58-14:11, 15:01-17:10, 17:30-17:40, 21:10-21:26, 21:36-21:50
Observed context: 12:00-13:30 social behavioural opportunity; 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 15:30-21:30 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 18:30-21:30 social behavioural opportunity

### Sunday 2026-08-23 (planned busy time 10.5 h)
Free windows: 06:00-07:49, 07:59-12:15, 19:30-19:40
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-13:30 social behavioural opportunity; 12:00-14:00 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 18:30-19:30 raining or snowing; 18:30-21:30 social behavioural opportunity

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
| W7T08 | Make a Calming Drink ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W7T09 | Message One New Contact 💬 | 30 min | 1 | MentalWellbeing | standalone |
| W7T10 | Move in the Afternoon 🚶 | 15 min | 1 | MentalWellbeing | alongside |
| W7T11 | Plan a Low-Cost Outing 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T12 | Plan Three Recharge Activities 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T13 | Play a Guided Meditation 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W7T14 | Play Calm Sleep Sounds 🎶 | 10 min | 1 | MentalWellbeing | alongside |
| W7T15 | Read Something Calm 📖 | 20 min | 1 | MentalWellbeing | standalone |
| W7T16 | Schedule a Short Rest Break 🗓️ | 10 min | 1 | MentalWellbeing | alongside |
| W7T17 | Schedule One Enjoyable Activity 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T18 | Set a Podcast Sleep Timer 🎙️ | 15 min | 1 | MentalWellbeing | alongside |
| W7T19 | Set a Repeatable Bedtime 😴 | 10 min | 1 | MentalWellbeing | alongside |
| W7T20 | Set Up a Calm Spot 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W7T21 | Step Outside for Fresh Air 🌬️ | 5 min | 1 | MentalWellbeing | alongside |
| W7T22 | Write One Meaningful Action ✍️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T23 | Write Tomorrow's List ✍️ | 10 min | 1 | MentalWellbeing | alongside |
| W7T24 | Batch-Cook Healthy Meal 🍲 | 120 min | 2 | Nutrition | standalone |
| W7T25 | Eat One Screen-Free Meal 😌 | 20 min | 1 | Nutrition | standalone |
| W7T26 | Swap A Meaty Meal for Legumes 🍲 | 30 min | 2 | Nutrition | standalone |
| W7T27 | Try a Different Fruit 🥝 | 30 min | 1 | Nutrition | standalone |
| W7T28 | Try a Veggie Recipe 🧑‍🍳 | 30 min | 2 | Nutrition | standalone |
| W7T29 | Write a Grocery List 🛒 | 30 min | 1 | Nutrition | standalone |
| W7T30 | Do 30 Minutes of Cardio 💪 | 30 min | 3 | PhysicalActivity | standalone |
| W7T31 | Do 45 Minutes of Cardio 💪 | 45 min | 4 | PhysicalActivity | standalone |
| W7T32 | Make One Trip Car-Free 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W7T33 | Walk Over 10,000 Steps 🚶 | 85 min | 3 | PhysicalActivity | standalone |
| W7T34 | Walk Over 8,000 Steps 🚶 | 70 min | 3 | PhysicalActivity | standalone |

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\free_spirited_social_student_0000\static\week_7_plan.json`
