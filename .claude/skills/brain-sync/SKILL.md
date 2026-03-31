---
name: brain-sync
version: 1.0.0
description: This skill should be used when the user wants to "sync Jira", "pull my tickets", "sync Confluence", "update my brain from Jira", "pull sprint tickets", "sync a specific ticket WFM-XXXX", or "show my open PRs". Invokes the Scout agent to pull live Jira, Confluence, and GitHub data into ~/brain/knowledge/.
allowed-tools: Read, Write, Bash, Task, mcp__atlassian__jira_search, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_get_sprint_issues, mcp__atlassian__jira_get_sprints_from_board, mcp__atlassian__confluence_search, mcp__atlassian__confluence_get_page, mcp__github__list_pull_requests
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`
- brain.db ticket count: !`sqlite3 ~/brain/data/brain.db "SELECT COUNT(*) FROM jira_tickets;" 2>/dev/null || echo "0"`

## Instructions

You are running /brain-sync. Your job is to pull live data from Jira, Confluence, and/or GitHub into ~/brain/knowledge/ and update brain.db.

### Step 1: Parse sync mode from $ARGUMENTS

Determine which mode to run:

| Argument | Mode |
|---|---|
| (no args) | **full** — sprint sync + recently updated tickets + open PRs |
| `sprint` | **sprint** — all tickets in the current open sprint |
| `WFM-XXXX` or any ticket key | **ticket** — single ticket |
| `confluence <term>` | **confluence** — search and sync a Confluence page |
| `prs` | **prs** — sync open GitHub PRs only |

### Step 2: Execute sync

**Ticket mode:** Call `mcp__atlassian__jira_get_issue` for the given key. Write to `~/brain/knowledge/jira/{KEY}.md` with this structure:

```markdown
---
title: "{KEY}: {summary}"
category: jira
tags: [{project}, {epic_key}, {priority}, {status}]
created: {issue_created}
updated: {issue_updated}
jira_tickets: [{KEY}]
confluence_pages: []
stakeholders: [{assignee}]
---

# {KEY}: {summary}

**Status:** {status} | **Priority:** {priority} | **Assignee:** {assignee}
**Epic:** {epic_key} | **Sprint:** {sprint}

## Description
{description}

## Acceptance Criteria
{acceptance_criteria — omit section if not present}

**Synced:** {datetime}
```

Then upsert into brain.db:
```bash
sqlite3 ~/brain/data/brain.db "INSERT OR REPLACE INTO jira_tickets (ticket_key, summary, status, assignee, priority, epic_key, sprint, file_path, last_synced) VALUES ('{KEY}', '{summary}', '{status}', '{assignee}', '{priority}', '{epic_key}', '{sprint}', 'knowledge/jira/{KEY}.md', datetime('now'));"
```

**Sprint mode:** Call `mcp__atlassian__jira_search` with JQL: `project = WFM AND sprint in openSprints() ORDER BY priority ASC`. Process each ticket as above.

**Full mode:** Run sprint mode, then also search `project = WFM AND updated >= -3d ORDER BY updated DESC` for recently changed tickets.

**Confluence mode:** Call `mcp__atlassian__confluence_search` with the search term, pick the top result, call `mcp__atlassian__confluence_get_page` for the body. Write to `~/brain/knowledge/confluence/{page_id}.md`. Upsert into confluence_pages table.

**PRs mode:** Call `mcp__github__list_pull_requests` for each active repo (task-assignment-service, rx-os-backend, rx-os-frontend, wfm-microfrontends). Write summary to `~/brain/knowledge/scratch/github-pr-status.md`.

### Step 3: Verify sync

After writing all files, confirm rows were updated:
```bash
sqlite3 ~/brain/data/brain.db "SELECT ticket_key, summary, status FROM jira_tickets WHERE last_synced >= datetime('now', '-5 minutes') ORDER BY last_synced DESC;"
```

### Step 4: Report what changed

Compare current status against what was stored before this sync. Surface:
- Tickets that changed status (e.g. "In Progress → Done")
- New tickets not previously in brain.db
- Confluence pages updated since last sync

Output a clean summary table:

```
Synced: X tickets, Y Confluence pages, Z PRs

Changed since last sync:
  WFM-XXXX: In Progress → Done
  WFM-YYYY: NEW — "Description of new ticket"

All synced files:
  ~/brain/knowledge/jira/WFM-XXXX.md
  ...
```
