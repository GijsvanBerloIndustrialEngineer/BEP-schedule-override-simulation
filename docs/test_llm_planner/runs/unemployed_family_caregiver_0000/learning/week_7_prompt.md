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

# Calendar of week 7 (17 Aug - 23 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-08-17 (planned busy time 11.3 h)
Free windows: 07:10-09:40, 10:10-11:10, 11:40-12:21, 12:41-13:20, 18:34-19:30, 21:00-21:30
Observed context: 09:11-11:11 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 17:30-18:30 social behavioural opportunity; 17:30-19:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 19:30-20:30 raining or snowing; 20:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-08-18 (planned busy time 10.2 h)
Free windows: 06:40-06:55, 08:40-10:10, 10:40-12:21, 12:41-13:30, 18:34-19:00, 20:00-21:30, 21:40-22:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 17:30-19:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-08-19 (planned busy time 12.5 h)
Free windows: 06:39-06:55, 09:00-09:55, 11:25-12:21, 12:41-13:50, 14:20-14:40, 16:30-17:00, 18:34-19:30
Observed context: 06:59-09:59 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 17:30-18:30 social behavioural opportunity; 17:30-19:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 19:30-21:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Thursday 2026-08-20 (planned busy time 12.2 h)
Free windows: 06:00-06:29, 06:39-06:55, 08:25-09:08, 11:08-12:21, 15:50-16:30, 18:34-19:30
Observed context: 06:30-07:30 suitable for outdoor; 07:30-09:00 raining or snowing; 12:00-13:00 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 16:30-17:30 physical behavioural opportunity; 17:30-18:30 social behavioural opportunity; 17:30-19:30 habitual behaviour; 17:30-19:30 low physical opportunity to enact a behaviour; 21:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-08-21 (planned busy time 9.7 h)
Free windows: 06:39-06:55, 10:00-10:10, 10:40-12:21, 12:41-13:40, 14:10-16:30, 18:34-20:00, 21:40-22:00
Observed context: 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:30 social behavioural opportunity; 20:30-22:00 low physical opportunity to enact a behaviour

