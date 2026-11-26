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

# Calendar of week 3 (20 Jul - 26 Jul 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-07-20 (planned busy time 10.2 h)
Free windows: 06:39-06:55, 09:00-09:55, 11:25-12:30, 13:00-13:50, 14:10-16:30, 18:34-20:00, 21:40-22:00
Observed context: 07:31-09:31 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-19:00 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 20:30-21:30 raining or snowing; 20:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-07-21 (planned busy time 10.3 h)
Free windows: 06:39-06:55, 08:25-09:55, 11:25-12:21, 12:41-13:10, 14:40-17:50, 18:20-19:20
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 17:30-18:30 social behavioural opportunity; 17:30-18:30 suitable for outdoor; 17:30-19:00 habitual behaviour; 18:30-20:00 raining or snowing; 20:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-07-22 (planned busy time 10.7 h)
Free windows: 06:39-07:40, 08:10-08:40, 09:10-09:55, 11:25-12:21, 12:41-14:00, 15:30-16:00, 18:34-20:00, 21:40-22:00
Observed context: 06:41-09:41 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-19:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-19:30 suitable for outdoor; 21:30-22:00 low physical opportunity to enact a behaviour

### Thursday 2026-07-23 (planned busy time 11.9 h)
Free windows: 06:39-06:55, 11:08-12:21, 12:41-14:50, 18:34-19:10, 20:40-21:30, 21:40-21:50
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-19:00 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-19:30 suitable for outdoor; 19:30-20:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-07-24 (planned busy time 10.3 h)
Free windows: 07:10-09:55, 11:25-12:21, 12:41-13:50, 15:20-15:50, 18:34-20:00, 21:40-22:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-18:30 suitable for outdoor; 17:30-19:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 18:30-19:30 raining or snowing; 20:30-22:00 low physical opportunity to enact a behaviour

### Saturday 2026-07-25 (planned busy time 11.2 h)
Free windows: 06:39-06:55, 08:25-08:40, 09:10-09:55, 11:25-12:21, 12:41-15:00, 15:30-16:30, 18:34-19:30
Observed context: 07:41-09:41 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:30 social behavioural opportunity; 18:30-19:00 raining or snowing; 19:00-20:00 suitable for outdoor; 19:30-22:00 low physical opportunity to enact a behaviour; 20:00-21:00 raining or snowing

