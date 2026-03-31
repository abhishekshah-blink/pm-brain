# pm-brain

**A second brain for product managers who build.**

pm-brain is a personal knowledge + dev workflow system that runs entirely inside [Claude Code](https://claude.ai/code). It combines two proven AI-agent patterns:

- **PKA-style knowledge management** — raw inputs (Jira tickets, Confluence pages, meeting notes, PDFs) become structured, searchable markdown files indexed in SQLite
- **gstack-style slash commands** — 11 skills that make Claude Code a PM's dev workflow co-pilot

The result: every planning session, code review, bug triage, and weekly email is informed by accumulated product context. The system learns as you work.

---

## What it does

```
Drop ops Slack message         →  /brain-ops-feedback   →  Jira story ticket, ready to assign
Paste a bug report from ops    →  /brain-ops-bug         →  Jira bug ticket + root cause investigation
Start a new feature            →  /brain-plan            →  PRD grounded in existing decisions + live Jira
End of day Friday              →  /brain-weekly-email    →  VP status email, auto-filled from Jira sprint data
Need a user story              →  /brain-user-story      →  Full AS A / I WANT / SO THAT + AC + story points in Jira
Staged code changes            →  /brain-review          →  Code review using ticket AC + your team's checklist
Ready to ship                  →  /brain-ship            →  Tests → lint → commit → push → PR → Jira transition
Something is broken            →  /brain-investigate     →  Root cause analysis with past incident context
End of week                    →  /brain-retro           →  Sprint retrospective from git log + Jira + brain
Jira / Confluence out of sync  →  /brain-sync            →  Pull live tickets + pages into knowledge base
```

---

## Architecture

```
~/brain/
├── .claude/
│   ├── CLAUDE.md              ← Single source of truth. Identity, taxonomy, MCP tools, invariants.
│   ├── PREAMBLE.md            ← Cross-cutting standards injected into every skill at runtime.
│   ├── agents/
│   │   ├── roni.md            ← Orchestrator: processes inbox, delegates to Nova + Spark
│   │   ├── nova.md            ← Knowledge librarian: writes + indexes markdown, answers lookups
│   │   └── spark.md           ← MCP sync agent: pulls Jira, Confluence, GitHub into knowledge base
│   └── skills/
│       ├── brain-plan/        ← /brain-plan
│       ├── brain-review/      ← /brain-review
│       ├── brain-ship/        ← /brain-ship
│       ├── brain-investigate/ ← /brain-investigate
│       ├── brain-retro/       ← /brain-retro
│       ├── brain-sync/        ← /brain-sync
│       ├── brain-ops-feedback/← /brain-ops-feedback
│       ├── brain-ops-bug/     ← /brain-ops-bug
│       ├── brain-weekly-email/← /brain-weekly-email
│       ├── brain-user-story/  ← /brain-user-story
│       └── brain-prd/        ← /brain-prd
├── knowledge/                 ← Your structured markdown knowledge base (gitignored)
│   ├── prd/                   ← Product requirements docs
│   ├── decisions/             ← ADRs, product decisions, tradeoff docs
│   ├── stakeholders/          ← People profiles
│   ├── jira/                  ← Live ticket snapshots synced by Spark
│   ├── confluence/            ← Live page snapshots synced by Spark
│   ├── features/              ← Feature briefs at various stages
│   ├── retros/                ← Weekly retrospectives
│   ├── domain/                ← Domain knowledge and business glossary
│   ├── oncall/                ← Incident postmortems and runbooks
│   ├── daily-journals/        ← Daily meeting notes and standups
│   ├── business-reviews/      ← Weekly/monthly business reviews
│   ├── ai-strategy/           ← AI adoption plans and frameworks
│   ├── coaching-sessions/     ← Coaching notes and feedback
│   ├── operating-plans/       ← Quarterly/annual plans and roadmaps
│   └── scratch/               ← Unclassified working notes
├── inbox/                     ← Drop raw files here; Roni classifies them
├── data/brain.db              ← SQLite index (gitignored)
└── scripts/setup.sh           ← Idempotent setup script
```

**Markdown is truth. SQLite is the query layer.** Skills query SQLite to find relevant files, read only those, then write new markdown entries when they produce artifacts. Nothing is ever deleted — only updated.

---

## How skills work

Skills are Markdown files with YAML frontmatter. Claude Code reads `SKILL.md` when you type `/brain-plan` and executes the workflow instructions inside it. No binaries. No build step. No runtime dependencies beyond Claude Code itself.

Every skill:
1. Reads `PREAMBLE.md` — voice, completion protocol, AskUserQuestion format, Fix-First heuristic, error escalation
2. Reads `CLAUDE.md` — your identity, active projects, knowledge taxonomy, MCP tools
3. Runs its workflow (which may query SQLite, call Jira/GitHub MCP, read codebase files)
4. Writes output to `knowledge/` and updates `brain.db`
5. Ends with a status: **DONE** / **DONE_WITH_CONCERNS** / **BLOCKED** / **NEEDS_CONTEXT**

Skills use the Atlassian MCP and GitHub MCP for live data — no copy-pasting from Jira.

---

## Three agents

| Agent | What they do |
|---|---|
| **Roni** | Orchestrator. Reads `inbox/`, classifies each file into the right knowledge category (≥70% confidence threshold), delegates writing to Nova. Below threshold → `scratch/` with a flag. |
| **Nova** | Knowledge librarian. Writes structured markdown with YAML frontmatter. Upserts into SQLite. Handles lookup queries from skills — "find everything we know about X". |
| **Spark** | MCP sync agent. Pulls live Jira tickets, Confluence pages, and GitHub PRs into `knowledge/`. Updates `brain.db`. Surfaces what changed since the last sync. |

---

## What makes this different from standard Claude Code

| Standard Claude Code | pm-brain |
|---|---|
| Answers questions in context | Every answer is grounded in your accumulated product knowledge |
| Reviews code generically | Reviews against your ticket's acceptance criteria + your team's specific checklist |
| Plans features from scratch | Plans features by first loading existing PRDs, decisions, domain knowledge, and live Jira data |
| No memory between sessions | SQLite index persists and grows — context compounds over time |
| Manual Jira updates | `/brain-ship` transitions your Jira ticket to "In Review" automatically |
| Write the weekly email manually | `/brain-weekly-email` pulls the sprint data and fills your template |

---

## Prerequisites

- [Claude Code](https://claude.ai/code) (CLI or desktop app)
- [Atlassian MCP](https://github.com/sooperset/mcp-atlassian) configured for your Jira + Confluence workspace
- [GitHub MCP](https://github.com/github/github-mcp-server) configured for your GitHub org
- `sqlite3` available in your shell (`brew install sqlite` on macOS)

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/abhishekshah-blink/pm-brain ~/brain
cd ~/brain
```

### 2. Customize for your company

Edit `~/brain/.claude/CLAUDE.md` and replace all `[placeholder]` values:

```yaml
# Your identity
Name:       [Your Name]
Role:       Product Manager, [Your Team], [Your Company]
Jira:       your-workspace.atlassian.net
GitHub org: github.com/your-org
Projects:   your-service-1, your-service-2, ...
Project root: ~/Documents/your-company/
```

Also update the service → Jira project mappings in `brain-review/SKILL.md`, `brain-ship/SKILL.md`, and `brain-ops-feedback/SKILL.md` to match your actual services.

### 3. Add your weekly email template

If your team has a weekly status email format, add it as HTML to:
```
~/brain/.claude/skills/brain-weekly-email/references/email-template.html
```
The skill will fill in the live Jira data automatically each Friday.

### 4. Configure your MCPs

In `~/.claude/mcp.json`, ensure you have:
```json
{
  "mcpServers": {
    "atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian", "--toolsets", "jira_issues,jira_comments,jira_transitions,jira_projects,jira_agile,confluence_pages"]
    },
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"]
    }
  }
}
```

### 5. Run setup

```bash
bash ~/brain/scripts/setup.sh
```

This creates the full directory structure, initializes the SQLite schema, and symlinks all 11 skills into `~/.claude/skills/` where Claude Code discovers them.

### 6. Start using it

Open Claude Code from `~/brain/` and run:

```
/brain-sync sprint        — pull your current sprint from Jira
/brain-retro              — generate your first weekly retrospective
```

From any project directory:
```
/brain-plan "feature name"  — plan with full context
/brain-review               — review your staged changes
```

---

## Inspiration

This system combines two ideas:

- **[PKA](https://github.com/garrytan/gstack)** — the "personal knowledge assistance" pattern: raw inputs → structured markdown → SQLite index. Agents as specialists behind a single orchestrator.
- **[gstack](https://github.com/garrytan/gstack)** by Garry Tan — the skill system: markdown prompt templates as slash commands, the PREAMBLE pattern for cross-cutting standards, voice directive, completion protocol.

The key addition on top of both: **MCP-native live data**. Rather than manually dropping files into an inbox, the `brain-sync` skill and Spark agent pull directly from Jira and Confluence via the Atlassian MCP. The knowledge base stays current without manual effort.

---

## Skill reference

| Skill | Trigger | What it does |
|---|---|---|
| `/brain-plan` | "plan a feature", "break down a ticket" | Loads brain context + live Jira + Confluence, produces structured feature plan |
| `/brain-review` | "review my code", "check my diff" | Project-aware review using ticket AC + team checklist |
| `/brain-ship` | "ship this", "create a PR" | Tests → lint → review → commit → push → PR → Jira transition |
| `/brain-investigate` | "debug this", "root cause WFM-1234" | Root cause analysis with past incident context from knowledge base |
| `/brain-retro` | "weekly retro", "summarize my week" | Retrospective from git log + Jira sprint + new knowledge items |
| `/brain-sync` | "sync Jira", "sync sprint" | Pulls Jira tickets + Confluence pages + GitHub PRs into knowledge base |
| `/brain-ops-feedback` | "ops feedback", paste Slack | Ops feature request → codebase search → Jira story ticket |
| `/brain-ops-bug` | "ops bug", paste Slack | Ops bug report → investigation → severity assessment → Jira bug ticket |
| `/brain-weekly-email` | "weekly email", "Friday email" | Fills weekly VP status email from sprint data + decisions + activity log |
| `/brain-user-story` | "write a story", "create a ticket" | Full user story (AS A / I WANT / SO THAT + AC + estimates) in Jira |
| `/brain-prd` | "write a PRD", "one-pager for X" | One-pager or full PRD, saved to knowledge/prd/ + optional Confluence page |

---

## Knowledge base

All knowledge lives in `~/brain/knowledge/` as plain markdown files — gitignored since it's personal data. The SQLite database at `data/brain.db` is a query index over these files. Skills query SQLite first (fast), then read only the matching files (efficient).

Every knowledge item has YAML frontmatter:
```yaml
---
title: Feature Plan: Shift Summary
category: features
tags: [wfm, scheduling, v2]
created: 2026-03-30
updated: 2026-03-30
jira_tickets: [WFM-1234]
confluence_pages: []
stakeholders: [eng-lead]
---
```

Ask Nova to look things up: *"Nova, find everything we know about task SLA"*

---

Built with Claude Code. Inspired by PKA and gstack.
