# Limitations

*Plain-language note: what this dataset can and cannot tell you. Read this before quoting any number from it.*

1. **No planned enrollment in v1.0.** When a trial reports its final count, the registry replaces the planned figure with the actual one. So v1.0 cannot say how far short of target a trial fell. v1.1 recovers planned enrollment from AACT archived snapshots, which will not cover every trial (see NEXT_STEPS.md).
2. **A snapshot, not a history.** Every value is as shown on the access date in `data/raw/PROVENANCE.txt`. Sponsors can and do edit records later, and a trial listed as recruiting may since have stopped.
3. **Stop reasons are the sponsor's own words.** They are often brief, vague or diplomatic. "Business decision" may hide slow enrollment, and 71 of 468 stopped trials (15 percent) give no usable reason. The six groups classify what was *stated*, not what actually happened.
4. **One group per trial.** When a reason mentions several causes ("low enrollment and lack of funding"), a fixed priority order picks one. All matching groups are kept in `stop_categories_all` so others can apply a different order.
5. **Rule-based text matching.** Both the condition rules and the stop-reason rules use written word patterns, not an expert reading of each record. The 10 percent hand check estimates how often they get it wrong. The rules were tightened on 26 October 2026 after a review found 13 missed wordings and 17 prevention trials wrongly included. Other gaps of this kind may remain.
6. **Scope follows the listed conditions.** A trial is included when one of the conditions its sponsor listed names one of the five diseases, in any of the wordings in CODING_RULES.md. A trial that lists only another disease is not included, even if its participants have one of the five. Examples are a cholesterol drug listed under "Atherosclerotic Cardiovascular Disease" and a blood-pressure drug listed under "Chronic Kidney Disease". `data/processed/scope_index_crosscheck.csv` lists the 244 out-of-scope trials that the registry's own disease index links to one of the five areas, with the reason each is out. Readers who want a broader definition can start there.
7. **"US trial" means at least one US site.** Large multinational trials are included, and their enrollment and site counts are global, not US-only.
8. **Registry coverage.** Not every trial is registered, and the rules on registration and reporting have changed since 2008. Early years may be less complete.
9. **Status UNKNOWN.** 60 trials have status Unknown, meaning they were not updated after their expected end date. They are kept but cannot be classified as completed or stopped.
10. **Site counts depend on what sponsors list.** Some trials list only a few sites or remove sites over time.
