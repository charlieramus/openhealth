# OpenHealth — Figma Make prompt

> Paste the block below into Figma Make. Attach `Screenshot 2026-10-06 153715.png` (the home
> screen) as the visual reference when you do — the prompt refers to it.
>
> Screens 1 and 7 are the ones to get right. Everything else can be rough on the first pass.
>
> **Every number in this prompt is a placeholder.** In the real app they are engine output
> (see [`SIMPLIFY.md`](SIMPLIFY.md) §6). Do not treat any of them as a spec value.

---

Design a mobile app called **OpenHealth** — a clinical-trial eligibility checker wrapped in a
personal health hub. Use the attached screenshot as the visual reference for the home screen
and extend that language across all 10 screens below.

## What the product does

A patient uploads photos of their lab paperwork and syncs their fitness watch. The app reads
the lab values off the documents, combines them with the watch's vitals, and checks them
against the published eligibility criteria of real clinical trials — showing, criterion by
criterion, what they pass, what they fail, and **by exactly how much**.

**The single most important idea: the user is never asked what condition they have.** There
is no search bar, no condition dropdown, no questionnaire anywhere in this app. Every other
product in this category opens with a form. This one opens by asking for a document. Do not
design a search field.

**The audit table (screen 7) is the product.** Everything else exists to fill it or to lead
to it. If a layout decision trades away clarity on screen 7, make the other choice.

## Visual direction

From the attached screenshot — carry this across every screen:

- **Light, warm-neutral canvas** (#E6EAE5), cards in pure white (#FFFFFF) with generous
  rounded corners (22px; 14px for small chips) and a soft low shadow
- **Heavy black display type** for numbers and headings — tight, confident, almost editorial.
  Big numerals are the main visual event. Body text is a clean neutral sans
- **Chunky, friendly, tappable.** Large hit targets, pill-shaped buttons, nothing hairline
- iPhone proportions, ~390pt wide, with a status bar and a home indicator

**Colors — each biomarker always keeps its own color, on every screen:**

| Token | Hex | Use |
|---|---|---|
| Iron / Ferritin | `#E11D74` | magenta |
| Hemoglobin | `#7C4DFF` | purple |
| SpO2 | `#12B3A6` | teal |
| LDL | `#2F80ED` | blue |
| Score ring | amber → orange gradient | the home hero ring only |
| Pass / good | `#12B76A` | |
| Near-miss / caution | `#F5A524` | |
| Fail | a muted red, not alarming | |
| Ink | `#131A16` / `#59645C` / `#95A099` | primary / secondary / tertiary text |

Verdicts must be distinguishable **without relying on color alone** — pair every color with
an icon and a word.

---

## The 10 screens

### 1. Home

Rebuild the attached screenshot, with these changes:

- Header: "OpenHealth" wordmark left; profile avatar pill and a notification bell right
- **Health Score ring** — the hero. Large concentric amber/orange ring, big black numeral in
  the middle, "Health Score" beneath it. **Add a small confidence line directly under the
  number: "6 of 8 markers".** This is non-negotiable — the score is only computed from
  markers that have values, and the app always says how many it had
- **Three biomarker bars** under the ring (Iron, Hemoglobin, SPo2) — each a slim horizontal
  track with a filled segment in the marker's color, the label above, and "value / range"
  beneath. A "See Details" pill button under them
- **Today card** — date and a chevron. Inside it, **one full-width panel: "Records Captured"**
  with a grid of document thumbnails and a "See more" link
- ❌ **Remove the "Recent Chats" panel entirely.** Give Records Captured the full width. Then
  add a single row beneath it: **"Prepare for your appointment →"**
- **Top trial match card** — circular condition icon, trial name in heavy black type,
  condition + NCT ID beneath, a bookmark toggle top-right, then three chips in a row: the
  **match score** ("79/100 Match"), the **distance** ("22.3 Mi. Away"), and a "Tap To View →"
  button
- **Bottom tab bar** — three tabs: Home, Metrics, Trials. Pill-shaped, floating, with small
  notification dots

### 2. Add records

Reached from the Today card. Two large stacked options:

- **"Take a photo"** — big camera target with a document-edge guide overlay
- **"Upload a file"** — drop zone for PDF or image

Beneath: a short, plain line — *"Your documents are read on your phone. Nothing is uploaded
anywhere."* Then a list of previously captured documents with their dates.

### 3. Extraction review — *the honesty screen*

After a document is read. This screen is what makes the whole product credible, so give it
real care.

- Top: a thumbnail of the scanned document
- **"Here's what we read"** — a list of extracted values, each row showing the analyte name,
  the value with its unit, the date, and a **confidence indicator**
- Rows the app is unsure about are **visually flagged and editable in place** — a tap target
  to correct the number, not a separate edit mode
- A distinct section at the bottom: **"2 lines we couldn't read"**, showing the raw text
  verbatim, with the option to enter those values by hand
- Primary button: "Add to my profile"

**Never design a state where unreadable content is silently hidden.** Showing what failed is
the point of this screen.

### 4. Metrics tab

A scrollable list of every tracked biomarker. Each row: marker name in its color, current
value large, reference range beneath, and a small sparkline showing its trend. Group lab
values and watch vitals under two quiet subheads: **"From your records"** and **"From your
watch"**. Markers with no value show "Not measured" in a neutral style — **never a zero and
never a dash that could read as a result**.

### 5. Marker detail

Tapping a marker. A large line chart of that marker over time with the reference range drawn
as a soft shaded band behind it. Current value huge at the top. Beneath the chart: which
trials in the user's list reference this marker, and whether they currently pass it.

### 6. Trials tab

Every trial the engine knows about, **ranked by match score** — not filtered, not searched.
Each row: trial name, condition, sponsor, NCT ID, the match score as a colored chip,
distance, and a compact row of small verdict dots previewing its criteria. Include a visibly
weak match far down the list — a 20-something score — so the ranking reads as real output
rather than a list of wins. A small header line: "Ranked against your profile · 24 trials".

### 7. Trial audit — **the hero screen**

Tapping a trial. This is the screen the whole app exists for.

- Header: trial name, sponsor, phase, recruiting status, NCT ID linking out
- **Two numbers, side by side and clearly distinct** — the **match score** ("79/100") and the
  **confidence** ("8 of 11 criteria checkable"). They must not look like one number. They
  measure different things and the design has to make that obvious
- **The audit table — the hero element.** One row per criterion:
  - the rule in plain language ("Ferritin ≤ 50 µg/L")
  - **the user's actual value** ("8 ng/mL")
  - a verdict chip: **PASS · FAIL · UNKNOWN · NEAR MISS**, each with its own icon and color
  - a quiet line beneath quoting the trial's **original wording**, verbatim
- **Near-miss callout** — visually distinct, amber, the most prominent thing after the table:
  *"Ferritin 8 ng/mL — needs ≥ 10. Short by 2. Your resting heart rate has risen for three
  straight weeks. Worth asking your doctor whether a re-test is worthwhile."* Pair the lab
  number with the watch trend; that combination is this app's signature output
- **"3 criteria we couldn't check automatically"** — a collapsed section showing the raw
  criterion text verbatim. Present, never hidden
- A persistent disclaimer: *"This is not an eligibility decision. Only a screening visit can
  determine that."*
- Bottom action: **"Download prep sheet"** — the only action on this screen

❌ There is **no "send to doctor" button** anywhere in this app. Do not design one.

### 8. Appointment prep sheet

A preview of the actual document the app generates. Style it like a clean printable one-pager
inside a phone frame: the user's values with dates, every failed criterion, every near-miss
with its exact gap, and the NCT numbers — laid out as something a clinician could read in
thirty seconds. One button: "Download". Supporting line: *"Bring this to your appointment.
OpenHealth doesn't contact your doctor — it gets you ready to."*

### 9. Connected sources

Two cards:

- **Documents** — how many captured, when the last one was added, a button to add more
- **Garmin** — connection state, *"Last synced 2 days ago"*, and the list of metrics it
  supplies (resting HR, SpO2, HRV, sleep, body composition). Make "Last synced" prominent
  rather than hidden — the data is a periodic snapshot and the UI should say so plainly

### 10. First run — empty state

What a new user sees with no data at all. The Health Score ring is empty with a quiet
"No data yet" rather than a zero. One clear primary action: **"Add your first lab result"**.
A single sentence explaining the product: *"Add your lab results and we'll tell you which
clinical trials you might qualify for. You don't need to know what to look for."*

---

## Rules that apply to every screen

1. **No search bar and no condition picker.** Anywhere.
2. **Unknown is a first-class state**, visually distinct from both pass and fail, and never
   rendered as a zero, a dash, or an empty bar. A missing value must never be able to read as
   a good result.
3. **Score and confidence are always two separate numbers**, never merged into one figure.
4. **Nothing is sent anywhere.** No outbound messaging, no doctor inbox, no chat, no AI
   assistant. The only output is a downloaded file.
5. **All numbers shown are placeholders** — in the real app every one is computed. Design the
   components so a 3-digit score, a long trial name, or a missing value doesn't break the
   layout.
6. Verdicts are legible without color: always an icon plus a word.
