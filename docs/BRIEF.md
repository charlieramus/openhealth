# OpenHealth — Project Brief

> The single source of truth for **what OpenHealth is** and **why**. The prototype,
> the poster, and the Congressional App Challenge video all draw their content from
> this file. If a fact about the concept changes, change it here.

---

## The problem

The US healthcare system scatters a patient's data across 5+ separate portals — one per
hospital, lab, insurer, and pharmacy. No one place shows the whole picture. Two things
break because of this:

1. **Patients can't see their own health clearly.** Labs live in one portal, bills in
   another, prescriptions in a third.
2. **Patients can't tell what they qualify for.** Trial eligibility is published as free
   text full of numeric thresholds. Consumer matching tools do exist — ResearchMatch,
   Antidote Match, TrialJectory — but they ask a questionnaire and return a list. **None
   shows the patient the per-criterion arithmetic**, so a patient can't see that they missed
   by 2, or which number to ask their doctor about. The clinically deep tools (MatchMiner,
   TrialMatchAI) are B2B and sold to hospitals and pharma.

The cost of that opacity is measurable: **40–60% of patients who begin formal screening are
rejected** (70–80% in oncology, rare disease and CNS), and conservative numeric biomarker
thresholds are a leading cause — patients who fell just outside a window at the moment they
happened to be measured.

## The idea

OpenHealth puts a patient's health record and the clinical-trial registry in the same place,
then does the thing no consumer app does: it **reads each trial's eligibility criteria —
published as unstructured free text — turns them into checkable rules, and evaluates them
against the patient's actual lab values, one criterion at a time.**

The "whoa" moment is not a number. It is the **audit**: a patient seeing *which* criterion
they fail, against *which* threshold, by *how much* —

> **Ferritin 8 ng/mL · trial needs ≥ 10 · short by 2.**
> *Worth asking your doctor whether that's worth re-testing.*

— and then sending that question to a doctor in one tap.

Trial matchers already exist for patients (see §6). What none of them show is the
arithmetic. **The arithmetic is the product.**

---

## The six required deliverable elements

These map directly to the class rubric (and cover the CAC video talking points).

### 1. App name + problem
**OpenHealth.** Clinical-trial eligibility criteria are published as free text full of
numeric thresholds, so patients can't tell what they qualify for — and **40–60% of patients
who start formal screening are rejected**, frequently on a single biomarker threshold they
fell just outside of.

### 2. Three-screen prototype
**Home → Metrics → Trials**, as a three-tab hub. (See `DESIGN.md` / `BUILDSPEC.md`, live at
the URL in the README.)

### 3. Input → Processing → Output
**The user is never asked what condition they have.** There is no search box and no
condition dropdown anywhere in the app. That is the central design decision — see
[`SIMPLIFY.md`](SIMPLIFY.md) §2.

- **Input** — Two rails, both keyless and both running entirely in the browser.
  **Documents:** the user photographs or uploads lab paperwork; `Tesseract.js` OCRs it
  in-page and the parser extracts `{ analyte, value, unit, drawnOn }`. **Vitals:** a local
  Python script pulls the operator's own Garmin data every few days and commits
  `garmin.json`, which the app reads as a static file. Both are normalized into **FHIR R4 /
  US Core shapes with LOINC codes** — the standard every certified US EHR is federally
  required to expose.
- **Processing** — Real recruiting trials are stored with their **raw inclusion/exclusion
  text exactly as ClinicalTrials.gov published it**. The same parser turns each criterion
  into a checkable rule (`{ analyte, op, threshold, unit }`) **at runtime**, an evaluator
  returns **pass · fail · unknown · near-miss** per rule, and a weighted sum produces a
  0–100 score with a **separate confidence** figure for how much of the criteria set was
  machine-checkable. Every trial is ranked; none is filtered out by a condition the user
  typed.
