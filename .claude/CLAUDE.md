# Brain System — CLAUDE.md

> Single source of truth for ~/pm/brain/. All agents and skills read this file.

## Identity

- **Name:** Abhishek Shah
- **Role:** Product Manager (PM-first; engineering work is secondary context), Workforce Management (WFM) team, Blinkhealth
- **Jira workspace:** blinkhealth.atlassian.net
- **GitHub org:** github.com/blinkhealth
- **Active projects:** task-assignment-service, rx-os-backend, rx-os-frontend, wfm-microfrontends, ui-tools
- **Project root:** ~/Documents/blinkhealth/

## What This System Is

~/pm/brain/ is a Personal Knowledge Accelerator — a second brain that combines:
1. **Knowledge management** (PKA-style): raw inputs → structured markdown → SQLite index
2. **PM + dev workflow skills** (gstack-style): slash commands that check the brain before any product or dev work

The result: every planning, discovery, PRD, story, review, ship, and investigate action is informed by accumulated product context, PM frameworks, Jira state, Confluence docs, and past decisions.

## Knowledge Base

- **Root:** ~/pm/brain/knowledge/
- **SQLite index:** ~/pm/brain/data/brain.db
- **Inbox (unprocessed):** ~/pm/brain/inbox/

### Taxonomy

| Category | Path | What goes here |
|---|---|---|
| `prd` | knowledge/prd/ | PRDs, user stories, acceptance criteria, launch checklists |
| `decisions` | knowledge/decisions/ | ADRs, product decisions, tradeoff docs, meeting decisions with rationale |
| `stakeholders` | knowledge/stakeholders/ | One file per person/team: role, preferences, priorities, communication style |
| `jira` | knowledge/jira/ | Ticket snapshots synced by Scout — filename: `{KEY}.md` (e.g. WFM-1234.md) |
| `confluence` | knowledge/confluence/ | Page snapshots synced by Scout — filename: `{page_id}.md` |
| `features` | knowledge/features/ | Feature briefs at various stages: discovery → design → dev → shipped |
| `domain` | knowledge/domain/ | WFM/pharmacy domain knowledge, SLA concepts, business glossary |
| `oncall` | knowledge/oncall/ | Incident postmortems, runbooks, alert context |
| `wins` | knowledge/wins/ | Work accomplishments and impact records — auto-captured by hooks + nightly enricher. Digests in knowledge/wins/digests/ |
| `scratch` | knowledge/scratch/ | Unclassified/working notes; reclassify later with Sorter |

### Naming Conventions

- Dated artifacts: `YYYY-MM-DD-<slug>.md` (e.g. `2026-03-30-wfm-shift-summary-prd.md`)
- Reference/evergreen content: `<slug>.md` (e.g. `task-assignment-sla.md`)
- Jira tickets: `{KEY}.md` (e.g. `WFM-1234.md`)
- Confluence pages: `{page_id}.md` (e.g. `123456789.md`)

### Required Frontmatter (every knowledge item)

