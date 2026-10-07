# OpenHealth — Design

> **Status: OPEN BRIEF, not an answer. Reset 2026-10-07.**
>
> The previous contents of this file described a green-forward light theme with a
> pink/purple/teal/blue biomarker spectrum, an amber Health Score ring, Bricolage Grotesque
> + Inter, 22px radii and a green→lime hero gradient. **All of it is retired.** The visual
> execution was rejected, and the palette was stripped out of `BUILDSPEC.md`,
> `FIGMA-MAKE-PROMPT.md` and `BRIEF.md` at the same time so no stale copy can quietly
> become the spec again.
>
> Nothing below prescribes a look. This file holds the **brief** — the subject, the
> constraints a direction has to survive, and the invariants that are not negotiable
> whatever direction wins. The direction itself gets decided, then written here.

## 1 · Three retired directions — do not reinstate

Recording these so none of them gets rediscovered and mistaken for the plan.

| | Direction | Where it lived | Why it is dead |
|---|---|---|---|
| 1 | **Dark theme** — `#0D1117` canvas, `#E91E8C`/`#9C27B0`/`#26A69A`/`#2196F3` bars | `BUILDSPEC.md` | Never shipped. Contradicted this file's light theme for weeks while both sat in the repo |
| 2 | **Green-forward light** — green→lime hero gradient, white cards, warm-green neutrals, amber ring, Bricolage + Inter | this file, `FIGMA-MAKE-PROMPT.md`, shipped in `index.html` | Rejected 2026-10-07. This is the one that is live and hideous |
| 3 | **Warm paper + serif** — cream sheet, Fraunces/Instrument Serif numerals | uncommitted `styleguide.html` draft | Deleted unbuilt. It is the single most recognisable AI-generated design cliché there is (see §4) |

`Screenshot 2026-10-06 153715.png` is the reference *for direction 2*. It is now a
historical artifact. **It is not a design reference and must not be matched.**

## 2 · The subject — what is actually being designed

This is the part the old docs never wrote down, and it is where a non-generic direction has
to come from. It is not "a health app".

**It is an instrument that reads documents you already have and tells you, criterion by
criterion, whether you are eligible for a real clinical trial — and by exactly how much you
miss.** You never tell it what condition you have.

The things that are true about this subject and should drive the look:

- **It is evidentiary, not motivational.** Consumer health apps congratulate you. This one
  adjudicates. The emotional register is a lab report or a court docket, not a fitness ring.
  Nothing here should cheer.
- **The per-criterion audit table is the product.** Not the score, not the ring. The table
  where each of a trial's own eligibility sentences resolves to pass / fail / unknown /
  near-miss next to your actual number. Everything else exists to fill that table or lead
  to it. **If a visual decision makes the table less clear, it is the wrong decision.**
- **Its integrity is the differentiator.** The app shows you what it *cannot* determine
  (`UNKNOWN`) with the same weight as what it can. A1c is deliberately missing to prove the
  engine does not treat absence as a pass. A design that hides or softens uncertainty
  destroys the one thing this project is actually selling.
- **Near-miss is the most interesting state in the app** — "you are 14 ng/mL short" is more
  useful than pass or fail, and no competitor shows it. It deserves real visual invention,
  not a yellow chip.
- **The raw source text is always reachable.** Every verdict can be traced to the trial's
  own sentence. The design should make that feel like a feature, not a footnote.
- **The audience is a patient reading bad news carefully**, on a phone, probably once.
  Not a dashboard user who returns daily.

## 3 · Hard constraints — a direction that violates these is not a candidate

These are not aesthetic preferences. They are the architecture.

1. **Zero network calls at runtime.** This is a published rule in `CLAUDE.md` and Stage 7
   audits it. **This currently rules out Google Fonts** — the live build violates it with
   three font requests (`HANDOFF-V1.md` §4.1). Typography must be **self-hosted (base64 or
   inline `@font-face`) or a system stack.** A direction whose personality depends on a
   webfont has to pay for it in artifact bytes — budget it up front.
2. **One self-contained HTML file.** No build step, no framework, no Tailwind, no CSS
   preprocessor. Hand-written CSS with custom properties. Only CDN library is Tesseract.js.
3. **≤ 16MB rendered**, and `index.html` is already ~260KB. Embedded fonts and images count.
4. **No API key, ever** — so no icon CDN, no image service, no remote anything.
5. **Mobile-first, phone width.** Must hold with no horizontal scroll.
6. **No condition input anywhere.** No search box, no dropdown, no questionnaire. Designing
   a search field is designing the wrong app.
