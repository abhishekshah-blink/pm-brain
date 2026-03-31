---
title: "Jobs to Be Done (JTBD)"
category: domain
tags: [jtbd, discovery, frameworks, christensen, user-needs, jobs]
created: 2026-03-30
updated: 2026-03-30
---

# Jobs to Be Done (JTBD)

**Source:** Clayton Christensen, *Competing Against Luck* (2016); Tony Ulwick, *Outcome-Driven Innovation*; Osterwalder, *Value Proposition Canvas*
**When to use:** When converting feature requests into real user needs. Before writing acceptance criteria. When repositioning or discovering why users churn.

---

## Core Idea

Users don't buy products or use features — they "hire" them to get a job done. Understanding the job reveals what to build, how to message it, and why alternatives fail.

> "People don't want a quarter-inch drill — they want a quarter-inch hole."

Applied to WFM: Ops agents don't want a "batch assignment screen" — they want to get through their task queue without anxiety that something got missed.

---

## Three Types of Jobs

### 1. Functional Jobs
Tasks the user is trying to perform. Verb-driven, observable, solution-agnostic.

**Formula:** `[verb] + [object] + [context/constraint]`

Examples:
- "Assign unassigned pharmacy tasks before the end of shift"
- "Confirm task completion without leaving the current screen"
- "Identify which tasks are blocked and why"

**Quality check:** Can you observe someone doing this job? If not, it's probably too abstract.

---

### 2. Social Jobs
How the user wants to be perceived by others while doing the functional job.

Examples:
- "Look organized and on top of my queue in front of my manager"
- "Be seen as the person who catches things before they fall through the cracks"
- "Not be the reason a patient prescription is delayed"

**Why it matters:** Social jobs explain why aesthetics, confirmation messages, and visible status indicators matter more than their functional value alone.

---

### 3. Emotional Jobs
How the user wants to feel (or avoid feeling) while doing the functional job.

Examples:
- "Feel confident that nothing was missed before end of shift"
- "Avoid the anxiety of not knowing queue status in real time"
- "Feel in control during high-volume periods"

**Why it matters:** Emotional jobs explain onboarding friction, why "simple" features generate strong opinions, and what drives word-of-mouth.

---

## Pains (What Blocks the Job)

| Type | Question to ask | WFM Example |
|---|---|---|
| Challenges | What makes the job hard to do? | "The task list doesn't refresh automatically" |
| Costliness | What takes too long or costs too much? | "Finding unassigned tasks requires multiple clicks" |
| Common Mistakes | What errors do users frequently make? | "Reassigning a task that was already claimed" |
| Unresolved Problems | What can't they do at all? | "No way to see task history without leaving the view" |

---

## Gains (What Success Looks Like)

| Type | Question to ask | WFM Example |
|---|---|---|
| Expectations | What's the minimum expected outcome? | "Task list shows accurate counts" |
| Savings | What would save time or effort? | "One-click bulk assignment" |
| Adoption Factors | What would make them use a new feature? | "Works on mobile without a separate login" |
| Life Improvement | What would delight them? | "Proactive alerts when queue is filling up" |

---

## How to Apply JTBD in Practice

### Step 1: Define the Segment and Context
- Who is the user? (ops agent / pharmacy manager / pharmacist)
- What situation triggers the job? (start of shift / peak volume / EOD handoff)
- What are they currently using instead? (spreadsheet / Slack DMs / memory)

### Step 2: Identify the Functional Job
- Ask: "What are they trying to accomplish right now?"
- Use the formula: `[verb] + [object] + [context]`
- Keep it solution-agnostic — no product names

### Step 3: Layer in Social and Emotional Jobs
- "In front of whom does this job need to happen?"
- "How do they want to feel when it goes well / badly?"

### Step 4: Map Pains and Gains
- Work through the 4 pain types
- Work through the 4 gain types
- Rank each by intensity (critical / moderate / minor)

### Step 5: Validate
- Cross-reference with discovery interview notes
- Check if existing product decisions addressed any of these
- Surface to `/brain-discovery` or `/brain-prd` as persona context

---

## JTBD vs. User Stories

| JTBD | User Story |
|---|---|
| Why users need something | What to build |
| Solution-agnostic | Solution-specific |
| Discovered through research | Written for engineering |
| Stable over time | Changes sprint to sprint |

JTBD informs the "So that..." clause of a user story. A story without a JTBD-grounded "so that" is probably a task, not an outcome.

**Bad:** "As an ops agent, I want a bulk assign button, so that I can click fewer times."
**Better:** "As an ops agent, I want to assign multiple tasks at once, so that I can clear my queue before end of shift without losing track of what's unassigned." (functional + emotional job embedded)

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Confusing jobs with solutions | Ask "why?" 5 times until you find the human need |
| Generic jobs ("be more productive") | Narrow to specific context + verb + object |
| Ignoring social and emotional jobs | These often explain adoption more than functional fit |
| Fabricating JTBD without any research | Even 3 user interviews changes the picture dramatically |
| Treating all pains as equal | Rank by intensity — critical pains deserve solutions, minor ones don't |

---

## Related Frameworks

- `domain/problem-framing.md` — Frame the problem context before generating jobs
- `domain/opportunity-solution-tree.md` — Use jobs as inputs to opportunities in OST
- `domain/customer-discovery-frameworks.md` — Gather JTBD insights through discovery interviews and CJM
- `domain/user-story-best-practices.md` — Embed JTBD in the "so that" clause
