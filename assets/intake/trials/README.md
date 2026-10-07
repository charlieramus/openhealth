# intake/trials — ClinicalTrials.gov primary sources

**23 real clinical trials**, as the registry returned them. The original four were
downloaded **2026-09-29**; the other nineteen on **2026-10-06**. These are the authority
behind every verdict the matching engine produces in
[`index.html`](../../../index.html).

**Intake rule applies: do not edit these.** They are what the registry gave us. If a record
changes upstream, download the new one alongside the old and date it — don't overwrite.

Each file is the unmodified JSON response from:

```
https://clinicaltrials.gov/api/v2/studies/<NCT ID>
```

## How these become the app's corpus

```
assets/intake/trials/*.json        scripts/build_corpus.py            index.html
  23 unmodified API responses  ──►  extracts the real fields,     ──►  var CORPUS = [...]
  (primary sources, never edited)   copies the criteria VERBATIM       inline, loaded at
                                    computes nearest-site distance     page load, no fetch
                                    from the registry's own geoPoint
```

Run `python scripts/build_corpus.py` after adding a record. It is a **build-time step, not
a backend** — nothing listens on a port, and the published artifact makes no network call.

**The corpus stores the raw `eligibilityCriteria` text and nothing resembling a predicate.**
No `{op, threshold}`, no pre-split bullets, no cleaned-up units, no corrected typos. Turning
that text into checkable rules is `parseCriteria()`'s job, done **by code, at runtime, in
front of the viewer**. A hand-structured corpus would be that job done by hand, which is
precisely what the 2026-10-06 rewrite set out to delete — see
[`SIMPLIFY.md`](../../../docs/SIMPLIFY.md) §4.4.

## The corpus

| NCT ID | Sponsor | Phase | Status | Condition | Age | Sex |
|---|---|---|---|---|---|---|
| `NCT04485871` | Institut de Recherches Cliniques de Montreal | NA | Recruiting | Type 2 diabetes, inflammation | 45–74 | All |
| `NCT05226169` | Asan Medical Center | 3 | Recruiting | Advanced gastric carcinoma | 19+ | All |
| `NCT05462704` | Women and Infants Hospital of Rhode Island | 3 | Recruiting | Iron deficiency anemia, pregnancy | 18–45 | Female |
| `NCT05614219` | Odense University Hospital | NA | Recruiting | Familial hypercholesterolemia | 18+ | All |
| `NCT05759078` | Wroclaw Medical University | 4 | Recruiting | Acute myocardial infarction | 18–90 | All |
| `NCT05856838` | University Hospital, Ghent | NA | Recruiting | Heavy menstrual bleeding | 35–50 | Female |
| `NCT06270498` | Raffaele De Caterina | 4 | Recruiting | Chronic heart failure, iron deficiency | 18+ | All |
| `NCT06422741` | Fundació Eurecat | NA | Recruiting | Cardiovascular disease, shift work | 18+ | All |
| `NCT06510998` | Chinese University of Hong Kong | NA | Recruiting | Hypertension | 18+ | All |
| `NCT06851130` | Swiss Federal Institute of Technology | NA | Recruiting | Iron deficiency without anemia | 18–45 | Female |
| `NCT06894004` | Washington University School of Medicine | NA | Recruiting | Hypercholesterolemia | 18–39 | All |
| `NCT06897475` | Eli Lilly and Company | 2 | Recruiting | Type 2 diabetes | 18–75 | All |
| `NCT06942208` | University of Calgary | NA | Recruiting | Iron deficiency | 16–35 | Female |
| `NCT06990373` | Hung Vuong Hospital | — *(observational)* | Recruiting | Iron deficiency without anemia | 18–45 | Female |
| `NCT07014371` | Phramongkutklao College of Medicine | NA | Recruiting | Iron deficiency anemia | 20+ | All |
| `NCT07225998` | Johns Hopkins University | 2 | Not yet recruiting | Crohn's disease | 18–80 | All |
| `NCT07394972` | Nicole Stoffel | NA | Recruiting | Iron deficiency without anemia | 18–45 | Female |
| `NCT07502508` | Biomea Fusion Inc. | 2 | Recruiting | Type 2 diabetes | 18–70 | All |
| `NCT07546591` | Lindenwood University | NA | Recruiting | Iron deficiency, low ferritin | 18–45 | Female |
| `NCT07588438` | Las Rías Medical Center | 4 | Recruiting | Obesity, type 2 diabetes | 18–70 | All |
| `NCT07729332` | Massachusetts General Hospital | 4 | Not yet recruiting | Obesity | 18–80 | All |
| `NCT07743983` | BrightGene Bio-Medical Technology | 3 | Recruiting | Type 2 diabetes | 18–75 | All |
| `NCT07775404` | AstraZeneca | 3 | Recruiting | Obesity, overweight | 18+ | All |