- **Output** — Ranked trials, each with a **per-criterion audit table** (the rule, the
  user's value, the verdict), near-miss callouts enriched with the watch's trend over time,
  the criteria the parser *couldn't* read shown plainly rather than hidden, the real NCT link
  — and a **downloadable appointment prep sheet** listing every failure and gap, to take to
  a real appointment. *The app never contacts a clinician.*

### 4. One benefit
A patient learns **why** — which specific number, against which specific threshold — instead
of getting a yes, a no, or a list. That turns a dead end into a specific question for a
specific doctor, and it is the near-misses that make it matter: being short by 2 is
actionable information, and no existing consumer tool surfaces it.

### 5. One unintended consequence
**Showing the exact threshold invites gaming it.** The near-miss feature is the app's best
idea and its most dangerous one: a patient told "your ferritin is short by 2" now knows
precisely what number to clear, and lab values can be nudged — time the draw, change
supplements beforehand. Someone enrolls who the criterion was written to exclude, which
corrupts the trial's data and can put that person at real risk.

The consequence is **structural, not a bug**: transparency about a threshold and the ability
to game that threshold are the same information. We can soften it — frame near-misses as
questions for a doctor rather than targets to hit, never suggest how to move a value, and
state that site screening is the real gate — but we cannot remove it without removing the
feature that makes the app worth building.

*(Secondary: a record this complete is a high-value target for attackers. Protections reduce
that risk; concentration itself is the consequence.)*

### 6. Why it's a computing innovation
**Not because it's the first patient-facing trial matcher — it isn't.** ResearchMatch
(NIH-funded), Antidote Match, and TrialJectory are all free and consumer-facing. Claiming
otherwise would be the easiest thing in this document for a judge to disprove.

The precise claim, which [`MARKET.md`](MARKET.md) §2 works out against each competitor:

> **Every product that matches a patient's actual clinical record against trial eligibility
> criteria sells to institutions. Every product that serves the patient directly either
> aggregates the record without matching it (Apple Health) or offers trial search without the
> record (Antidote, ClinicalTrials.gov). OpenHealth is the first to do both on the patient's
> side** — and the first to show the patient the per-criterion arithmetic either way.

What the consumer tools do is ask the patient a **questionnaire** and keyword-match the
self-reported answers — which requires the patient to already know, in medical vocabulary,
what they have. **OpenHealth asks for a document, not an answer.** And what none of them does
is **show the patient the computation**: parse the published
free-text criteria into machine-checkable predicates, normalize units so `8 ng/mL` and
`15 µg/L` can be compared at all, evaluate each predicate against a real lab value, and
report per-criterion pass/fail/unknown/near-miss with the numbers visible.

That is a text-to-predicate extraction problem over unstructured clinical prose, and it is
the innovation: the app is **auditable**. A patient can check its work, and so can their
doctor. It reports what it *couldn't* parse instead of hiding it, and it keeps **score
separate from confidence** so an unknown never masquerades as a pass.

---

## What is real and what is synthetic

**The line to hold, in the video and everywhere else:**

> **The trials are real. The lab values are read off real documents. The vitals are from a
> real watch. The data standard is real and federally mandated. There is no server, so there
> is nothing to take my word for — the whole thing runs in the page.**

| Layer | Status |
|---|---|
| **Trials** | **Real.** ClinicalTrials.gov records — real NCT IDs, real sponsors, real inclusion/exclusion text, saved verbatim and parsed at runtime |
| **Data standard** | **Real.** FHIR R4 / US Core shapes with LOINC codes, which the 21st Century Cures Act requires every certified EHR to expose to patients. The *format* is used; the server call is cut |
| **Lab values** | **Real.** OCR'd in-browser from actual lab documents, with what was extracted shown for correction before it enters the profile |
| **Vitals** | **Real.** The repo owner's own Garmin account, pulled by a local script into a committed `garmin.json`. Their own fitness data, voluntarily contributed — **not patient data** |
| **Patient data** | **Never real.** A permanent rule, not a roadmap item |
| **Every score on screen** | **Computed**, not authored. Change a lab value and the score, verdict, bars and ranking all follow |

**Cut on 2026-10-06, and not to be reintroduced:** the synthetic patient, the FHIR server
call, live registry search, and the send-to-doctor flow. Each failed the standard that
everything in the app has to be actually real, not merely clickable. See
[`SIMPLIFY.md`](SIMPLIFY.md) §4.

### The profile

There is **no synthetic patient any more.** Jordan Reyes is retired, along with the
presentational "18 updates from 5 providers", the insurance balance, and the 9 doctors on a
care team. All of it described things the app did not do.

The profile is built at runtime from whatever the two rails actually extracted. The only
fixtures that remain are the **reference ranges** and the **marker colors**:

| Marker | Reference range | Color |
|---|---|---|
| Iron (Ferritin) | 12–150 ng/mL | magenta |
| Hemoglobin | 12–16 g/dL | purple |
| Oxygen saturation | 95–100 % | teal |
| LDL cholesterol | target < 100 mg/dL | blue |
| **A1c** | **Expected to be absent.** A routine panel often omits it. This is the UNKNOWN case, and the engine has to cope rather than assume a pass. Worth 15 seconds of the video | — |

Colors are straight from the marker colors in the hand-drawn mockups and are used everywhere.
The Health Score ring on the home screen is amber/orange and is **computed** — see
[`SIMPLIFY.md`](SIMPLIFY.md) §6 for the formula.

### Known stale values — fix before the video

| Where | Problem |
|---|---|
| `index.html` home health score | Still a hardcoded literal. Must be replaced by the computed Health Score in [`SIMPLIFY.md`](SIMPLIFY.md) §6, with its `n of N markers` confidence line |
| `index.html` criteria objects | `criteria:[{ key, op, threshold }]` is the parser's job done by hand. Must be replaced by raw `eligibilityCriteria` text parsed on load |
| `index.html` doctor flow | The send-to-clinician screen and "Doctors Available: 9" must be deleted outright, not restyled |
| Scores in any doc or mockup | "CGX Trial #4 — 87/100" is gone, and so are "89" and "79/100" from the 2026-10-06 homepage design. The app's real scored trials are **Iron Revisited** (`NCT06942208`) and **Icovamenib in Type 2 Diabetes** (`NCT07502508`); scores and the Health Score are engine output and change with the profile, so **do not quote either as a constant anywhere** |

---

Every claim in this document that cites a number or an existing product is sourced in
[`REBUILD.md`](REBUILD.md) §10. The screen-failure figures and the list of existing consumer
matchers in particular — quote them from there, not from memory.
