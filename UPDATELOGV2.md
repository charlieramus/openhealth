charlie

# OpenHealth — Twelve Days to Freeze 2/2: The Hub and the Output
# Work on one stage at a time. Do NOT combine stages.

---

## Context

Read `UPDATELOGV1.md` first — it must be complete before this log starts, because every
stage here renders engine output that V1 produces. Then `docs/SIMPLIFY.md` §3 (the three
tabs), §5.2 (the Garmin pipeline), §6 (the Health Score definition), and
`docs/ROADMAP.md` Weeks 2–3 for the dates.

V1 made the app *read*. **This log is everything the user lives in between results** — the
three-tab hub that holds the engine, the watch data that sharpens the near-miss callout, and
the one real file the app hands you.

**A prep sheet = a real generated download: your values with dates, every failed criterion,
every near-miss with its exact gap, and the NCT numbers — the thing you take to an
appointment. The app never contacts a clinician.**

This log builds only the hub and the output. It does **not** touch the parser, the evaluator,
or the document rail — those are V1 and are frozen by the time this starts. It adds **no**
new trials, **no** condition input, and **no** network call.

**Everything in this log is cuttable, and the stage order is the cut order reversed.**
`docs/SIMPLIFY.md` §7 says: if days are lost, cut the prep sheet first, then the Garmin rail,
then the hub shell. So Stages 1–2 are the most defensible work here and Stage 4 is the first
thing to go. One tension to carry knowingly: `docs/SIMPLIFY.md` §9's third judge answer — *"it
does not contact your doctor; it prepares the sheet you take to one"* — leans on Stage 4
existing. **If Stage 4 gets cut, that sentence changes with it.** Do not claim the sheet in
the video and then not ship it.

## Decisions (carried from `docs/SIMPLIFY.md`)

- **Three tabs, not three screens:** Home, Metrics, Trials. Trials is still the product; the
  hub is how you live in it between results.
- **Health Score, per §6:** the weighted share of tracked biomarkers inside their reference
  range, with partial credit for near-range values, **markers with no value excluded from the
  score entirely**. A missing marker never counts as a pass — it lowers *confidence*
  instead, shown as "n of N markers" beneath the ring. Same two-number rule as the trial
  side, deliberately: one formula applied in two places is a much better answer to "explain
  your code" than two unrelated ones.
- **The Health Score is never an input to matching.** The engine reads the underlying values
  directly. Do not wire the ring into `matchScore`.
- **Garmin is a committed snapshot, not a live sync.** `garmin.json` is written by a local
  Python script (`python-garminconnect`) every few days — a build-time pipeline, **not a
  backend**; nothing listens on a port. The UI must say "Last synced N days ago" prominently
  rather than implying live data.
- **`garmin.json` holds the operator's real fitness data and is committed in the clear.**
  Deliberate, and noted in the README so collaborators aren't surprised. It is the operator's
  own fitness data — **it is not patient data**.
- **The prep sheet is generated, not mocked.** If the download is a placeholder file, the
  stage is not done — it gets cut instead. Per the project standard: a screen that looks like
  it does something it does not do gets deleted, not polished.
- **Design:** `docs/FIGMA-MAKE-PROMPT.md` is the written 10-screen spec and
  `Screenshot 2026-10-06 153715.png` is the home reference. **No Figma Make pass** — screens
  4, 5, 8, 9 and 10 get sketched directly in HTML, where a long analyte name or a three-digit
  score breaks the row immediately instead of looking fine in a picture. Tokens per
  `docs/DESIGN.md`; each biomarker keeps its own colour on every screen.
- **Never quote a score as a constant** — not the Health Score, not a match score. Both are
  engine output and both move with the profile.
- Medium feature: **five stages.**

---

# Stage 1 — Hub shell: three tabs and the Health Score ring

