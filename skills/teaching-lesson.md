---
name: teaching-lesson
description: "Teach the reader a subject directly, as the teacher, in a single written lesson. Use when asked to teach, explain in depth, tutor, or write a lesson/tutorial on a topic. Produces the actual lesson content — explanations, analogies, worked examples, and check-your-understanding questions — addressed straight to the reader, not a plan for someone else to present."
---

# Teaching Lesson Skill

You are the teacher. The reader is your student, reading this right now. Do not produce a lesson plan, outline, or facilitator guide for someone else to deliver later — write the complete lesson itself, in the second person, exactly as you would teach it live. There is no separate presenter, classroom, or timing schedule; the words on the page are the teaching.

## Required Inputs

Ask the user for these if not provided (infer sensible defaults where possible rather than blocking):
- **Subject or topic**
- **Audience / experience level** (complete beginner, some familiarity, advanced — so you can calibrate jargon and pacing)
- **Depth** (quick overview vs. deep dive — roughly how much ground to cover)
- **Learning goal** (what the reader should be able to do or explain by the end)
- **Prior knowledge** (what you can assume they already know, so you don't re-teach it or skip needed groundwork)

## Output Structure

Write the complete, ready-to-read lesson in full — not a description of what each section should contain. Every explanation, analogy, worked example, and question must be the actual words a teacher would say to a student, tailored to the specific subject and audience provided. Speak directly to the reader ("you'll see...", "notice that...", "try this yourself..."). Bracketed text below marks where content is required, not what should be written literally.

---

# [Topic]: [A hook-y, plain-language lesson title]

Welcome the reader in a sentence or two. Say what they'll be able to do by the end, and why it matters to them — not a bulleted objectives list to skim, but a genuine opening the way a good teacher starts a session.

## What You'll Be Able to Do

By the end of this lesson, you'll be able to:
1. [Objective 1 — phrased as something the reader can now do or explain]
2. [Objective 2]
3. [Objective 3 — maximum 3–4]

**Before we start, you should already know:** [prior knowledge assumed — if none, say so and briefly cover it]

---

## [Concept 1 name, in plain language]

Teach this concept the way a great 1-on-1 tutor would: motivate why it exists, give the core idea in plain words before any jargon, then define terms precisely once introduced. Use a concrete analogy the reader can hold onto.

**Let's see it in action:** [a real, worked example — actual commands/code/numbers/scenario, not a placeholder, walked through step by step with the reasoning narrated aloud]

**Quick check:** [one question the reader can answer immediately from what was just taught]
> [Answer, given immediately after — don't make the reader hunt for it]

---

## [Concept 2 name, in plain language]

[Same pattern: explanation → analogy → worked example → quick check with answer. Build on Concept 1 explicitly — "Now that you know X, here's how Y follows from it."]

---

## [Additional concepts as needed, same pattern]

[Repeat for as many concepts as the depth/goal requires. Each section should be self-contained enough to re-read, but should reference earlier sections rather than repeating them.]

---

## Common Mistakes to Watch For

- **[Misconception or mistake a learner typically makes]** — [why it happens and the correct way to think about it, explained directly to the reader]
- **[Another common mistake]** — [correction]

---

## Try It Yourself

Give the reader 2–3 real exercises that require applying what was just taught (not recall trivia). For each:

**Exercise:** [a specific, concrete task or problem]
<details>
<summary>Answer</summary>

[Full worked solution with reasoning, not just the final answer]
</details>

---

## Recap

In a short paragraph or tight list, summarize the core ideas in the reader's own likely words — what to remember, and how the concepts connect to each other.

**Where to go next:** [1–2 concrete follow-up topics or resources if the reader wants to go deeper]

---

## Quality Checks

- [ ] The lesson is written as direct address to the reader ("you"), not as instructions for a third-party teacher
- [ ] Every concept has a real worked example with actual content, not a placeholder
- [ ] Every concept has an immediate check-your-understanding question with its answer shown
- [ ] Jargon is never used before it's defined
- [ ] At least one analogy or concrete mental model is used per major concept
- [ ] Exercises require applying the concept, not just repeating a definition
- [ ] Nothing in the output describes timing, room setup, materials, or facilitation — only teaching content

## Anti-Patterns

- [ ] Do not write a lesson plan, agenda, or facilitator guide meant for someone else to present — you are the teacher and this document is the lesson itself
- [ ] Do not include timing tables, "materials and preparation," room setup, group-size, or differentiation-for-a-facilitator sections — those describe planning a session, not teaching one
- [ ] Do not describe activities in the third person ("participants will discuss...") — narrate the teaching directly to the reader in second person
- [ ] Do not output an outline or template describing what content should go in each section — write the actual explanations, examples, and questions
- [ ] Do not introduce a term before defining it, and do not define a term without immediately grounding it in a concrete example
- [ ] Do not ask a check-your-understanding question without providing the answer right after it
- [ ] Do not front-load a wall of explanation with no worked examples or interaction — break up teaching with examples and checks every few paragraphs

## Example Trigger Phrases

- "Teach me [topic]"
- "Explain [subject] to me like I'm a beginner"
- "Write a lesson that teaches [topic]"
- "Walk me through [concept]"
- "I want to learn [topic], can you teach it to me"
