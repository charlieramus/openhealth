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

Documentation only, as specified. Two files changed — `docs/DESIGN.md` and `CLAUDE.md`.
`git status` shows nothing else modified.

**1 · §7.2 repainted, read out of the gallery rather than retyped.** The single-table
palette is replaced by thermal's three layers, taken from `mockups/thermal.src.html`'s
`:root` block: the zinc primitives (`--zinc-050` → `--zinc-900`), the heat family
(`--h-wash` `#FFF2EC`, `--h-out` `#FFE2D4`, `--h-tint` `#FFD3BC`, `--h-flare` `#F2541B`,
`--h-sig` `#D7122A`, `--h-deep` `#7F1026`), the four marker hues (`--m-fe` `#B01E5B`,
`--m-hgb` `#E2561F`, `--m-o2` `#C8860A`, `--m-ldl` `#6E2250`) and the semantic aliases.
**The rule is kept verbatim** — your value is ink, the requirement is a tint, the gap is the
only thing in signal colour — because the repaint moved hexes and nothing else.

Two things worth having in writing before Stage 2 repoints the alias band, both found by
grepping the gallery rather than assumed:

- **`--paper` and `--sheet` swap meaning.** In the retired v1 palette `--paper` was the
  canvas *behind the device* and `--sheet` was the app background; in thermal `--paper` is
  the page and `--sheet` is white. Written into §7.2 as a named trap, since those two
  aliases are referenced from static markup.
- **`--h-flare` is defined and unspent** outside the ramp swatch, and `--h-deep` has
  exactly two uses (`.vd.missed svg`, `.verd b`). Recorded so neither gets treated as a
  surface colour on the way in.

**2 · §7.3 is one face.** Inter, four weights (400/500/600/700), embedded as base64 by
`mockups/build.py` — which already exists, already fetches nothing at runtime, and already
has its four woff2 subsets committed at `mockups/fonts/` (~90KB before encoding). The
mono-for-quantities restriction and the two-face stack are **deleted**, and the replacement
rule is stated in their place: quantities get `font-variant-numeric: tabular-nums` and
`-.02em` tracking. The scale table is thermal's seven steps (`--t-display` 40px →
`--t-micro` 11.5px) instead of v1's `--t-quant-xl`/`--t-tick` set, and the `'Inter Fallback'`
metric-matched face is documented so the first-paint reflow question does not get reopened.

The verify asks that §7.3 carry no reference to IBM Plex Mono or to a second typeface.
**It carries neither** — no occurrence of "Plex" or "IBM" in the section. Two occurrences of
the word "mono" survive and both exist to argue *against* a second face: the sentence
deleting the rule, and the §4 citation (*"a monospace face for small data labels"*) that is
the reason one family ships. Removing that citation would delete the argument, so it stays.

**3 · §1 is four retired directions**, not three. Heading changed and row 4 added —
Tolerance v1 cool blue, `#E7ECEE` paper and `#B81D40` signal, retired 2026-10-16 with the
reason stated: two Tolerance palettes contradicted each other in the repo, and the mono rule
was itself the §4 tell. The row says plainly that the **system** survives and only the paint
and the second face are retired, so nobody reads row 4 as Tolerance being dead.

**4 · §7.9 closed, both items.** The Plex Mono subset item is closed as obsolete. The fake
vitals item is closed with the deletion decision and a pointer to Stage 4 of this log —
**and corrected on a point of fact**: it named three tiles (`Resting HR 62`, `Weight 154 lb`,
`Hydration 6 glasses`) and there are **four**. `Oxygen 97` was missing from the list. The
closure text names all four with the markup location (`index.html:1086` and down), because
Stage 4 has to delete what is actually there rather than what the doc remembered.

**5 · `docs/ROADMAP.md` needed no edit — the condition already holds.** Line 56 reads
*"**3, corrected 2026-10-16 from 5.**"* with the reason in one clause (score ring over
invented numbers, four hard-coded vitals, the gauge needle, eleven all-caps eyebrows) and
`UPDATELOGV3.md` named as what recovers it; the rubric summary at line 254 agrees. That
landed in `f6e7ae1`, the Oct 19 commit of the untracked design work. Grepped for the old
assertion — *"strongest box"* appears nowhere in `docs/` or `CLAUDE.md`. **This is the one
spec item that produced no diff**, and it is reported rather than restated as work done.

**6 · `CLAUDE.md` is honest about the Garmin rail.** The `Vitals | Real` row now reads
**Cut 2026-10-16**, states that the rail was never built, and says the four hard-coded tiles
are deleted rather than relabelled. The three-tab description is untouched, as the spec says,
because the tabs are real.

**Deviation, same file, same reason:** two other lines in `CLAUDE.md` asserted the same
thing the Vitals row did. Line 45 said the corpus **and `garmin.json`** are committed files,
and the Efficiency note at line 114 said *"`garmin.json` holds the operator's real fitness
data and is committed in the clear."* Neither is true — the file does not exist in the repo.
Fixing one row and leaving two is the failure mode the stage exists to prevent, so both are
corrected: the Python bullet now names the two scripts that do exist
(`scripts/build_corpus.py`, `mockups/build.py`) and says the `python-garminconnect` script
was never written, and the Efficiency note says plainly that no fitness data is committed
anywhere. The zero-network bullet also now says *"apart from the one CDN library above"*,
which is Tesseract.js and was already true of the shipping build.

