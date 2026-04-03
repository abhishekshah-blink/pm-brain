---
name: brain-prd
version: 1.0.0
description: This skill should be used when the user wants to "write a PRD", "create a one-pager", "write a product spec", "draft a requirements doc", or "write a brief for <feature>". Produces a complete PRD or one-pager saved to ~/pm/brain/knowledge/prd/ and optionally creates a Confluence page.
allowed-tools: Read, Glob, Grep, Bash, Write, Task, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_search, mcp__atlassian__confluence_create_page, mcp__atlassian__confluence_search, mcp__atlassian__confluence_get_page
---

## Brain Context
Read ~/pm/brain/.claude/PREAMBLE.md now. Follow all directives within it.
Read ~/pm/brain/knowledge/domain/problem-framing.md — used in Step 1.5.
Read ~/pm/brain/knowledge/domain/customer-discovery-frameworks.md — used in Step 1.6.
Read ~/pm/brain/knowledge/domain/product-strategy-frameworks.md — used in Working Backwards stress-test.
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
sqlite3 ~/pm/brain/data/brain.db "SELECT title, file_path, summary FROM knowledge_items WHERE category IN ('stakeholders', 'domain') AND (tags LIKE '%persona%' OR title LIKE '%persona%' OR title LIKE '%ops agent%' OR title LIKE '%pharmacy manager%') LIMIT 3;" 2>/dev/null
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
sqlite3 ~/pm/brain/data/brain.db "
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

#### FULL BRD FORMAT

Read the company template first: `~/.claude/blink-ai-tools/report_templates/brd_template.md`

Follow that structure exactly. The sections are: Objective, Background, Problems, Solution (Audience + FAQs), Stakeholders, Outcome Metrics and Analytics, Detailed Requirements (P0/P1/P2 priority table), User Stories, Roadmap/Launch Plan.

Key guidance per section:
- **Objective**: hero statement — the "why" all stakeholders must align on
- **Background**: context + links to prior docs, decisions from brain.db, relevant Jira/Confluence
- **Problems**: cite the problem statement locked in Step 1.5; include any ops feedback, error rates, or user quotes from brain context
- **Solution → Audience**: use the persona from Step 1.6
- **Solution → FAQs**: populate from the template's standard questions; add any specific open questions
- **Stakeholders**: pull names from `knowledge/stakeholders/` where available; use template defaults for legal/finance/data/cloud/ITSEC
- **Outcome Metrics**: leading + lagging indicators from the problem statement; align with Segment event tracking if relevant
- **Detailed Requirements**: use P0/P1/P2 priority table from template; write as use-case groups, not a flat list
- **User Stories**: as a [persona]... format — derive from acceptance criteria
- **Roadmap/Launch Plan**: chunk into phases if multi-sprint

Document title format: `[WIP] BRD – {Feature Name}`
Add header note: `## Note: This is an AI generated document. Stakeholders are required to review the content before publishing the final version.`

**Working Backwards Stress-Test** (run before saving — brain addition not in the company template):
Before finalizing, answer these 5 questions. If you can't answer them confidently, the BRD needs more work:
1. Would an ops agent or pharmacy manager recognize themselves in this document?
2. Is the problem statement specific enough that a new team member would understand why it matters?
3. Are the success metrics measurable without ambiguity?
4. Is the document free of internal jargon a non-Blinkhealth person couldn't understand?
5. Does this pass the "so what?" test — would someone reading cold care about this?

---

### Step 4: Confirm and save

Show the draft. Ask: "Shall I save this? Also create a Confluence page? (yes/no)"

**Always save locally:**
Write to `~/pm/brain/knowledge/prd/<YYYY-MM-DD>-<slug>.md` and upsert into brain.db.

**If Confluence confirmed:**
Call `mcp__atlassian__confluence_create_page` with:
- title: `PRD: {Feature Name}`
- body: the markdown content
- space: the WFM or appropriate space

### Step 5: Auto-log

```bash
echo "- PRD created: <title> → knowledge/prd/<filename>.md ($(date +%Y-%m-%d))" >> ~/pm/brain/knowledge/scratch/$(date +%G-W%V)-activity.md
```
