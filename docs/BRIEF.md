# OpenHealth — Project Brief

> The single source of truth for **what OpenHealth is** and **why**. The prototype,
> the poster, and the Congressional App Challenge video all draw their content from
> this file. If a fact about the concept changes, change it here.

---

## The problem

The US healthcare system scatters a patient's data across 5+ separate portals — one per
hospital, lab, insurer, and pharmacy. No one place shows the whole picture. Two things
break because of this:

1. **Patients can't see their own health clearly.** Labs live in one portal, bills in
   another, prescriptions in a third.
2. **Patients miss clinical trials they qualify for.** Trial-matching tools exist, but
   they're all **B2B** — sold to hospitals and pharma (MatchMiner, TrialMatchAI). The
   patient, who has the most to gain, is the last to know.

## The idea

OpenHealth aggregates a patient's health data into one consumer app, then does the thing
no consumer app does: it **matches the patient to clinical trials they qualify for** and
lets them **send their records to a doctor in one tap.**

The "whoa" moment is a patient opening the app and seeing:
**"You qualify for CGX Clinical Trial #4 — 87/100 match"** — something their doctor
never told them.

---

## The six required deliverable elements

These map directly to the class rubric (and cover the CAC video talking points).

### 1. App name + problem
**OpenHealth.** US health data is fragmented across 5+ portals, so patients can't see
their full health picture and miss clinical trials they'd qualify for.

### 2. Three-screen prototype
**Home → Labs → Trials.** (See `DESIGN.md` / `BUILD.md`, live at the URL in the README.)

### 3. Input → Processing → Output
- **Input** — The patient's bloodwork, diagnoses, insurance, and health profile. *(In a
  real deployment this is aggregated from healthcare APIs across labs, insurers, and
  providers. The prototype shows it as realistic fake data.)*
- **Processing** — OpenHealth cross-references that health data against clinical-trial
  eligibility criteria and computes a match score.
- **Output** — A personalized trial match with an eligibility score (**87/100** for CGX
  Trial #4) and one-tap send-to-doctor.

### 4. One benefit
Patients see their whole health picture in one place **and discover trials their doctor
never mentioned** — then act on them by sending records to a doctor in one tap. It shifts
agency from the healthcare system to the patient.

### 5. One unintended consequence
Putting all of a person's health *and* financial data in one place makes that account a
**high-value target for attackers** — a single bundle worth stealing. Protections can
reduce the risk but not remove it; concentration itself is the consequence.

### 6. Why it's a computing innovation
OpenHealth is the **first consumer-facing clinical-trial matcher.** Every existing tool
is B2B, sold to hospitals and pharma. By aggregating fragmented health data and running
eligibility matching on the patient's own device, OpenHealth streamlines the US
healthcare process, puts the trial match in the patient's hands, and encourages more
informed patient-doctor communication.

---

## Fake data used in the prototype

Keep these consistent across the app, the poster, and the video.

| Thing | Value |
|-------|-------|
| Patient | Jordan Reyes |
| New updates | 18, synced from 5 providers |
| Featured trial | CGX Clinical Trial #4 — Hematology, Phase II, recruiting |
| Match score | **87 / 100** |
| Iron (Ferritin) | 8 ng/mL — *too low* (normal 12–150) |
| Hemoglobin | 13.1 g/dL — *average* (normal 12–16) |
| Oxygen saturation | 97% — *steady* (normal 95–100) |
| LDL cholesterol | 95 mg/dL — *optimal* (target < 100) |
| Insurance | Full coverage · $0.00 balance |
| Doctors on care team | 9 (records auto-send to Dr. Chen) |
| Other trials | LMI (metabolic), PPF (pulmonary) — "coming soon" |

Color coding: Iron = magenta, Hemoglobin = purple, Oxygen = teal, LDL = blue. These come
straight from the marker colors in the hand-drawn mockups and are used everywhere.
