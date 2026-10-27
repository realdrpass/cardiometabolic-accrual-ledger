#!/usr/bin/env python3
"""Step 3: classify each stated stop reason into one of six groups.

Plain-language note: when a trial stops early, the sponsor types a short reason
into the registry ("slow enrollment", "business decision"). This script reads
that text and assigns one of six groups using the written rules below. Every
rule has an ID (R01, R02, ...) so each decision can be traced. Where more than
one group matches, a fixed priority order decides, and the trial is flagged so
the author can review it. Rulings by the author are marked with their date.
The same rules are written out in plain English in docs/CODING_RULES.md.

Input:  data/processed/ledger.csv
Output: data/processed/ledger.csv (adds stop-reason columns, rewritten in place)
        data/processed/stop_reason_review.csv (every flagged case, for the author)
"""
import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "processed" / "ledger.csv"
REVIEW = ROOT / "data" / "processed" / "stop_reason_review.csv"

RULES_VERSION = "1.0 (author rulings 2026-10-13)"

# Phrases that deny a reason ("not related to a safety concern", "no safety/efficacy
# concerns") are removed, from the denying word to the end of that clause, so the
# denied reason does not count. Rule N1.
NEGATION = re.compile(
    r"\b(no|not|without|unrelated|non)\b[^.;()]{0,40}?\b(safety|efficacy)\b"
    r"(?=[^.;()]{0,25}\b(concern|issue|reason|related|finding|problem))[^.;()]*")

# Rewrites applied before matching. Rule N2: "enrollment futility" is an enrollment
# problem, not a lack of benefit.
REWRITES = [
    # Rule N3: the name of a monitoring board is not itself a safety reason.
    (re.compile(r"data (and )?safety monitoring (board|committee)|\bdsmb\b|\bdmc\b"), " dsmb "),
    (re.compile(r"futil\w*\s+(for|of|due to)?\s*(the )?(lower than expected )?"
                r"(enrol|recruit|accru)\w*"), " enrollment "),
    (re.compile(r"(enrol|recruit|accru)\w*\s+futil\w*"), " enrollment "),
]

# Text that says the trial stopped but gives no reason. Rule R00 -> other_or_not_stated,
# no review needed.
UNINFORMATIVE = re.compile(
    r"^\W*(study |trial )?(was )?(withdrawn|terminated|never initiated|did not (begin|start)|"
    r"study completed|terminated prior to initiation|study terminated prior to initiation|"
    r"see (termination reason in )?(the )?detailed description|no longer looking for participants)\W*$")

# (rule_id, group, pattern). Patterns run on lowercased text after N1 and N2.
RULES = [
    ("R01", "safety", r"safety|adverse|\bae\b|toxicit|side effect|\bsaes?\b|\badrs?\b|\bharm\b|"
                      r"health risk|risk profile|death|mortality|hepat\w*tox|transaminit|"
                      r"liver (injury|signal|concern)|lymphodepletion|"
                      r"nonclinical (studies|findings)|animal|neutralizing"),
    ("R02", "lack_of_benefit", r"efficacy|futil|no (significant |clinical )?benefit|lack of (effect|benefit)|"
                               r"did not (meet|show|demonstrate)|no statistically significant|"
                               r"unlikely to (meet|achieve|demonstrate)|not (effective|efficacious)|"
                               r"no (significant )?clinical advantage|inadequate to continue|"
                               r"not (be )?completed? successfully|could not be complete"),
    ("R03", "poor_enrollment", r"recruit|enrol|accru|sample size|enough (patients|participants|subjects)|"
                               r"eligible (patients|participants|subjects)|lack of (patients|participants|subjects)|"
                               r"(identify\w*|find\w*) (subjects|patients|participants)|"
                               r"more participants than|(patients|subjects|participants) (that|who) meet|"
                               r"no (patients|participants|subjects|one)( were| was)? (screened|enrolled|consented)|"
                               r"(patients|participants|subjects) (were )?not (enrolled|screened)|"
                               r"(meet|met|satisfying the) inclusion|i/e criteria|screen fail"),
    ("R04", "business_sponsor", r"business|sponsor|company|corporate|industry|strateg|portfolio|commercial|"
                                r"fund|financ|budget|grant|award|acquir|merger|divest|priorit|"
                                r"program|development plan|no longer (interested|pursu)|"
                                r"moving forward|move forward|regulatory (uncertainty|value)|"
                                r"internal review|university decision|manufacturer discontinued"),
    ("R05", "design_logistics", r"investigator|\bpi\b|irb|ethic|logistic|administrat|technical|"
                                r"supply|supplies|unavailab|availab|shortage|manufactur|drug (was )?not|"
                                r"protocol|endpoint|design|feasib|\bsites?\b|staff|personnel|covid|pandemic|"
                                r"\bind\b|regulatory|fda|contract|replace|alternative study|follow-up|"
                                r"not (deemed )?(necessary|required)|evaluated in other stud|"
                                r"population changed"),
]
PRIORITY = ["safety", "lack_of_benefit", "poor_enrollment", "business_sponsor", "design_logistics"]

