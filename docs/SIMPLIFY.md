# OpenHealth — Simplify: Your Data In, Trials Out

> **Decision doc.** Written 2026-10-06, 20 days before the Congressional App Challenge
> deadline (**Monday, October 26, 2026, 12:00 PM ET**), 12 days before feature freeze.
>
> It supersedes parts of [`REBUILD.md`](REBUILD.md) — which is still correct about the
> wedge and the rubric, and is still the doc to read first. This one answers a different
> question: *the app currently assumes you already know what condition to search for, and
> it is full of screens that are clickable but not real — so what is the smallest version
> that is 100% functional?*
>
> Every reversal below names the line it reverses.

---

## 1 · The standard this doc is written to

One sentence, set by the project owner on 2026-10-06:

> **Everything has to be functional — not just clickable, but actually real. The only
> accepted limitation is that there is no backend.**

That is a harder bar than "it demos well," and it is the right one, because the Function
sub-criterion is scored on a scale where **3 is "works with errors"** and **2 is "contains
snippets of code/action."** A screen that looks like it does something it does not do is
not a 4. It is a liability in the Q&A.

Applying that standard honestly to the current build produces the cut list in §4.

---

## 2 · The inversion — the app stops asking what you have

**Today:** the user is assumed to know their condition; the trial side is organized around
searching for it.

**From now on:** there is **no condition input anywhere in the app.** You give it your lab
documents and your watch data. It builds a profile and ranks every trial it knows about
against that profile, then tells you which ones you might qualify for and exactly why.

This is the single biggest simplification available, and it is also a competitive claim
that holds up. Every consumer-facing matcher named in [`REBUILD.md`](REBUILD.md) §4 —
ResearchMatch, Antidote Match, TrialJectory — **opens with a questionnaire.** The patient
self-reports, in medical vocabulary, before the tool does anything. That is a real barrier
for exactly the patient who most needs the tool: the one who does not yet know the name of
what they have.

> **OpenHealth's opening screen asks for a document, not an answer.**

It also removes an entire class of fake: there is no condition dropdown to populate with
plausible-looking options the engine cannot actually serve.

---

## 3 · The product, after simplification

A **clinical-trial matcher wrapped in a health hub** — matching is the product, the hub is
how you live in it between results. Three tabs, per the 2026-10-06 homepage design:

| Tab | What it is |
|---|---|
| **Home** | Health Score ring, top biomarkers, today's captures, and your single best trial match |
| **Metrics** | The biomarker detail — values, reference ranges, trends over time |
| **Trials** | Ranked matches, each opening into the per-criterion audit. **Still the product** |

```
INPUT  (keyless, client-side, no condition question)
  ├─ Documents → Tesseract.js OCR → PARSER → { analyte, value, unit, date }
  └─ Garmin    → local sync script → garmin.json → vitals + 30-day trends
                        │
                        ▼
PROFILE — normalized to FHIR R4 / US Core shapes, LOINC-coded
          (the format is real; the server call is cut; the synthetic patient is cut)
                        │
                        ▼
ENGINE
  ├─ Health Score   = biomarkers in range, weighted (§6)
  └─ PARSER reads the raw eligibilityCriteria TEXT of ~20–25 real trials
     → predicates → evaluator → PASS / FAIL / UNKNOWN / NEAR-MISS
     → ranks all of them. No search box. No condition.
                        │
                        ▼
OUTPUT
  ├─ Per-criterion audit — rule, your value, verdict, by how much
  ├─ Near-miss + Garmin trend — "ferritin short by 2, resting HR up 3 weeks"
  └─ Appointment prep sheet — a real file you download and take to a real doctor
```

---

## 4 · What gets deleted, and why

Each of these fails the §1 standard. None of them is a small loss; all of them are
necessary.

### 4.1 · The doctor-send flow — **deleted**

`index.html` has a send-to-clinician screen, and [`CLAUDE.md`](../CLAUDE.md) currently
specifies *"Doctors Available: 9"* on it as though it were a requirement.

**There are no doctors.** There is no inbox, no clinician, no 24-hour review by Dr. Chen.
It is the most fake thing in the build, and it is the first thing a judge would ask to see
working.

**Replaced by something that is real:** an **appointment prep sheet**. The app generates an
actual downloadable one-page summary — every criterion you failed, every near-miss with the
exact numeric gap, your values with their dates, and the NCT numbers — that you take to an
appointment you book yourself. Nothing is simulated. The file really exists.

> OpenHealth does not talk to your doctor. It gets you ready to.

That sentence is also the correct answer to the ethics question in the judging Q&A, and it
is stronger than the fake inbox was.

