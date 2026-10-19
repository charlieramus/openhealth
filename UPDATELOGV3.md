charlie

# OpenHealth — Nine Days to Submission: The Thermal Port
# Work on one stage at a time. Do NOT combine stages.

---

## Context

Read `mockups/thermal.src.html` first — it is the component gallery this log ports into the
app, and every section in it carries the argument for why it is drawn that way. Then
`docs/DESIGN.md` §7 (the Tolerance system), `docs/COPY.md` §3 (the word budgets and the
eight rules), and `docs/ROADMAP.md` "Oct 16 → Oct 26" for the dates.

**Prerequisite, before Stage 1 runs:** the nine days of design work that produced the
gallery — `mockups/`, `docs/COPY.md`, and the unstaged edits to `docs/DESIGN.md` and
`docs/README.md` — were still untracked as of 2026-10-16. **Commit them before starting.**
Every stage below reads from files that were, at the time this log was written, one
`git clean -fd` from not existing.

V1 made the app *read*. V2 built the hub it lives in. **This log makes the app look like
what it is** — an instrument that measures a distance — and deletes the three things on
screen that claim a capability the app does not have.

**The app does not gain a single feature in this log.** No new trials, no condition input,
no network call, no new screen. The parser, the evaluator, the ranking and the document
rail are V1 and are untouched end to end. What changes is the sheet it is all drawn on, and
what gets removed from it.

**Stages 1–5 are the feature window and close at the freeze.** Stages 6–7 are restyling and
verification, which are not features and are therefore freeze-legal. If Saturday Oct 17 goes
badly, **Stage 5 is the agreed casualty** — the ring slot it fills takes thermal's smaller
score-and-confidence block instead, and the app is still coherent. Stages 2, 3 and 4 are
**not** cuttable as a set: stopping after Stage 2 leaves thermal's CSS sitting on top of the
October 6 skeleton, which is the half-rethemed outcome and is worse than shipping today's
build untouched.

## Decisions

- **Thermal wins the palette, and `docs/DESIGN.md` is rewritten to match** — decided
  2026-10-16. Two Tolerance systems existed in the repo and contradicted each other: the
  shipping `index.html` (cool grey-blue `#E7ECEE`, signal `#B81D40`, IBM Plex Mono for all
  quantities, locked 2026-10-07) and `mockups/thermal.html` (neutral zinc `#F4F4F5`, signal
  `#D7122A`, Inter only). Thermal is newer, its argument that a mono face on small data
  labels is itself a generated-design tell is correct, and `mockups/build.py` already solves
  the embedded-font problem that `DESIGN.md` §7.9 left open. **The cool-blue v1 palette joins
  the retired list in §1 and does not come back.**
- **The mono-for-quantities rule is deleted, not softened.** Inter's tabular figures with
  `-.02em` tracking do the alignment job that rule existed for, which is why thermal ships
  one family instead of two.
- **Colour never carries a verdict.** Your value is ink, the requirement is a tint, the gap
  is the only thing in signal colour. This is what makes the app pass greyscale by
  construction rather than by a special pass, and it survives the palette change unchanged.
- **The fake vitals are deleted, not relabelled** — decided 2026-10-16, closing the question
  `docs/DESIGN.md` §7.9 flagged and declined to answer. `Resting HR 62`, `Weight 154 lb`,
  `Hydration 6 glasses` and their hand-drawn SVG sparklines are hard-coded in static HTML,
  are not read from `garmin.json`, and `garmin.json` does not exist in this repo. Per the
  project standard: a screen that looks like it does something it does not do gets deleted,
  not polished.
- **The Garmin rail is cut.** `docs/SIMPLIFY.md` §7 already ranked it second-to-cut. With the
  vitals deleted the claim it was meant to support is gone cleanly rather than half-made.
  **`CLAUDE.md`'s "Vitals | Real" row changes with it** — if the rail is cut and that row
  stays, the standards doc becomes one of the things that is lying.
- **The gauge is an amputation, not a deletion.** `renderGauge()` computes its counts from
  real lab states; only the needle is slop. Keep "n of N markers in range", delete the
  needle and its `--ang` write.
- **Two of the eleven eyebrows are engine-written.** `auditHead` (`index.html:1239`) and
  `tRelatedHead` (1260) are `getElementById` targets. They become section headings. Deleting
  them breaks `renderTrial()`.
- **The three-tab nav already exists** — `index.html:1774`, `TAB_OF = [0,1,2,1,1]`, five
  screens behind three tabs, shipped in V2 Stage 1. Do not rebuild it.
- **Never quote a score, a margin or a Health Score as a constant.** Every number thermal's
  gallery shows is typed, because a gallery has no engine. Every number the app shows is
  engine output. A constant that survives a port is how "87/100" survived in this repo for
  weeks.