# Author rulings 2026-10-13 (defaults accepted):
# Rule M1: the drug was withdrawn from the market. Safety only if the stated reason
#          itself mentions a risk or safety problem (rule R01 fired); otherwise
#          other_or_not_stated.
MARKET = re.compile(r"withdrawn from (the )?(us )?market|removed from (the )?market|"
                    r"withdraw \w+ \w* ?from (the )?(us )?market|being withdrawn")
# Rule EB1: stopped early because the drug clearly worked -> other_or_not_stated.
BENEFIT = re.compile(r"compelling efficacy|overwhelming efficacy|early (benefit|success)")
# Rule CV1: COVID-19 as the only reason stays in design_logistics (via R05).

# Rule F1: phrases that always send a case to the author's review queue, whatever group
# it lands in, because the group cannot be read from the text alone.
ALWAYS_REVIEW = re.compile(
    r"benefit[- ]risk|interim analysis|"
    r"results (from|of) (an |the |a |recent |previous |other )|based on (the )?(results|data)|"
    r"data from other|dsmb|monitoring (board|committee)")

COVID = re.compile(r"covid|pandemic|sars-cov|coronavirus")
FUNDING = re.compile(r"fund|financ|budget|grant|award")


def clean(text):
    t = NEGATION.sub(" ", text.lower())
    for rx, rep in REWRITES:
        t = rx.sub(rep, t)
    return t


def classify(why):
    raw = why.strip()
    if not raw or UNINFORMATIVE.match(raw.lower()):
        return {"stop_category": "other_or_not_stated", "stop_categories_all": "",
                "stop_rules_fired": "R00" if raw else "", "stop_needs_review": 0}
    t = clean(raw)
    fired = [(rid, grp) for rid, grp, rx in RULES if re.search(rx, t)]
    groups = sorted({g for _, g in fired}, key=PRIORITY.index)
    if not groups:
        cat, review = "other_or_not_stated", 1  # text present but no rule matched
    else:
        cat, review = groups[0], int(len(groups) > 1)
    low = raw.lower()
    if MARKET.search(low):
        cat = "safety" if "safety" in groups else "other_or_not_stated"
        return {"stop_category": cat, "stop_categories_all": ";".join(groups),
                "stop_rules_fired": ";".join([r for r, _ in fired] + ["M1"]), "stop_needs_review": 0}
    if BENEFIT.search(low):
        return {"stop_category": "other_or_not_stated", "stop_categories_all": ";".join(groups),
                "stop_rules_fired": ";".join([r for r, _ in fired] + ["EB1"]), "stop_needs_review": 0}
    if ALWAYS_REVIEW.search(low):
        review = 1
        fired.append(("F1", ""))
    return {"stop_category": cat, "stop_categories_all": ";".join(groups),
            "stop_rules_fired": ";".join(r for r, _ in fired), "stop_needs_review": review}


def main():
    rows = list(csv.DictReader(LEDGER.open()))
    for r in rows:
        stopped = r["overall_status"] in ("TERMINATED", "WITHDRAWN", "SUSPENDED")
        if stopped:
            r.update(classify(r["why_stopped"]))
        else:
            r.update({"stop_category": "", "stop_categories_all": "",
                      "stop_rules_fired": "", "stop_needs_review": 0})
        r["stop_mentions_covid"] = int(stopped and bool(COVID.search(r["why_stopped"].lower())))
        r["stop_mentions_funding"] = int(stopped and bool(FUNDING.search(r["why_stopped"].lower())))
        r["stop_rules_version"] = RULES_VERSION if stopped else ""
    cols = list(rows[0].keys())
    with LEDGER.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    review = [r for r in rows if str(r["stop_needs_review"]) == "1"]
    with REVIEW.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["nct_id", "overall_status", "why_stopped",
                                          "stop_categories_all", "stop_category",
                                          "author_ruling", "author_note"])
        w.writeheader()
        for r in review:
            w.writerow({k: r.get(k, "") for k in w.fieldnames})
    print(f"classified {sum(1 for r in rows if r['stop_rules_version'])} stopped trials; "
          f"{len(review)} flagged for review")


if __name__ == "__main__":
    main()
