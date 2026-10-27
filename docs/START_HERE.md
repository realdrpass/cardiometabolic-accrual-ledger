# Start Here: Cardiometabolic Trial Accrual Ledger

*Read this first. It explains your project in plain language. Words in bold are explained in [GLOSSARY.md](GLOSSARY.md).*

## What you are building

A free public spreadsheet of 2,834 US drug trials for diabetes, obesity, high blood pressure, heart failure, and high cholesterol. For each trial it shows how many patients it enrolled and, if it stopped early, why. Version 1.1 adds how many patients each trial planned to enroll.

## Why it matters

Clinical trials often fail to sign up enough patients. When that happens, the trial stops early or finishes too small to answer its question, and the money and the patients' time are partly wasted. Everyone in the field knows this happens, but nobody publishes one clean, national count for heart and metabolic disease that others can cite and recheck each year.

This project makes that count. Think of it as a public scoreboard for trial enrollment: for every trial, the target, the final score, and the reason the game was called off if it was.

## Where the information comes from

All sources are free and public. Nothing here needs special permission.

| Source | In plain terms | What one row looks like | Link |
|---|---|---|---|
| ClinicalTrials.gov (version 2 data interface) | The US government's official registry of clinical trials, run by the National Library of Medicine. Sponsors are required by law to report most trials here. | One trial: its ID (like NCT01234567), conditions, phase, sponsor, number of sites, planned and actual enrollment, status, and the sponsor's stated reason for stopping, if it stopped. | https://clinicaltrials.gov/data-api/api |

The download on October 13, 2026 found 3,881 candidate trials. After your rules were applied, 2,834 trials are in scope.

## What you will have at the end

- [ ] **A public project page** on GitHub with the data, the code, and the coding rules (link added when published)
- [ ] **A permanent citation number (DOI)** from Zenodo for version 1.0 (November 2026), added when the Zenodo record is published
- [ ] **Version 1.1** (December 2026), an update under the same DOI family, with corrections from your hand check and any refinements
- [ ] **A codebook** explaining every column, and **published coding rules** for how stop reasons were classified
- [ ] **A hand-check record**: a 10 percent random sample (284 trials) compared field by field against the registry
- [ ] **A short technical report** describing the dataset and its headline numbers (planned with v1.1)

## How it connects to your work

Your petition argues that recruitment failure in trials is widespread and nobody measures it. This dataset is that measurement, made public. It is also the reference data your CTROF tool is tuned against, so it anchors the rest of your plan.

## What you need to do

| Your task | When | Time |
|---|---|---|
| Create accounts (ORCID, GitHub, Zenodo) | Now | 15 min |
| Answer five setup questions | Now | 10 min |
| Rule on the stop-reason coding rules | After the first data pull | 30 to 45 min |
| Hand-check the 10 percent sample | Now | 9 to 10 hours, spread over a few sittings |
| Check the headline counts with the checklist | Now | 1 to 2 hours |
| Approve publishing | After checking | 5 min |

The hand check is the largest task. It is also the part that makes this dataset trustworthy to a referee, so it is worth the time.

## The steps ahead

1. **Data collected.** We download every matching trial record and log exactly where and when.
2. **Data cleaned and combined.** One row per trial. The enrollment ratio follows in v1.1.
3. **Stop reasons classified.** Using written rules that you approved or changed.
4. **Quality checks.** Counts, ranges, and odd cases flagged.
5. **Hand-check sample drawn.** 284 trials, picked at random, with a form for you to fill in.
6. **Figures.** Every number pulled straight from the data.
7. **Ready for your check.** You verify, then we publish version 1.0.

*You are here: step 7. Version 1.0 was verified and approved by the author on 26 October 2026, and is ready to publish (see PUBLISH_GUIDE.md). Hand-check agreement rates and planned enrollment follow in v1.1.*
