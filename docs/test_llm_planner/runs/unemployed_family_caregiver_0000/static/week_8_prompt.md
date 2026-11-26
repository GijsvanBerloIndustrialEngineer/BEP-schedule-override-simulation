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

# Calendar of week 8 (24 Aug - 30 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-08-24 (planned busy time 12.2 h)
Free windows: 06:00-06:29, 06:39-06:55, 08:25-08:40, 11:10-12:21, 12:41-13:30, 15:00-15:10, 16:40-17:00, 18:34-18:50, 20:20-20:30, 21:40-21:50
Observed context: 07:41-10:41 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-08-25 (planned busy time 10.3 h)
Free windows: 06:00-06:29, 06:39-06:55, 08:25-09:55, 11:25-12:40, 13:10-13:30, 13:50-14:50, 19:40-20:00, 21:40-22:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 20:30-22:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-08-26 (planned busy time 12.2 h)
Free windows: 06:39-06:55, 10:30-11:20, 11:50-12:21, 13:20-14:00, 18:34-20:00, 21:40-22:00
Observed context: 09:01-11:01 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-18:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 20:30-21:00 raining or snowing; 20:30-22:00 low physical opportunity to enact a behaviour

### Thursday 2026-08-27 (planned busy time 12.4 h)
Free windows: 06:39-06:55, 08:40-09:08, 11:08-12:21, 12:41-13:00, 14:30-14:40, 16:10-17:00, 18:34-19:10, 19:40-20:00, 21:40-22:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 17:30-19:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-19:30 suitable for outdoor; 20:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-08-28 (planned busy time 10.8 h)
Free windows: 06:00-06:29, 06:39-06:55, 08:25-09:55, 11:25-12:21, 18:34-21:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-18:30 social behavioural opportunity; 17:30-18:30 suitable for outdoor; 17:30-19:30 habitual behaviour; 18:30-20:00 raining or snowing; 19:30-22:00 low physical opportunity to enact a behaviour

### Saturday 2026-08-29 (planned busy time 10.2 h)
Free windows: 06:39-06:55, 08:30-08:50, 09:20-09:55, 11:25-12:21, 12:41-13:40, 14:10-15:00, 18:34-20:20, 20:50-21:30, 21:40-22:00
Observed context: 07:19-10:19 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-18:30 social behavioural opportunity; 17:30-19:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 19:30-20:00 raining or snowing; 20:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-08-30 (planned busy time 11.8 h)
Free windows: 06:39-06:55, 11:08-12:21, 12:41-13:10, 16:10-16:50, 17:20-18:04, 18:34-19:40, 21:10-21:30, 21:40-22:00
Observed context: 12:00-14:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 20:30-21:30 raining or snowing; 20:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 8
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W8T01 | Ask One Person for Support 💬 | 20 min | 1 | MentalWellbeing | alongside |
| W8T02 | Block Distractions 📵 | 5 min | 1 | MentalWellbeing | alongside |
| W8T03 | Care for One Friendship 🫂 | 10 min | 1 | MentalWellbeing | standalone |
| W8T04 | Eat A Lighter Dinner 🍽️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T05 | Log Afternoon Caffeine ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W8T06 | Message One New Contact 💬 | 30 min | 1 | MentalWellbeing | standalone |
| W8T07 | Move in the Afternoon 🚶 | 15 min | 2 | MentalWellbeing | alongside |
| W8T08 | Mute Non-Essential Notifications 🔕 | 5 min | 1 | MentalWellbeing | alongside |
| W8T09 | Plan a Coffee Chat ☕ | 30 min | 1 | MentalWellbeing | standalone |
| W8T10 | Plan Three Recharge Activities 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T11 | Play a Guided Meditation 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W8T12 | Play Calm Sleep Sounds 🎶 | 10 min | 1 | MentalWellbeing | alongside |
| W8T13 | Read Something Calm 📖 | 20 min | 1 | MentalWellbeing | standalone |
| W8T14 | Schedule a Short Rest Break 🗓️ | 10 min | 1 | MentalWellbeing | alongside |
| W8T15 | Schedule One Enjoyable Activity 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T16 | Schedule One Social Moment 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T17 | Set a Podcast Sleep Timer 🎙️ | 15 min | 1 | MentalWellbeing | alongside |
| W8T18 | Set a Repeatable Bedtime 😴 | 10 min | 1 | MentalWellbeing | alongside |
| W8T19 | Set Up a Calm Spot 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W8T20 | Start One Conversation 💬 | 10 min | 1 | MentalWellbeing | standalone |
| W8T21 | Step Outside for Fresh Air 🌬️ | 5 min | 1 | MentalWellbeing | alongside |
| W8T22 | Write About Stressors ⚡ | 15 min | 1 | MentalWellbeing | alongside |
| W8T23 | Write One Kind No ✍️ | 10 min | 1 | MentalWellbeing | standalone |
| W8T24 | Write One Meaningful Action ✍️ | 15 min | 1 | MentalWellbeing | standalone |
| W8T25 | Write Tomorrow's List ✍️ | 10 min | 1 | MentalWellbeing | alongside |
| W8T26 | Eat One Screen-Free Meal 😌 | 20 min | 1 | Nutrition | standalone |
| W8T27 | Plan Meals and Groceries 🗓️ | 60 min | 1 | Nutrition | standalone |
| W8T28 | Share a Meal 🌮 | 30 min | 1 | Nutrition | standalone |
| W8T29 | Swap A Meaty Meal for Legumes 🍲 | 30 min | 2 | Nutrition | standalone |
| W8T30 | Try a Different Fruit 🥝 | 30 min | 1 | Nutrition | standalone |
| W8T31 | Try a Veggie Recipe 🧑‍🍳 | 30 min | 2 | Nutrition | standalone |
| W8T32 | Write a Grocery List 🛒 | 30 min | 1 | Nutrition | standalone |
| W8T33 | Do 30 Minutes of Cardio 💪 | 30 min | 3 | PhysicalActivity | standalone |
| W8T34 | Do 45 Minutes of Cardio 💪 | 45 min | 3 | PhysicalActivity | standalone |
| W8T35 | Make One Trip Car-Free 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W8T36 | Walk Over 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\unemployed_family_caregiver_0000\static\week_8_plan.json`