### Sunday 2026-07-26 (planned busy time 11.8 h)
Free windows: 06:00-06:20, 11:08-12:21, 12:41-14:00, 18:40-18:50, 19:20-20:10, 21:40-22:00
Observed context: 12:00-14:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-18:30 social behavioural opportunity; 17:30-19:00 habitual behaviour; 19:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 3
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W3T01 | Ask One Person for Support 💬 | 20 min | 1 | MentalWellbeing | alongside |
| W3T02 | Eat A Lighter Dinner 🍽️ | 15 min | 1 | MentalWellbeing | standalone |
| W3T03 | Log Afternoon Caffeine ☕ | 10 min | 1 | MentalWellbeing | alongside |
| W3T04 | Play a Guided Meditation 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W3T05 | Set a Repeatable Bedtime 😴 | 10 min | 1 | MentalWellbeing | alongside |
| W3T06 | Write One Difficult Thought ✍️ | 15 min | 1 | MentalWellbeing | alongside |
| W3T07 | Write One Meaningful Action ✍️ | 15 min | 1 | MentalWellbeing | standalone |
| W3T08 | Write Tomorrow's List ✍️ | 10 min | 1 | MentalWellbeing | alongside |
| W3T09 | Share a Meal 🌮 | 30 min | 1 | Nutrition | standalone |
| W3T10 | Try a Veggie Recipe 🧑‍🍳 | 30 min | 2 | Nutrition | standalone |
| W3T11 | Do 15 Minutes of Cardio 💪 | 15 min | 2 | PhysicalActivity | standalone |
| W3T12 | Log Each Walk 📒 | 15 min | 1 | PhysicalActivity | alongside |
| W3T13 | Prepare Your Workout Clothes 👟 | 10 min | 1 | PhysicalActivity | alongside |
| W3T14 | Schedule a 30-Minute Walk 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W3T15 | Tidy Up for 5 Minutes 🧹 | 5 min | 1 | PhysicalActivity | standalone |
| W3T16 | Walk a New Route 🚶 | 15 min | 2 | PhysicalActivity | standalone |
| W3T17 | Walk Somewhere Nearby 🚶 | 30 min | 2 | PhysicalActivity | standalone |
| W3T18 | Write a Backup Plan 🗓️ | 5 min | 1 | PhysicalActivity | standalone |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 2
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Add One Personal Touch 🪴 | Tue 14 Jul 08:30 | 11.2 h | - | done |
| Care for One Friendship 🫂 | Wed 15 Jul 12:50 | 10.6 h | psychological behavioural capability | done |
| Get Morning Light ☀️ | Mon 13 Jul 06:40 | 12.2 h | suitable for outdoor | skipped |
| Prepare a Sleep-Friendly Room 😴 | Wed 15 Jul 14:10 | 10.6 h | - | postponed, done later |
| Schedule a Short Rest Break 🗓️ | Thu 16 Jul 12:00 | 12.2 h | physical behavioural opportunity, psychological behavioural capability | done |
| Schedule One Social Moment 🗓️ | Wed 15 Jul 18:40 | 10.6 h | habitual behaviour, suitable for outdoor | done |
| Step Outside for Fresh Air 🌬️ | Wed 15 Jul 09:20 | 10.6 h | physical behavioural opportunity | skipped |
| Write About Stressors ⚡ | Thu 16 Jul 12:30 | 12.2 h | physical behavioural opportunity, psychological behavioural capability | done |
| Write Control Table ✍️ | Fri 17 Jul 12:00 | 12.2 h | physical behavioural opportunity, psychological behavioural capability | postponed, done later |
| Drink A Glass of Water 🫗 | Tue 14 Jul 12:00 | 11.2 h | physical behavioural opportunity, psychological behavioural capability | done |
| Try a Different Fruit 🥝 | Tue 14 Jul 11:40 | 11.2 h | - | done |
| Add Five Walk Minutes 🚶 | Mon 13 Jul 09:10 | 12.2 h | physical behavioural opportunity | postponed, done later |
| Log How Movement Felt ✍️ | Mon 13 Jul 12:00 | 12.2 h | psychological behavioural capability | done |
| Walk Over 2,000 Steps 🚶 | Mon 13 Jul 11:30 | 12.2 h | - | done |

## Memory: completion rate of your placements so far (weeks 1-2)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | afternoon | 13 / 13 | 100% |
| time of day | morning | 7 / 9 | 78% |
| time of day | evening | 2 / 2 | 100% |
| day type | weekday | 22 / 24 | 92% |
| day load | heavy (>9 h) | 22 / 24 | 92% |
| intensity | intensity 1 | 17 / 19 | 89% |
| intensity | intensity 2 | 5 / 5 | 100% |
| observed context at the planned time | physical behavioural opportunity | 12 / 13 | 92% |
| observed context at the planned time | psychological behavioural capability | 10 / 10 | 100% |
| observed context at the planned time | habitual behaviour | 2 / 2 | 100% |
| observed context at the planned time | suitable for outdoor | 1 / 2 | 50% |

## Your lessons from last week
Week 1 had 100% completion everywhere, so no factor is discriminating yet. I assume this caregiver follows through best in midday windows (12:00-14:00, psychological capability/physical opportunity) and mornings with physical opportunity. Walks go in those slots. Short alongside tasks are anchored to lunch and routines. One social task sits in the habitual early evening. Tasks are spread over weekdays; weekends and low-opportunity evenings are avoided.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\unemployed_family_caregiver_0000\learning\week_3_plan.json`
