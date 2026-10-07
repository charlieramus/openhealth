# OpenHealth

**Clinical trials hide who can join inside pages of medical fine print. OpenHealth reads it,
checks it against your real lab results, and shows you which number is keeping you out — and
by how much.**

OpenHealth is an interactive mobile-app prototype built for the **Congressional App
Challenge** (and a computing-innovation class project). Trial eligibility is published as
free text full of numeric thresholds, which is part of why **40–60% of patients who begin
formal screening are rejected** — frequently over a single biomarker value they fell just
outside of. OpenHealth turns those criteria into checkable rules, evaluates them against
your labs, and shows the per-criterion arithmetic.

**You never tell it what you have.** Every other consumer trial matcher opens with a
questionnaire — you self-report, in medical vocabulary, before the tool does anything.
OpenHealth opens by asking for a document. It reads your lab paperwork, builds a profile, and
ranks every trial it knows about against it. (Watch data is the second rail and is on the
plan, not in the app — see *What is real* below.)

**The trials are real, and so is everything else that ships.** The standard the project is
held to: *everything has to be functional — not just clickable, but actually real. The only
accepted limitation is that there is no backend.* Lab values are OCR'd from actual documents
in the browser. The trials are genuine [ClinicalTrials.gov](https://clinicaltrials.gov)
records, and the app parses their raw eligibility text at runtime rather than reading rules a
human pre-encoded.

### What is real, what is not, and what is not built yet

Stated plainly, because the difference is the project. Last walked end to end **2026-10-07**,
at the close of [`UPDATELOGV1.md`](UPDATELOGV1.md).

| | |
|---|---|
| ✅ **The criteria parser** | `parseCriteria()` turns a trial's published eligibility text into checkable rules **in the browser, at render time**. 460 rules across the 23 records. Every rule keeps the registry's own sentence in `source`; what it cannot read goes in an `unparsed` bucket shown verbatim on screen, never guessed and never dropped. This is the actual computer science and it is done |
| ✅ **The matching engine** | Every score on screen is computed by `matchScore()` from the profile against those parsed rules. Change a lab value and the scores, the bars and the ranking all move. There is **no** hand-written rule array left in the file, so there is no second score that can disagree with the first |
| ✅ **The trial records** | 23 genuine ClinicalTrials.gov records, downloaded 2026-10-06, stored with their eligibility text **verbatim** — original line breaks, bullets and typos. `scripts/build_corpus.py` asserts the text survives the round trip byte-for-byte |
| ✅ **The document rail** | Drop in a photo or scan of a lab report and Tesseract.js reads it on the device. Values are converted into each analyte's canonical unit; a unit with no conversion on file is **refused rather than read as a bare number**, and every refused line is shown to you with its raw text. Every row is editable before anything enters the profile |
| ✅ **Two numbers, never one** | Score and confidence are reported separately — *"100 / 100"* beside *"3 of 32 checkable"*. A missing value is `UNKNOWN`, which lowers confidence and **can never raise the score**. HbA1c is deliberately absent from the committed baseline as the standing test case for exactly that |
| ⚠️ **The baseline lab history is invented** | The seven committed draws the app opens with are not anyone's. The *rails* that replace them are real: read a document or type a value and it is yours from then on. Nothing in this repo is, or has ever been, real patient data |
| 🔨 **The three-tab hub** | The tabs today are **Home · Labs · Trials**. The Metrics tab is `UPDATELOGV2.md` |
| 🔨 **The Garmin rail** | **Not built.** There is no `garmin.json` and no sync script in this repo yet. `UPDATELOGV2.md` |
| 🔨 **The appointment prep sheet** | **Not built.** The app currently produces no downloadable file at all, which is why there is no download button anywhere. `UPDATELOGV2.md` |

**Start with [`docs/SIMPLIFY.md`](docs/SIMPLIFY.md)** for the current plan, what got cut and
why, then [`docs/REBUILD.md`](docs/REBUILD.md) for the API evidence the whole thing rests on.

### What leaves your device

Nothing you give it. The document is read by a worker on the page and is never uploaded;
`index.html` contains no `fetch`, no `XMLHttpRequest`, no `sendBeacon`, no `WebSocket`, no
`<form>` and no `mailto:`. Nothing is stored either — there is no `localStorage` and no
IndexedDB for your data, so closing the tab is the delete button.

There are exactly two inbound requests, and neither carries anything of yours: the Google
Fonts stylesheet at page load, and — **only when you read your first document** — the
Tesseract.js bundle from one CDN. Verified 2026-10-07 with both hosts unreachable: the app
renders and scores normally on fallback fonts, and the document rail says it is offline and
hands you the typing path, which works. So the accurate claim is *"nothing you give it ever
leaves the device,"* not *"there are no network calls."*

---

## ▶ See it live

**Prototype:** https://claude.ai/artifact/5H4KWf2bja3DKDydumaqyo

Open it on a phone for the intended experience. Tap through **Home → Labs → Trials** using the
bottom tab bar, the in-screen buttons, or any scored trial card. The published artifact is
redeployed on ship, so it may trail the repo; `index.html` on this branch is the source of
truth.

---

## The three tabs

What ships today. The Metrics tab in the design spec is `UPDATELOGV2.md`; the tab in its
place is **Labs**, which covers the same ground with less of it.

| # | Tab | Role (I→P→O) | What it shows |
|---|--------|--------------|---------------|
| 1 | **Home** | Input | Health Score ring with its `n of N markers` confidence line, biomarker bars, entries captured, your top-ranked trials |
| 2 | **Labs** | Processing | Each biomarker against its reference range with trend over time, and the way in to adding a document or typing a value |
| 3 | **Trials** | Output | Computed match score **and** confidence per trial, the per-criterion audit behind each one, and the criteria the parser could not read, shown verbatim |

**The Health Score** on the home screen is the weighted share of your tracked biomarkers
sitting inside their reference range, with partial credit for near-range values. A marker you
have no value for is **excluded from the score and lowers the confidence instead** — it never
counts as a pass. The exact formula is in [`docs/SIMPLIFY.md`](docs/SIMPLIFY.md) §6.

**OpenHealth does not contact your doctor,** and has no channel with which to. The planned
replacement — a real one-page prep sheet carrying every failed criterion, every near-miss with
its exact gap, your values and dates, and the NCT numbers — is **specified but not built**
(`UPDATELOGV2.md`). Until it ships the app generates no file, so this is a plan, not a
feature, and should not be described as one.

### The trials in the app

**23** genuine registry records, retrieved from ClinicalTrials.gov on **2026-10-06** and
stored with their **raw eligibility text verbatim**, which the app parses at render time. The
unmodified API response for each one is in `assets/intake/trials/`, so every line the audit
screen quotes can be checked against the registry in ten seconds. A few, by way of example:

| Trial | NCT ID | Sponsor |
|---|---|---|
| Iron Revisited | [NCT06942208](https://clinicaltrials.gov/study/NCT06942208) | University of Calgary |
| Icovamenib in Type 2 Diabetes | [NCT07502508](https://clinicaltrials.gov/study/NCT07502508) | Biomea Fusion |
| N-acetylglucosamine in Crohn's | [NCT07225998](https://clinicaltrials.gov/study/NCT07225998) | Johns Hopkins |
| Weight regain after GLP-1 | [NCT07729332](https://clinicaltrials.gov/study/NCT07729332) | Mass General |

Rebuild the corpus from intake with `python scripts/build_corpus.py`.

Scores are computed by `matchScore()` in `index.html`, not typed in, so they move with the
profile and are **deliberately not quoted here**. Distance to the nearest site is computed at
build time from the registry's own `geoPoint` to a **fixed origin named in
`scripts/build_corpus.py`** — the app does not know where you are and never asks, so the
screen says what the number is measured from. It is a preference, marked `protocol:false`, and
never blocks eligibility.

### A note on `garmin.json`

**This file does not exist yet, and neither does the sync script.** The Garmin rail is
`UPDATELOGV2.md`. The note is kept here because it describes the arrangement collaborators
will find when it lands, and it is better agreed now than discovered later:

the vitals will be the **repo owner's own real Garmin data** — resting heart rate, SpO2, HRV,
sleep, body composition — pulled by a local Python script and committed in the clear. That is
deliberate, so nobody is surprised to find it in the repo. It is fitness data voluntarily
contributed by the person who owns it; **it is not patient data, and no real patient data is
ever used in this project.**

---

## Repo map

```
index.html              ← the entire prototype (one file, no build step)
tests.html              ← the engine test harness. Loads index.html and drives the SHIPPED
                          functions, not a copy. Needs the dir served over http:
                          `python -m http.server 8731`, then open /tests.html
scripts/
  build_corpus.py       ← regenerates the 23-record corpus in index.html from
                          assets/intake/trials/. Asserts the criteria text is byte-identical
garmin.json             ← NOT YET. The Garmin rail is UPDATELOGV2.md (see above)
scripts/sync_garmin.py  ← NOT YET. Same
docs/
  README.md             ← doc index + reading paths. Start here if you're browsing
  BRIEF.md              ← the idea + all 6 required deliverable answers (source of truth)
  SIMPLIFY.md           ← the current plan: the no-condition inversion, the two input rails, what got cut
  REBUILD.md            ← why the app works this way: the pivot, the API evidence, the build order
  PITCH.md              ← two-person mock Shark Tank script + offer sheet (equal speaking time)
  MISSION.md            ← mission, values, positioning, the pitch at three lengths
  ARCHITECTURE.md       ← data collection, matching, distribution (flowcharts) + §4a parser contract
  COSTS.md              ← run cost at 1k/50k/500k users, unit economics, real vendor prices
  MARKET.md             ← competitive landscape, the precise claim that survives scrutiny, market size
  RISKS.md              ← full risk register, HIPAA/FDA surface, ethical commitments
  ROADMAP.md            ← the dev plan to the Oct 26 CAC deadline, the cut list, submission checklist
  DESIGN.md             ← design system: color, type, components, motion
  BUILDSPEC.md          ← the three-screen spec the prototype was built from
  STACK.md              ← why it's one static HTML file and not Next.js; when to revisit
assets/
  README.md             ← what counts as intake vs. processed, and why
  intake/               ← raw source material. Never edited in place.
    sketches/           ← IMG_0631–0634: the original hand-drawn mockups
    references/         ← look-and-feel references the visual language came from
  processed/            ← generated output: screenshots, QR codes, poster art
CLAUDE.md               ← instructions for AI collaborators (Claude Code)
```

New here? Read **[docs/BRIEF.md](docs/BRIEF.md)** first — it explains the whole idea in
two minutes — then **[docs/SIMPLIFY.md](docs/SIMPLIFY.md)** for the current plan and
**[docs/REBUILD.md](docs/REBUILD.md)** for why it's built this way. Then
**[docs/README.md](docs/README.md)** for reading paths through the rest (there's a 15-minute
path for a presentation and a 45-minute one for "is this real?").

---

## The analysis behind the prototype

The prototype shows the output. These docs are the thinking — including an honest account of
which layers are implemented and which are depicted
([ARCHITECTURE.md](docs/ARCHITECTURE.md) §8 has it row by row).

| Question | Doc |
|----------|-----|
| **What are we building right now, and what got cut?** | [**SIMPLIFY.md**](docs/SIMPLIFY.md) |
| **Does it actually work, and what's still faked?** | [**REBUILD.md**](docs/REBUILD.md) |
| Why does this exist, and what won't we do? | [**MISSION.md**](docs/MISSION.md) |
| How would it actually collect and distribute data? | [**ARCHITECTURE.md**](docs/ARCHITECTURE.md) |
| What would it cost to run, and is it a business? | [**COSTS.md**](docs/COSTS.md) |
| Hasn't someone already built this? | [**MARKET.md**](docs/MARKET.md) |
| What could go wrong? | [**RISKS.md**](docs/RISKS.md) |
| What's left to build before the deadline? | [**ROADMAP.md**](docs/ROADMAP.md) |
| Shouldn't this be Next.js? | [**STACK.md**](docs/STACK.md) |
| How do we pitch it out loud in 3 minutes? | [**PITCH.md**](docs/PITCH.md) |

Cost and market figures are tagged `[sourced]`, `[modeled]`, or `[assumed]` so you can tell
a real vendor price from our arithmetic from a guess. Sources are linked in each doc.

---

## Editing the prototype

`index.html` is the single source. There is no build step — open it, edit, save.

To publish your changes to the live URL, in a Claude Code session run something like:

> "Read docs/DESIGN.md, make \<change\>, and re-publish `index.html` to the existing
> artifact URL."

Publishing to the **same URL** keeps the link (and any QR code on the poster) stable.

---

## Working on this together

This is a co-shared repo. Every commit explains *what changed and why* in plain English
in the commit body — so a collaborator is never surprised by a pull. See `CLAUDE.md`.
