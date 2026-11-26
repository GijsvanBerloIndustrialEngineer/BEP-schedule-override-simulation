"""
Test: an LLM planner with and without a learning model (feedback from the
executed calendar), evaluated with the v2 override simulation.

Workflow (the LLM is called outside this script; every weekly plan is made by
a fresh LLM instance that sees only the prompt file):

    python v2/llm_planner/llm_planner_test.py prompt  --person P --variant static   --week W
    python v2/llm_planner/llm_planner_test.py prompt  --person P --variant learning --week W
        -> docs/test_llm_planner/runs/<P>/<variant>/week_<W>_prompt.md
        the LLM writes          .../week_<W>_plan.json
    python v2/llm_planner/llm_planner_test.py evaluate [--replications 10]
        -> KPIs, charts and tables in docs/test_llm_planner/

Variants:
  static    every week the same kind of prompt: profile, free windows,
            observable context, the week's tasks. No feedback.
  learning  the same, plus a learning model: what happened to every task of
            the previous week in the executed calendar, a memory of
            completion rates (by time of day, weekday/weekend, day load,
            intensity, observable context) over all earlier weeks, and the
            planner's own lessons from the previous week.
Week 1 is shared by both variants (identical prompt, identical plan).

The planner observes the same context categories as calendar-bench's
"context aware" planners (weather, behaviour state, capability/opportunity,
goals, motivation); energy, mood, stress and location stay hidden.
"""

import argparse
import copy
import csv
import hashlib
import json
import statistics
import sys
from datetime import date, datetime, time, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
V2_SRC = REPO / "v2" / "src"
sys.path.insert(0, str(V2_SRC))

from common import load_setup, triggers_of, mean_ci, write_workbook  # noqa: E402
from health_tasks import (  # noqa: E402
    load_catalog, load_solution, task_batch_from_solution, health_block,
    placements_from_solution,
)
from model_v2 import load_config  # noqa: E402
from simulation_v2 import run_replication  # noqa: E402
from sensitivity_population import person_traits, persona_from_traits  # noqa: E402

OUT = REPO / "docs" / "test_llm_planner"
RUNS = OUT / "runs"
POP = REPO / "calendar_bench_population"
PERSONS = ["diligent_anxious_active_0000", "free_spirited_social_student_0000",
           "unemployed_family_caregiver_0000"]
WEEKS = 8
OBSERVED = {"weather_environment", "behaviour_state", "capability_opportunity",
            "goal_intention", "sdt_regulation"}
WAKE, SLEEP, STEP = 6 * 60, 22 * 60, 10
WINDOWS = [("early morning", 0, 390), ("morning", 390, 720), ("afternoon", 720, 1050),
           ("evening", 1050, 1290), ("night", 1290, 1440)]
FEEDBACK_SEED = 42


# ============================================================
# setup per person
# ============================================================

_CACHE = {}


def person_setup(person):
    if person in _CACHE:
        return _CACHE[person]
    config = load_config()
    setup = load_setup(config, POP / "ics" / f"{person}.ics")
    traits = person_traits(POP / "persons" / f"{person}.json")
    persona = persona_from_traits(traits)
    profile = json.loads((POP / "persons" / f"{person}.json").read_text(encoding="utf-8"))["persona"]["characteristics"]
    hs = config["health_scenario"]
    catalog = load_catalog(hs["health_task_catalog"])
    start = setup["horizon"][0].date()
    sol = load_solution(hs["solutions"]["human_coach"], person)
    batch = task_batch_from_solution(sol, catalog, start)
    # tasks the coach left unscheduled have no week and cannot be assigned to one
    batch = [t for t in batch if t["week"] is not None]
    batch.sort(key=lambda t: (t["week"], t["domain"], t["slug"]))
    counters = {}
    for t in batch:
        counters[t["week"]] = counters.get(t["week"], 0) + 1
        t["id"] = f"W{t['week']}T{counters[t['week']]:02d}"
    coach = placements_from_solution(sol, batch, person, setup["persona_id"], "human_coach", start)
    _CACHE[person] = dict(config=config, setup=setup, traits=traits, persona=persona,
                          profile=profile, batch=batch, start=start, coach=coach)
    return _CACHE[person]


