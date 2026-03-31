---
title: "User Story Best Practices — Anatomy, INVEST, Splitting, Epic Hypothesis"
category: domain
tags: [user-stories, invest, splitting, epic-hypothesis, backlog, lawrence, patton]
created: 2026-03-30
updated: 2026-03-30
---

# User Story Best Practices

**Sources:** Mike Cohn (User Story format); Bill Wake (INVEST); Richard Lawrence / Humanizing Work (9 splitting patterns); Jeff Patton (Story Mapping); Tim Herbig / Jeff Gothelf (Epic Hypothesis)
**When to use:** Writing or reviewing any Jira story, splitting an epic, validating a story before sprint.

---

## Part 1: Story Anatomy

### Standard Format
```
As a [specific persona],
I want to [specific action],
So that [meaningful outcome / job done].
```

**Rules:**
- Persona must be a real WFM role (ops agent, pharmacy manager, pharmacist, admin) — not "user"
- Action must be observable behavior — not "I can see a screen"
- Outcome must connect to a job or business value — not "so that I can click less"

**Alternative format** (when the "As a" feels forced):
`[Feature area]: [concise description of behavior]`

Use this for technical enablers and infrastructure — but flag it, since it means the story has no direct user value statement.

---

## Part 2: INVEST Criteria

Every story should pass all 6 before entering a sprint. Run this check before finalizing.

| Criterion | What it means | Failure example | Fix |
|---|---|---|---|
| **I**ndependent | Can be built and delivered without depending on another unfinished story | "This story requires Story B to be done first" | Reorder, split, or absorb the dependency |
| **N**egotiable | The solution is not locked in — only the outcome is | "Must use the existing modal component" in AC | Move to Tech Notes, keep AC outcome-focused |
| **V**aluable | Delivers value to a user or the business by itself | Only adds a DB migration with no UI or behavior | Either find the user value or make it a sub-task |
| **E**stimable | Engineering can estimate it | "TBD — depends on API response" | Add a spike story first to answer the unknown |
| **S**mall | Can be completed in one sprint (≤ 5 days of work) | 13-point estimate | Split using Lawrence's patterns below |
| **T**estable | Has clear, observable acceptance criteria | "The experience feels smooth" | Rewrite as Given/When/Then |

If a story fails **Valuable**, don't split it — reframe it.
If a story fails **Small**, split it using the patterns below.

---

## Part 3: Acceptance Criteria Format (Given/When/Then)

```
Given [initial context / user state],
When [user action or system event],
Then [expected system response / observable outcome].
```

**Quality checks:**
- Each AC tests one behavior (not "and then also")
- ACs cover happy path + at least one edge case
- No implementation details in AC ("the system sends a POST request" is not an AC)
- A QA engineer can write a test case from each AC without asking questions

---

## Part 4: Epic Hypothesis

Use before committing resources to an epic. Forces assumptions into the open.

```
Epic Hypothesis:

If we [specific action / solution for the epic]
For [target persona]
Then we will [desirable outcome — measurable]

Tiny Acts of Discovery:
We will test our assumption by:
- [Experiment 1 — prototype / concierge / A/B test]
- [Experiment 2]

Validation Measures:
We know our hypothesis is valid if within [2-4 weeks]
we observe:
- [Quantitative signal — e.g., "task reassignment rate drops by ≥15%"]
- [Qualitative signal — e.g., "5/5 ops agents in usability test complete queue review without errors"]
```

**Rules:**
- "If we" = specific behavior change, not a vague improvement
- "Then we will" = measurable outcome, not feature presence ("it exists" is not a hypothesis)
- Experiments must be smaller than building the full epic
- Timeframe: 2–4 weeks; 6-month hypotheses aren't hypotheses

---

## Part 5: Lawrence's 9 Epic Splitting Patterns

When a story estimates ≥ 8 points, split before planning. Apply patterns in order — don't skip to Pattern 9 (spike) unless the first 8 genuinely don't apply.

**Pre-split check (INVEST minus Small):**
Before splitting, confirm the epic is Independent, Negotiable, and Valuable. If it's not Valuable — don't split it, reframe it.

