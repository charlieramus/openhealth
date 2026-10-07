# OpenHealth — Documentation

Thirteen docs, five groups. Start wherever your question is.

> **If you read one thing, read [`SIMPLIFY.md`](SIMPLIFY.md).** Two decision docs stack:
>
> - **2026-10-02, [`REBUILD.md`](REBUILD.md)** — the health-data *aggregation* story is out
>   (not buildable by one student, and never the interesting part), **criteria parsing** is
>   in, and the "first consumer trial matcher" claim was deleted as false.
> - **2026-10-06, [`SIMPLIFY.md`](SIMPLIFY.md)** — **the app stops asking what condition you
>   have.** Input becomes your own documents (OCR) and your own watch data. The synthetic
>   patient, the doctor-send flow, the live registry search and the FHIR server call are all
>   cut, against a single standard: *everything has to be actually real; the only accepted
>   limitation is no backend.*
>
> Anything in these docs written before 2026-10-06 and not yet reconciled should be read
> against `SIMPLIFY.md`.

---

## Start here

| Doc | Answers | Read if |
|-----|---------|---------|
| [**BRIEF.md**](BRIEF.md) | What is OpenHealth, and the six required class deliverable elements | You have two minutes and need the whole idea |
| [**SIMPLIFY.md**](SIMPLIFY.md) | What is being built right now: the no-condition inversion, the two keyless input rails, the Health Score formula, and everything that got deleted | You're about to write code, or you want to know what changed on 2026-10-06 |
| [**REBUILD.md**](REBUILD.md) | What the app should actually *do*, why the pivot happened, and the two APIs that make it buildable for $0 | You're asking "does this thing actually work?" — read it after `SIMPLIFY.md` |
| [**MISSION.md**](MISSION.md) | Why it exists, what we won't do, how we'd know it worked | You want the pitch at 10 seconds, 30 seconds, or 2 minutes |

## How it works

| Doc | Answers | Read if |
|-----|---------|---------|
| [**ARCHITECTURE.md**](ARCHITECTURE.md) | How data is collected from APIs, normalized, matched, and distributed — with flowcharts | You want to see the wires. **This is the API flow doc** |
| [**BUILDSPEC.md**](BUILDSPEC.md) | The screen-by-screen spec the prototype was built from | You're changing the prototype |
| [**DESIGN.md**](DESIGN.md) | Color, type, layout, motion, voice | You're touching anything visual |
| [**STACK.md**](STACK.md) | Why the prototype is one static HTML file and not Next.js, what a port would cost, and what would change the answer | You're asking "shouldn't this be a framework?" or planning Figma handoff |

## Is it a business

| Doc | Answers | Read if |
|-----|---------|---------|
| [**COSTS.md**](COSTS.md) | What it costs to run at 1k / 50k / 500k users, benchmarked against real vendor prices; the revenue model and unit economics | You want the numbers, with the arithmetic shown |
| [**MARKET.md**](MARKET.md) | Who else does this — the B2B engines *and* the consumer tools — market size, and the precise competitive claim that survives scrutiny | You're asking "hasn't someone built this?" **Read §2 before repeating any claim about being first** |

## What could go wrong, and what's next

| Doc | Answers | Read if |
|-----|---------|---------|
| [**RISKS.md**](RISKS.md) | The full risk register, the consequence we can't remove, HIPAA and FDA surface, ethical commitments | You're evaluating whether this is responsible |
| [**ROADMAP.md**](ROADMAP.md) | The 4-week build plan to the Oct 26 Congressional App Challenge deadline, what's being cut, and the submission checklist | You're asking "what's left to build?" |

## Presenting it

| Doc | Answers | Read if |
|-----|---------|---------|
| [**PITCH.md**](PITCH.md) | The 2–4 min two-person mock Shark Tank script, the $250k/20% offer sheet, the negotiation ladder, and split Q&A prep | You're presenting tomorrow. **Speaking time is split equal by word count — rebalance if you edit a beat** |

---

## Reading paths

**For the mock pitch panel (rehearsal)**
→ [`PITCH.md`](PITCH.md) start to finish, then [`COSTS.md`](COSTS.md) §5 and §7 so you can
defend the offer sheet under questioning