**Deviation, `docs/DESIGN.md` §7.4 — two lines item 2 invalidated.** §7.4 described `.pin`
as carrying *"its value in mono beneath"* and `.gap` as a bracket in `--gap`. With the mono
rule deleted and `--gap` replaced by `--h-sig`, both would have contradicted the two
sections directly above them. Changed to "tabular figures (§7.3)" and `--h-sig`. No other
line of §7.4–7.8 was touched.

**Two self-inflicted errors, caught before commit, reported rather than quietly repaired.**
Inserting the §1 row shifted every later line by one, so the §7.2/§7.3 replacement — written
against line numbers read *before* the insert — ate the blank line above the §7.2 heading and
left the final line of the old §7.3 paragraph orphaned above §7.4. Both found by re-reading
the boundaries after writing, both fixed; §7.2 now opens at line 165 with its blank line
intact and §7.4 at line 291 with no orphan.

**Noted, not fixed, not this stage's call:** the file's header block still reads *"Status:
OPEN BRIEF, not an answer. Reset 2026-10-07"* while §7 locks a system and §7.2–7.3 now
specify it down to the hex. That is a coherence edit for Stage 7, not a palette decision,
and changing a status banner in a stage scoped to six named items would be scope creep.

### Verify

- **The four retired directions in §1:** 1 Dark theme · 2 Green-forward light · 3 Warm paper
  + serif · 4 Tolerance v1, cool blue.
- **§7.3 contains no reference to IBM Plex Mono and specifies no second typeface.** Grep of
  the section: `Plex` 0, `IBM` 0. The two surviving `mono` strings are the rule's deletion
  sentence and the §4 citation, quoted above.
- **New §7.2 `--h-sig`:** `#D7122A`.
- **`docs/ROADMAP.md` no longer asserts a UI score of 5** — line 56 reads
  `**3, corrected 2026-10-16 from 5.**`, line 254 reads `3`, and *"strongest box"* is gone
  from the repo.
- **No file outside `docs/` and `CLAUDE.md` touched** — `git status --porcelain` returns
  exactly `M CLAUDE.md` and `M docs/DESIGN.md`. No code ran and none needed to; `index.html`
  and `tests.html` are byte-identical to `f6e7ae1`.

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

The paint is thermal's. `index.html` 4454 → 4641 lines, 162KB → 392KB, all of the growth
being the four Inter weights now travelling inside the file.

**The spec's item 1 could not be executed literally, and this is the one thing in this stage
worth reading carefully.** "Replace `index.html` lines 13–935 with the stylesheet from
`mockups/thermal.src.html`" assumes the two sheets cover the same ground. They do not. I
inventoried both before touching either:

```
index.html  <style>   191 class selectors   the app's markup + render functions use 177
thermal.src <style>    74 class selectors   the gallery uses 75
of the 177 the app uses, thermal defines 23 — and does not define 154
```

A wholesale paste would have left **154 classes unstyled** — the device shell, the five
screens, the scroll track, the tab bar, the OCR panel, the manual-entry form, the document
rows, the print block — which is a total collapse, not a repaint, and it would have failed
this stage's own verify on the first line. The gallery is a component sheet; it was never
the app's sheet.

**What the swap actually is, and why that is still the whole system.** The v1 sheet was
already Tolerance, in the same token vocabulary (`--paper`, `--sheet`, `--ink`, `--rule`,
`--m-*`, `--t-*`, `--r-*`, `--pad`). So the system swapped at the token layer and the type
layer, where a system lives, and every one of those 191 rules repainted with it:

1. **The face.** Four weights of Inter as base64 `@font-face`, plus the metric-matched
   `'Inter Fallback'`, between `/*INTER_FACES:BEGIN*/` and `/*INTER_FACES:END*/` markers.
2. **`:root` replaced** with thermal's three layers verbatim — eight zinc primitives, the
   six-step heat family, the four marker hues, the semantic aliases, `--pad` 20px → 22px,
   `--r-tag` 4px.
3. **The type scale replaced** with thermal's seven steps. `--t-h1` 1.375rem → 1.75rem,
   `--t-h2` 1.0625 → 1.1875, `--t-small` .8125 → .84375, and `--t-display`/`--t-micro`
   taking over from `--t-quant-xl`/`--t-tick`.
4. **`body`** is now `400 var(--t-body)/1.6 var(--f)` with Inter's `cv05`/`cv11`/`ss01`
   alternates set once, and `text-rendering:optimizeLegibility`. The grid rows/columns line
   is untouched — it is load-bearing below 404px and the comment saying so is still there.
5. **The mono rule is gone at the root.** `--mono` now resolves to the Inter stack, so the
   35 `font-family:var(--mono)` declarations further down the sheet stop being a second face
   without 35 separate edits, and `.n` picks up thermal's
   `tabular-nums` + `-.02em` + 600. Those 35 declarations are now no-ops and can be deleted
   in Stage 6 or 7; leaving them in this stage kept the diff reviewable.
