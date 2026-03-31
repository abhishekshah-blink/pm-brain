# Brain System — AGENTS.md

> Agent discovery file for Cursor, Codex, Gemini CLI, and other AI tools that don't auto-read `.claude/CLAUDE.md`.
> The full system instructions live at `.claude/CLAUDE.md` — refer there for complete context.

## What This Is

~/brain/ is Abhishek Shah's Personal Knowledge Accelerator — a second brain for a PM who builds at Blinkhealth. It combines:
- **Knowledge management:** raw inputs (Jira, Confluence, PDFs, meeting notes) → structured markdown → SQLite index
- **Dev workflow skills:** slash commands for planning, reviewing, shipping, debugging, and retrospectives

## Agents

| Agent | Role |
|---|---|
| **Roni** | Orchestrator. Processes inbox, classifies files, delegates to Nova and Spark. Entry point for batch operations. |
| **Nova** | Knowledge librarian. Writes and indexes knowledge items. Answers lookup queries from skills. |
| **Spark** | MCP sync agent. Pulls Jira tickets, Confluence pages, and GitHub PRs into ~/brain/knowledge/. |

## Skills (slash commands)

| Skill | Purpose |
|---|---|
| `/brain-plan` | Plan a feature using brain context + live Jira/Confluence |
| `/brain-review` | Code review with project rules + ticket acceptance criteria |
| `/brain-ship` | Full pipeline: test → lint → review → commit → push → PR → Jira |
| `/brain-investigate` | Root cause analysis with oncall history and knowledge base |
| `/brain-retro` | Weekly retro from git + Jira sprint + brain knowledge items |
| `/brain-sync` | Pull Jira/Confluence/GitHub into knowledge base via MCP |

## Knowledge Base

- Root: ~/brain/knowledge/
- Categories: prd, decisions, stakeholders, jira, confluence, features, retros, domain, oncall, daily-journals, business-reviews, ai-strategy, coaching-sessions, operating-plans, scratch
- SQLite index: ~/brain/data/brain.db
- Inbox: ~/brain/inbox/

## Full Instructions

See `.claude/CLAUDE.md` for the complete taxonomy, naming conventions, frontmatter requirements, SQLite query patterns, MCP tools, and system invariants.
