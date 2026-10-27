#!/usr/bin/env python3
"""Step 4: quality report and the author's review lists.

Plain-language note: this script counts rows at every stage, checks value
ranges, and writes data/processed/qa_report.txt plus the list of borderline
trials (scope_borderline.csv), a cross-check against the registry's own disease
index (scope_index_crosscheck.csv), and the counts file qa_counts.json. Read the
report before trusting any number.
"""
import json
import pathlib
import re

import pandas as pd

from raw_records import raw_lines

ROOT = pathlib.Path(__file__).resolve().parents[1]
P = ROOT / "data" / "processed"


def main():
    raw_n = sum(1 for _ in raw_lines())
    a = pd.read_csv(P / "ledger_all_candidates.csv", keep_default_na=False)
    L = pd.read_csv(P / "ledger.csv", keep_default_na=False)
    out = []
    w = out.append
    w("QA REPORT — Cardiometabolic Trial Accrual Ledger v1.0")
    w(f"Raw records fetched: {raw_n}")
    w(f"Candidate rows built: {len(a)}  (must equal raw: {'OK' if len(a) == raw_n else 'FAIL'})")
    w(f"Duplicate NCT IDs: {a.nct_id.duplicated().sum()}")
    w(f"No cardiometabolic condition match: "
      f"{((a.n_areas.astype(int) == 0) & (a.borderline_group == '')).sum()}")
    w(f"Held out as borderline: {(a.borderline_group != '').sum()}")
    for g, n in a[a.borderline_group != ""].borderline_group.value_counts().items():
        w(f"   {g}: {n}")
    w(f"IN SCOPE (ledger.csv): {len(L)}")
    for c in [c for c in L if c.startswith("area_")]:
        w(f"   {c}: {L[c].astype(int).sum()}")
    w(f"   trials in 2+ areas: {(L.n_areas.astype(int) > 1).sum()}")
    w("Status:")
    for s, n in L.overall_status.value_counts().items():
        w(f"   {s}: {n}")
    fin = L.overall_status.isin(["COMPLETED", "TERMINATED"])
    w(f"Completed or terminated: {fin.sum()}; of these reporting ACTUAL enrollment: "
      f"{(fin & (L.enrollment_type == 'ACTUAL')).sum()}")
    w(f"Planned enrollment available: {(L.planned_enrollment != '').sum()}  "
      "(empty in v1.0 by design; added in v1.1, see docs/NEXT_STEPS.md)")
    e = pd.to_numeric(L.enrollment_reported, errors="coerce")
    w(f"Enrollment reported: min {e.min():.0f}, median {e.median():.0f}, max {e.max():.0f}, missing {e.isna().sum()}")
    w(f"Site count: min {L.site_count.astype(int).min()}, median {L.site_count.astype(int).median():.0f}, "
      f"max {L.site_count.astype(int).max()}; trials listing 0 sites: {(L.site_count.astype(int) == 0).sum()}")
    w(f"US site count 0 (should be 0): {(L.us_site_count.astype(int) == 0).sum()}")
    w("Sponsor class:")
    for s, n in L.sponsor_class.value_counts().items():
        w(f"   {s}: {n}")
    w("Phase:")
    for s, n in L.phase.value_counts().items():
        w(f"   {s}: {n}")
    st = L[L.stop_rules_version != ""]
    w(f"Stopped trials classified: {len(st)}; flagged for review: {(st.stop_needs_review.astype(int) == 1).sum()}")
    for s, n in st.stop_category.value_counts().items():
        w(f"   {s}: {n}")
    # Cross-check: out-of-scope trials that the registry's own disease index (MeSH,
    # assigned automatically by NLM) places in one of the five areas. The index is
    # not used for inclusion because it is noisy (it tags some cancer trials as
    # diabetes, and lung hypertension as hypertension); this list exists so that
    # readers can see every disagreement and why each trial is out.
    mesh_rx = re.compile(
        r"^(Diabetes Mellitus.*|Diabetes, Gestational|Obesity.*|Pediatric Obesity|Overweight|Hypertension|"
        r"Essential Hypertension|Hypertension, (Pregnancy-Induced|Renal|Malignant)|Pre-Eclampsia|Eclampsia|"
        r"Heart Failure.*|Dyslipidemias|Hyperlipidemia.*|Hypercholesterolemia.*|Hypertriglyceridemia.*|"
        r"Hyperlipoproteinemia.*|Hypoalphalipoproteinemias|Hypolipoproteinemias)$")
    out_scope = set(a[a.in_scope.astype(int) == 0].nct_id)
    xc = []
    for line in raw_lines():
        s = json.loads(line)
        n = s["protocolSection"]["identificationModule"]["nctId"]
        if n not in out_scope:
            continue
        ms = [m["term"] for m in s.get("derivedSection", {}).get("conditionBrowseModule", {}).get("meshes", [])]
        hit = [m for m in ms if mesh_rx.match(m)]
        if hit:
            xc.append({"nct_id": n, "index_terms": "; ".join(hit)})
    xc = pd.DataFrame(xc).merge(a[["nct_id", "brief_title", "conditions", "borderline_group",
                                   "excluded_htn_conditions"]], on="nct_id")
    xc["why_out"] = xc.apply(
        lambda r: f"borderline: {r.borderline_group}" if r.borderline_group
        else ("hypertension type excluded (X2)" if r.excluded_htn_conditions
              else "listed conditions are other diseases"), axis=1)
    xc.to_csv(P / "scope_index_crosscheck.csv", index=False)
    w(f"Out-of-scope trials the registry index places in a target area: {len(xc)} "
      f"(listed with reasons in scope_index_crosscheck.csv)")
    for k, v in xc.why_out.value_counts().items():
        w(f"   {k}: {v}")
    (P / "qa_report.txt").write_text("\n".join(out) + "\n")
    a[a.borderline_group != ""][["nct_id", "brief_title", "conditions", "borderline_group"]].assign(
        author_ruling="").to_csv(P / "scope_borderline.csv", index=False)
    stats = {"raw": raw_n, "in_scope": len(L), "borderline": int((a.borderline_group != "").sum()),
             "stopped_classified": len(st)}
    (P / "qa_counts.json").write_text(json.dumps(stats, indent=2))
    print("\n".join(out))


if __name__ == "__main__":
    main()