6. **The four hardcoded v1 literals** that were not tokens: the near-miss callout's
   `#FDF4F6`/`#F0D3DA` and the near verdict chip's `#FDF4F6` became `--h-wash`/`--h-out`,
   the ink button's `#0E1720` hover became a `color-mix` off `--ink`, and the device bezel's
   two near-blacks and its drop shadow were rebased off zinc. **Grep confirms no retired v1
   hex survives anywhere in the file** — the only three matches for the old palette are
   prose in comments saying it is retired.

**The alias band is kept and repointed, per item 2.** All nineteen aliases plus the six the
v1 sheet itself used (`--card`, `--inset`, `--band`, `--gap`, `--mono`, `--sans`,
`--t-quant-xl`, `--t-tick`, `--r-chip`). Nothing was deleted without grepping: a scripted
pass over every `var(--x)` in the file against every token defined in `:root` reports
**zero undefined tokens**, with `--c`, `--from`, `--to`, `--at`, `--tint`, `--i` and `--ang`
excluded as locals the markup and render functions set inline. `--brand` and `--brand-d`
still resolve to ink; no green came back. `--gap` resolves to `--h-sig`, so every rule that
drew the signal still draws it, now in `#D7122A`.

**Item 3 — the engine's class names.** Checked by reading what the render functions actually
emit rather than by trusting the list: `.scale`, `.scale none`, `.scale excl`,
`.scale-legend`, `.arow`, `.arow miss`, `.vchip pass|fail|near|unk|weak`, `.band`, `.pin`,
`.gap`, `.chip`. **All of them already exist in this sheet and all of them still do.** The
spec's list also names `.audit-row`, `.vd`, `.trial` and `.tally`, which this app does not
emit at all — they are thermal's names for rows the app currently draws as `.arow` and
`.row-item`. They are now defined too, so Stages 3 and 6 have a drawing to render into, but
nothing on screen uses them yet.

**Item 4 — one rename, and five deliberate non-ports.** Collisions were checked by name,
not assumed:

- **Renamed:** thermal's `.lead` (the heat-wash insight card) → **`.leadcard`**. `.lead`
  already means a paragraph of intro copy on the manual-entry screen, and importing
  thermal's would have painted that paragraph as a heat card. Exactly the b4149dc failure
  mode, caught before it shipped.
- **Not ported: `.btn`, `.nav`, `.tabs`.** Thermal paints all three in `--h-sig`. §7.2
  reserves the signal colour for the gap, so chrome does not get to spend it — a red primary
  button would be the single biggest thing on the screen wearing the one colour the near-miss
  owns. The app's ink button and ink tab mark stay. This is a deviation from the gallery and
  it is the gallery that is wrong here, because a gallery has no navigation to compete with
  its own annotation.
- **Not ported: `.score`, `.conf`.** Both collide with layout the render functions depend
  on (`.score` is a column here; `.conf` is the confidence line inside it). Stage 5 or 6 can
  port them knowingly.
- **Not ported: thermal's `.scale .band` and `.scale .pin`.** Same selectors, different
  positioning model — the gallery drives them off `--from`/`--to`/`--at`, this app writes
  inline `left`/`right` from `axisPct()`. Swapping them blind would have silently broken
  every scale on every screen. **The scale is Stage 3's job**, so its existing two rules are
  untouched and thermal's new sub-parts (`.axis`, `.out`, `.edge`, `.ext`, `.dim`, `.noread`,
  `.scale-wrap`, `.scale-head`) are added alongside, unused, ready for it.

**`mockups/build.py` gained `--into`,** which is the only file outside `index.html`'s
`<style>` that this stage changed. It rewrites a page in place between the two markers
instead of copying src → out, so `python mockups/build.py --into index.html` is idempotent
and the app stays a single file with no build step of its own. This is the same arrangement
`scripts/build_corpus.py` already uses for the corpus, down to the BEGIN/END marker pair.
The gallery path (`thermal.src.html` → `thermal.html`) is unchanged and still works.

**One more comment edited outside `<style>`, deliberately.** The five-line HTML comment above
the stylesheet still said the system "runs on a system sans + system mono stack" and that the
Plex subset "gets embedded as base64 when it lands". Both became false the moment Inter
landed. A comment is not behaviour, but leaving a lie in the file is the thing this log is
for, so it now says what is actually there.

### Verify

- **All five screens render, no missing-style collapse.** Measured, not eyeballed: all five
  `.screen` elements report a 404px box with populated `.screen-inner` (3, 8, 9, 6 and 9
  children). Screenshots taken at 430×940: **Home** (wordmark, score, three tinted marker
  scales with ink ticks), **Metrics** (marker switch, the seven-draw chart with the dashed
  `12 floor` limit in signal red), **Trials** (the score/confidence pair, chips, audit rows
  with verdict chips), plus **Add records** and **Here's what we read**, the two document
  screens behind the Metrics tab.
- **The three tabs navigate.** Home → Metrics → Trials driven by clicking the real tab bar;
  `go(3)` and `go(4)` reach the two document screens.
