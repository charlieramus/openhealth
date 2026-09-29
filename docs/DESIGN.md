# OpenHealth — Design System

> How the app looks and moves. These tokens live in the `:root` block at the top of
> `index.html`; this file explains the intent behind them so changes stay consistent.

## Direction

**Premium, editorial, trustworthy — light theme.** Think Apple Health / Function Health:
clean white cards on a soft cool-neutral canvas, generous whitespace, crisp type, and one
vibrant four-color "spectrum" that runs through all the health data.

The light theme is deliberate: the original hand-drawn mockups are vivid marker on white
paper. The app is meant to look like a real, shipped 2026 health product, not a template.

## Color

| Token | Hex | Use |
|-------|-----|-----|
| `--canvas` | `#E7EAEF` | page behind the phone |
| `--screen` | `#F6F7F9` | app background |
| `--surface` | `#FFFFFF` | cards |
| `--surface-2` | `#F1F3F6` | insets, bar tracks |
| `--ink` | `#141821` | primary text **and** primary buttons |
| `--ink-2` | `#5A6472` | secondary text |
| `--ink-3` | `#97A0AE` | captions, tertiary |
| `--line` / `--line-2` | `#E7EAEE` / `#DCE0E6` | hairlines |

**The biomarker spectrum** (the identity of the app — used for bars, dots, avatars, the logo):

| Token | Hex | Meaning |
|-------|-----|---------|
| `--iron` | `#E11D74` | magenta — Iron / Ferritin |
| `--hgb` | `#7C4DFF` | purple — Hemoglobin |
| `--o2` | `#12B3A6` | teal — Oxygen saturation |
| `--ldl` | `#2F80ED` | blue — LDL cholesterol |

**Semantic** (separate from the spectrum): `--good #12B76A` (match / success),
`--warn #F5A524` (attention). Each biomarker keeps the *same* color everywhere it appears,
so a color always means the same marker.

## Type

Three faces, each with one job:

- **Bricolage Grotesque** (`--display`) — headings, labels, buttons, wordmark. Characterful,
  editorial. Weights 600/700/800.
- **Inter** (`--body`) — body and UI text. Neutral and legible.
- **Fraunces** (`--num`) — big hero numerals only (the 87 score, biomarker values, gauge
  status). An editorial serif that makes the numbers feel human and premium.

All from Google Fonts (the only font host the artifact sandbox allows), each with a real
fallback stack.

## Layout & spacing

- One phone device, `max-width: 404px`, centered on the canvas. On a wide + tall desktop
  it floats in a rounded device bezel with a caption; on a phone it's full-bleed.
- Structure: **status bar → sliding screen track → bottom tab bar.** Each screen scrolls
  its own content.
- `--pad: 20px` screen gutter, `--r: 20px` card radius, `--r-sm: 13px` control radius.
- Cards get border + soft shadow only where an element is genuinely a separate object —
  not on everything (that flattens hierarchy).

## Motion

Motion is used to make data feel alive, not for decoration. Everything below is disabled
under `prefers-reduced-motion`.

- **Screen transitions** — horizontal slide of the track (0.45s).
- **On screen enter** — content rises + fades in with a short stagger (`.reveal`).
- **Labs** — the gauge needle swings into place; each biomarker's value marker springs up.
- **Trials** — the match ring draws to 87% while the number counts up 0→87; eligibility
  bars fill.
- **Send** — a paper plane flies up off the button (straight from the mockup), then a
  confirmation modal, then the button becomes a "Sent" state. This is the signature moment.

## Voice

Plain, warm, patient-side. Name things the way a person would ("Your bloodwork", "Why you
qualify", "Send my records to Dr. Chen"), never system jargon. Buttons say exactly what
happens; the confirmation confirms it happened.
