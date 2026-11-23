"""
Decision models of version 3.

Stage 1, REVIEW (new): before the day starts, a multinomial logit over
{keep, move, drop} for every eligible task of the day, with "keep" as the
reference:

    U_a = b0_a + b_load,a * (day_load - centre_load) + b_int,a * (intensity - 1)
               + sum_tr th_a,tr * (trait_tr - centre)        (a = move, drop)

The review knows the load of the day and the task, not the momentary
context at the planned time.

Stage 2, EXECUTION: the version 2 model (model_v2.action_probabilities)
at the planned start, then a PROGRESS draw for a started task:

    logit P(finish) = c0 + sum_c c_c * x_c(t_start) + c_int * (intensity - 1)
                         + sum_tr k_tr * (trait_tr - centre)

with c0 = logit(base_completion).
"""

import math
import sys
from pathlib import Path

import yaml

V3_DIR = Path(__file__).resolve().parent.parent
V2_SRC = V3_DIR.parent / "v2" / "src"
if str(V2_SRC) not in sys.path:
    sys.path.append(str(V2_SRC))

from model_v2 import deep_merge, load_config as load_v2_config  # noqa: E402

DEFAULT_CONFIG = V3_DIR / "config" / "v3_config.yaml"
REVIEW_ACTIONS = ("move", "drop")
KEEP = "keep"


def load_config(path=DEFAULT_CONFIG):
    """v2 config (base_config) with the v3 settings merged on top."""
    path = Path(path).resolve()
    with path.open("r", encoding="utf-8") as f:
        own = yaml.safe_load(f) or {}
    base = (path.parent / own["base_config"]).resolve()
    config = load_v2_config(base)
    config["stages"] = own.get("stages") or {}
    config["triggers"] = deep_merge(config["triggers"], own.get("triggers") or {})
    if (own.get("output") or {}).get("dir"):
        config["output"]["dir"] = (path.parent / own["output"]["dir"]).resolve()
    config["config_path"] = path
    config["base_config_path"] = base
    validate(config)
    return config


def validate(config):
    review = config["stages"].get("review") or {}
    if review.get("enabled"):
        base = review.get("base_probabilities") or {}
        if any(base.get(a, 0) <= 0 for a in REVIEW_ACTIONS) or sum(base.values()) >= 1:
            raise ValueError(f"review.base_probabilities must be > 0 and sum < 1; got {base}")
        if review.get("mode", "same_morning") not in ("same_morning", "evening_before"):
            raise ValueError("review.mode must be same_morning or evening_before")
    progress = config["stages"].get("progress") or {}
    if progress.get("enabled"):
        p = progress.get("base_completion", 0.92)
        if not 0 < p < 1:
            raise ValueError("progress.base_completion must be between 0 and 1")
        lo, hi = progress.get("stop_fraction", [0.25, 0.85])
        if not 0 <= lo <= hi <= 1:
            raise ValueError("progress.stop_fraction must be [lo, hi] within [0, 1]")


def _trait_term(coefs, traits, centre):
    return sum(b * (traits[t] - centre) for t, b in (coefs or {}).items()
               if traits.get(t) is not None)


def review_probabilities(review, day_load, intensity, traits, centre):
    """P(keep), P(move), P(drop) for one task at the review."""
    base = review["base_probabilities"]
    p_keep = 1 - sum(base[a] for a in REVIEW_ACTIONS)
    coef = review.get("coefficients") or {}
    tcoef = review.get("trait_coefficients") or {}
    level = max(0, (intensity or 1) - 1)
    load = day_load - review.get("day_load_centre", 0)
    weights = {KEEP: 1.0}
    for a in REVIEW_ACTIONS:
        c = coef.get(a) or {}
        u = (math.log(base[a] / p_keep)
             + c.get("day_load", 0) * load
             + c.get("intensity", 0) * level
             + _trait_term(tcoef.get(a), traits, centre))
        weights[a] = math.exp(u)
    total = sum(weights.values())
    return {a: w / total for a, w in weights.items()}


def finish_probability(progress, ctx_values, intensity, traits, centre):
    """P(a started task is finished) given the context at its start."""
    p0 = progress.get("base_completion", 0.92)
    coef = progress.get("coefficients") or {}
    level = max(0, (intensity or 1) - 1)
    z = math.log(p0 / (1 - p0))
    z += sum(coef.get(name, 0) * x for name, x in ctx_values.items())
    z += coef.get("intensity", 0) * level
    z += _trait_term(progress.get("trait_coefficients"), traits, centre)
    return 1 / (1 + math.exp(-z))


def draw(probabilities, rng, order):
    u, cum = rng.random(), 0.0
    for a in order:
        cum += probabilities[a]
        if u < cum:
            return a
    return order[0]
