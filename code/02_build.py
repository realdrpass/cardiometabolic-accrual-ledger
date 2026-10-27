#!/usr/bin/env python3
"""Step 2: turn raw registry records into one row per trial, applying the scope rules.

Plain-language note: this script reads the downloaded trial records, decides
which ones are in scope (using the written rules below), and writes the main
table, data/processed/ledger.csv. Every rule is at the top of the file, in
plain patterns, so a reviewer can see exactly what was included and why.
Rule IDs match docs/CODING_RULES.md.

Inputs:  data/raw/ctgov_studies.jsonl (or .jsonl.gz)
Outputs: data/processed/ledger_all_candidates.csv  (every fetched trial, with match flags)
         data/processed/ledger.csv                  (in-scope trials only)
"""
import csv
import json
import pathlib
import re

from raw_records import raw_lines

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"

# ---------------------------------------------------------------------------
# CONDITION RULES. Applied to each condition the sponsor listed, lowercased.
# Rule IDs match docs/CODING_RULES.md.
# A trial is in scope if at least one listed condition is a plain match (C1-C5)
# that is not set aside by X1-X2 or a borderline group (B1-B3), and the trial is
# not a diabetes-prevention trial (B2t) unless another area keeps it in.
# ---------------------------------------------------------------------------
HARD_EXCLUDE = re.compile(r"insipidus")  # X1: diabetes insipidus is not diabetes mellitus

HTN_NOT_SYSTEMIC = re.compile(  # X2: author ruling 2026-10-13
    r"pulmon|portopulm|ocular|oular|intraocular|glaucoma|portal|intracranial")

CORE = {
    # C1
    "diabetes": re.compile(r"diabet|\bt[12]d(m)?\b|\bdm\b|\biddm\b|\bniddm\b|\bmody\b|"
                           r"glyc(a)?emic control"),
    # C2
    "obesity": re.compile(r"obes|overweight|weight management|adiposity|weight loss|"
                          r"weight reduction|(elevated|high|increased) (body mass index|bmi)"),
    # C3
    "hypertension": re.compile(r"hypertens|blood pressure|\bhtn\b|pre-?eclamp|eclampsia"),
    # C4
    "heart_failure": re.compile(r"heart failure|cardiac failure|\bhf(r|p|mr)?ef\b|\bchf\b|cardiomyopathy.*failure"),
    # C5
    "dyslipidemia": re.compile(
        r"dyslipid|hyperlipid|hypercholest|hypertriglycerid|hyperlipoprot|\blipid(a)?emia|"
        r"lipoprotein\(a\)|\blp\(a\)|\bldl\b|chylo\w*micron|lipid disorder|mixed lipid|"
        r"(high|elevated) (cholesterol|triglycerid)|(cholesterol|triglycerides?),? (elevated|high)|"
        r"lipoprotein disorder|hypoalphalipoprot|lipoprotein lipase deficiency|\blpl deficiency"),
}

# Borderline groups. A condition that matches one of these does not count toward
# any area (author ruling 2026-10-13: borderline trials are left out).
BORDERLINE = {
    # B1: a complication of diabetes rather than diabetes itself.
    "diabetes_complication": re.compile(
        r"diabet\w*\s+(retinopath|macular|neuropath|foot|ulcer|wound|gastroparesis|"
        r"nephropath|kidney|ketoacid)|"
        r"(retinopath|neuropath|foot ulcer|gastroparesis|nephropath|kidney disease).*diabet"),
    # B2: prediabetes, insulin resistance, or people at risk of diabetes who do not
    # have it (rule widened 2026-10-26 to cover "non-diabetic", "at risk for
    # diabetes" and "pre diabetes" written with a space).
    "prediabetes": re.compile(
        r"pre[- ]?diabet|impaired (fasting )?glucose|insulin resist|glucose intoleran|"
        r"(abnormal|impaired) glucose (tolerance|metabolism|regulation)|disorder of glucose regulation|"
        r"non-?diabet|without diabet|at[- ]risk\b.*diabet|risk (for|of) (developing )?(type ?[12] )?diabet|"
        r"(diabetes|diabetic) risk|prevent\w*( of)? (new[- ]onset )?(type ?[12] )?diabet|diabetes prevention"),
    # B3: short-term blood pressure spikes around surgery, not chronic hypertension.
    "acute_periop_hypertension": re.compile(
        r"(intraoperative|perioperative|postoperative|tourniquet|emergenc|acute)\s+hypertens"),
}