Phase is the registry's own value. An observational study has no phase, and the corpus
records that as empty rather than inventing an "N/A".

## Why these, and why not an easier set

**Picked for spread, not for wins.** A corpus of easy cases produces a parser that only
works on easy cases, and a ranked list where everything is a strong match reads as fake.
So the set is deliberately uneven:

| Group | Records | What it is there to prove |
|---|---|---|
| **Iron deficiency *without* anemia** | `NCT06942208`, `NCT07394972`, `NCT06851130`, `NCT07546591` | The profile's actual picture — low ferritin, hemoglobin still normal. These are the ones that should genuinely score well |
| **Iron trials that require established anemia** | `NCT07014371`, `NCT05462704` | The profile has hemoglobin 13.1 g/dL and **should fail them.** Nothing was adjusted to make it match |
| **Iron in a disease the profile doesn't have** | `NCT05226169`, `NCT05759078`, `NCT06270498` | Gastric carcinoma, post-MI, heart failure. Right analyte, wrong patient — these must fail on context, not on ferritin |
| **A1c-gated** | `NCT07743983`, `NCT06897475`, `NCT07588438`, `NCT07775404`, `NCT07502508` | **The standing UNKNOWN test.** A1c is deliberately absent from the profile, and the engine must return UNKNOWN, never a pass |
| **Lipids** | `NCT06894004`, `NCT06422741`, `NCT05614219`, `NCT04485871` | The profile has a real LDL. `NCT04485871` also fails cleanly on an age window of 45–74 |
| **Prose only** | `NCT05856838`, `NCT06510998`, `NCT06990373` | No analyte the engine knows. **Honest input for the `unparsed` bucket** — criteria the parser must surface verbatim rather than guess at or quietly drop |

Three of 23 records contain no analyte in the engine's vocabulary at all. That is on
purpose. A parser that never reports an unparsed criterion is not reading carefully — it is
hiding.

## What the engine takes from each record

Only real, checkable registry fields:

- `eligibilityModule.eligibilityCriteria` → **the raw text the parser reads**, and the
  wording the audit table quotes beneath every row
- `eligibilityModule.minimumAge` / `maximumAge` / `sex` → the demographic criteria
- `identificationModule.nctId`, `briefTitle` → shown on screen
- `sponsorCollaboratorsModule.leadSponsor`, `statusModule.overallStatus` → shown on screen
- `designModule.phases`, `enrollmentInfo.count`, `conditionsModule.conditions` → tags and
  the trial-details rows
- `contactsLocationsModule.locations[].geoPoint` → great-circle distance to the nearest real
  site

Travel distance is measured from a single documented location constant in
`scripts/build_corpus.py` (Philadelphia, PA). It is **OpenHealth's own filter, not a trial
requirement** — never `required`, and it never blocks eligibility. It is a map coordinate,
not a person: the synthetic patient was deleted on 2026-10-06 and nothing here replaces one.

## Verifying a claim

Any trial on screen can be checked in about ten seconds — the NCT ID is displayed in the
match hero. Paste it into [clinicaltrials.gov](https://clinicaltrials.gov) and compare, or
diff the live API response against the file here. The stored eligibility text was confirmed
byte-identical to the live registry response on 2026-10-06.
