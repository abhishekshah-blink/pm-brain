# Brain System — CLAUDE.md

> Single source of truth for ~/brain/. All agents and skills read this file.

## Identity

- **Name:** [Your Name]
- **Role:** Product Manager, [Your Team], [Your Company]
- **Jira workspace:** your-workspace.atlassian.net
- **GitHub org:** github.com/your-org
- **Active projects:** task-assignment-service, rx-os-backend, rx-os-frontend, wfm-microfrontends, ui-tools
- **Project root:** ~/Documents/your-company/

## What This System Is

~/brain/ is a Personal Knowledge Accelerator — a second brain that combines:
1. **Knowledge management** (PKA-style): raw inputs → structured markdown → SQLite index
2. **Dev workflow skills** (gstack-style): slash commands that check the brain before any dev work

The result: every planning, review, ship, investigate, and retro action is informed by accumulated product context, Jira state, Confluence docs, and past decisions.

## Knowledge Base

- **Root:** ~/brain/knowledge/
- **SQLite index:** ~/brain/data/brain.db
- **Inbox (unprocessed):** ~/brain/inbox/

### Taxonomy

| Category | Path | What goes here |
|---|---|---|
| `prd` | knowledge/prd/ | PRDs, user stories, acceptance criteria, launch checklists |
| `decisions` | knowledge/decisions/ | ADRs, product decisions, tradeoff docs, meeting decisions with rationale |
| `stakeholders` | knowledge/stakeholders/ | One file per person/team: role, preferences, priorities, communication style |
| `jira` | knowledge/jira/ | Ticket snapshots synced by Scout — filename: `{KEY}.md` (e.g. WFM-1234.md) |
| `confluence` | knowledge/confluence/ | Page snapshots synced by Scout — filename: `{page_id}.md` |
| `features` | knowledge/features/ | Feature briefs at various stages: discovery → design → dev → shipped |
| `retros` | knowledge/retros/ | Weekly retro outputs — filename: `YYYY-WW.md` |
| `domain` | knowledge/domain/ | WFM/pharmacy domain knowledge, SLA concepts, business glossary |
| `oncall` | knowledge/oncall/ | Incident postmortems, runbooks, alert context |
| `daily-journals` | knowledge/daily-journals/ | Daily meeting notes, standups, key decisions and action items from the day |
| `business-reviews` | knowledge/business-reviews/ | Weekly/monthly business reviews, OKR updates, metrics summaries |
| `ai-strategy` | knowledge/ai-strategy/ | AI adoption plans, agentic architecture decisions, AI tooling evaluations |
| `coaching-sessions` | knowledge/coaching-sessions/ | 1:1 coaching notes, leadership feedback, growth areas |
| `operating-plans` | knowledge/operating-plans/ | Quarterly/annual operating plans, roadmaps, team capacity plans |
| `scratch` | knowledge/scratch/ | Unclassified/working notes; reclassify later with Sorter |

### Naming Conventions

- Dated artifacts: `YYYY-MM-DD-<slug>.md` (e.g. `2026-03-30-wfm-shift-summary-prd.md`)
- Reference/evergreen content: `<slug>.md` (e.g. `task-assignment-sla.md`)
- Jira tickets: `{KEY}.md` (e.g. `WFM-1234.md`)
- Confluence pages: `{page_id}.md` (e.g. `123456789.md`)
- Retros: `YYYY-WW.md` (e.g. `2026-W13.md`)

### Required Frontmatter (every knowledge item)

```yaml
---
title: <title>
category: prd|decisions|stakeholders|jira|confluence|features|retros|domain|oncall|daily-journals|business-reviews|ai-strategy|coaching-sessions|operating-plans|scratch
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
jira_tickets: []       # optional: [WFM-1234]
confluence_pages: []   # optional: [page_id]
stakeholders: []       # optional: [name]
---
```

## Agent Roster

| Agent | File | Role | Invocation |
|---|---|---|---|
| **Sorter** | .claude/agents/sorter.md | Orchestrator — inbox processing and delegation | "Ask Sorter to process inbox" / "Sorter, classify these notes" |
| **Keeper** | .claude/agents/keeper.md | Knowledge librarian — writes + indexes knowledge items; answers lookup queries | "Keeper, index this PRD" / "Keeper, find context on task assignment SLA" |
| **Scout** | .claude/agents/scout.md | MCP sync agent — pulls Jira, Confluence, GitHub into knowledge base | "Scout, sync my sprint" / "Scout, pull WFM-1234" |

