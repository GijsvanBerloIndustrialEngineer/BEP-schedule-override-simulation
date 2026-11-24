# Data copied from calendar-bench

Source: https://github.com/MaaniBeigy/calendar-bench (MIT licence, (c) 2026 Maani Beigy et al.). The repository is only read, never changed.

- `scenario_solutions/human_coach/<person_id>.json`: handcrafted schedules of the `human_coach` scenario for all 30 persons, copied unchanged from `src/experiments/persona/healthy_lifestyle_promotion/human_coach_schedules/` (calendar-bench commit `2c823c2`).
- `health_task_catalog.json`: for every health task in those schedules (99 tasks), its domain, sub-class, level and ontology context links, extracted from `src/assets/ontologies/HealthTasks_2026.05.19.json`.

Recreate or add persons with:

    python v2/tools/import_calendar_bench.py --calendar-bench path/to/calendar-bench [--persons <person_id> ...]

Other planning methods (PTIME, greedy, LLM, MAS, DQN) have no published output in calendar-bench. Comparing planning methods is not done in this repository: the plan is to run the override simulation inside calendar-bench, so each calendar-bench planner gets execution KPIs there.