# B2t (added 2026-10-26): a trial whose title says its aim is to prevent or delay
# diabetes, or that it enrolls people at risk of diabetes, is a prevention trial in
# people without diabetes, whatever its condition list says. Its diabetes match is
# set aside as "prediabetes". It stays in the ledger only if another area matches.
PREVENTION_TITLE = re.compile(
    r"prevent\w*\s+(of\s+)?(the\s+)?(abnormal glucose tolerance and\s+)?(new[- ]onset\s+|post-?transplant\w*\s+)?"
    r"(stage\s*3\s+)?(type\s*[12]\s+)?diabetes\b|"
    r"\bdelay\w*\s+(of\s+)?(the\s+)?(onset\s+of\s+)?(stage\s*3\s+)?(type\s*[12]\s+)?diabetes\b|"
    r"at[- ]risk\W*\s+(for|of)\s+(developing\s+)?(type\s*[12]\s+)?diabetes|"
    r"relatives\s+\W?at[- ]risk|"
    r"(reduce|lower)\w*\s+(the\s+)?diabetes risk")


def classify_conditions(conds, title=""):
    """Return (areas, borderline groups that kept the trial out, hypertension wordings set aside)."""
    areas, borderline_seen, excluded_htn = set(), set(), []
    for raw in conds:
        c = raw.lower().strip()
        if HARD_EXCLUDE.search(c):
            continue
        hits = set()
        for area, rx in CORE.items():
            if not rx.search(c):
                continue
            if area == "hypertension" and HTN_NOT_SYSTEMIC.search(c):
                excluded_htn.append(raw)
                continue
            hits.add(area)
        if not hits:
            continue
        b = {name for name, brx in BORDERLINE.items() if brx.search(c)}
        if b:
            borderline_seen |= b      # borderline wording: counts toward no area
        else:
            areas |= hits
    if "diabetes" in areas and PREVENTION_TITLE.search(title.lower()):
        areas.discard("diabetes")
        borderline_seen.add("prediabetes")
    return areas, (set() if areas else borderline_seen), excluded_htn


def g(d, *path, default=None):
    for p in path:
        if not isinstance(d, dict):
            return default
        d = d.get(p)
        if d is None:
            return default
    return d


def row_for(s):
    p = s["protocolSection"]
    conds = g(p, "conditionsModule", "conditions", default=[])
    title = g(p, "identificationModule", "briefTitle", default="")
    areas, borderline, ex_htn = classify_conditions(conds, title)
    locs = g(p, "contactsLocationsModule", "locations", default=[])
    phases = g(p, "designModule", "phases", default=[])
    enr = g(p, "designModule", "enrollmentInfo", default={})
    status = g(p, "statusModule", "overallStatus")
    itypes = sorted({i.get("type") for i in g(p, "armsInterventionsModule", "interventions", default=[])})
    return {
        "nct_id": g(p, "identificationModule", "nctId"),
        "brief_title": g(p, "identificationModule", "briefTitle"),
        "in_scope": int(bool(areas) and not borderline),
        "area_diabetes": int("diabetes" in areas),
        "area_obesity": int("obesity" in areas),
        "area_hypertension": int("hypertension" in areas),
        "area_heart_failure": int("heart_failure" in areas),
        "area_dyslipidemia": int("dyslipidemia" in areas),
        "n_areas": len(areas),
        "borderline_group": ";".join(sorted(borderline)),
        "excluded_htn_conditions": "; ".join(ex_htn),
        "conditions": "; ".join(conds),
        "phase": "/".join(phases),
        "phase1_2_combined": int(phases == ["PHASE1", "PHASE2"]),
        "intervention_types": ";".join(t for t in itypes if t),
        "overall_status": status,
        "why_stopped": (g(p, "statusModule", "whyStopped") or "").strip(),
        "first_posted": g(p, "statusModule", "studyFirstPostDateStruct", "date"),
        "start_date": g(p, "statusModule", "startDateStruct", "date"),
        "primary_completion_date": g(p, "statusModule", "primaryCompletionDateStruct", "date"),
        "completion_date": g(p, "statusModule", "completionDateStruct", "date"),
        "enrollment_reported": enr.get("count"),
        "enrollment_type": enr.get("type"),
        # Planned enrollment is not in the current public record once a trial reports
        # its actual count. Empty in v1.0; recovered from AACT snapshots in v1.1.
        "planned_enrollment": "",
        "actual_enrollment": enr.get("count") if enr.get("type") == "ACTUAL" else "",
        "enrollment_ratio": "",
        "site_count": len(locs),
        "us_site_count": sum(1 for l in locs if l.get("country") == "United States"),
        "lead_sponsor": g(p, "sponsorCollaboratorsModule", "leadSponsor", "name"),
        "sponsor_class": g(p, "sponsorCollaboratorsModule", "leadSponsor", "class"),
        "has_results": int(bool(s.get("hasResults"))),
        "last_update_posted": g(p, "statusModule", "lastUpdatePostDateStruct", "date"),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [row_for(json.loads(l)) for l in raw_lines()]
    cols = list(rows[0].keys())
    for name, subset in (("ledger_all_candidates.csv", rows),
                         ("ledger.csv", [r for r in rows if r["in_scope"]])):
        with (OUT / name).open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(subset)
        print(f"{name}: {len(subset)} rows")


if __name__ == "__main__":
    main()