7. **Never render a score as a constant.** Every score is engine output. `87/100`, `89`,
   `79/100` and `CGX Trial #4` are retired strings and must not appear in markup or mocks.

## 4 · Calibration — what "AI-generated" looks like, so we do not ship it

From the installed `frontend-design` skill. Current AI design clusters hard around:

1. **Warm cream background (~`#F4F1EA`) + high-contrast serif display + terracotta accent
   (~`#D97757`).** This is cluster one, it is the most recognisable tell, and **the deleted
   `styleguide.html` draft was exactly this.** Do not go back.
2. Near-black background with one acid-green or vermilion accent.
3. Purple gradients, uniform rounded corners everywhere, everything centered, Inter.

Specific tells to avoid, all of which the current build commits:

- Accenting a single word in a headline in a different colour or weight.
- All-caps micro-labels above content.
- Unnecessary typographic labels introducing a section that needs no introduction.
- Numbered markers (01 / 02 / 03) on content that is not a sequence.
- Fade-and-slide-up entrance on every section, hover transition on every card. **One**
  orchestrated moment lands; scattered effects read as generated. The current build animates
  the ring, the bars, the gauge needle, the range pins and every screen entrance.
- A big number with a small label plus a gradient accent as the hero. This is *the* default
  treatment and the current home screen is precisely it.

Structural devices — borders, dividers, numbering, eyebrows — must **encode information**,
not decorate. In an audit table that is an unusually easy bar to clear: the structure can
carry verdict, margin and provenance honestly.

## 5 · Invariants — true in every direction

Carried over because they are functional or ethical, not stylistic.

- **One accent per biomarker, consistent everywhere** it appears, so a colour always means
  the same marker. *Which* accents is open.
- **Verdicts legible without colour.** `PASS` / `FAIL` / `UNKNOWN` / `NEAR MISS` each pair a
  colour with an icon *and* a word, and must survive greyscale and colour-blindness.
- **`UNKNOWN` is never a zero, a dash, or visually quieter than a fail.**
- **Score and confidence never merge** into one number.
- **Reference ranges are visible** next to any value they judge.
- **Text contrast ≥ 4.5:1.** Touch targets ≥ 44×44px with ≥ 8px separation.
- **`prefers-reduced-motion` disables all non-essential motion.**
- **Voice: plain, warm, patient-side.** Name things as a person would — "Your bloodwork",
  "Why you qualify", "Take this to your appointment". A button says exactly what happens and
  never more. "Download prep sheet" is accurate; "Send to your doctor" is not, because
  nothing is sent. A button that overstates its effect is the fastest way to lose a user's
  trust in every number on the screen.
- **Synthetic faces, if any survive, are disclosed as synthetic.** No implication that a
  care team exists. The send-to-doctor flow and "Doctors Available: 9" are retired.

## 6 · Tooling available for the rethink

Installed under `.claude/skills/` and committed, so a collaborator gets them too:

| Skill | Source | Use |
|---|---|---|
| `frontend-design` | `anthropics/skills` | Aesthetic direction, typography, anti-slop calibration. §4 above comes from it |
| `theme-factory` | `anthropics/skills` | 10 pre-built palette/font themes + `theme-showcase.pdf` to compare directions fast |
| `ui-ux-pro-max` | `nextlevelbuilder/ui-ux-pro-max-skill` | Searchable local DB: 79 styles, 192 product palettes, 74 font pairings, 119 UX rules. Entry point `.claude/skills/ui-ux-pro-max/scripts/search.py` |
| `design-system` | same | Three-layer token architecture (primitive → semantic → component) |
| `webapp-testing` | `anthropics/skills` | Playwright verification of the rebuilt UI |

