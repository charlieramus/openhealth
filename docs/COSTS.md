# OpenHealth — Cost Model & Unit Economics

> What it would actually cost to build and run OpenHealth for real, benchmarked against
> the prices real vendors and real competitors charge today.
>
> **Every number is labeled.** `[sourced]` means a public price or published figure, with a
> link in §9. `[modeled]` means arithmetic we did from sourced inputs — the work is shown.
> `[assumed]` means a planning estimate with no source; treat it as the thing to challenge.
>
> **What the prototype costs today: $0.** It is one static HTML file published as an
> artifact. Everything below is the cost of the product it depicts.
>
> Prices checked September 2026.

---

## 1 · Executive summary

| | Pilot (1,000 users) | Growth (50,000) | Scale (500,000) |
|---|---|---|---|
| **Monthly run cost** | ≈ $1,700 | ≈ $27,150 | ≈ $172,000 |
| **Cost per user / month** | **$1.70** | **$0.54** | **$0.34** |
| One-time / annual overlay | $10k–$30k compliance setup | + SOC 2 and pen testing, $40k–$100k/yr | + direct integrations, clinical review |

**Three findings that matter more than the totals:**

1. **Data aggregation is the cost of this business** — 24% of spend at pilot, 58% at scale.
   The trial registry, which is the clever part of the product, is free.
2. **Cost per user falls by 5x from pilot to scale**, because the two largest fixed costs
   (HIPAA hosting, registry mirror) barely move while users grow 500x.
3. **Infrastructure is not the risk. Acquisition is.** The unit cost of serving a user is
   about 34 cents a month at scale. Healthcare's benchmark cost to *acquire* a patient is
   about $560 `[sourced]`. If we pay anything close to that, nothing else in this document
   saves us. See §7.

---

## 2 · What each input actually costs (the sourced layer)

### Health data aggregation — the big line item

| Vendor | Published price | Notes |
|--------|----------------|-------|
| **Metriport** | **$0.20 per user / month** `[sourced]` | The only transparently published per-user price in the category. Free tier available |
| **1upHealth** | Custom / enterprise `[sourced]` | Not published. Priced on products selected, member connections, data volume, and compliance scope |
| **Health Gorilla** | Not published `[sourced]` | TEFCA-designated Qualified Health Information Network |

**Planning figure: $0.20–$0.40 per user per month `[modeled]`** — Metriport's published rate
as the floor, with a premium at low volume where we have no negotiating leverage. We model
$0.40 at pilot, $0.28 at growth, $0.20 at scale.

### Trial data — free

ClinicalTrials.gov REST API v2: **no API key, no signup, no cost**, rate-limited to roughly
50 requests per minute per IP `[sourced]`.

The rate limit, not the price, is the constraint — which is why
[`ARCHITECTURE.md`](ARCHITECTURE.md) §2 mirrors the registry nightly instead of querying it
live. **Consequence: trial-data cost is flat at every scale.** A nightly sync for 1,000
users and for 500,000 users costs the same.

### EHR integration — cheaper than people assume

| Item | Cost | Who pays |
|------|------|----------|
| Epic read-only USCDI FHIR APIs | **$0 to the developer** `[sourced]` | The health system, which pays Epic $4,500–$47,000/yr per production instance (five tiers, or from $300 for a single API) `[sourced]` |
| Registering on Epic on FHIR | **Free** `[sourced]` | — |
| Epic **Vendor Services** (optional paid developer program: support, testing tools, private APIs) | **from $1,900/yr** `[sourced]` | Us |
| Epic **Showroom / Connection Hub** listing | **$500 per product per year** `[sourced]` | Us — but only available once the product is in production with at least one Epic customer |

**Total Epic-side cost to us: about $2,400/year.** The expensive integration work is
engineering time, not license fees. Note that App Orchard and App Market no longer exist —
they were replaced by Showroom and Vendor Services `[sourced]`.

### HIPAA-compliant hosting

| Option | Cost | Notes |
|--------|------|-------|
| AWS / GCP / Azure | Usage-based, **no flat HIPAA fee** `[sourced]` | Raw fees can start under $100/mo, but managed setup and ongoing compliance work typically puts small deployments at $400+ `[sourced]` |
| **Aptible** (managed HIPAA PaaS) | Production tier **from ~$499/mo** `[sourced]` | Compliance scaffolding included |
| Typical early-stage digital-health budget | **$1,000–$5,000/mo** for HIPAA-eligible infra and tooling `[sourced]` | |
| One-time compliance setup | **$10,000–$30,000** for policies, legal review, and risk assessment (before any SOC 2 audit) `[sourced]` | |

