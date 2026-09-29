# OpenHealth

**One app for your whole health picture — and the clinical trials you actually qualify for.**

OpenHealth is an interactive three-screen mobile-app prototype built for the
**Congressional App Challenge** (and a computing-innovation class project). It shows a
patient's fragmented US health data — labs, insurance, billing, doctors — pulled into one
place, then surfaces a clinical trial the patient qualifies for and lets them send their
records to a doctor in one tap.

Everything runs on realistic **fake data**. No real APIs, accounts, or PHI.

---

## ▶ See it live

**Prototype:** https://claude.ai/artifact/5H4KWf2bja3DKDydumaqyo

Open it on a phone for the intended experience. Tap through **Home → Labs → Trials**
using the bottom tab bar, the in-screen buttons, or the CGX trial card.

---

## The three screens

| # | Screen | Role (I→P→O) | What it shows |
|---|--------|--------------|---------------|
| 1 | **Home** | Input | Updates, new trials, bloodwork snapshot, insurance, doctors |
| 2 | **Labs** | Processing | Four color-coded biomarkers vs. normal range + a health gauge |
| 3 | **Trials** | Output | CGX Trial #4 match (87/100), why you qualify, one-tap send to doctor |

---

## Repo map

```
index.html              ← the entire prototype (one file, no build step)
docs/
  BRIEF.md              ← the idea + all 6 required deliverable answers (source of truth)
  DESIGN.md             ← design system: color, type, components, motion
  BUILDSPEC.md          ← the three-screen spec the prototype was built from
assets/
  README.md             ← what counts as intake vs. processed, and why
  intake/               ← raw source material. Never edited in place.
    sketches/           ← IMG_0631–0634: the original hand-drawn mockups
    references/         ← look-and-feel references the visual language came from
  processed/            ← generated output: screenshots, QR codes, poster art
CLAUDE.md               ← instructions for AI collaborators (Claude Code)
```

New here? Read **[docs/BRIEF.md](docs/BRIEF.md)** first — it explains the whole idea in
two minutes.

---

## Editing the prototype

`index.html` is the single source. There is no build step — open it, edit, save.

To publish your changes to the live URL, in a Claude Code session run something like:

> "Read docs/DESIGN.md, make \<change\>, and re-publish `index.html` to the existing
> artifact URL."

Publishing to the **same URL** keeps the link (and any QR code on the poster) stable.

---

## Working on this together

This is a co-shared repo. Every commit explains *what changed and why* in plain English
in the commit body — so a collaborator is never surprised by a pull. See `CLAUDE.md`.