### 4.2 · The synthetic patient — **deleted**

Jordan Reyes, age 34, BMI 22.4, goes. **This reverses the line in
[`CLAUDE.md`](../CLAUDE.md) §"Efficiency notes"** that names the synthetic patient as a
fixture, and it retires the hardcoded `PROFILE` object in `index.html`.

The profile is now built from the operator's own real documents and own real watch data.
The confusing demo sentence — *"connect to a public test server and match a synthetic
stranger"* — disappears entirely.

**A1c stays absent, and stays load-bearing.** It was the UNKNOWN test case under the
synthetic patient and it remains one under real data, for the ordinary reason that a
healthy 2026 lab panel often does not include one. The engine must still refuse to treat a
missing value as a pass. That rule does not change; only where the gap comes from changes.

### 4.3 · The FHIR server call — **cut, format kept**

**This reverses item 6 of [`REBUILD.md`](REBUILD.md) §8.** No `fetch()` to
`r4.smarthealthit.org`.

What survives, and it is the part that was always worth having: the profile is still
**normalized into FHIR R4 / US Core resource shapes with LOINC codes.** A ferritin reading
is still `{ code: "2276-4", valueQuantity: { value, unit } }` whether it came from a photo
of a printout or a watch export.

The on-camera line changes from *"I connect to a real FHIR server"* to the more defensible:

> **"Everything I extract is normalized into FHIR R4 with LOINC codes — the format every
> certified EHR in the country is legally required to expose. That is why this profile
> would drop straight into a real patient-access API."**

The standard is still real and still federally mandated. The claim is now about the shape
of the data, which is true, rather than about a sandbox call, which was always the weakest
real thing in the app.

### 4.4 · Live ClinicalTrials.gov search — **cut, parser kept**

**This takes the first cut named in [`REBUILD.md`](REBUILD.md) §8** — "fall back to the ~20
saved real trials; criteria are still real, search is not live."

**The critical detail, and the easiest thing to get wrong:** cutting live search must not
cut the parser. Today `index.html` stores criteria as hand-written rule objects
(`{ key:'ferritin', op:'<=', threshold:50 }`) with the original wording kept only as a
`source:` string for display. **That is the parser's job, done by hand.**

The corpus now stores the **raw `eligibilityCriteria` text verbatim**, exactly as
ClinicalTrials.gov returned it, and the app parses it **at runtime, on load, in front of the
judge.** Same zero network calls, same offline reliability — but the free-text→predicate
code actually executes, which is where the Function and Code points live.

> *"These are cached real API responses. At one user I would query live; at a thousand I
> would mirror nightly."* — [`ARCHITECTURE.md`](ARCHITECTURE.md) §2 already contains this
> reasoning and it is unchanged.

---

## 5 · The two input rails, and why both are keyless

[`STACK.md`](STACK.md) §6a holds: **no API key in client-side JavaScript.** The reason is
not that we lack a key — it is that a key in a published static page is readable by anyone
who opens View Source. Making one safe requires a proxy, which is a server, which §1
excludes. Both rails below are built so that no key is ever shipped.

### 5.1 · Documents — OCR in the browser

`Tesseract.js`, loaded from a CDN, runs OCR entirely client-side. The extracted text goes
into **the same parser** that reads trial criteria. A lab printout and an eligibility
criterion are the same computational problem: free text in, `{ analyte, comparator, value,
unit }` out.

**This is the efficiency argument for the whole pivot.** One parser, three consumers:
trial criteria, scanned documents, and the Garmin snapshot. The 4 days budgeted for it in
[`REBUILD.md`](REBUILD.md) §8 now buy two features instead of one.

Known limitation, to be stated rather than hidden: OCR on a clean PDF or a flatbed scan is
reliable; OCR on an angled phone photo of a creased page is not. The app shows what it
extracted, with the confidence, and lets the user correct it before it enters the profile.
That is the §6 "never hide what you could not parse" rule applied to the input side.

### 5.2 · Garmin — a local sync script, not a backend