### Saturday 2026-08-22 (planned busy time 11.5 h)
Free windows: 06:00-06:29, 06:39-06:55, 09:00-09:55, 11:25-12:21, 12:41-13:40, 15:40-16:10, 18:34-19:30
Observed context: 07:31-10:31 physical behavioural opportunity; 10:00-12:00 suitable for outdoor; 12:00-14:00 psychological behavioural capability; 17:30-18:30 social behavioural opportunity; 17:30-18:30 suitable for outdoor; 17:30-19:30 habitual behaviour; 18:30-19:00 raining or snowing; 19:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-08-23 (planned busy time 12.3 h)
Free windows: 06:39-07:20, 07:50-09:08, 11:08-12:21, 15:40-16:40, 21:40-22:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 17:30-18:30 suitable for outdoor; 17:30-19:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 21:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 7
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W7T01 | Add One Personal Touch 🪴 | 15 min | 1 | MentalWellbeing | standalone |
| W7T02 | Ask One Person for Support 💬 | 20 min | 1 | MentalWellbeing | alongside |
| W7T03 | Block Distractions 📵 | 5 min | 1 | MentalWellbeing | alongside |
| W7T04 | Care for One Friendship 🫂 | 10 min | 1 | MentalWellbeing | standalone |
| W7T05 | Eat A Lighter Dinner 🍽️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T06 | Log Afternoon Caffeine ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W7T07 | Move in the Afternoon 🚶 | 15 min | 2 | MentalWellbeing | alongside |
| W7T08 | Mute Non-Essential Notifications 🔕 | 5 min | 1 | MentalWellbeing | alongside |
| W7T09 | Plan a Coffee Chat ☕ | 30 min | 1 | MentalWellbeing | standalone |
| W7T10 | Play a Guided Meditation 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W7T11 | Read Something Calm 📖 | 20 min | 1 | MentalWellbeing | standalone |
| W7T12 | Schedule a Short Rest Break 🗓️ | 10 min | 1 | MentalWellbeing | alongside |
| W7T13 | Schedule One Enjoyable Activity 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T14 | Schedule One Social Moment 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T15 | Set a Podcast Sleep Timer 🎙️ | 15 min | 1 | MentalWellbeing | alongside |
| W7T16 | Set a Repeatable Bedtime 😴 | 10 min | 1 | MentalWellbeing | alongside |
| W7T17 | Set Up a Calm Spot 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W7T18 | Step Outside for Fresh Air 🌬️ | 5 min | 1 | MentalWellbeing | alongside |
| W7T19 | Write One Meaningful Action ✍️ | 15 min | 1 | MentalWellbeing | standalone |
| W7T20 | Write Tomorrow's List ✍️ | 10 min | 1 | MentalWellbeing | alongside |
| W7T21 | Eat One Screen-Free Meal 😌 | 20 min | 1 | Nutrition | standalone |
| W7T22 | Swap A Meaty Meal for Legumes 🍲 | 30 min | 2 | Nutrition | standalone |
| W7T23 | Try a Different Fruit 🥝 | 30 min | 1 | Nutrition | standalone |
| W7T24 | Try a Veggie Recipe 🧑‍🍳 | 30 min | 2 | Nutrition | standalone |
| W7T25 | Write a Grocery List 🛒 | 30 min | 1 | Nutrition | standalone |
| W7T26 | Clean Actively for 30 Minutes 🧹 | 30 min | 3 | PhysicalActivity | standalone |
| W7T27 | Do 30 Minutes of Cardio 💪 | 30 min | 2 | PhysicalActivity | standalone |
| W7T28 | Do 45 Minutes of Cardio 💪 | 45 min | 3 | PhysicalActivity | standalone |
| W7T29 | Make One Trip Car-Free 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W7T30 | Try Walk-Run Intervals 🏃 | 30 min | 3 | PhysicalActivity | standalone |
| W7T31 | Walk 6,000 to 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |
| W7T32 | Walk Over 10,000 Steps 🚶 | 85 min | 3 | PhysicalActivity | standalone |
| W7T33 | Walk Over 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 6
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Ask One Person for Support 💬 | Wed 12 Aug 12:00 | 10.6 h | psychological behavioural capability | done |
| Eat Dinner Earlier 🗓️ | Thu 13 Aug 18:00 | 13.2 h | habitual behaviour, social behavioural opportunity, suitable for outdoor | done |
| Log Afternoon Caffeine ☕ | Mon 10 Aug 15:00 | 11.2 h | - | done |
| Message One New Contact 💬 | Tue 11 Aug 11:30 | 10.2 h | - | done |
| Move in the Afternoon 🚶 | Thu 13 Aug 15:00 | 13.2 h | - | done |
| Plan a Low-Cost Outing 🗓️ | Mon 10 Aug 11:30 | 11.2 h | - | postponed, done later |
| Play a Guided Meditation 🧘 | Tue 11 Aug 12:00 | 10.2 h | physical behavioural opportunity, psychological behavioural capability | done |
| Schedule One Enjoyable Activity 🗓️ | Mon 10 Aug 11:50 | 11.2 h | - | done |
| Set a Podcast Sleep Timer 🎙️ | Wed 12 Aug 20:30 | 10.6 h | low physical opportunity to enact a behaviour | done |
| Write One Difficult Thought ✍️ | Fri 14 Aug 12:00 | 10.8 h | physical behavioural opportunity, psychological behavioural capability | done |
| Write One Kind No ✍️ | Mon 10 Aug 12:10 | 11.2 h | physical behavioural opportunity, psychological behavioural capability | skipped |
| Write One Meaningful Action ✍️ | Mon 10 Aug 12:50 | 11.2 h | physical behavioural opportunity, psychological behavioural capability | done |
| Write Tomorrow's List ✍️ | Fri 14 Aug 21:00 | 10.8 h | low physical opportunity to enact a behaviour | done |
| Share a Meal 🌮 | Thu 13 Aug 11:30 | 13.2 h | - | done |
| Add Five Walk Minutes 🚶 | Thu 13 Aug 11:10 | 13.2 h | - | done |
| Clean Actively for 10 Minutes 🧹 | Tue 11 Aug 13:10 | 10.2 h | physical behavioural opportunity, psychological behavioural capability | done |
| Clean Actively for 20 Minutes 🧹 | Tue 11 Aug 13:20 | 10.2 h | physical behavioural opportunity, psychological behavioural capability | done |
| Do 20 Minutes of Cardio 💪 | Tue 11 Aug 12:50 | 10.2 h | physical behavioural opportunity, psychological behavioural capability | postponed, done later |
| Do 30 Minutes of Cardio 💪 | Mon 10 Aug 14:00 | 11.2 h | - | done |
| Plan Sitting Breaks 🗓️ | Mon 10 Aug 13:20 | 11.2 h | - | done |
| Schedule a 30-Minute Walk 🚶 | Mon 10 Aug 09:20 | 11.2 h | physical behavioural opportunity | postponed, done later |
| Try Walk-Run Intervals 🏃 | Thu 13 Aug 12:50 | 13.2 h | physical behavioural opportunity, psychological behavioural capability | done |
| Walk 4,000 to 6,000 Steps 🚶 | Wed 12 Aug 14:00 | 10.6 h | - | skipped |
| Walk 6,000 to 8,000 Steps 🚶 | Sun 16 Aug 11:10 | 12.4 h | - | done |
| Walk One Routine Route 🚶 | Tue 11 Aug 14:10 | 10.2 h | physical behavioural opportunity | done |
| Plan a Coffee Chat ☕ | Wed 12 Aug 12:50 | 10.6 h | psychological behavioural capability | done |

## Memory: completion rate of your placements so far (weeks 1-6)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | afternoon | 50 / 57 | 88% |
| time of day | morning | 18 / 22 | 82% |
| time of day | evening | 9 / 10 | 90% |
| day type | weekday | 76 / 88 | 86% |
| day load | heavy (>9 h) | 77 / 89 | 87% |
| intensity | intensity 1 | 55 / 61 | 90% |
| intensity | intensity 2 | 16 / 22 | 73% |
| intensity | intensity 3 | 6 / 6 | 100% |
| observed context at the planned time | psychological behavioural capability | 34 / 39 | 87% |
| observed context at the planned time | physical behavioural opportunity | 31 / 35 | 89% |
| observed context at the planned time | suitable for outdoor | 4 / 6 | 67% |
| observed context at the planned time | habitual behaviour | 3 / 4 | 75% |
| observed context at the planned time | social behavioural opportunity | 3 / 3 | 100% |
| observed context at the planned time | low physical opportunity to enact a behaviour | 3 / 3 | 100% |

## Your lessons from last week
She follows through best at midday and afternoons on weekdays, esp. with psychological capability or physical opportunity. Intensity 1 is reliable; intensity 2 less so (64%), but intensity 3 midday worked. Morning is weaker. Light planning tasks postponed when clustered near busy Monday midday, so I spread them and kept hard tasks in 12:00-14:00 weekday windows. Alongside tasks sit at midday, afternoon or habitual evening times; the one long walk goes Sunday midday.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\unemployed_family_caregiver_0000\learning\week_7_plan.json`