def week_days(start, week):
    first = start + timedelta(days=7 * (week - 1))
    return [first + timedelta(days=i) for i in range(7)]


def hm(minutes):
    return f"{int(minutes) // 60:02d}:{int(minutes) % 60:02d}"


def at(day, minutes):
    return datetime.combine(day, time()) + timedelta(minutes=minutes)


# ============================================================
# busy time, free windows, context
# ============================================================

def busy_intervals(setup, day):
    """[start, end) minutes of time-blocking planned events on `day` (incl. sleep)."""
    out = []
    d0 = datetime.combine(day, time())
    for t in setup["tasks"]:
        if t.get("is_marker") or t.get("is_concurrent"):
            continue
        s, e = max(t["start"], d0), min(t["end"], d0 + timedelta(days=1))
        if e > s:
            out.append(((s - d0).total_seconds() / 60, (e - d0).total_seconds() / 60))
    return sorted(out)


def free_windows(busy, lo=WAKE, hi=SLEEP):
    out, cur = [], lo
    for s, e in busy:
        if e <= cur or s >= hi:
            continue
        if s > cur:
            out.append((cur, min(s, hi)))
        cur = max(cur, e)
    if cur < hi:
        out.append((cur, hi))
    return [w for w in out if w[1] - w[0] >= 10]


def day_load_hours(setup, day):
    d0 = datetime.combine(day, time())
    ivs = []
    for t in setup["tasks"]:
        if t.get("is_marker") or t.get("is_concurrent") or t.get("category") == "sleep":
            continue
        s, e = max(t["start"], d0), min(t["end"], d0 + timedelta(days=1))
        if e > s:
            ivs.append((s, e))
    ivs.sort()
    total, cs, ce = 0.0, None, None
    for s, e in ivs:
        if ce is None or s > ce:
            if ce is not None:
                total += (ce - cs).total_seconds()
            cs, ce = s, e
        else:
            ce = max(ce, e)
    if ce is not None:
        total += (ce - cs).total_seconds()
    return total / 3600


def observed_context(setup, day):
    """Observable context episodes between 06:00 and 22:00, touching episodes merged."""
    d0 = datetime.combine(day, time())
    by_value = {}
    for c in setup["context_events"]:
        if c["context_category"] not in OBSERVED:
            continue
        s = max(c["start"], d0 + timedelta(minutes=WAKE))
        e = min(c["end"], d0 + timedelta(minutes=SLEEP))
        if e > s:
            by_value.setdefault(c["context_value"].replace("_", " "), []).append(
                ((s - d0).total_seconds() / 60, (e - d0).total_seconds() / 60))
    out = []
    for v, ivs in by_value.items():
        ivs.sort()
        cs, ce = ivs[0]
        for s, e in ivs[1:]:
            if s <= ce:
                ce = max(ce, e)
            else:
                out.append((cs, ce, v)); cs, ce = s, e
        out.append((cs, ce, v))
    return sorted(out)


def context_at(setup, moment):
    return sorted({c["context_value"].replace("_", " ") for c in setup["context_events"]
                   if c["context_category"] in OBSERVED and c["start"] <= moment < c["end"]})


# ============================================================
# prompts
# ============================================================

SYSTEM = """# Role
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
"""


def profile_text(info):
    p = info["profile"]
    bits = [f"age {p.get('age')}", p.get("gender"), f"occupation: {p.get('occupation_status')}",
            "has children" if p.get("has_kids") else "no children",
            "part-time job" if p.get("has_part_time_job") else None,
            f"aims for about {p.get('weekly_workouts')} workouts a week"]
    return ", ".join(str(b) for b in bits if b)