- **Copy is governed by `docs/COPY.md`.** The lead card's sentence is thermal draft E —
  *"Ferritin, below the minimum for NCT06942208."* — and it is **generated from engine
  output**, never written into the markup.
- Medium feature: **seven stages.**

---

# Stage 1 — Reconcile the design record

```
Documentation only. No code changes in this stage. It runs first because every stage after
it builds against a doc that currently contradicts the thing being built.

1. docs/DESIGN.md §7.2 — replace the palette table with thermal's tokens, read from
   mockups/thermal.src.html's :root block, not retyped from memory. The heat family
   (--h-wash #FFF2EC, --h-tint #FFD3BC, --h-flare #F2541B, --h-sig #D7122A, --h-deep
   #7F1026), the zinc ground, and the four marker hues (--m-fe #B01E5B, --m-hgb #E2561F,
   --m-o2 #C8860A, --m-ldl #6E2250). Keep the "your value is ink / the requirement is a
   tint / the gap is the only signal colour" rule verbatim — it is unchanged by the repaint.
2. docs/DESIGN.md §7.3 — replace with Inter, four weights, embedded as base64 by
   mockups/build.py. DELETE the mono-for-quantities restriction and the two-face stack.
   State the replacement rule: quantities get font-variant-numeric: tabular-nums and
   -.02em tracking, which is what the mono rule existed to achieve.
3. docs/DESIGN.md §1 — add the cool-blue v1 palette to the retired list, with the date and
   the reason, so it reads as four retired directions rather than three.
4. docs/DESIGN.md §7.9 — close the "embedding the Plex Mono subset" open item (obsolete,
   Inter ships instead) and close the fake-vitals item with the deletion decision and a
   pointer to Stage 4 of this log.
5. docs/ROADMAP.md line 55 — the UI rubric row reads "5. This is our strongest box and it's
   already earned". That predates the 2026-10-07 wholesale rejection and is not true. Change
   it to 3, state why in one clause (ring, invented vitals and eleven eyebrow labels still in
   the markup), and note that this log is what recovers it.
6. CLAUDE.md — the "Vitals | Real" row becomes honest about the Garmin rail being cut, and
   the three-tab description stays as is because the tabs are real.

Verify: report the four retired directions named in §1, confirm §7.3 contains no reference
to IBM Plex Mono or to a second typeface, and quote the new §7.2 --h-sig value. Confirm
docs/ROADMAP.md no longer asserts a UI score of 5. No file outside docs/ and CLAUDE.md is
touched in this stage.
```

## Stage 1 Report

_Pending._

---

# Stage 2 — The system swap

```
Replace the stylesheet wholesale. This is the largest single diff in the log and the one
with the clearest boundary: nothing outside <style> changes.

1. Replace index.html lines 13-935 (the entire <style> block) with the stylesheet from
   mockups/thermal.src.html, built through mockups/build.py so the four Inter weights
   travel inside the file as base64. Zero network calls is a hard constraint, not a
   preference — see CLAUDE.md and docs/STACK.md §6a.
2. KEEP THE ALIAS BAND. index.html's :root carries ~20 alias tokens (--iron, --hgb, --o2,
   --ldl, --brand, --brand-d, --good, --warn, --line, --line-2, --surface, --surface-2,
   --screen, --canvas, --display, --body, --r, --r-sm, --shadow) that are referenced from
   the static markup and from the render functions via t.color. Repoint every one of them
   at a thermal token. Do not delete one without first grepping for it. --brand must
   resolve to ink: no green comes back.
3. The engine writes into ~60 surviving id hooks and emits its own class names inside
   innerHTML strings. Those class names (.scale, .band, .pin, .gap, .chip, .audit-row,
   .vd, .trial, .tally) must all exist in the new sheet. thermal.src.html defines them; the
   job is confirming none was dropped, not inventing any.
4. The 193-class selector contract stays intact. If a thermal class name collides with an
   engine class name that means something different, rename the THERMAL one and note it —
   there is prior art for this exact bug at commit b4149dc, where a class-name collision ate
   the Home grid.

Verify: open the app and report that all five screens render without a missing-style
collapse, that the three tabs still navigate, and that tests.html still passes all 61 cases.
Report the total count of network requests the page makes (must be 0) and the file size.
Screenshot Home, Metrics and Trials at phone width.
```

## Stage 2 Report

_Pending._

---

# Stage 3 — The dimension line