**Every vendor that touches PHI needs a signed Business Associate Agreement. A missing BAA
is a HIPAA violation on its own, regardless of how strong the other controls are**
`[sourced]`. That is a contract cost and a legal-review cost, not a line item on a
dashboard — which is exactly why it gets missed.

---

## 3 · Matching compute — the one cost we control by design

This is the only major cost that is a function of *our engineering choices* rather than a
vendor's price list. It is worth showing the arithmetic.

### Per-run token math `[modeled]`

One match run for one patient, using the funnel in [`ARCHITECTURE.md`](ARCHITECTURE.md) §4:

| | Value | Source of the number |
|---|---|---|
| Studies after Stage 1 structured prefilter | 40 candidates | `[assumed]` — tune this and everything below moves |
| Eligibility criteria text per study | ~1,400 tokens | `[assumed]` — criteria are typically several hundred words |
| Patient clinical profile | ~500 tokens | `[assumed]` |
| Instructions / schema | ~400 tokens | `[assumed]` |
| Output per study (per-criterion verdicts + evidence) | ~250 tokens | `[assumed]` |

**Stage 2 on Claude Haiku 4.5** — $1.00 per million input tokens, $5.00 per million output
`[sourced]`:

```
input :  40 × (1,400 + 500 + 400) =  92,000 tok × $1.00/M = $0.092
output:  40 × 250                 =  10,000 tok × $5.00/M = $0.050
                                                   subtotal  $0.142
```

**Escalation on ambiguous criteria** — 15% of candidates `[assumed]` re-read by Claude
Sonnet 5 at $2.00 / $10.00 per million `[sourced]`:

```
input :   6 × 2,300 = 13,800 tok × $2.00/M = $0.028
output:   6 ×   400 =  2,400 tok × $10.00/M = $0.024
                                   subtotal  $0.052
```

**Cost per full match run ≈ $0.19** at list price `[modeled]`.

### Three levers that cut that number

| Lever | Effect | Why it works |
|-------|--------|--------------|
| **Prompt caching** | Up to ~40% off Stage 2 input | The instructions and patient profile are identical across all 40 candidates in a run — cache that prefix once, pay a fraction on reads |
| **Batch API** | **50% off** the nightly re-scoring runs | Re-scoring when the registry changes is not latency-sensitive. Only the user-triggered run needs to be synchronous |
| **A tighter Stage 1 prefilter** | **Linear.** 40 → 20 candidates halves the whole bill | The single highest-leverage engineering investment in the product |

**Planning figure: 2 runs per active user per month `[assumed]`** — one when new labs
arrive, one when the registry delta produces new candidates.

| Scale | Per-run cost | Runs/user/mo | Per active user / month |
|-------|-------------|--------------|------------------------|
| Pilot (list price, no optimization) | $0.19 | 2 | **$0.30** (rounded up) |
| Growth (caching + batch on one run) | ~$0.10 | 2 | **$0.20** |
| Scale (+ tightened prefilter to ~20 candidates) | ~$0.065 | 2 | **$0.13** |

**This is the good news in the model.** Matching — the thing that sounds expensive, the
"AI cost" a reviewer will ask about first — is roughly a quarter of what we pay the data
aggregator. The funnel design is why.

---

## 4 · Full run cost by scale `[modeled]`

Assumes 60% of registered users are monthly active at pilot and growth, 55% at scale
`[assumed]`.

### Tier 1 — Pilot · 1,000 users · 600 active

| Line | Monthly | Share |
|------|---------|-------|
| Data aggregation — 1,000 × $0.40 | $400 | 24% |
| HIPAA hosting (Aptible production + managed Postgres + backups) | $700 | 41% |
| Matching compute — 600 × $0.30 | $180 | 11% |
| Epic Vendor Services + Showroom listing ($2,400/yr) | $200 | 12% |
| Observability (logs, error tracking, uptime) | $120 | 7% |
| Transactional messaging (push, SMS, email) | $60 | 4% |
| Registry mirror (VM, storage, nightly ETL) | $40 | 2% |
| **Total** | **≈ $1,700** | |
| **Per user / month** | **$1.70** | |

*Plus one-time: $10,000–$30,000 compliance setup `[sourced]`.*

### Tier 2 — Growth · 50,000 users · 30,000 active

