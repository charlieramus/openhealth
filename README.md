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
OpenHealth opens by asking for a document. It reads your lab paperwork and your watch data,
builds a profile, and ranks every trial it knows about against it.

**The trials are real, and so is everything else.** The standard the project is held to:
*everything has to be functional — not just clickable, but actually real. The only accepted
limitation is that there is no backend.* Lab values are OCR'd from actual documents in the
browser. Vitals come from a real Garmin account. The trials are genuine
[ClinicalTrials.gov](https://clinicaltrials.gov) records, and the app parses their raw
eligibility text at runtime rather than reading rules a human pre-encoded.

### What works today, and what's next

Stated plainly, because the difference is the project:

| | |
|---|---|
| ✅ **The matching engine is real** | Every score on screen is computed from a structured profile against protocol-quoted criteria. Change a lab value and the scores, bars and ranking all move. No literals |
| ✅ **The trial records are real** | Real NCT IDs, sponsors, phases, and inclusion/exclusion text |
| 🔨 **The criteria parser** | Criteria are still hand-transcribed into rule objects. **Automating that — free text → checkable rule — is the work in progress**, and it's the actual computer science. The same parser reads OCR'd lab documents |
| 🔨 **The two input rails** | Document OCR (Tesseract.js, in-browser) and the Garmin sync script. Both keyless, both real. See [`docs/SIMPLIFY.md`](docs/SIMPLIFY.md) §5 |

**Start with [`docs/SIMPLIFY.md`](docs/SIMPLIFY.md)** for the current plan, what got cut and
why, then [`docs/REBUILD.md`](docs/REBUILD.md) for the API evidence the whole thing rests on.

---

## ▶ See it live

**Prototype:** https://claude.ai/artifact/5H4KWf2bja3DKDydumaqyo

Open it on a phone for the intended experience. Tap through **Home → Metrics → Trials**
using the bottom tab bar, the in-screen buttons, or any scored trial card.

---

## The three tabs

| # | Tab | Role (I→P→O) | What it shows |
|---|--------|--------------|---------------|
| 1 | **Home** | Input | Health Score ring, biomarker bars, documents captured, your top trial match |
| 2 | **Metrics** | Processing | Each biomarker vs. its reference range, with trend over time |
| 3 | **Trials** | Output | Computed match score per trial, the per-criterion audit behind each one, and a downloadable appointment prep sheet |

**The Health Score** on the home screen is the weighted share of your tracked biomarkers
sitting inside their reference range, with partial credit for near-range values. A marker you
have no value for is **excluded from the score and lowers the confidence instead** — it never
counts as a pass. The exact formula is in [`docs/SIMPLIFY.md`](docs/SIMPLIFY.md) §6.

**OpenHealth does not contact your doctor.** It generates a real one-page prep sheet — every
failed criterion, every near-miss with the exact gap, your values and dates, the NCT numbers
— that you take to an appointment you book yourself.

### The trials in the app

Genuine registry records, retrieved from ClinicalTrials.gov and stored with their **raw
eligibility text verbatim**, which the app parses on load.

| Trial | NCT ID | Sponsor |
|---|---|---|
| Iron Revisited | [NCT06942208](https://clinicaltrials.gov/study/NCT06942208) | University of Calgary |
| Icovamenib in Type 2 Diabetes | [NCT07502508](https://clinicaltrials.gov/study/NCT07502508) | Biomea Fusion |
| N-acetylglucosamine in Crohn's | [NCT07225998](https://clinicaltrials.gov/study/NCT07225998) | Johns Hopkins |
| Weight regain after GLP-1 | [NCT07729332](https://clinicaltrials.gov/study/NCT07729332) | Mass General |

Scores are computed by `matchScore()` in `index.html`, not typed in, so they move with the
profile and are **deliberately not quoted here**. Distance is OpenHealth's own preference
filter, marked `protocol:false`, and never blocks eligibility.

### A note on `garmin.json`

The vitals in the app are the **repo owner's own real Garmin data** — resting heart rate,
SpO2, HRV, sleep, body composition — pulled by a local Python script and committed in the
clear. This is deliberate, so collaborators aren't surprised to find it. It is fitness data
voluntarily contributed by the person who owns it; **it is not patient data, and no real
patient data is ever used in this project.**

---

## Repo map

```
index.html              ← the entire prototype (one file, no build step)
garmin.json             ← committed snapshot of the owner's real Garmin data (see above)
scripts/
  sync_garmin.py        ← local sync script. Run every few days; never deployed
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
