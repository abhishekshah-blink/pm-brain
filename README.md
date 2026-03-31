# pm-brain

> A second brain for product managers who build — powered by Claude Code.

Most PMs carry too much in their heads: what was decided last sprint, what ops reported on Slack, what the acceptance criteria were for that ticket three weeks ago. pm-brain captures all of it, organizes it automatically, and surfaces it the moment you need it — whether you're writing a PRD, shipping code, or compiling the Friday status email.

It runs entirely inside [Claude Code](https://claude.ai/code). No new app. No extra subscription. Just slash commands you type, and agents that do the work.

---

## What it does

**Builds a knowledge base from everything you encounter at work.**
Jira tickets, Confluence pages, ops Slack messages, incident reports, meeting notes — organized into clean markdown files with a searchable database behind it. A filing system that files itself.

**Gives you 13 slash commands grounded in that context.**
When you run `/brain-plan`, it doesn't just help you plan — it first reads your existing PRDs, pulls the relevant Jira tickets live, checks your past decisions, and *then* writes the plan. Every skill is grounded in what you actually know.

**And silently records everything you ship.**
Every Jira transition, every GitHub PR, every bug triaged — captured automatically in the background, enriched by Claude overnight, ready for review season. When it's time for your performance review or promo case, the evidence is already there.

---

## Automatic wins tracking

The hardest part of performance reviews is remembering what you did six months ago. pm-brain solves this without any extra effort.

### How it works

```
You ship code or close a ticket
        │
        ▼
┌─────────────────────────────────────────────┐
│  Hook fires instantly (no Claude needed)    │
│  Jira transition, GitHub PR, ticket create  │
│  → appends raw signal to wins/pending.jsonl │
└─────────────────────────────────────────────┘
        │
        ▼  (every night at 10:37pm)
┌─────────────────────────────────────────────┐
│  Nightly cron enriches the queue            │
│  Claude pulls Jira context, writes:         │
│  • what you did                             │
│  • why it mattered                          │
│  • review-ready bullet                      │
│  • resume bullet                            │
│  • missing evidence flag                    │
│  → saves to knowledge/wins/                 │
└─────────────────────────────────────────────┘
        │
        ▼  (every Friday at 6:43pm)
┌─────────────────────────────────────────────┐
│  Weekly digest auto-generated               │
│  Top wins, theme breakdown, evidence gaps   │
│  → saved to knowledge/wins/digests/         │
└─────────────────────────────────────────────┘
```

**What gets captured automatically:**
- Every GitHub PR you create or merge
- Every Jira ticket you transition (In Review, Done, Closed)
- Every Jira ticket created via `/ops-feedback` or `/ops-bug`
- Every shipment via `/brain-ship`

**For things that never touch Jira or GitHub** (a key conversation, a process you improved, a decision you drove): `/wins "what you did"` in under 30 seconds.

**When review season arrives:**
```
/wins-digest quarterly    → full self-review draft, bullets by competency, manager talking points
/wins-digest promo        → promotion case narrative, strongest examples, gaps to close
```

---

## The 13 skills

### Product work

| Skill | What it does |
|---|---|
| `/brain-discovery` | Frame a problem before jumping to solutions — customer discovery, JTBD, and opportunity mapping |
| `/brain-plan` | Plan a feature end-to-end — loads existing PRDs, live Jira tickets, Confluence docs, and past decisions |
| `/brain-prd` | Write a PRD or one-pager — concise one-pager for small features, full spec for major initiatives |
| `/brain-user-story` | Turn a feature idea into a Jira story with acceptance criteria — creates the actual ticket |
| `/ops-feedback` | Paste a Slack message from ops — reads the codebase, checks prior work, creates a structured Jira story |
| `/ops-bug` | Paste a bug report from ops — investigates the code path, assesses severity, creates a Jira bug ticket |
| `/brain-weekly-email` | Compile the Friday VP status email — pulls Jira sprint data and formats your team's weekly update |

### Dev workflow

| Skill | What it does |
|---|---|
| `/brain-review` | Code review before committing — checks project coding standards and the linked ticket's acceptance criteria |
| `/brain-ship` | Full ship pipeline — tests → lint → review → commit → push → GitHub PR → Jira transition |
| `/brain-investigate` | Root cause analysis — searches the codebase, checks past incidents, produces a hypothesis and proposed fix |
| `/brain-sync` | Pull Jira and Confluence into your knowledge base — syncs your sprint, a specific ticket, or a page |

### Wins tracking

| Skill | What it does |
|---|---|
| `/wins` | Manually capture a win not auto-detected — accepts a raw note or a Jira key |
| `/wins-digest` | Synthesize accumulated wins — pass `weekly`, `monthly`, `quarterly`, or `promo` as the scope |

---

## How it works

### Three agents behind the scenes

**Sorter** is the orchestrator. Drop any file in `~/brain/inbox/` and Sorter reads it, figures out what kind of document it is, and routes it to the right folder. Confident (≥70%)? Precise routing. Unsure? Puts it in `scratch/` and flags it. Cleans up the inbox after filing.

**Keeper** is the librarian. Every time something needs to be written — a PRD, a synced ticket, an incident note, an enriched win — Keeper does the writing. Adds consistent metadata, indexes everything in the SQLite database, and links related items together.

**Scout** connects to Jira, Confluence, and GitHub. Run `/brain-sync sprint` and Scout pulls your entire current sprint — all tickets, descriptions, acceptance criteria, comments — and saves them as searchable markdown files. Skills call Scout automatically when they need live data.

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
├── domain/         ← Domain knowledge and PM frameworks
├── oncall/         ← Incident notes and runbooks
├── wins/           ← Auto-captured accomplishment records (enriched nightly)
│   └── digests/    ← Weekly and quarterly synthesized summaries
└── scratch/        ← Unclassified notes (Sorter will reclassify)
```

Every file has structured metadata:

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

The SQLite database at `data/brain.db` indexes all of these so skills can search across thousands of notes instantly. The database is a query layer — the markdown files are the source of truth, and they're all yours.

> Your knowledge base is gitignored. It stays on your machine and is never published anywhere.

---

### Where each skill saves its output

| Skill | Output |
|---|---|
| `/brain-discovery` | Conversation + optionally `knowledge/features/` |
| `/brain-plan` | `knowledge/features/` + conversation |
| `/brain-prd` | `knowledge/prd/` + optionally Confluence |
| `/brain-user-story` | Jira ticket (created) + `knowledge/features/` |
| `/ops-feedback` | Jira ticket (created) + `knowledge/features/` |
| `/ops-bug` | Jira ticket (created) + optionally `knowledge/oncall/` |
| `/brain-review` | Conversation — confidence-scored issues grouped by severity |
| `/brain-ship` | GitHub PR (created) + Jira status updated |
| `/brain-investigate` | Conversation + optionally `knowledge/oncall/` |
| `/brain-weekly-email` | Conversation — ready to copy and send |
| `/brain-sync` | `knowledge/jira/` and `knowledge/confluence/` |
| `/wins` | `knowledge/wins/YYYY-MM-DD-slug.md` |
| `/wins-digest` | `knowledge/wins/digests/` + conversation |

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
```

**2. Tell it who you are**

Edit `~/brain/.claude/CLAUDE.md` and update the identity section at the top:
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

**4. Run setup**
```bash
bash ~/brain/scripts/setup.sh
```

Creates all knowledge folders, initializes the SQLite database, and symlinks all 13 skills into Claude Code so they appear as slash commands.

**5. Enable automatic wins tracking**

Add the PostToolUse hook to `~/.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "mcp__atlassian__jira_transition_issue|mcp__atlassian__jira_create_issue|mcp__github__create_pull_request|mcp__github__merge_pull_request",
        "hooks": [{ "type": "command", "command": "python3 ~/brain/scripts/wins-hook.py" }]
      }
    ]
  }
}
```

Install the cron jobs (nightly enrichment + weekly digest):
```bash
(crontab -l 2>/dev/null; cat <<'EOF'
# Brain wins enrichment — nightly at 10:37pm
37 22 * * * /bin/bash -l ~/brain/scripts/wins-enrich-cron.sh
# Brain wins weekly digest — Fridays at 6:43pm
43 18 * * 5 /bin/bash -l ~/brain/scripts/wins-digest-cron.sh
EOF
) | crontab -
```

**6. Add your weekly email template** *(optional)*

If your team has a standard status email format, drop it as HTML at:
`~/brain/.claude/skills/brain-weekly-email/references/email-template.html`

**7. First run**
```bash
/brain-sync sprint     # pull your current Jira sprint
/brain-plan            # plan something with live context
```

---

## Credits

**[PKA (Personal Knowledge Assistance)](https://github.com/nir-sheep/pka)** by **Nir Sheep** — the pattern of building a second brain with AI agents: a filing inbox, specialist agents that classify and index, and a clean taxonomy of knowledge categories.

**[gstack](https://github.com/garrytan/gstack)** by **Garry Tan** (President & CEO of Y Combinator) — the pattern of writing slash-command skills as plain markdown files that Claude Code reads and executes. The PREAMBLE system, voice directives, completion protocol, and fix-first heuristic are all adapted from gstack.

What pm-brain adds on top: **MCP-native live data** (Scout pulls Jira and Confluence directly instead of manual file drops) and **automatic wins tracking** (hooks + nightly cron so your accomplishment record builds itself).

---

*Built with Claude Code. Your knowledge stays on your machine.*
