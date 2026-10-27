# Your verification checklist (v1.0)

*Plain-language version: before anything goes public under your name, you check it. Tick each box and write the date. Part 3 is the largest piece. The rest takes about 2 hours.*

## Part 1: Make sure the results can be rebuilt (15 to 30 min)

Pick one:
- [ ] **Option A: run it yourself.** In a terminal in the project folder, paste:
  `pip install pandas openpyxl matplotlib && python code/01_fetch.py && python code/02_build.py && python code/03_classify.py && python code/04_qa.py && python code/06_figures.py`
  The run ends by printing the headline numbers. A fresh download reflects the registry on the day you run it, so expect small differences from the numbers below. To reproduce them exactly, skip `01_fetch.py` and use the archived 13 October 2026 download.
- [ ] **Option B: ask Claude.** In a new chat with Opus 5.5 or Fable 5, upload the project and say: "Re-run this pipeline from the archived download and give me the headline numbers." Compare them against these:
  - 3,881 records fetched
  - 2,834 in scope
  - 1,914 completed
  - 337 terminated
  - 122 withdrawn
  - 468 stopped trials classified, of which 151 are poor enrollment

Then:
- [ ] Every number in the README and the figures matches `report/stats.json`. (The quality report's own counts are in `data/processed/qa_counts.json`.)

## Part 2: Check the source terms (10 min)

- [ ] Open https://clinicaltrials.gov/data-api/api. The page loads and the data is free to use.
- [ ] The registry's terms (https://classic.clinicaltrials.gov/ct2/about-site/terms-conditions) and NLM's general terms (https://www.nlm.nih.gov/databases/download/terms_and_conditions.html) ask users to do four things. They must credit the source, describe any changes made to the data, show the date the data were processed, and not suggest that NLM endorses the work. The README's Source section does all four. It uses the wording "Courtesy of the U.S. National Library of Medicine", gives the access date, points to the coding rules, and states that the dataset is not an NLM product and is a dated snapshot. Read it and confirm.

## Part 3: The 10 percent hand check (about 9 to 10 hours, over several sittings)

- [ ] Open `report/handcheck_form.xlsx` and follow its Instructions tab for all 284 trials. Pick each answer from the dropdown list in the yellow cells. The Codes tab shows which code matches each wording on the website.
- [ ] When you're done, the Summary tab shows the agreement rate for each field. Send Claude the file. If any field is below 95 percent agreement, the rule behind it is fixed and the pipeline rerun before release.
- [ ] Once the hand check is done, its agreement rates are added to the README.

## Part 4: Spot checks of extremes and of the 26 October fixes (20 min)

In `data/processed/ledger.csv`:
- [ ] Largest trial: **NCT01764633**. `enrollment_reported` is 27,564 and `site_count` is 1,284. Check at https://clinicaltrials.gov/study/NCT01764633.
- [ ] **NCT02271230** lists 25,871 enrolled at a single site. That is unusual, so confirm both numbers at https://clinicaltrials.gov/study/NCT02271230.
- [ ] **NCT01991795**. `site_count` is 1,237, of which 295 are in the US. Check the Locations section.
- [ ] **NCT05889156** ("High Triglycerides") is now in the ledger, under dyslipidemia.
- [ ] **NCT01030861** (teplizumab in at-risk relatives) is now out. It appears in `data/processed/scope_borderline.csv` as prediabetes.

## Part 5: Your decisions (10 min)

Confirm each one or change it:
- [ ] A US trial means at least one US site. (13 Oct)
- [ ] Hypertension excludes pulmonary, ocular, portal and intracranial hypertension. (13 Oct)
- [ ] The enrollment ratio is computed only for completed and terminated trials with an actual count. (13 Oct; applies from v1.1)
- [ ] There are six stop-reason groups, with the priority order in CODING_RULES.md. (13 Oct)
- [ ] Borderline trials are left out: diabetes complications, prediabetes, and surgical blood-pressure spikes. (13 Oct)
- [ ] Market withdrawal counts as safety only when a risk is stated. Stopping for benefit counts as other. COVID-19 alone counts as design or logistics. (13 Oct)
- [ ] The new condition wordings in C1, C2 and C5 are correct, and so are the widened prediabetes rule and the prevention-trial rule, B2 and B2t. (26 Oct) In particular, two added trials are judgment calls:
  - NCT03411902 is a bone-health drug given to bariatric surgery candidates. Its listed conditions include "Weight Loss".
  - NCT01041521 is omega-3 in people with HIV. Its listed conditions include "High Triglyceride Level".
- [ ] Weight gain caused by other medicines or by quitting smoking is not counted as obesity. (26 Oct)
- [ ] The 85 flagged stop reasons in `data/processed/stop_reason_review.csv` are reviewed, with any changes written in the author_ruling column.

## Part 6: Before it goes public (15 to 30 min)

- [ ] The README summary is in your own words. Edit it if it doesn't sound like you.
- [ ] Your name, ORCID and affiliation are correct in `AUTHORS.json`. Your email will appear in the public files. Change it there if you prefer a different one.
- [ ] You have read `docs/LIMITATIONS.md` and agree with it.
- [ ] The publish check script passes.

**When every box is ticked, reply to Claude in your own words that you have checked the package and approve publishing.**
