# pm-brain

> A second brain for product managers who build — powered by Claude Code.

Most PMs carry too much in their heads: what was decided last sprint, what ops reported on Slack, what the acceptance criteria were for that ticket three weeks ago. **pm-brain captures all of it, organizes it automatically, and surfaces it the moment you need it** — whether you're writing a PRD, shipping code, or drafting the Friday status email.

It runs entirely inside [Claude Code](https://claude.ai/code). No new app. No extra subscription. Just slash commands you already know how to type.

---

## What it does

pm-brain does two things:

**Builds a knowledge base from everything you encounter at work.**
Jira tickets, Confluence pages, ops Slack messages, meeting notes, incident reports — all of it gets organized into a folder of clean markdown files, with a searchable database behind it. A filing system that files itself.

**Gives you 11 slash commands that use that knowledge to do PM and dev work.**
When you run `/brain-plan`, it doesn't just help you plan — it first reads your existing PRDs, pulls the relevant Jira tickets live, checks your past decisions, and *then* writes the plan. Every skill is grounded in what you actually know.

---

## The 11 skills

### Product work

| Skill | What it does |
|---|---|
| `/brain-discovery` | Frame a problem before jumping to solutions — runs customer discovery, JTBD, and opportunity mapping |
| `/brain-plan` | Plan a feature end-to-end — loads existing PRDs, live Jira tickets, Confluence docs, and past decisions before writing anything |
| `/brain-prd` | Write a PRD or one-pager — two formats: a concise one-pager for small features, full spec for major initiatives |
| `/brain-user-story` | Turn a feature idea into a Jira story — writes the story, acceptance criteria, and creates the actual ticket |
| `/brain-ops-feedback` | Paste a Slack message from ops — reads the codebase, checks prior work, creates a structured Jira story |
| `/brain-ops-bug` | Paste a bug report from ops — investigates the code path, assesses severity, creates a Jira bug ticket |
| `/brain-weekly-email` | Compile the Friday VP status email — pulls Jira sprint data and formats your team's weekly update |

### Dev workflow

| Skill | What it does |
|---|---|
| `/brain-review` | Code review before committing — checks your project's coding standards and the linked ticket's acceptance criteria |
| `/brain-ship` | Full ship pipeline — tests → lint → review → commit → push → GitHub PR → Jira transition, in one command |
| `/brain-investigate` | Root cause analysis — searches the codebase, checks past incidents, produces a hypothesis with evidence and a proposed fix |
| `/brain-sync` | Pull Jira and Confluence into your knowledge base — syncs your sprint, a specific ticket, or a Confluence page |

---

## How it works

### Three agents run behind the scenes

You don't manage these agents — they work automatically when you use skills or drop files in the inbox.

**Sorter** is the orchestrator. Drop any file in `~/brain/inbox/` and Sorter reads it, figures out what kind of document it is, and sends it to the right folder. Confident (≥70%)? It routes it precisely. Unsure? It puts it in `scratch/` and flags it for you. After filing, it cleans up the inbox.

**Keeper** is the librarian. Every time something needs to be written to the knowledge base — a new PRD, a synced Jira ticket, an incident note — Keeper does the writing. It adds consistent metadata, indexes everything in the SQLite database, and links related items together. When skills need context, they ask Keeper.

**Scout** connects to Jira, Confluence, and GitHub. Instead of copy-pasting from Jira, Scout fetches it for you. Run `/brain-sync sprint` and Scout pulls your entire current sprint — all tickets, descriptions, acceptance criteria, comments — and saves them as searchable markdown files.

---

### The knowledge base

Everything lives in `~/brain/knowledge/` as plain markdown files:

```
knowledge/
├── prd/            ← PRDs, one-pagers, acceptance criteria
├── decisions/      ← Every decision made, with date and rationale
├── features/       ← Feature briefs and plans
├── stakeholders/   ← One file per person or team
├── jira/           ← Live Jira ticket snapshots (synced by Scout)
├── confluence/     ← Live Confluence page snapshots (synced by Scout)
├── domain/         ← Domain knowledge and business glossary
├── oncall/         ← Incident notes and runbooks
└── scratch/        ← Unclassified notes (Sorter will reclassify)
```

Every file has structured metadata at the top:

```yaml
---
title: Feature Plan: Shift Summary View
category: features
tags: [scheduling, wfm, v2]
created: 2026-03-30
updated: 2026-03-30
jira_tickets: [WFM-1234]
---
```

The SQLite database at `data/brain.db` indexes all of these files so skills can search across thousands of notes instantly without reading every file. The database is a query layer — the markdown files are what actually matter, and they're all yours.

> Your knowledge base is gitignored. It stays on your machine and is never published anywhere.

---

### Where each skill saves its output

| Skill | Where the output goes |
|---|---|
| `/brain-discovery` | Conversation + optionally `knowledge/features/` |
| `/brain-plan` | `knowledge/features/` + conversation |
| `/brain-prd` | `knowledge/prd/` + optionally Confluence |
| `/brain-user-story` | Jira (ticket created) + `knowledge/features/` |
| `/brain-ops-feedback` | Jira (ticket created) + `knowledge/features/` |
| `/brain-ops-bug` | Jira (ticket created) + optionally `knowledge/oncall/` |
| `/brain-review` | Conversation (confidence-scored issues, grouped by severity) |
| `/brain-ship` | GitHub PR + Jira status updated + conversation |
| `/brain-investigate` | Conversation + optionally `knowledge/oncall/` |
| `/brain-weekly-email` | Conversation (ready to copy) |
| `/brain-sync` | `knowledge/jira/` and `knowledge/confluence/` |

---

## Prerequisites

- [Claude Code](https://claude.ai/code) (CLI or desktop app)
- [Atlassian MCP](https://github.com/sooperset/mcp-atlassian) — connects Claude to your Jira and Confluence
- [GitHub MCP](https://github.com/github/github-mcp-server) — connects Claude to your GitHub org
- `sqlite3` in your shell (`brew install sqlite` on macOS)

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/abhishekshah-blink/pm-brain ~/brain
cd ~/brain
```

**2. Tell it who you are**

Edit `~/brain/.claude/CLAUDE.md` and fill in your details at the top:
- Your name and role
- Your Jira workspace URL (e.g. `yourcompany.atlassian.net`)
- Your GitHub org
- Your active projects and where they live on your machine

**3. Configure your MCPs**

In `~/.claude/mcp.json`:
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

**4. Add your weekly email template** *(optional)*

If your team has a standard status email format, drop it as HTML at:
`~/brain/.claude/skills/brain-weekly-email/references/email-template.html`

**5. Run setup**
```bash
bash ~/brain/scripts/setup.sh
```

This creates all the knowledge folders, initializes the SQLite database, and symlinks all 11 skills into Claude Code so they show up as `/brain-*` commands.

**6. First run**
```bash
/brain-sync sprint     # pull your current Jira sprint into the knowledge base
/brain-plan            # plan something — it will now have live context
```

---

## Credits

This system combines two ideas:

**[PKA (Personal Knowledge Assistance)](https://github.com/nir-sheep/pka)** by **Nir Sheep** — the pattern of building a second brain with AI agents: an inbox, specialist agents that classify and index, and a clean taxonomy of knowledge categories. PKA showed that "drop files in, get organized knowledge out" is a genuinely powerful workflow.

**[gstack](https://github.com/garrytan/gstack)** by **Garry Tan** (President & CEO of Y Combinator) — the pattern of writing slash-command skills as plain markdown files that Claude Code reads and executes. The PREAMBLE system, voice directives, completion protocol, and fix-first heuristic are all adapted from gstack.

What pm-brain adds: **MCP-native live data.** Instead of manually dropping Jira tickets into an inbox, Scout pulls them directly from Jira and Confluence via MCP. The knowledge base stays current automatically, and every skill uses live data rather than stale copies.

---

*Built with Claude Code. Your knowledge stays on your machine.*
