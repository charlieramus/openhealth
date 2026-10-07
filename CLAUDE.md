# OpenHealth

School project — computing innovation class, and a Congressional App Challenge entry
(**deadline: Oct 26, 2026, 12:00 pm ET**). A working clinical-trial eligibility checker.

## Project

A clinical-trial matcher wrapped in a health hub, published as a web artifact.

**The standard everything is held to, set 2026-10-06:** *everything has to be functional —
not just clickable, but actually real. The only accepted limitation is that there is no
backend.* If a screen looks like it does something it does not do, it gets deleted, not
polished.

| | |
|---|---|
| **Trials** | **Real** — ClinicalTrials.gov records, saved verbatim. Raw criteria text parsed at runtime |
| **Matching engine** | **Real** — every score computed from a structured profile |
| **Lab values** | **Real** — OCR'd from actual documents in-browser (Tesseract.js) |
| **Vitals** | **Real** — the operator's own Garmin data via a local sync script |
| **Data standard** | **Real** — FHIR R4 / US Core shapes with LOINC codes (format only; no server call) |
| **Patient data** | **Never real.** The operator's own fitness data is not patient data |

**What it does:** you give it your lab documents and your watch data — **you never tell it
what condition you have.** It parses trials' free-text eligibility criteria into checkable
rules, evaluates them against your values, and shows a **per-criterion audit** — pass / fail
/ unknown / near-miss, with the actual numbers. The audit is the product.

**Three tabs:**
1. **Home** — Health Score ring, biomarker bars, today's captures, top trial match
2. **Metrics** — biomarker detail, reference ranges, trends
3. **Trials** — ranked matches, each opening the per-criterion audit

**Read before changing anything:** [`docs/SIMPLIFY.md`](docs/SIMPLIFY.md) (the current plan
and what was cut), [`docs/REBUILD.md`](docs/REBUILD.md) (why the app works the way it does),
and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) §4a (the parser/evaluator contract). What
to build next: [`docs/SIMPLIFY.md`](docs/SIMPLIFY.md) §7.

**Design doc:** `~/.gstack/projects/openhealth/jason-master-design-20260928-150904.md`

## Stack

- Pure HTML/CSS/JS — single file per published artifact
- No build step, no framework. Two CDN libraries only: Tesseract.js (OCR)
- **Zero network calls at runtime.** The trial corpus and `garmin.json` are committed files
- Python, off to the side: a local sync script (`python-garminconnect`) that writes
  `garmin.json` every few days. A build-time pipeline, **not a backend** — nothing listens
  on a port
- Published via Claude Artifacts (live URL)

**Do not add an API key to this project — including one we already have.** A key can't live
in client-side JS without a proxy, which means a server, which breaks the whole
architecture. Having a key does not help: a key in a published static page is readable by
anyone who opens View Source. See [`docs/STACK.md`](docs/STACK.md) §6a.

## Skill routing

When the request matches an available skill, invoke it via the Skill tool.

Key routing rules:
- Brainstorming / narrowing idea → invoke /office-hours
- Architecture / lock in plan → invoke /plan-eng-review
- Visual polish / design audit → invoke /design-review
- QA / test the prototype → invoke /qa-only
- Code review → invoke /review
- Ship / publish → invoke /ship

## Commit & push communication rule

This is a co-shared repo. Every commit and push must include a brief plain-English message explaining:
- What changed and why
- Any context a collaborator needs to not be surprised

Put it in the commit message body (after the subject line), not just the subject. Example format:
```
feat: add bloodwork results screen

Built out Screen 2 with the four biomarker bars (Iron, Hemoglobin, SpO2, LDL).
Colors match the palette from the hand-drawn mockups. Navigation back to Screen 1
and forward to Screen 3 both working. Fake data only.
```

This applies to every commit — no silent one-liner pushes.

## Efficiency notes

- The design doc at `~/.gstack/projects/openhealth/` is discoverable by all plan-review skills automatically
- Layout reference is now `Screenshot 2026-10-06 153715.png` (the homepage design) — it supersedes the hand-drawn mockups (IMG_0631-0634.JPG) for the home screen
- Color palette: pink/magenta, purple, teal/green, blue, plus the amber/orange Health Score ring — use these for the biomarker bars
- **Never quote a match score or a Health Score as a constant.** Both are engine output and change with the profile. "87/100", "89", "79/100" and "CGX Trial #4" are all retired — `NCT06942208` and `NCT07502508` are real trials and may be named, their scores may not
- **No condition input anywhere in the app.** No search box, no condition dropdown. The app reads your data and ranks every trial it knows about. See [`docs/SIMPLIFY.md`](docs/SIMPLIFY.md) §2
- **A1c is deliberately absent** — it's the UNKNOWN test case, and the engine must not treat a missing value as a pass
- **Retired, do not reintroduce:** the synthetic patient (Jordan Reyes), the send-to-doctor flow, "Doctors Available: 9", and the `r4.smarthealthit.org` call. The doctor flow is replaced by a real downloadable **appointment prep sheet** — the app never contacts a clinician
- `garmin.json` holds the operator's real fitness data and is committed in the clear. Deliberate; noted in the README so collaborators aren't surprised
