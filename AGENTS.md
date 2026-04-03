# Brain System — AGENTS.md

> Agent discovery file for Cursor, Codex, Gemini CLI, and other AI tools that don't auto-read `.claude/CLAUDE.md`.
> The full system instructions live at `.claude/CLAUDE.md` — refer there for complete context.

## What This Is

~/pm/brain/ is Abhishek Shah's Personal Knowledge Accelerator — a second brain for a PM who builds at Blinkhealth. It combines:
- **Knowledge management:** raw inputs (Jira, Confluence, PDFs, meeting notes) → structured markdown → SQLite index
- **Dev workflow skills:** slash commands for planning, reviewing, shipping, debugging, and retrospectives

## Agents

| Agent | Role |
|---|---|
| **Sorter** | Orchestrator. Processes inbox, classifies files, delegates to Keeper and Scout. Entry point for batch operations. |
| **Keeper** | Knowledge librarian. Writes and indexes knowledge items. Answers lookup queries from skills. |
| **Scout** | MCP sync agent. Pulls Jira tickets, Confluence pages, and GitHub PRs into ~/pm/brain/knowledge/. |

## Skills (slash commands)

| Skill | Purpose |
|---|---|
| `/brain-discovery` | Problem framing and customer discovery |
| `/brain-plan` | Plan a feature using brain context + live Jira/Confluence |
| `/brain-prd` | Write a PRD or one-pager |
| `/brain-user-story` | Create a Jira user story |
| `/brain-review` | Code review with project rules + ticket acceptance criteria |
| `/brain-ship` | Full pipeline: test → lint → review → commit → push → PR → Jira |
| `/brain-investigate` | Root cause analysis with oncall history and knowledge base |
| `/brain-sync` | Pull Jira/Confluence/GitHub into knowledge base via MCP |
| `/ops-feedback` | Ops Slack feedback → structured Jira story |
| `/ops-bug` | Ops Slack bug report → Jira bug ticket |
| `/brain-weekly-email` | Compile Friday VP status email |
| `/brain-decision` | Log a decision with alternatives, rationale, tradeoffs, and revisit trigger |

## Knowledge Base

- Root: ~/pm/brain/knowledge/
- Categories: prd, decisions, stakeholders, jira, confluence, features, domain, oncall, wins, scratch
- SQLite index: ~/pm/brain/data/brain.db
- Inbox: ~/pm/brain/inbox/

## Full Instructions

See `.claude/CLAUDE.md` for the complete taxonomy, naming conventions, frontmatter requirements, SQLite query patterns, MCP tools, and system invariants.