- **`tests.html`: `all 61 passed`.** Served over `python -m http.server 8731`, which is what
  the harness needs — it drives the shipped engine through an iframe, so this is the engine
  in `index.html`, not a copy.
- **Network requests: zero beyond the page itself.** The tab records one GET for
  `index.html` and three `data:` entries, which are the embedded faces — no HTTP font
  request, no CDN, no API. (Chrome also logs two `chrome-extension://` requests; those are
  the automation extension, not the page.) `document.fonts` reports Inter 400/600/700
  loaded, 500 present and not yet needed.
- **No console errors or exceptions.**
- **File size: 392KB** (401,971 bytes), up from 162KB. 88KB of woff2 becomes ~118KB of
  base64 per the four weights. `<style>` now spans lines 13–1122.

**Two things this stage changed that Stage 4 and Stage 6 should expect.** The type scale is
larger than v1's, so (a) the nine surviving `.eyebrow` headings now set at 19px and wrap to
two lines on the trial screen — Stage 4 deletes nine of the eleven, which removes most of
them; and (b) the trial screen's `h1` is now 28px, and a 90-character registry title clamps
to three lines and takes about a tenth of the screen. Both are honest consequences of
thermal's scale rather than bugs, and both are cheaper to judge once Stage 4 has taken the
subtraction pass through. Flagging rather than quietly re-tuning a token this stage just
landed.

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

`auditScale()` now draws thermal's dimensioned scale, and it lands on every audit row in the
app at once, as the spec said it would. One function rewritten, one row-renderer line
changed, three CSS blocks added.

**The drawing, in the order the function emits it.** `.axis` hairline across the full width,
then the band, then the threshold labels, then — only if the verdict earns it — the
annotation, then the tick last so it stays the highest-contrast mark on the scale.

**Item 5 is the stage, and it is verified across the whole corpus rather than on one row.**
Heat tracks actionability:

```
all 23 trials, driven through the real screen renderer via openTrial():
  18 trials draw at least one scale
   2 dimension lines in the entire corpus   <- near misses, and nothing else
   5 .out washes                            <- flat fails, no dimension on any of them
   6 unread hatches                         <- no value on file
```

Two dimension lines, on exactly the two rows the engine calls `NEAR_MISS`. No flat FAIL
anywhere in the corpus grew one. The predicate that guarantees it is a named function,
`hasDimension()`, rather than a condition inlined twice — so when Stage 6 touches the row,
the rule is in one place.

**Item 4 — the tag carries `marginPhrase()`'s own words, not a second computation.**
`auditScale()` calls `marginPhrase(rule, v)` and puts the string in the tag that breaks the
line. Verified against a path that shares no code with it: on `NCT04485871` the tag reads
**`2.6 kg/m2 short of it`** and the near-miss callout above the table, which is built by
`gapOf()`, reads *"you are at 22.4 kg/m2, short by 2.6 kg/m2."* Same number, two renderers,
one source.

**One row-renderer change, and the reason for it.** The `.ev` cell printed `marginPhrase()`
too, so a near-miss row would have stated its own margin twice, once in the tag and once in
the cell twenty pixels below. The cell is now suppressed when a dimension is drawn, and only
then — a flat fail keeps it (`2.1 g/dL outside it` on `NCT05226169`), and so does every rule
with no scale at all. That is the only line outside `auditScale()` that this stage touched.

**Item 2 — the thresholds carry the numbers, with the unit on the outer label only.** A
two-sided band labels `25` and `40 kg/m2`; a one-sided rule labels its single threshold with
the unit (`11 g/dL`, `5.6 %`). The label carries the sheet colour, so the extension line
passing behind it breaks for the text, which is the drafting convention thermal is quoting.

**Item 6 — the exclusion inversion is preserved and is visibly doing its job.** The shaded
region on an exclusion is still the disqualifying zone, still hatched, and the gap still
follows the verdict rather than `predicateHolds()`. One correction inside that: the old
function picked the threshold by `value < lo`, which on an exclusion the patient is *inside*
picked the wrong edge. It now takes the crossed threshold when the value is outside the band
and the **nearer** one when it is inside, which is the distance `marginPhrase()` is already
describing in words for that case ("inside the excluded range"). Visible on `NCT04485871`
row 2: `Hemoglobin < 12 g/dL` as an exclusion, hatched band, tick outside it, **Pass**.

**Item 7 — the unknown state draws, where it used to draw nothing.** The old function
returned `''` for a rule with no value on file. It now emits the band as a hatch with a
dashed edge, both thresholds still labelled, no tick, and `not read` set where the tick
would be. Verified on the load-bearing case: `NCT06894004`, `HbA1c ≤ 5.6 %`, value cell `No
HbA1c on file`, scale class `scale dimd unread`, band background a
`repeating-linear-gradient`, `pin` absent. **A1c is still the UNKNOWN test case and it is now
drawn rather than omitted** — a hatch, never a dash, never a zero.