**For a class presentation or a judge (15 min)**
→ [`BRIEF.md`](BRIEF.md) → [`MISSION.md`](MISSION.md) §"The pitch, at three lengths" →
[`ARCHITECTURE.md`](ARCHITECTURE.md) §1 (the one big diagram) →
[`RISKS.md`](RISKS.md) §1 (the unintended consequence)

**For "is this real?" (45 min)**
→ [`MARKET.md`](MARKET.md) → [`COSTS.md`](COSTS.md) → [`ROADMAP.md`](ROADMAP.md)
§"Appendix A — the hypothetical company roadmap"

**For an engineer picking this up**
→ [`SIMPLIFY.md`](SIMPLIFY.md) (what we're building now) → [`REBUILD.md`](REBUILD.md) (why) →
[`ARCHITECTURE.md`](ARCHITECTURE.md) **§4a — the parser/evaluator contract** →
[`BUILDSPEC.md`](BUILDSPEC.md) → [`DESIGN.md`](DESIGN.md) → [`STACK.md`](STACK.md) §6a →
`../index.html`

**For "what do I build next, right now"**
→ [`SIMPLIFY.md`](SIMPLIFY.md) §7 (the ordered item list, with the cut order) →
[`ARCHITECTURE.md`](ARCHITECTURE.md) §4a (the types and function signatures)

**For a security or privacy reviewer**
→ [`RISKS.md`](RISKS.md) → [`ARCHITECTURE.md`](ARCHITECTURE.md) §6 (trust boundary) and §5
(distribution)

---

## Conventions

**Prototype vs. real deployment.** `BRIEF.md`, `BUILDSPEC.md`, `DESIGN.md`, `STACK.md`,
`REBUILD.md`, and `SIMPLIFY.md` describe **what exists**. `ARCHITECTURE.md`, `COSTS.md`, `MARKET.md`, `RISKS.md`,
and `ROADMAP.md` describe **what a real deployment would be**. Every doc in the second group
says so at the top.

The line between them moved on 2026-10-02, and again on 2026-10-06. It is no longer "fake
data, no APIs" — and as of `SIMPLIFY.md` there is no "depicted, not implemented" row left in
the prototype at all:

| In the prototype | Status |
|---|---|
| **Trials** | **Real** — ClinicalTrials.gov records saved verbatim; the app parses their raw criteria text at runtime |
| **The matching engine** | **Real** — every score computed from a structured profile |
| **Lab values** | **Real** — OCR'd in-browser from actual documents (Tesseract.js) |
| **Vitals** | **Real** — the repo owner's own Garmin data, via a local sync script that commits `garmin.json` |
| **The data standard** | **Real** — FHIR R4 / US Core shapes with LOINC codes. The *format*; the server call is cut |
| **Patient data** | **Never real.** The owner's own fitness data is not patient data |
| **Aggregation across providers, and record delivery to a doctor** | **Deleted, not depicted.** The doctor-send flow is replaced by a real downloadable appointment prep sheet |

**Number labels.** In `COSTS.md`, `MARKET.md`, and `ROADMAP.md`:

| Label | Means |
|-------|-------|
| `[sourced]` | A public price or published figure, with a link in that doc's sources section |
| `[modeled]` | Arithmetic we did from sourced inputs — the work is shown |
| `[assumed]` | A planning estimate with no source. **These are the ones to challenge** |

**Single source of truth.** `BRIEF.md` owns the concept. `MARKET.md` §2 owns every
competitive claim. `SIMPLIFY.md` owns the current build order, the cut list and the Health
Score formula. `REBUILD.md` owns the wedge and the sources behind the statistics. `ARCHITECTURE.md` §4a owns the parser/evaluator contract.
`MISSION.md` owns the positioning. `DESIGN.md` owns the visual tokens. `ROADMAP.md` owns the
schedule. If a fact appears in two docs and they disagree, the owning doc wins — and the other
one is a bug.

**Never quote a match score or a Health Score as a constant.** Both are engine output and
change with the profile. Any doc containing a literal like "87/100", "89" or "79/100" is
stale by construction.

**Not legal or medical advice.** Every regulatory claim in `RISKS.md` needs review by a
healthcare attorney before OpenHealth touches one real patient record.
