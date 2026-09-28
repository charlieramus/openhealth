# OpenHealth — Prototype Build Spec

**Task for next session:** Build and publish the three-screen interactive OpenHealth prototype as a Claude Artifact (live URL). Pure HTML/CSS/JS, single file. No frameworks, no build step.

---

## Context

School project, computing innovation class. Mobile app UI mockup with fake data. Deliverable: three-screen prototype + poster. The prototype needs a live URL + QR code for classroom demo.

Design doc: `C:\Users\jason\.gstack\projects\openhealth\jason-master-design-20260928-150904.md`

---

## Tech Spec

- **Format:** Single `.html` file published as a Claude Artifact
- **Stack:** Pure HTML + CSS + JS. No React, no Tailwind, no bundler.
- **Layout:** Mobile-first, ~390px wide (iPhone), centered on desktop
- **Style:** Dark-ish background, card-based layout, health app aesthetic

**Color palette (from hand-drawn mockups):**
- Pink/magenta `#E91E8C` — Iron (Ferritin) bar, low result
- Purple `#9C27B0` — Hemoglobin bar, average result
- Teal/green `#26A69A` — Oxygen Saturation bar, steady result
- Blue `#2196F3` — LDL Cholesterol bar, optimal
- Accent/score `#4CAF50` — health score green
- Background `#0D1117` or `#1A1A2E`
- Card bg `#1E2A3A` or similar dark card

---

## Screen 1: Home Dashboard (Input)

**Header:** "OpenHealth" logo/wordmark top center

**Notification banner:** Blue/teal card — "There are 18 new updates for you"

**New Trials section** (label: "New Trials"):
- CGX card — tappable → navigates to Screen 3
  - "CGX Clinical Trial #4"
  - Health Match score: 87/100
  - Small colored eligibility bars
- LMI card — display-only, dimmed/grayed, "Coming Soon" badge
- PPF card — display-only, dimmed/grayed, "Coming Soon" badge

**Your Bloodwork section** (label: "Your Bloodwork"):
- Iron (Ferritin) — "Below Avg" — pink/magenta short bar
- Hemoglobin — "Steady" — purple medium bar
- CTA button: "View Details →" → navigates to Screen 2

**Insurance row:** "Full Coverage ✓" — green check

**Recent Doctors:** Row of 4 circular avatar placeholders (gray circles with initials)

---

## Screen 2: Your Test Levels / Bloodwork Results (Processing)

**Header:** Back arrow (top-left) → Screen 1. Title: "Your Test Levels"

**Gauge meter:** Semicircle gauge, arrow pointing to "OK" zone

**Colored bars** (horizontal, show value vs. normal range):
| Marker | Color | Status | Fake value |
|---|---|---|---|
| Iron (Ferritin) | Pink `#E91E8C` | Too Low | 8 ng/mL (normal: 12–150) |
| Hemoglobin | Purple `#9C27B0` | Average | 13.1 g/dL (normal: 12–16) |
| Oxygen Saturation (SpO2) | Teal `#26A69A` | Steady | 97% (normal: 95–100%) |
| LDL Cholesterol | Blue `#2196F3` | Optimal | 95 mg/dL (normal: <100) |

**Recommendations panel:**
1. "Increase iron intake — consider iron-rich foods or supplements"
2. "Schedule follow-up for hemoglobin levels"
3. "Maintain current O2 levels — great work"

**CTA button:** "View Trial Matches →" → Screen 3

---

## Screen 3: CGX Clinical Trial #4 (Output)

**Header:** Back arrow (top-left) → Screen 2. Title: "CGX Clinical Trial #4"

**Health Score:** Large display — "87 / 100" with green ring/arc

**Eligibility bars:** 3–4 small colored bars showing criteria match (similar to Screen 1 CGX card, expanded)

**"Auto Send to Doctor?" section:**
- Label: "Auto Send to Doctor?"
- Button: "Send to Dr. Chen"
- On tap: show modal overlay:
  - Checkmark animation (✓ draws in)
  - Text: "Sent to Dr. Chen ✓"
  - **Behavior (R3-1 resolved):** Doctor avatars below are display-only (care team context, not selectable). Auto-targets Dr. Chen.
  - **Behavior (R3-2 resolved):** Modal auto-dismisses after 1.5s. Send button then shows "Sent ✓" (disabled, green).

**Doctor avatars:** Row of 9 circular avatar placeholders with initials. Display-only. First one labeled "Dr. Chen".

**Related Trials section:**
- LMI Clinical Trial — dimmed row
- PPF Clinical Trial — dimmed row

---

## Navigation Map

```
Screen 1 (Home)
  ├── CGX card tap → Screen 3
  └── "View Details →" button → Screen 2

Screen 2 (Bloodwork)
  ├── Back arrow → Screen 1
  └── "View Trial Matches →" → Screen 3

Screen 3 (Trial Match)
  ├── Back arrow → Screen 2
  └── "Send to Dr. Chen" → modal → stays on Screen 3
```

---

## I→P→O (for class deliverable)

- **Input:** User's bloodwork results, diagnoses, and health profile *(in a real deployment, aggregated via healthcare APIs from labs, insurers, and providers — shown in the prototype as realistic fake data)*
- **Processing:** OpenHealth cross-references the user's health data against clinical trial eligibility criteria and computes a match score
- **Output:** Personalized trial matches with an eligibility score (87/100 for CGX Clinical Trial #4) and one-tap doctor send

---

## Class Deliverable Map (all 6 required elements)

| Required | OpenHealth Answer |
|---|---|
| App name + problem | OpenHealth — US healthcare data is fragmented across 5+ portals; patients miss clinical trials they qualify for |
| Three-screen prototype | Home Dashboard → Bloodwork Results → CGX Trial Match |
| Input → Processing → Output | Health profile (concept: healthcare APIs) → cross-reference trial criteria → eligibility score 87/100 |
| One benefit | Patients discover trials their doctor never told them about and can send records in one tap |
| One unintended consequence | All health + financial data in one place = high-value attack target for hackers |
| Why it's a computing innovation | First consumer-facing clinical trial matcher — every competitor (MatchMiner, TrialMatchAI) is B2B (sold to hospitals/pharma). OpenHealth puts the match in the patient's hands. |

---

## Build Instructions for Next Session

1. Load the artifact-design skill before writing HTML
2. Build as a single HTML file with all 3 screens as `div` panels — only one visible at a time via JS `show/hide`
3. Use smooth CSS transitions between screens (slide or fade)
4. Publish as a Claude Artifact — get live URL
5. Add QR code to the poster using the published URL (can use a QR code library or api.qrserver.com)
6. Test that it loads on mobile (phone-width layout)

**Start prompt for next session:**
> "Read BUILDSPEC.md in the openhealth project folder and build the three-screen OpenHealth prototype as a published HTML artifact."