Deliberately **not** installed: `web-artifacts-builder` and `ui-styling` (both mandate
React + Tailwind + shadcn and a build step — see §3.2), `canvas-design` (posters, and 80
font binaries), `brand-guidelines` (Anthropic's own brand, not ours).

## 7 · The system — **Tolerance**, locked 2026-10-07

Chosen from four directions put side by side. The three rejected: *redline the source*
(the trial paragraph marked up in place), *docket / finding* (criteria as formal rulings),
*assay plate* (criteria as wells on a lab plate). They are recorded here because any of
them could be revived; none should be mixed into this one.

### 7.1 · The idea

**Every judgement in this app is a measurement against a tolerance, so draw it that way.**
A criterion is not a chip that says FAIL. It is a required band on a scale, your value as a
tick, and — when you miss — the distance between them, named. Near-miss is the most useful
thing this engine computes, so it is the thing the design is built around rather than a
yellow badge bolted to the side.

This came straight out of §2: the product adjudicates, and `marginPhrase()` already knows
exactly how far short you are. The old UI threw that away into a caption.

**The hero is the tolerance stack, not a score ring.** `DESIGN.md` §4 flags
big-number-plus-ring-plus-gradient as *the* generic default, and the old home screen was
precisely it. The score survives as a small figure with its confidence line, below the
stack — it is a summary of the scales, so it does not outrank them.

### 7.2 · Colour — the rule that makes this system work

> **Your value is ink. The requirement is a tint. The gap is the only thing in signal
> colour.**

Colour never carries a verdict. It carries *identity* (which marker) and *attention* (the
gap). That has three consequences worth stating:

- The app **passes greyscale by construction**, satisfying §5 without a special pass.
- A passing value and a failing value are drawn in the same ink, so nothing cheers and
  nothing alarms — the §2 register.
- There is exactly **one** high-chroma colour in the whole interface, spent on the one
  number no competitor shows. That is the boldness budget, spent in one place.

| Token | Hex | Role |
|---|---|---|
| `--paper` | `#E7ECEE` | canvas behind the device — cool grey-blue, engineering paper |
| `--sheet` | `#F7F9FA` | app background |
| `--card` | `#FFFFFF` | raised surface, used sparingly |
| `--ink` | `#17212A` | graphite. Primary text **and every value tick** |
| `--ink-2` | `#53646F` | secondary text |
| `--ink-3` | `#8698A3` | tick labels, captions |
| `--rule` | `#C9D5DB` | scale axes, threshold edges, card borders |
| `--band` | `#DCE6EA` | neutral required-range fill where no marker owns the scale |
| `--gap` | `#B81D40` | **the signal.** Deep carmine, the annotation pen. The near-miss bracket and its number. Nothing else, ever |

Deliberately cool and deliberately not: cream (`#F4F1EA`), terracotta (`#D97757`),
tinted near-black (`#0B0B0B`), acid green, purple gradient. See §4.

**Marker identity** — low-chroma, used as the band tint (~22% alpha) and the marker dot.
Low chroma on purpose: these identify, they do not shout, because the tick has to stay the
loudest thing on the scale. Lightness is spread so they separate in greyscale too.

| Token | Hex | Marker |
|---|---|---|
| `--m-fe` | `#8C3C62` | Iron / Ferritin — mulberry |
| `--m-hgb` | `#3F4A86` | Hemoglobin — indigo |
| `--m-o2` | `#1F6B64` | SpO₂ — deep teal |
| `--m-ldl` | `#4A6B8A` | LDL — steel |

### 7.3 · Type

**One self-hosted face**, per the budget decision: **IBM Plex Mono**, weights 400 and 600,
embedded as base64 `@font-face`. It was drawn for technical readout, it has true tabular
figures, and tabular figures are **load-bearing here** — values have to align vertically
against scale ticks or the stack stops reading as an instrument.

`DESIGN.md` §4 lists "a monospace face for small data labels" as template chrome, and that
warning is accepted with a hard restriction:

> **Mono is for measured quantities only** — values, units, scale tick labels, margins,
> NCT IDs. **Never** for labels, headings, buttons, prose or eyebrows. If it is not a
> number you could put a unit on, it is not mono.

Prose and UI take a **system humanist sans stack** (`ui-sans-serif, -apple-system,
"Segoe UI", Roboto, …`) — zero bytes, zero network, and clearly distinct from the mono, so
the two-face rule is satisfied without a second download.

Scale, 16px base at a 1.25 ratio:

| Token | Size | Use |
|---|---|---|
| `--t-quant-xl` | 2.25rem | the one big quantity on a screen. Mono 600, tracking `-.03em` |
| `--t-h1` | 1.375rem | screen title. Sans 650, sentence case |
| `--t-h2` | 1.0625rem | section title. Sans 650 |
| `--t-quant` | 1rem | inline values. Mono 600 |
| `--t-body` | .9375rem / 1.55 | prose |
| `--t-small` | .8125rem | captions |
| `--t-tick` | .6875rem | scale tick labels. Mono 400 |

**Sentence case everywhere. No all-caps, at any size.** The 11 `.eyebrow` all-caps labels
in the old build are deleted, not restyled — §4 names both all-caps labels and unnecessary
labels-above-content as tells, and most of them introduced a section that needed no
introduction.

### 7.4 · The tolerance scale — the signature primitive

The engine already emits this. `renderMarkerCard()` writes `.scale > .band + .pin` and
`axisPct()` positions them; the old CSS rendered it as a thin decorative bar. The
primitive promotes what is already there.

```
Ferritin                                    8 ng/mL
  ────────────┬───────────────────────────────────
         ▌    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
         8    12                          150
         └ 4 short
```

- **axis** — a 1px `--rule` baseline across the full width. A hairline in this system must
  mark a value or a boundary; it is never decoration.
- **`.band`** — the required range, filled in the marker's tint, with 1px solid edges at
  the thresholds. The edges are the numbers that matter, so they are drawn.
- **`.pin`** — your value. A 2px full-height `--ink` tick, the highest-contrast mark on the
  scale, with its value in mono beneath.
- **`.gap`** *(new)* — drawn only on a near-miss: a bracket in `--gap` spanning tick to
  threshold, labelled with the exact margin from `marginPhrase()`.
- **`.scale.none`** — the unknown state. **Axis drawn, band drawn as a dashed outline, no
  tick**, and "not read" set where the tick would be. Unknown is drawn, not omitted, and it
  is not quieter than a fail (§5).

### 7.5 · Layout

- Single column, **left-aligned**. Quantities right-align in their own column so they
  stack. Nothing is centre-aligned except the device on the canvas.
- `--pad: 20px` gutter. Vertical rhythm on a 4px grid.
- **Radius encodes hierarchy** — `--r-sheet: 16px`, `--r-card: 10px`, `--r-chip: 3px`,
  scales and ticks `0`. §4 cluster 4 is one radius on everything; this is the opposite, and
  the differences are meant to be legible.
- **Shadows: one**, on the device shell. Cards separate by a 1px `--rule` border and a
  background delta. The old build put the same soft shadow under everything, which is
  exactly the SaaS-card tell, and it flattened the hierarchy it was trying to create.
- The green→lime hero gradient on `.phone::before` is **deleted**. No gradient washes.

### 7.6 · Motion

**One orchestrated moment: the audit resolving.** When a trial opens, the ticks travel from
the axis origin to position (260ms, 40ms stagger) and each near-miss margin counts up once.

Everything else stops moving. The old build animated the ring, the bars, the gauge needle,
the range pins *and* every screen entrance — §4 names scattered entrances as the generated
default. `.reveal` keeps its class (the JS contract) but becomes a no-op. Press and
expand/collapse feedback stays, because it answers a user action. All of it off under
`prefers-reduced-motion`.

### 7.7 · Invariant checklist for this system

| §5 invariant | How Tolerance satisfies it |
|---|---|
| One accent per biomarker | `--m-*`, as band tint and dot, same marker everywhere |
| Verdicts legible without colour | Colour never carries a verdict at all — mark + word + tick position do |
| Unknown never a zero or a dash | `.scale.none` draws the axis and band, omits only the tick, and says "not read" |
| Score and confidence never merge | Two separate figures, the confidence line in its own block |
| Reference ranges visible | The band *is* the reference range, with its thresholds labelled |
| Contrast ≥ 4.5:1 | `--ink` on `--sheet` ≈ 13:1; `--ink-2` ≈ 6.2:1; `--ink-3` only on tick labels ≥ 3:1 at 11px+ and never load-bearing alone |
| Reduced motion | §7.6 |

### 7.8 · Build order

1. ~~Lock the system (this section).~~ **Done.**
2. Replace the `<style>` block in `index.html` wholesale, keeping the **193-class
   selector contract** intact so the render functions keep working.
3. Strip the slop from the static HTML: both score rings, the gauge needle, the 11
   `.eyebrow` labels, the `·`-joined meta strings, the `→` button suffixes.
4. Add `.gap` to the audit row — the only render-function change the direction needs.
5. Verify: screenshots at phone width, greyscale pass, contrast, reduced motion, zero
   network calls, no retired score string.

### 7.9 · Open, and deliberately not decided here

- **The fake vitals on the Metrics screen.** `Resting HR 62`, `Weight 154 lb`,
  `Hydration 6 glasses` are hard-coded in the static HTML with hand-drawn SVG sparklines.
  They are not read from `garmin.json` and they are not real. By the standard in
  `CLAUDE.md` — *if a screen looks like it does something it does not do, it gets deleted,
  not polished* — these should go. Deleting features is not a presentation decision, so
  they are flagged rather than removed.
- **Embedding the Plex Mono subset.** Needs the woff2 fetched once at build time and
  base64'd into the file. Until that lands the stack falls back to system mono, which
  renders correctly but without the identity.
