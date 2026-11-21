# Parameters of version 2 and where their values come from

All values are in [`config/v2_config.yaml`](config/v2_config.yaml). **No parameter is fitted to data.** Every parameter has a status:

| Status | Meaning |
|---|---|
| **CB** | Taken from the calendar-bench experiment configs (no choice by me) |
| **LIT-DIR** | The *sign* (direction) is supported by the literature below; the *size* is an assumption |
| **ASSUMPTION** | Chosen by me; covered by the sensitivity analysis (`src/sensitivity.py`) |
| **[CITE]** | Placeholder: a source still has to be found and added |

> The references below are real publications that support the *direction* of an effect. Before citing them in the report, check the exact numbers and page references against the papers yourself. They do **not** give the coefficient values used here. Where no suitable source is known, the table says **[CITE]**. Never replace a [CITE] with a reference you haven't read.

## 1. Triggers

| Parameter | Value | Status | Source / reasoning | Sensitivity range |
|---|---|---|---|---|
| λ `triggers.rate_per_hour` | 0.4 /h | ASSUMPTION | As v1 (D1). [CITE] for how often people reconsider plans during the day (e.g. experience-sampling studies) | 0.2 – 0.8 |
| `triggers.task_start` | on | ASSUMPTION | New in v2: a decision at the planned start of each eligible task. Without it, short (health) tasks are rarely hit by a Poisson arrival and almost always count as completed. | off / on |

## 2. Base probabilities (reference decision)

| Parameter | Value | Status | Source / reasoning | Range |
|---|---|---|---|---|
| p postpone / skip / replace | 0.12 / 0.08 / 0.05 (p none 0.75) | ASSUMPTION, LIT-DIR for the order of magnitude | The intention–behaviour gap: a large share of people who intend to act do not (Sheeran, 2002; Rhodes & de Bruijn, 2013, about half of the intenders for physical activity). That is over a whole intention, not per decision, so this is only a plausibility check. The split over postpone/skip/replace is [CITE]. | ×0.5 – ×1.5 |

v1 had separate base probabilities per persona. v2 drops them: persona differences now come from the Big Five traits (section 5), so they are not counted twice.

## 3. State coefficients (as v1)

| Parameter | Value (postpone / skip / replace) | Status | Source / reasoning | Range |
|---|---|---|---|---|
| β fill (per planned hour left today) | 0.10 / 0.08 / 0.05 | ASSUMPTION | A fuller day gives more reason to drop or move something. [CITE] (time pressure and plan adherence) | ×0 – ×2 |
| β earlier overrides | −0.40 (all) | ASSUMPTION | v1 decision D5: an override "uses up" the slack of the day. The opposite sign (a "what-the-hell" cascade) is also plausible. [CITE] | ×0 – ×2 |
| β notified | −0.30 / −0.50 / −0.20 | LIT-DIR | Reminders and prompts improve adherence to health behaviours (Fry & Neff, 2009). Planning with if-then cues improves goal attainment (Gollwitzer & Sheeran, 2006). | ×0 – ×2 |
| q `notification_share` | 0.5 | ASSUMPTION | Share of tasks with a reminder; a design choice of the planner, not a person property | 0 – 1 |
| `earlier_overrides_window`, cap | day, 3 | ASSUMPTION | As v1 | – |

## 4. Context coefficients (new)

Context comes from the `[ctx:...]` episodes calendar-bench writes into the `.ics` (**CB**: which contexts exist, and when, per persona). A covariate is 1 when the context is active at the decision moment.

