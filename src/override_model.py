"""
Override decision model (REPORT D3, D4, D5, D6, D9, D10, D15).

When an arrival hits an eligible task, the user picks one of four actions:
no override, postpone, skip or replace. The probabilities come from a
multinomial logit with "no override" as the reference action:

    eta_k = beta0_k + beta_fill_k * fill
                    + beta_overrides_k * earlier_overrides
                    + beta_notified_k * notified          (k = postpone, skip, replace)

    p_k    = exp(eta_k) / (1 + sum_j exp(eta_j))
    p_none = 1        / (1 + sum_j exp(eta_j))

beta0_k is not entered directly. It follows from the base probabilities
(the action probabilities when fill = 0, no earlier overrides and no
notification): beta0_k = ln(p_k / p_none).

The rule-based part (D4) decides which tasks can get an override at all,
caps the number of postponements, and turns a postponement without a free
slot into a skip (see override_simulation.py).
"""

import copy
import math

ACTIONS = ("postpone", "skip", "replace")
NO_OVERRIDE = "none"


# ============================================================
# 1. PARAMETER SETS PER PERSONA (D15)
# ============================================================

def _deep_merge(base, extra):
    merged = copy.deepcopy(base)
    for key, value in (extra or {}).items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def parameters_for(config, persona_id):
    """
    Effective override parameters for a persona: the `default` set in
    override_config.yaml with the persona's own set merged on top.
    """
    model = config.get("override_model") or {}
    params = _deep_merge(model.get("default") or {}, {})
    persona_sets = model.get("personas") or {}
    source = "default"
    if persona_id and persona_id in persona_sets:
        params = _deep_merge(params, persona_sets[persona_id])
        source = f"default + personas.{persona_id}"
    validate_parameters(params)
    return params, source


def validate_parameters(params):
    base = params.get("base_probabilities") or {}
    missing = [a for a in ACTIONS if a not in base]
    if missing:
        raise ValueError(
            f"override_model base_probabilities is missing: {missing}"
        )
    total = sum(base[a] for a in ACTIONS)
    if not all(0 < base[a] for a in ACTIONS) or total >= 1:
        raise ValueError(
            "base_probabilities must be > 0 and sum to less than 1 "
            f"(the rest is 'no override'); got {base}"
        )
    q = params.get("notification_share", 0)
    if not 0 <= q <= 1:
        raise ValueError("notification_share must be between 0 and 1")


# ============================================================
# 2. ELIGIBILITY (D9, rule-based)
# ============================================================

def is_eligible(task, params):
    """
    A task can get an override unless its catalog event, its label or its
    category is on the explicit exclusion lists in override_config.yaml.
    """
    excluded = params.get("excluded") or {}
    if task.get("is_marker"):
        return False
    if task.get("event") in set(excluded.get("events") or []):
        return False
    if task.get("label") in set(excluded.get("labels") or []):
        return False
    if task.get("category") in set(excluded.get("categories") or []):
        return False
    return True


# ============================================================
# 3. MULTINOMIAL LOGIT (D3, D4, D5, D6, D10)
# ============================================================

def intercepts(params):
    base = params["base_probabilities"]
    p_none = 1 - sum(base[a] for a in ACTIONS)
    return {a: math.log(base[a] / p_none) for a in ACTIONS}


def action_probabilities(params, fill_hours, earlier_overrides, notified,
                         allowed=ACTIONS):
    """
    Probabilities of {none, postpone, skip, replace} for one decision.

    fill_hours        : planned hours left in the day (D6)
    earlier_overrides : overrides earlier in the window (D5; capped)
    notified          : 1 if the task has a notification (D10)
    allowed           : actions that are possible; the others get p = 0
                        (e.g. postpone after the postponement cap)
    """
    coef = params.get("coefficients") or {}
    cap = params.get("earlier_overrides_cap")
    if cap is not None:
        earlier_overrides = min(earlier_overrides, cap)

    beta0 = intercepts(params)
    weights = {NO_OVERRIDE: 1.0}
    etas = {}
    for action in ACTIONS:
        c = coef.get(action) or {}
        eta = (
            beta0[action]
            + c.get("fill", 0) * fill_hours
            + c.get("earlier_overrides", 0) * earlier_overrides
            + c.get("notified", 0) * notified
        )
        etas[action] = eta
        weights[action] = math.exp(eta) if action in allowed else 0.0

    total = sum(weights.values())
    return {action: w / total for action, w in weights.items()}, etas


def draw_action(probabilities, rng):
    u = rng.random()
    cumulative = 0.0
    for action in (NO_OVERRIDE,) + ACTIONS:
        cumulative += probabilities[action]
        if u < cumulative:
            return action
    return NO_OVERRIDE