**Scoping, so nothing else moved.** Thermal's geometry (62px, 104px on a near miss, band at
`top:22px`) is scoped to `.scale.dimd`, which only `auditScale()` emits. The compact marker
scales on Home and in the Metrics list keep their v1 drawing until Stage 6 looks at them, so
this stage changed exactly one screen. The v1 `.gap` bracket is no longer emitted anywhere;
its animation rule, which would have become dead, was repointed to the extension lines and
the dimension sweep (`ext-drop` → `dim-sweep` → `tag-land`, the one orchestrated moment).

### Verify

- **Near miss:** `NCT04485871`, rule `BMI 25–40 kg/m2`, value `22.4 kg/m2`, chip `Near miss`,
  scale class `scale dimd near`, dimension tag **`2.6 kg/m2 short of it`** — matching the
  independently-rendered callout's `short by 2.6 kg/m2`.
- **Flat fail:** `NCT05226169`, rule `Hemoglobin < 11 g/dL`, value `13.1 g/dL`, chip `Fail`.
  `.out` wash present, **`.dim` absent**, tick still ink. Corpus-wide: 5 washes, 0 dimensions
  on fails.
- **Unread:** `NCT06894004`, `HbA1c ≤ 5.6 %` — hatch, `not read`, no tick, threshold still
  labelled.
- **No number in a rendered scale comes from the markup.** The static markup between
  `</style>` and `<script>` contains **zero** `.scale`, `.band`, `.pin`, `.edge`, `.dim`,
  `.out` or `.axis` elements — `#auditTable` is an empty `<div>` — and the only literal
  matches for the numbers on screen are SVG `stroke-width="2.6"` attributes on icons.
- **`tests.html`: `all 61 passed`**, re-run after the rewrite.
- JS re-parsed clean (`new Function` over the whole script block) before the browser ever
  loaded it.

**Found while verifying, out of scope, and it needs a decision — flagging rather than
fixing.** The near miss above is computed from `PROFILE.facts = { age:34, bmi:22.4 }` at
`index.html:1872`. **Those are the retired synthetic patient's numbers** — `CLAUDE.md` names
"Jordan Reyes, age 34, BMI 22.4" as deleted, and V1 Stage 1 deleted the character, but these
two facts survived the strip-out and are currently producing real verdicts on real trials.
Either they are the operator's own age and BMI, in which case the coincidence is unfortunate
and the comment above them should say so, or they are Jordan's, in which case a retired
fixture is driving the audit and they have to go. That is a data question only the operator
can answer, and deleting two facts changes engine output on every trial that asks about age
or BMI, so it is not a change to make inside a drawing stage. **Stage 4 is the subtraction
stage and is the right place for it.**

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

Everything in the spec is deleted, plus one thing the spec did not know about. `index.html`
4722 → 4646 lines, 401,496 → 399,431 bytes. **Both fell**, which is the point of the stage;
the byte drop looks small only because the four Inter weights now account for three quarters
of the file.

**1 · The Health Score ring is gone, and the score moved below the stack.** The 216px SVG
and its hard-coded `style="--off:534"` are deleted from the markup, and so is the
`renderHealth()` line that wrote into `.ring-prog`. The score survives exactly as
`docs/DESIGN.md` §7.1 asks — a small figure with its confidence line, **below** the three
tolerance scales rather than above them, because it is a summary of them and must not
outrank them. `#hs`, `#hsConf` and `#hsTrend` keep their ids; the wrapper is now `.figure`,
since a class called `.ring-center` with no ring in it is the kind of residue this log
exists to remove.

**2 · The trial-detail ring is gone** the same way, and with it the `#ring` write in
`renderTrial()`. The two numbers still sit side by side in two shapes with two labels, which
was always the honest part of that card.

**3 · The vitals are deleted, not relabelled.** All four tiles — `Resting HR 62`,
`Oxygen 97`, `Weight 154`, `Hydration 6` — with their hand-drawn SVG sparklines, and the
`.vitals`/`.vital` CSS block with them. A comment stands where they were, naming what was
there and why it went, so the deletion is legible to anyone reading the file later rather
than looking like something that was never built.

**4 · The needle is gone, and so is the dial it sat on.** The spec names the `<g id="needle">`
and the one `--ang` write. I deleted the whole `<svg>`: the dial was already
`display:none` under `.gauge-wrap svg`, so leaving a hidden dial behind to delete its needle
would have left dead markup claiming a component that renders nothing. `#gaugeStatus` and
`#gaugeNote` and everything that computes them are untouched and still correct — the card now
reads **`Leaning low`** over **`3 of 4 markers in range · 1 outside · 1 marker never drawn`**,
all four figures counted from `labStates()`. The `tilt` variable, which existed only to feed
the needle's angle, went with it, and the comment above `renderGauge()` no longer describes a
dial that is not there.

**5 · Eight eyebrow labels deleted, two converted.** `auditHead` and `tRelatedHead` are now
`<h2>` elements with their ids intact, so `renderTrial()`'s two `textContent` writes still
land. **A correction on the count: there are ten in the file, not eleven.** The spec and the
CSS comment both said eleven; `grep` finds ten, and I did not go looking for a phantom
eleventh to make the number match. With all ten gone the `.eyebrow` class has no users at
all, so its two CSS rules went too.

