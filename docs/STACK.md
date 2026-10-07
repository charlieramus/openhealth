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

**③ It scores zero points.**
[`ROADMAP.md`](ROADMAP.md) has 27 days on the clock and one named gap — the match score is a
hardcoded literal, so the app computes nothing. Framework choice is not on the judging
rubric; a working matching engine is. A port moves nothing that's scored. It's motion, not
progress, and the Congressional App Challenge submission is live against the current URL.

**④ It costs the "$0, one static HTML file" line.**
The prototype costs nothing to run and needs no account, and that's load-bearing in the doc
set. Vercel's free tier keeps it $0 in dollars, but it stops being *trivially* true, and it
adds an account and a deploy to a school project.

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
| ~~**Real data, auth, or an API arrives**~~ — **EVALUATED 2026-10-02: does not fire.** See below | Server-side rendering, routing, and secret handling become real requirements. Port against those, not against a guess |
| **Screens grow past ~6, with genuinely shared components** | Repetition to dedupe is the actual thing components solve |
| **A second person needs to edit in parallel** | File-level separation starts preventing conflicts rather than creating searches |
| **Code Connect round-tripping becomes the design workflow** | Per §4, this is the one place React is the better-supported target |

At that point the port is a few hours of markup conversion plus a careful rewrite of the
motion logic in §2 — a known, bounded cost, paid when something is actually bought with it.

### 6a · The first trigger was tested, and it does not fire

[`REBUILD.md`](REBUILD.md) put two real APIs into the app — ClinicalTrials.gov v2 and
`r4.smarthealthit.org`. That looked like trigger #1 firing. **It didn't**, and the reason is
worth recording because it is the whole basis of the trigger:

The trigger is not "an API arrives." It is **"secret handling and server-side rendering become
real requirements."** Both of those APIs were:

- **unauthenticated** — no key, no OAuth, no token. **There is no secret to keep off the
  client**, which is the only thing that would force a server
- **CORS-enabled** (`access-control-allow-origin: *` on CT.gov; permissive on the SMART
  sandbox) — verified by live test, so `fetch()` from a static file works
- **read-only GETs** — no write path, no session, no auth state to render against

So the app could gain real data and keep every property §3 was protecting: `$0`, no account,
no build step, no deploy, one link that works. **A static file calling a public API is still a
static file.**

[`SIMPLIFY.md`](SIMPLIFY.md) §4.3–4.4 has since cut both calls for unrelated reasons — the
app now ships cached real responses and a committed data snapshot, and makes **zero network
calls at runtime**. That strengthens this section rather than changing it: there is now not
even a request to be rate-limited on stage.

### 6b · A key we **have** is as unusable as a key we lack

Recorded 2026-10-06, because it came up and the reasoning is not obvious:

> "We have an API key for a model" is **not** an argument for using one.

The constraint was never key *acquisition*. It is that **a key shipped in client-side
JavaScript is readable by anyone who opens View Source** — so publishing the page publishes
the credential. Making it safe requires a proxy that holds the key server-side, which is a
server, which re-fires trigger #1 for real and costs every property in §3.

This applies to every key-bearing idea that has been floated: an LLM criteria parser, an
AI chat surface, an AI document reader, a live wearable OAuth integration. The answer is the
same in each case, and it is not "no" — it is **"find the keyless route, and it is usually
better anyway."** Two worked examples, both now shipping:

| Wanted | Key route | Keyless route taken |
|---|---|---|
| Read a lab document | Send the photo to a model API | `Tesseract.js` OCR in-browser, feeding the parser we had to write regardless. **More demonstrated coding skill, not less** |
| Real wearable vitals | Garmin Health API: partner approval, OAuth 1.0a signing, a webhook endpoint we host | A local Python script writes `garmin.json`; the app reads a committed static file. A **build-time pipeline, not a backend** — credentials never leave the operator's machine |

The second pattern generalizes and is worth naming: **when real data is needed but a server is
not allowed, move the credentialed work to build time and commit the result.** Nothing listens
on a port, nothing is deployed, nothing can be down during a demo, and the data is genuinely
real.

If an LLM pass is ever added, **re-read this section first** — it is no longer a free decision
at that point, and [`REBUILD.md`](REBUILD.md) §7 explains why the deterministic parser is also
the better answer on the merits.

---

## 7 · Sources

Everything in §2 is measured from `index.html` at the time of this decision, not estimated:
line ranges from the `<style>`/`<script>` boundaries, `112K` from `du`, the ID and global
counts from `grep`. Re-measure before quoting these if the file has moved on.
