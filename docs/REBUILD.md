# OpenHealth — Rebuild: Making the App Actually Work

> ⚠️ **Partly superseded by [`SIMPLIFY.md`](SIMPLIFY.md), 2026-10-06.** Still the doc that
> explains *why the app is a criteria-parsing trial matcher at all*, and §1 (the rubric), §4
> (the false "first consumer matcher" claim), §5 (the wedge), §6 (the three design rules),
> §7 (why the parser is deterministic) and §9 (why live-vs-mirror is not a contradiction) are
> all unchanged and still binding.
>
> What `SIMPLIFY.md` changes: the app **stops asking what condition you have**; input becomes
> the user's own documents (OCR) and own watch data; and four things are cut for failing the
> standard that everything must be *actually real, not merely clickable* — the synthetic
> patient, the FHIR server call (§3.2 below, §8 item 6), live registry search (§8 item 1), and
> the doctor-send flow. **The build order in §8 is replaced by `SIMPLIFY.md` §7.**
>
> Note that §3's API evidence was *correct* and is not being disputed — both calls were
> verified working. They are cut for product reasons, not technical ones.

> **Decision doc.** Written 2026-10-02, 24 days before the Congressional App Challenge
> deadline (**Monday, October 26, 2026, 12:00 PM ET**).
>
> It answers one question: *the concept assumed aggregating health data from many
> provider APIs, which is not buildable by one student — so what should the app
> actually do instead?*
>
> It reverses one line on the [`ROADMAP.md`](ROADMAP.md) cut list and deletes one claim
> from [`BRIEF.md`](BRIEF.md). Both are named below with the evidence.

---

## 1 · What the rubric actually rewards