**6 · Sentence case holds.** No all-caps label survives; the two converted headings are
sentence case, and nothing in the deleted set was replaced with a caps variant.

**7 · The last of the synthetic patient — the thing the spec did not know about.**
`PROFILE.facts` was `{ age:34, bmi:22.4 }` at `index.html:1872`. Those are **Jordan Reyes's
numbers**, which `CLAUDE.md` lists as retired; V1 Stage 1 deleted the character but these two
facts survived and were still deciding real verdicts on every trial that asks about age or
BMI. Raised with the project owner rather than decided here, and the answer was **delete
them**. `facts` is now `{}`, with a comment saying why, and a criterion with no fact on file
evaluates UNKNOWN — the same rule a1c already proves, now applied to two more inputs. Both
are addable through the manual-entry screen, which is the honest path: the app's own input
rail, not a literal in the source.

**8 · Two retired-green strokes, while in the neighbourhood.** `stroke="#12301C"` appeared
twice on visible SVG icons and is dark green from the theme retired on 2026-10-07. Now
`currentColor`. **This also corrects a claim in the Stage 2 report**, which said no retired
hex survived anywhere in the file: that grep covered the v1 Tolerance palette, not the older
green one, and these two were outside `<style>`.

### Verify

The spec's own grep, every surviving hit and why:

| Term | Hits | Why it survived |
|---|---|---|
| `154` | 1 — line 1271 | Inside the comment that records what the vitals block held. No tile, no value |
| `62<` | 0 | — |
| `Hydration` | 1 — line 1271 | Same comment |
| `ring-wrap` | 0 | — |
| `ring-prog` / `ring-center` | 0 | — |
| `eyebrow` | 1 — line 256 | The CSS comment recording that the class and its rules were removed |
| `needle` | 3 — lines 628, 956, 1278 | All three are comments: the gauge CSS note, the retired-animation note, and the marker left where the dial stood |

Confirmed in the running app, not by reading:

- `.ring-wrap`, `.ring-prog`, `.ring-center`, `.vitals`, `.vital`, `#needle`, `.needle`,
  `.eyebrow` and `.gauge-wrap svg` all return **0 elements**. `#auditHead` and
  `#tRelatedHead` are both `H2`.
- **`renderGauge()` still reports its real line:** `3 of 4 markers in range · 1 outside ·
  1 marker never drawn`.
- **`renderTrial()` runs clean on all 23 trials** — every trial opened in sequence through
  `openTrial()`, no exception thrown, no console error.
- **Home reads as §7.1 specifies**: three tolerance scales first, then `99` with
  `4 of 5 markers` and the trend line beneath them.
- **`tests.html`: `all 61 passed`**, including the case that asserts a1c is absent from the
  shipped profile — which still holds with `facts` emptied.

**The cost of item 7, stated plainly, because it is larger than it looks.** Emptying `facts`
changed engine output across the corpus:

```
                before      after
dimension lines      2           0
.out washes          5           2
unread hatches       6          26
```

**There is now no near miss anywhere in the corpus on the shipped profile**, which means the
dimension line — Stage 3's whole subject, and the most distinctive thing this app draws — has
nothing to draw on the app as it stands. That is an honest result, not a regression: both
near misses were computed from a retired fixture's BMI, so the app was showing its best
screen on invented data. But it has a direct consequence for **Stage 5, whose lead card is
specified as "the smallest margin across the whole corpus"**, and for the video. The fix is
real data, not a code change: entering a real age and BMI through the manual-entry screen
restores genuine age and BMI verdicts, and any near miss among them is then a true one.
Flagged for the project owner at the end of this stage rather than worked around.

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

Built, not cut. The slot the ring vacated now holds the smallest margin the engine found
anywhere in the corpus, and the card re-derives from the profile every time anything is
added.

**1 · The reduce.** `leadMargin()` walks `RANKED`, takes each trial's `result.nearMisses`,
and keeps the minimum `shortfall(rule, value)` — the evaluator's own function, so the card
and the audit row can never disagree about a distance. Candidacy is narrowed exactly as the
spec says: numeric and range rules only, **no exclusions** (an exclusion is not a distance
you can close) and **nothing unread** (an absent value has no distance at all). A card that
ranked flat fails by size would be pointing at the trial you are furthest from.

**2 · The card** is thermal's `.leadcard` — renamed from `.lead` in Stage 2 to avoid the
manual-entry paragraph of the same name — with the quantity at `--t-display` in signal
colour, its unit beside it, the sentence beneath, and **the full dimensioned
`.scale.dimd.near` from Stage 3** under both. One thing was adjusted on arrival: the
threshold label breaks the extension line behind it, and that break is now `--h-wash` rather
than `--sheet`, or it renders as a white chip sitting on the card's own wash.

**3 · The sentence is generated, in six words.** `leadSentence()` assembles
`ANALYTE_LABEL[analyte] + direction + 'for' + nctId`, where the direction is read off the
rule's shape (below the minimum / above the maximum). `docs/COPY.md` §3.1 caps this slot at
twelve words and C8 forbids a typed number; this is six words and carries no number at all,
because the quantity above it is the number. **Grep confirms the sentence exists nowhere as
a literal:** zero matches for `below the minimum for NCT` in the whole file; the only
occurrence of either direction phrase is inside `leadSentence()` at line 3945.

