"""Charts and summary tables for sensitivity_population.py."""

import statistics
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import write_workbook

KPI_C = "Completion rate (eligible tasks)"
KPI_D = "Plan-execution deviation (hours)"
PERSONAS = ["diligent_anxious_active", "free_spirited_social_student", "unemployed_family_caregiver"]
SHORT = {"diligent_anxious_active": "Diligent, anxious, active",
         "free_spirited_social_student": "Free-spirited social student",
         "unemployed_family_caregiver": "Unemployed family caregiver"}
COL = {"diligent_anxious_active": "#1F7A80", "free_spirited_social_student": "#E39B1B",
       "unemployed_family_caregiver": "#8E6BBF"}
LABEL = {
    "task-start trigger (off/on)": "Decision at task start (off / on)",
    "base probabilities (x factor)": "Base probabilities (×0.5 / ×1.5)",
    "beta earlier overrides (x factor)": "β earlier overrides (×0 / ×2)",
    "beta fill (x factor)": "β fill (×0 / ×2)",
    "beta persona traits (x factor)": "β persona traits (×0 / ×2)",
    "replanning window (days)": "Replanning window (1 / 14 days)",
    "lambda (arrivals per hour)": "λ arrivals per hour (0.2 / 0.8)",
    "q notification share": "q notification share (0 / 1)",
    "beta notified (x factor)": "β notified (×0 / ×2)",
    "beta context (x factor)": "β context (×0 / ×2)",
    "beta tired x intensity": "β tired × intensity (0 / 0.3)",
}
ABL = ["v1 inputs only (no context, no persona)", "+ context", "+ persona", "+ context + persona (v2)"]
ABL_SHORT = {ABL[0]: "v1 inputs", ABL[1]: "+ context", ABL[2]: "+ persona", ABL[3]: "+ context\n+ persona"}

plt.rcParams.update({"font.family": "Calibri", "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": "#B9C6CA",
                     "xtick.color": "#5F6F75", "ytick.color": "#1D2B30"})


def _mean(v):
    v = [x for x in v if x is not None]
    return statistics.mean(v) if v else None


def _sd(v):
    v = [x for x in v if x is not None]
    return statistics.stdev(v) if len(v) > 1 else 0.0


