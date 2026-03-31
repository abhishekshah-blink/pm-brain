---
name: brain-prd
version: 1.0.0
description: This skill should be used when the user wants to "write a PRD", "create a one-pager", "write a product spec", "draft a requirements doc", or "write a brief for <feature>". Produces a complete PRD or one-pager saved to ~/brain/knowledge/prd/ and optionally creates a Confluence page.
allowed-tools: Read, Glob, Grep, Bash, Write, Task, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_search, mcp__atlassian__confluence_create_page, mcp__atlassian__confluence_search, mcp__atlassian__confluence_get_page
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
Read ~/brain/knowledge/domain/problem-framing.md — used in Step 1.5.
Read ~/brain/knowledge/domain/customer-discovery-frameworks.md — used in Step 1.6.
Read ~/brain/knowledge/domain/product-strategy-frameworks.md — used in Working Backwards stress-test.
- Current date: !`date +%Y-%m-%d`
- ISO week: !`date +%G-W%V`

## Instructions

You are running /brain-prd. Your job is to produce a clear, decision-enabling product document. The format scales with scope: a one-pager for small features, a full PRD for significant initiatives.

**A great PRD answers: What, Why, Who, How we'll know it worked, and What's NOT included.**

### Step 1: Determine scope and format

If $ARGUMENTS contains a feature name or Jira ticket, use it. If empty, ask:
"What feature or initiative is this PRD for?"

Also ask: "What format? (One-pager for small feature / Full PRD for major initiative)"

| Format | When to use |
|---|---|
| **One-pager** | Small feature, internal tool improvement, single-team scope |
| **Full PRD** | New product capability, multi-team, significant user impact |

### Step 1.5: Problem Statement Gate

Before loading context, lock in the problem. Ask:

> "Before drafting, let's confirm we're solving the right problem:
> 1. What is the user struggling to do right now? (Observable behavior — not a solution)
> 2. What is the root cause? (Ask 'why' at least twice — don't stop at the symptom)
> 3. What is the consequence when this problem occurs? (For the user, and for the business)"

From these answers, write one sentence:
> **"[Persona] needs a way to [desired outcome] because [root cause], which currently [emotional/practical impact]."**

Show this to the user and confirm before proceeding. A PRD without a confirmed problem statement will drift.

If the user says discovery hasn't been done yet, suggest running `/brain-discovery` first.

### Step 1.6: Proto-Persona

Identify the primary persona. Check brain first:
```bash
sqlite3 ~/brain/data/brain.db "SELECT title, file_path, summary FROM knowledge_items WHERE category IN ('stakeholders', 'domain') AND (tags LIKE '%persona%' OR title LIKE '%persona%' OR title LIKE '%ops agent%' OR title LIKE '%pharmacy manager%') LIMIT 3;" 2>/dev/null
```

If no existing persona, draft quickly:
```
Persona: [alliterative name — e.g., "Ops Agent Olivia"]
Role: [specific WFM role and team]
Primary job: [functional outcome they're trying to achieve]
Key pain: [the specific barrier this PRD addresses]
Success feels like: [emotional state when this works]
[ASSUMPTION — validate with 3 user interviews]
```

### Step 2: Load all available context

**From brain knowledge base:**
```bash
sqlite3 ~/brain/data/brain.db "
SELECT title, category, file_path, summary
FROM knowledge_items
WHERE (title LIKE '%<term>%' OR tags LIKE '%<term>%')
AND category IN ('prd', 'decisions', 'features', 'domain', 'stakeholders')
ORDER BY updated_at DESC LIMIT 8;
" 2>/dev/null
```

**From Jira** (if an epic or ticket key is mentioned):
- Call `mcp__atlassian__jira_get_issue` for the epic
- Call `mcp__atlassian__jira_search` with `project = WFM AND "Epic Link" = <key>` for child stories

**From Confluence** (check if a design doc already exists):
- Call `mcp__atlassian__confluence_search` with `title ~ "<feature_name>"`

**From codebase** (understand technical context):
```bash
grep -r "<key_term>" ~/Documents/blinkhealth/ --include="*.py" --include="*.ts" -l 2>/dev/null | head -5
```

### Step 3: Write the document

---

#### ONE-PAGER FORMAT

```markdown
# One-Pager: {Feature Name}

**Author:** Abhishek Shah | **Date:** {today} | **Status:** Draft
**Jira Epic:** {KEY or TBD} | **Target:** {sprint or quarter}

## TL;DR
{1-2 sentence summary: what this is and why we're doing it}

## Problem
{The specific user pain or business gap — be concrete. Cite data or ops feedback if available.}

## Proposed Solution
{What we'll build. Keep it behavioral — what users will be able to do, not how it works.}

## Success Metrics
- {Metric 1}: {target} (e.g. "Task assignment errors reduced by 50%")
- {Metric 2}: {target}

## Scope
**In:** {bullet list of what's included}
**Out:** {bullet list of explicit exclusions — be specific}

## Key Decisions Needed
1. {Decision 1 — who decides?}
2. {Decision 2}

## Risks & Open Questions
- {Risk or open question}
```

---

#### FULL PRD FORMAT

```markdown
# PRD: {Feature Name}

**Author:** Abhishek Shah | **Date:** {today} | **Status:** Draft
**Jira Epic:** {KEY or TBD} | **Target:** {sprint or quarter}
**Stakeholders:** {names from knowledge/stakeholders/ — PM, Eng Lead, Design, Ops}

---

## Executive Summary
{3-5 sentences: problem, solution, expected impact. Should stand alone if someone reads nothing else.}

## Background & Problem Statement
{What's happening today. Why this is a problem worth solving now.
Include: user quotes, ops feedback, error rates, frequency if known.}

## Goals
- **Primary:** {The one thing this must achieve — measurable}
- **Secondary:** {Nice to have outcomes}
- **Non-goals (Won't Have this cycle):** {What we're explicitly NOT trying to do — be specific. "We will not..." format}

## Users & Personas
| Persona | Role | Primary Need |
|---|---|---|
| {Ops Agent} | {Uses WFM daily} | {What they need} |
| {Pharmacy Manager} | {Oversees ops} | {What they need} |

## Proposed Solution

### User Experience
{How the feature works from the user's perspective — written as a narrative walkthrough.
What do they see? What do they click? What's the result?}

### Key User Flows
1. {Flow 1}: {step by step}
2. {Flow 2}: {step by step}

## Functional Requirements
| # | Requirement | Priority |
|---|---|---|
| FR-1 | {Specific behavior} | Must Have |
| FR-2 | {Specific behavior} | Should Have |
| FR-3 | {Specific behavior} | Could Have |

## Non-Functional Requirements
- **Performance:** {e.g. "Task list loads in < 2s with 1000 tasks"}
- **Reliability:** {SLA expectations}
- **Accessibility:** {Any requirements}

## Technical Approach
{High-level approach for engineering — services involved, API changes, data model.
Based on codebase investigation.}

**Affected services:** {list}
**Estimated complexity:** {S / M / L / XL}

## Success Metrics
| Metric | Type | Baseline | Target | Measurement |
|---|---|---|---|---|
| {Metric 1 — leading indicator} | Leading | {current} | {goal} | {how to measure — leading indicators change within weeks} |
| {Metric 2 — lagging indicator} | Lagging | {current} | {goal} | {how to measure — lagging indicators change over months} |

*Leading indicators* (signal early): task assignment rate, session frequency, feature adoption rate
*Lagging indicators* (confirm later): error rate reduction, SLA compliance, ops throughput

## Working Backwards Stress-Test (Full PRD only)
Before finalizing, answer these 5 questions. If you can't answer them confidently, the PRD needs more work:
1. Would an ops agent or pharmacy manager recognize themselves in this document?
2. Is the problem statement specific enough that a new team member would understand why it matters?
3. Are the success metrics measurable without ambiguity?
4. Is the document free of internal jargon a non-Blinkhealth person couldn't understand?
5. Does this pass the "so what?" test — would someone reading cold care about this?

## Rollout Plan
- **Phase 1:** {What ships first}
- **Phase 2:** {What comes next}
- **Rollback plan:** {How to revert if needed}

## Open Questions
| Question | Owner | Due |
|---|---|---|
| {Question 1} | {name} | {date} |

## Appendix
{Links to related Jira tickets, Confluence pages, brain knowledge items}
```

---

### Step 4: Confirm and save

Show the draft. Ask: "Shall I save this? Also create a Confluence page? (yes/no)"

**Always save locally:**
Write to `~/brain/knowledge/prd/<YYYY-MM-DD>-<slug>.md` and upsert into brain.db.

**If Confluence confirmed:**
Call `mcp__atlassian__confluence_create_page` with:
- title: `PRD: {Feature Name}`
- body: the markdown content
- space: the WFM or appropriate space

### Step 5: Auto-log

```bash
echo "- PRD created: <title> → knowledge/prd/<filename>.md ($(date +%Y-%m-%d))" >> ~/brain/knowledge/scratch/$(date +%G-W%V)-activity.md
```
