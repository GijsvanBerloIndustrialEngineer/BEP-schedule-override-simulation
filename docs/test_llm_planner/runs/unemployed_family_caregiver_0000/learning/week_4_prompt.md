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

# Calendar of week 4 (27 Jul - 02 Aug 2026)
Free windows are the times without planned activities between 06:00 and 22:00. Observed context comes from the person's sensors and check-ins.

### Monday 2026-07-27 (planned busy time 10.4 h)
Free windows: 06:00-06:29, 06:39-06:55, 09:10-09:55, 11:25-12:21, 12:41-13:50, 14:20-15:00, 18:34-20:00, 21:40-21:50
Observed context: 07:09-10:09 physical behavioural opportunity; 12:00-14:00 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-18:30 suitable for outdoor; 17:30-19:30 social behavioural opportunity; 18:30-19:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Tuesday 2026-07-28 (planned busy time 11.2 h)
Free windows: 06:00-06:29, 06:39-06:55, 08:25-09:55, 11:25-12:21, 14:20-14:40, 16:40-17:00, 20:10-21:30
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-18:30 suitable for outdoor; 17:30-19:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 18:30-19:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Wednesday 2026-07-29 (planned busy time 11.2 h)
Free windows: 06:39-07:10, 07:40-08:10, 08:40-08:50, 11:25-12:21, 13:20-14:50, 16:20-16:30, 18:34-19:40, 21:10-21:30, 21:40-22:00
Observed context: 06:30-08:30 physical behavioural opportunity; 12:00-13:00 psychological behavioural capability; 17:30-18:30 suitable for outdoor; 17:30-19:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 18:30-19:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Thursday 2026-07-30 (planned busy time 12.2 h)
Free windows: 06:39-07:00, 11:08-12:21, 14:20-15:50, 17:20-18:00, 19:30-20:10, 20:40-21:30
Observed context: 12:00-14:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-19:30 social behavioural opportunity; 17:30-19:30 suitable for outdoor; 21:30-22:00 low physical opportunity to enact a behaviour

### Friday 2026-07-31 (planned busy time 9.7 h)
Free windows: 06:00-06:29, 06:39-06:55, 08:25-09:55, 11:25-12:21, 12:41-14:30, 18:34-20:00, 21:40-22:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-15:00 physical behavioural opportunity; 17:30-18:30 habitual behaviour; 17:30-18:30 social behavioural opportunity; 17:30-19:30 suitable for outdoor; 19:30-21:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Saturday 2026-08-01 (planned busy time 11.2 h)
Free windows: 06:39-06:55, 08:25-08:50, 09:20-09:55, 11:25-12:21, 12:41-13:00, 13:30-13:50, 14:20-16:30, 20:10-21:30
Observed context: 07:51-09:51 physical behavioural opportunity; 11:00-12:00 suitable for outdoor; 12:00-14:00 psychological behavioural capability; 17:30-18:30 habitual behaviour; 17:30-18:30 social behavioural opportunity; 17:30-19:30 suitable for outdoor; 19:30-20:30 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

### Sunday 2026-08-02 (planned busy time 13.4 h)
Free windows: 06:39-06:55, 11:08-12:21, 14:30-15:30, 19:00-19:20, 21:20-21:30, 21:40-22:00
Observed context: 12:00-13:00 psychological behavioural capability; 12:00-14:00 physical behavioural opportunity; 17:30-18:30 social behavioural opportunity; 17:30-19:30 habitual behaviour; 17:30-19:30 suitable for outdoor; 19:30-21:00 raining or snowing; 21:30-22:00 low physical opportunity to enact a behaviour

# Health tasks of week 4
| id | task | duration | intensity (1-4) | domain | type |
|---|---|---|---|---|---|
| W4T01 | Plan a Coffee Chat ☕ | 30 min | 1 | MentalWellbeing | standalone |
| W4T02 | Plan Three Recharge Activities 🗓️ | 15 min | 1 | MentalWellbeing | standalone |
| W4T03 | Set Up a Calm Spot 🧘 | 15 min | 1 | MentalWellbeing | standalone |
| W4T04 | Do 20 Minutes of Cardio 💪 | 20 min | 3 | PhysicalActivity | standalone |
| W4T05 | Log Run Wins 🏅 | 5 min | 1 | PhysicalActivity | alongside |
| W4T06 | Plan Sitting Breaks 🗓️ | 5 min | 1 | PhysicalActivity | standalone |
| W4T07 | Plan This Week's Exercises 🗓️ | 30 min | 2 | PhysicalActivity | standalone |
| W4T08 | Tell Someone Your Plan 💬 | 10 min | 1 | PhysicalActivity | alongside |

