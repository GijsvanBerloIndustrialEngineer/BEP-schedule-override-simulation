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

# Calendar of week 5 (03 Aug - 09 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-08-03 (planned busy time 11.3 h)
Free windows: 06:39-06:55, 08:25-08:40, 09:10-09:55, 11:25-12:20, 14:20-15:50, 16:10-16:20, 18:34-20:00, 21:40-22:00
Observed context: 07:41-09:41 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-19:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 20:30-21:30 raining or snowing; 20:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-08-04 (planned busy time 11.2 h)
Free windows: 06:00-06:29, 06:39-06:55, 08:25-08:40, 12:10-12:21, 12:41-14:00, 18:34-21:30
Observed context: 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-18:30 social behavioural opportunity; 17:30-19:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 19:30-20:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-08-05 (planned busy time 10.4 h)
Free windows: 06:39-06:55, 09:10-09:55, 11:25-12:21, 12:41-13:00, 13:30-14:50, 16:20-16:30, 18:34-20:00, 20:30-21:30, 21:40-22:00
Observed context: 07:41-09:41 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 17:30-19:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-20:30 suitable for outdoor; 19:30-22:00 low physical opportunity to enact a behaviour; 20:30-21:30 raining or snowing

### Thursday 2026-08-06 (planned busy time 13.2 h)
Free windows: 06:39-06:55, 08:25-09:08, 11:08-11:20, 12:41-13:00, 15:00-15:10, 16:40-17:00, 18:34-19:10, 20:40-21:30, 21:40-22:00
Observed context: 06:30-07:30 habitual behaviour; 11:00-12:00 habitual behaviour; 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-18:30 social behavioural opportunity; 17:30-18:30 suitable for outdoor; 20:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-08-07 (planned busy time 10.8 h)
Free windows: 07:10-09:00, 10:00-10:40, 12:40-13:40, 14:00-14:30, 17:30-18:04, 18:34-19:50, 21:40-22:00
Observed context: 12:00-13:00 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 15:30-17:30 physical behavioural opportunity; 17:30-18:30 low physical opportunity to enact a behaviour; 17:30-18:30 social behavioural opportunity; 17:30-18:30 suitable for outdoor; 17:30-19:00 habitual behaviour

### Saturday 2026-08-08 (planned busy time 10.7 h)
Free windows: 06:39-06:55, 09:00-09:55, 11:25-12:21, 12:41-13:40, 14:10-16:00, 18:34-19:10, 20:40-21:30, 21:40-22:00
Observed context: 07:31-09:31 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-19:00 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-19:30 suitable for outdoor; 19:30-21:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-08-09 (planned busy time 13.4 h)
Free windows: 06:39-06:55, 09:50-10:00, 10:30-11:00, 16:40-18:10, 20:10-21:00, 21:40-22:00
Observed context: 11:30-12:00 habitual behaviour; 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-19:00 habitual behaviour; 17:30-19:30 social behavioural opportunity; 19:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 5
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W5T01 | Set a Podcast Sleep Timer 🎙️ | 15 min | 1 | MentalWellbeing | alongside |
| W5T02 | Batch-Cook Healthy Meal 🍲 | 120 min | 2 | Nutrition | standalone |
| W5T03 | Eat Dinner Earlier 🗓️ | 15 min | 1 | Nutrition | alongside |
| W5T04 | Plan Meals and Groceries 🗓️ | 60 min | 1 | Nutrition | standalone |
| W5T05 | Do 30 Minutes of Cardio 💪 | 30 min | 3 | PhysicalActivity | standalone |
| W5T06 | Move in the Afternoon 🚶 | 15 min | 1 | PhysicalActivity | alongside |
| W5T07 | Try Walk-Run Intervals 🏃 | 30 min | 3 | PhysicalActivity | standalone |
| W5T08 | Walk 6,000 to 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |
| W5T09 | Walk One Routine Route 🚶 | 25 min | 2 | PhysicalActivity | standalone |
| W5T10 | Message One New Contact 💬 | 30 min | 1 | Unknown | standalone |
| W5T11 | Plan a Low-Cost Outing 🗓️ | 15 min | 1 | Unknown | standalone |
| W5T12 | Schedule One Enjoyable Activity 🗓️ | 15 min | 1 | Unknown | standalone |
| W5T13 | Write One Kind No ✍️ | 10 min | 1 | Unknown | standalone |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 4
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Plan a Coffee Chat ☕ | Mon 27 Jul 12:50 | 10.4 h | psychological behavioural capability | done |
| Plan Three Recharge Activities 🗓️ | Mon 27 Jul 13:30 | 10.4 h | psychological behavioural capability | skipped |
| Set Up a Calm Spot 🧘 | Tue 28 Jul 12:00 | 11.2 h | physical behavioural opportunity, psychological behavioural capability | skipped |
| Do 20 Minutes of Cardio 💪 | Wed 29 Jul 14:00 | 11.2 h | - | done |
| Log Run Wins 🏅 | Thu 30 Jul 12:30 | 12.2 h | physical behavioural opportunity, psychological behavioural capability | skipped |
| Plan Sitting Breaks 🗓️ | Wed 29 Jul 12:00 | 11.2 h | psychological behavioural capability | done |
| Plan This Week's Exercises 🗓️ | Wed 29 Jul 13:20 | 11.2 h | - | done |
| Tell Someone Your Plan 💬 | Fri 31 Jul 12:30 | 9.7 h | physical behavioural opportunity, psychological behavioural capability | done |

## Memory: completion rate of your placements so far (weeks 1-4)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | afternoon | 29 / 33 | 88% |
| time of day | morning | 9 / 13 | 69% |
| time of day | evening | 4 / 4 | 100% |
| day type | weekday | 42 / 50 | 84% |
| day load | heavy (>9 h) | 42 / 50 | 84% |
| intensity | intensity 1 | 33 / 38 | 87% |
| intensity | intensity 2 | 8 / 11 | 73% |
| observed context at the planned time | psychological behavioural capability | 22 / 26 | 85% |
| observed context at the planned time | physical behavioural opportunity | 20 / 23 | 87% |
| observed context at the planned time | suitable for outdoor | 2 / 3 | 67% |
| observed context at the planned time | habitual behaviour | 2 / 2 | 100% |

## Your lessons from last week
This person follows through best at midday (12:00-14:00) and in afternoons, especially with psychological capability and physical opportunity; mornings, outdoor-context and late-evening slots are skipped or postponed more often. Heavy days are not a problem. Intensity 1 tasks are done reliably, higher intensity less so, so I keep the cardio at midday/early afternoon and cluster tasks in lunch windows on weekdays, avoiding weekends.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\unemployed_family_caregiver_0000\learning\week_5_plan.json`