| Line | Monthly | Share |
|------|---------|-------|
| Data aggregation — 50,000 × $0.28 | $14,000 | 52% |
| Matching compute — 30,000 × $0.20 | $6,000 | 22% |
| HIPAA hosting (multi-AZ, monitoring) | $4,500 | 17% |
| Transactional messaging | $1,100 | 4% |
| Observability | $900 | 3% |
| Vendor programs | $400 | 1% |
| Registry mirror | $250 | 1% |
| **Total** | **≈ $27,150** | |
| **Per user / month** | **$0.54** | |

*Plus annually: SOC 2 Type II audit $25k–$60k, third-party penetration test $15k–$40k
`[assumed]`, and the first dedicated security hire.*

### Tier 3 — Scale · 500,000 users · 275,000 active

| Line | Monthly | Share |
|------|---------|-------|
| Data aggregation — 500,000 × $0.20 | $100,000 | 58% |
| Matching compute — 275,000 × $0.13 | $35,750 | 21% |
| HIPAA hosting (multi-region) | $20,000 | 12% |
| Transactional messaging | $8,000 | 5% |
| Observability | $4,500 | 3% |
| Vendor programs + direct integrations | $3,000 | 2% |
| Registry mirror | $600 | <1% |
| **Total** | **≈ $172,000** | |
| **Per user / month** | **$0.34** | |

### What the shape tells you

```
Cost per user per month
$1.70  ████████████████████  1,000 users
$0.54  ██████                50,000 users
$0.34  ████                  500,000 users
```

Two fixed costs — HIPAA hosting and the registry mirror — are 43% of the pilot bill and 12%
of the scale bill. Everything else is genuinely per-user. **The business gets structurally
cheaper per user as it grows, and the floor is the aggregator's per-member price.** That
floor is the number to renegotiate, or eventually engineer around with direct integrations.

---

## 5 · Revenue model — charging the budget that already exists

We do not charge patients. Ever — see [`MISSION.md`](MISSION.md). So the money has to come
from somewhere that is already spending it on this exact problem.

### What trial recruitment costs today

| Benchmark | Figure | Note |
|-----------|--------|------|
| Cost per enrolled subject, industry-sponsored trials | **~$6,094**, excluding overhead `[sourced]` | From a 2003 *JCO* analysis — **dated**. Roughly $10,000–$12,000 in 2026 dollars on general inflation `[modeled]`; medical cost inflation would put it higher |
| Centralized patient-outreach recruitment, cost per enrolled patient | **$143 (vaccine studies) to $11,392 (immunology)** `[sourced]` | A 2026 study. The 80x spread is the real story: recruitment cost is dominated by therapeutic area |
| Patient recruitment as a share of total trial budget | **~20%** `[sourced]` | Alongside site costs ~30%, data management ~15%, regulatory ~10% |
| Trials missing their original enrollment timeline | **~80%** `[sourced]` | The reason any of this is a market |

### Our price

**$400 per qualified, consented, site-accepted referral `[assumed]`.**

That sits inside the sourced outreach range and below its midpoint, which is the whole
argument: we are cheaper than the channel a sponsor is using today, and the patient arrives
pre-screened against the actual criteria.

We bill on **site acceptance**, not on a click or a lead. A referral that fails screening
earns nothing. That alignment is deliberate — it makes score honesty (§3 of
[`ARCHITECTURE.md`](ARCHITECTURE.md)) a commercial requirement, not just an ethical one.

### The funnel `[assumed]` — and this is the number to attack

Per 100 monthly active users:

```
100 monthly active users
 └─ 12  see at least one match scoring ≥ 70/100        (12%)
     └─ 4  send records to a doctor or site            (33% of matched)
         └─ 1  accepted by a site as qualified         (25% of sent)

= 1.0% of MAU produce a billable referral per month
= $4.00 revenue per monthly active user per month
```

| Scenario | Referral rate | Revenue / MAU / mo |
|----------|--------------|-------------------|
| Pessimistic | 0.25% | $1.00 |
| **Base** | **1.0%** | **$4.00** |
| Optimistic | 2.5% | $10.00 |

### Does it work?

| | Pilot (600 MAU) | Growth (30,000 MAU) |
|---|---|---|
| Run cost | $1,700/mo | $27,150/mo |
| Revenue — pessimistic | $600 | $30,000 |
| Revenue — base | $2,400 | $120,000 |
| Revenue — optimistic | $6,000 | $300,000 |

