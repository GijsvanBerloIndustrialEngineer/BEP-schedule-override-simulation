"""
Link between the override simulation and the calendar-bench experiment configs.

calendar-bench describes an experiment with YAML files (see
calendar_bench_configs/CONFIG.md). The planned calendars (.ics) that the
override simulation reads are generated from such an experiment. This module
loads the parts of that experiment the simulation needs:

- environment.yaml : horizon (start date, weeks), time windows, daily window
- event_config.yaml: catalog of events with category and flexibility flags
- persona_config.yaml: persona templates and their characteristics

and the simulation's own settings from override_config.yaml.
"""

import re
from datetime import datetime, date, timedelta
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OVERRIDE_CONFIG = REPO_ROOT / "config" / "override_config.yaml"


# ============================================================
# 1. LOADING THE CONFIG FILES
# ============================================================

def _read_yaml(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found:\n{path}")
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def load_override_config(path=DEFAULT_OVERRIDE_CONFIG):
    """
    Load the override simulation's own settings.

    Relative paths in the file (experiment_dir) are resolved against the
    folder that holds override_config.yaml.
    """
    path = Path(path).resolve()
    config = _read_yaml(path)

    experiment_dir = config.get("experiment_dir")
    if not experiment_dir:
        raise ValueError(f"'experiment_dir' is missing in {path}")
    config["experiment_dir"] = (path.parent / experiment_dir).resolve()

    config.setdefault("horizon_source", "experiment")
    arrivals = config.setdefault("arrivals", {})
    arrivals.setdefault("rate_per_hour", 0.4)
    arrivals.setdefault("seed", 42)

    config["config_path"] = path
    return config


def load_experiment(experiment_dir):
    """Load environment, event catalog and personas of one experiment."""
    experiment_dir = Path(experiment_dir)
    environment = _read_yaml(experiment_dir / "environment.yaml")
    event_config = _read_yaml(experiment_dir / "event_config.yaml")
    persona_config = _read_yaml(experiment_dir / "persona_config.yaml")

    return {
        "dir": experiment_dir,
        "name": environment.get("experiment_name") or experiment_dir.name,
        "environment": environment,
        "horizon": get_horizon(environment),
        "time_windows": environment.get("time_windows", {}),
        "daily_window": environment.get("daily_window", {}),
        "event_catalog": build_event_catalog(event_config),
        "personas": {
            persona["id"]: persona
            for persona in persona_config.get("personas", [])
        },
    }


# ============================================================
# 2. ENVIRONMENT: HORIZON AND TIME WINDOWS
# ============================================================

def get_horizon(environment):
    """
    Simulation horizon from environment.yaml.

    calendar-bench plans `weeks` full weeks starting on `start_date`
    (a Monday) at 00:00. Returns (start, end) as datetimes.
    """
    horizon = environment.get("horizon", {})
    start_date = horizon.get("start_date")
    weeks = horizon.get("weeks")
    if start_date is None or weeks is None:
        return None, None

    if isinstance(start_date, str):
        start_date = date.fromisoformat(start_date)

    start = datetime.combine(start_date, datetime.min.time())
    end = start + timedelta(weeks=int(weeks))
    return start, end


def minutes_since_midnight(moment):
    return moment.hour * 60 + moment.minute + moment.second / 60


def time_window_of(moment, time_windows):
    """Name of the time window (morning, evening, ...) a moment falls in."""
    minute = minutes_since_midnight(moment)
    for name, (start, end) in time_windows.items():
        if start <= minute < end:
            return name
    return None


def in_daily_window(moment, daily_window):
    """True if a moment lies inside the waking window of environment.yaml."""
    wake = daily_window.get("wake_minutes")
    sleep = daily_window.get("sleep_minutes")
    if wake is None or sleep is None:
        return None
    return wake <= minutes_since_midnight(moment) < sleep


# ============================================================
# 3. EVENT CATALOG
# ============================================================

def build_event_catalog(event_config):
    """
    Flatten event_config.yaml into {event name: properties}.

    Task labels from `calendar_variations.task_labels` are not separate
    catalog entries; the .ics file names them in its DESCRIPTION, see
    parse_generated_event().
    """
    catalog = {}
    for category, category_body in (event_config.get("categories") or {}).items():
        for name, body in ((category_body or {}).get("events") or {}).items():
            body = body or {}
            catalog[name] = {
                "category": category,
                "is_concurrent": body.get("is_concurrent"),
                "is_dividable": body.get("is_dividable"),
                "intensity": body.get("intensity"),
                "weekdays": body.get("weekdays"),
                "per_event_duration": body.get("per_event_duration"),
            }
    return catalog


# ============================================================
# 4. MATCHING .ICS EVENTS TO THE EXPERIMENT
# ============================================================

# calendar-bench writes planned events as
#   SUMMARY:     "<label> (Person <person_id>)"
#   DESCRIPTION: "Generated event for <label> (<catalog event>), duration .."
#            or  "Generated event for <catalog event>, duration .."
#            or  "Generated event for wake_up (was sleep end)"
# and context annotations as
#   SUMMARY:     "[ctx:<category>] <value>"   with CATEGORIES:<category>

_PERSON_RE = re.compile(r"\(Person ([^)]+)\)\s*$")
_GENERATED_RE = re.compile(r"^Generated event for (.+?)(?:,|$)")
_PAREN_RE = re.compile(r"^(.*?)\s*\(([^()]+)\)$")
_CONTEXT_RE = re.compile(r"^\[ctx:([^\]]+)\]\s*(.*)$")

# Markers calendar-bench derives from the sleep episode.
SLEEP_MARKERS = {"wake_up": "sleep", "go_to_bed": "sleep"}


def parse_context_event(summary, categories=None):
    """Return (context category, value) for a [ctx:...] event, else None."""
    match = _CONTEXT_RE.match(summary)
    if match:
        return match.group(1), match.group(2)
    if categories:
        return categories, summary
    return None


def parse_generated_event(summary, description):
    """
    Split a planned calendar-bench event into its parts.

    Returns a dict with person_id, label (what the calendar shows) and
    event (the name in event_config.yaml).
    """
    person_match = _PERSON_RE.search(summary)
    person_id = person_match.group(1).strip() if person_match else None
    label = _PERSON_RE.sub("", summary).strip()
    event = label

    generated = _GENERATED_RE.match(description.replace("\\,", ","))
    if generated:
        text = generated.group(1).strip()
        paren = _PAREN_RE.match(text)
        if paren and not paren.group(2).startswith("was "):
            label, event = paren.group(1).strip(), paren.group(2).strip()
        else:
            event = paren.group(1).strip() if paren else text

    return {"person_id": person_id, "label": label, "event": event}


def persona_of(person_id, personas):
    """
    Persona id for a person id such as 'diligent_anxious_active_0000'.

    calendar-bench names persons <persona id>_<instance number>.
    """
    if not person_id:
        return None
    base = re.sub(r"_\d+$", "", person_id)
    return base if base in personas else None


def enrich_task(task, experiment):
    """Add catalog and persona information from the experiment to a task."""
    parsed = parse_generated_event(task["summary"], task.get("description", ""))
    catalog_name = SLEEP_MARKERS.get(parsed["event"], parsed["event"])
    entry = experiment["event_catalog"].get(catalog_name)

    task.update({
        "person_id": parsed["person_id"],
        "persona": persona_of(parsed["person_id"], experiment["personas"]),
        "label": parsed["label"],
        "event": parsed["event"],
        "in_catalog": entry is not None,
        "is_marker": parsed["event"] in SLEEP_MARKERS,
        "category": entry["category"] if entry else None,
        "is_concurrent": entry["is_concurrent"] if entry else None,
        "is_dividable": entry["is_dividable"] if entry else None,
        "intensity": entry["intensity"] if entry else None,
        "time_window": (
            time_window_of(task["start"], experiment["time_windows"])
            if task["start"] else None
        ),
    })
    return task


def persona_characteristics(persona):
    """
    Rows (characteristic, type, parameters) for a persona from
    persona_config.yaml. These are distributions, not the values sampled
    for one person: calendar-bench does not write those into the .ics.
    """
    rows = []
    for name, spec in (persona.get("characteristics") or {}).items():
        spec = spec or {}
        kind = spec.get("type")
        details = {k: v for k, v in spec.items() if k != "type"}
        rows.append((name, kind, str(details)))
    return rows
