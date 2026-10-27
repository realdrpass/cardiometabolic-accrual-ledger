# Codebook: data/processed/ledger.csv

*Plain-language note: this explains every column in the main table. One row is one trial. "Registry" means ClinicalTrials.gov; field paths are from its version 2 data interface. You only need this when reading or citing a specific column.*

| Column | Meaning | Source / transformation |
|---|---|---|
| nct_id | Trial registry number | `identificationModule.nctId` |
| brief_title | Short title | `identificationModule.briefTitle` |
| in_scope | 1 if the trial meets all inclusion rules (always 1 in ledger.csv) | Rules C1–C5, X1–X2, B1–B3 and B2t in CODING_RULES.md |
| area_diabetes … area_dyslipidemia | 1 if any listed condition is a plain (non-borderline) match for that area | Rules C1–C5 applied to `conditionsModule.conditions`; B2t can remove diabetes |
| n_areas | Number of areas matched (a trial can be in more than one) | Sum of area flags |
| borderline_group | Borderline group that kept the trial out (always empty in ledger.csv) | Rules B1–B3, B2t |
| excluded_htn_conditions | Hypertension wordings that were set aside under rule X2 | Rule X2 |
| conditions | Conditions as the sponsor listed them, joined with "; " | `conditionsModule.conditions` |
| phase | Phase(s), e.g. PHASE2, PHASE1/PHASE2 | `designModule.phases` |
| phase1_2_combined | 1 if the trial is a combined Phase 1/2 | Derived from phase |
| intervention_types | All intervention types listed (DRUG is always present) | `armsInterventionsModule.interventions[].type` |
| overall_status | Status on the access date | `statusModule.overallStatus` |
| why_stopped | Sponsor's stated reason for stopping, verbatim | `statusModule.whyStopped` |
| first_posted, start_date, primary_completion_date, completion_date, last_update_posted | Key dates (YYYY-MM or YYYY-MM-DD as registered) | `statusModule` date fields |
| enrollment_reported | Enrollment number currently shown | `designModule.enrollmentInfo.count` |
| enrollment_type | ACTUAL or ESTIMATED | `designModule.enrollmentInfo.type` |
| planned_enrollment | **Empty in v1.0.** Planned enrollment before the trial reported its actual count. Added in v1.1 from AACT archived snapshots | See NEXT_STEPS.md |
| actual_enrollment | enrollment_reported when enrollment_type is ACTUAL, otherwise empty | Derived |
| enrollment_ratio | **Empty in v1.0.** actual ÷ planned, completed and terminated trials only | v1.1 |
| site_count | Number of sites listed | Length of `contactsLocationsModule.locations` |
| us_site_count | Number of listed sites in the United States | Locations with country "United States" |
| lead_sponsor | Lead sponsor name | `sponsorCollaboratorsModule.leadSponsor.name` |
| sponsor_class | Registry sponsor class: INDUSTRY, NIH, FED, OTHER_GOV, NETWORK, INDIV, OTHER (OTHER is mostly universities and hospitals) | `leadSponsor.class` |
| has_results | 1 if results are posted on the registry | `hasResults` |
| stop_category | One of six stop-reason groups; empty unless status is Terminated, Withdrawn or Suspended | Rules R00–R05, N1–N3, M1, EB1, CV1 |
| stop_categories_all | Every group whose rule matched, in priority order | Same |
| stop_rules_fired | Rule IDs that matched, so each decision can be traced | Same |
| stop_needs_review | 1 if the case was flagged for the author's review | Multiple groups, no match, or rule F1 |
| stop_mentions_covid | 1 if the reason mentions COVID-19 or the pandemic | Text match |
| stop_mentions_funding | 1 if the reason mentions funding, grants or budget | Text match |
| stop_rules_version | Version of the coding rules applied | 03_classify.py |
