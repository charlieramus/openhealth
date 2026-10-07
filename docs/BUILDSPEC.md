# OpenHealth — Prototype Build Spec

> ⚠️ **Partly superseded — 2026-10-02, and again 2026-10-06.** This was written from the
> hand-drawn mockups and the prototype was built from it. **The motion, interaction and
> component specs below still hold.** The layout reference for the home screen is now
> `Screenshot 2026-10-06 153715.png` in the repo root. The *content* has moved on twice:
>
> | This doc says | Reality |
> |---|---|
> | CGX Trial #4, LMI, PPF | Real trials — **Iron Revisited** (`NCT06942208`), **Icovamenib in Type 2 Diabetes** (`NCT07502508`) |
> | "87/100" | **Computed by the engine.** Never a constant. Do not quote a match score or a Health Score anywhere |
> | Fake data, no APIs | Lab values are OCR'd from real documents; vitals are real Garmin data; the engine is real |
> | Screen 3 = score + eligibility bars | Screen 3 becomes the **per-criterion audit table** — see the Screen 3 section |
> | Three screens, forward/back | **Three tabs** — Home / Metrics / Trials, with a persistent bottom nav |
> | Notification banner, insurance row, doctors, send-to-doctor | **All deleted 2026-10-06.** Each described something the app does not do |
>
> **The standard, as of 2026-10-06:** *everything has to be functional — not just clickable,
> but actually real. The only accepted limitation is that there is no backend.* A screen that
> looks like it does something it does not do gets deleted, not restyled.
>
> The current plan and the cut list: [`SIMPLIFY.md`](SIMPLIFY.md). The concept pivot and its
> reasoning: [`REBUILD.md`](REBUILD.md). What to build next:
> [`SIMPLIFY.md`](SIMPLIFY.md) §7.

**Task as originally written:** Build and publish the three-screen interactive OpenHealth prototype as a Claude Artifact (live URL). Pure HTML/CSS/JS, single file. No frameworks, no build step.

---

## Context

School project, computing innovation class, and a Congressional App Challenge entry.
**No longer a mockup with fake data** — see the banner above. Deliverable: the three-tab
prototype + poster. The prototype needs a live URL + QR code for classroom demo.

Design doc: `C:\Users\jason\.gstack\projects\openhealth\jason-master-design-20260928-150904.md`

---

## Tech Spec

- **Format:** Single `.html` file published as a Claude Artifact
- **Stack:** Pure HTML + CSS + JS. No React, no Tailwind, no bundler. **One CDN library:**
  `Tesseract.js`, for in-browser OCR
- **Network:** **zero runtime calls.** The trial corpus and `garmin.json` are committed data
- **Keys:** none, ever — including one we already have. [`STACK.md`](STACK.md) §6b
- **Layout:** Mobile-first, ~390px wide (iPhone), centered on desktop
- **Style:** Card-based layout, health app aesthetic

**Off to the side, never deployed:** `scripts/sync_garmin.py` uses `python-garminconnect` to
write `garmin.json` every few days. A build-time pipeline, not a backend — nothing listens on
a port and no credential is ever shipped to the client. [`SIMPLIFY.md`](SIMPLIFY.md) §5.2.

**Color palette (from hand-drawn mockups):**
- Pink/magenta `#E91E8C` — Iron (Ferritin) bar, low result
- Purple `#9C27B0` — Hemoglobin bar, average result
- Teal/green `#26A69A` — Oxygen Saturation bar, steady result
- Blue `#2196F3` — LDL Cholesterol bar, optimal
- Accent/score `#4CAF50` — health score green
- Background `#0D1117` or `#1A1A2E`
- Card bg `#1E2A3A` or similar dark card

---

## Screen 1: Home (Input)

> Layout reference: `Screenshot 2026-10-06 153715.png`.

**Header:** "OpenHealth" wordmark left; profile pill and notification bell right.

**Health Score ring** — the hero. A large amber/orange concentric ring with the **computed**
score at its centre and the confidence line (`n of N markers`) beneath it. The formula is in
[`SIMPLIFY.md`](SIMPLIFY.md) §6: the weighted share of tracked biomarkers inside their
reference range, with partial credit for near-range values. **A marker with no value is
excluded from the score and lowers the confidence — it never counts as a pass.** Never a
constant.

**Biomarker bars** — three to four markers beneath the ring (Iron, Hemoglobin, SPo2 …), each
showing value against its reference range in the marker's colour. Tapping any of them, or
"See Details", opens the Metrics tab at that marker.

