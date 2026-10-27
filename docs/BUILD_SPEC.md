# Build spec: Cardiometabolic Trial Accrual Ledger

*Plain-language note: this is the one-page plan the whole build follows. If the project changes, this file changes first. The plain version is at the bottom.*

```
PROJECT:        Cardiometabolic Trial Accrual Ledger (archetype: open dataset + technical report)
                v1.0 November 2026, v1.1 December 2026, Zenodo versioned DOI.
QUESTION:       Among US interventional drug trials in five cardiometabolic conditions, how often
                do trials miss their planned enrollment or stop early, and for what stated reasons?
SOURCES:        ClinicalTrials.gov API v2, https://clinicaltrials.gov/api/v2/studies
                Vintage: snapshot pulled on the access date in data/raw/PROVENANCE.txt.
                Terms: public US government data; attribution to ClinicalTrials.gov / NLM.
UNIT:           One trial (NCT ID).
INCLUSION:      Study type INTERVENTIONAL; phase includes PHASE2, PHASE3 or PHASE4
                (PHASE1/PHASE2 combined trials included, see ASSUMPTIONS); at least one
                intervention of type DRUG; first posted 2008-01-01 to 2025-12-31;
                at least one site in the United States (author ruling, 2026-10-13).
CONDITIONS:     Diabetes (type 1, type 2, unspecified, gestational), obesity/overweight,
                hypertension (essential/systemic, including hypertension in pregnancy and
                preeclampsia; EXCLUDING pulmonary, ocular, portal, intracranial: author ruling
                2026-10-13), heart failure, dyslipidemia (incl. hypercholesterolemia,
                hypertriglyceridemia, hyperlipidemia). Matching rules in docs/CODING_RULES.md.
                Diabetes complications, prediabetes, and diabetes-prevention trials in
                people without diabetes are left out (rulings 2026-10-13, widened 2026-10-26).
MEASURES:       planned_enrollment: last ESTIMATED enrollment count recorded before the
                  count switched to ACTUAL, from AACT archived snapshots (v1.1).
                actual_enrollment: enrollment count where type = ACTUAL.
                enrollment_ratio = actual / planned, only for COMPLETED or TERMINATED trials
                  that report an ACTUAL count (author ruling 2026-10-13).
                termination_category: six-group classification of whyStopped (coding rules 1.0).
                site_count (total and US), sponsor_class, phase, status, dates.
OUTPUTS:        data/processed/ledger.csv, CODEBOOK.md, CODING_RULES.md, qa_report.txt, qa_counts.json,
                scope_index_crosscheck.csv, report/stats.json,
                hand-check sample (10 percent) and form, technical report, figures.
VENUES:         GitHub (realdrpass) -> Zenodo DOI v1.0 -> Zenodo v1.1 -> data descriptor later.
VERIFY POINTS:  (1) condition match rules; (2) source of "planned" enrollment;
                (3) every stop-reason rule and each borderline case; (4) 10 percent hand check;
                (5) headline counts in the report.
LICENSE:        Code MIT; data and documents CC BY 4.0.
VERSIONS:       Author ruling 2026-10-13 ("A plus C"):
                v1.0 (Nov 2026): actual enrollment, stop-reason classification, site count,
                  sponsor class, phase, status, dates. planned_enrollment and enrollment_ratio
                  columns present but empty, with a documented reason.
                v1.1 (Dec 2026): planned_enrollment recovered from AACT archived snapshots
                  (Duke/CTTI); enrollment_ratio computed; coverage reported by year.
ASSUMPTIONS:    Phase 1/2 combined trials included because they carry PHASE2 (flag column).
                Withdrawn trials (enrolled zero) kept but excluded from the ratio.
```

## The plan in plain words

- **Unit: one trial.** Every row in your final table is one registered trial.
- **Who is in:** drug trials, Phase 2 to 4, first posted 2008 to 2025, with at least one US site, in your five disease areas.
- **The key number:** for each finished trial, actual patients divided by planned patients. 1.0 means it hit its target. 0.5 means it got half.
- **Stop reasons:** each early stop gets one of six labels, using written rules you approve.
- **Your checks:** you approve the rules, rule on unclear cases, hand-check about 10 percent of trials, and confirm the headline numbers.
