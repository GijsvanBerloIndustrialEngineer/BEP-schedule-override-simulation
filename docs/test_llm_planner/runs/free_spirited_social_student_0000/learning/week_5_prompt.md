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

# Calendar of week 5 (03 Aug - 09 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-08-03 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 10:00-14:00 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 16:00-17:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-19:30 physical behavioural opportunity; 18:30-21:30 social behavioural opportunity

### Tuesday 2026-08-04 (planned busy time 11.8 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:10, 17:40-17:50, 19:39-19:50
Observed context: 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-20:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 18:30-19:00 raining or snowing

### Wednesday 2026-08-05 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 15:30-19:30 physical behavioural opportunity; 16:00-20:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 18:30-19:00 raining or snowing

### Thursday 2026-08-06 (planned busy time 11.8 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:10, 17:40-17:50, 19:39-19:50
Observed context: 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 16:00-20:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-20:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 20:30-21:30 raining or snowing

### Friday 2026-08-07 (planned busy time 11.7 h)
Free windows: 06:00-07:49, 12:04-13:38, 13:58-15:30, 19:39-19:50
Observed context: 06:30-08:30 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 15:30-19:30 physical behavioural opportunity; 16:00-20:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-20:30 suitable for outdoor; 20:30-21:30 raining or snowing

### Saturday 2026-08-08 (planned busy time 9.8 h)
Free windows: 06:00-07:49, 10:00-12:00, 13:58-14:11, 15:01-17:10, 17:30-17:40, 21:10-21:26, 21:36-21:50
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 16:00-20:30 social behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-21:30 physical behavioural opportunity; 18:30-19:30 raining or snowing

### Sunday 2026-08-09 (planned busy time 10.3 h)
Free windows: 06:00-07:49, 07:59-12:15, 19:30-19:40, 21:10-21:26
Observed context: 12:00-14:00 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 15:30-21:30 physical behavioural opportunity; 16:00-17:30 social behavioural opportunity; 17:30-18:00 habitual behaviour; 17:30-19:30 suitable for outdoor; 18:30-21:30 social behavioural opportunity

# Health tasks of week 5
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W5T01 | Set a Podcast Sleep Timer 🎙️ | 15 min | 1 | MentalWellbeing | alongside |
| W5T02 | Batch-Cook Healthy Meal 🍲 | 120 min | 2 | Nutrition | standalone |
| W5T03 | Eat Dinner Earlier 🗓️ | 15 min | 1 | Nutrition | alongside |
| W5T04 | Make a Calming Drink ☕ | 10 min | 1 | Nutrition | alongside |
| W5T05 | Plan Meals and Groceries 🗓️ | 60 min | 2 | Nutrition | standalone |
| W5T06 | Clean Actively for 20 Minutes 🧹 | 20 min | 2 | PhysicalActivity | standalone |
| W5T07 | Do 30 Minutes of Cardio 💪 | 30 min | 3 | PhysicalActivity | standalone |
| W5T08 | Try Walk-Run Intervals 🏃 | 30 min | 3 | PhysicalActivity | standalone |
| W5T09 | Walk 6,000 to 8,000 Steps 🚶 | 70 min | 2 | PhysicalActivity | standalone |
| W5T10 | Make One Trip Car-Free 🚶 | 30 min | 2 | Unknown | standalone |
| W5T11 | Message One New Contact 💬 | 30 min | 1 | Unknown | standalone |
| W5T12 | Plan a Low-Cost Outing 🗓️ | 15 min | 1 | Unknown | standalone |
| W5T13 | Schedule One Enjoyable Activity 🗓️ | 15 min | 1 | Unknown | standalone |
| W5T14 | Write One Kind No ✍️ | 10 min | 1 | Unknown | standalone |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 4
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Plan This Week's Exercises 🗓️ | Mon 27 Jul 12:10 | 11.7 h | psychological behavioural capability, social behavioural opportunity | skipped |
| Plan Sitting Breaks 🗓️ | Mon 27 Jul 12:50 | 11.7 h | psychological behavioural capability, social behavioural opportunity | done |
| Write One Movement Step ✍️ | Mon 27 Jul 13:10 | 11.7 h | psychological behavioural capability, social behavioural opportunity | done |
| Set Up a Calm Spot 🧘 | Tue 28 Jul 12:10 | 11.7 h | psychological behavioural capability | skipped |
| Clean Actively for 10 Minutes 🧹 | Tue 28 Jul 12:40 | 11.7 h | psychological behavioural capability | done |
| Walk One Routine Route 🚶 | Wed 29 Jul 12:10 | 11.7 h | physical behavioural opportunity, psychological behavioural capability | postponed, done later |
| Write About Stressors ⚡ | Wed 29 Jul 13:00 | 11.7 h | physical behavioural opportunity, psychological behavioural capability | done |
| Move for 10 Minutes 💪 | Fri 31 Jul 12:10 | 11.7 h | psychological behavioural capability, social behavioural opportunity | skipped |
| Move in the Afternoon 🚶 | Fri 31 Jul 14:00 | 11.7 h | - | done |
| Walk Somewhere Nearby 🚶 | Sat 01 Aug 10:00 | 9.8 h | - | done |
| 7-Minute Workout 💪 | Sun 02 Aug 09:00 | 10.3 h | - | done |

## Memory: completion rate of your placements so far (weeks 1-4)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | afternoon | 28 / 34 | 82% |
| time of day | morning | 13 / 16 | 81% |
| time of day | evening | 2 / 2 | 100% |
| day type | weekday | 31 / 39 | 79% |
| day type | weekend | 12 / 13 | 92% |
| day load | heavy (>9 h) | 43 / 52 | 83% |
| intensity | intensity 1 | 31 / 39 | 79% |
| intensity | intensity 2 | 10 / 11 | 91% |
| intensity | intensity 3 | 2 / 2 | 100% |
| observed context at the planned time | psychological behavioural capability | 22 / 28 | 79% |
| observed context at the planned time | physical behavioural opportunity | 19 / 21 | 90% |
| observed context at the planned time | social behavioural opportunity | 10 / 14 | 71% |

## Your lessons from last week
This person follows through best on midday weekday windows (12:00-13:30) and weekend mornings; intensity 1-2 tasks are done reliably. Early mornings and evenings are less reliable (social plans), so standalone tasks go at lunch or Saturday morning, alongside tasks in the afternoon. Keep two or three tasks per day, put walks at lunch or on weekend mornings, and avoid evening standalone tasks.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\free_spirited_social_student_0000\learning\week_5_plan.json`
