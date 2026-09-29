# assets/

Everything visual that isn't the prototype itself.

```
intake/       ← raw source material dropped in by a human. Never edited in place.
  sketches/     the original hand-drawn mockups (IMG_0631–0634)
  references/   look-and-feel references we borrowed the visual language from
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
