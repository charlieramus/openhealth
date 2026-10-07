charlie

# OpenHealth — Twelve Days to Freeze 1/2: The Engine Rails
# Work on one stage at a time. Do NOT combine stages.

---

## Context

Read `docs/SIMPLIFY.md` first, then `docs/ROADMAP.md` Weeks 2–3 and
`docs/ARCHITECTURE.md` §4a. The app currently ships three screens in a single `index.html`
with a **real** evaluator — `evaluateCriterion()` and `matchScore()` at `index.html:1324`
and `index.html:1369` compute every score on screen from `PROFILE` (`index.html:1190`) and
`TRIALS` (`index.html:1415`). The gap is one level up: those criteria were
**hand-transcribed** by a human reading two trials' eligibility text. **The app can evaluate
criteria. It cannot yet read them.**

This is log 1 of 2 covering the twelve days to feature freeze (**Saturday, October 18**).
V1 builds the four items `docs/SIMPLIFY.md` §7 marks *never cut* — corpus, parser, evaluator
re-wire, document rail — plus the strip-out pass and the test harness. V2 covers the
cuttable tail: the hub shell, the Garmin rail, and the prep sheet.

**A Rule = one bullet of a trial's published eligibility text, parsed into a checkable
predicate, carrying the original wording verbatim in `source` and never discarded.**

This log builds only the rails that turn free text into verdicts. It does **not** build the
three-tab hub, the Garmin rail, or the prep sheet — those are V2 — and it does **not** add a
condition input, a search box, or any runtime network call, which are permanently cut
(`docs/SIMPLIFY.md` §2, §4.4).

## Decisions (carried from `docs/SIMPLIFY.md` and `docs/ARCHITECTURE.md` §4a)

- **Parser contract:** build exactly the interface in `docs/ARCHITECTURE.md` §4a —
  `parseCriteria(text) → Rule[]`, `parseLabDocument(text) → Measurement[]`,
  `evaluateRule(profile, rule) → Verdict`, `matchScore(profile, trial) → Result`. Do not
  invent a different shape. It is written so a model-backed extractor could drop in behind
  the same interface later.
- **One parser, two kinds of text.** The same tokenizer and analyte vocabulary read trial
  criteria *and* OCR'd lab reports. This is why the document rail is cheap once the parser
  exists — do not write a second extractor for Stage 6.
- **Reuse, do not reimplement:** `evaluateCriterion()` and `matchScore()` already work and
  already handle `band` near-miss tolerance and `weight`. Stage 5 changes what they *read*,
  not what they compute.
- **Score and confidence are two numbers, always.** Score = weighted PASS ÷ weighted
  **decidable**. Confidence = decidable ÷ total, reported as "n of N criteria checkable". An
  unknown lowers confidence and must never inflate the score. A missing analyte is
  `UNKNOWN`, **never a pass** — A1c is deliberately absent from the profile as the standing
  test case for this.
- **`unparsed` is a first-class output,** surfaced in the UI verbatim, never dropped and
  never guessed.
- **Real now:** trials and their raw `eligibilityCriteria` text (ClinicalTrials.gov, saved
  verbatim), every score and verdict on screen, lab values OCR'd in-browser.
- **Never real:** patient data. No synthetic person either — Jordan Reyes and the fictional
  care team are deleted in Stage 1, not re-skinned.
- **Zero network calls at runtime.** The corpus is a committed file. Tesseract.js is the only
  CDN library. **Do not add an API key** — see `docs/STACK.md` §6a.
- **Design:** build screens from `docs/FIGMA-MAKE-PROMPT.md` as the written 10-screen spec
  and `Screenshot 2026-10-06 153715.png` as the home reference. **No Figma Make pass** — its
  output is React + Tailwind this stack cannot consume. Tokens per `docs/DESIGN.md`: canvas
  `#E6EAE5`, surfaces `#FFFFFF`, ink `#131A16` / `#59645C` / `#95A099`, and the biomarker
  spectrum held constant per marker — iron `#E11D74`, hemoglobin `#7C4DFF`, SpO2 `#12B3A6`,
  LDL `#2F80ED`, good `#12B76A`, warn `#F5A524`. Verdicts legible without colour: always an
  icon **and** a word.
