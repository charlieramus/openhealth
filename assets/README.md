# assets/

Source material and generated output — everything that isn't the prototype or the docs.

```
intake/       ← raw source material dropped in by a human. Never edited in place.
  sketches/     the original hand-drawn mockups (IMG_0631–0634)
  references/   look-and-feel references we borrowed the visual language from
  cac/          Congressional App Challenge official rules + judging rubric (PDFs)
  trials/       the four ClinicalTrials.gov records the matching engine is built on (JSON)
processed/    ← anything we produce FROM intake: screenshots, poster art, QR codes,
                exported mockups. Safe to regenerate/delete.
```

**Rule:** intake is read-only history — it's what we were given. processed is output —
if it's lost, it can be remade. If you're not sure which a file is, ask: "could I
recreate this from the repo?" Yes → `processed/`. No → `intake/`.

## intake/references

| File | What it is | What we took from it |
|------|-----------|----------------------|
| `ref-reveal-home.webp` | A calorie-tracker home screen (green gradient, big ring, macro bars) | The layout grammar: gradient hero → oversized ring metric → three labeled mini-bars → white sheet of list rows. **Not** the content — kcal became Health Score, macros became biomarkers, food rows became trial rows. |
| `ref-stats-dashboard.webp` | A fitness dashboard + statistics screen | The pale-green hero card, 2-up stat tiles with colored icon chips, and the big-number + weekly bar-chart pattern. We point that chart at biomarker history instead of calories. |

These are inspiration, not assets — nothing from them is copied into `index.html`.

## intake/cac

The official Congressional App Challenge rulebook and judging rubric, downloaded
2026-09-29. Not visual reference — primary sources. Every rule, date, and scoring claim in
[`docs/ROADMAP.md`](../docs/ROADMAP.md) is quoted from these rather than from a summary of
them, which matters because the summaries circulating online get at least two things wrong
(the video must be **public**, not unlisted; the rubric is six sub-criteria, not three).

See [`intake/cac/README.md`](intake/cac/README.md) for the extracted facts.

## intake/trials

The four ClinicalTrials.gov records the prototype's trials are built from, as the public
API returned them on 2026-09-29. Also primary sources: every eligibility threshold the
matching engine compares against is quoted from the protocol text in these files, so a
judge can check any number on screen 3 against the registry.

The patient is still entirely invented. The trials are not.

See [`intake/trials/README.md`](intake/trials/README.md) for what the engine takes from
each record and why these four were chosen.