**Today card** — dated, with the captures the app has actually ingested: **Records Captured**
(thumbnails of the lab documents OCR'd, tapping one opens what was extracted and lets the
user correct it) and the **appointment prep sheet** entry point.

> **Deleted 2026-10-06, do not reintroduce:** the "18 new updates" notification banner, the
> insurance row, the care-team doctors, and the "Recent Chats" card from the design
> screenshot. The chats card was an AI question surface, which needs a key, which needs a
> server. Everything in this list described something the app does not do.

**Top trial match** — a single scored card for the best-ranked trial: name, condition, NCT ID,
**computed** match score, distance to the nearest site, and a bookmark toggle. Tapping it
opens that trial's audit on the Trials tab.

**Bottom nav** — persistent, three tabs: Home · Metrics · Trials.

**Trial cards, wherever they appear** — built from the engine's ranked output, not typed into
markup, so a name or score can never disagree between screens:
- **Scored trial cards** — tappable → navigate to Screen 3. *Built from the engine's ranked
  output, not typed into markup, so a name or score can never disagree between screens.*
  - Trial name (real, from the registry)
  - Match score chip — **computed**, with a `weak` variant below the threshold
  - Small colored eligibility bars, widths derived from each criterion's `margin`
- **"Starting soon" cards** — display-only, dimmed, from the `SOON` list. Real NCT IDs and
  sponsors, not scored, because the registry says they aren't recruiting yet

**Your Bloodwork section** (label: "Your Bloodwork"):
- Iron (Ferritin) — "Below Avg" — pink/magenta short bar
- Hemoglobin — "Steady" — purple medium bar
- CTA button: "View Details →" → navigates to Screen 2

**Insurance row:** "Full Coverage ✓" — green check

**Recent Doctors:** Row of 4 circular avatar placeholders (gray circles with initials)

---

## Screen 2: Your Test Levels / Bloodwork Results (Processing)

**Header:** Back arrow (top-left) → Screen 1. Title: "Your Test Levels"

**Gauge meter:** Semicircle gauge, arrow pointing to "OK" zone

**Colored bars** (horizontal, show value vs. normal range):
| Marker | Color | Status | Fake value |
|---|---|---|---|
| Iron (Ferritin) | Pink `#E91E8C` | Too Low | 8 ng/mL (normal: 12–150) |
| Hemoglobin | Purple `#9C27B0` | Average | 13.1 g/dL (normal: 12–16) |
| Oxygen Saturation (SpO2) | Teal `#26A69A` | Steady | 97% (normal: 95–100%) |
| LDL Cholesterol | Blue `#2196F3` | Optimal | 95 mg/dL (normal: <100) |

**Recommendations panel:**
1. "Increase iron intake — consider iron-rich foods or supplements"
2. "Schedule follow-up for hemoglobin levels"
3. "Maintain current O2 levels — great work"

**CTA button:** "View Trial Matches →" → Screen 3

---

## Screen 3: Trial Match (Output)

**Header:** Back arrow (top-left) → Screen 2. Title: the selected trial's real name, with its
NCT ID.

**Match score:** Large display with the green ring/arc. **The number is `matchScore()` output
and counts up to it** — never a literal.

**Confidence, next to the score:** *"8 of 11 criteria checkable."* A **second, separate
number** — unknowns and unparsed criteria lower confidence; only real failures lower the
score. Conflating the two is the bug this exists to prevent.

**Eligibility bars:** colored bars per criterion, widths derived from `margin`, so the chart is
a picture of the same numbers that produced the score.

### Per-criterion audit table — the new hero of this screen

The thing no competitor shows (see [`MARKET.md`](MARKET.md) §2). One row per criterion:

| Column | Content |
|---|---|
| **Criterion** | The parsed rule in plain form — "Ferritin ≤ 50 ng/mL" |
| **Your value** | The patient's value, after unit conversion — "8 ng/mL" |
| **Verdict** | **PASS** · **FAIL** · **UNKNOWN** · **NEAR MISS**, color-coded |

Rules for this table — all three are non-negotiable, per
[`ARCHITECTURE.md`](ARCHITECTURE.md) §4a:

1. **A `NEAR MISS` row expands** into the callout: *"Short by 2. Worth asking your doctor
   whether that's worth re-testing."* Never suggest *how* to move a value — see the unintended
   consequence in [`BRIEF.md`](BRIEF.md) §5.
2. **`UNKNOWN` rows are shown, not hidden.** The patient's missing A1c is the demo case: it
   reads UNKNOWN, never an assumed pass.