- **Never quote a score as a constant.** No `87`, no `93`, no `79/100` anywhere in prose,
  markup, or the video script. `NCT06942208` and `NCT07502508` are real and may be named;
  their scores may not.
- Large build, first half: **seven stages.**

---

# Stage 1 — Strip-out pass, and the last literal

```
Delete every screen and fixture that looks functional but is not, per docs/SIMPLIFY.md §4.
This is a deletion stage — do not improve or re-skin anything, remove it.

1. Delete the send-to-doctor flow from index.html: the #sendBtn button (index.html:1090),
   send(), and the two call sites that set its label (index.html:1546, index.html:1603).
   There are no doctors on the other end, so the screen is theater. No replacement button
   on this screen in this stage — V2 adds "Download prep sheet" as the only action there.
2. Delete the synthetic patient Jordan Reyes, including the .pill-profile avatar at
   index.html:739, and the fictional care-team portraits with their .av.f-<name> classes
   and base64 data URIs. Nothing in the app is a synthetic person any more.
3. Delete "Doctors Available: 9" and any surrounding count.
4. Delete any condition input, search field, or condition dropdown. The app ranks every
   trial it knows about against the profile; it never asks what you have.
5. Kill the last literal: index.html:1292 calls countUp(document.getElementById('hs'), 87).
   Replace 87 with a computed Health Score per docs/SIMPLIFY.md §6 — the weighted share of
   tracked markers inside their reference range, with partial credit, markers with no value
   EXCLUDED from the score entirely. Render the confidence line "n of N markers" directly
   beneath the number. The ring must never show a figure the engine did not produce.
6. Remove any remaining reference to r4.smarthealthit.org or any other runtime fetch.

Verify: grep the repo for "Jordan", "sendBtn", "Doctors Available", "smarthealthit", and the
bare literals 87 / 93 / 79 in markup or script — report each hit or confirm zero. Open
index.html, confirm the Health Score ring renders a computed number with its "n of N markers"
line, and confirm DevTools Network shows no request other than the Tesseract.js CDN. Report
what you deleted, file and line.
```

## Stage 1 Report

Deletion pass done, plus the Health Score. `index.html` went **1666 → 1556 lines** and
**134,755 → 81,100 bytes** (`125 insertions, 235 deletions`). Line numbers below are the
pre-edit ones, so they match the spec.

**1 · Send-to-doctor flow — deleted.**

| Lines | What |
|---|---|
| markup 1078–1092 | the whole `Auto-send to your doctor` card, including `#sendBtn` (1090) and the `Dr. Chen · reviews within 24h` block |
| markup 1137–1144 | the `Sent to Dr. Chen` confirmation overlay and modal |
| markup 1115–1116 | the paper-plane `<span id="plane">` |
| script 1601–1623 | `window.send()` and the overlay dismiss listener |
| script 1545–1550 | the two call sites in `renderTrial()` that set the button label (spec cites 1546 and 1603 — they sat inside these two blocks) |
| script | the `sentFor` ledger the flow kept |
| css 568–577, 597–607, 636–657 | `.send`, `.plane` + `@keyframes fly`, `.overlay` / `.modal` |
| TRIALS data | `sendHead`, `cta` and `sent` dropped from both trial records |

No replacement button on that screen, per the spec. Screen 3 now ends on **Other trials
for you**, which reads as a deliberate ending rather than a gap.

**2 · Jordan Reyes and the fictional care team — deleted.**
Markup 739 (the `.pill-profile` avatar, `aria-label="Jordan Reyes"`), markup 850–860
(*Your recent doctors*), css 191–207 (`.pill-profile`), css 348–359 (`.docs` / `.doc`),
and **css 663–708 — the `.av` portrait machinery and all ten base64 StyleGAN faces.**
Those faces alone were ~47 KB, which is most of the file-size drop. `document.querySelectorAll('.av').length`
is now `0`. The top-right of Home keeps only the bell.