```yaml
---
title: <title>
category: prd|decisions|stakeholders|jira|confluence|features|domain|oncall|wins|scratch
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
| `/brain-discovery` | "run discovery on X", "help me frame the problem", "do discovery for WFM-1234", "I don't want to jump to a solution" |
| `/brain-plan` | "plan a feature", "write a PRD", "break down a ticket", "design X" |
| `/brain-prd` | "write a PRD", "one-pager for X", "product spec", "requirements doc" |
| `/brain-user-story` | "write a user story", "create a story", "create a ticket for X" |
| `/brain-review` | "review my code", "check my changes", "review before commit" |
| `/brain-ship` | "ship this", "commit and push", "create a PR", "deploy to review" |
| `/brain-investigate` | "debug this", "root cause this", "investigate WFM-1234", "why is X failing" |
| `/brain-sync` | "sync Jira", "pull my tickets", "sync sprint", "sync WFM-1234" |
| `/ops-feedback` | "ops feedback", "ops wants X", "feature request from ops", paste ops Slack |
| `/ops-bug` | "ops bug", "ops reported X is broken", paste ops Slack describing broken behavior |
| `/brain-weekly-email` | "write the weekly email", "weekly status", "draft email for VP", "Friday email" |
| `/brain-decision` | "log a decision", "we decided X", "document this tradeoff", "record the rationale" — captures decision, alternatives, rationale, tradeoffs, revisit trigger |
| `/wins` | "log a win", "capture this", "add a win", or pass a Jira key — manual capture for work not auto-detected by hooks |
| `/wins-digest` | "review my wins", "prep for review", "quarterly digest", "promo case", "monthly summary" — accepts scope: weekly/monthly/quarterly/promo |

**Skills always check the brain before starting product or dev work.** They query SQLite for relevant context, then load only the matching markdown files — keeping context window usage efficient.

## Engineering Skills (via blink-ai-tools)

These skills are synced from `~/pm/blink-ai-tools/` into `~/.claude/commands/` on session start. Do not re-implement them in brain.

| Skill | When to use |
|---|---|
| `/eng-workflow` | Any non-trivial feature implementation — 7-phase workflow with plan gate and SP-based depth selection |
| `/ai-retro` | After a ticket is delivered — produces SP Evaluation Report with scope analysis and effort calibration |
| `/eng-scorecard` | Score tickets from retro files → `output/baseline_scorecard.csv` |
| `/pr-review` | After pushing a branch — creates pending GitHub draft review with inline comments |
| `/jira-status-update` | Add a structured living status comment (phase checklist + PR link + evidence) to a Jira ticket |
| `/generate-manual` | Auto-generate a user manual via journey-explorer → screenshot-capture → manual-writer pipeline |

**Rule:** If a task is covered by a blink-ai-tools skill, use it. Don't duplicate it here.

**Additional templates** (at `~/.claude/blink-ai-tools/report_templates/`, available after bootstrap):
- `technical_design_document_template.md` — TRD with architecture, ERD, IAM, threat model, cost analysis
- `test_plan_template.md` — QA test plan with scope, entry/exit criteria, risk matrix
- `sprint_report_template.html` — alternate weekly status format (table-based with completion %)

## PM Frameworks Reference

PM best practices are stored as domain knowledge and auto-surfaced by skills. Key files:

| File | Contents |
|---|---|
| `knowledge/domain/pm-frameworks-overview.md` | When-to-use index for all PM frameworks |
| `knowledge/domain/opportunity-solution-tree.md` | Teresa Torres OST — used by brain-discovery, brain-plan |
| `knowledge/domain/jobs-to-be-done.md` | JTBD framework — used by brain-discovery, brain-user-story |
| `knowledge/domain/problem-framing.md` | MITRE canvas + problem statement — used by brain-discovery, brain-plan, brain-prd |
| `knowledge/domain/user-story-best-practices.md` | Story anatomy, INVEST, 9 splitting patterns, epic hypothesis |
| `knowledge/domain/prioritization-frameworks.md` | RICE, ICE, Kano, MoSCoW, Cost of Delay |
| `knowledge/domain/product-strategy-frameworks.md` | Geoffrey Moore positioning, Working Backwards, Lean UX Canvas |
| `knowledge/domain/customer-discovery-frameworks.md` | Proto-persona, CJM, Mom Test interviews |
| `knowledge/domain/feature-investment-framework.md` | Build/don't-build ROI framework |

**Rule:** Before starting any product work, check the relevant domain knowledge file. These are the standing best practices for the PM role.

## SQLite Query Patterns

```bash
# Always use:
sqlite3 ~/pm/brain/data/brain.db "<query>"

# Find knowledge items by topic:
sqlite3 ~/pm/brain/data/brain.db "SELECT title, file_path, summary FROM knowledge_items WHERE category IN ('prd','decisions','domain') AND (title LIKE '%<term>%' OR tags LIKE '%<term>%') LIMIT 10;"

# Find open Jira tickets for a feature:
sqlite3 ~/pm/brain/data/brain.db "SELECT ticket_key, summary, status FROM jira_tickets WHERE status != 'Done' AND (epic_key = '<key>' OR summary LIKE '%<term>%');"

# List all stakeholder files:
sqlite3 ~/pm/brain/data/brain.db "SELECT name, role, team, file_path FROM stakeholders;"

# Check what was indexed this week:
sqlite3 ~/pm/brain/data/brain.db "SELECT title, category FROM knowledge_items WHERE indexed_at >= date('now', '-7 days') ORDER BY indexed_at DESC;"

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
5. **Wins are captured automatically.** PostToolUse hooks fire on Jira transitions and GitHub PR events → pending.jsonl. Nightly cron enriches into structured win files. Never manually log something the hooks already captured.
6. **Jira syncs automatically every morning at 6:53am.** knowledge/jira/ and brain.db stay fresh without manual /brain-sync runs. Run /brain-sync manually only for specific tickets or Confluence pages.
6. **When classification is uncertain (< 70% confidence), use scratch/.** Sorter will reclassify on request.