```
Rebuild the home screen per Screenshot 2026-10-06 153715.png and docs/FIGMA-MAKE-PROMPT.md
screen 1, and put the existing screens behind a three-tab shell.

1. Bottom tab bar: Home, Metrics, Trials. Pill-shaped, floating. Replace the current
   three-screen track (index.html:1268-1273) with real tab navigation, keeping the existing
   screens' content intact where it maps.
2. Home header: the OpenHealth wordmark left, a notification bell right. NO profile avatar —
   the synthetic patient was deleted in V1 Stage 1 and does not come back.
3. Health Score ring as the hero: concentric amber/orange ring, large black numeral, "Health
   Score" beneath, and the confidence line "n of N markers" directly under the number. The
   confidence line is non-negotiable — the score is computed only from markers that have
   values, and the app always says how many it had.
4. Three biomarker bars under the ring (Iron, Hemoglobin, SpO2): slim track, filled segment
   in the marker's own colour, label above, "value / range" beneath. A "See details" pill
   under them, clicking through to the Metrics tab.
5. Today card: date and a chevron, containing ONE full-width panel, "Records Captured", with
   document thumbnails and a "See more" link. There is no "Recent Chats" panel — delete it
   if present. Beneath it, a single row: "Prepare for your appointment ->" (it may be inert
   until Stage 4; if Stage 4 is cut, delete this row rather than leaving it dead).
6. Top trial match card: condition icon, trial name, condition + NCT ID, bookmark toggle,
   then three chips — the match score, the distance, and "Tap to view ->". The score is read
   from the engine, never written into the markup.
7. Empty / first-run state per spec screen 10: the ring reads "No data yet", NOT a zero. One
   primary action: "Add your first lab result". A missing value must never be able to read as
   a good result.

Verify: open the app and report the Health Score with its "n of N markers" line, then delete
a marker's value from the profile and report that BOTH numbers change correctly and the ring
never shows a zero for a missing marker. Confirm all three tabs navigate. tests.html still
passes. Report whether any number on this screen is a literal.
```

## Stage 1 Report

_Pending._

---

# Stage 2 — Metrics tab and marker detail

```
Per docs/FIGMA-MAKE-PROMPT.md screens 4 and 5. This is where the hub earns its place.

1. Metrics tab: a scrollable list of every tracked biomarker. Each row — marker name in its
   own colour, current value large, reference range beneath, and a small sparkline of its
   trend.
2. Group under two quiet subheads: "From your records" and "From your watch". The split is
   the provenance claim, visible without being explained.
3. Markers with no value show "Not measured" in a neutral style — never a zero, never a dash
   that could read as a result, never an empty bar. A1c is the standing test case: it is
   deliberately absent and must render as not measured here and as UNKNOWN in any audit.
4. Marker detail on tap: a large line chart of that marker over time with the reference range
   drawn as a soft shaded band behind it, current value large at the top.
5. Beneath the chart: which trials in the ranked list reference this marker, and whether the
   profile currently passes it. Read this from the V1 evaluator's verdicts — do not
   recompute it here, and do not hand-write it.

Verify: report every marker rendered, its source group, and its value or "Not measured".
Open the detail for one marker and report which trials it lists and the pass state for each,
then cross-check those against the audit table for the same trial so the two surfaces agree.
tests.html still passes.
```

## Stage 2 Report

_Pending._

---

# Stage 3 — Garmin rail

```
Real data, no server. Per docs/SIMPLIFY.md §5.2. This is the first stage to cut after
Stage 4.

1. Local Python sync script, off to the side, using python-garminconnect: writes garmin.json
   every few days. A build-time pipeline, NOT a backend — nothing listens on a port, and the
   app never calls it. Keep the script out of the published artifact.
2. garmin.json supplies resting HR, SpO2, HRV, sleep, and body composition. Commit it.
   Note in README.md that it holds the operator's real fitness data in the clear and that
   this is deliberate — it is the operator's own data, not patient data.
3. Reader in the app: load garmin.json at page load, fold the vitals into the same profile
   the engine reads, with 30-day trends.
4. The signature output: pair the lab number with the watch trend on the near-miss callout
   built in V1 Stage 5. "Ferritin is short by 2, and your resting heart rate has risen for
   three straight weeks" is the combination no competitor produces. Compute the trend
   direction and the streak length — do not write the sentence by hand.
5. Connected sources screen per spec screen 9: a Documents card (how many captured, when the
   last one was added, a button to add more) and a Garmin card (connection state, the list of
   metrics it supplies, and "Last synced N days ago" PROMINENT, not hidden). The data is a
   periodic snapshot and the UI says so plainly.

Verify: report the actual vitals read out of garmin.json with the file's own date, the
computed trend and streak for the marker used in the near-miss callout, and the rendered
callout text. Confirm the app still works with garmin.json absent or stale — a missing
snapshot degrades to "not measured", never to a zero and never to a crash. Confirm DevTools
Network shows no request for it beyond the local file load.
```