**The honest read:** the base case is contribution-positive at pilot scale. The pessimistic
case loses ~$1,100/month at pilot and reaches breakeven somewhere around 50,000 users. The
model does not require the optimistic case to work — but it does require the funnel to
clear roughly 0.3%, and **we have no evidence for that number yet.** Measuring it is the
single most important goal of the pilot ([`ROADMAP.md`](ROADMAP.md)).

### Revenue we have deliberately refused

| Option | Why not |
|--------|---------|
| Patient subscription | Breaks the mission. The patients who most need trials are least able to pay |
| Selling de-identified datasets | We would become the data broker we exist to route around |
| Hospital-facing admin dashboard | The moment the hospital is the customer, the patient stops being the user |
| Advertising | Targeting ads by health condition is the worst version of this product |

Each of these would be *more* profitable than the referral model in year one. Listing them
is the point: the constraint is real, and it's chosen.

---

## 6 · How the app would run — the operating cadence

Cost is a function of what runs when, so this table belongs here rather than in the
architecture doc.

| Job | Trigger | Frequency | Cost driver |
|-----|---------|-----------|-------------|
| Registry full sync | Cron, overnight | Nightly | Flat — one job serves all users |
| Registry delta poll | Cron | Hourly | Flat |
| Patient data refresh | Per connected source | Daily, or on source webhook | Per user (aggregator) |
| Match run — user-triggered | Patient opens Trials tab after new data | On demand | Per active user, synchronous, full price |
| Match run — re-score | New registry candidates affect a stored profile | Batched nightly | Per active user, **Batch API at 50% off** |
| Referral delivery | Patient taps send | On demand | Negligible |
| Consent ledger write | Every share and every revocation | On demand | Negligible, non-negotiable |

**The cost-control principle: only the run a patient is waiting on pays full price.**
Everything else batches overnight.

### Service levels we'd hold ourselves to `[assumed]`

| | Target | Why |
|---|--------|-----|
| Trials tab loads | < 1.5s p95 | It's the payoff screen |
| A user-triggered match run completes | < 20s p95 | Long enough to need a progress state, short enough to wait for |
| Registry freshness | < 24h | Trials close; a stale "recruiting" badge is a cruel bug |
| Referral delivery confirmed | < 5 min | The patient just watched a confirmation animation |
| Consent revocation takes effect | < 60s | Non-negotiable. This one is a promise, not a target |

---

## 7 · The real risk: acquisition cost

Everything above says serving a user costs 34 cents a month at scale. Here is the number
that could still sink it.

| | Figure |
|---|--------|
| Healthcare benchmark cost to acquire a patient | **~$560** `[sourced]` |
| Our revenue per registered user per month (base case, 55% active) | **$2.20** `[modeled]` |
| Our cost per registered user per month (scale) | **$0.34** `[modeled]` |
| Contribution margin per user per month | **$1.86** `[modeled]` |
| Assumed retention | 18 months `[assumed]` |
| **Lifetime contribution per user** | **≈ $33** `[modeled]` |
| **Maximum CAC for a 3:1 ratio** | **≈ $11** `[modeled]` |

**An $11 CAC ceiling against a $560 category benchmark is a 50x gap.** Paid acquisition
cannot close it. That is not a marketing problem to solve later — it determines the
go-to-market, and the only viable answer is partner distribution.

**The precedent is in the market already.** Antidote Match reaches an estimated **15 million
patients a month** by embedding its trial search across **more than 250 patient communities
and health portals** — sponsors and advocacy organizations pay to distribute through those
trusted channels, and patients pay nothing `[sourced]`.

So: condition-specific advocacy organizations, patient communities, and provider referral —
channels where the trusted intermediary already has the audience and a mission-aligned
reason to introduce us. Target blended CAC **$15–$40 `[assumed]`**, and be honest that even
the low end of that is above the $11 ceiling until either retention or referral rate beats
the base case.

**Conclusion: distribution partnerships are not a growth tactic for this product. They are
a precondition.**

---

## 8 · What would break this model

| Risk | Impact | What we'd do |
|------|--------|--------------|
| Aggregator raises per-member price 3x | Scale cost/user $0.34 → $0.74; still viable, margin halves | Direct Epic/Oracle integrations for top systems; multi-vendor sourcing |
| Stage 1 prefilter is weaker than assumed (200 candidates, not 40) | Matching cost 5x, becomes the largest line item | The prefilter is the highest-leverage thing to engineer well. Cap candidates and page |
| Referral funnel comes in at 0.1%, not 1% | No viable business at any scale | Kill or pivot. This is the pilot's go/no-go metric |
| Sites won't pay a consumer-sourced referral fee | Revenue model gone | Test with signed letters of intent *before* building the billing side |
| One breach | Existential, independent of cost | See [`RISKS.md`](RISKS.md) |
| CMS/ONC weaken patient-access API mandates | Aggregation gets harder and costlier | The regulatory tailwind is load-bearing. Worth tracking as a real dependency |