Also rewritten rather than left half-deleted: `notePass` / `noteFail` on both trials and
the *Book a follow-up* recommendation all named **Dr. Chen**. She does not exist, so the
copy no longer names a clinician — e.g. *"The only site is in Calgary, though — worth
asking whether a closer one is opening."*

**3 · "Doctors Available: 9" — deleted.** The string itself was not in `index.html`; the
surrounding count was, as the *Care team · 9 doctors* eyebrow plus a nine-portrait row at
markup 1093–1107. Both gone.

**4 · Condition input — none existed, and none exists now.** The live page has
`document.querySelectorAll('input, select, textarea').length === 0` and no element with a
`placeholder` or `type=search`. Confirmed rather than assumed.

**5 · The last literal — killed.** `countUp(document.getElementById('hs'), 87)` is now
`renderHealth()`. Added `TRACKED`, `markerCredit()`, `healthScore(idx)`, `renderHealth()`
implementing `docs/SIMPLIFY.md` §6 exactly: in range → 1.0, outside by `d` →
`clamp(1 − d/(hi−lo), 0, 1)`, **no value → excluded entirely**. Weights are a real term and
are kept explicit, uniform at 1 — no marker was given a clinical weight this build can
defend. A one-sided range takes its implicit bound (`under 100` is the interval `[0, 100]`),
so partial credit always measures against a real interval instead of an invented tolerance.

`a1c` is in `TRACKED` with no values, so it is excluded from the score and costs confidence
instead — the same standing UNKNOWN case the trial evaluator has to survive. Verified:
`markerCredit(a1c) === null`, and it is neither `0` nor `1`.

Engine output, read out of the live DOM:

```
ferritin    8      ref 12-150    credit 0.97101
hemoglobin  13.1   ref 12-16     credit 1.00000
spo2        97     ref 95-100    credit 1.00000
ldl         95     ref 0-100     credit 1.00000
a1c         none   ref 0-5.7     EXCLUDED (no value)

Health Score  99      ring --off 5.3   (was a typed 87 / typed --off:69.4)
Confidence    4 of 5 markers            rendered directly beneath the number
```

The trend pill was a typed *"4 points since your June panel"*. It now runs the same
formula over the June column (`healthScore(MONTHS.indexOf('Jun'))` → 98) and renders
**"1 point up since your June panel"**, with the arrow direction computed too.

**6 · `r4.smarthealthit.org` — zero hits**, and there is no `fetch` or `XMLHttpRequest`
anywhere in the file.

### Verify

Greps over `index.html`, each **0**: `Jordan`, `sendBtn`, `Doctors Available`,
`smarthealthit`, `Dr. Chen`, `Care team`, `f-patient`, `f-chen`, `class="docs"`,
`pill-profile`, `window.send`, `sentFor`, `data:image`. `window.send` is `undefined` on the
live page.

Bare literals `87` / `93` / `79`: **three hits, all SVG geometry** — `cx="93" cy="93"` and
`rotate(-90 93 93)` on the match ring at markup 916–918. No score constant remains.

Served the page at `127.0.0.1:8731` and drove it: Home → Labs → Trials → switch to
`NCT07502508` → back to `NCT06942208` → Home. **Zero console errors, zero uncaught
exceptions.** The ring renders **99** with **"4 of 5 markers"** beneath it (screenshotted).
Screen 3 still renders 5 criterion rows, *"You meet all 4 entry criteria"*, and the ranked
related list.

**Network — one honest failure against the spec.** No application request is made: no
`smarthealthit`, no API call, nothing. But the page still pulls **Google Fonts** at markup
5–7, so DevTools shows three third-party requests (the `css2` stylesheet plus two `woff2`
files). The spec's wording is *"no request other than the Tesseract.js CDN"*, and this does
not meet it. I did not rip the webfonts out in a deletion stage — Bricolage Grotesque and
Inter are the whole typographic identity, and self-hosting vs. falling back to system fonts
is a design decision that belongs with the Stage 7 six-rule audit, not to a silent swap
here. **Named, not rounded up to done.**

