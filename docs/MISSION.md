# OpenHealth — Mission & Positioning

> What we are, in the fewest words that are still true. Every other doc in `docs/`
> answers to this one. If the mission changes, change it here first.

---

## Mission statement

**OpenHealth exists to put a patient's whole health record — and the clinical trials it
qualifies them for — in the patient's own hands.**

## Vision (the world if we win)

A patient never again learns about a trial they qualified for *after* it closed. The
default assumption flips: your health data is yours, assembled, legible, and working for
you — not scattered across five portals, each of which knows a fifth of you.

---

## The pitch, at three lengths

**10 seconds (the elevator)**
> Clinical trials hide who can join inside pages of medical fine print. OpenHealth reads it,
> checks it against your real lab results, and shows you exactly which number is keeping you
> out — and by how much.

**30 seconds (the judge)**
> Clinical trials publish who can join as free text full of numeric thresholds — "hemoglobin
> at least 9," "A1c between 7.5 and 9.5." Patients can't read it, so **40 to 60 percent of
> people who start screening get rejected**, often over one number they missed by a little.
> Trial search tools exist, but they ask you a questionnaire and hand you a list. OpenHealth
> reads the registry's own criteria text, turns each line into a rule, checks it against your
> actual labs, and shows you the arithmetic: *"Ferritin 8, this trial needs 10 — you're short
> by 2. Worth asking your doctor whether that's worth re-testing."* One tap sends that exact
> question to your doctor.

**2 minutes (the investor / the teacher)**
> Start with the number: roughly 80% of clinical trials miss their original enrollment
> timeline. Sponsors spend a fifth of a trial's budget hunting for patients. Meanwhile
> millions of patients would say yes if anyone asked them — they just never find out.
>
> That's not a data problem. The data exists, and since the 21st Century Cures Act it is
> legally required to be available to patients through APIs. The registry of every
> recruiting trial in the country is a free public API. The missing piece is a product
> that assembles one patient's scattered record, reads trial eligibility criteria against
> it, and hands the patient the answer.
>
> Every existing matcher solves this for the institution. MatchMiner runs inside Dana-Farber.
> Deep 6 AI mines hospital EHRs. TrialJectory profiles patients for sites. All valuable,
> all pointed the wrong way — the institution gets the match, and the patient hears about
> it only if someone remembers to call.
>
> OpenHealth points it at the patient. Free to the patient, forever. We aggregate through
> patient-access APIs the patient authorizes, run a two-stage match (structured prefilter,
> then criteria reasoning), and return a scored, explained result: here are the criteria
> you meet, here are the two we can't determine, take this to your doctor. Revenue comes
> from the recruitment budget that already exists — sites and sponsors pay for qualified,
> consented referrals, at a fraction of what centralized outreach costs them today.
>
> The prototype is three screens and it's live. See `README.md`.

---

## What we do / what we don't

| We do | We don't |
|-------|----------|
| Aggregate a patient's record with their explicit, revocable authorization | Buy, sell, broker, or rent health data — ever, at any price |
| Show a **scored, explained** trial match with per-criterion reasoning | Tell a patient they *are* eligible. Only a clinician and a site can say that |
| Hand the patient a prep sheet to take to their own doctor | Contact a clinician on the patient's behalf, or imply we have |
| Charge the recruitment budget that already exists | Charge the patient. Not a subscription, not a paywall, not an upsell |
| Say "we don't know" when a criterion is undecidable from the record | Guess, round up, or hide uncertainty to make a score look better |
| Translate labs into plain language | Diagnose, prescribe, or advise treatment |
| Read the patient's own records and tell them what they might qualify for | Ask the patient to name their condition before we will help them |

## Non-goals (deliberate, not "not yet")

1. **Not a telehealth product.** We connect you to *your* doctor, not to ours.
2. **Not a B2B EHR module.** The moment the hospital is the customer, the patient stops
   being the user. That's the exact failure we exist to fix.
3. **Not an AI doctor.** The model reads eligibility criteria. It does not offer medical
   opinions, and the UI never implies it does.
4. **Not international at launch.** The whole thesis rests on US patient-access API
   mandates. Other countries need a different product.
5. **Not a data platform with an app on top.** If the business ever pays better for the
   dataset than for the referrals, we've become the thing we replaced.
6. **We do not contact your doctor.** Not a message, not a referral, not a fax. We generate
   the sheet; you book the appointment and bring it. Any feature that implies a clinician is
   on the other end is a lie about what the software does — see
   [`SIMPLIFY.md`](SIMPLIFY.md) §4.1.
7. **We do not ask you what you have.** Every competitor opens with a questionnaire, which
   quietly requires the patient to already know the medical name for their situation. We
   read the record and do the work. See [`SIMPLIFY.md`](SIMPLIFY.md) §2.

---

## Values, each with a test

A value you can't fail isn't a value. Each of these has a decision it would lose.

1. **The patient is the customer.**
   *Test:* A hospital network offers seven figures for an admin dashboard over aggregated
   patient data. We decline.
2. **Uncertainty is shown, not smoothed.**
   *Test:* The match score would look better if we treated missing labs as passing
   criteria. We show them as "unknown" and the score goes down.
3. **Consent is specific and revocable.**
   *Test:* A patient wants to share their record with their own clinician but not with the
   trial site. That must be two separate decisions, and both must be undoable. In the
   prototype this is trivially satisfied: nothing leaves the device at all, and the prep
   sheet is a file the patient chooses to download and hand over themselves.
4. **Concentration is a real risk we own.**
   *Test:* We write the attack surface into our own docs (`RISKS.md`) instead of letting a
   reviewer find it.
5. **Plain language, always.**
   *Test:* If a sentence in the app would need a clinician to decode, it gets rewritten —
   even when the precise term is technically better.

---

## Positioning statement

> For **patients managing an ongoing condition** who **have their health data split across
> paperwork, portals and devices and no way to see what it qualifies them for**, OpenHealth
> is a **consumer health app** that **reads their own records and devices — without asking
> them to name their condition — and returns scored clinical-trial matches with the
> per-criterion arithmetic shown**.
>
> Unlike **MatchMiner, Deep 6 AI, and TrialJectory — which sell matching to hospitals,
> pharma, and sites** — OpenHealth **answers to the patient, because the patient is the
> one holding the phone.**

## Success, measured

| | Metric | Why this one |
|---|--------|--------------|
| **North star** | Qualified matches a patient *acted on* (sent to a doctor or a site) | Not installs, not matches shown. The only number that means a patient's life changed |
| **Quality guardrail** | Site-confirmed screening pass rate on referrals we send | If we flood sites with bad referrals we destroy the business and waste patients' hope |
| **Trust guardrail** | Authorization revocations per 1,000 connected accounts | Patients pulling their data back out is the earliest signal we broke faith |
| **Honesty guardrail** | % of shown matches where we surfaced at least one "unknown" criterion | A matcher that is never uncertain is lying |

---

## Related docs

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — how the data actually moves
- [`MARKET.md`](MARKET.md) — who else is in this space and why they're pointed elsewhere
- [`COSTS.md`](COSTS.md) — what it costs to run, benchmarked against real vendors
- [`RISKS.md`](RISKS.md) — what we're taking on, including the consequence we can't remove
- [`ROADMAP.md`](ROADMAP.md) — the build plan to the submission deadline; Appendix A for the long-horizon version