Scoring is **six sub-criteria, 5 points each, 30 total** — per the official 2026 rubric
archived at [`assets/intake/cac/CAC-Judging-Rubric.pdf`](../assets/intake/cac/). The
breakdown and our current standing are already worked out in
[`ROADMAP.md`](ROADMAP.md#what-is-actually-being-scored) and are not re-derived here. Two of
those six are what this document exists to move:

| Sub-criterion | 5 points looks like | Why this doc |
|---|---|---|
| **Function** | "App is functional with **complex features**" | The scale: 1 lacks functionality · 2 "contains snippets of code/action" · 3 works with errors · 4 fully functional · 5 complex features |
| **Code** | "**Explanation of code** indicates immense understanding" | You cannot explain an algorithm that does not exist. Function and Code move together |

**A UI mockup with hardcoded numbers sits at 2.** That is the single biggest available point
gain, and it is a coding-skill gain, not a design gain — no amount of visual polish moves
it. Note also that the broader public-facing criteria ("quality of the idea,"
"implementation," "demonstrated coding skill," and whether the app is "fully functional and
applicable for societal use") are the same scale in coarser language.

Context on the field: in 2025, **13,800+ students submitted 4,600+ apps**, 394 districts
participated, and ~70% of apps targeted civic engagement or social good. Health apps won
widely — *CanScreen* (tailored cancer-screening guidance), *MemoryLane* (Alzheimer's care
companion), *PhosTrack* (phosphate tracking for dialysis patients), *AnemoDx* (early anemia
detection), *Pulmo Lens* (pneumonia detection). Note the shape of every one: **narrow
condition, real computation, one clear user.** None of them aggregate an industry.

---

## 2 · The structural problem, stated honestly

The current concept has three layers. Only one of them was ever the interesting part.

| Layer | Current state | Honest verdict |
|---|---|---|
| **Aggregation** — pull a patient's data from 5+ portals | Fake data, described in the brief as "in a real deployment this is aggregated from healthcare APIs" | **Not buildable, and not the contribution.** 1upHealth and Health Gorilla do this; it needs contracts, not code |
| **Matching** — score the patient against trial eligibility | Already real: `matchScore()` computes a 0–100 from weighted per-criterion checks | **This is the app.** Keep and deepen |
| **Presentation** — the three screens | Strong; passed design review | Keep |

So the pivot is not "throw it out." It is: **delete the aggregation fantasy, replace it
with a real data path, and make matching the whole product.**

---

## 3 · Two verified facts that change the plan

Both tested live from this machine on 2026-10-02. Not assumed — the responses are
summarized below.

### 3.1 · ClinicalTrials.gov API v2 is fully open to a browser

```
GET https://clinicaltrials.gov/api/v2/studies?query.cond=anemia
    &filter.overallStatus=RECRUITING&fields=NCTId,BriefTitle,EligibilityCriteria
→ HTTP 200 · access-control-allow-origin: *
```

- **No API key, no signup, no auth.**
- `access-control-allow-origin: *` — callable from `fetch()` in a static HTML page.
- Returns `eligibilityCriteria` as **raw inclusion/exclusion text**, e.g.
  `"* Laboratory-confirmed diagnosis of sickle cell disease * Age >= 35 years old ..."`
- Practical ceiling is community-estimated at ~50 req/min per IP; undocumented, no
  rate-limit headers observed. Irrelevant at our volume.

**Consequence:** the trial side stops being seeded data and becomes **live search**. Zero
backend, zero cost, zero accounts. This is the headline capability.

### 3.2 · There is a free, CORS-enabled, real FHIR server with synthetic patients

```
GET https://r4.smarthealthit.org/Patient?_count=1                        → HTTP 200 · ACAO: <origin>
GET https://r4.smarthealthit.org/Observation?code=http://loinc.org|718-7 → HTTP 200
```

The SMART Health IT R4 reference server serves **US Core / FHIR R4** resources — `Patient`,
`Condition`, `Observation` (labs, by LOINC code), `MedicationRequest` — for synthetic
patients, over CORS, with no key.

This matters because of what it is *not*: it is not fake data in a JS object. It is a real
request, to a real FHIR server, parsing the real resource shapes that every US health
system is legally required to expose. The 21st Century Cures Act and the CMS
Interoperability rule mandate that every certified EHR offer exactly this patient-access
API; Epic and Oracle Health both run public sandboxes on the same standard.

**Consequence — this reverses a cut-list line.** [`ROADMAP.md`](ROADMAP.md) §"Cut list"
says: *"Real API connections (Epic, FHIR, aggregators) — No accounts, no BAAs, no time,
and zero judging benefit."* The accounts-and-BAAs part was right about **Epic production**.
It was wrong about FHIR generally, because the open sandbox needs none of those things.

The honest on-camera line becomes: **"The data standard is real and federally mandated. The
server is a public test server. The patient is synthetic. The trials are real."** That is a
stronger sentence than the current one, and it is true.

---

## 4 · The claim that has to be deleted

[`BRIEF.md`](BRIEF.md) §6 says OpenHealth is *"the **first consumer-facing clinical-trial
matcher.** Every existing tool is B2B, sold to hospitals and pharma."*

**This is false, and a judge finds out in one search.** Consumer-facing, free, patient-first
trial matchers that already exist:

| Tool | What it is |
|---|---|
| **ResearchMatch** | **NIH-funded**, free, nationwide, built specifically so patients find studies themselves |
| **Antidote Match** | Free patient-facing search; patients answer questions about history and demographics. Deployed across 180+ patient communities, part of Cancer Moonshot |
| **TrialJectory** | Patient-driven; AI extraction of eligibility criteria from ClinicalTrials.gov |

The B2B claim is accurate about MatchMiner and TrialMatchAI. It is not accurate about the
category. Leaving it in trades a few points of "originality" for a direct hit to
credibility — and credibility is the thing the rubric's top band ("indicates immense
understanding") is actually measuring.

---

## 5 · The new wedge — true, narrower, and harder

Drop "first consumer trial matcher." The defensible gap is one step further in.

**What every existing consumer tool does:** asks the patient a questionnaire, then
keyword-matches the answers to trials. The patient self-reports. The output is a list.

**What none of them shows the patient:** the arithmetic. Which specific criterion they pass
or fail, against which specific threshold, using their actual lab value.

And that gap has a real cost attached:

- Average **screen failure rate is 40–60%** across therapeutic areas — of 10 patients who
  start formal screening, 4 to 6 are rejected. In oncology, rare disease, and CNS, **70–80%**
  is not unusual.
- **Specific numeric biomarker thresholds** (HbA1c, creatinine, liver enzymes, platelet
  counts) are a leading screen-failure trigger, and those thresholds are often conservative
  — **many otherwise-eligible patients fall just outside the window** at the moment they
  happen to be measured.
- In early-phase oncology, criteria rule out **47.5% of patients who are in fact alive at
  6 months**, which the literature itself flags as questionable selection accuracy.

So the product sentence becomes:

> **OpenHealth reads a trial's eligibility criteria — which are published as unstructured
> free text — turns them into checkable rules, evaluates each rule against the patient's
> actual FHIR lab values, and shows a per-criterion audit: what passed, what failed, by how
> much, and which near-misses are worth asking a doctor about.**

That is a different app from a questionnaire, and it is a different app from a document
simplifier.

### Why this does not repeat the Gemini document-scanner that won the district

| | That app | This app |
|---|---|---|
| **Input** | A photo/PDF of a medical document | Structured FHIR `Observation` / `Condition` resources |
| **Core operation** | Summarize prose → simpler prose | Parse constraints → evaluate predicates → rank |
| **Output** | Easier-to-read text | A decision, with a numeric audit trail per criterion |
| **CS content** | Prompt + render | Text→predicate extraction, unit normalization, weighted scoring, near-miss detection |

Same domain, no overlap in the actual computation. If a judge saw both, they would not
describe them as the same idea.

---

## 6 · The rebuilt architecture

Still one static file, still no build step, still $0 — the [`STACK.md`](STACK.md) decision
holds, and §6 of that doc listed "real data or an API arrives" as a port trigger. It is
worth noting explicitly that **it does not fire here**: both APIs are unauthenticated GETs
with permissive CORS, so there is no secret to hide and no server to run. No Next.js.

```
┌─ INPUT ─────────────────────────────────────────────────────────┐
│  A. Connect a test record  → GET r4.smarthealthit.org/Patient   │
│       Condition, Observation (LOINC), MedicationRequest         │
│  B. Or enter it manually   → condition, age, sex, 4–6 labs      │
│       (also the offline demo path — never let the video depend  │
│        on someone else's uptime)                                │
│                        ↓                                        │
│            normalize → { age, sex, conditions[], labs{} }       │
│            with units coerced to a canonical unit per LOINC     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─ PROCESSING ────────────────────────────────────────────────────┐
│  1. GET clinicaltrials.gov/api/v2/studies                       │
│       query.cond=<condition>  filter.overallStatus=RECRUITING   │
│       filter.geo=distance(lat,lon,100mi)                        │
│       → N real trials, with raw eligibilityCriteria text        │
│                              ↓                                  │
│  2. CRITERIA PARSER  ← the actual computer science              │
│       split Inclusion / Exclusion blocks, then per bullet:      │
│         • numeric   "Hemoglobin >= 9 g/dL"  → {lab,op,val,unit} │
│         • range     "Age 18-65 years"       → {lab,lo,hi}       │
│         • presence  "Diagnosis of X"        → {condition}       │
│         • negation  "No prior Y"            → {exclude}         │
│         • unparsed  everything else         → {manual review}   │
│                              ↓                                  │
│  3. EVALUATOR                                                   │
│       each rule → PASS | FAIL | UNKNOWN | NEAR-MISS (within 10%)│
│       exclusion hit → hard block, score forced down             │
│       weighted sum → 0–100, UNKNOWNs reduce *confidence*,       │
│       not score — and the app says so                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─ OUTPUT ────────────────────────────────────────────────────────┐
│  Ranked trials, each with:                                      │
│    • score + confidence ("8 of 11 criteria checkable")          │
│    • per-criterion table: rule, your value, verdict             │
│    • NEAR-MISS callout: "Ferritin 8 ng/mL, needs >= 10 — short  │
│      by 2. Ask your doctor whether this is worth re-testing."   │
│    • the unparsed criteria, shown plainly, not hidden           │
│    • real NCT link, sponsor, phase, sites                       │
│    • one-tap question to a doctor, pre-filled with the failures  │
└─────────────────────────────────────────────────────────────────┘
```

### The three design rules that make it credible

1. **Never hide what you could not parse.** A tool that silently drops 40% of the criteria
   and shows a confident 87 is lying. Showing "8 of 11 criteria checkable" is more
   impressive to a judge than a fake 11 of 11, because it proves you know what the parser
   does and does not do.
2. **Confidence and score are separate numbers.** Unknowns lower confidence. Only real
   failures lower score. Conflating them is the most common bug in this class of tool.
3. **The score is never advice.** Output is "worth asking about," never "you qualify."
   Eligibility is determined by a screening visit. Say that in the UI, not just the video —
   it is also the correct answer to a judge's ethics question.

---

## 7 · Where AI belongs, and where it does not

Step 2 — free text → structured predicate — is the one place a model genuinely helps, and
it should be **the second implementation, not the first.**

| Approach | Cost | Coverage | What a judge sees |
|---|---|---|---|
| **Regex/rules parser** (build first) | $0, no key, offline-capable | Handles the common numeric, range, and presence patterns — which is most of what matters | Readable logic they can scroll through. Fully yours. Clean AI disclosure |
| **+ LLM extraction** (optional second pass) | API key, per-call cost, needs a proxy to hide the key — which breaks the no-backend property | Catches the messy long-form criteria | Better coverage, but "an API did it" |

**Recommendation: ship the deterministic parser.** It is the version where the coding-skill
points are unambiguously yours, it keeps the single-static-file architecture intact (an LLM
key cannot live in client-side JS), and it demos without a network dependency on a paid
service. If the LLM pass gets added, keep the extracted predicate visible on screen so the
output stays auditable rather than oracular — and disclose it precisely.

---

## 8 · Build order for 24 days

Feature freeze still lands **Saturday, October 18**; the video and submission still own the
final week. That leaves **~16 working days** for the rebuild.

| # | Work | Days | Why it is in this order |
|---|---|---|---|
| 1 | Live CT.gov search replacing seeded `TRIALS` | 2 | Biggest credibility gain per hour. Everything downstream needs real criteria text to parse |
| 2 | Criteria parser — numeric, range, presence, negation + `unparsed` bucket | 4 | The core CS. Build against ~20 saved real trials so it is testable offline |
| 3 | Evaluator: pass/fail/unknown/near-miss, score + separate confidence | 2 | Turns the parser into the product |
| 4 | Per-criterion audit UI on Screen 3 | 2 | This is the screen that wins the function points. Make the table the hero |
| 5 | Manual-entry input form + normalization | 1.5 | Also the offline demo path |
| 6 | FHIR connect against `r4.smarthealthit.org` | 2 | Headline feature, but last among the functional work — it is the one with an external dependency |
| 7 | Near-miss "ask your doctor" output + disclaimers | 1 | The distinctive output, and the ethics answer |
| 8 | Caching + graceful degradation when either API is down | 1.5 | A demo that dies on stage scores zero. Cache the last good response |
| — | **Freeze Oct 18** → video, six questions, AI disclosure, submit by **Oct 25** | 7 | Never submit into a noon cutoff |

**If something slips, cut in this order:** 6 (FHIR connect — manual entry covers input), then
7, then 1 (fall back to the ~20 saved real trials; criteria are still real, search is not
live). **Never cut 2, 3, or 4** — they are the app.

---

## 9 · What changes in the other docs

| Doc | Change |
|---|---|
| [`BRIEF.md`](BRIEF.md) | Delete "first consumer-facing clinical-trial matcher" (§4). Replace the §6 innovation claim with the §5 wedge above. Rewrite Input/Processing/Output to describe the real pipeline. The fake-data table shrinks to a synthetic *patient* — the trials are no longer in it |
| [`ROADMAP.md`](ROADMAP.md) | Cut-list line on FHIR is reversed with the §3.2 evidence. Weeks 1–3 replaced by §8 |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Add the parser/evaluator contract. Update §8's prototype-mapping table, which still says "a hardcoded 87/100." **§2's "why we mirror the registry" does not need reversing** — see below |
| [`STACK.md`](STACK.md) | Add a note that the §6 "real API arrives" port trigger was evaluated and **does not fire** — unauthenticated CORS GETs need no server |
| [`ROADMAP.md`](ROADMAP.md) risk register | Demo-specific risks go here, not in `RISKS.md`: CT.gov down or rate-limited mid-demo; the parser silently mis-extracting a threshold |
| [`RISKS.md`](RISKS.md) | **No change needed.** It is the hypothetical-company doc and already carries the right entries — #2 false hope, #3 false despair, #4 missed exclusion, #9 model error on criteria reading. The §5 design rules above are the prototype's implementation of #2 and #9 |

### Why `ARCHITECTURE.md` §2 is not a contradiction

That section argues the real system should **mirror** ClinicalTrials.gov nightly rather than
query it live, because "a single match run reads thousands of study records. At even 1,000
users that is impossible live — and it would be an abuse of a public good."

**That reasoning is correct, and it is about scale.** The prototype has **one** user and runs
one search returning on the order of 20 candidates — a handful of requests against a ~50
req/min ceiling. The two statements coexist:

> **Live query at prototype scale; nightly mirror at product scale.** The crossover is the
> point where one user's match run stops being a rounding error on a public API.

Say it that way in the video. "I query it live because I have one user; at a thousand users
I'd mirror it nightly, because of the rate limit and because it's a public good" is a
*better* answer than either half alone — it is exactly the scaling judgment the Code
sub-criterion is looking for.

---

## 10 · Sources

Judging criteria and field size — [Congressional App Challenge judging
guidelines](https://www.congressionalappchallenge.us/wp-content/uploads/2018/10/CAC_Rubric_2018.pdf),
[2025 CAC rules](https://www.congressionalappchallenge.us/wp-content/uploads/2024/04/2024-CAC-Rules.pdf),
[Lumiere guide to the 2026-27 challenge](https://www.lumiere-education.com/post/winning-the-congressional-app-challenge-everything-you-need-to-know).
2025 winners — [Rep. Gluesenkamp Perez (CanScreen)](https://gluesenkampperez.house.gov/posts/rep-gluesenkamp-perez-announces-2025-congressional-app-challenge-winners),
[Rep. Mannion (PhosTrack)](https://mannion.house.gov/media/press-releases/representative-mannion-ny-22-announces-2025-congressional-app-challenge),
[Rep. Lieu](https://lieu.house.gov/media-center/press-releases/rep-lieu-announces-winners-2025-congressional-app-challenge),
[Rep. Clyde (Pulmo Lens)](https://clyde.house.gov/news/documentsingle.aspx?DocumentID=3377).
APIs — live-tested 2026-10-02; [ClinicalTrials.gov API v2
reference](https://conorscode.github.io/clinicaltrials-api-reference/),
[SMART Health IT sandboxes](https://good-neighbor.smarthealthit.org/sandboxes/),
[Epic on FHIR docs](https://fhir.epic.com/Documentation?docId=fhir).
Existing consumer matchers — [ResearchMatch / Antidote / TrialJectory overview, ACS
CAN](https://www.fightcancer.org/sites/default/files/CT_MatchingServicesWhitepaper_ACSCAN_May2018Web_0.pdf),
[Antidote Match](https://www.antidote.me/blog/how-to-match-to-clinical-trials),
[patient-centric NLP trial matching,
PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10857751/).
Screen-failure rates — [Addressing screening failures in early-phase oncology trials,
PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12362514/),
[screen failure rate overview](https://trialpartners.co/articles/what-percentage-of-clinical-trial-patients-fail-screening-and-how-to-reduce-it).
