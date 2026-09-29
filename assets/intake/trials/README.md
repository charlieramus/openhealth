# intake/trials — ClinicalTrials.gov primary sources

The four clinical trials in the prototype, as the registry returned them on
**2026-09-29**. These are the authority behind every threshold in the matching engine in
[`index.html`](../../../index.html).

**Intake rule applies: do not edit these.** They are what the registry gave us. If a record
changes upstream, download the new one alongside the old and date it — don't overwrite.

Each file is the unmodified JSON response from:

```
https://clinicaltrials.gov/api/v2/studies/<NCT ID>
```

| File | Study | Sponsor | Used as |
|------|-------|---------|---------|
| `NCT06942208.json` | Iron Revisited — alternate-day oral iron in female athletes | University of Calgary | The strong match (scores **79**) |
| `NCT07502508.json` | Phase 2 trial of icovamenib in type 2 diabetes | Biomea Fusion, Inc. | The weak match (scores **21**) |
| `NCT07225998.json` | Oral N-acetylglucosamine in Crohn's disease | Johns Hopkins University | Screening-soon row |
| `NCT07729332.json` | Oral weight management after GLP-1 discontinuation | Massachusetts General Hospital | Screening-soon row |

## Why these four

The patient profile is a 34-year-old woman with **iron deficiency but not anemia** —
ferritin 8 ng/mL with hemoglobin still at 13.1 g/dL. Most iron trials require established
anemia (Hb ≤9 or <12), so she genuinely fails them. NCT06942208 is the one that fits: it
enrolls on low ferritin and *excludes* anemia. Nothing was adjusted to make her match.

The diabetes trial is in the feed deliberately. Its nearest site is 138 mi away against the
iron trial's 2,006 mi, and it still scores 21 — distance is not what decides a match.

## What the engine takes from each record

Only numeric, checkable facts:

- `eligibilityModule.eligibilityCriteria` → the inclusion/exclusion line each criterion
  quotes in its `source` field
- `eligibilityModule.minimumAge` / `maximumAge` → the age criterion
- `identificationModule.nctId`, `sponsorCollaboratorsModule.leadSponsor` → shown on screen
- `designModule.phases`, `enrollmentInfo.count` → the tags and the trial-details rows
- `contactsLocationsModule.locations[].geoPoint` → great-circle distance from the (invented)
  patient's home city of Philadelphia, PA to the nearest real site

Travel distance is OpenHealth's own filter, not a trial requirement. It is marked
`protocol:false` in the code, is never `required`, and never blocks eligibility.

## Verifying a claim

Any number on screen 3 can be checked in about ten seconds — the NCT ID is displayed in the
match hero. Paste it into [clinicaltrials.gov](https://clinicaltrials.gov) and compare, or
diff the live API response against the file here.
