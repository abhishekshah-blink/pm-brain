---
title: "Problem Framing — MITRE Canvas + Problem Statement Framework"
category: domain
tags: [problem-framing, mitre, discovery, frameworks, problem-statement]
created: 2026-03-30
updated: 2026-03-30
---

# Problem Framing

**Sources:** MITRE Innovation Toolkit (Problem Framing Canvas v3); deanpeters/Product-Manager-Skills
**When to use:** Before writing a PRD, before building an OST, when a stakeholder brings a "solution." Any time you're not 100% sure you're solving the right problem.

> "A well-stated problem is half solved." — Charles Kettering

---

## Part 1: MITRE Problem Framing Canvas

Three-phase process. Fill in order. Don't skip Phase 1 even when it feels obvious.

---

### Phase 1: Look Inward

**Question 1: What is the problem (as you currently understand it)?**
Don't overthink this — write the symptoms you observe today.
- What are users complaining about?
- What do you see in the data?
- What's the workaround people are using right now?

**Question 2: Why hasn't it been solved yet?**
Pick all that apply:
- [ ] It's new — didn't exist before
- [ ] It's hard — technically or organizationally complex
- [ ] It was low priority — other things came first
- [ ] Lack of resources — no one was assigned
- [ ] Lack of authority — the right person couldn't act
- [ ] Systemic inequity — certain users were deprioritized

**Question 3: How might we be part of the problem?**
Biases to check:
- **Confirmation bias** — Are we finding evidence for a solution we already prefer?
- **Internal/organizational bias** — Are we solving for our own convenience instead of the user's?
- **Survivorship bias** — Are we only hearing from power users who found a workaround?
- **Premature convergence** — Did we jump to a solution before mapping the space?

---

### Phase 2: Look Outward

**Question 4: Who experiences this problem? When? Where? What are the consequences?**
- Name the specific user segment (not "users" — ops agent / pharmacy manager / etc.)
- Describe the trigger situation (start of shift / during peak volume / at EOD)
- Name the specific consequence when the problem occurs (task missed / reassignment needed / patient delay)

**Question 5: Who else has this problem? Who doesn't?**
- Who else in Blinkhealth or adjacent teams experiences something similar?
- Who does NOT experience it — and what's different about their situation?

**Question 6: Who has been left out? Who benefits from the problem existing?**
- Which user segments have we NOT heard from?
- Are there stakeholders who benefit from the status quo continuing?

---

### Phase 3: Reframe

**Question 7: Restate the problem**

Template:
> "[Persona] struggles to [functional job] because [root cause], which results in [consequence], affecting [secondary impact]. This is often overlooked because [bias or assumption].

Example:
> "Ops agents struggle to track unassigned tasks during peak volume because the task list doesn't refresh in real time, resulting in missed assignments and pharmacist idle time. This is often overlooked because managers see the problem resolved at EOD, not during the shift."

**Question 8: "How Might We" question**

Template: `How might we [action] as we aim to [objective]?`

Example: `"How might we give ops agents real-time confidence about queue status as we aim to reduce missed task assignments?"`

The HMW question is the input to your OST. It should be:
- Open enough to allow multiple solutions
- Narrow enough to be actionable
- Framed around the user outcome, not the solution

---

## Part 2: Problem Statement Framework

Use after MITRE canvas to write a shareable, stakeholder-ready problem statement.

### Narrative Template

```
I am:           [persona — 3-4 specific behavioral characteristics]
Trying to:      [desired outcome — not a task, an outcome]
But:            [real barriers preventing success]
Because:        [root cause — ask "why" until you hit structure, not symptoms]
Which makes me feel: [emotional impact — from research, not assumption]
```

### Final Statement Formula

`[Persona] needs a way to [desired outcome] because [root cause], which currently [emotional/practical impact].`

**Example:**
> "Ops agents need a way to monitor unassigned task volume in real time because the task list only updates on page reload, which currently causes end-of-shift scrambles and missed assignments they can't always recover from."

---

### Quality Checks

| Section | Check |
|---|---|
| "I am" | Specific enough to picture — not "a user" |
| "Trying to" | Outcome, not a task ("finish shift confident nothing's missed" not "click the assign button") |
| "But" | Real barrier, not an inconvenience |
| "Because" | Root cause, not a symptom (keep asking "why?") |
| "Makes me feel" | Based on actual research — frustration, anxiety, embarrassment |
| Final statement | One sentence. No feature names. No solution implied. |

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Solution smuggling ("the problem is we don't have X") | Reframe as user outcome, remove the solution from the statement |
| Business problem disguised as user problem | Separate "we need more throughput" from "users need to feel less overwhelmed" |
| Generic personas | Name the specific role and context |
| Symptom instead of root cause | Ask "why" 3-5 times |
| Skipping Phase 1 (Look Inward) | Bias check prevents building the wrong thing confidently |
| HMW that's too narrow | "How might we build a refresh button" is not a HMW — it's a solution |

---

## When to Stop Framing

Problem framing is a gate, not a destination. Stop when:
1. You can write the problem statement without mentioning a solution
2. You have a clear HMW question
3. You've identified the primary user segment and their root-cause barrier

Then move to OST (`domain/opportunity-solution-tree.md`) to generate solutions.

---

## Related Frameworks

- `domain/opportunity-solution-tree.md` — Use the HMW output as the desired outcome input
- `domain/jobs-to-be-done.md` — JTBD gives richer Phase 2 "who experiences this" content
- `domain/customer-discovery-frameworks.md` — CJM helps map Phase 2 touchpoints and consequences
