---
name: brain-plan
version: 1.0.0
description: This skill should be used when the user wants to "plan a feature", "write a PRD", "break down a ticket", "design X", "draft acceptance criteria", or needs an implementation plan for a Jira ticket or product idea. Looks up existing PRDs, decisions, stakeholder context, and live Jira data before producing a structured feature plan.
allowed-tools: Read, Glob, Grep, Bash, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_search, mcp__atlassian__confluence_search, mcp__atlassian__confluence_get_page, Task, Write
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`

## Instructions

You are running /brain-plan. Your job is to produce a structured feature plan grounded in existing product context, live Jira data, and Blinkhealth's technical constraints.

**Iron Law: Never plan in a vacuum.** Always load brain context before writing a single line of the plan.

### Step 1: Parse arguments

Extract from $ARGUMENTS:
- **Feature name or description** (e.g. "shift summary feature")
- **Jira ticket key** if present (e.g. WFM-1234)
- **Target project** if mentioned (e.g. task-assignment-service)

If no arguments, ask: "What feature or ticket should I plan? Provide a name, description, or Jira ticket key."

### Step 2: Brain context lookup

Search the knowledge base for relevant existing context:

```bash
# Search for related PRDs, decisions, features, and domain knowledge
sqlite3 ~/brain/data/brain.db "
SELECT category, title, file_path, summary
FROM knowledge_items
WHERE (title LIKE '%{term}%' OR tags LIKE '%{term}%' OR summary LIKE '%{term}%')
AND category IN ('prd', 'decisions', 'domain', 'features', 'oncall')
ORDER BY updated_at DESC
LIMIT 10;
"
```

Read the top 3–5 matching files. Note any existing decisions, constraints, or prior art relevant to this feature.

Also check stakeholders:
```bash
sqlite3 ~/brain/data/brain.db "SELECT name, role, team, file_path FROM stakeholders;"
```

### Step 3: Live Jira lookup

If a ticket key was provided: call `mcp__atlassian__jira_get_issue` for full detail (description, acceptance criteria, comments, epic).

If no ticket key: call `mcp__atlassian__jira_search` with JQL `project = WFM AND text ~ "{feature_name}" ORDER BY updated DESC` to find related tickets and epics.

Load the epic context if present (call `mcp__atlassian__jira_get_issue` on the epic key).

### Step 4: Live Confluence lookup

Search for related design docs:
- Call `mcp__atlassian__confluence_search` with: `title ~ "{feature_name}" OR text ~ "{feature_name}"`
- If results found: call `mcp__atlassian__confluence_get_page` for the top result
- Note the page URL for reference in the plan

### Step 5: Load technical context

Determine the most likely target project from context. Read its CLAUDE.md:
- task-assignment-service → `~/Documents/your-company/task-assignment-service/CLAUDE.md`
- rx-os-backend → `~/Documents/your-company/rx-os-backend/CLAUDE.md`
- rx-os-frontend → `~/Documents/your-company/rx-os-frontend/CLAUDE.md`
- wfm-microfrontends → `~/Documents/your-company/wfm-microfrontends/CLAUDE.md`

If the project is ambiguous, note it as an open question.

### Step 6: Draft the feature plan

Produce a structured plan in this format:

```markdown
# Feature Plan: {Feature Name}

**Date:** {today}
**Jira Ticket:** {KEY or TBD}
**Epic:** {epic_key}
**Status:** Discovery

## Problem Statement
{1-2 sentences: what problem does this solve, for whom, and why now}

## Stakeholder Context
{Who cares about this feature, their priorities (from knowledge/stakeholders/)}

## Prior Art & Decisions
{Relevant existing PRDs, decisions, or domain knowledge found in brain — with file links}

## Proposed Solution
{High-level approach — what we're building}

## Acceptance Criteria
- [ ] {criterion 1}
- [ ] {criterion 2}
- [ ] ...

## Technical Approach
{Based on target project's patterns from CLAUDE.md}
- Service: {project}
- Key components to modify: {files/modules}
- Data model changes: {if any}
- API changes: {if any}

## Open Questions
1. {Question that needs PM decision}
2. {Question that needs engineering input}

## Suggested Jira Sub-Tasks
(Not created yet — confirm before creating)
- [ ] {sub-task 1}
- [ ] {sub-task 2}

## References
- Jira: {ticket URL}
- Confluence: {page URL if found}
- Brain knowledge: {linked files}
```

### Step 7: Write to knowledge base

Write the plan to `~/brain/knowledge/features/{YYYY-MM-DD}-{slug}.md` and upsert into brain.db:

```bash
sqlite3 ~/brain/data/brain.db "
INSERT OR REPLACE INTO knowledge_items (file_path, category, title, summary, tags, created_at, updated_at, indexed_at)
VALUES ('knowledge/features/{YYYY-MM-DD}-{slug}.md', 'features', '{Feature Name}', '{1-sentence summary}', '{tag1},{tag2},{tag3}', '{today}', '{today}', datetime('now'));
"
```

Report the file path written and ask: "Shall I create the Jira sub-tasks listed above?"