**4 · Both empty cases are real branches, and one of them is what currently ships.**

- **No near miss anywhere** → `No near miss` over *"Across 23 trials, every criterion read
  is met or missed outright."* — eleven words, with the 23 interpolated from `RANKED.length`
  rather than typed. **This is the live state of the app after Stage 4**, because emptying
  the synthetic patient's `facts` removed the only near misses in the corpus. The card says
  so instead of inventing a margin, which is the whole point of the branch.
- **Nothing read at all** → `No documents yet` + the one action. Honest limitation,
  reported rather than claimed: **this branch cannot be reached in the shipped build.** Its
  condition is `healthScore() === null`, and `MARKERS` ships with the operator's committed
  lab values, so the score is never null. The same condition gates `#firstRun`, which means
  that button has been unreachable since it was written. The branch is correct by reading
  and by the condition it shares with existing code, but I did not see it render and am not
  going to say I did. **Noted for Stage 7.**

**5 · One filled button.** The lead card carries it, and it is on the single thing worth
doing: `Open NCT…` when there is a margin to look at, `Add a document` when there is not.
The "See details" pill stays ghost, and `#firstRun` only ever appears in the unreachable
branch, so no screen shows two filled buttons.

### Verify

Driven through the app's own manual-entry rail — no values written into the source, which is
also the honest way to demonstrate the card re-derives.

- **The margin it shows, and the trial it names.** With BMI 24.1 entered: **`0.9 kg/m2`**,
  *"BMI, below the minimum for NCT04485871."*, dimension tag `0.9 kg/m2 short of it`, button
  `Open NCT04485871`.
- **Confirmed by hand that nothing in the corpus is smaller.** Every trial opened in sequence
  and every audit row read back: the corpus holds exactly **three** near misses —
  `NCT04485871` BMI 25–40 at **0.9**, `NCT07502508` BMI 25–40 at **0.9**, `NCT06897475`
  BMI ≥ 27 at **2.9**. 0.9 is the minimum. **Two trials tie at 0.9**, and the card takes the
  first in `RANKED` order because the comparison is strict (`s < best.short`) — so a tie goes
  to the better-ranked trial, which is the defensible way round. Worth knowing before someone
  reads the tie as a bug.
- **It changes when the profile changes.** BMI re-entered as 26.5: 25–40 becomes a PASS, and
  the card moves to a **different trial and a different rule shape** — `0.5 kg/m2`, *"BMI,
  below the minimum for NCT06897475."*, one-sided rule, one edge label `27 kg/m2`. Nothing
  about the card is pinned to a trial.
- **Clearing everything** returns the `No near miss` branch rather than a zero or a blank —
  that is the state the app loads in. The `No documents yet` branch is the unreachable one
  described above.
- **`tests.html`: `all 61 passed`.**

**One consequence to carry into Stage 6 and the video.** The lead card is the app's best
screen and it currently renders its fallback sentence, because the only near misses in the
corpus come from a BMI the operator has not entered. Entering one real age and one real BMI
through the manual-entry screen turns the card on with a true margin — that is a data
decision for the owner, not a code change, and it is the same point the Stage 4 report
closes on.

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

Built, and freeze-legal: nothing here adds a capability. The audit table is drawn the way
thermal draws a measurement, the rows are ordered by what a person can still act on, and the
two numbers on a trial row stopped being a percentage. Two defects were found on the way
through and both are fixed below.

**1 · The row is one button now.** `.audit-row` holds a `<button>` carrying the criterion,
the value, the verdict mark and a caret; `auditScale()` draws underneath it unchanged; and
the trial's own sentence sits behind the expand in `.source`, with a citation line reading
`NCT…, inclusion|exclusion, verbatim`. `toggleRow()` flips `aria-expanded` and the `.open`
class, so the control reports its own state rather than relying on the caret's rotation.

**2 · Not-read rows lead.** `VERDICT_ORDER` is now `UNKNOWN 0, NEAR_MISS 1, FAIL 2, PASS 3`.
A value you have not had drawn is a value you can go and get, which is the same reasoning
that puts the dimension line on near misses and nowhere else. `Array#sort` is stable, so
source order survives inside each group and a row can still be found in the registry text it
came from.

**3 · One fill in the table, and it is the near miss.** A flat miss is a hairline like
everything else — a fill reads as "act on this", and on a FAIL there is nothing to act on.

**4 · The patient's word, not the engine's constant.** `Met` / `Not met` / `Near miss` /
`Not read`. Each chip pairs a shape, a word and a position, so none of the four needs colour.

**5 · The tally replaced the percentage.** `listChip()` reports `met of decidable`, and the
criteria the parser could not read stay on the row as `n not read` instead of being folded
into the denominator. `nearChip()` carries the margin itself on the list row, because "near
miss" is already the verdict word on the row the chip opens — the only new information there
is how far.

