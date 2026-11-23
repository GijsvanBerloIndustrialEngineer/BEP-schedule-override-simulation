"""
Override decision model, version 2.

Same multinomial logit as v1 ("no override" is the reference action), with
two new groups of inputs:

    eta_k = beta0_k
          + b_fill_k * fill + b_earlier_k * earlier + b_notified_k * notified   (v1)
          + sum_c  b_ctx_k[c]   * x_c(t)                                         (NEW: context)
          + b_int  * x_tired(t) * (intensity - 1)                                (NEW: tired x intensity)
          + sum_tr b_trait_k[tr] * (trait_tr - centre)                           (NEW: persona)

    p_k = exp(eta_k) / (1 + sum_j exp(eta_j)),   p_none = 1 / (1 + sum_j exp(eta_j))

x_c(t) is 1 when context covariate c is active at decision time t (read from
the [ctx:...] events of the calendar), else 0. beta0_k follows from the base
probabilities as in v1: beta0_k = ln(p_k / p_none).

It also chooses the replacement activity (NEW): a weighted draw over the
`replacements` list, with weights that depend on the active contexts and
on the persona traits.
"""

import copy
import math
import random
from pathlib import Path

import yaml

ACTIONS = ("postpone", "skip", "replace")
NO_OVERRIDE = "none"
BIG_FIVE = ("openness", "conscientiousness", "extraversion", "agreeableness",
            "neuroticism")

V2_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = V2_DIR / "config" / "v2_config.yaml"

# Location context values -> ontology location links that mean the same.
LOCATION_SYNONYMS = {
    "home": {"home", "home_2", "human_dwelling", "household_environment",
             "living_room", "room"},
    "workplace": {"workplace", "workplace_2", "office", "office_building"},
    "public_park": {"public_park", "park", "outdoor", "outdoors",
                    "urban_park"},
}


# ============================================================
# 1. CONFIG
# ============================================================

def deep_merge(base, extra):
    merged = copy.deepcopy(base)
    for key, value in (extra or {}).items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def load_config(path=DEFAULT_CONFIG):
    """Read v2_config.yaml and resolve its relative paths."""
    path = Path(path).resolve()
    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
    base = path.parent
    config["experiment_dir"] = (base / config["experiment_dir"]).resolve()
    if config.get("default_calendar"):
        config["default_calendar"] = (base / config["default_calendar"]).resolve()
    out = config.setdefault("output", {})
    out["dir"] = (base / (out.get("dir") or "../output")).resolve()
    out.setdefault("executed_ics_replications", 1)
    out.setdefault("calendar_bench_json", True)
    hs = config.setdefault("health_scenario", {})
    hs["solutions"] = {
        name: (base / folder).resolve()
        for name, folder in (hs.get("solutions") or {}).items()
    }
    if hs.get("health_task_catalog"):
        hs["health_task_catalog"] = (base / hs["health_task_catalog"]).resolve()
    config.setdefault("triggers", {}).setdefault("rate_per_hour", 0.4)
    config["triggers"].setdefault("task_start", True)
    config.setdefault("replications", {}).setdefault("count", 30)
    config["replications"].setdefault("base_seed", 42)
    config.setdefault("persona", {}).setdefault("trait_source", "mean")
    config["persona"].setdefault("centre", 0.5)
    config["config_path"] = path
    return config


def parameters_for(config, persona_id):
    model = config.get("override_model") or {}
    params = deep_merge(model.get("default") or {}, {})
    source = "default"
    if persona_id and persona_id in (model.get("personas") or {}):
        params = deep_merge(params, model["personas"][persona_id])
        source = f"default + personas.{persona_id}"
    validate_parameters(params)
    return params, source


def validate_parameters(params):
    base = params.get("base_probabilities") or {}
    if any(a not in base for a in ACTIONS):
        raise ValueError("base_probabilities needs postpone, skip and replace")
    if not all(base[a] > 0 for a in ACTIONS) or sum(base[a] for a in ACTIONS) >= 1:
        raise ValueError(
            f"base_probabilities must be > 0 and sum to < 1; got {base}")
    if not 0 <= params.get("notification_share", 0) <= 1:
        raise ValueError("notification_share must be between 0 and 1")


# ============================================================
# 2. PERSONA TRAITS
# ============================================================

def persona_traits(persona, source="mean", rng=None):
    """
    Big Five of a persona from persona_config.yaml.

    mean   : the `loc` of each trait's normal distribution
    sample : one draw from norm(loc, scale), clipped to [min, max]
    Missing traits are returned as None (they then add nothing).
    """
    traits = {}
    chars = (persona or {}).get("characteristics") or {}
    for name in BIG_FIVE:
        spec = chars.get(name) or {}
        p = spec.get("params") or {}
        if "loc" not in p:
            traits[name] = None
            continue
        value = p["loc"]
        if source == "sample":
            rng = rng or random.Random()
            value = rng.gauss(p["loc"], p.get("scale", 0))
            clip = spec.get("clip") or {}
            value = min(max(value, clip.get("min", 0)), clip.get("max", 1))
        traits[name] = value
    return traits


# ============================================================
# 3. CONTEXT AT A MOMENT
# ============================================================

