# pm-brain

> A second brain for product managers who build — powered by Claude Code.

Most PMs carry too much in their heads: what was decided last sprint, what ops reported on Slack, what the acceptance criteria were for that ticket three weeks ago. pm-brain captures all of it, organizes it automatically, and surfaces it the moment you need it — whether you're writing a BRD, shipping code, or compiling the Friday status email.

It runs entirely inside [Claude Code](https://claude.ai/code). No new app. No extra subscription. Just slash commands you type, and agents that do the work.

---

## What it does

**Builds a knowledge base from everything you encounter at work.**
Jira tickets, Confluence pages, ops Slack messages, incident reports, meeting notes — organized into markdown files with a searchable SQLite database behind them. A filing system that files itself.

**Gives you slash commands grounded in that context.**
When you run `/brain-plan`, it first reads your existing PRDs, pulls the relevant Jira tickets live, checks your past decisions, and *then* writes the plan. Every skill is grounded in what you actually know.

**Uses company-standard templates automatically.**
BRDs, Jira ticket descriptions, and the weekly status email all follow company templates from `blink-ai-tools`, not custom formats. Output is always compatible with the TDLC standard.

**And silently records everything you ship.**
Every Jira transition, every GitHub PR, every bug triaged — captured automatically in the background, enriched by Claude overnight, ready for review season.

---

## PM Skills

| Skill | Trigger phrases | What it does |
|---|---|---|
| `/brain-discovery` | "run discovery on X", "frame the problem", "do discovery for WFM-1234" | Problem framing before building — JTBD analysis, OST, MITRE canvas |
| `/brain-plan` | "plan a feature", "break down WFM-1234", "design X" | Feature planning with live brain context — queries brain.db + Jira + Confluence |
| `/brain-prd` | "write a PRD", "one-pager for X", "product spec" | BRD/PRD using the company BRD template — adds problem statement gate and Working Backwards stress-test |
| `/brain-user-story` | "write a user story", "create a ticket for X" | Jira story using the company roadmap ticket template — adds JTBD framing and INVEST validation |
| `/brain-decision` | "log a decision", "we decided X", "document this tradeoff" | ADR-style decision logging into `knowledge/decisions/` |
| `/ops-feedback` | "ops feedback", paste ops Slack text | Ops Slack → structured Jira story with codebase context |
| `/ops-bug` | "ops bug", paste ops Slack bug report | Ops Slack → Jira bug ticket with severity assessment |
| `/brain-weekly-email` | "write the weekly email", "Friday email", "draft VP status" | VP status email using the company HTML template — pulls Jira sprint data automatically |
| `/brain-review` | "review my code", "check before commit" | Pre-commit review using project CLAUDE.md rules + Jira acceptance criteria |
| `/brain-ship` | "ship this", "commit and push", "create a PR" | Quick ship pipeline — tests → lint → review → commit → push → PR → Jira transition |
| `/brain-investigate` | "debug this", "root cause WFM-1234", "why is X failing" | Root cause analysis with prior incident context from brain.db |
| `/brain-sync` | "sync Jira", "pull my tickets", "sync sprint", "sync WFM-1234" | Pull Jira/Confluence/GitHub into knowledge base via MCP |
| `/skill-scout` | "what should be a skill", "scan my sessions", "find repeatable processes" | Surfaces repeatable processes from past sessions — auto-runs Mondays, drafts candidates into real skills |

---

## Engineering Skills

| Skill | When to use |
|---|---|
| `/eng-workflow` | Any non-trivial feature — 7-phase workflow with plan approval gate and SP-based depth |
| `/pr-review` | After pushing a branch — creates a pending GitHub draft review with inline comments |
| `/ai-retro` | After a ticket is delivered — SP evaluation report and calibration |
| `/jira-status-update` | Add a structured living status comment to a Jira ticket |
| `/eng-scorecard` | Score tickets from retro files → `output/baseline_scorecard.csv` |
| `/generate-manual` | Auto-generate a user manual via journey-explorer → screenshot-capture → manual-writer |

> **brain-ship vs eng-workflow:** Use `/brain-ship` for small fixes and hotfixes. Use `/eng-workflow` for feature work with story points ≥ 0.5 — it includes a plan approval gate, structured phases, and E2E validation.

---

## Automatic wins tracking

The hardest part of performance reviews is remembering what you did six months ago. pm-brain solves this without any extra effort.

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
        ▼  (nightly)
┌─────────────────────────────────────────────┐
│  Nightly cron enriches the queue            │
│  Claude pulls Jira context and writes:      │
│  • what you did + why it mattered           │
│  • review-ready bullet + resume bullet      │
│  • SPM I pillar signal (delivery/impact/    │
│    ambiguity/complexity)                    │
│  → saves to knowledge/wins/                 │
└─────────────────────────────────────────────┘
        │
        ▼  (every Friday)
┌─────────────────────────────────────────────┐
│  Weekly digest auto-generated               │
│  Top wins, pillar breakdown, evidence gaps  │
│  → saved to knowledge/wins/digests/         │
└─────────────────────────────────────────────┘
```

**Captured automatically:**
- Every GitHub PR you create or merge
- Every Jira ticket you transition (In Review, Done, Closed)
- Every ticket created via `/ops-feedback` or `/ops-bug`
- Every shipment via `/brain-ship`

**For things that never touch Jira or GitHub** — `/wins "what you did"` in 30 seconds.

**At review time:**
```
/wins-digest quarterly    → full self-review draft, bullets by competency
/wins-digest promo        → promotion case narrative, strongest examples, gaps to close
```

---

## Three agents behind the scenes

**Sorter** is the orchestrator. Drop any file in `inbox/` and Sorter reads it, classifies it, and routes it to the right folder. Confident (≥70%)? Precise routing. Unsure? `scratch/` and flagged. Cleans up after filing.

**Keeper** is the librarian. Writes knowledge items — PRDs, synced tickets, incident notes, enriched wins. Adds structured metadata, indexes everything in brain.db, links related items.

**Scout** connects to Jira, Confluence, and GitHub via MCP. Run `/brain-sync sprint` and Scout pulls your entire current sprint as searchable markdown. Skills call Scout automatically when they need live data.

---

## The knowledge base

Everything lives in `knowledge/` as plain markdown files with structured frontmatter:

```
knowledge/
├── prd/            ← BRDs, one-pagers, acceptance criteria
├── decisions/      ← ADRs — every decision with date, rationale, revisit trigger
├── features/       ← Feature briefs from discovery through shipped
├── stakeholders/   ← One file per person or team
├── jira/           ← Live Jira ticket snapshots (auto-synced by Scout)
├── confluence/     ← Live Confluence page snapshots (auto-synced by Scout)
├── domain/         ← PM frameworks, Claude Code tips, domain knowledge
├── oncall/         ← Incident notes and runbooks
├── wins/           ← Auto-captured accomplishment records (enriched nightly)
│   └── digests/    ← Weekly and quarterly synthesized summaries
└── scratch/        ← Unclassified notes (Sorter reclassifies on request)
```

Every file has YAML frontmatter:

```yaml
---
title: BRD: Shift Summary View
category: prd
tags: [scheduling, wfm, v2]
created: 2026-03-30
updated: 2026-03-30
jira_tickets: [WFM-1234]
---
```

The SQLite database at `data/brain.db` indexes all files so skills can search across thousands of notes instantly. The database is a query layer — the markdown files are the source of truth.

> The knowledge base is gitignored. It stays on your machine.

---

## How brain delegates to other tools

Some brain skills are thin wrappers — they add PM context (JTBD framing, brain.db lookup, acceptance criteria) and then hand off to a canonical tool or template rather than re-implementing it.

**Templates** — three skills read company-standard templates at runtime from `~/.claude/blink-ai-tools/report_templates/`:

| Brain skill | Delegates to |
|---|---|
| `/brain-prd` | `brd_template.md` — brain adds problem statement gate, JTBD framing, Working Backwards stress-test |
| `/brain-user-story` | `roadmap_ticket.md` — brain adds JTBD framing, INVEST check, epic hypothesis |
| `/brain-weekly-email` | `weekly_status_email_template.html` — brain pulls Jira sprint data and fills it |

Additional templates (reference manually from `~/.claude/blink-ai-tools/report_templates/`):
- `technical_design_document_template.md` — TRD with architecture diagrams, IAM, threat model, cost analysis
- `test_plan_template.md` — QA test plan with scope, entry/exit criteria, risk matrix

**Engineering skills** — brain-ship checks whether `/eng-workflow` is the better tool before proceeding:

| Brain skill | Defers to | When |
|---|---|---|
| `/brain-ship` | `/eng-workflow` | Story points ≥ 0.5, new features, architecture changes |
| `/brain-review` | `/pr-review` | After a branch is pushed (post-push GitHub review vs pre-commit local check) |

---

## Hooks

Four hooks are wired in `~/.claude/settings.json`:

| Event | Hook | What it does |
|---|---|---|
| `PostToolUse` | `wins-hook.py` | Fires on Jira transitions and GitHub PR events → appends to `wins/pending.jsonl` |
| `Stop` | `wins-hook.py` | Scans the session transcript for meaningful work → logs aggregated session entry |
| `PreCompact` | `pre-compact-hook.py` | Before context compression → snapshots session state to `scratch/compact-log.jsonl` |

---

## Cron jobs

Three background jobs run on schedule:

| Schedule | Script | What it does |
|---|---|---|
| Daily 8:00am | `scripts/sync-cron.sh` | Pulls open sprint + recently updated Jira tickets into `knowledge/jira/` |
| Daily 5:30pm | `scripts/wins-enrich-cron.sh` | Enriches `wins/pending.jsonl` → structured win files with SPM I pillar tags |
| Fridays 4:30pm | `scripts/wins-digest-cron.sh` | Synthesizes the week's wins into `knowledge/wins/digests/YYYY-WW.md` |
| Mondays 9:00am | `scripts/skill-scout-cron.sh` | Scans last week's sessions → `knowledge/scratch/skill-suggestions-YYYY-WW.md` |

---

## Prerequisites

- [Claude Code](https://claude.ai/code) (CLI or desktop app)
- [Atlassian MCP](https://github.com/sooperset/mcp-atlassian) — connects Claude to Jira and Confluence
- [GitHub MCP](https://github.com/github/github-mcp-server) — connects Claude to your GitHub org
- `sqlite3` in your shell (`brew install sqlite` on macOS)

---

## Setup

**1. Clone**
```bash
git clone https://github.com/abhishekshah-blink/pm-brain ~/pm/brain
```

**2. Tell it who you are**

Edit `~/pm/brain/.claude/CLAUDE.md` and update the identity section:
- Your name and role
- Jira workspace URL (e.g. `yourcompany.atlassian.net`)
- GitHub org
- Active projects and their paths on your machine

**3. Configure MCPs**

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
bash ~/pm/brain/scripts/setup.sh
```

Creates all knowledge folders, initializes brain.db, and symlinks skills into `~/.claude/skills/`.

**5. Wire the hooks**

Add to `~/.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "mcp__atlassian__jira_transition_issue|mcp__atlassian__jira_create_issue|mcp__github__create_pull_request|mcp__github__merge_pull_request",
        "hooks": [{ "type": "command", "command": "python3 ~/pm/brain/scripts/wins-hook.py" }]
      }
    ],
    "Stop": [
      {
        "hooks": [{ "type": "command", "command": "python3 ~/pm/brain/scripts/wins-hook.py" }]
      }
    ],
    "PreCompact": [
      {
        "hooks": [{ "type": "command", "command": "python3 ~/.claude/scripts/pre-compact-hook.py" }]
      }
    ]
  }
}
```

**6. Install cron jobs**
```bash
(crontab -l 2>/dev/null; cat <<'EOF'
# Brain daily Jira sync
0 8 * * * /bin/zsh -l ~/pm/brain/scripts/sync-cron.sh
# Brain wins enrichment
30 17 * * * /bin/zsh -l ~/pm/brain/scripts/wins-enrich-cron.sh
# Brain wins weekly digest
30 16 * * 5 /bin/zsh -l ~/pm/brain/scripts/wins-digest-cron.sh
EOF
) | crontab -
```

**7. First run**
```bash
/brain-sync sprint     # pull your current Jira sprint into the knowledge base
/brain-plan            # plan something — with live context
```

---

## What gets saved where

| Skill | Output |
|---|---|
| `/brain-discovery` | Conversation + optionally `knowledge/features/` |
| `/brain-plan` | `knowledge/features/` + conversation |
| `/brain-prd` | `knowledge/prd/` + optionally Confluence |
| `/brain-decision` | `knowledge/decisions/YYYY-MM-DD-slug.md` |
| `/brain-user-story` | Jira ticket (created) + `knowledge/features/` |
| `/ops-feedback` | Jira ticket (created) + `knowledge/features/` |
| `/ops-bug` | Jira ticket (created) + optionally `knowledge/oncall/` |
| `/brain-review` | Conversation — issues grouped by severity |
| `/brain-ship` | GitHub PR + Jira transitioned to In Review |
| `/brain-investigate` | Conversation + optionally `knowledge/oncall/` |
| `/brain-weekly-email` | `knowledge/retros/YYYY-WW-weekly-email.html` + conversation |
| `/brain-sync` | `knowledge/jira/` and `knowledge/confluence/` |

---

## Credits

Patterns borrowed from three projects:

- **[PKA](https://github.com/nir-sheep/pka)** by Nir Sheep — filing inbox, specialist agents, knowledge taxonomy
- **[gstack](https://github.com/garrytan/gstack)** by Garry Tan — slash-command skills as markdown, PREAMBLE system, voice directives, fix-first heuristic
- **[blink-ai-tools](https://github.com/blinkhealth/blink-ai-tools)** — company SDLC automation: engineering skills, Cursor rules, and document templates that brain skills delegate to

---

*Built with Claude Code. Your knowledge stays on your machine.*