```
The signature primitive, and the highest payoff-per-line change in the project. One
function, and it lands on every audit row in the app simultaneously.

auditScale() at index.html:3364 currently emits .scale > .band + .gap + .pin. Extend it to
thermal's full dimensioned scale, drawn in the "The tolerance scale" section of
mockups/thermal.src.html:

1. .axis — the 1px construction hairline across the full width.
2. .edge labels at the band thresholds, carrying the actual numbers with the unit on the
   outer one.
3. .ext — extension lines dropping from the tick and from the threshold it fell short of.
4. .dim — the dimension line between them, with the margin in a tag that breaks the line.
   marginPhrase() at index.html:3415 already produces this string; do not compute it twice.
5. Heat tracks ACTIONABILITY, not badness, exactly as the gallery argues it: a met criterion
   gets no annotation at all, a wide miss gets the .out wash and NO dimension line, and a
   near miss gets the full dimension in signal red. This is the whole point of the system —
   if a flat FAIL gets a red dimension line, the port has failed.
6. The exclusion inversion in the current function is correct and load-bearing: on an
   exclusion the shaded region is the DISQUALIFYING zone. Preserve it. The gap follows the
   verdict, not predicateHolds().
7. .scale.none — the unknown state. Axis drawn, band drawn as a dashed outline, no tick, and
   "not read" set where the tick would be. An unread value is a hatch, never a dash and
   never a zero.

Verify: open a trial with a near miss and report the margin the dimension tag shows, then
confirm it matches marginPhrase() for the same rule. Open a trial with a flat fail and
confirm it has a wash and NO dimension line. Open one with an unread criterion and confirm
the hatch, not a dash. Report that no number in the rendered scale came from the markup.
tests.html still passes.
```

## Stage 3 Report

_Pending._

---

# Stage 4 — The subtraction

```
Deleting the three things on screen that claim a capability the app does not have. This
stage makes the app smaller and more honest, and it clears the slot Stage 5 fills.

1. The Health Score ring, home — index.html:974, the .ring-wrap block and its SVG with the
   hard-coded --off:534. Delete the markup; delete the countUp/countScore writes into #hs,
   #hsConf, #ring, #scoreNum that no longer have a target.
2. The score ring, trial detail — index.html:1203, same treatment. The score itself survives
   as thermal's small figure with its confidence line BELOW the scales, per docs/DESIGN.md
   §7.1: the score is a summary of the scales, so it does not outrank them.
3. The vitals block — index.html:1084 through the end of the fourth .vital. All four are
   hard-coded, none is read from a file, and garmin.json does not exist. Delete the markup
   and the CSS.
4. The gauge needle — index.html:1126 (id="needle") and the single --ang line in
   renderGauge() at index.html:3840. KEEP #gaugeStatus and #gaugeNote and everything that
   computes them: those counts are real.
5. Nine of the eleven .eyebrow labels — delete. The two that are engine-written, auditHead
   (1239) and tRelatedHead (1260), CONVERT to section headings keeping their ids. Deleting
   either breaks renderTrial().
6. Sentence case everywhere. No all-caps at any size.

Verify: grep index.html for "154", "62<", "Hydration", "ring-wrap", "eyebrow" and report
every surviving hit with its line and why it survived. Confirm renderGauge() still reports
its "n of N markers in range" line correctly. Confirm renderTrial() runs without a console
error. tests.html still passes. Report the new line count and file size — both must fall.
```

## Stage 4 Report

_Pending._

---

# Stage 5 — The lead card

```
What opens the app, replacing the ring Stage 4 deleted. THE AGREED CASUALTY: if the freeze
weekend runs short, cut this stage and put thermal's score-and-confidence block in the slot
instead. Do not half-build it.

The lead card is the single smallest margin the engine found ANYWHERE in the corpus, named
in full. No other matcher computes this, and it is the one thing on screen a person could
take to an appointment.

1. A reduce over RANKED (index.html:3430) for the minimum shortfall across every trial and
   every rule in the corpus. shortfall() is at 3036 and headroom() at 3344; use them rather
   than recomputing. Exclusions and unread criteria are not candidates — only a near miss on
   something the engine actually read.
2. Render thermal's .lead: the quantity at --t-display with its unit, the sentence beneath,
   and the full dimensioned .scale.near under both.
3. The sentence is docs/COPY.md's applied draft E — which marker, which direction, whose
   rule. Six words. "Ferritin, below the minimum for NCT06942208." GENERATE it from the
   winning rule; do not write it into the markup. The marker name, the direction word and
   the NCT id all come from the engine.
4. Handle the empty cases honestly: no documents yet gets thermal's empty state ("No
   documents yet" + one action, no illustration, no centred icon circle); documents but no
   near miss anywhere gets a different true sentence, NOT a fabricated margin.
5. One filled button on the screen, on the single thing worth doing.

Verify: report the margin the lead card shows and the trial it names, then confirm by hand
that no other rule in the corpus has a smaller shortfall. Delete a lab value from the
profile and report that the card changes to a different marker or a different trial. Clear
all documents and report that the empty state appears rather than a zero or a blank. Confirm
the sentence is assembled from engine output and appears nowhere as a literal in the markup.
```