def calendar_text(info, week):
    setup = info["setup"]
    lines = []
    for day in week_days(info["start"], week):
        fw = free_windows(busy_intervals(setup, day))
        ctx = observed_context(setup, day)
        lines.append(f"### {day:%A %Y-%m-%d} (planned busy time {day_load_hours(setup, day):.1f} h)")
        lines.append("Free windows: " + ", ".join(f"{hm(s)}-{hm(e)}" for s, e in fw))
        lines.append("Observed context: " + ("; ".join(f"{hm(s)}-{hm(e)} {v}" for s, e, v in ctx) or "none"))
        lines.append("")
    return "\n".join(lines)


def tasks_text(info, week):
    rows = ["| id | task | duration | intensity (1-4) | domain | type |", "|---|---|---|---|---|---|"]
    for t in info["batch"]:
        if t["week"] != week:
            continue
        rows.append(f"| {t['id']} | {t['display_name']} | {t['duration_min']} min | {t['intensity']} | "
                    f"{t['domain']} | {'alongside' if t['is_concurrent'] else 'standalone'} |")
    return "\n".join(rows)


def run_dir(person, variant):
    d = RUNS / person / variant
    d.mkdir(parents=True, exist_ok=True)
    return d


def plan_path(person, variant, week):
    v = "shared" if week == 1 else variant
    return run_dir(person, v) / f"week_{week}_plan.json"


def make_prompt(person, variant, week):
    info = person_setup(person)
    days = week_days(info["start"], week)
    parts = [SYSTEM,
             f"# Person\n{profile_text(info)}.\n",
             f"# Calendar of week {week} ({days[0]:%d %b} - {days[-1]:%d %b %Y})\n"
             "Free windows are the times without planned activities between 06:00 and 22:00. "
             "Observed context comes from the person's sensors and check-ins.\n\n" + calendar_text(info, week),
             f"# Health tasks of week {week}\n{tasks_text(info, week)}\n"]
    if variant == "learning" and week > 1:
        parts.append(feedback_text(person, week))
    out_path = plan_path(person, variant, week)
    parts.append(f"# Output path\nWrite the JSON to: `{out_path}`\n")
    prompt = "\n".join(parts)
    p = run_dir(person, "shared" if week == 1 else variant) / f"week_{week}_prompt.md"
    p.write_text(prompt, encoding="utf-8")
    return p, out_path


# ============================================================
# plans: read, validate, repair
# ============================================================

def load_plan(person, variant, week):
    return json.loads(plan_path(person, variant, week).read_text(encoding="utf-8"))


def placed_blocks(person, variant, weeks):
    """Validated health blocks for weeks 1..weeks; returns (blocks, log)."""
    info = person_setup(person)
    setup = info["setup"]
    by_id = {t["id"]: t for t in info["batch"]}
    blocks, log = [], []
    taken = {}       # day -> list of (s, e) of placed standalone tasks
    for w in range(1, weeks + 1):
        plan = load_plan(person, variant, w)
        days = week_days(info["start"], w)
        seen = set()
        for pl in plan.get("placements", []):
            t = by_id.get(pl.get("task"))
            if t is None or t["week"] != w or t["id"] in seen:
                log.append({"week": w, "task": pl.get("task"), "status": "invalid id / duplicate"})
                continue
            seen.add(t["id"])
            dur = t["duration_min"]
            try:
                day = date.fromisoformat(pl["date"])
                hh, mm = (int(x) for x in pl["start"].split(":"))
                s = hh * 60 + mm
            except Exception:
                day, s = None, None
            status = "valid"
            if day not in days or s is None or not ok(setup, taken, day, s, dur, t["is_concurrent"]):
                status = "repaired"
                day, s = repair(setup, taken, days, day, s, dur, t["is_concurrent"])
            if day is None:
                log.append({"week": w, "task": t["id"], "status": "could not be placed"})
                continue
            if not t["is_concurrent"]:
                taken.setdefault(day, []).append((s, s + dur))
            blocks.append(health_block(t, at(day, s), at(day, s + dur), person, setup["persona_id"],
                                       len(blocks), variant))
            log.append({"week": w, "task": t["id"], "status": status, "date": day.isoformat(), "start": hm(s)})
        for t in info["batch"]:
            if t["week"] == w and t["id"] not in seen:
                log.append({"week": w, "task": t["id"], "status": "missing from plan"})
    return blocks, log