**Rule:** Agents are spawned via the Task tool. Skills and users interact with Sorter; Sorter delegates to Keeper and Scout.

## Skills

| Skill | Trigger phrases |
|---|---|
| `/brain-plan` | "plan a feature", "write a PRD", "break down a ticket", "design X" |
| `/brain-review` | "review my code", "check my changes", "review before commit" |
| `/brain-ship` | "ship this", "commit and push", "create a PR", "deploy to review" |
| `/brain-investigate` | "debug this", "root cause this", "investigate WFM-1234", "why is X failing" |
| `/brain-retro` | "run a retro", "weekly retro", "summarize my week" |
| `/brain-sync` | "sync Jira", "pull my tickets", "sync sprint", "sync WFM-1234" |
| `/brain-ops-feedback` | "ops feedback", "ops wants X", "feature request from ops", paste ops Slack |
| `/brain-ops-bug` | "ops bug", "ops reported X is broken", paste ops Slack describing broken behavior |
| `/brain-weekly-email` | "write the weekly email", "weekly status", "draft email for VP", "Friday email" |
| `/brain-user-story` | "write a user story", "create a story", "create a ticket for X" |
| `/brain-prd` | "write a PRD", "one-pager for X", "product spec", "requirements doc" |

**Skills always check the brain before starting dev work.** They query SQLite for relevant context, then load only the matching markdown files — keeping context window usage efficient.

## SQLite Query Patterns

```bash
# Always use:
sqlite3 ~/brain/data/brain.db "<query>"

# Find knowledge items by topic:
sqlite3 ~/brain/data/brain.db "SELECT title, file_path, summary FROM knowledge_items WHERE category IN ('prd','decisions','domain') AND (title LIKE '%<term>%' OR tags LIKE '%<term>%') LIMIT 10;"

# Find open Jira tickets for a feature:
sqlite3 ~/brain/data/brain.db "SELECT ticket_key, summary, status FROM jira_tickets WHERE status != 'Done' AND (epic_key = '<key>' OR summary LIKE '%<term>%');"

# List all stakeholder files:
sqlite3 ~/brain/data/brain.db "SELECT name, role, team, file_path FROM stakeholders;"

# Check what was indexed this week:
sqlite3 ~/brain/data/brain.db "SELECT title, category FROM knowledge_items WHERE indexed_at >= date('now', '-7 days') ORDER BY indexed_at DESC;"

# List 1:1s for a stakeholder:
sqlite3 ~/brain/data/brain.db "SELECT o.date, o.summary, o.action_items FROM one_on_ones o JOIN stakeholders s ON o.stakeholder_id = s.id WHERE s.name LIKE '%<name>%' ORDER BY o.date DESC;"

# List daily journal entries this week:
sqlite3 ~/brain/data/brain.db "SELECT date, summary FROM daily_summaries WHERE date >= date('now', '-7 days') ORDER BY date DESC;"
```

## MCP Tools Available

### Atlassian (Jira + Confluence)
- `mcp__atlassian__jira_search` — JQL queries
- `mcp__atlassian__jira_get_issue` — full ticket detail
- `mcp__atlassian__jira_get_sprint_issues` — all issues in a sprint
- `mcp__atlassian__jira_get_sprints_from_board` — list sprints
- `mcp__atlassian__jira_get_transitions` — available status transitions
- `mcp__atlassian__jira_transition_issue` — change ticket status
- `mcp__atlassian__jira_add_comment` — add comment to ticket
- `mcp__atlassian__confluence_search` — CQL search
- `mcp__atlassian__confluence_get_page` — full page content

### GitHub
- `mcp__github__list_pull_requests` — list open PRs
- `mcp__github__create_pull_request` — create PR
- `mcp__github__get_commit` — commit detail
- `mcp__github__search_pull_requests` — search PRs

## Invariants

1. **Markdown is truth.** SQLite is the query index. Never delete markdown files — update them.
2. **Every knowledge item must have YAML frontmatter** with at minimum: title, category, tags, created, updated.
3. **Jira tickets → knowledge/jira/{KEY}.md. Confluence pages → knowledge/confluence/{page_id}.md.**
4. **Skills always check the brain before starting dev or product work.** Query SQLite first; read only matching files.
5. **Retros are written weekly** to knowledge/retros/YYYY-WW.md.
6. **When classification is uncertain (< 70% confidence), use scratch/.** Sorter will reclassify on request.