# Learning model: feedback from the executed calendar
## What happened to your plan of week 3
| task | planned at | busy time that day | observed context then | outcome |
|---|---|---|---|---|
| Ask One Person for Support 💬 | Fri 24 Jul 12:00 | 10.3 h | physical behavioural opportunity, psychological behavioural capability | done |
| Eat A Lighter Dinner 🍽️ | Thu 23 Jul 13:30 | 11.9 h | physical behavioural opportunity | done |
| Log Afternoon Caffeine ☕ | Wed 22 Jul 15:30 | 10.7 h | - | done |
| Play a Guided Meditation 🧘 | Mon 20 Jul 12:00 | 10.2 h | psychological behavioural capability | done |
| Set a Repeatable Bedtime 😴 | Thu 23 Jul 21:00 | 11.9 h | - | done |
| Write One Difficult Thought ✍️ | Fri 24 Jul 12:30 | 10.3 h | physical behavioural opportunity, psychological behavioural capability | done |
| Write One Meaningful Action ✍️ | Mon 20 Jul 11:40 | 10.2 h | - | done |
| Write Tomorrow's List ✍️ | Mon 20 Jul 19:00 | 10.2 h | social behavioural opportunity, suitable for outdoor | done |
| Share a Meal 🌮 | Thu 23 Jul 12:50 | 11.9 h | physical behavioural opportunity, psychological behavioural capability | done |
| Try a Veggie Recipe 🧑‍🍳 | Wed 22 Jul 11:30 | 10.7 h | - | skipped |
| Do 15 Minutes of Cardio 💪 | Wed 22 Jul 13:20 | 10.7 h | psychological behavioural capability | skipped |
| Log Each Walk 📒 | Wed 22 Jul 13:40 | 10.7 h | psychological behavioural capability | done |
| Prepare Your Workout Clothes 👟 | Mon 20 Jul 09:00 | 10.2 h | physical behavioural opportunity | postponed, done later |
| Schedule a 30-Minute Walk 🚶 | Tue 21 Jul 11:30 | 10.3 h | - | skipped |
| Tidy Up for 5 Minutes 🧹 | Tue 21 Jul 12:50 | 10.3 h | physical behavioural opportunity, psychological behavioural capability | done |
| Walk a New Route 🚶 | Tue 21 Jul 12:00 | 10.3 h | physical behavioural opportunity, psychological behavioural capability | done |
| Walk Somewhere Nearby 🚶 | Wed 22 Jul 12:50 | 10.7 h | psychological behavioural capability | postponed, done later |
| Write a Backup Plan 🗓️ | Mon 20 Jul 13:00 | 10.2 h | psychological behavioural capability | done |

## Memory: completion rate of your placements so far (weeks 1-3)
| factor | value | done / placed | rate |
|---|---|---|---|
| time of day | afternoon | 24 / 25 | 96% |
| time of day | morning | 9 / 13 | 69% |
| time of day | evening | 4 / 4 | 100% |
| day type | weekday | 37 / 42 | 88% |
| day load | heavy (>9 h) | 37 / 42 | 88% |
| intensity | intensity 1 | 30 / 32 | 94% |
| intensity | intensity 2 | 7 / 10 | 70% |
| observed context at the planned time | psychological behavioural capability | 19 / 20 | 95% |
| observed context at the planned time | physical behavioural opportunity | 19 / 20 | 95% |
| observed context at the planned time | suitable for outdoor | 2 / 3 | 67% |
| observed context at the planned time | habitual behaviour | 2 / 2 | 100% |

## Your lessons from last week
Completion is high at midday (12:00-14:00) with psychological capability and physical opportunity, and in afternoons/evenings; mornings and outdoor-context slots were skipped more often. Heavy days still work, so load is not discriminating. I place standalone tasks in midday windows on weekdays, keep intensity-2 walks at midday, anchor alongside tasks to lunch or routines, and avoid weekends and low-opportunity late evenings.

Use this feedback to place this week's tasks where this person is most likely to follow through, and update your lessons.

# Output path
Write the JSON to: `C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Claude_LinkingtoCalendarBench\docs\test_llm_planner\runs\unemployed_family_caregiver_0000\learning\week_4_plan.json`