def ok(setup, taken, day, s, dur, concurrent):
    if s % STEP or s < WAKE or s + dur > SLEEP:
        return False
    if concurrent:
        return True
    busy = busy_intervals(setup, day) + taken.get(day, [])
    return all(not (bs < s + dur and s < be) for bs, be in busy)


def repair(setup, taken, days, day, s, dur, concurrent):
    """Nearest feasible start: same day first (closest to the requested time), then the week."""
    order = ([day] if day in days else []) + [d for d in days if d != day]
    target = s if s is not None else 12 * 60
    for d in order:
        cands = [m for m in range(WAKE, SLEEP - dur + 1, STEP) if ok(setup, taken, d, m, dur, concurrent)]
        if cands:
            return d, min(cands, key=lambda m: abs(m - target))
    return None, None


# ============================================================
# simulation with health blocks
# ============================================================

def notified_map(uids, q, seed):
    """Notification per task from a hash, so adding tasks does not reshuffle the others."""
    out = {}
    for u in uids:
        h = int(hashlib.sha256(f"{seed}:{u}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
        out[u] = 1 if h < q else 0
    return out


def simulate(person, blocks, seed):
    info = person_setup(person)
    setup, config = info["setup"], info["config"]
    tasks = sorted(setup["tasks"] + blocks, key=lambda t: t["start"])
    notified = notified_map([t["uid"] for t in tasks], setup["params"].get("notification_share", 0), seed)
    return run_replication(tasks, setup["context_events"], setup["experiment"], setup["params"],
                           setup["rules"], setup["horizon"], triggers_of(config), seed,
                           info["persona"], config["persona"], notified_override=notified)


def health_outcomes(res, blocks):
    """Outcome label per health block."""
    repl = {}
    for c in res["changes"]:
        if c["action"] == "replace":
            repl[c["task_uid"]] = (c.get("replacement") or "another activity").replace("_", " ")
    by_uid = {o["uid"]: o for o in res["outcomes"]}
    out = {}
    for b in blocks:
        o = by_uid[b["uid"]]
        acts = o["actions"]
        if o["completed"]:
            lab = "postponed, done later" if "postpone" in acts else "done"
        elif "replace" in acts:
            lab = f"replaced by {repl.get(b['uid'], 'another activity')}"
        elif "skip" in acts:
            lab = "skipped"
        elif "postpone" in acts:
            lab = "postponed, not done"
        elif o["executed_hours"] > 0:
            lab = "partly done"
        else:
            lab = "not done"
        out[b["uid"]] = (lab, o["completed"])
    return out


# ============================================================
# learning model: feedback text
# ============================================================

def window_of(minutes):
    for name, lo, hi in WINDOWS:
        if lo <= minutes < hi:
            return name
    return "night"


def feedback_text(person, week):
    """Feedback from the executed calendar of weeks 1..week-1 (one realised run)."""
    info = person_setup(person)
    setup = info["setup"]
    blocks, _ = placed_blocks(person, "learning", week - 1)
    res = simulate(person, blocks, FEEDBACK_SEED)
    outc = health_outcomes(res, blocks)
    by_task = {t["display_name"]: t for t in info["batch"]}
    rows, stats = [], {}

    def add(key, val, done):
        a = stats.setdefault(key, {}).setdefault(val, [0, 0])
        a[0] += done
        a[1] += 1

    for b in blocks:
        lab, done = outc[b["uid"]]
        d = b["start"].date()
        m = b["start"].hour * 60 + b["start"].minute
        load = day_load_hours(setup, d)
        ctx = context_at(setup, b["start"])
        add("time of day", window_of(m), done)
        add("day type", "weekend" if d.weekday() >= 5 else "weekday", done)
        add("day load", "light (<6 h)" if load < 6 else "medium (6-9 h)" if load <= 9 else "heavy (>9 h)", done)
        add("intensity", f"intensity {b['intensity']}", done)
        for c in ctx:
            add("observed context at the planned time", c, done)
        if b["health_week"] == week - 1:
            rows.append(f"| {b['label']} | {b['start']:%a %d %b %H:%M} | {load:.1f} h | "
                        f"{', '.join(ctx) or '-'} | {lab} |")
    prev = load_plan(person, "learning", week - 1).get("lessons", "")
    lines = [f"# Learning model: feedback from the executed calendar",
             f"## What happened to your plan of week {week - 1}",
             "| task | planned at | busy time that day | observed context then | outcome |",
             "|---|---|---|---|---|", *rows, "",
             f"## Memory: completion rate of your placements so far (weeks 1-{week - 1})",
             "| factor | value | done / placed | rate |", "|---|---|---|---|"]
    for key in ("time of day", "day type", "day load", "intensity", "observed context at the planned time"):
        for val, (dn, n) in sorted(stats.get(key, {}).items(), key=lambda kv: -kv[1][1]):
            if n >= 2:
                lines.append(f"| {key} | {val} | {dn} / {n} | {100 * dn / n:.0f}% |")
    lines += ["", "## Your lessons from last week", prev or "(none)", "",
              "Use this feedback to place this week's tasks where this person is most likely to "
              "follow through, and update your lessons.", ""]
    return "\n".join(lines)


# ============================================================
# evaluation
# ============================================================

def evaluate(reps, seed0=42, out=None):
    out = Path(out) if out else globals()["OUT"]
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "Calibri", "font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False})
    variants = ["human_coach", "static", "learning"]
    lab = {"human_coach": "Human coach (reference)", "static": "LLM without learning model",
           "learning": "LLM with learning model"}
    col = {"human_coach": "#AEB9BF", "static": "#E39B1B", "learning": "#1F7A80"}
    seeds = [seed0 + r for r in range(reps)]
    rows, weekly, logs, outcome_mix, all_reps = [], {}, [], {}, {}
    for person in PERSONS:
        info = person_setup(person)
        for v in variants:
            if v == "human_coach":
                blocks, log = info["coach"], []
            else:
                blocks, log = placed_blocks(person, v, WEEKS)
            logs += [dict(person=person, variant=v, **l) for l in log]
            group = {b["uid"]: (b["health_slug"], b["health_week"]) for b in blocks}
            per_rep = []
            for seed in seeds:
                res = simulate(person, blocks, seed)
                outc = health_outcomes(res, blocks)
                per_task = {}
                for b in blocks:
                    per_task.setdefault(group[b["uid"]], []).append(outc[b["uid"]])
                done = {k: all(d for _, d in v_) for k, v_ in per_task.items()}
                n = len(info["batch"])
                labels = [lab_.split(" by ")[0] for k, v_ in per_task.items() for lab_, _ in v_[:1]]
                for l in labels:
                    outcome_mix.setdefault((person, v), {}).setdefault(l, 0)
                    outcome_mix[(person, v)][l] += 1 / reps
                elig = [o for o in res["outcomes"] if o["eligible"] and o["uid"] not in group]
                k = {"Health completion (all tasks)": sum(done.values()) / n,
                     "Base calendar completion": sum(o["completed"] for o in elig) / len(elig),
                     "Plan-execution deviation (h)": sum(o["deviation_hours"] for o in res["outcomes"])}
                for w in range(1, WEEKS + 1):
                    wk = [d for (s_, ww), d in done.items() if ww == w]
                    nw = sum(1 for t in info["batch"] if t["week"] == w)
                    k[f"week {w}"] = sum(wk) / nw if nw else None
                later = [d for (s_, ww), d in done.items() if ww >= 2]
                k["Health completion (weeks 2-8)"] = sum(later) / sum(1 for t in info["batch"] if t["week"] >= 2)
                per_rep.append(k)
            all_reps[(person, v)] = per_rep
            summary = {key: mean_ci([r[key] for r in per_rep]) for key in per_rep[0]}
            placed = [l for l in log]
            summary["Placements valid"] = (sum(l["status"] == "valid" for l in placed) / len(placed), None, None) if placed else (None, None, None)
            rows.append((person, v, summary))
            weekly[(person, v)] = [summary[f"week {w}"][0] for w in range(1, WEEKS + 1)]
            print(f"  {person:34s} {v:12s} health completion {summary['Health completion (all tasks)'][0]:.3f}")
    OUT = out
    OUT.mkdir(parents=True, exist_ok=True)
    # paired differences (same seeds = common random numbers)
    pkeys = ["Health completion (all tasks)", "Health completion (weeks 2-8)", "Base calendar completion",
             "Plan-execution deviation (h)"]
    with (OUT / "paired_differences.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["person", "comparison", "kpi", "mean_diff", "ci_low", "ci_high", "reps_better"])
        for person in PERSONS + ["mean of 3 persons"]:
            for a_, b_ in (("learning", "static"), ("static", "human_coach"), ("learning", "human_coach")):
                for k in pkeys:
                    if person.startswith("mean"):
                        diffs = [statistics.mean(all_reps[(p, a_)][i][k] - all_reps[(p, b_)][i][k] for p in PERSONS)
                                 for i in range(reps)]
                    else:
                        diffs = [ra[k] - rb[k] for ra, rb in zip(all_reps[(person, a_)], all_reps[(person, b_)])]
                    m, lo, hi = mean_ci(diffs)
                    better = sum((d < 0) if "deviation" in k else (d > 0) for d in diffs)
                    w.writerow([person, f"{a_} - {b_}", k, m, lo, hi, f"{better}/{reps}"])
    keys = ["Health completion (all tasks)", "Health completion (weeks 2-8)", "Base calendar completion", "Plan-execution deviation (h)",
            "Placements valid"] + [f"week {w}" for w in range(1, WEEKS + 1)]
    with (OUT / "kpis.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["person", "variant", "kpi", "mean", "ci_low", "ci_high"])
        for person, v, s in rows:
            for k in keys:
                w.writerow([person, v, k, *s[k]])
    write_workbook(OUT / "kpis.xlsx", [
        ("KPIs", ["Person", "Variant"] + keys, [[p, v] + [s[k][0] for k in keys] for p, v, s in rows]),
        ("Placement log", ["Person", "Variant", "Week", "Task", "Status", "Date", "Start"],
         [[l["person"], l["variant"], l["week"], l["task"], l["status"], l.get("date"), l.get("start")] for l in logs]),
    ])
    # learning curve
    fig, axs = plt.subplots(1, 4, figsize=(15, 3.6), sharey=True)
    for ax, person in zip(axs, PERSONS + ["mean"]):
        for v in variants:
            ys = ([statistics.mean(weekly[(p, v)][i] for p in PERSONS) for i in range(WEEKS)] if person == "mean"
                  else weekly[(person, v)])
            ax.plot(range(1, WEEKS + 1), [100 * y for y in ys], marker="o", color=col[v], label=lab[v], lw=2)
        ax.set_title("Mean of 3 persons" if person == "mean" else person.replace("_0000", "").replace("_", " "), fontsize=10)
        ax.set_xlabel("Week"); ax.set_xticks(range(1, WEEKS + 1))
    axs[0].set_ylabel("Health tasks completed (%)")
    axs[0].legend(frameon=False, fontsize=8.5, loc="lower left")
    fig.suptitle(f"Learning curve: health-task completion per week (mean of {reps} replications)", fontsize=11)
    fig.tight_layout(); fig.savefig(OUT / "fig1_learning_curve.png", dpi=200, bbox_inches="tight"); plt.close(fig)
    # KPI bars
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.6))
    for ax, k, scale, unit in [(axs[0], "Health completion (all tasks)", 100, "%"),
                               (axs[1], "Base calendar completion", 100, "%"),
                               (axs[2], "Plan-execution deviation (h)", 1, " h")]:
        x = range(len(PERSONS))
        for i, v in enumerate(variants):
            vals = [next(s for p, vv, s in rows if p == person and vv == v)[k] for person in PERSONS]
            ax.bar([xi + (i - 1) * 0.27 for xi in x], [scale * m for m, _, _ in vals], 0.25, color=col[v], label=lab[v],
                   yerr=[[scale * (m - lo) for m, lo, _ in vals], [scale * (hi - m) for m, _, hi in vals]], capsize=2)
        ax.set_xticks(list(x)); ax.set_xticklabels([p.replace("_0000", "").replace("_", "\n") for p in PERSONS], fontsize=8.5)
        ax.set_title(k + (" (%)" if unit == "%" else ""), fontsize=10)
        if unit == "%":
            ax.set_ylim(50, 100)
    axs[0].legend(frameon=False, fontsize=8, loc="lower left")
    fig.tight_layout(); fig.savefig(OUT / "fig2_kpis.png", dpi=200, bbox_inches="tight"); plt.close(fig)
    # outcome mix
    cats = ["done", "postponed, done later", "partly done", "postponed, not done", "skipped", "replaced", "not done"]
    ccol = ["#1F7A80", "#9FC3C7", "#CFE3E5", "#F0C98A", "#C8382E", "#1A1A1A", "#AEB9BF"]
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ylabels = []
    for i, (person, v) in enumerate([(p, v) for p in PERSONS for v in variants]):
        mix = outcome_mix.get((person, v), {})
        tot = sum(mix.values()) or 1
        left = 0
        for c, cc in zip(cats, ccol):
            share = mix.get(c, 0) / tot
            ax.barh(i, share, left=left, color=cc, label=c if i == 0 else None, height=0.7)
            left += share
        ylabels.append(f"{person.split('_')[0]} - {lab[v]}")
    ax.set_yticks(range(len(ylabels))); ax.set_yticklabels(ylabels, fontsize=8)
    ax.invert_yaxis(); ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1))
    ax.legend(ncol=4, frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.45, -0.1))
    ax.set_title("Outcome of the health tasks (first piece per task)", fontsize=11)
    fig.savefig(OUT / "fig3_outcomes.png", dpi=200, bbox_inches="tight"); plt.close(fig)
    print(f"written to {OUT}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    pp = sub.add_parser("prompt")
    pp.add_argument("--person", required=True)
    pp.add_argument("--variant", choices=["static", "learning"], required=True)
    pp.add_argument("--week", type=int, required=True)
    pe = sub.add_parser("evaluate")
    pe.add_argument("--replications", type=int, default=10)
    pe.add_argument("--seed0", type=int, default=42)
    pe.add_argument("--out", default=None)
    pc = sub.add_parser("check")
    pc.add_argument("--person", required=True)
    pc.add_argument("--variant", required=True)
    pc.add_argument("--week", type=int, required=True)
    a = ap.parse_args(argv)
    if a.cmd == "prompt":
        p, out = make_prompt(a.person, a.variant, a.week)
        print(f"prompt: {p}\nplan:   {out}")
    elif a.cmd == "check":
        _, log = placed_blocks(a.person, a.variant, a.week)
        wk = [l for l in log if l["week"] == a.week]
        from collections import Counter
        print(a.person, a.variant, a.week, dict(Counter(l["status"] for l in wk)))
    else:
        evaluate(a.replications, a.seed0, a.out)


if __name__ == "__main__":
    main()
