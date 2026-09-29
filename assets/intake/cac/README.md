# intake/cac — Congressional App Challenge primary sources

Official 2026 competition documents, downloaded **2026-09-29** from
`congressionalappchallenge.us`. These are the authority behind every rule, date, and
scoring claim in [`docs/ROADMAP.md`](../../../docs/ROADMAP.md).

**Intake rule applies: do not edit these.** They are what we were given. If the CAC
republishes a document, download the new one alongside the old and date it — don't
overwrite.

| File | What it is | Downloaded from |
|------|-----------|-----------------|
| `2026-CAC-Rules.pdf` | The complete official 2026 rulebook — eligibility, registration, app parameters, AI usage, submission requirements, deadline, judging, IP terms | [congressionalappchallenge.us/wp-content/uploads/2026/05/2026-CAC-Rules.pdf](https://www.congressionalappchallenge.us/wp-content/uploads/2026/05/2026-CAC-Rules.pdf) |
| `CAC-Judging-Rubric.pdf` | The official judging rubric guide — the 6 sub-criteria and the 1–5 scale for each, /30 total | [congressionalappchallenge.us/wp-content/uploads/2022/09/CAC-Judging-Rubric.pdf](https://www.congressionalappchallenge.us/wp-content/uploads/2022/09/CAC-Judging-Rubric.pdf) |

Live pages (not archived — they change):
[Rules](https://www.congressionalappchallenge.us/students/rules/) ·
[Student registration](https://www.congressionalappchallenge.us/students/student-registration/) ·
[Find your Member](https://www.congressionalappchallenge.us/participating-members/)

---

## The facts that drive the roadmap

Everything below is quoted or read directly from the two PDFs above.

### Deadline — rules §5

> **12:00 pm EDT, Monday, October 26th, 2026.**

Noon, not midnight. And §4: *"After the Submission Period has ended, the Submission cannot
be modified in any way."*

### The rubric is six sub-criteria, not three — rubric guide

| Category | Sub-criteria | Points |
|---|---|---|
| **Concept** | Ideology · Impact · Structure | /15 |
| **Technology** | Function · Code · UI | /15 |
| | | **/30** |

Two of the six are scored on the **video**, not the app:

- **Structure** — 1 pt: *"Video does not follow time limit and/or is difficult to view"* →
  5 pts: *"Video is innovative and engaging"*
- **Code** — 1 pt: *"**Video does not explain code**"* → 5 pts: *"Explanation of code
  indicates immense understanding"*

**Function** is the one that rewards a real algorithm — 2 pts is *"App contains snippets of
code/action"*, 4 is *"App is fully functional"*, 5 is *"App is functional with **complex
features**"*.

### Video requirements — rules §4

Max 3 min, **1–3 minutes** target. Must include: participant name(s), app name, purpose in
one clear sentence, target audience, **tools and coding languages used**, and a showcase of
functionality. Upload to YouTube or Vimeo — *"The video must be set to 'public'."*

The rules call it *"the most critical component"* of the application.

### The six written questions — rules §4

Published in advance, so they can be drafted in advance:

1. What is the title of your app?
2. Explain the app's purpose.
3. What inspired you to create this app?
4. What technical/coding difficulty did you face in programming your app, and how did you address this technical challenge?
5. What did you learn while participating in the CAC? What was your biggest takeaway?
6. What would you change about your app if you were to create a 2.0 version?

### Originality and AI — rules §3

> **ORIGINALITY:** "The app must be original and solely created by the contestant. All coding
> and technical development must be done by the student or student team. While participants
> may use open-source libraries, frameworks, and external tools, they must clearly document
> any such usage and ensure their project reflects significant personal effort and technical
> understanding."

> **AI USAGE:** "The use of AI tools in app development for the Congressional App Challenge
> is permitted, provided that all AI usage is fully disclosed in the submission materials. AI
> may only be used to support specific aspects of the project and must not constitute the
> entirety of the technical development. Participants are expected to demonstrate significant
> individual contributions and technical understanding of their app."

### Judges can request the source — rules §7.3

> "The Judges have the right to request access to the App and source code in person or via
> any reasonable manner to verify that the App functions and operates as stated in the
> Submission Form. **Failure by a Contestant to honor such a request will result in the
> Submission's immediate disqualification.**"

### Eligibility — rules §1

- Enrolled in middle or high school **on October 26, 2026**
- Compete in the district where you **live or attend school** — one district, one app, one entry per person per year
- Teams up to **4**; at least half must live or attend school in the same district
- App must have been created **after October 30, 2025**

### Platform — rules §3

> "The app can be developed for any platform, including but not limited to **web apps**,
> desktop/PC apps, mobile apps…"

Web apps are explicitly eligible, and any programming language is permitted. This is the
line that settles the "shouldn't it be native / shouldn't it be React?" question in
[`STACK.md`](../../../docs/STACK.md) — it isn't scored.

---

## Why these are in `intake/` and not `docs/`

Per [`assets/README.md`](../../README.md): *"could I recreate this from the repo?"* No —
these are third-party documents we were given, and the CAC could change or remove them from
their site at any point. That makes them intake. `docs/ROADMAP.md` is what we *produced*
from them.
