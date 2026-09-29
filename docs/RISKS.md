# OpenHealth — Risks, Ethics & Regulatory Surface

> The required class deliverable asks for **one** unintended consequence. This is the honest
> version: the full list, including the one we can't design away.
>
> This doc exists because the strongest thing a project like this can do is find its own
> problems before a reviewer does. Nothing here is hedging — every item is a real property
> of the design in [`ARCHITECTURE.md`](ARCHITECTURE.md).
>
> **Not legal advice.** Every regulatory item below needs review by a healthcare attorney
> before OpenHealth touches one real patient record.

---

## 1 · The consequence we cannot remove

**Putting a person's complete health and financial record in one place makes that account a
concentrated, high-value target.** Today an attacker who breaches one portal gets a fifth of
a patient. Breach OpenHealth and they get the whole person: diagnoses, medications, lab
history, insurance, billing, care team, and — because trial matching implies it —
information about conditions the patient may not have told their employer or family.

Encryption, per-user keys, short-lived tokens, and audit logs reduce the *probability*. They
do not reduce the *value of the target*. **Aggregation is the product; concentration is
therefore intrinsic, not incidental.**

What we can honestly claim:

| We can | We cannot |
|--------|-----------|
| Make a breach less likely (defense in depth, minimum necessary, BAAs) | Make the target less valuable — that's what the product is |
| Limit the blast radius (per-user keys, no global decrypt path, scoped tokens) | Promise it won't happen |
| Make a breach discoverable fast (append-only access ledger, anomaly alerts) | Un-leak a leaked record |
| Give the patient a real exit (delete means delete, revocation means revocation) | Recall data a patient already shared with a site |

**This is the answer to the class question**, and the reason to state it this way: a project
that claims it solved a problem it structurally can't solve is less credible than one that
names the tradeoff and shows what it did about it.

---

## 2 · The rest of the risk register

Ranked by severity × likelihood. "Designed for" means the mitigation is already in
[`ARCHITECTURE.md`](ARCHITECTURE.md); "open" means it isn't solved yet.

| # | Risk | Severity | Mitigation | Status |
|---|------|----------|-----------|--------|
| 1 | **Breach of the aggregated record** (§1) | Existential | Per-user keys, minimum necessary to every third party, append-only access ledger, signed BAAs, third-party pen testing | Designed for; residual risk permanent |
| 2 | **False hope** — a patient reads 87/100 as "I'm in" and isn't | High | Score is framed as screening, never eligibility. Unknowns shown. Hard exclusions drop the trial. Every match carries its reasoning | Designed for; needs user testing to confirm the framing actually lands |
| 3 | **False despair** — a low score discourages a patient a doctor would have referred | High | Never show a score as a ceiling. Always offer "ask your doctor anyway." Never tell a patient they don't qualify | Designed for |
| 4 | **A missed exclusion criterion** sends a patient toward an unsafe trial | High | Hard exclusions remove trials rather than scoring them down; site screening is always the gate; we never present ourselves as the final check | Designed for |
| 5 | **Equity inversion** — the app helps the patients who need it least | High | The patients with the most portals, best insurance, and newest phone are the easiest to serve. Advocacy-partner distribution is chosen partly to counter this | **Open.** Requires deliberate measurement, not good intentions |
| 6 | **Consent theater** — patients tap through without understanding | Medium-high | Per-recipient, per-instance confirmation showing exactly what will be sent; plain-language scope; revocation in Settings | Designed for; the honest test is whether users can say what they shared |
| 7 | **Data sold after an acquisition** — a future owner monetizes the dataset | High | Cannot be solved in code. Needs binding commitments: charter provisions, a privacy policy that survives change of control | **Open.** A governance problem, and a real one |
| 8 | **Site spam** — low-quality referrals waste site staff time and patient hope | Medium | Billing on site *acceptance* aligns the incentive. Referral-quality metrics tracked per site | Designed for |
| 9 | **Model error on criteria reading** | Medium | Structured prefilter does the deterministic work; the model handles prose only. Per-criterion verdicts with evidence pointers make errors reviewable. Escalation for ambiguity | Designed for; needs a labeled eval set before any real use |
| 10 | **A stale "recruiting" badge** sends a patient to a closed trial | Medium | Hourly delta poll on status; freshness timestamp surfaced in the UI | Designed for |
| 11 | **Aggregator coverage gaps** look like missing health history | Medium | Show which sources are connected and which aren't; never imply completeness | Designed for |
| 12 | **Family and genetic implications** — trial matching reveals things about relatives | Medium | Genomic criteria are out of scope at launch, partly for this reason | Deliberately deferred |
| 13 | **Insurance or employment discrimination** from data the patient surfaced | Medium | GINA covers genetic information; broader health data is less protected. We never share with payers or employers | Partially open — a legal limitation, not ours to fix |

---

## 3 · Regulatory surface

Everything a real deployment has to clear. Written as a checklist because that's how it will
actually be worked.

### HIPAA

| Requirement | What it means for us |
|-------------|---------------------|
| **Business Associate Agreements** | Signed with *every* vendor touching PHI — aggregator, cloud host, model provider, error tracking, analytics. **A missing BAA is a violation on its own**, regardless of other controls `[sourced]` |
| **Minimum necessary** | The criteria-reasoning step gets clinical codes and values, not names or addresses. See [`ARCHITECTURE.md`](ARCHITECTURE.md) §6 |
| **Security Rule** | Encryption in transit and at rest, access controls, audit controls, risk assessment |
| **Breach Notification Rule** | 60-day notification; a written, rehearsed incident response plan |
| **Right of access** | The patient can export everything. This one we're glad to comply with — it's the mission |