## Stage 3 Report

_Pending._

---

# Stage 4 — Appointment prep sheet

```
The distinctive output, the ethics answer, and the FIRST thing to cut if a day is lost. If
it cannot be real, delete the entry points rather than shipping a placeholder.

1. Generate a real downloadable file from the live profile and the live verdicts. Not a
   screenshot, not a static asset, not a stub.
2. Contents, laid out so a clinician could read it in thirty seconds: the user's values with
   their draw dates, every failed criterion, every near-miss with its exact gap, the
   criteria that could not be checked automatically, and the NCT numbers.
3. Preview screen per docs/FIGMA-MAKE-PROMPT.md screen 8: a clean printable one-pager inside
   the phone frame. One button, "Download". Supporting line: "Bring this to your appointment.
   OpenHealth doesn't contact your doctor — it gets you ready to."
4. "Download prep sheet" becomes the single bottom action on the trial audit screen, and the
   "Prepare for your appointment ->" row on Home now leads here.
5. There is no send-to-doctor button anywhere in this app, in any form. The only output is a
   downloaded file.

Verify: download the sheet and report its contents verbatim against the on-screen audit for
the same trial — every value, every failed criterion, every near-miss gap, every NCT number
must match. Open the downloaded file and confirm it is readable standalone. If any part of it
is hardcoded rather than generated, say so plainly instead of shipping it.
```

## Stage 4 Report

_Pending._

---

# Stage 5 — Coherence, verify, and freeze

```
No new features. This stage closes the build and hands off to the video.

1. Run tests.html and report every case. Then run /design-review and /qa-only and report
   what they find, fixing what is real.
2. Full literal walkthrough as a judge would do it, cold: open with no data, add a lab
   document, correct a flagged value, read the Health Score and its confidence line, open
   Metrics and a marker detail, open Trials, open the audit for a strong match and for a weak
   one, read the unparsed section, download the prep sheet. Report each step.
3. Audit the whole app against the six rules in docs/FIGMA-MAKE-PROMPT.md and report each as
   pass or fail with a location: no search bar or condition picker anywhere; unknown never a
   zero, dash, or empty bar; score and confidence never merged; nothing sent anywhere;
   verdicts legible without colour; no quoted score constant.
4. Edge and empty states: no readable values, no matching trials, OCR failure, garmin.json
   missing or stale, localStorage unavailable. None may render a zero that reads as a result.
5. Cross-device check on a real iPhone, a real Android, and desktop. Load offline after first
   load.
6. Update the docs to the shipped truth and nothing more: README.md "what is real" plus the
   garmin.json privacy note, docs/ARCHITECTURE.md §8 prototype map, docs/ROADMAP.md Weeks 2-3
   marked delivered, and docs/SIMPLIFY.md §7 annotated with what actually shipped and what
   was cut. Then publish to the existing artifact URL — same link, do not create a new one.

Verify: tests.html fully green, the walkthrough reported step by step, the six-rule audit
line by line, every edge state named, and the three devices confirmed. List anything cut,
explicitly, so the video's "what's next" is accurate rather than optimistic. FEATURE FREEZE
is end of day Saturday, October 18 — after this stage, bug fixes only.
```

## Stage 5 Report

_Pending._

---

# After These Stages

- The app is complete to the standard set on 2026-10-06: **everything functional, not just
  clickable, with no backend as the only accepted limitation.** Documents and watch data in,
  a ranked per-criterion audit out, and one real file to take to an appointment.
- What remains is the submission, which is a third of the score: the video (up to 10 of 30
  points, and the only place *Code* moves from 1 to 4), the six written answers, and the AI
  disclosure. See `docs/ROADMAP.md` Week 4 — plus the 3.5 days of freeze-legal non-feature
  work (accessibility, persistence, QA, cross-device) that shares that week.
- Deferred on purpose, and the honest answer to "what's next": genomic matching,
  multi-condition expansion, and a live wearable sync that would need partner approval and a
  hosted webhook. They belong in the video's closing line, not in the code.
- **Internal submission date is Sunday, October 25.** The official deadline is noon ET on
  Monday, October 26, and nothing gets submitted into a noon cutoff.