def _save(fig, path):
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def make_report(rows, out, reps):
    out = Path(out)
    base = {r["person"]: r for r in rows if r["analysis"] == "base"}
    persons = sorted(base)
    persona_of = {p: base[p]["persona"] for p in persons}
    oat = {}
    for r in rows:
        if r["analysis"] == "oat":
            oat.setdefault(r["parameter"], {}).setdefault(r["person"], {})[r["level"]] = r
    abl = {}
    for r in rows:
        if r["analysis"] == "ablation":
            abl.setdefault(r["parameter"], {})[r["person"]] = r
    params = list(oat)

    # per person: change vs base (percentage points) and swing
    delta = {p: {} for p in params}          # param -> person -> (low_pp, high_pp)
    for p in params:
        for person in persons:
            b = base[person][KPI_C]
            lo, hi = oat[p][person]["low"][KPI_C], oat[p][person]["high"][KPI_C]
            delta[p][person] = (100 * (lo - b), 100 * (hi - b))
    swing = {p: {person: abs(h - l) for person, (l, h) in delta[p].items()} for p in params}
    order = sorted(params, key=lambda p: _mean(swing[p].values()))

    # ---------------------------------------------------------------- fig 1
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.6))
    for ax, kpi, fmt, lab in [(axs[0], KPI_C, 100, "Completion rate of eligible tasks (%)"),
                              (axs[1], KPI_D, 1, "Plan–execution deviation (hours, 8 weeks)")]:
        for i, ps in enumerate(PERSONAS):
            v = [base[p][kpi] * fmt for p in persons if persona_of[p] == ps]
            ax.scatter([i + (k - 4.5) * 0.04 for k in range(len(v))], v, color=COL[ps], s=28, zorder=3)
            ax.hlines(_mean(v), i - 0.3, i + 0.3, color="#1D2B30", lw=2, zorder=4)
            ax.text(i + 0.33, _mean(v), f"{_mean(v):.1f}", va="center", fontsize=9)
        ax.set_xticks(range(3)); ax.set_xticklabels([SHORT[p].replace(", ", ",\n").replace(" social", "\nsocial").replace(" family", "\nfamily") for p in PERSONAS], fontsize=9)
        ax.set_ylabel(lab); ax.set_xlim(-0.6, 2.8)
    fig.suptitle(f"Base setting per person (mean of {reps} replications; bar = persona mean)", fontsize=11)
    fig.tight_layout()
    _save(fig, out / "fig1_base_per_person.png")

    # ---------------------------------------------------------------- fig 2
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    for i, p in enumerate(order):
        lo = [d[0] for d in delta[p].values()]
        hi = [d[1] for d in delta[p].values()]
        ax.barh(i, _mean(lo), color="#2A6F97", height=0.6, xerr=_sd(lo), ecolor="#5F6F75", capsize=2,
                label="low value" if i == 0 else None)
        ax.barh(i, _mean(hi), color="#E07A5F", height=0.6, xerr=_sd(hi), ecolor="#5F6F75", capsize=2,
                label="high value" if i == 0 else None)
    ax.set_yticks(range(len(order))); ax.set_yticklabels([LABEL.get(p, p) for p in order], fontsize=9)
    ax.axvline(0, color="#1D2B30", lw=0.8)
    ax.set_xlabel("Change in completion rate vs. base (percentage points); mean over 30 persons, error bar = SD")
    ax.legend(frameon=False, loc="lower right")
    ax.set_title("One-at-a-time sensitivity over the whole population", fontsize=11)
    _save(fig, out / "fig2_tornado_population.png")

    # ---------------------------------------------------------------- fig 3
    mat = [[_mean([swing[p][x] for x in persons if persona_of[x] == ps]) for ps in PERSONAS] for p in reversed(order)]
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    im = ax.imshow(mat, cmap="YlOrBr", aspect="auto")
    ax.set_xticks(range(3)); ax.set_xticklabels([SHORT[p].replace(", ", ",\n").replace(" social", "\nsocial").replace(" family", "\nfamily") for p in PERSONAS], fontsize=9)
    ax.set_yticks(range(len(order))); ax.set_yticklabels([LABEL.get(p, p) for p in reversed(order)], fontsize=9)
    vmax = max(max(r) for r in mat)
    for i, r in enumerate(mat):
        for j, v in enumerate(r):
            ax.text(j, i, f"{v:.1f}", ha="center", va="center", fontsize=9,
                    color="white" if v > 0.6 * vmax else "#1D2B30")
    cb = fig.colorbar(im, ax=ax, fraction=0.04); cb.set_label("Swing |high − low| (pp)")
    ax.set_title("Swing in completion rate per persona (mean of 10 persons)", fontsize=11)
    ax.spines[:].set_visible(False)
    _save(fig, out / "fig3_swing_per_persona.png")

    # ---------------------------------------------------------------- fig 4
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.8))
    for ax, kpi, scale, lab in [(axs[0], KPI_C, 100, "Completion change vs. v1 inputs (pp)"),
                                (axs[1], KPI_D, 1, "Deviation change vs. v1 inputs (hours)")]:
        width = 0.25
        for j, a in enumerate(ABL[1:]):
            for i, ps in enumerate(PERSONAS):
                v = [scale * (abl[a][p][kpi] - abl[ABL[0]][p][kpi]) for p in persons if persona_of[p] == ps]
                x = j + (i - 1) * width
                ax.bar(x, _mean(v), width * 0.9, color=COL[ps], label=SHORT[ps] if j == 0 else None)
                ax.scatter([x] * len(v), v, color="#1D2B30", s=6, zorder=3)
        ax.axhline(0, color="#1D2B30", lw=0.8)
        ax.set_xticks(range(3)); ax.set_xticklabels(["+ context", "+ persona", "+ context + persona"])
        ax.set_ylabel(lab)
    axs[0].legend(frameon=False, fontsize=8.5, loc="upper left")
    fig.suptitle("Effect of the context and persona inputs per persona (bars = persona mean, dots = persons)", fontsize=11)
    fig.tight_layout()
    _save(fig, out / "fig4_ablation_per_persona.png")

    # ---------------------------------------------------------------- fig 5
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.6))
    for ax, trait in [(axs[0], "conscientiousness"), (axs[1], "neuroticism")]:
        for ps in PERSONAS:
            sel = [p for p in persons if persona_of[p] == ps]
            ax.scatter([base[p][trait] for p in sel], [100 * base[p][KPI_C] for p in sel],
                       color=COL[ps], s=30, label=SHORT[ps])
        xs = [base[p][trait] for p in persons]; ys = [100 * base[p][KPI_C] for p in persons]
        r = statistics.correlation(xs, ys)
        ax.set_xlabel(f"{trait.capitalize()} (sampled value of the person)")
        ax.set_ylabel("Completion rate (%)")
        ax.set_title(f"r = {r:.2f} over 30 persons", fontsize=10)
    axs[0].legend(frameon=False, fontsize=8.5)
    fig.suptitle("Completion rate against the person's own traits (base setting)", fontsize=11)
    fig.tight_layout()
    _save(fig, out / "fig5_traits_vs_completion.png")

    # ---------------------------------------------------------------- tables
    base_rows = [[p, persona_of[p], *[round(base[p][t], 3) for t in ("openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism")],
                  base[p][KPI_C], base[p][KPI_D], base[p]["Share postponed"], base[p]["Share skipped"],
                  base[p]["Share replaced"], base[p]["Share of postponements to a later day"]] for p in persons]
    oat_rows = []
    for p in reversed(order):
        row = [LABEL.get(p, p)]
        for group in [None] + PERSONAS:
            sel = [x for x in persons if group is None or persona_of[x] == group]
            row += [_mean([delta[p][x][0] for x in sel]), _mean([delta[p][x][1] for x in sel]),
                    _mean([swing[p][x] for x in sel])]
        oat_rows.append(row)
    abl_rows = []
    for a in ABL:
        for group in [None] + PERSONAS:
            sel = [x for x in persons if group is None or persona_of[x] == group]
            abl_rows.append([a, SHORT.get(group, "All 30 persons"),
                             _mean([abl[a][x][KPI_C] for x in sel]), _mean([abl[a][x][KPI_D] for x in sel]),
                             _mean([100 * (abl[a][x][KPI_C] - abl[ABL[0]][x][KPI_C]) for x in sel]),
                             _mean([abl[a][x][KPI_D] - abl[ABL[0]][x][KPI_D] for x in sel])])
    rank_rows = []
    for person in persons:
        ranked = sorted(params, key=lambda p: -swing[p][person])
        rank_rows.append([person, persona_of[person], *[LABEL.get(p, p) for p in ranked[:3]]])
    hdr = ["Parameter"]
    for g in ["All"] + [SHORT[p] for p in PERSONAS]:
        hdr += [f"{g}: low (pp)", f"{g}: high (pp)", f"{g}: swing (pp)"]
    write_workbook(out / "summary.xlsx", [
        ("Base per person", ["Person", "Persona", "Openness", "Conscientiousness", "Extraversion",
                             "Agreeableness", "Neuroticism", "Completion", "Deviation (h)",
                             "Share postponed", "Share skipped", "Share replaced",
                             "Postponements to a later day"], base_rows),
        ("OAT (completion)", hdr, oat_rows),
        ("Ablation", ["Model inputs", "Group", "Completion", "Deviation (h)",
                      "Completion change vs v1 inputs (pp)", "Deviation change vs v1 inputs (h)"], abl_rows),
        ("Top 3 per person", ["Person", "Persona", "1st", "2nd", "3rd"], rank_rows),
    ])
    print(f"Charts and summary written to {out.resolve()}")
    return {"order": order, "delta": delta, "swing": swing, "base": base, "abl": abl, "persona_of": persona_of}
