# OpenHealth — Design System

> How the app looks and moves. These tokens live in the `:root` block at the top of
> `index.html`; this file explains the intent behind them so changes stay consistent.

## Direction

**Green-forward consumer health app — light theme.** A green-to-lime gradient owns the
home screen and the one number that matters; everything below it is white cards on a soft
light canvas. The four-color biomarker spectrum survives only where color carries meaning:
lab bars and trial eligibility.

The layout grammar comes from two reference apps in `assets/intake/references/` — gradient
hero → oversized ring metric → three labeled mini-bars → white sheet of list rows, and the
big-number + bar-chart statistics screen. We took the **grammar**, not the content: kcal
became Health Score, macros became biomarkers, food rows became trial rows, and the weekly
calorie chart became seven lab draws of one biomarker.

The light theme is deliberate: the original hand-drawn mockups are vivid marker on white
paper. The app is meant to look like a real, shipped 2026 health product, not a template.

## Color

| Token | Hex | Use |
|-------|-----|-----|
| `--canvas` | `#E6EAE5` | page behind the phone |
| `--screen` | `#F3F5F1` | app background |
| `--surface` | `#FFFFFF` | cards |
| `--surface-2` | `#F0F3EC` | insets, bar tracks |
| `--ink` | `#131A16` | primary text, the active marker chip |
| `--ink-2` | `#59645C` | secondary text |
| `--ink-3` | `#95A099` | captions, tertiary |
| `--line` / `--line-2` | `#E9ECE6` / `#DCE1D7` | hairlines |

The neutrals are very slightly warm-green so white cards sit calm against the hero.

**The brand green** (hero gradient, CTAs, active tab, success):

| Token | Hex | Use |
|-------|-----|-----|
| `--brand` | `#46BC5C` | primary buttons, active tab, ring fill |
| `--brand-d` | `#2C9F45` | green text on light, icon strokes |
| `--lime` | `#B6E354` | accent dot inside the dark match chip |
| `--soft` | `#E9F6D5` | pale-green tile and chip fills |

The home hero is a single `linear-gradient(174deg, …)` on the phone shell, not on a
child — so the white sheet scrolls *over* it. It falls green → lime → cream → app
background by 60% of the phone height, which puts the cream right behind "See details".

**The biomarker spectrum** (the identity of the app — used for bars, dots, the logo):

| Token | Hex | Meaning |
|-------|-----|---------|
| `--iron` | `#E11D74` | magenta — Iron / Ferritin |
| `--hgb` | `#7C4DFF` | purple — Hemoglobin |
| `--o2` | `#12B3A6` | teal — Oxygen saturation |
| `--ldl` | `#2F80ED` | blue — LDL cholesterol |

**Semantic** (separate from the spectrum): `--good #12B76A` (match / success),
`--warn #F5A524` (attention). Each biomarker keeps the *same* color everywhere it appears,
so a color always means the same marker.

**Portraits.** The patient and the care team use photographic avatars, not initials on a
colored disc — initials read as a placeholder, and this app is meant to look shipped. The
faces are **synthetic (StyleGAN-generated): none of these people exist**, which is the only
honest option for a fictional care team. They are embedded as base64 data URIs (~46KB for
ten) because the artifact sandbox blocks external images; each is a `.av.f-<name>` class so
one face is defined once and reused wherever that person appears.

Two details keep ten unrelated photos reading as one set: a 1.5px inset white ring, and a
**0.6px blur** on the photo. The blur is deliberately below the threshold you'd notice as
blur — it just takes the stock-photo edge off and stops the mismatched backgrounds from
competing. Both live on pseudo-elements: `::before` carries the image and the blur,
`::after` carries the ring. Blurring `.av` itself would smear the ring and the drop shadow
too, and the image layer is inset `-3px` so the blur's feathered edge falls outside the
circular clip instead of leaving a translucent rim.

## Type

Three faces, each with one job:

- **Bricolage Grotesque** (`--display`) — headings, labels, buttons, wordmark. Characterful,
  editorial. Weights 600/700/800.
- **Inter** (`--body`) — body and UI text. Neutral and legible.
- Big numerals use Bricolage at weight 800 with tight tracking (`-.04em`), not a separate
  face — the score, the lab values, the stat tiles.

**Units never sit inside a display-size numeral.** They are their own element in the body
face (`.unit`, `.u`). Chromium paints a phantom strikethrough across a small inline span
nested inside a 2.7rem numeral, and Bricolage adds a stray crossbar to `ng/mL` at display
sizes. Both go away when the unit is a sibling in Inter.

All from Google Fonts (the only font host the artifact sandbox allows), each with a real
fallback stack.

## Layout & spacing

- One phone device, `max-width: 404px`, centered on the canvas. On a wide + tall desktop
  it floats in a rounded device bezel with a caption; on a phone it's full-bleed.
- Structure: **status bar → sliding screen track → bottom tab bar.** Each screen scrolls
  its own content.
- `--pad: 18px` screen gutter, `--r: 22px` card radius, `--r-sm: 14px` control radius.
- The phone is `flex: 1 1 auto; min-height: 0` inside a `grid-template-rows: minmax(0,1fr)`
  body. Both are load-bearing — without them the screen content stretches the phone past
  the viewport and the tab bar walks off the bottom.
- Cards get border + soft shadow only where an element is genuinely a separate object —
  not on everything (that flattens hierarchy).

## Motion

Motion is used to make data feel alive, not for decoration. Everything below is disabled
under `prefers-reduced-motion`.

- **Screen transitions** — horizontal slide of the track (0.45s).
- **On screen enter** — content rises + fades in with a short stagger (`.reveal`).
- **Labs** — bars grow from the baseline with a 55ms per-column stagger; the gauge needle
  swings into place; each biomarker's range pin springs up. Switching markers re-runs it.
- **Home / Trials** — the ring draws to 87% while the number counts up 0→87; the three
  biomarker bars and the eligibility bars fill from zero.
- ~~**Send**~~ — the paper-plane send-to-doctor moment is **deleted, 2026-10-06**. There were
  no doctors on the other end. The signature moment is now the **audit table filling in**:
  each criterion resolving to pass / fail / unknown / near-miss as the parser works through
  the trial's own text, with the near-miss gap counting up to its exact number.

## Voice

Plain, warm, patient-side. Name things the way a person would ("Your bloodwork", "Why you
qualify", "Take this to your appointment"), never system jargon. Buttons say exactly what
happens; the confirmation confirms it happened.

**And never more than happened.** "Download prep sheet" is accurate; "Send to your doctor"
would not be, because nothing is sent. This is a voice rule, not only an honesty rule — a
button that overstates its effect is the fastest way to lose a user's trust in every other
number on the screen.