---

### Pattern 1: Workflow Steps (Most Powerful)
Split along steps of the user's workflow. Each story delivers a thin end-to-end slice.

**Critical:** This is NOT step-by-step. Each story should support the complete workflow at a reduced capability level.

Example: "Manage task assignments" →
- Story 1: Assign a single task manually (complete workflow, minimal capability)
- Story 2: Assign multiple tasks in one action
- Story 3: Reassign from a different agent's queue

---

### Pattern 2: Operations (CRUD)
"Manage" signals Create, Read, Update, Delete. Split by operation.

Example: "Manage shift templates" →
- Story 1: View shift templates
- Story 2: Create a new shift template
- Story 3: Edit an existing template
- Story 4: Archive / deactivate a template

Deliver read before write. Deliver the most-used operation first.

---

### Pattern 3: Business Rule Variations
Different business rules = different stories.

Example: "Assign tasks based on pharmacist availability" →
- Story 1: Assign to available pharmacists
- Story 2: Handle assignment when no pharmacist is available (queue + alert)
- Story 3: Handle high-priority task assignment override

---

### Pattern 4: Data Variations
Different data types handled in separate stories. Deliver just-in-time.

Example: "Bulk upload task assignments" →
- Story 1: Upload via CSV
- Story 2: Upload via API integration (delivered when needed)

---

### Pattern 5: Data Entry Methods
Start with simple UI. Add convenience later.

Example: "Create a new task" →
- Story 1: Create via form with required fields
- Story 2: Duplicate an existing task
- Story 3: Create from a template

---

### Pattern 6: Major Effort (One + Remaining)
Build core infrastructure first; add remaining variations as follow-on stories.

Example: "Add audit logging for task changes" →
- Story 1: Log assignment events (most important)
- Story 2: Log status change events
- Story 3: Log deletion events

---

### Pattern 7: Simple / Complex
Build the simple version first; add complexity later.

Example: "Task assignment recommendation" →
- Story 1: Recommend based on workload (simple heuristic)
- Story 2: Recommend based on skill match (complex matching)

---

### Pattern 8: Defer Performance
Make it work, then make it fast.

Example: "Load task list for pharmacy" →
- Story 1: Load task list (no performance constraint)
- Story 2: Optimize to load in < 2s with 1000+ tasks

---

### Pattern 9: Break Out a Spike (Last Resort)
When there's genuine technical uncertainty that blocks estimation.

- Time-box the spike (1–3 days max)
- Spike must have a clear question and deliverable answer
- After the spike, restart at Pattern 1 with the original epic

---

## Part 6: User Story Mapping

**Source:** Jeff Patton, *User Story Mapping* (2014)

A story map organizes backlog by user journey (horizontal) and release priority (vertical):

```
User Activity 1    | User Activity 2    | User Activity 3
─────────────────────────────────────────────────────────
Story A (MVP)      | Story C (MVP)      | Story E (MVP)
Story B (v2)       | Story D (v2)       | Story F (v2)
                   | Story G (v3)       |
```

Use when:
- Planning a new feature with multiple workflows
- Deciding what to cut for MVP
- Communicating scope to engineering without a Gantt chart

---

## Common Pitfalls Summary

| Pitfall | Pattern |
|---|---|
| Stories that are really tasks | No "so that" value → reframe |
| Horizontal slicing (front end separate from back end) | Almost always creates non-valuable stories |
| Stories that depend on each other | Violates Independent — restructure |
| Estimates that never get smaller after splitting | You're splitting wrong (probably horizontal) |
| ACs that test implementation, not behavior | Rewrite as Given/When/Then |
| Skipping epic hypothesis | Building the wrong thing with perfect stories |

---

## Related Frameworks

- `domain/opportunity-solution-tree.md` — OST identifies solutions; stories implement validated solutions
- `domain/jobs-to-be-done.md` — JTBD informs the "so that" clause
- `domain/problem-framing.md` — Good problem framing makes acceptance criteria easier to write