### Deviations and things to flag

- **Beyond the literal spec:** the three biomarker bars under the ring were typed markup
  (`8`, `13.1`, `97`, widths `16%` / `66%` / `92%`) sitting directly beneath a now-computed
  ring. Typed numbers next to a computed one is the same bug item 5 exists to kill, so
  `renderMacros()` now reads them from `MARKERS`. Width is value ÷ reference ceiling,
  floored at 3%. Iron lands at **5%** — a thin sliver, which is the truth: ferritin 8
  against a 150 ceiling really is almost nothing.
- **§6 produces 99, and that number is soft.** The formula is implemented exactly as
  written, but partial credit is measured against the width of the reference interval, and
  ferritin's is 138 wide — so being 4 units under the floor costs only 2.9% of its credit.
  The result is a **99 on a profile whose load-bearing marker is below range and falling**,
  which is the "judge reads it as decoration" failure §6 was written to prevent. This is a
  spec problem, not an implementation bug, so I shipped §6 as specified rather than quietly
  redesigning a locked decision doc. It wants either per-marker weights or a tighter
  partial-credit span, and that is a `docs/SIMPLIFY.md` §6 revision.
- **Still fake, still on screen, out of scope here:** the Home tiles — *Records synced 18
  new*, *Providers connected 5 of 5*, *Insurance: Full coverage*, *Balance due $0.00* — and
  the bell's *18 new updates*. None is in this stage's six items, and `docs/SIMPLIFY.md` §7
  item 6 (hub shell, **V2**) owns that screen. Flagging so it is not mistaken for cleared.
- Screen 2's per-marker scale pins and the *"3 of 4 markers in range"* gauge are still typed
  percentages. True today against `MARKERS`, but not computed. V2's Metrics tab owns it.

---

# Stage 2 — Trial corpus: ~20–25 real records, criteria verbatim

```
Build the corpus the parser will be tested against. It must exist before Stage 3 can be
tested honestly.

1. assets/intake/trials/ already holds four real records (NCT06942208, NCT07225998,
   NCT07502508, NCT07729332). Extend to 20–25 real ClinicalTrials.gov records, same JSON
   shape, following that folder's README.
2. For every record, save the raw eligibilityCriteria TEXT verbatim — unedited, including
   its original line breaks and bullet markers. This text is the parser's input and the
   audit table's quoted "original wording". Do not clean it up, do not pre-structure it,
   do not fix its typos.
3. Keep the real sponsor, phase, recruiting status, condition, and NCT ID per record.
4. Pick for spread, not for wins: include trials whose criteria the parser will handle
   cleanly, trials with prose that will land in the unparsed bucket, and at least a few the
   profile will clearly FAIL. A corpus of easy cases produces a parser that only works on
   easy cases, and a ranked list where everything is a strong match reads as fake.
5. Commit the corpus as a file loaded at page load. No runtime fetch.

Verify: report the count, and for three records print the first 200 characters of the stored
eligibilityCriteria next to the same field on ClinicalTrials.gov so the verbatim claim is
checkable. Confirm no record was hand-structured into {op, threshold} objects — that is
Stage 3's job, done by code.
```

## Stage 2 Report

_Pending._

---

# Stage 3 — The criteria parser