def active_contexts(context_by_day, moment):
    """{(category, value)} of the [ctx:...] episodes active at `moment`."""
    return {
        (c["context_category"], c["event"])
        for c in context_by_day.get(moment.date(), [])
        if c["start"] <= moment < c["end"]
    }


def current_location(contexts):
    for category, value in contexts:
        if category == "location":
            return value
    return None


def _is_outdoor(task, params):
    if task.get("event") in set(params.get("outdoor_events") or []):
        return True
    return task.get("health_subclass") in set(
        params.get("outdoor_health_subclasses") or [])


def location_mismatch(task, contexts, params):
    """1 if the current location is known and does not fit the task."""
    location = current_location(contexts)
    if location is None:
        return 0
    allowed = None
    if task.get("location_links") is not None:            # health task
        links = set(task["location_links"])
        if not links:
            return 0
        allowed = {loc for loc, syn in LOCATION_SYNONYMS.items() if syn & links}
        if _is_outdoor(task, params):
            allowed.add("public_park")
    else:
        fit = (params.get("location_fit") or {}).get(task.get("event"))
        if fit is None:
            return 0
        allowed = set(fit)
    return 0 if location in allowed else 1


def context_covariates(task, contexts, params):
    """{covariate name: 0/1} for one decision."""
    values = {}
    for name, spec in (params.get("context_covariates") or {}).items():
        if spec.get("special") == "location_mismatch":
            values[name] = location_mismatch(task, contexts, params)
            continue
        hit = any((spec["category"], v) in contexts for v in spec.get("values", []))
        if hit and spec.get("only_outdoor_tasks") and not _is_outdoor(task, params):
            hit = False
        values[name] = 1 if hit else 0
    return values


# ============================================================
# 4. MULTINOMIAL LOGIT
# ============================================================

def intercepts(params):
    base = params["base_probabilities"]
    p_none = 1 - sum(base[a] for a in ACTIONS)
    return {a: math.log(base[a] / p_none) for a in ACTIONS}


def action_probabilities(params, fill_hours, earlier_overrides, notified,
                         ctx_values, traits, centre, intensity=1,
                         allowed=ACTIONS):
    """Probabilities of {none, postpone, skip, replace} for one decision."""
    coef = params.get("coefficients") or {}
    ctx_coef = params.get("context_coefficients") or {}
    trait_coef = params.get("trait_coefficients") or {}
    slopes = params.get("intensity_slope") or {}
    cap = params.get("earlier_overrides_cap")
    if cap is not None:
        earlier_overrides = min(earlier_overrides, cap)
    level = max(0, (intensity or 1) - 1)

    beta0 = intercepts(params)
    weights = {NO_OVERRIDE: 1.0}
    parts = {}
    for action in ACTIONS:
        c = coef.get(action) or {}
        state = (c.get("fill", 0) * fill_hours
                 + c.get("earlier_overrides", 0) * earlier_overrides
                 + c.get("notified", 0) * notified)
        context = sum((ctx_coef.get(action) or {}).get(name, 0) * x
                      for name, x in ctx_values.items())
        context += sum(slope * ctx_values.get(name, 0) * level
                       for name, slope in slopes.items())
        persona = sum(b * (traits[t] - centre)
                      for t, b in (trait_coef.get(action) or {}).items()
                      if traits.get(t) is not None)
        eta = beta0[action] + state + context + persona
        parts[action] = {"state": state, "context": context, "persona": persona}
        weights[action] = math.exp(eta) if action in allowed else 0.0
    total = sum(weights.values())
    return {a: w / total for a, w in weights.items()}, parts


def draw_action(probabilities, rng):
    u = rng.random()
    cumulative = 0.0
    for action in (NO_OVERRIDE,) + ACTIONS:
        cumulative += probabilities[action]
        if u < cumulative:
            return action
    return NO_OVERRIDE


# ============================================================
# 5. REPLACEMENT ACTIVITY
# ============================================================

def replacement_weights(params, contexts, traits, centre):
    """Weight per replacement activity given the context and the traits."""
    ctx_map = params.get("replacement_contexts") or {}
    active = {name for name, (cat, val) in ctx_map.items()
              if (cat, val) in contexts}
    weights = {}
    for name, spec in (params.get("replacements") or {}).items():
        w = spec.get("base_weight", 1.0)
        for ctx_name, mult in (spec.get("context_multipliers") or {}).items():
            if ctx_name in active:
                w *= mult
        # trait multiplier m: weight * m ** ((trait - centre) / 0.5), so a
        # trait of 1.0 multiplies by m and a trait of 0.0 divides by m
        for trait, mult in (spec.get("trait_multipliers") or {}).items():
            if traits.get(trait) is not None:
                w *= mult ** ((traits[trait] - centre) / 0.5)
        weights[name] = w
    return weights


def choose_replacement(params, contexts, traits, centre, rng):
    weights = replacement_weights(params, contexts, traits, centre)
    total = sum(weights.values())
    if total <= 0:
        return None, weights
    u = rng.random() * total
    cumulative = 0.0
    for name, w in weights.items():
        cumulative += w
        if u < cumulative:
            return name, weights
    return name, weights
