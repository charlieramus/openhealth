# OpenHealth

**One app for your whole health picture — and the clinical trials you actually qualify for.**

OpenHealth is an interactive three-screen mobile-app prototype built for the
**Congressional App Challenge** (and a computing-innovation class project). It shows a
patient's fragmented US health data — labs, insurance, billing, doctors — pulled into one
place, then surfaces a clinical trial the patient qualifies for and lets them send their
records to a doctor in one tap.

**The patient is invented. The trials are real.** Every lab value, doctor and insurance
detail is fabricated — no real APIs, accounts, or PHI. The four clinical trials are genuine
records pulled from the [ClinicalTrials.gov](https://clinicaltrials.gov) public API, and
every eligibility threshold in the matching engine is quoted from the trial's own protocol.
Each NCT ID shown in the app can be looked up.

---

## ▶ See it live

**Prototype:** https://claude.ai/artifact/5H4KWf2bja3DKDydumaqyo

Open it on a phone for the intended experience. Tap through **Home → Labs → Trials**
using the bottom tab bar, the in-screen buttons, or either scored trial card.

---

## The three screens

| # | Screen | Role (I→P→O) | What it shows |
|---|--------|--------------|---------------|
| 1 | **Home** | Input | Updates, new trials, bloodwork snapshot, insurance, doctors |
| 2 | **Labs** | Processing | Four color-coded biomarkers vs. normal range + a health gauge |
| 3 | **Trials** | Output | Computed match score per trial, the comparison behind each criterion, one-tap send to doctor |

### The trials in the app

All four are live registry records, retrieved 2026-09-29.

| Trial | NCT ID | Sponsor | Match | Why |
|---|---|---|---|---|
| Iron Revisited | [NCT06942208](https://clinicaltrials.gov/study/NCT06942208) | University of Calgary | **79** | Meets all 4 entry criteria; only site is 2,006 mi away |
| Icovamenib in Type 2 Diabetes | [NCT07502508](https://clinicaltrials.gov/study/NCT07502508) | Biomea Fusion | **21** | No A1c on file and BMI outside 25–40, despite a site 138 mi away |
| N-acetylglucosamine in Crohn's | [NCT07225998](https://clinicaltrials.gov/study/NCT07225998) | Johns Hopkins | — | Not yet recruiting |
| Weight regain after GLP-1 | [NCT07729332](https://clinicaltrials.gov/study/NCT07729332) | Mass General | — | Not yet recruiting |

The two scores are computed by `matchScore()` in `index.html`, not typed in. Distance is
OpenHealth's own preference filter, marked `protocol:false`, and never blocks eligibility.

---

## Repo map

```
index.html              ← the entire prototype (one file, no build step)
docs/
  README.md             ← doc index + reading paths. Start here if you're browsing
  BRIEF.md              ← the idea + all 6 required deliverable answers (source of truth)
  PITCH.md              ← two-person mock Shark Tank script + offer sheet (equal speaking time)
  MISSION.md            ← mission, values, positioning, the pitch at three lengths
  ARCHITECTURE.md       ← how data is collected from APIs, matched, and distributed (flowcharts)
  COSTS.md              ← run cost at 1k/50k/500k users, unit economics, real vendor prices
  MARKET.md             ← competitive landscape, why every rival is B2B, market size
  RISKS.md              ← full risk register, HIPAA/FDA surface, ethical commitments
  ROADMAP.md            ← the 4-week dev plan to the Oct 26 CAC deadline, and the cut list
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
two minutes. Then **[docs/README.md](docs/README.md)** for reading paths through the rest
(there's a 15-minute path for a presentation and a 45-minute one for "is this real?").

---

## The analysis behind the prototype

The prototype is the picture. These docs are the thinking.

| Question | Doc |
|----------|-----|
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