```
This is the core computer science of the project and the single most valuable stage in both
logs. Build parseCriteria(text) -> Rule[] exactly to the contract in
docs/ARCHITECTURE.md §4a.

1. Split the inclusion and exclusion blocks, setting Rule.sense accordingly. An exclusion
   rule that MATCHES the patient is a FAIL, not a pass — get the polarity right here, once.
2. One Rule per bullet, kind in: numeric, range, presence, negation, unparsed. Fill op,
   threshold or min/max, unit, analyte, band, weight, required.
3. Normalize units to one canonical UCUM unit per analyte on the way in. Both sides of every
   comparison must already be in the same unit before evaluateRule sees them.
4. Rule.source always carries the original wording verbatim. It is never discarded, because
   the audit table quotes it beneath every row.
5. Anything the parser cannot confidently extract becomes kind:'unparsed'. Never dropped,
   never guessed, never silently treated as satisfied. This is the honesty guarantee the
   whole product rests on.
6. Build it against the committed corpus from Stage 2 so it is testable offline.

Do not wire it into the UI in this stage. Parse, return Rules, and prove the shape.

Verify: run parseCriteria over all 20–25 corpus records and report, per trial, the count by
kind and the total unparsed rate. Print the parsed Rules for NCT06942208 beside their source
text. State the overall unparsed percentage plainly — a high number honestly reported is a
result; a low number achieved by guessing is a bug.
```

## Stage 3 Report

_Pending._

---

# Stage 4 — Test harness and parser fixtures

```
Almost no entry at this level ships tests, and the parser is the thing that most needs them.
This rides alongside Stage 3, not long after it.

1. Create tests.html — a standalone page, no framework, no build step, that runs assertions
   in the browser and prints pass/fail per case.
2. Evaluator cases, each asserting a known profile produces a known verdict:
   - a value exactly at the threshold (boundary, both directions)
   - a missing analyte -> UNKNOWN, never PASS (use the deliberately absent A1c)
   - a value inside band of failing -> NEAR_MISS, with the correct signed margin
   - an all-fail profile
   - an unparsed criterion -> UNKNOWN, counted against confidence, not score
   - a matched exclusion -> the trial is blocked, not merely scored down
   - a failed required inclusion -> blocked
3. Parser fixtures: for a hand-checked subset of the corpus, assert the exact Rule[] that
   parseCriteria should return. These are the regression net for Stages 5 and 6.
4. Assert the two-number invariant directly: score is computed over decidable rules only,
   and adding an unparsed criterion to a trial must lower confidence and leave score
   unchanged. That assertion is the one a judge is most likely to ask about.

Verify: open tests.html and report the full pass/fail list with counts. Every case passes, or
the failures are named and explained. Do not weaken an assertion to make it pass.
```

## Stage 4 Report

_Pending._

---

# Stage 5 — Evaluator re-wire: parsed predicates in, score and confidence out

```
evaluateCriterion() and matchScore() already work. This stage changes what they read, not
what they compute. Keep the near-miss band logic and the weighting.

1. Rename/retarget to the §4a contract: evaluateRule(profile, rule) -> Verdict and
   matchScore(profile, trial) -> { score, confidence, verdicts[], blocked, unparsedCount }.
2. Feed them the parser's Rule[] instead of the hand-written criteria objects in TRIALS
   (index.html:1415). Delete the hand-transcribed objects once the parser output replaces
   them — leaving both is how the two disagree on stage.
3. Score = weighted PASS / weighted DECIDABLE. Confidence = decidable / total, reported as
   "n of N criteria checkable". Return both, always, never merged into one figure.
4. unparsed -> UNKNOWN. Missing analyte -> UNKNOWN. Within band of failing -> NEAR_MISS with
   a signed margin. Matched exclusion or failed required inclusion -> blocked.
5. Rank every trial in the corpus through matchScore. No search, no filter, no condition.
   Verify the ranking generalizes past the two hand-picked trials it was built on.
6. Per-criterion audit UI, per docs/FIGMA-MAKE-PROMPT.md screen 7 — this is the screen the
   whole app exists for. One row per criterion: the rule in plain language, the patient's
   actual value, a verdict chip (PASS / FAIL / UNKNOWN / NEAR MISS, each with its own icon
   AND word), and the trial's original wording quoted verbatim beneath. Score and confidence
   side by side and visibly distinct. A collapsed "N criteria we couldn't check
   automatically" section showing raw text — present, never hidden. The persistent
   disclaimer: this is not an eligibility decision.
7. Near-miss callout, amber, the most prominent thing after the table, naming the exact gap.

Verify: tests.html still fully passes. Open the app and report the ranked list with each
trial's score AND confidence, including the weakest match, plus the full audit table for one
trial with every row's verdict and source line. Confirm no hand-transcribed criteria objects
remain anywhere in index.html.
```

