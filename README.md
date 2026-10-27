# Cardiometabolic Trial Accrual Ledger

**Version 1.0 (26 October 2026). Registry data accessed 13 October 2026.**

This is a free, open dataset of 2,834 US interventional drug trials in diabetes, obesity, hypertension, heart failure and dyslipidemia. The trials are Phase 2 to 4, were first posted from 2008 to 2025, and have at least one US site. For each trial the dataset records enrollment, status, sites, sponsor class and phase. For the 468 trials that stopped early, it also records the sponsor's stated reason, classified into one of six groups by published, traceable coding rules. Poor enrollment is the most common stated reason, given for 151 of the 468. Every number can be rebuilt from the archived registry download with the scripts here, and the ledger can be updated each year.

## What is in it

| File | What it is |
|---|---|
| `data/processed/ledger.csv` | The ledger: one row per trial (2,834 rows) |
| `docs/CODEBOOK.md` | Every column explained |
| `docs/CODING_RULES.md` | Inclusion rules and stop-reason rules, each with an ID and the date of each ruling |
| `docs/LIMITATIONS.md` | What the data can and cannot support |
| `data/processed/qa_report.txt`, `qa_counts.json` | Row counts and range checks at every stage |
| `data/processed/ledger_all_candidates.csv` | All 3,881 fetched trials, with the reason each was in or out |
| `data/processed/scope_borderline.csv` | The 220 trials left out as borderline (diabetes complications, prediabetes and prevention, surgical blood-pressure spikes) |
| `data/processed/scope_index_crosscheck.csv` | The 244 out-of-scope trials that the registry's own disease index links to one of the five areas, with the reason each is out |
| `data/processed/stop_reason_review.csv` | The 85 stop reasons flagged for review |
| `data/processed/handcheck_sample.csv`, `report/handcheck_form.xlsx` | The 10 percent random sample (284 trials, seed 20261013) and the form used to check it by hand against the registry |
| `report/figures/`, `report/stats.json` | Figures, and every headline number in this README |
| `data/raw/` | The registry download (compressed), the exact query, and file fingerprints |

**Hand check.** The 10 percent sample is drawn, and the form compares eight fields per trial. Agreement rates will be reported here when the check is complete.

**Version plan.** v1.0 has actual enrollment, stop reasons, sites, sponsor class and phase. v1.1 (December 2026) adds planned enrollment and the enrollment ratio, recovered from archived registry snapshots. See `docs/NEXT_STEPS.md`.

## How to rebuild it

```
pip install pandas openpyxl matplotlib
python code/02_build.py      # one row per trial; apply inclusion rules
python code/03_classify.py   # classify stop reasons
python code/04_qa.py         # quality report and cross-checks
python code/05_sample.py     # draw the 10 percent hand-check sample (seed 20261013)
python code/06_figures.py    # figures and report/stats.json
```

These steps use the archived 13 October 2026 download (`data/raw/ctgov_studies.jsonl.gz`). Its uncompressed contents match the SHA-256 fingerprint in `data/raw/PROVENANCE.txt`. To take a fresh snapshot of the registry instead, run `python code/01_fetch.py` first. The exact query is in `data/raw/query.json`.

## Source and terms

Courtesy of the U.S. National Library of Medicine. Source: ClinicalTrials.gov, version 2 data interface (https://clinicaltrials.gov/data-api/api), data accessed and processed 13 October 2026.

This dataset is derived from those records. Records were selected and fields extracted, and stop reasons were classified, as described in `docs/CODING_RULES.md` and `docs/CODEBOOK.md`. It is a dated snapshot and does not reflect later changes to the registry. It is not a product of, and is not endorsed by, the National Library of Medicine. NLM notes that ClinicalTrials.gov data may carry copyright outside the United States.

## License

Code: MIT (`LICENSE`). Data and documentation: CC BY 4.0 (`LICENSE-DATA`).

## Cite

See `CITATION.cff`. The DOI is added when the Zenodo record is published.

## Author

Olufisayo Ogunbayo, Independent Researcher. ORCID [0009-0003-0351-0786](https://orcid.org/0009-0003-0351-0786). The author set every inclusion and coding rule and checked the counts. AI assistance (Claude, Anthropic) was used to write the data pipeline and documentation.
