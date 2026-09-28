# OpenHealth

School project — computing innovation class. Mobile app UI mockup with fake data.

## Project

Three-screen interactive prototype published as a web artifact. Fake data throughout — no real API connections.

**Three screens:**
1. Home Dashboard (Input)
2. Bloodwork / Test Results (Processing)
3. CGX Clinical Trial Match (Output)

**Design doc:** `~/.gstack/projects/openhealth/jason-master-design-20260928-150904.md`

## Stack

- Pure HTML/CSS/JS — single file per published artifact
- No build step, no framework, no external dependencies
- Published via Claude Artifacts (live URL)

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
- Fake data is already sketched in hand-drawn mockups (IMG_0631-0634.JPG in project root)
- Color palette from sketches: pink/magenta, purple, teal/green, blue — use these for the bloodwork bars
- Health score is 87/100 for CGX Trial #4
- "Doctors Available: 9" on the send screen