## Stage 5 Report

_Pending._

---

# Stage 6 — The document rail

```
The headline input, and the one that removes the condition question. The parser already
exists, so this stage is wiring plus an honesty screen.

1. Tesseract.js from CDN, in-browser only. Nothing is uploaded anywhere, and the UI says so
   in plain language.
2. OCR text -> parseLabDocument(text) -> Measurement[] { analyte, value, unit, drawnOn,
   confidence, source }, using the SAME tokenizer, analyte vocabulary, and unit
   normalization as Stage 3. Do not write a second extractor.
3. Measurements merge into the profile the engine reads, normalized to FHIR R4 / US Core
   shapes with LOINC codes — the format only, no server call.
4. Build the extraction review screen per docs/FIGMA-MAKE-PROMPT.md screen 3, the honesty
   screen. Every extracted value with its unit, date, and a confidence indicator. Low-
   confidence rows visually flagged and editable IN PLACE, not behind a separate edit mode.
   A distinct bottom section: "N lines we couldn't read", showing the raw text verbatim with
   manual entry available.
5. Never build a state where unreadable content is silently hidden. Showing what failed is
   the point of the screen.
6. Manual entry with unit normalization is the correction path AND the offline demo path.
   The video must never depend on OCR succeeding live.
7. Add-records screen per spec screen 2: take a photo, or upload a PDF/image.

Verify: OCR a real lab document end to end and report what was extracted, what was flagged
low-confidence, and what landed in the unreadable bucket with its raw text. Then show the
ranked trial list recomputing from those values — WITHOUT having told the app what condition
you have. Confirm DevTools Network shows only the Tesseract.js CDN. tests.html still passes.
```

## Stage 6 Report

_Pending._

---

# Stage 7 — Coherence and verify

```
Full walkthrough, no new features.

1. Run tests.html and report every case.
2. Literal demo walkthrough, in order: open the app cold with no data, add a lab document,
   correct a flagged value, read the ranked trials, open the audit table for a strong match
   and for a weak one, and read the unparsed section. Report what a judge would see at each
   step, including anything that looks worse than it should.
3. Check the whole app against the six rules in docs/FIGMA-MAKE-PROMPT.md: no search bar or
   condition picker anywhere; unknown never rendered as a zero, a dash, or an empty bar;
   score and confidence never merged; nothing sent anywhere; verdicts legible without
   colour; no quoted score constant. Report each as pass or fail with the location.
4. Load with the network disconnected after first load and confirm the app works.
5. Update the docs to match what now exists: docs/ARCHITECTURE.md §8 prototype map,
   docs/ROADMAP.md Weeks 2–3 (mark the delivered stages), and README.md "what is real".
   Do not claim anything this log did not actually ship.

Verify: tests.html fully green, the walkthrough reported step by step, the six-rule audit
reported line by line, and the offline load confirmed. Name anything still outstanding rather
than rounding it up to done.
```

## Stage 7 Report

_Pending._

---

# After These Stages

- The app reads trials instead of being told about them. Free-text eligibility criteria
  become checkable rules at runtime, in front of the viewer, with an honest `unparsed`
  bucket — which is the difference between *fully functional* (4) and *functional with
  complex features* (5) on the rubric's Function sub-criterion.
- The condition question is gone for good. You give it a document; it ranks everything it
  knows. That is the `docs/SIMPLIFY.md` §2 inversion, and it is also the competitive claim
  that holds up.
- Deliberately still missing: the three-tab hub, the Garmin vitals trend on the near-miss
  callout, and the appointment prep sheet. All three are **V2**, and `docs/SIMPLIFY.md` §7
  says to cut them in the order 8 → 7 → 6 if days are lost. Cutting all of V2 loses no
  functionality built here.
- Next: `UPDATELOGV2.md`, then feature freeze end of day **Saturday, October 18**, then the
  video — worth up to 10 of 30 points, and where *Code* goes from 1 to 4.