---

## 9 · Sources

Health data aggregation
- [Metriport pricing (SaaSworthy)](https://www.saasworthy.com/product/metriport/pricing) — $0.20/user/month
- [Metriport Medical API](https://www.metriport.com/medical)
- [1upHealth Patient Access API](https://1up.health/products/1up-comply/1up-patient-access-api/)
- [1upHealth pricing (SaaSworthy)](https://www.saasworthy.com/product/1uphealth/pricing)
- [Health Gorilla](https://www.healthgorilla.com/)

Trial registry
- [ClinicalTrials.gov API documentation](https://clinicaltrials.gov/data-api/api)
- [How to search ClinicalTrials.gov programmatically (v2 API, rate limits)](https://dev.to/avabuildsdata/how-to-search-clinicaltrialsgov-programmatically-the-v2-api-is-actually-good-now-2i2a)

EHR integration
- [Epic on FHIR — developer portal](https://fhir.epic.com/)
- [How to get your app into Epic, 2026 — Vendor Services, Showroom, USCDI subscription tiers](https://nirmitee.io/blog/how-to-get-your-app-into-epic/)
- [Epic introduces App Orchard low-cost option (Healthcare IT News)](https://www.healthcareitnews.com/news/epic-introduces-app-orchard-low-cost-option)
- [Epic EHR integration guide — FHIR, APIs, cost](https://topflightapps.com/ideas/how-integrate-health-app-with-epic-ehr-emr/)

HIPAA hosting and compliance
- [How much does HIPAA hosting cost in 2026?](https://hipaacomplianthosting.com/blog/how-much-does-hipaa-hosting-cost-2026)
- [What does a HIPAA-compliant cloud cost in 2026? (TechRev)](https://www.techrev.us/blog/what-does-a-hipaa-compliant-cloud-cost-in-2026/)
- [HIPAA compliance for digital health startups (Aptible)](https://www.aptible.com/hipaa/hipaa-overview)
- [HIPAA-compliant app hosting: who signs a BAA in 2026](https://hipaacomplianthosting.com/blog/hipaa-compliant-app-hosting)

Matching compute
- [Claude API pricing](https://claude.com/pricing) — Haiku 4.5 $1/$5 per MTok; Sonnet 5 $2/$10 per MTok (September 2026)

Trial recruitment economics
- [The Costs of Conducting Clinical Research (*JCO*, 2003)](https://ascopubs.org/doi/10.1200/JCO.2003.08.156) — ~$6,094 per enrolled subject excluding overhead
- [Measuring Centralized Patient Outreach Recruitment Strategies and their Costs in Clinical Trials (*Therapeutic Innovation & Regulatory Science*, 2026)](https://link.springer.com/article/10.1007/s43441-026-00991-3) — $143–$11,392 cost per enrolled patient
- [The Ultimate Guide to Clinical Trial Costs (Sofpromed)](https://www.sofpromed.com/ultimate-guide-clinical-trial-costs) — trial budget breakdown
- [AI Patient Recruitment for Clinical Trials: Platform Guide (IntuitionLabs)](https://intuitionlabs.ai/articles/ai-patient-recruitment-clinical-trials-platforms) — ~80% of trials miss enrollment timelines; Antidote Match distribution model

Acquisition cost
- [Average Customer Acquisition Cost industry benchmarks 2026 (Userpilot)](https://userpilot.com/blog/average-customer-acquisition-cost/) — healthcare ~$560 per patient (Accenture)
- [Customer Acquisition Cost benchmarks 2026 by industry](https://www.digitalapplied.com/blog/customer-acquisition-cost-benchmarks-2026-industry)

---

## Related docs

- [`MISSION.md`](MISSION.md) — the constraints that rule out the easier revenue models
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — the funnel design §3 depends on
- [`MARKET.md`](MARKET.md) — who we're priced against
- [`RISKS.md`](RISKS.md) — the costs that don't show up on an invoice
- [`ROADMAP.md`](ROADMAP.md) — what the pilot has to prove
