# OpenHealth — Documentation

Eleven docs, five groups. Start wherever your question is.

---

## Start here

| Doc | Answers | Read if |
|-----|---------|---------|
| [**BRIEF.md**](BRIEF.md) | What is OpenHealth, and the six required class deliverable elements | You have two minutes and need the whole idea |
| [**MISSION.md**](MISSION.md) | Why it exists, what we won't do, how we'd know it worked | You want the pitch at 10 seconds, 30 seconds, or 2 minutes |

## How it works

| Doc | Answers | Read if |
|-----|---------|---------|
| [**ARCHITECTURE.md**](ARCHITECTURE.md) | How data is collected from APIs, normalized, matched, and distributed — with flowcharts | You want to see the wires. **This is the API flow doc** |
| [**BUILDSPEC.md**](BUILDSPEC.md) | The three-screen spec the prototype was built from | You're changing the prototype |
| [**DESIGN.md**](DESIGN.md) | Color, type, layout, motion, voice | You're touching anything visual |
| [**STACK.md**](STACK.md) | Why the prototype is one static HTML file and not Next.js, what a port would cost, and what would change the answer | You're asking "shouldn't this be a framework?" or planning Figma handoff |

## Is it a business

| Doc | Answers | Read if |
|-----|---------|---------|
| [**COSTS.md**](COSTS.md) | What it costs to run at 1k / 50k / 500k users, benchmarked against real vendor prices; the revenue model and unit economics | You want the numbers, with the arithmetic shown |
| [**MARKET.md**](MARKET.md) | Who else does this, why they're all B2B, market size, competitive position | You're asking "hasn't someone built this?" |

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
→ [`ARCHITECTURE.md`](ARCHITECTURE.md) → [`BUILDSPEC.md`](BUILDSPEC.md) →
[`DESIGN.md`](DESIGN.md) → [`STACK.md`](STACK.md) → `../index.html`

**For a security or privacy reviewer**
→ [`RISKS.md`](RISKS.md) → [`ARCHITECTURE.md`](ARCHITECTURE.md) §6 (trust boundary) and §5
(distribution)

---

## Conventions

**Prototype vs. real deployment.** The prototype (`../index.html`) is fake data, no APIs, no
persistence. `BRIEF.md`, `BUILDSPEC.md`, `DESIGN.md`, and `STACK.md` describe **what exists**.
`ARCHITECTURE.md`, `COSTS.md`, `MARKET.md`, `RISKS.md`, and `ROADMAP.md` describe **what a
real deployment would be**. Every doc in the second group says so at the top.

**Number labels.** In `COSTS.md`, `MARKET.md`, and `ROADMAP.md`:

| Label | Means |
|-------|-------|
| `[sourced]` | A public price or published figure, with a link in that doc's sources section |
| `[modeled]` | Arithmetic we did from sourced inputs — the work is shown |
| `[assumed]` | A planning estimate with no source. **These are the ones to challenge** |

**Single source of truth.** `BRIEF.md` owns the concept and the fake-data values.
`MISSION.md` owns the positioning. `DESIGN.md` owns the visual tokens. If a fact appears in
two docs and they disagree, the owning doc wins — and the other one is a bug.

**Not legal or medical advice.** Every regulatory claim in `RISKS.md` needs review by a
healthcare attorney before OpenHealth touches one real patient record.