| Covariate | Context values | Sign | Status | Source / reasoning |
|---|---|---|---|---|
| tired | energy_state: tired | + | LIT-DIR | Momentary fatigue and low energy go with less physical activity in daily life (Liao, Shonkoff & Dunton, 2015) |
| tired × (intensity − 1) | | + | LIT-DIR / ASSUMPTION | The same review; the stronger effect for intensive tasks is my assumption. **Note:** for `diligent_anxious_active`, `tired` only occurs at night, so this parameter has no effect on that calendar |
| energetic | energy_state: energetic | − | LIT-DIR | Liao et al. (2015). **Note:** `energetic` is active 4.5–12 h per day for this persona, so its negative coefficient weighs a lot in the net context effect |
| negative_mood | mood_emotion: anxious | + | LIT-DIR | Procrastination as short-term mood repair (Sirois & Pychyl, 2013); negative affect and activity (Liao et al., 2015) |
| positive_mood | happy, calm | − (0 for replace) | LIT-DIR | Liao et al. (2015) |
| stress | stress: stress_episode | + | LIT-DIR | Sirois & Pychyl (2013). [CITE] for stress and health behaviour |
| low_self_efficacy | capability_opportunity: low_self_efficacy | + | LIT-DIR | Self-efficacy is a core predictor of acting on intentions in the HAPA model (calendar-bench's behaviour-state contexts use it). [CITE] Schwarzer's HAPA papers |
| intention_not_to_act | behaviour_state: intention_not_to_enact_a_behaviour | + | LIT-DIR | Intention predicts behaviour (Sheeran, 2002) |
| intention_to_act | intention_to_enact_a_behaviour, action_planning | − | LIT-DIR | Sheeran (2002); Gollwitzer & Sheeran (2006) for action planning |
| bad_weather_outdoor | weather_environment: raining_or_snowing, only for outdoor tasks | + | LIT-DIR | Bad weather goes with less physical activity (Tucker & Gilliland, 2007) |
| location_mismatch | current location does not fit the task | + | ASSUMPTION | The task cannot be done where the person is. Location fit: `location_fit` per catalog event (my assumption) and, for health tasks, the ontology `context_links.location` of calendar-bench (**CB**) |

All sizes (0.1–0.7 on the log-odds scale) are **ASSUMPTION**. The sensitivity analysis scales the whole context block by ×0 – ×2, and the ablation switches it off.

## 5. Persona traits (new)

| Parameter | Value | Status | Source / reasoning |
|---|---|---|---|
| Trait values | persona `loc` (or a sample of norm(loc, scale), clipped) | CB | `persona_config.yaml`; calendar-bench doesn't write the sampled per-person values into the `.ics` |
| centre | 0.5 | ASSUMPTION | Traits enter as (trait − 0.5), so a "middle" person adds nothing |
| β conscientiousness | −2.0 / −2.0 / −1.0 | LIT-DIR | Conscientiousness is strongly and negatively related to procrastination (Steel, 2007); positively to physical activity (Rhodes & Smith, 2006) |
| β neuroticism | +0.8 / +0.6 / +0.3 | LIT-DIR | Positive, weaker relation with procrastination (Steel, 2007); negative with physical activity (Rhodes & Smith, 2006) |
| β openness, extraversion (replace) | +0.5 / +0.5 | ASSUMPTION | More spontaneous switching to another activity. [CITE] |
| β agreeableness | 0 | ASSUMPTION | No direction assumed |

Range in the sensitivity analysis: the whole block ×0 – ×2.

## 6. Replanning (postpone)

| Parameter | Value | Status | Source / reasoning | Range |
|---|---|---|---|---|
| `postpone_window` | rolling, 7 days | ASSUMPTION | Replanning looks at a week instead of a day (v1: same day only). `calendar_week` limits it to the same Mon–Sun week, matching calendar-bench's weekly task batches. | 1 – 14 days |
| `max_postpones_per_task` | 1 | ASSUMPTION | As v1 | – |
| `postpone_respect_weekdays` | false | ASSUMPTION | true: only move to weekdays allowed in `event_config.yaml` | – |
| `check_temporal_rules` | true | CB | Rules from `temporal_relation_rules.yaml` (as v1) | – |

## 7. Replacement activities (new)

Weight of an activity = `base_weight` × the multipliers of the active contexts × `m ** ((trait − 0.5) / 0.5)` per trait multiplier. All base weights, multipliers and `max_minutes` are **ASSUMPTION**. The direction of `screen_time` and `snack` under negative mood or stress follows procrastination as mood repair (Sirois & Pychyl, 2013). The activities map onto calendar-bench catalog events (`napping`, `snacking`, `socialising`, `reading`, `walking`), so the executed calendar can be scored by calendar-bench; `screen_time` is not a catalog event.

## 8. Health scenario

| Parameter | Value | Status |
|---|---|---|
| Task batch (tasks, weeks, duration, intensity, flags) | from the human coach solution of the person | CB |
| Human coach placements | `human_coach_schedules/<person>.json` | CB |
| Domain and sub-class of a task | HealthTasks ontology; keyword fallback for 15 task slugs that aren't in the ontology (see sheet *Task batch*, column *Domain source*) | CB / ASSUMPTION |
| `fcfs_greedy_v2`, `random_slot_v2`, `context_aware_v2` | built into v2 | ASSUMPTION (see README) |

## 9. Method references (sensitivity analysis, output analysis)

- One-at-a-time screening, and Morris elementary effects as the next step: Morris (1991); Saltelli et al. (2008).
- Replications and confidence intervals: Law (2015).

## References

- Fry, J. P., & Neff, R. A. (2009). Periodic prompts and reminders in health promotion and health behavior interventions: Systematic review. *Journal of Medical Internet Research, 11*(2), e16.
- Gollwitzer, P. M., & Sheeran, P. (2006). Implementation intentions and goal achievement: A meta-analysis of effects and processes. *Advances in Experimental Social Psychology, 38*, 69–119.
- Law, A. M. (2015). *Simulation modeling and analysis* (5th ed.). McGraw-Hill.
- Liao, Y., Shonkoff, E. T., & Dunton, G. F. (2015). The acute relationships between affect, physical feeling states, and physical activity in daily life: A review of current evidence. *Frontiers in Psychology, 6*, 1975.
- Morris, M. D. (1991). Factorial sampling plans for preliminary computational experiments. *Technometrics, 33*(2), 161–174.
- Rhodes, R. E., & de Bruijn, G.-J. (2013). How big is the physical activity intention–behaviour gap? A meta-analysis using the action control framework. *British Journal of Health Psychology, 18*(2), 296–309.
- Rhodes, R. E., & Smith, N. E. I. (2006). Personality correlates of physical activity: A review and meta-analysis. *British Journal of Sports Medicine, 40*(12), 958–965.
- Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global sensitivity analysis: The primer*. Wiley.
- Sheeran, P. (2002). Intention–behavior relations: A conceptual and empirical review. *European Review of Social Psychology, 12*(1), 1–36.
- Sirois, F., & Pychyl, T. (2013). Procrastination and the priority of short-term mood regulation: Consequences for future self. *Social and Personality Psychology Compass, 7*(2), 115–127.
- Steel, P. (2007). The nature of procrastination: A meta-analytic and theoretical review of quintessential self-regulatory failure. *Psychological Bulletin, 133*(1), 65–94.
- Tucker, P., & Gilliland, J. (2007). The effect of season and weather on physical activity: A systematic review. *Public Health, 121*(12), 909–922.
- calendar-bench: Beigy, M., et al. https://github.com/MaaniBeigy/calendar-bench (MIT licence); experiment `healthy_lifestyle_promotion`.
