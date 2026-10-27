# Next steps

*Plain-language note: what each version of the ledger contains, and what the next one adds.*

## v1.0 (November 2026)

One row per trial, with: conditions and disease areas, phase, sponsor class, site counts (total and US), status, key dates, actual enrollment, and the stop-reason group with the rule that assigned it.

The planned-enrollment and enrollment-ratio columns are included but left empty in v1.0. ClinicalTrials.gov overwrites the planned number with the actual number when a trial reports its final count, so the current public record does not contain it. v1.1 restores it.

## v1.1 (December 2026)

- **Planned enrollment** recovered from AACT's archived monthly snapshots. AACT is the research copy of the registry run by Duke University and the Clinical Trials Transformation Initiative. For each trial, the planned figure is the last "anticipated" enrollment recorded before the count switched to "actual".
- **Enrollment ratio** (actual divided by planned), computed for completed and terminated trials that report an actual count.
- **Coverage report:** how many trials have a recovered planned figure, broken down by year of completion, so readers can see where the snapshots run out.
- Corrections from the 10 percent hand check, and its agreement rates per field.
- A short technical report describing the dataset and its headline numbers.

## Open items

- AACT account (author) and a test of how far back the snapshots go.
- Optional: ask ClinicalTrials.gov for bulk version history, as a cross-check for trials the AACT snapshots don't cover.
