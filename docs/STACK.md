# OpenHealth — Stack Decision: Should the Prototype Be Next.js?

> **No — not yet.** This doc records the decision, the measurements behind it, and the
> conditions that would reverse it.
>
> This describes **what exists**: `index.html`, one static file, no build step. It is the
> companion to [`BUILDSPEC.md`](BUILDSPEC.md) (what the screens do) and
> [`DESIGN.md`](DESIGN.md) (what they look like) — this one is *what they're made of*.
>
> Decided 2026-09-28. Revisit when a trigger in §6 fires, not before.

---

## 1 · The question

The prototype is a single hand-written HTML file. The recurring temptation is to move it to
Next.js/React "to make it easily editable," especially with Figma possibly entering the
workflow later.

Two claims are doing the work in that sentence, and both turn out to be false at this size:

1. **That a framework is what makes code easily editable.** At 1,247 lines it isn't — file
   count is.
2. **That Next.js makes Figma handoff easier.** It doesn't. A token layer does, and we
   already have one.

---

## 2 · What we'd actually be porting

Measured, not estimated — `index.html` at the time of this decision:

| Region | Lines | Port cost | Why |
|--------|-------|-----------|-----|
| `<style>` (L8–638) | ~630 | **Near-free** | Already CSS custom properties. Drops into `globals.css` as-is |
| Markup (L639–1110) | ~470 | **Mechanical** | `class`→`className`, self-closing tags, `style=""`→objects, inline SVGs. Tedious, low-risk |
| `<script>` (L1111–1247) | ~136 | **A genuine rewrite** | This is the whole cost |

**Totals:** 1,247 lines · 112 KB · **zero** dependencies · **zero** build step · 3 external
requests, all Google Fonts.

### Why the script is the real cost

The JS is imperative DOM mutation against **23 `getElementById` targets** and **4 `window.*`
globals** (`go`, `pick`, `send`, `key`). None of it survives into React unchanged:

| Current technique | Becomes | Risk |
|---|---|---|
| `renderChart()` writing into `#cVal`, `#cUnit`, `#vTx`… | Derived render from state | Low |
| `track.style.transform` screen slide | State + CSS transform | Low |
| `void s.offsetWidth` forced reflow to replay animations | A `key` bump or an effect | **Regresses quietly** |
| `countUp()` rAF loop | rAF in `useEffect` with cleanup | **StrictMode double-invoke** |
| `send()` `setTimeout` chain + `classList` toggles | State machine or effect chain | Medium |
| `prefers-reduced-motion` branch in each of the above | Re-implemented in each hook | **Easy to drop** |

The reflow hack and the reduced-motion branches are exactly the polish that got the
prototype through design review, and they're exactly what a port tends to lose.

**Plus new surface that doesn't exist today:** `package.json`, `node_modules`,
`next.config`, `next/font`, a Vercel account, a deploy step, and a second live URL to keep
in sync with the artifact link in [`../README.md`](../README.md).

---

## 3 · The four costs

**① It trades away the fastest edit loop we have.**
Today: ctrl-F, save, reload. After: dev server, HMR that occasionally desyncs, a build
before anything is publishable. For a project whose whole mode is quick visual changes,
that's the wrong direction.

**② "Easily editable" is a file-count property, not a framework property.**
1,247 lines in one file is trivially editable, and it's a single read for an AI
collaborator. Split across 8–12 component files and every change begins with a search.
Components pay off when there's repetition to dedupe or people editing in parallel. There
are three screens, each used exactly once.

**③ It's Phase-0 rework.**
[`ROADMAP.md`](ROADMAP.md) puts us at Phase 0 complete and Phase 1 explicitly **no code**,
with **A2** — will a trial site pay for a referral — as the first assumption to test. A
port moves nothing on that list. It's motion, not progress, and the Congressional App
Challenge submission is live against the current URL.

**④ It costs the "$0, one static HTML file" line.**
[`ROADMAP.md`](ROADMAP.md) claims **current cost to run: $0**, and that claim is load-bearing
in the doc set. Vercel's free tier keeps it $0 in dollars, but it stops being *trivially*
true, and it adds an account and a deploy to a school project.

---

## 4 · Figma: the part that's usually backwards

**Figma → Next.js is not meaningfully easier than Figma → HTML.** Neither direction is
automatic, and neither is a code generator you'd ship from.

What actually makes Figma handoff cheap is a **token layer** — one place where a color or
radius is defined, so a design change is a variable change. We have one already: the
`:root` block in `index.html` (`--brand`, `--iron`, `--hgb`, `--o2`, `--ldl`, `--r`,
`--pad`, `--shadow`…), owned by [`DESIGN.md`](DESIGN.md). It maps roughly 1:1 onto Figma
Variables. **That's framework-independent and it exists today.**

| Direction | What it needs | Does Next.js help? |
|---|---|---|
| Figma → code (read design context) | A token layer to write into | **No.** Framework-agnostic |
| Code → Figma (push a page in) | A rendered page | **No.** Works off the render |
| Figma ⇄ code round-trip via **Code Connect** | Real named components to map onto | **Yes** — this is the one genuine advantage |

Code Connect is the real exception, and it's an enterprise design-system workflow: you map
Figma components to code components so designers and engineers share one source. That's
worth having when there's a component library and more than one person maintaining it.
It is a long way past a three-screen prototype with no repeated components.

---

## 5 · What to do instead

Both of these buy most of "easily editable" without a build step, and both keep the
single-artifact publish flow in [`../README.md`](../README.md) intact:

| Move | Effort | What it gets |
|------|--------|--------------|
| **Split into `index.html` + `styles.css` + `app.js`** | ~10 min | Three files instead of one 112 KB file. Still no build step, still $0; artifacts publish supporting files |
| **Hoist remaining fake data to a `DATA` object** at the top of the JS, the way `MARKERS` already is | ~20 min | Content edits (trial cards, home rows, doctor names) stop touching markup |

Neither is a prerequisite for the other, and neither is a step toward a port — they're the
alternative to one.

---

## 6 · When to revisit

Port when **any one** of these is true. Not before, and not on general principle:

| Trigger | Why it changes the answer |
|---------|---------------------------|
| **Real data, auth, or an API arrives** (Phase 2 in [`ROADMAP.md`](ROADMAP.md)) | Server-side rendering, routing, and secret handling become real requirements. Port against those, not against a guess |
| **Screens grow past ~6, with genuinely shared components** | Repetition to dedupe is the actual thing components solve |
| **A second person needs to edit in parallel** | File-level separation starts preventing conflicts rather than creating searches |
| **Code Connect round-tripping becomes the design workflow** | Per §4, this is the one place React is the better-supported target |

At that point the port is a few hours of markup conversion plus a careful rewrite of the
motion logic in §2 — a known, bounded cost, paid when something is actually bought with it.

---

## 7 · Sources

Everything in §2 is measured from `index.html` at the time of this decision, not estimated:
line ranges from the `<style>`/`<script>` boundaries, `112K` from `du`, the ID and global
counts from `grep`. Re-measure before quoting these if the file has moved on.
