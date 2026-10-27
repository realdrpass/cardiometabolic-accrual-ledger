# Coding rules, version 1.0

*Plain-language note: these are the written rules that decide (A) which trials are in the ledger and (B) which group each stop reason falls into. They are published with the dataset so anyone can check or reuse them. Every rule was set or approved by Olufisayo Ogunbayo; each ruling is dated. The code that applies them is `code/02_build.py` (Part A) and `code/03_classify.py` (Part B), and the rule IDs match.*

## Part A. Which trials are in the ledger

**Structural criteria** (applied by the registry query in `code/01_fetch.py`): interventional study; phase includes Phase 2, 3 or 4; at least one intervention of type Drug; first posted 1 January 2008 to 31 December 2025; at least one site in the United States (ruling, 13 Oct 2026).

**Condition criteria** (applied to each condition the sponsor listed, ignoring case):

| Rule | Area | A listed condition counts if it contains |
|---|---|---|
| C1 | Diabetes | "diabet"; the abbreviations T1D, T2D, DM, IDDM, NIDDM, MODY; "glycemic control" |
| C2 | Obesity | "obes", "overweight", "weight management", "weight loss", "weight reduction", "adiposity", elevated or high body mass index (BMI) |
| C3 | Hypertension | "hypertens", "blood pressure", HTN, preeclampsia, eclampsia |
| C4 | Heart failure | "heart failure", "cardiac failure", HFrEF, HFpEF, HFmrEF, CHF |
| C5 | Dyslipidemia | dyslipidemia, hyperlipidemia, lipidemia, hypercholesterolemia, hypertriglyceridemia, hyperlipoproteinemia, hypoalphalipoproteinemia (low HDL), lipoprotein(a), LDL, chylomicronemia (including misspellings such as "chylocmicronemia"), lipoprotein lipase (LPL) deficiency, high or elevated cholesterol or triglycerides (either word order), "lipid disorder", "lipoprotein disorder" |
| X1 | Excluded | "diabetes insipidus" never counts |
| X2 | Excluded (ruling, 13 Oct) | Hypertension wording that mentions pulmonary, ocular or intraocular, glaucoma, portal, or intracranial does not count for C3 |

The wordings added to C1, C2 and C5 on 26 October 2026 close gaps found in the author's review. Thirteen trials whose listed condition names one of the five diseases in other words ("Glycemic Control", "Weight Loss", "High Triglycerides", "Cholesterol, Elevated", "Chylocmicronemia", and others) had been missed.

**Borderline groups (left out: ruling, 13 Oct).** A listed condition that matches one of these groups counts toward no area. A trial is left out unless another of its listed conditions is a plain match.

| Group | What it is | Trials left out |
|---|---|---|
| B1 diabetes_complication | A diabetes complication (eye, nerve, foot ulcer, stomach, kidney, ketoacidosis) rather than diabetes itself | 182 |
| B2 prediabetes | Prediabetes (including "pre diabetes" written with a space), impaired glucose tolerance, insulin resistance, and people **without** diabetes who are at risk of it ("non-diabetic", "at risk for diabetes", "diabetes prevention") | 36 (with B2t) |
| B2t prevention trials | A trial whose title says it aims to prevent or delay diabetes, or that it enrolls people at risk of diabetes (for example, relatives at risk of type 1 diabetes), is treated as B2 whatever its condition list says. It stays in only if it also matches another area. | included above |
| B3 acute_periop_hypertension | Short-term blood-pressure spikes during or after surgery | 2 |

B2 was widened and B2t added on 26 October 2026, because some prevention trials in people without diabetes had been included. NCT01030861 is one example: its conditions say "Non-diabetic Relatives at Risk for Type 1 Diabetes".

**What stays out, and why.** Inclusion depends on the conditions the sponsor listed. A trial is out when it lists only another disease (for example, "Atherosclerotic Cardiovascular Disease" for a cholesterol-lowering drug, or "Chronic Kidney Disease" for a blood-pressure drug), even if its participants have one of the five. Weight gain caused by another medicine or by quitting smoking, hospital hyperglycemia, and hypoglycemia unawareness are not counted as obesity or diabetes trials. Every out-of-scope trial that the registry's own disease index places in one of the five areas is listed, with the reason it is out, in `data/processed/scope_index_crosscheck.csv`.

## Part B. Stop-reason groups

Applied to every trial whose status is Terminated, Withdrawn or Suspended, using the sponsor's "why stopped" text.

| Group | Rule | Matches text about |
|---|---|---|
| Safety | R01 | safety, adverse events, toxicity, side effects, health risk, liver injury, animal or nonclinical findings |
| Lack of benefit | R02 | efficacy, futility, no benefit, did not meet or show, not effective |
| Poor enrollment | R03 | recruitment, enrollment, accrual, sample size, cannot find or identify eligible patients, screen failures |
| Business or sponsor decision | R04 | business, sponsor or company decision, strategy, portfolio, funding, grant or award ended, acquisition or divestment, program ended |
| Study design or logistics | R05 | investigator left, IRB or ethics, drug supply, manufacturing, protocol or endpoint change, feasibility, staffing, COVID-19, regulatory or IND issues |
| Other or not stated | R00 | blank, or text that says only "withdrawn", "terminated", "never initiated", "see detailed description" |

**Preparation steps before matching**

- **N1 Denials don't count.** "Not related to a safety concern" or "no safety or efficacy concerns" removes that reason before matching.
- **N2 Enrollment futility is enrollment.** "Futility due to low recruitment" or "enrollment futility" counts as poor enrollment, not lack of benefit.
- **N3 Board names aren't reasons.** "Data Safety Monitoring Board" alone does not count as a safety reason.

**When more than one group matches**, the first one in this order wins: Safety, Lack of benefit, Poor enrollment, Business or sponsor, Design or logistics. The case is flagged for review, and all matching groups are kept in `stop_categories_all`.

**Rulings, 13 October 2026**

- **M1 Market withdrawal.** If the drug was withdrawn from the market, the trial counts as Safety only if the stated reason itself mentions a risk or safety problem. Otherwise it counts as Other or not stated.
- **EB1 Stopped for benefit.** "Compelling" or "overwhelming" efficacy, or early success, counts as Other or not stated.
- **CV1 COVID-19.** COVID-19 as the only reason stays in Design or logistics.

**Always flagged for review (F1):** benefit-risk wording, interim analyses, decisions based on other studies' results, and monitoring-board recommendations. These can't be read reliably from the text alone.

**Extra flags** (do not change the group): `stop_mentions_covid`, `stop_mentions_funding`.

## Results under these rules

| Group | Total |
|---|---|
| Poor enrollment | 151 |
| Business or sponsor | 134 |
| Other or not stated | 71 |
| Design or logistics | 60 |
| Safety | 27 |
| Lack of benefit | 25 |
| **Total** | **468** |

85 cases are flagged for review. They are listed in `data/processed/stop_reason_review.csv`.
