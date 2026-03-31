---
title: "Opportunity Solution Tree (OST)"
category: domain
tags: [discovery, ost, teresa-torres, frameworks, opportunities, solutions]
created: 2026-03-30
updated: 2026-03-30
---

# Opportunity Solution Tree (OST)

**Source:** Teresa Torres, *Continuous Discovery Habits* (2021)
**When to use:** Before committing to a solution. When you have a stakeholder request, a vague problem, or a direction you want to explore. Prevents "feature factory" syndrome.

---

## What It Is

A visual structure that connects:

```
Desired Outcome (1)
    └── Opportunity 1 (problem worth solving)
    │       ├── Solution A → Experiment
    │       ├── Solution B → Experiment
    │       └── Solution C → Experiment
    └── Opportunity 2
    │       ├── Solution A
    │       └── Solution B
    └── Opportunity 3
            └── ...
```

**Key insight:** You don't pick one opportunity and abandon the others. You work across the tree simultaneously — running small experiments to learn.

---

## How to Build One

### Step 1: Define the Desired Outcome

The outcome must be:
- Measurable behavior change (not a feature or output)
- Something the team can influence
- Specific enough to know when you've achieved it

**Common WFM outcome types:**
- Reduce task assignment errors (efficiency)
- Increase pharmacist utilization rate (efficiency)
- Reduce task reassignment rate (quality)
- Reduce ops agent time-to-complete per task (speed)

**Bad outcome:** "Improve the task assignment experience"
**Good outcome:** "Reduce manual task reassignment rate by 25% in 90 days"

---

### Step 2: Generate Opportunities (Not Solutions)

An opportunity = a customer problem, pain, or desire that, if addressed, would drive the outcome.

**Rules:**
- Frame as problems the user experiences, not features to build
- Generate at least 3 before converging
- Each opportunity should be independent (solving one doesn't solve the others)

**Test:** "Is this phrased from the user's perspective?" If you can't say "users experience this as a problem," it's probably a solution in disguise.

**Bad opportunity:** "Build a batch assignment feature"
**Good opportunity:** "Ops agents lose track of which tasks still need to be assigned during busy periods"

---

### Step 3: Generate Solutions per Opportunity

For each opportunity, brainstorm at least 3 solutions:
- Solutions should be concrete enough to prototype or test
- Diverge before converging — don't jump to the obvious solution
- Solutions don't have to be full features; they can be workflow changes, copy changes, or process changes

---

### Step 4: Select a POC (Proof of Concept)

Score each candidate solution on:

| Criterion | Score (1–5) | Notes |
|---|---|---|
| Feasibility | | How hard is this to build? |
| Impact | | If it works, how much does it move the outcome? |
| Market/Mission Fit | | Does it align with product strategy? |

Pick the highest-scoring solution as the POC. The point is not certainty — it's to pick the most promising bet to test first.

---

### Step 5: Design an Experiment

For the selected POC, define:
- **Hypothesis:** If we [solution], then [measurable outcome] will occur
- **Experiment type:**
  - A/B test (for live product with sufficient traffic)
  - Prototype + usability test (for UX questions)
  - Manual/concierge (fake it before building it)
  - Wizard-of-Oz (simulate the feature manually)
- **Success criteria:** What data or observation would validate this?
- **Timeframe:** 2–4 weeks typical; don't design 6-month experiments

---

## Common Pitfalls

| Pitfall | What to do instead |
|---|---|
| Opportunities that are really solutions | Ask "why does this problem exist?" until you find the user pain |
| Only one opportunity per tree | Generate at least 3 before converging |
| Vague desired outcome | Make it measurable (number + timeframe) |
| Skipping experiments (building IS the test) | Always define a smaller, faster way to learn |
| Using OST once and abandoning it | Update the tree weekly as you learn |

---

## Blinkhealth Application

Use OST when:
- A WFM ticket comes in as a feature request — convert to an opportunity first
- An ops Slack message suggests a solution — extract the underlying job via `/brain-discovery`
- You're starting a new epic and want to avoid premature convergence
- Product strategy session / quarterly planning

When running `/brain-discovery`, the OST is constructed as part of the workflow.

---

## Related Frameworks

- `domain/jobs-to-be-done.md` — Use JTBD to generate better opportunities
- `domain/problem-framing.md` — Use problem framing to define the desired outcome
- `domain/user-story-best-practices.md` — After OST, convert validated solutions to epics/stories
- `domain/feature-investment-framework.md` — Use financial lens to validate investment before building
