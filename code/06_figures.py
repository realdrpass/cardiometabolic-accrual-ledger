#!/usr/bin/env python3
"""Step 6: figures and the stats file.

Plain-language note: this script draws the report's charts and writes every
headline number into report/stats.json. The documents quote their numbers from
that file, so the text can be checked against the data in one place.

Outputs: report/figures/fig1_stop_reasons.png
         report/figures/fig2_stopped_by_area.png
         report/stats.json
"""
import json
import pathlib
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
P = ROOT / "data" / "processed"
OUT = ROOT / "report"
FIG = OUT / "figures"

SURFACE, INK, INK2, GRID, SERIES = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df", "#2a78d6"
STOPPED = ["TERMINATED", "WITHDRAWN", "SUSPENDED"]
LABELS = {"poor_enrollment": "Poor enrollment", "business_sponsor": "Business or sponsor decision",
          "other_or_not_stated": "Other or not stated", "design_logistics": "Design or logistics",
          "safety": "Safety", "lack_of_benefit": "Lack of benefit"}
AREAS = {"area_diabetes": "Diabetes", "area_obesity": "Obesity", "area_hypertension": "Hypertension",
         "area_heart_failure": "Heart failure", "area_dyslipidemia": "Dyslipidemia"}


def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, length=0)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def hbar(labels, values, annot, title, xlabel, caption, path, pct=False):
    fig, ax = plt.subplots(figsize=(8, 0.5 * len(labels) + 1.8), facecolor=SURFACE)
    style(ax)
    y = range(len(labels))[::-1]
    ax.barh(list(y), values, color=SERIES, height=0.62, edgecolor=SURFACE, linewidth=2)
    ax.set_yticks(list(y), labels, color=INK, fontsize=10)
    for yi, v, a in zip(y, values, annot):
        ax.text(v, yi, f"  {a}", va="center", ha="left", color=INK, fontsize=9.5)
    ax.set_xlabel(xlabel, color=INK2, fontsize=9.5)
    if pct:
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_xlim(0, max(values) * 1.25)
    ax.set_title(title, loc="left", color=INK, fontsize=12, fontweight="bold", pad=12)
    fig.text(0.01, 0.015, textwrap.fill(caption, 125), ha="left", va="bottom", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.09, 1, 0.97))
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    L = pd.read_csv(P / "ledger.csv", keep_default_na=False)
    prov = (ROOT / "data" / "raw" / "PROVENANCE.txt").read_text().split(" | ")[0]
    src = f"Source: ClinicalTrials.gov API v2, accessed {prov}. Cardiometabolic Trial Accrual Ledger v1.0."

    st = L[L.overall_status.isin(STOPPED)]
    counts = st.stop_category.value_counts()
    order = list(counts.index)
    hbar([LABELS[k] for k in order], [counts[k] for k in order],
         [f"{counts[k]}  ({counts[k] / len(st):.0%})" for k in order],
         f"Stated reasons for stopping early ({len(st)} trials)",
         "Trials", src + " Terminated, withdrawn and suspended trials; coding rules 1.0.",
         FIG / "fig1_stop_reasons.png")

    ended = L[L.overall_status.isin(["COMPLETED", "TERMINATED"])]
    rows = []
    for col, name in AREAS.items():
        e = ended[ended[col].astype(int) == 1]
        rows.append((name, len(e), (e.overall_status == "TERMINATED").sum()))
    rows.sort(key=lambda r: r[2] / r[1], reverse=True)
    hbar([r[0] for r in rows], [r[2] / r[1] for r in rows],
         [f"{r[2] / r[1]:.1%}  ({r[2]} of {r[1]})" for r in rows],
         "Share of finished trials that were terminated early",
         "Terminated / (completed + terminated)",
         src + " Trials in more than one area are counted in each.",
         FIG / "fig2_stopped_by_area.png", pct=True)

    term_enr = (L.overall_status == "TERMINATED") & (L.stop_category == "poor_enrollment")
    stats = {
        "access_date": prov,
        "n_in_scope": len(L),
        "n_completed": int((L.overall_status == "COMPLETED").sum()),
        "n_terminated": int((L.overall_status == "TERMINATED").sum()),
        "n_withdrawn": int((L.overall_status == "WITHDRAWN").sum()),
        "n_stopped_classified": len(st),
        "stop_counts": {k: int(v) for k, v in counts.items()},
        "terminated_share_of_finished": round((ended.overall_status == "TERMINATED").mean(), 4),
        "n_terminated_poor_enrollment": int(term_enr.sum()),
        "by_area": {r[0]: {"finished": int(r[1]), "terminated": int(r[2])} for r in rows},
        "median_actual_enrollment_completed": float(pd.to_numeric(
            L[(L.overall_status == "COMPLETED") & (L.enrollment_type == "ACTUAL")].enrollment_reported).median()),
    }
    (OUT / "stats.json").write_text(json.dumps(stats, indent=2))
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
