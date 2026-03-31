---
name: brain-prd
version: 1.0.0
description: This skill should be used when the user wants to "write a PRD", "create a one-pager", "write a product spec", "draft a requirements doc", or "write a brief for <feature>". Produces a complete PRD or one-pager saved to ~/brain/knowledge/prd/ and optionally creates a Confluence page.
allowed-tools: Read, Glob, Grep, Bash, Write, Task, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_search, mcp__atlassian__confluence_create_page, mcp__atlassian__confluence_search, mcp__atlassian__confluence_get_page
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
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
grep -r "<key_term>" ~/Documents/your-company/ --include="*.py" --include="*.ts" -l 2>/dev/null | head -5
```

### Step 3: Write the document

---

#### ONE-PAGER FORMAT

```markdown
# One-Pager: {Feature Name}

**Author:** [Your Name] | **Date:** {today} | **Status:** Draft
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

**Author:** [Your Name] | **Date:** {today} | **Status:** Draft
**Jira Epic:** {KEY or TBD} | **Target:** {sprint or quarter}
**Stakeholders:** {names from knowledge/stakeholders/ — PM, Eng Lead, Design, Ops}

---

## Executive Summary
{3-5 sentences: problem, solution, expected impact. Should stand alone if someone reads nothing else.}

## Background & Problem Statement
{What's happening today. Why this is a problem worth solving now.
Include: user quotes, ops feedback, error rates, frequency if known.}

## Goals
- **Primary:** {The one thing this must achieve}
- **Secondary:** {Nice to have outcomes}
- **Non-goals:** {What we're explicitly NOT trying to do}

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
| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| {Metric 1} | {current} | {goal} | {how to measure} |

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
