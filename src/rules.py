"""
Temporal rules from calendar-bench's temporal_relation_rules.yaml, used to
check whether a postponed task may be placed in a new time slot (D7).

Only the rule shapes that say "these two must not overlap / must be apart"
are used, because those are the ones a new slot can break:

- LTL     G ¬(A ∧ B)                      A and B never at the same time
- Allen   admissible_relations ⊆ {p, P, m, M}   A and B separated
                                          (gap >= buffer minutes; with
                                          only p/P the gap must be > 0)

A and B are catalog events (e.g. running, office_work) or contexts
(context:tired). Allen rules on `kind: task` (scenario health tasks) and the
other LTL shapes (F, →, weekly_count) are not used here: they describe
co-occurrence or counts over the whole horizon, not a single placement.
"""

import re

_NO_OVERLAP_RE = re.compile(r"^\s*G\s*¬\s*\(\s*(.+?)\s*∧\s*(.+?)\s*\)\s*$")
SEPARATION_RELATIONS = {"p", "P", "m", "M"}


def _operand(text):
    text = text.strip()
    if text.startswith("context:"):
        return {"kind": "context", "name": text[len("context:"):]}
    return {"kind": "event", "name": text}


def _selector(raw):
    """Selector of an Allen rule; None if it is not usable here."""
    if not raw:
        return None
    kind = raw.get("kind", "event")
    if kind == "task":              # scenario health task, not a persona event
        return None
    selector = {"kind": kind}
    if "name" in raw:
        selector["name"] = raw["name"]
    if "intensity" in raw:
        selector["intensity"] = set(raw["intensity"])
    if len(selector) == 1:          # no name and no intensity: cannot match
        return None
    return selector


def parse_rules(temporal_rules):
    """Turn temporal_relation_rules.yaml into a list of separation rules."""
    parsed = []

    for rule in temporal_rules.get("rules") or []:
        match = _NO_OVERLAP_RE.match(rule.get("formula", ""))
        if not match or rule.get("applies_to"):
            continue
        parsed.append({
            "id": rule.get("id"),
            "a": _operand(match.group(1)),
            "b": _operand(match.group(2)),
            "min_gap": 0,
            "touch_ok": True,       # only overlap is forbidden
        })

    for rule in temporal_rules.get("allen_pair_rules") or []:
        relations = set(rule.get("admissible_relations") or [])
        if not relations or not relations <= SEPARATION_RELATIONS:
            continue
        a, b = _selector(rule.get("event_a")), _selector(rule.get("event_b"))
        if a is None or b is None:
            continue
        parsed.append({
            "id": rule.get("id"),
            "a": a,
            "b": b,
            "min_gap": rule.get("buffer") or 0,
            "touch_ok": bool(relations & {"m", "M"}),
        })

    return parsed


def matches(selector, item):
    """Does an executed block or context event match a rule selector?"""
    if selector["kind"] == "context":
        if item.get("kind") != "context":
            return False
    elif item.get("kind") != "task":
        return False
    if "name" in selector and item.get("event") != selector["name"]:
        return False
    if "intensity" in selector and item.get("intensity") not in selector["intensity"]:
        return False
    return True


def _gap_minutes(start_a, end_a, start_b, end_b):
    """Gap between two intervals in minutes; negative if they overlap."""
    if end_a <= start_b:
        return (start_b - end_a).total_seconds() / 60
    if end_b <= start_a:
        return (start_a - end_b).total_seconds() / 60
    return -1


def violated_rules(candidate, start, end, neighbours, rules):
    """
    Ids of the rules a candidate block would break at [start, end).

    neighbours: executed blocks and context events near that time.
    """
    broken = []
    for rule in rules:
        for own, other in ((rule["a"], rule["b"]), (rule["b"], rule["a"])):
            if not matches(own, candidate):
                continue
            for item in neighbours:
                if item is candidate or not matches(other, item):
                    continue
                gap = _gap_minutes(start, end, item["start"], item["end"])
                too_close = gap < rule["min_gap"] or (
                    gap == 0 and not rule["touch_ok"]
                ) or gap < 0
                if too_close:
                    broken.append(rule["id"])
                    break
            else:
                continue
            break
    return broken