The official Garmin Health API needs partner-program approval, OAuth 1.0a request signing
and a webhook endpoint you host; multiple sources also report the Connect Developer Program
is currently closed to new signups. [`cyberjunky/python-garminconnect`](https://github.com/cyberjunky/python-garminconnect)
is the practical alternative, but it is **Python**, it authenticates with an account email
and password, and it prompts for MFA. None of that can run in a browser.

**It does not have to.** The data does not need to be live — refreshed every few days is
enough for biomarkers that move on the scale of weeks.

```
  Operator's laptop, every few days          The published app
  ┌───────────────────────────────┐          ┌──────────────────────────┐
  │  python-garminconnect         │          │  reads garmin.json       │
  │   → resting HR, SpO2, HRV,    │  commit  │  no key · no CORS        │
  │     sleep, body composition   │  ──────► │  no network · no server  │
  │   → writes garmin.json        │          │  works offline on stage  │
  └───────────────────────────────┘          └──────────────────────────┘
       credentials never leave
       the operator's machine
```

This is a **build-time data pipeline, not a backend.** Nothing listens on a port, nothing is
deployed, nothing costs money. The app reads a committed static file.

| §1 requirement | How this satisfies it |
|---|---|
| Real data | The operator's actual Garmin account. Not invented |
| No key in client JS | Credentials live only on the operator's machine, never shipped |
| No backend | Nothing serves requests; the app reads a static file |
| Demo-proof | If Garmin changes auth on Oct 24 and the script breaks, the last snapshot still loads and the demo is unaffected |

It also adds a second language to the submission, which the Code sub-criterion rewards.

**Privacy note, because this is a co-shared repo:** `garmin.json` contains the operator's
real resting heart rate, sleep and SpO2, committed in the clear and visible to
collaborators. That is an accepted, deliberate decision — it is the operator's own fitness
data, not patient data, and [`README.md`](../README.md) says so plainly so no collaborator
is surprised. The rule in [`CLAUDE.md`](../CLAUDE.md) — *never use real patient data* — is
unchanged and still absolute. The operator's own voluntarily-contributed watch data is not
patient data.

### 5.3 · What Garmin data is actually for

Watch metrics and lab-based eligibility criteria barely overlap, so this has to be answered
rather than assumed. It has two jobs:

1. **Direct profile input where criteria allow it.** SpO2, BMI, body composition, resting
   heart rate and activity level do appear in real eligibility criteria, particularly in
   cardiopulmonary and metabolic trials. Where a criterion asks for one, the watch answers
   it, and the audit cites the watch as the source.
2. **Trend context on near-misses — the distinctive output.** A lab value is one point in
   time; the watch is a line. *"Ferritin 8 ng/mL, needs ≥10 — short by 2. Your resting heart
   rate has risen for three straight weeks. Worth asking about a re-test."* No existing
   matcher shows this, because no existing matcher has both halves.

Job 2 is the one to protect if time runs short. It is what makes the near-miss callout — the
most distinctive thing in the app — sharper than anyone else's.

---

## 6 · The Health Score, defined

The homepage hero is a ring reading **89**. A number that large and that central has to be
defensible, or a judge reads it as decoration.

**Definition: the weighted share of your tracked biomarkers that sit inside their reference
range, with partial credit for near-range values.**

```
for each tracked marker m with reference range [lo, hi] and value v:
    in range                → 1.0
    outside by d            → clamp(1 − d / (hi − lo), 0, 1)     // partial credit
    no value                → EXCLUDED from the score entirely

HealthScore  = round(100 × Σ(weight_m · score_m) / Σ(weight_m))   // over markers WITH values
Confidence   = "n of N markers"                                   // how much you actually have
```

Two rules carried over from [`REBUILD.md`](REBUILD.md) §6, because they are what makes the
number honest:

1. **A missing marker never counts as a pass.** It is excluded from the score and lowers the
   *confidence* instead. The ring reads `89` with `6 of 8 markers` beneath it — never a
   silent 89 computed from whatever happened to be available.
2. **Score and confidence are two numbers.** Exactly as on the trial side. The same rule,
   applied in two places, is also a much better answer to "explain your code" than two
   unrelated formulas would be.

**The Health Score is not a diagnosis and not a fitness grade.** It is a legibility
statement: how much of your measurable picture is currently where it is supposed to be.
Every bar beneath the ring clicks through to the Metrics detail, and the score is never
used as an input to trial matching — the engine reads the underlying values directly.

---

## 7 · Build order for 12 days to freeze

Feature freeze is still **Saturday, October 18**. The video and submission still own the
final week, and nothing is submitted into a noon cutoff — submit by **Oct 25**.

| # | Work | Days | Why here |
|---|---|---|---|
| 1 | **Criteria parser** — free text → predicates, with an `unparsed` bucket | 4 | The core CS, still unbuilt, and now it pays for two rails. Build against the saved corpus so it is testable offline |
| 2 | Re-wire the evaluator to consume parsed predicates | 1 | `evaluateCriterion` / `matchScore` already work; they just need to read the parser's output instead of hand-written objects |
| 3 | Trial corpus — ~20–25 real trials, raw `eligibilityCriteria` saved verbatim | 1 | Must exist before #1 can be tested honestly |
| 4 | Document rail — Tesseract.js → parser → profile, with user correction | 2 | The headline input, and the one that removes the condition question |
| 5 | Strip-out pass — doctor flow, Jordan Reyes, condition input, `Doctors Available: 9` | 0.5 | Cheap, and every day it stays is a day the demo can be caught out |
| 6 | Hub shell — 3-tab nav, Health Score, Metrics tab | 1.5 | The 2026-10-06 homepage design |
| 7 | Garmin rail — sync script, `garmin.json`, reader, trend on near-miss | 1.5 | Real, but it is the rail the app can survive without |
| 8 | Appointment prep sheet — real generated download | 1 | The distinctive output and the ethics answer |

**≈ 12.5 days against 12.** It is tight by half a day, which is the correct amount of tight
this close in.

**If something slips, cut in this order:** 8, then 7, then 6. **Never cut 1, 2, 3, or 4** —
they are the app. Cutting 7 costs the Metrics tab its best content; cutting 6 means shipping
the existing three screens with the new engine behind them, which is a perfectly respectable
fallback and loses no functionality at all.

---

## 8 · What changes in the other docs

| Doc | Change |
|---|---|
| [`CLAUDE.md`](../CLAUDE.md) | Delete `Doctors Available: 9`. Delete the Jordan Reyes fixture. Replace the three-screen description with the three-tab hub. Add the no-condition-input rule and the keyless-rails rule |
| [`README.md`](../README.md) | Rewrite "The three screens". Add the `garmin.json` privacy note for collaborators. Update what is real vs. synthetic |
| [`BRIEF.md`](BRIEF.md) | §3 Input/Processing/Output rewritten around the two rails. §"The synthetic patient" deleted — nothing in the app is a synthetic person any more. The §6 innovation claim becomes the §2 inversion |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | §2 collection layer rewritten for two rails. §4a parser contract extended to cover OCR text as a second input. §8 prototype map updated. §2's live-vs-mirror reasoning is **unchanged and still correct** |
| [`STACK.md`](STACK.md) | §6a strengthened: a key we *have* is as unusable as a key we lack, for the same reason. Add the §5.2 pipeline as the pattern for "real data without a server" |
| [`BUILDSPEC.md`](BUILDSPEC.md) | Screens re-specified as tabs. Per-criterion audit table is unchanged and is still the hero |
| [`ROADMAP.md`](ROADMAP.md) | Weeks 2–3 replaced by §7. Cut list gains live search and the FHIR call, with the reversals named |
| [`MISSION.md`](MISSION.md) | Non-goals gain "we do not contact your doctor" and "we do not ask you what you have" |
| [`RISKS.md`](RISKS.md) | **No change needed.** It remains the hypothetical-company doc; #2 false hope and #9 model error still cover the parser |

---

## 9 · The three sentences this has to survive

A judge gets about three questions. These are the answers.

> **"What does it do?"** — You give it your lab paperwork and your watch data. It reads
> every trial's eligibility criteria, which are published as free text, turns them into
> checkable rules, and shows you which ones you pass, which you fail, and by exactly how
> much. You never tell it what you have.

> **"What's real?"** — The trials and their criteria are real records from
> ClinicalTrials.gov. The lab values are read off real documents. The vitals are from a real
> Garmin account. The data format is FHIR R4 with LOINC codes, which every certified EHR is
> legally required to expose. There is no server, so there is nothing to take my word for —
> the whole thing runs in the page.

> **"What doesn't it do?"** — It does not decide whether you are eligible. Eligibility is
> determined at a screening visit by a clinician. It does not contact your doctor; it
> prepares the sheet you take to one. And it shows you the criteria it could not parse
> instead of hiding them, because a tool that silently drops a third of the rules and shows
> you a confident number is lying to you.

---

## 10 · Sources

Garmin Health API access requirements and the suspended developer program —
[openwearables.io Garmin API integration guide](https://openwearables.io/docs/providers/garmin-api-integration.md),
[Garmin Connect API developer guide](https://openwearables.io/blog/garmin-connect-api-developer-guide-activities-health-metrics).
Unofficial client — [`cyberjunky/python-garminconnect`](https://github.com/cyberjunky/python-garminconnect),
[garminconnect on PyPI](https://pypi.org/project/garminconnect/).
Judging rubric, field size, consumer-matcher landscape and screen-failure literature — all
carried forward from [`REBUILD.md`](REBUILD.md) §10, unchanged.