3. **Criteria the parser couldn't read appear at the bottom**, verbatim, under a plain heading
   like *"3 criteria we couldn't check automatically."* Dropping them silently is the dishonest
   output; showing them is what makes the score trustworthy.

**A hard-blocked trial** (failed required inclusion, or a matched exclusion) says so outright
instead of displaying a misleading mid-range score.

**Registry footer:** real NCT ID linking to clinicaltrials.gov, sponsor, phase, status, and
the **age of the cached data** if it came from cache.

**Appointment prep sheet** — replaces the "Auto Send to Doctor?" section, **deleted
2026-10-06**. There are no doctors on the other end, so that screen, its nine avatars and its
"Sent to Dr. Chen ✓" modal were theater. Do not restyle them; they are gone.

- Label: "Prepare for your appointment"
- Button: "Download prep sheet"
- On tap: the app **generates a real file** — every failed criterion, every near-miss with
  its exact numeric gap, the user's values with their draw dates, and the NCT numbers — and
  hands it to the browser's download. Nothing is simulated and nothing is sent anywhere.
- Copy rule: the app **gets you ready for** an appointment. It never claims to have made,
  booked, or notified one. [`SIMPLIFY.md`](SIMPLIFY.md) §4.1.

**Related Trials section:** the next-ranked trials from the engine's output, as dimmed rows.
Real NCT IDs, engine order — never hand-picked names.

---

## Navigation Map

Three tabs, not a forward/back stack. The bottom nav is persistent and any tab is reachable
from any other at any time.

```
[ Home ]  [ Metrics ]  [ Trials ]      ← persistent bottom nav

Home
  ├── Health Score ring / biomarker bar / "See Details" → Metrics, at that marker
  ├── Records Captured thumbnail → what OCR extracted, with correction
  └── top trial card → Trials, at that trial's audit

Metrics
  └── marker row → expands to range + trend (Garmin trend where there is one)

Trials
  ├── ranked trial row → per-criterion audit
  └── "Download prep sheet" → generates a real file, stays on the tab
```

---

## I→P→O (for class deliverable)

**Owned by [`BRIEF.md`](BRIEF.md) §3 — if the two disagree, `BRIEF.md` wins.** In short:

- **Input:** Two keyless, in-browser rails, and **no question about what condition the user has** — lab documents through `Tesseract.js` OCR into the parser, and the operator's own Garmin data from a committed `garmin.json`. Both normalized into FHIR R4 / US Core shapes with LOINC codes
- **Processing:** Real recruiting trials stored with their **raw eligibility text verbatim** → the same parser turns each free-text criterion into a checkable rule at runtime → an evaluator returns pass/fail/unknown/near-miss per rule → a weighted score **plus a separate confidence figure**, over every trial in the corpus
- **Output:** Ranked trials with a **per-criterion audit table**, near-miss callouts enriched with the watch's trend, the unparsed criteria shown honestly, the real NCT link, and a **downloadable appointment prep sheet**

---

## Class Deliverable Map (all 6 required elements)

| Required | OpenHealth Answer |
|---|---|
| App name + problem | OpenHealth — trial eligibility is published as free text full of numeric thresholds, so patients can't tell what they qualify for; **40–60% who start screening are rejected**, often on one threshold they just missed |
| Three-screen prototype | Home Dashboard → Bloodwork Results → Trial Match (per-criterion audit) |
| Input → Processing → Output | Structured FHIR record → parse criteria into rules, evaluate against real lab values → ranked trials with a per-criterion audit |
| One benefit | A patient learns **why** — which number, which threshold, by how much — turning a dead end into a specific question for a doctor |
| One unintended consequence | **Showing the exact threshold invites gaming it.** Transparency about a threshold and the ability to game it are the same information — see [`BRIEF.md`](BRIEF.md) §5 |
| Why it's a computing innovation | First consumer-facing clinical trial matcher — every competitor (MatchMiner, TrialMatchAI) is B2B (sold to hospitals/pharma). OpenHealth puts the match in the patient's hands. |

---

## Build Instructions for Next Session

1. Load the artifact-design skill before writing HTML
2. Build as a single HTML file with all 3 screens as `div` panels — only one visible at a time via JS `show/hide`
3. Use smooth CSS transitions between screens (slide or fade)
4. Publish as a Claude Artifact — get live URL
5. Add QR code to the poster using the published URL (can use a QR code library or api.qrserver.com)
6. Test that it loads on mobile (phone-width layout)

**Start prompt for next session:**
> "Read BUILDSPEC.md in the openhealth project folder and build the three-screen OpenHealth prototype as a published HTML artifact."
