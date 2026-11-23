# Data copied from calendar-bench

Source: https://github.com/MaaniBeigy/calendar-bench (MIT licence, (c) 2026 Maani Beigy et al.). The repository is only read, never changed.

- `scenario_solutions/human_coach/<person_id>.json`: handcrafted schedules of the `human_coach` scenario, copied unchanged from `src/experiments/persona/healthy_lifestyle_promotion/human_coach_schedules/`.
- `health_task_catalog.json`: for every health task in those schedules, its domain, sub-class, level and ontology context links, extracted from `src/assets/ontologies/HealthTasks_2026.05.19.json`.

Recreate or add persons with:

    python v2/tools/import_calendar_bench.py --calendar-bench path/to/calendar-bench [--persons <person_id> ...]

Other planning methods (PTIME, greedy, LLM, MAS, DQN) have no published output in calendar-bench. When you have their solution files (`augmented/persons/<person_id>.json` of a calendar-bench run), put each method in its own folder here and add it under `health_scenario.solutions` in `config/v2_config.yaml`, or pass `--solutions name=folder`.