## Stage 5 Report

_Pending._

---

# 🔒 FEATURE FREEZE — end of day Sunday, October 18

**After this point: restyling, verification and bug fixes only.** No new screens, no new
trials, no new animations. Stages 6 and 7 are freeze-legal because neither adds a feature —
Stage 6 changes how existing engine output is drawn, and Stage 7 only verifies.

---

# Stage 6 — Audit and trial rows

```
Freeze-legal: this restyles output the engine already produces and adds nothing. Runs
Mon Oct 19 to Wed Oct 21, alongside the video script.

1. Audit rows to thermal's treatment: the criterion, the value, the verdict mark, and the
   expand that opens the trial's own sentence VERBATIM with its citation. The quote bar is
   the only indent in the system.
2. Sort not-read rows FIRST. They are the ones a person can still do something about, which
   is the same logic that makes the dimension line appear on near misses and nothing else.
3. The near miss is the only row that carries a fill. Nothing is numbered — a trial's
   criteria are a set, not a sequence.
4. Verdict marks pair a shape, a word and a position, so none needs colour to be read. The
   patient-side wording ships: "Not read" rather than UNKNOWN, "Not met" rather than FAIL.
5. Trial rows trade the percentage for the tally — "9/11 criteria met" — which reports what
   the engine actually checked and leaves no room to read a number as a chance of getting
   in. Unread criteria stay visible on the row instead of being folded into the count. The
   near-miss chip carries the margin itself, not the words "near miss".

Verify: open a trial and report the row order, confirming every not-read row precedes every
decided one. Expand a row and confirm the quoted sentence matches the corpus record
verbatim, including its punctuation. Report the tally for two trials and confirm each equals
the engine's decidable count. Run the greyscale check and report that all four verdicts are
still distinguishable. tests.html still passes.
```

## Stage 6 Report

_Pending._

---

# Stage 7 — Coherence, verify, and freeze

```
No new work. This stage closes the port and hands off to the video.

1. Accessibility pass: keyboard nav through all five screens, visible focus rings,
   prefers-reduced-motion honoured, roles verified. Thermal specifies exactly one
   orchestrated motion — the measurement resolving — and nothing else in the app moves on
   its own. Confirm that is true: no section entrances, no card hovers, no animated ring.
2. Persistence: localStorage for last-viewed marker, every access in try/catch with a
   working no-storage fallback.
3. Run /design-review and /qa-only. Fix what they find.
4. Cross-device: real iPhone, real Android, desktop. Phone width with no horizontal scroll
   is the one that matters.
5. Grep the whole repo for the retired constants — "87/100", "89", "79/100", "CGX Trial #4",
   "Jordan Reyes", "Doctors Available", "r4.smarthealthit.org" — and report every hit.
6. Confirm the docs match the app that exists: CLAUDE.md's three-tab description, its table
   of what is real, docs/README.md's doc count, and docs/ROADMAP.md's rubric row.

Verify: report the network request count (0), the contrast ratios for ink, ink-2 and ink-3
on the new ground, the result of the greyscale pass, and the full output of the retired
constants grep. Confirm tests.html passes all 61 cases. Screenshot all five screens at phone
width and at desktop width.
```

## Stage 7 Report

_Pending._

---

# After These Stages

- The app is drawn in one system, end to end, and the system is the one `docs/DESIGN.md`
  actually describes. There is no second Tolerance.
- **Nothing on screen claims a capability the app does not have.** The ring that averaged
  invented numbers, the four vitals that were typed into the markup, and the needle that
  pointed at nothing are gone. What is left is measured.
- The per-criterion audit — the thing `CLAUDE.md` calls the product — is drawn as a
  measurement against a tolerance, with the near miss dimensioned, because the near miss is
  the most useful thing the engine computes and no competitor shows it.
- **Still true, and still the honest limitation:** there is no backend. The corpus is
  committed, the OCR runs in the browser, and the page makes zero network calls at runtime.

**What this log deliberately does not deliver**, so the video does not claim it:

- **The Garmin rail.** Cut. `garmin.json` does not exist and the vitals that implied it are
  deleted rather than left standing.
- **The appointment prep sheet.** Not in this log. It is V2 Stage 4 and is still `_Pending_`.
  It is ~1 day, it is the only file the app would produce, and `docs/SIMPLIFY.md` §9's third
  judge answer leans on it existing. **Decide on the night of Sunday Oct 18**, with the
  freeze weekend's actual pace in hand — and if it is cut, cut it from the video script in
  the same sitting.