**6 · Defect found: two CSS blocks were styling the same rows.** The block written for this
stage and an existing block further down both declared `.audit-row > button`, `.crit`,
`.val`, `.is-near` and `.is-near .caret`. The later block won every conflict, which meant the
new comment — *"it is 16px of card padding wide, not --pad"* — was describing the rule that
lost. It also mattered: `#auditTable` is `.card.audit` and `.audit` sets `padding:0 16px`,
but the surviving rule bled the fill by `var(--pad)`, 22px, so the near-miss fill overhung
the card's rounded edge by 6px a side. Resolved to one block, 16px kept, and the measured
result is below. The now-unreachable `.audit-row .margin` rule went with it — the row emits
`class="ev"` for that phrase, and a solid fill there would have broken rule 3 anyway.

**7 · Defect found: a bullet leaking into a quote.** `forDisplay()` stripped one leading list
marker. NCT07743983 publishes `* ● Previous diagnosis of type 1 diabetes…`, so the `●`
survived into the quoted criterion — in the one place in the app that claims to be verbatim.
The strip now repeats. **The parser's own `BULLET` (line 2687) was deliberately left alone:**
`findAnalyte` scans the whole string, so the leading marker changes no verdict there, and
re-validating rule extraction the week of submission is not worth a cosmetic gain.

### Verify

Driven with Playwright against the file as it ships. All 23 trials, not a sample.

- **Row order: 23 of 23 trials correct, zero violations.** Every not-read row precedes every
  decided row in all 23 audits. Printed per trial; e.g. NCT06942208 reads
  `Not read ×7 | Met | Met`, NCT05226169 reads `Not read ×6 | Not met | Met`.
- **Verbatim: 132 of 132 quotes.** Every quoted criterion is a contiguous substring of that
  trial's `eligibilityCriteria` once the registry's own markdown escaping is undone. 103 of
  the 132 are byte-identical to the raw record with no transform at all; the remainder differ
  only by the three things `forDisplay()` documents — unescaping, the list marker, and
  newlines collapsing to a double space. The 43 quotes in NCT06942208's unparsed bucket are
  verbatim on the same test. Expanded row 1 of NCT04485871 reads
  `Having a body mass index (BMI= 25-40 kg/m2)`, cited `NCT04485871, inclusion, verbatim`,
  and that string appears in the record byte for byte.
- **A quote that cites the right sentence, not just a real one.** For all 75 rows whose
  criterion names a topic that can be tested for (diabetes, cancer, pregnancy, smoking,
  anemia), the quoted block contains that topic. The single exception is NCT07775404's
  `Diabetes` row, which quotes `T1DM` — the registry's abbreviation, not a mis-citation.
  Worth knowing: where a sponsor nests criteria under a stem, the quote leads with the stem
  (NCT07729332's `No cancer history` opens `Known contraindications to phentermine:`), so the
  clause the row is about can sit a line or two into the quote. Verbatim, and correct, but
  it is the thing a judge is most likely to ask about.
- **Tally equals the engine's decidable count**, checked against `#confN` / `#confD`:
  NCT04485871 `1 met of 1` (of 31), NCT05226169 `1 met of 2` (of 25), NCT06942208 `2 met of 2`
  (of 52), NCT07502508 `0 of 0` → the `Nothing checkable` branch (of 13). The not-read figure
  on each row equals unknown rows plus unparsed criteria exactly — 6 + 24 = 30, 6 + 17 = 23,
  7 + 43 = 50, 7 + 6 = 13.
- **Greyscale: all four verdicts distinguishable with no colour.** Distinct words, distinct
  icons, and distinct border treatments — `Not read` dashed, `Met` solid outline, `Not met`
  solid ink fill with inverted text, `Near miss` solid outline on the one washed row.
  **Method note for Stage 7:** do not apply `filter:grayscale(1)` to `<html>` to check this.
  A filter makes the root a containing block and displaces the fixed phone shell, which cost
  an hour chasing a 17px left shift that does not exist. Screenshot untouched and convert the
  pixels.
- **The fill no longer overhangs.** Measured on the near-miss row: row rect sits 1px inside
  the card rect on both sides, which is the card's own border. It was 6px outside it.
- **Exactly one filled row** in the audit table when a near miss exists, counted from
  computed styles rather than by eye.
- **`tests.html`: all 61 passed.** **It cannot be run from `file://`** — it fetches
  `index.html` and prints *"Cannot reach index.html"* instead. Serve the directory
  (`python -m http.server 8731`) and open `http://127.0.0.1:8731/tests.html`. The page says
  so itself; this is recorded because the obvious way to open it is the way that fails.
- **Zero console errors or warnings** across all five screens, **zero non-`file:` network
  requests**, and **no horizontal scroll at 390px**.

**The near-miss state still has to be made, as Stage 5 said.** With the shipped profile there
is no near miss anywhere in the corpus, so `.is-near`, `nearChip()` and the fourth verdict
cannot be seen. Everything above was verified after entering **BMI 24.1** through the app's
own manual-entry rail, which produces `0.9 kg/m2 short of it` on NCT04485871 — matching
Stage 5's figure exactly, from a clean reload. **For the video, that entry has to happen on
camera or the app's best row never appears.** Still a data decision, still not a code change.

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
