---
name: brain-discovery
version: 1.0.0
description: This skill should be used when the user wants to "run discovery on X", "do discovery for WFM-1234", "help me understand the problem before building", "frame the problem", or "I don't want to jump to a solution." Guides through problem framing → JTBD mapping → Opportunity Solution Tree → discovery experiment plan.
allowed-tools: Read, Glob, Grep, Bash, Write, Task, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_search, mcp__atlassian__confluence_search, mcp__atlassian__confluence_get_page
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
Read ~/brain/knowledge/domain/problem-framing.md — this is your Phase 1 guide.
Read ~/brain/knowledge/domain/jobs-to-be-done.md — this is your Phase 2 guide.
Read ~/brain/knowledge/domain/opportunity-solution-tree.md — this is your Phase 3 guide.
- Current date: !`date +%Y-%m-%d`

## Instructions

You are running /brain-discovery. Your job is to prevent premature solution commitment by guiding through structured problem framing, JTBD analysis, and Opportunity Solution Tree construction before a single line of code is planned.

**Iron Law: No solutions before you've defined the problem and the job.**

---

### Step 1: Parse arguments

Extract from $ARGUMENTS:
- **Topic, feature area, or description** (e.g., "task assignment errors")
- **Jira ticket key** if provided (e.g., WFM-1234)

If no arguments: ask "What area or problem should we run discovery on? You can provide a Jira ticket key, a feature name, or describe the situation in plain language."

---

### Step 2: Load brain context

```bash
sqlite3 ~/brain/data/brain.db "
SELECT category, title, file_path, summary
FROM knowledge_items
WHERE (title LIKE '%{term}%' OR tags LIKE '%{term}%' OR summary LIKE '%{term}%')
AND category IN ('prd', 'decisions', 'features', 'domain', 'oncall')
ORDER BY updated_at DESC
LIMIT 8;
" 2>/dev/null
```

If a Jira key was provided: call `mcp__atlassian__jira_get_issue` for full ticket context (description, comments, acceptance criteria, epic).

If a search term only: call `mcp__atlassian__jira_search` with JQL: `project = WFM AND text ~ "{term}" ORDER BY updated DESC` to surface related tickets.

Check Confluence: call `mcp__atlassian__confluence_search` with `title ~ "{term}" OR text ~ "{term}"` to find any prior design docs.

---

### Step 3: Problem Framing (MITRE Canvas — 3 phases)

Present the three phases conversationally. For each question, offer 3–5 options to select from (numbered) OR invite free-form input. After all 3 phases, synthesize.

---

**Phase 1: Look Inward**

Ask (combine into one question):
> "Let's start by looking inward. Answer these 3 questions:
> 1. What are the symptoms you're observing? (What do users complain about? What does the data show? What workarounds exist?)
> 2. Why hasn't this been solved yet? (New problem / too hard / low priority / no resources / political / systemic)
> 3. Is there any bias or assumption that might be shaping how we're framing this? (Confirmation bias / internal convenience / survivorship bias / we already have a solution in mind)"

---

**Phase 2: Look Outward**

Ask:
> "Now let's look outward:
> 4. Who specifically experiences this problem? When? What are the consequences when it goes wrong?
> 5. Who else has a version of this problem? Who doesn't — and what's different about them?
> 6. Are there any user segments we haven't heard from? Is there anyone who benefits from this problem NOT being solved?"

---

**Phase 3: Reframe**

Synthesize answers from Phases 1 and 2 into:

**Restatement:**
> "[Persona] struggles to [functional job] because [root cause], which results in [consequence], affecting [secondary impact]. This is often overlooked because [bias]."

**HMW question:**
> "How might we [action] as we aim to [objective]?"

Show the restatement and HMW. Ask: "Does this capture the problem correctly? Any adjustments?"

---

### Step 4: JTBD Mapping

Based on the framing above, map the job:

```
Functional Job: "[verb] + [object] + [context/constraint]"
Social Job: "Be perceived as [X] by [Y]"
Emotional Job: "Feel [state] / Avoid feeling [state]"

Key Pains (top 2-3):
- [Pain 1: specific, behavioral]
- [Pain 2]

Key Gains (top 2):
- [Gain 1: what success looks like]
- [Gain 2]
```

Ask: "Does this match the job as you understand it from talking to users? Anything to add or correct?"

---

### Step 5: Opportunity Solution Tree (OST)

**Desired Outcome:**
Convert the HMW question into a measurable desired outcome:
> "[Measurable behavior change] by [timeframe]"

Example: "Reduce manual task reassignment rate by 25% within 90 days"

Ask for confirmation or help refine: "Is this the right outcome metric? What would we measure?"

---

**Generate 3 Opportunities:**

An opportunity = a user problem/pain that, if solved, would drive the desired outcome.
Frame each as: "[Persona] experiences [problem] when [situation]"

Offer 3 candidate opportunities based on the JTBD pains identified. Ask: "Do these feel right? Add, remove, or refine any."

---

**Generate Solutions per Opportunity:**

For the top opportunity, generate 3 candidate solutions.
Rate each on:
- **Feasibility** (1–5): How hard to build?
- **Impact** (1–5): If it works, how much does it move the outcome?
- **Mission fit** (1–5): Aligns with product strategy?

Recommend the highest-scoring solution as the POC.

---

### Step 6: Discovery Experiment Plan

For the recommended POC, define:

```markdown
## Discovery Experiment

**POC:** [solution name]

**Hypothesis:**
If we [solution], then [desired outcome] will occur.

**Experiment type:** [Choose one]
- [ ] Prototype + usability test (5 users, 45 min each) — best for UX questions
- [ ] Concierge test (manually deliver the experience before building it)
- [ ] A/B test (requires live traffic — only for incremental changes)
- [ ] Wizard-of-Oz (simulate the feature; users believe it's real)
- [ ] Discovery interviews (5 sessions) — best for validating the opportunity itself

**Success signal:**
We'll know this hypothesis is worth building if within [2–4 weeks] we observe:
- Quantitative: [specific measurable signal]
- Qualitative: [observable user behavior]

**Who to involve:** [ops agents / pharmacy managers / engineering / design]
**Timeline:** [start date] → [decision date]
```

---

### Step 7: Save the discovery artifact

Write to `~/brain/knowledge/features/{YYYY-MM-DD}-discovery-{slug}.md`:

```markdown
---
title: "Discovery: {topic}"
category: features
tags: [discovery, {topic-tags}]
created: {today}
updated: {today}
jira_tickets: [{KEY if any}]
---

# Discovery: {topic}

**Date:** {today} | **Status:** Discovery

## Problem Restatement
{the restatement from Phase 3}

## HMW Question
{the HMW from Phase 3}

## JTBD Summary
- Functional job: {job}
- Key pain: {top pain}
- Key gain: {top gain}

## OST
**Desired Outcome:** {outcome}
**Top Opportunity:** {opportunity}
**Recommended POC:** {solution}

## Experiment Plan
{experiment block from Step 6}

## Brain Context Used
{list of knowledge items referenced}
```

Upsert into brain.db:
```bash
sqlite3 ~/brain/data/brain.db "
INSERT OR REPLACE INTO knowledge_items (file_path, category, title, summary, tags, created_at, updated_at, indexed_at)
VALUES ('knowledge/features/{YYYY-MM-DD}-discovery-{slug}.md', 'features', 'Discovery: {topic}', '{1-sentence summary}', 'discovery,{slug}', '{today}', '{today}', datetime('now'));
"
```

Report the file written and ask: "Next steps: run the experiment, or should I create a Jira story for this now?"
