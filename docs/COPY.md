# OpenHealth — Copy

> **Status: rules, locked 2026-10-16.** Companion to [`DESIGN.md`](DESIGN.md). `DESIGN.md`
> decides how a thing looks; this file decides how many words it gets and what shape they
> take. Where the two touch — sentence case, mono-for-numbers — this file defers to
> `DESIGN.md` §7.3.

## 1 · Why this file exists

The lead card in `mockups/thermal.html` shipped this sentence:

> *4 ng/mL* — "of ferritin is the whole distance between you and **NCT06942208**. Every
> other criterion it lists, you already meet."

**Rejected 2026-10-16.** It is two sentences, 18 words, and it is written in an essay
register — "the whole distance between you and" is a figure of speech, not a readout. A
person opening the Trials screen has to parse a metaphor before they learn the fact. That
is backwards, and the fix is not a smaller font. It is fewer words.

The rest of this file is the standard that sentence failed, taken from how Apple writes
interface text.

---

## 2 · Notes from Apple

Two sources, both Apple's own: the WWDC22 session **"Writing for interfaces"** (session
10037), and the **Human Interface Guidelines** page on alerts. Everything in §2 is theirs;
§3 is what it becomes here.

### 2.1 · PACE — the frame the session hangs everything on

| | What it asks | The useful version |
|---|---|---|
| **P**urpose | What is the single most important thing a person needs to know on this screen? | Decide that first, write it, then delete everything that is not it |
| **A**nticipation | Text is one side of a conversation — what comes next? | Establish a voice once, vary only the tone per situation |
| **C**ontext | What else is the person doing while reading this? | Walking, driving, in a waiting room. Less text, bigger target |
| **E**mpathy | Plain language, no idioms, localizes and reads aloud to VoiceOver | Idioms are the first thing to break in translation and the first thing to confuse a reader |

### 2.2 · The six moves that actually make the text short

These are the mechanics behind the four letters — the ones that cut word count, drawn from
the session's own before/after examples.

1. **The picture already said it, so the words don't.** Their overheating screen is a
   thermometer, the headline "Temperature", and one sentence: the device needs to cool
   down. The draft had said *hot* three times — once in the image, once in the title, once
   in the body. **Never write the caption the graphic already is.**
2. **Specificity lives in the button, not in a paragraph.** Draft alert: title "Confirm
   Cancellation", body explaining "this plan", buttons "Cancel" and "Confirm" — which is
   ambiguous in the worst possible place. Theirs: title **"Cancel Platinum
   Subscription?"**, buttons **"Cancel Subscription"** and **"Keep Subscription"**, body
   one line of consequence: *You'll continue to have access until June 21, 2022.* Moving
   the nouns into the buttons deleted the paragraph that explained the buttons.
3. **A state is a noun phrase, not a sentence.** Podcasts' empty state is **"No Saved
   Episodes"** plus one line of how episodes get there. The draft — *"Nothing strike your
   fancy? Please come back if you do find something you want to eat."* — is an idiom, a
   plea, and no information.
4. **No performed feeling.** The session names *oops*, *uh-oh*, *sorry* and *please* as
   words to use sparingly: at best filler, at worst patronising. Exclamation marks are
   rationed to the one genuinely celebratory moment (a personal record), never spent on an
   error.
5. **Explain nothing twice.** HIG, on alerts: *if your alert text and button titles are
   clear, you don't need to explain what the buttons do.* Same page: a title must be
   complete and specific **without being verbose**, and "Error" is not a title. HIG also
   warns off **"you" and "your"** in alert titles — they can read as accusing.
6. **Read it out loud.** The session's closing tip, and the cheapest test there is. The
   rejected ferritin sentence does not survive being said to another person.

### 2.3 · The trap — Apple has two voices, and we copied the wrong one

Apple's *marketing* voice is lyrical, em-dashed and fond of distance metaphors. Apple's
*interface* voice is flat, concrete and short. "The whole distance between you and
NCT06942208" is written in the first voice and placed in the second one's slot. **In-app,
OpenHealth only ever has the interface voice.** Save the other one for the pitch deck and
`MISSION.md`.

---

## 3 · The rules

### 3.1 · Budgets, by slot

Hard ceilings. Over budget is not a style note, it is a bug.

| Slot | Budget | Shape |
|---|---|---|
| Screen title | 1–3 words | Noun phrase. "Closest trial", not "Your closest trial match" |
| Lead-card caption | **≤ 12 words, 1 sentence** | What the number is, and whose criterion it misses |
| Audit row criterion | ≤ 7 words | The trial's rule in plain terms — "Ferritin at or above 12 ng/mL" |
| Verdict | 1–2 words | Met · Near miss · Not met · Not read |
| Margin tag | ≤ 4 words | "4 ng/mL short" |
| Section note | ≤ 20 words, 1 sentence | Only if the section is not self-evident. Usually it is |
| Instruction (camera, upload) | ≤ 2 sentences, ≤ 20 words total | Imperative. One action per sentence |
| Empty / not-read state | Noun phrase + ≤ 12 words | "No ferritin on file" + how it would get there |
| Citation | fragment, no verb | "NCT06942208, inclusion 2, verbatim" |

