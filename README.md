# pm-brain

**A second brain for product managers who build — powered by Claude Code.**

Most PMs carry too much in their heads: what was decided last sprint, what ops said on Slack, what the acceptance criteria were for that ticket three weeks ago. pm-brain captures all of it, organizes it automatically, and makes it available the moment you need it — whether you're writing a PRD, reviewing code, or compiling the Friday status email.

It runs entirely inside [Claude Code](https://claude.ai/code). No new app. No subscription. Just slash commands you type, and agents that do the work.

---

## The big picture

pm-brain does two things:

**1. It builds a knowledge base from everything you encounter at work.**
Meeting notes, Jira tickets, Confluence pages, coaching sessions, business reviews — all of it gets organized into a folder of clean markdown files, with a searchable database behind it. Think of it as a filing system that files itself.

**2. It gives you 11 slash commands that use that knowledge to do PM and dev work.**
When you run `/brain-plan`, it doesn't just help you plan — it first reads your existing PRDs, pulls the relevant Jira tickets live, checks your past decisions, and *then* writes the plan. Every skill is grounded in what you actually know.

---

## Your three agents

pm-brain has three agents running behind the scenes. You don't manage them — they work automatically when you use the skills or drop files in your inbox.

### Sorter — handles what comes in

Sorter watches your `inbox/` folder. Drop any file in there — a PDF, a meeting transcript, a copy-pasted Slack thread, a doc — and Sorter reads it, figures out what type of document it is, and sends it to the right place.

> *"Is this a PRD? A decision? A stakeholder profile? A business review?"*

If Sorter is confident (≥70%), it routes the file to the right knowledge folder. If it's not sure, it puts it in `scratch/` and flags it for you to review. After filing, it deletes the original from your inbox so things stay clean.

**How to use:** Drop a file in `~/brain/inbox/`, then open Claude Code and say *"Sorter, process my inbox."*

---

### Keeper — writes and remembers everything

Keeper is the librarian. Every time something needs to be written to your knowledge base — whether Sorter is filing an inbox document, a skill is saving a new PRD, or Scout is syncing a Jira ticket — Keeper does the actual writing.

Keeper writes clean, structured markdown with consistent formatting, indexes everything in the SQLite database, and links related items together. When skills need context (like "what do we know about the task SLA?"), they ask Keeper, and Keeper searches the database and pulls the relevant files.

**You mostly don't talk to Keeper directly.** Skills and Sorter call Keeper automatically. But you can: *"Keeper, find everything we know about shift scheduling."*

---

### Scout — fetches live data from Jira, Confluence, and GitHub

Scout is your connection to the outside world. Instead of manually copy-pasting from Jira, Scout goes and gets it for you. Run `/brain-sync sprint` and Scout pulls your entire current sprint — all tickets, descriptions, acceptance criteria, comments — and saves them as markdown files in your knowledge base.

Scout also pulls Confluence pages and your open GitHub PRs. After syncing, it tells you what changed since the last sync (tickets that moved, new tickets, updated pages).

**How to use:** Just run a skill — Scout is called automatically. Or ask directly: *"Scout, sync WFM-1234"* or *"Scout, sync my sprint."*

---

## How the inbox works

```
You drop a file into ~/brain/inbox/
         │
         ▼
    ┌─────────────────────────────────────────┐
    │  Sorter reads the file                  │
    │  "What kind of document is this?"       │
    │                                         │
    │  ≥70% confident → routes to category   │
    │  <70% confident → sends to scratch/     │
    └─────────────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────────────┐
    │  Keeper writes the structured version   │
    │  • Adds YAML frontmatter (title, tags,  │
    │    category, date, linked tickets)      │
    │  • Saves to knowledge/<category>/       │
    │  • Indexes in brain.db (SQLite)         │
    └─────────────────────────────────────────┘
         │
         ▼
    Original file deleted from inbox/
    Clean markdown saved to knowledge/
    Searchable in brain.db forever
```

**What can go in the inbox?**
- Meeting notes (paste from Notion, Google Docs, anywhere)
- PDFs (converted to text first)
- Slack threads (copy-paste as text)
- Coaching session notes
- Business review docs
- Anything text-based

---

## Where does the output go?

Different skills produce different outputs. Here's exactly where to find what each skill creates:

| Skill | Output location | What you get |
|---|---|---|
| `/brain-plan` | `knowledge/features/` | Feature plan as a markdown file + shown in conversation |
| `/brain-prd` | `knowledge/prd/` + optionally Confluence | PRD or one-pager, with option to publish to Confluence |
| `/brain-user-story` | Jira (ticket created) + `knowledge/features/` | Live Jira story + local copy |
| `/brain-ops-feedback` | Jira (ticket created) + `knowledge/features/` | Live Jira story with codebase context |
| `/brain-ops-bug` | Jira (ticket created) + optionally `knowledge/oncall/` | Live Jira bug ticket with investigation findings |
| `/brain-review` | Conversation | Confidence-scored issues, grouped Critical / Important |
| `/brain-ship` | GitHub (PR created) + Jira (ticket transitioned) | PR URL + commit SHA + Jira status updated |
| `/brain-investigate` | Conversation + optionally `knowledge/oncall/` | Root cause analysis + option to save as incident note |
| `/brain-retro` | `knowledge/retros/` | Weekly retrospective markdown file |
| `/brain-weekly-email` | `knowledge/retros/` + conversation | Filled HTML email + plain text version to copy |
| `/brain-sync` | `knowledge/jira/`, `knowledge/confluence/` | Ticket and page snapshots, updated database |

**The pattern:** Skills always show you results in the conversation. If they produce a document, they also save it to `knowledge/` automatically. Jira tickets and GitHub PRs are created live via the Atlassian and GitHub integrations.

---

## The 11 skills

### Product work

**`/brain-plan`** — *"Plan a feature" / "Break down this ticket"*
Before writing a single line of the plan, it loads: related PRDs from your knowledge base, live Jira ticket details and acceptance criteria, relevant Confluence design docs, and your past decisions on similar problems. Then writes a structured feature plan with problem statement, acceptance criteria, technical approach, open questions, and suggested Jira sub-tasks.

**`/brain-prd`** — *"Write a PRD" / "One-pager for X"*
Two formats: a one-pager for small features, or a full PRD for major initiatives. Loads all available context first, then produces a complete product spec. Saves to your knowledge base and optionally creates a Confluence page.

**`/brain-user-story`** — *"Write a user story" / "Create a ticket for X"*
Takes a feature description and produces a complete user story — AS A / I WANT / SO THAT, acceptance criteria (Given/When/Then), story point estimate, epic link, and service labels. Creates the actual Jira ticket.

**`/brain-ops-feedback`** — *Paste Slack message from ops*
Ops wants a feature? Paste what they said. The skill reads the relevant codebase to understand the current implementation, checks your knowledge base for related prior work, then drafts and creates a structured Jira story ticket — ready for engineering to pick up.

**`/brain-ops-bug`** — *Paste bug report from ops*
Ops reports something broken? Paste the message. The skill searches the codebase for the likely code path, checks your past incident notes for similar bugs, assesses severity (P1–P4), and creates a Jira bug ticket with investigation findings already attached.

**`/brain-weekly-email`** — *"Weekly email" / "Friday email"*
Pulls the week's completed and in-progress Jira tickets automatically, reads any decisions you captured in the brain this week, and fills in your team's weekly status email template. Saves the HTML version to your knowledge base and shows you the plain text to copy.

---

### Dev workflow

**`/brain-review`** — *"Review my code" / "Check my diff"*
Not a generic review — it loads your project's specific coding standards, pulls the Jira ticket's acceptance criteria from your branch name, and checks your past decisions for anything relevant. Outputs confidence-scored issues (≥80% only) grouped Critical / Important, each with file:line and a concrete fix.

**`/brain-ship`** — *"Ship this" / "Create a PR"*
Full pipeline: runs tests → lint (with auto-fix) → code review → git commit → push → creates GitHub PR → transitions your Jira ticket to "In Review." Stops if tests fail. Asks before pushing if review found Critical issues.

**`/brain-investigate`** — *"Debug this" / "Root cause WFM-1234"*
Root cause analysis, not guesswork. Searches the codebase for the relevant code path, checks your past incident notes for similar bugs, and produces: hypothesis, evidence (code references + prior incidents), steps to reproduce, and a concrete proposed fix with file:line.

**`/brain-retro`** — *"Weekly retro" / "Summarize my week"*
Pulls git commits across all your repos for the last 7 days, pulls your sprint's Jira status, and lists new knowledge items you added this week. Writes a structured retrospective: what shipped, what's in flight, blockers, what you learned, and your top 3 priorities for next week.

**`/brain-sync`** — *"Sync Jira" / "Sync my sprint" / "Sync WFM-1234"*
Pulls live data from Jira and Confluence into your knowledge base. After syncing, tells you what changed: tickets that moved status, new tickets added, pages that were updated.

---

## How the knowledge base works

Everything lives in `~/brain/knowledge/` as plain markdown files — organized into folders by type:

```
knowledge/
├── prd/                 ← Product requirements docs
├── decisions/           ← Every decision made, with date and rationale
├── features/            ← Feature briefs and plans
├── stakeholders/        ← One file per person or team
├── jira/                ← Live Jira ticket snapshots (synced by Scout)
├── confluence/          ← Live Confluence page snapshots (synced by Scout)
├── retros/              ← Weekly retrospectives
├── domain/              ← Domain knowledge and business glossary
├── oncall/              ← Incident notes and runbooks
├── daily-journals/      ← Daily meeting notes
├── business-reviews/    ← Business reviews and OKR updates
├── ai-strategy/         ← AI adoption and tooling decisions
├── coaching-sessions/   ← Coaching notes and feedback
├── operating-plans/     ← Quarterly and annual plans
└── scratch/             ← Unclassified notes (Sorter will reclassify)
```

Every file has a header that looks like this:

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

The SQLite database at `data/brain.db` indexes all of these files so skills can search across thousands of notes instantly, without reading every file. The database is just a query layer — the markdown files are what actually matter, and they're all yours.

Your knowledge base is **gitignored** — it stays on your machine and is never published anywhere.

---

## Prerequisites

- [Claude Code](https://claude.ai/code) (CLI or desktop app)
- [Atlassian MCP](https://github.com/sooperset/mcp-atlassian) — connects to your Jira and Confluence
- [GitHub MCP](https://github.com/github/github-mcp-server) — connects to your GitHub org
- `sqlite3` in your shell (`brew install sqlite` on macOS)

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/abhishekshah-blink/pm-brain ~/brain
cd ~/brain
```

**2. Tell it who you are**
Edit `~/brain/.claude/CLAUDE.md` and fill in the `[placeholder]` values at the top:
- Your name and role
- Your Jira workspace URL (e.g. `yourcompany.atlassian.net`)
- Your GitHub org
- Your active projects and where they live on your machine

**3. Add your weekly email template** *(optional)*
If your team has a standard status email format, add it as HTML to:
`~/brain/.claude/skills/brain-weekly-email/references/email-template.html`

**4. Configure your MCPs**
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

**5. Run setup**
```bash
bash ~/brain/scripts/setup.sh
```
This creates all the folders, initializes the SQLite database, and links all 11 skills into Claude Code so they show up as `/brain-*` commands.

**6. First run**
Open Claude Code from `~/brain/` and start:
```
/brain-sync sprint     ← pull your current Jira sprint
/brain-retro           ← generate your first weekly retro
```

---

## Inspiration and credits

This system combines two ideas:

**[PKA (Personal Knowledge Assistance)](https://github.com/garrytan/gstack)** by **Nir Sheep** — the pattern of building a second brain with AI agents: a filing inbox, specialist agents that classify and index, and a clean taxonomy of knowledge categories. PKA showed that "drop files in, get organized knowledge out" is a genuinely powerful workflow.

**[gstack](https://github.com/garrytan/gstack)** by **Garry Tan** (President & CEO of Y Combinator) — the pattern of building slash-command skills as plain markdown files that Claude Code reads and executes. The PREAMBLE system, voice directive, completion protocol, and Fix-First heuristic are all adapted from gstack.

What pm-brain adds on top: **MCP-native live data**. Instead of manually dropping files into an inbox, Scout pulls directly from Jira and Confluence using the Atlassian MCP. The knowledge base stays current without manual effort, and every skill uses live Jira data rather than stale copies.

---

*Built with Claude Code. Your knowledge stays on your machine.*
