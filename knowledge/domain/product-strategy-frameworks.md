---
title: "Product Strategy Frameworks — Positioning, Working Backwards, Lean UX Canvas"
category: domain
tags: [strategy, positioning, press-release, working-backwards, lean-ux, gothelf, moore, frameworks]
created: 2026-03-30
updated: 2026-03-30
---

# Product Strategy Frameworks

**Sources:** Geoffrey Moore, *Crossing the Chasm* (Positioning); Amazon Working Backwards (Press Release); Jeff Gothelf, *Lean UX* (Lean UX Canvas v2)
**When to use:** When starting a new product area, when stakeholders disagree on direction, when building a business case for a major initiative, when validating assumptions before committing resources.

---

## Framework 1: Positioning Statement (Geoffrey Moore)

### What It Is
A strategic clarity tool that forces hard choices about who you serve, what problem you solve, what category you're in, and why you're different. Not marketing copy — a decision-making guide.

### Two-Part Structure

**Value Proposition:**
```
For [specific target customer — not "everyone"]
  that need [underserved need — specific, not generic]
  [product / feature name]
  is a [product category — what mental model should they use?]
  that [benefit statement — outcomes, not features]
```

**Differentiation Statement:**
```
Unlike [primary competitor or competitive alternative users actually consider]
  [product / feature name]
  provides [unique differentiation — outcomes and proof, not adjectives]
```

### WFM Application
For internal products, "target customer" = the user segment, and "unlike" = the status quo they're currently using (manual process, spreadsheet, Slack workaround).

**Example:**
> For ops agents who need to manage high task volumes during peak pharmacy hours, WFM Task Manager is a real-time operations console that ensures every task is assigned and tracked before end of shift. Unlike the current manual assignment process (Slack + spreadsheet), WFM Task Manager surfaces unassigned tasks automatically and reduces reassignment rate.

### 5-Question Stress Test
1. Would a target customer recognize themselves in "For [customer]"?
2. Is "need" something they'd articulate as a problem?
3. Does the category name help them understand the product (or hurt it)?
4. Is the differentiation defensible with evidence?
5. Does this statement guide our feature decisions?

### Common Pitfalls
- "For everyone who..." — you can't position for everyone
- Feature list as benefit statement — outcomes only
- Imaginary competitor ("unlike legacy systems") — name the real alternative
- Differentiation without proof — if you can't back it up, it's aspiration

---

## Framework 2: Press Release / Working Backwards (Amazon)

### What It Is
Write a press release **before building anything**. Forces you to define the customer value upfront, test if the story resonates, and align stakeholders — as a planning tool, not launch copy.

> "If you can't write a compelling press release about what you're building, you don't know what you're building."

### 9-Part Structure

1. **Headline** — `[Product] Aims to [Specific Measurable Benefit] for [Target Customer]`
   - Good: "WFM Task Manager Aims to Eliminate Missed Task Assignments for Pharmacy Ops"
   - Bad: "Introducing Enhanced AI-Powered Task Management Features"

2. **Dateline** — City, Date

3. **Introduction paragraph** — What's launching, who it's for, the key benefit, and the problem named in one paragraph

4. **Problem paragraph** — Specific customer problem with validated data or a real user quote
   - Include: frequency, consequence, current workaround

5. **Solution paragraph** — Outcome-focused (not feature list) + an executive quote that shows customer empathy
   - Bad quote: "We're excited to bring this innovative new solution to market"
   - Good quote: "Ops agents told us end-of-shift task scrambles are the most stressful part of their day. This eliminates that."

6. **Supporting details** — Additional benefits or supporting data points

7. **Boilerplate** — Company/team background

8. **Call to action** — What should the reader do next?

9. **Contact information**

### 5-Question Stress Test (Run Before Finalizing)
1. Would a target customer actually care about this?
2. Is the problem stated specifically (not generically)?
3. Are the benefits measurable?
4. Is it free of jargon a non-employee could understand?
5. Does it pass the "so what?" test if read cold?

### When to Use
- Before writing a PRD for a major initiative
- When pitching a new product area to leadership
- When you suspect stakeholders aren't aligned on the value proposition
- As a sanity check before committing engineering resources

---

## Framework 3: Lean UX Canvas (Jeff Gothelf, v2)

### What It Is
An 8-box canvas that frames work around a **business problem to solve** rather than a solution to implement. Acts as an "insurance policy" by making assumptions explicit before committing to development.

### 8-Box Layout (fill in this order: 1→2→3→4→5→6→7→8)

```
┌── Box 1: Business Problem ──┬── Box 5: Solutions ──┬── Box 2: Business Outcomes ──┐
├── Box 3: Users ─────────────┤   (solutions are     ├── Box 4: User Outcomes ───────┤
├── Box 6: Hypotheses ────────┤   hypotheses, not    ├── Box 7: What to Learn First ─┤
│                             │   commitments)       ├── Box 8: Smallest Experiment ─┘
```

### Box Definitions

| Box | Key Question | Common Failure |
|---|---|---|
| **1. Business Problem** | What changed in the world that creates this problem? | Describing a solution |
| **2. Business Outcomes** | What measurable behavior change indicates success? | Only lagging indicators (revenue) |
| **3. Users** | Which persona are we focusing on first? | "All users" — pick one to start |
| **4. User Outcomes** | What do users want to achieve? How do they want to feel? | Confusing with Box 2 |
| **5. Solutions** | What could we build? (min 3 candidates) | Only one solution — forced convergence |
| **6. Hypotheses** | "We believe [biz outcome] will be achieved if [user] attains [benefit] with [solution]" | Missing explicit assumption |
| **7. Most Important to Learn** | What's the riskiest assumption? | Not distinguishing value vs. usability vs. feasibility risk |
| **8. Smallest Experiment** | What's the least work to learn this? | Building the feature itself as the experiment |

### Box 2 vs. Box 4 (Critical Distinction)
- **Box 2 (Business Outcome):** Measurable behavior change the business can observe. "Task reassignment rate drops by 25%." "Ops agents complete EOD checklist 10% faster."
- **Box 4 (User Outcome):** The user's goal and emotional state. "Ops agents feel confident nothing was missed." "Managers can see queue status without asking agents."

### Hypothesis Format
```
We believe [business outcome — Box 2]
will be achieved if [user — Box 3]
attains [user outcome — Box 4]
with [solution — Box 5].
```

### Experiment Types (Box 8)
- **Discovery interviews** — cheapest way to validate value assumptions
- **Landing page** — measures demand before building
- **Concierge test** — manually deliver the service; validate demand before automating
- **Wizard of Oz** — simulate the feature; user believes it's real
- **Smoke test / prototype** — cheapest buildable version

### When to Use
- Before committing a sprint to a new feature
- When the team is about to build something "because leadership said so"
- When you have multiple possible solutions and need to identify which assumption to test first

---

## Applying All Three Together

These frameworks build on each other for major initiatives:

1. **Lean UX Canvas** — frame the business problem and make assumptions explicit
2. **Press Release** — force customer-value clarity and stress-test the story
3. **Positioning Statement** — sharpen who it's for and why it's different from alternatives

Use all three before writing a full PRD for a significant new product area.

---

## Related Frameworks

- `domain/problem-framing.md` — Problem framing feeds into the Lean UX Canvas (Box 1)
- `domain/opportunity-solution-tree.md` — OST generates the solutions for Canvas Box 5
- `domain/feature-investment-framework.md` — Financial validation before committing