### 3.2 · The eight rules

- **C1 · One string, one question.** If a string answers two, it is two strings, or the
  second one gets deleted. The ferritin caption answered *how far am I* **and** *what about
  everything else* — the second belongs to the audit rows underneath it.
- **C2 · Never narrate the graphic.** The tolerance scale already draws the gap, the pin
  and both thresholds. Words that restate it are deleted, per §2.2(1). This is the rule
  that file breaks most often.
- **C3 · The number carries the meaning; prose carries only what a number can't.** The
  mechanical version of this already exists — `DESIGN.md` §7.3: if it is a quantity it is
  mono, and if it is not a quantity it is not mono. A caption that re-speaks its own big
  number ("4 ng/mL of ferritin…" under a 4 ng/mL display) is paying twice.
- **C4 · No figures of speech.** No *the whole distance between you and*, no *standing
  between*, no *just shy of*, no *unlocks*, no *journey*. A margin is a number of units.
- **C5 · Nouns for states, verbs for buttons.** "Not read", not "We couldn't read it".
  "Add document", not "Documents". Never a bare "OK" where a verb would say which thing
  happens.
- **C6 · No filler and no apology.** No *oops*, *sorry*, *please*, *just*, *simply*, and no
  exclamation marks anywhere in the app. Nothing in a health readout is exciting enough.
- **C7 · Sentence case, always** — inherited from `DESIGN.md` §7.3, which also deletes
  all-caps eyebrows outright.
- **C8 · Numbers in copy are engine output, never typed.** Per `CLAUDE.md`: no score, no
  count and no margin may be written into a string as a constant. If a caption wants "12
  criteria met", the 12 is interpolated or the caption does not say it.

### 3.3 · What this does **not** apply to

The `.anno` and `.note` blocks in `mockups/thermal.html` are **a spec document that happens
to be rendered in a browser** — they argue for design decisions to whoever reads the
mockup, and they are allowed to be long. Product copy is everything inside a `.frame`.
Do not "fix" the annotations against §3.1, and do not let their register leak into a frame.
The ferritin caption is exactly what that leak looks like.

---

## 4 · Before → after

Real strings currently in the build, rewritten against §3.

| Where | Now | Rewrite |
|---|---|---|
| `thermal.html` lead card | "of ferritin is the whole distance between you and **NCT06942208**. Every other criterion it lists, you already meet." (18 words) | **"Ferritin, below the minimum for NCT06942208."** (6). Applied 2026-10-16; four drafts it beat are rendered in the mockup's *The description* section |
| `index.html` camera hint | "Point the camera at the printed result. Fill the frame and hold it square — the straighter the lines, the more of them get read." (25) | **"Point at the printed result. Hold the page square and fill the frame."** (13) |
| `index.html` upload hint | "A scan, a screenshot, or a photo already on the device. A PDF has to be exported as an image first — reading one here would mean a second library this app deliberately does not carry." (34) | **"Images only — scan, screenshot or photo. Export a PDF as an image first."** (13). The reason we carry no PDF library is a fact for `STACK.md`, not for the upload sheet |
| `index.html` audit header | "Every criterion this trial publishes is below, as written." (9) | **"Every criterion, as the trial wrote it."** (7) |
| `thermal.html` not-read tick | "no value in your documents" | **"Not in your documents"** — and sentence case, per C7 |
| `index.html` iron note | "Iron per typical serving. Pair with vitamin C to absorb more." (11) | Passes. Two facts, two short sentences, no metaphor |

The lead-card rewrite is the one that matters: the display already says **4 ng/mL**, the
scale underneath already draws the gap, and the audit rows underneath that already list
every other criterion with its verdict. Three of the caption's four jobs were already done
by something else on the same card.

**And the fourth job was being done wrong.** "Every other criterion it lists, you already
meet" is false for `NCT06942208` as the same sheet renders it — A1c is **not read** and LDL
is **188** against a limit of 100. A sentence long enough to summarise is long enough to
lie, which is the practical argument for C8: a claim about *how many* criteria is engine
output or it does not appear.

---

## 5 · The pass, before any string ships

Six questions. Any "no" is a rewrite, not a discussion.

1. What one thing does this screen need to say? Does this string say it?
2. Is any of it already on screen as a number, a shape or a verdict?
3. Is it inside budget for its slot (§3.1)?
4. Any metaphor, filler word, apology or exclamation mark?
5. Is every number in it computed?
6. Said out loud to a person, does it sound like a readout or like an essay?

---

## 6 · Sources

- Apple, **"Writing for interfaces"**, WWDC22 session 10037 —
  <https://developer.apple.com/videos/play/wwdc2022-10037> (PACE; the Temperature,
  subscription-cancellation, error-alert and empty-state examples; read-aloud)
- Apple, **Human Interface Guidelines — Alerts** —
  <https://developer.apple.com/design/human-interface-guidelines/alerts> (short specific
  titles, no button explanations, avoid "you"/"your", avoid a bare "OK")
- Apple, **Human Interface Guidelines — Writing** —
  <https://developer.apple.com/design/human-interface-guidelines/writing>