*Note: an app the patient chooses and authorizes may not itself be a covered entity in every
configuration. We plan to operate as though HIPAA applies regardless — the alternative is
building on a jurisdictional technicality, which is both fragile and a bad look.*

### 21st Century Cures Act / ONC information blocking

The tailwind. Providers must make records available to patients via API and may not block
access. **This is what makes the product legal to build without hospital partnerships** —
and a dependency worth tracking, since a rule change is a business-model change.

### CMS Interoperability & Patient Access

Payers must expose claims and coverage through a patient-access API. This is the source
behind Screen 1's insurance row.

### FDA — clinical decision support

The live question. Software that provides a patient-specific recommendation a user can't
independently review can be regulated as a medical device. Our design choices are
deliberately on the safe side of that line:

- We present **criteria and evidence**, not a conclusion — the patient and their doctor can
  see and check every input to the score
- We never state that a patient **is eligible**, only that they **may qualify**
- We route to a clinician rather than replacing one

**That posture is intentional but not self-certifying.** It needs regulatory counsel before
launch, and the answer could force real product changes.

### State law

| | |
|---|---|
| **California CCPA/CPRA, Washington My Health My Data, and similar** | Consumer health privacy laws with their own consent and deletion requirements — in some cases stricter than HIPAA, and with private rights of action |
| **State-specific medical-records rules** | Vary on minors, mental health, HIV status, and substance use — categories with extra protection that a naive aggregation would flatten |

### Other

- **GINA** — genetic information in employment and insurance
- **42 CFR Part 2** — substance use disorder records, materially stricter than HIPAA
- **COPPA** — we are 18+ at launch, specifically to avoid this surface
- **SOC 2 Type II** — not a law, but a practical requirement before any site or sponsor will
  contract with us

---

## 4 · Security posture

The controls, stated as commitments rather than aspirations.

| Layer | Control |
|-------|---------|
| **Transport** | TLS 1.3 everywhere; mTLS between internal services |
| **At rest** | Per-user encryption keys. **No single key decrypts the whole database** — this is what limits blast radius |
| **Tokens** | Short-lived access tokens; refresh tokens in the device keychain behind biometric gating; never in app storage |
| **Access** | Append-only access ledger: every read of a patient's record is logged, including ours. Patients can see their own access log |
| **Third parties** | Signed BAA before any PHI flows. Minimum necessary per vendor. Regular vendor review |
| **Model provider** | Clinical profile only — codes, values, dates. No identifiers. No training on our data |
| **Deletion** | Delete means delete: PHI store, aggregator-side connection, caches, and backups on a documented schedule. The consent ledger retains the *record of consent*, not the data |
| **Testing** | Third-party penetration test before launch and annually; bug bounty once there's something worth attacking |

**What we won't claim:** that any of this makes us unbreachable. See §1.

---

## 5 · Ethical commitments that cost us money

Listed because a commitment with no price attached isn't a commitment. Each of these is a
revenue option we've declined — the fuller list is in [`COSTS.md`](COSTS.md) §5.

1. **Free to patients, permanently.** The patients most likely to benefit from a trial are
   often those who have exhausted covered options. A paywall would select against them.
2. **No data sales, including "anonymized."** Re-identification of health data is a solved
   problem for a motivated attacker. "Anonymized" is a marketing word.
3. **No payer or employer channel.** Ever. The discrimination risk is not ours to gamble
   with on a patient's behalf.
4. **No advertising.** Targeting by health condition is the worst available version of this
   product. The one adjacent option we've left open — sponsored *nutrition* on the
   iron-rich-foods recommendation — is fenced by seven conditions in
   [`COSTS.md`](COSTS.md) §5, the first three of which exist precisely to keep it from
   becoming this. It is unvalidated, not in the pilot, and dropped if the fence can't hold.
5. **Uncertainty is displayed, even when it lowers the score.** A matcher that is never
   uncertain is lying, and a number that looks better than the evidence is a false promise
   to someone who is sick.

---

## 6 · What we'd need before touching a real patient record

A hard gate, not a wish list. The prototype stays fake data until every line is checked.

- [ ] Healthcare attorney review — HIPAA posture, FDA CDS analysis, state law
- [ ] Signed BAAs with every vendor in the PHI path
- [ ] Documented HIPAA risk assessment and written policies
- [ ] Third-party penetration test, findings remediated
- [ ] Incident response plan, written and rehearsed
- [ ] A labeled eval set for criteria matching, with a measured false-negative rate on
      exclusion criteria specifically
- [ ] Clinical advisor review of the score presentation and every piece of patient-facing copy
- [ ] Consent flow tested with real users — can they state what they shared and with whom?
- [ ] Deletion and revocation verified end to end, including backups
- [ ] Equity measurement plan — who is this reaching, and who is it missing?

---

## 7 · Sources

- [HIPAA-compliant app hosting: who signs a BAA in 2026](https://hipaacomplianthosting.com/blog/hipaa-compliant-app-hosting) — BAA requirement
- [HIPAA compliance for digital health startups (Aptible)](https://www.aptible.com/hipaa/hipaa-overview)
- [What does a HIPAA-compliant cloud cost in 2026? (TechRev)](https://www.techrev.us/blog/what-does-a-hipaa-compliant-cloud-cost-in-2026/) — compliance setup scope
- [Epic on FHIR](https://fhir.epic.com/) — SMART on FHIR and OAuth 2.0 scoping model

---

## Related docs

- [`MISSION.md`](MISSION.md) — the values these commitments come from
- [`ARCHITECTURE.md`](ARCHITECTURE.md) §6 — the trust boundary diagram
- [`COSTS.md`](COSTS.md) §5 — the revenue we've refused, and what it would have paid
- [`BRIEF.md`](BRIEF.md) — the one-consequence answer for the class deliverable
