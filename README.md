# pm-brain

> A second brain for product managers who build — powered by Claude Code.

Most PMs carry too much in their heads: what was decided last sprint, what ops reported on Slack, what the acceptance criteria were for that ticket three weeks ago. pm-brain captures all of it, organizes it automatically, and surfaces it the moment you need it — whether you're writing a BRD, shipping code, or compiling the Friday status email.

It runs entirely inside [Claude Code](https://claude.ai/code). No new app. No extra subscription. Just commands you type, and agents that do the work.

<details>
<summary>Table of contents</summary>

- [What it does](#what-it-does)
- [Capabilities](#capabilities)
  - [Product work](#product-work)
  - [Engineering work](#engineering-work)
  - [Ops intake](#ops-intake)
  - [Knowledge and sync](#knowledge-and-sync)
- [Wins tracking](#wins-tracking)
- [Skill Scout](#skill-scout)
- [Under the hood](#under-the-hood)
- [Getting started](#getting-started)
- [Credits](#credits)

</details>

---

## What it does

**Every artifact you create is grounded in what you already know.**
When you run `/brain-plan`, it doesn't start from scratch — it first reads your existing PRDs, pulls the relevant Jira tickets live, checks your past decisions, and *then* writes the plan. Context that would take 20 minutes to gather manually happens in seconds.

**Company templates, automatically.**
BRDs, Jira stories, and the weekly VP email are generated using Blinkhealth's standard templates — not custom formats. `/brain-prd` produces a BRD-format doc. `/brain-user-story` creates a roadmap-ticket-formatted Jira story. Output goes straight into the process.

**Ops feedback becomes Jira tickets without the back-and-forth.**
Paste a Slack message from ops into `/ops-feedback` or `/ops-bug`. Brain reads the relevant codebase, checks for prior incidents, assesses severity, and creates a structured, well-scoped Jira ticket — ready for grooming.

**Everything you ship is silently recorded.**
Every Jira transition, every GitHub PR, every ticket you create — captured automatically in the background, enriched overnight by Claude, and ready at review season. No end-of-year scramble to remember what you did.

**And it gets smarter every week.**
Every Monday, Skill Scout scans the previous week's work sessions and identifies processes you're doing manually that could become new skills. The system learns and grows from actual usage.

---

## Capabilities

### Product work

| Command | What you say | What happens |
|---|---|---|
| `/brain-discovery` | "help me frame the problem", "do discovery for WFM-1234" | Problem framing before building — JTBD analysis, opportunity mapping, problem statement |
| `/brain-plan` | "plan this feature", "break down WFM-1234" | Feature plan with live Jira + Confluence + prior PRD context pulled automatically |
| `/brain-prd` | "write a PRD for X", "one-pager for X" | BRD-format document with problem statement gate and Working Backwards stress-test |
| `/brain-user-story` | "create a ticket for X", "write a user story" | Jira story in roadmap ticket format with JTBD framing and acceptance criteria |
| `/brain-decision` | "log a decision", "we decided X" | Decision record with rationale, alternatives considered, and revisit trigger |
| `/brain-weekly-email` | "write the weekly email", "Friday email" | VP status email in company HTML format, Jira sprint data pulled automatically |

### Engineering work

| Command | What you say | What happens |
|---|---|---|
| `/brain-investigate` | "debug this", "why is X failing", "root cause WFM-1234" | Root cause analysis with prior incident context from the knowledge base |
| `/brain-review` | "review my code", "check before commit" | Pre-commit review using project rules + Jira acceptance criteria |
| `/brain-ship` | "ship this", "commit and push", "create a PR" | Tests → lint → review → commit → push → PR → Jira transition, in one command |
| `/eng-workflow` | "implement WFM-1234" | 7-phase structured workflow with plan approval gate (for non-trivial features) |
| `/pr-review` | "review this PR" | GitHub pending draft review with inline comments after a branch is pushed |

### Ops intake

| Command | What you say | What happens |
|---|---|---|
| `/ops-feedback` | paste ops Slack text | Ops message → scoped Jira story with codebase context and acceptance criteria |
| `/ops-bug` | paste ops Slack bug report | Ops message → Jira bug ticket with severity assessment and prior incident check |

### Knowledge and sync

| Command | What you say | What happens |
|---|---|---|
| `/brain-sync` | "sync sprint", "pull WFM-1234", "sync Confluence" | Pulls Jira tickets and Confluence pages into the local knowledge base |
| `/skill-scout` | "what should be a skill?", "find repeatable processes" | Reviews last week's sessions and surfaces automation candidates |

---

## Wins tracking

The hardest part of performance reviews is remembering what you did six months ago. pm-brain solves this passively.

Every time you transition a Jira ticket, merge a PR, or create a ticket from ops feedback — it's captured instantly in the background without any input from you. Each night, Claude enriches the raw signals: it pulls the Jira context, writes a concise description of what you did and why it mattered, maps it to your performance pillars, and generates both a review-ready bullet and a resume-style bullet.

Every Friday, a digest is generated automatically: top wins for the week, pillar coverage, and gaps to close before the next review cycle.

For work that doesn't touch Jira or GitHub — a tough stakeholder conversation, an unblocking decision, a process improvement — `/wins "what you did"` captures it in 30 seconds.

At review time:

- `/wins-digest quarterly` → full self-review draft, bullets organized by competency
- `/wins-digest promo` → promotion case narrative with your strongest examples and identified gaps

---

## Skill Scout

Most productivity systems are static — you build them once and they drift out of sync with how you actually work.

Every Monday at 9am, Skill Scout scans the previous week's Claude Code sessions and looks for three signals:

- **Frequency** — the same kind of task appearing across multiple sessions
- **Complexity** — tasks that required many steps and tool calls to complete
- **Guidance overhead** — tasks where you had to correct or redirect Claude repeatedly

For each pattern it finds, it writes a candidate skill description to your knowledge base: what you were doing, why it's worth formalizing, and a proposed workflow. Run `/skill-scout` to review the list and, if any candidate looks right, draft it into a real skill on the spot.

The system grows from actual usage. Skills you add this month get picked up by Skill Scout next month and refined further.

---

## Under the hood

Everything is stored as plain markdown files on your machine — never in the cloud. A SQLite database sits alongside the files as a query layer: every knowledge item, Jira ticket, Confluence page, stakeholder, and win is indexed with metadata. When you run a skill, it queries the database first to find what's relevant, then reads only those files — keeping responses fast and focused even as the knowledge base grows to thousands of entries. The markdown files are the source of truth; the database is just how skills find things quickly.

Three agents run silently in the background:

**Sorter** is the inbox processor. Drop any file into `inbox/` — meeting notes, a Confluence export, a Slack thread, a copied decision from a call — and Sorter reads it, determines what it is, and files it into the right category: PRD, decision, stakeholder note, incident, domain knowledge. If it's confident, it routes precisely. If it's unsure, it places the file in `scratch/` and flags it for review. Nothing gets lost; nothing requires manual filing.

**Keeper** is the librarian. Writes and indexes knowledge items, links related files, and maintains the metadata that makes search work.

**Scout** connects to Jira, Confluence, and GitHub via MCP. Skills call Scout automatically when they need live data — you rarely need to invoke it directly.

Background jobs run on a schedule: Jira syncs every morning, wins are enriched every evening, a digest is generated every Friday, and Skill Scout runs every Monday.

---

## Getting started

Requires [Claude Code](https://claude.ai/code), the [Atlassian MCP](https://github.com/sooperset/mcp-atlassian), and the [GitHub MCP](https://github.com/github/github-mcp-server).

```bash
git clone https://github.com/abhishekshah-blink/pm-brain ~/pm/brain
bash ~/pm/brain/scripts/setup.sh
```

Edit `~/pm/brain/.claude/CLAUDE.md` to set your name, Jira workspace, GitHub org, and active projects. Wire the hooks and cron jobs from `scripts/` into `~/.claude/settings.json`. Then:

```bash
/brain-sync sprint   # pull your current sprint into the knowledge base
/brain-plan          # plan something — with live context
```

Full configuration details are in [`.claude/CLAUDE.md`](.claude/CLAUDE.md).

---

## Credits

Patterns borrowed from three projects:

- **[PKA](https://github.com/nir-sheep/pka)** by Nir Sheep — filing inbox, specialist agents, knowledge taxonomy
- **[gstack](https://github.com/garrytan/gstack)** by Garry Tan — slash-command skills as markdown, PREAMBLE system, voice directives, fix-first heuristic
- **[blink-ai-tools](https://github.com/blinkhealth/blink-ai-tools)** — company SDLC automation: engineering skills, Cursor rules, and document templates that brain skills delegate to

---

*Built with Claude Code. Your knowledge stays on your machine.*
