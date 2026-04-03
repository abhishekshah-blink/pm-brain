---
title: Claude Code Tips & Best Practices
category: domain
tags: [claude-code, productivity, workflow, agents, skills, hooks]
created: 2026-04-03
updated: 2026-04-03
---

# Claude Code Tips & Best Practices

Curated from Boris Cherny (Claude Code creator) and Thariq (Anthropic), covering the highest-signal tips for using Claude Code effectively.

---

## Parallelism — The Single Biggest Unlock

- **Run 3–5 Claudes in parallel** using git worktrees (`claude -w`). It's the top tip from the Claude Code team.
- Use `claude.ai/code` for additional parallel sessions beyond your terminal.
- Name worktrees and set shell aliases (`2a`, `2b`, `2c`) to hop between them in one keystroke.
- `/batch` fans work out to dozens/hundreds of worktree agents for large migrations.
- Use `claude -w` or the "worktree" checkbox in the Desktop app.

---

## Planning — Pour Energy into the Plan

- **Start every complex task in Plan mode** (shift+tab twice). A good plan lets Claude 1-shot the implementation.
- Switch back to plan mode the moment something goes sideways — don't keep pushing.
- Have one Claude write the plan, then spin up a second Claude to review it as a staff engineer.
- Tell Claude to enter plan mode for verification steps, not just for the build.

---

## CLAUDE.md — Your Most Valuable Asset

- After every correction: "Update your CLAUDE.md so you don't make that mistake again." Claude is good at writing rules for itself.
- Ruthlessly edit CLAUDE.md over time. Keep iterating until Claude's mistake rate drops.
- Keep it under 200 lines. Too long and it loses signal.
- Share a single CLAUDE.md with the team — check it into git, have everyone contribute weekly.
- Tag `@claude` on PRs to automatically update CLAUDE.md as part of code review.

---

## Skills — Build Once, Reuse Always

From Thariq's detailed guide on how Anthropic uses skills internally:

**9 skill categories that work:**
1. **Library/API Reference** — how to use an internal library correctly (include gotchas)
2. **Product Verification** — how to test/verify your code works (pair with Playwright)
3. **Data Fetching & Analysis** — connect to data/monitoring stacks (BigQuery, Grafana)
4. **Business Process Automation** — repetitive workflows in one command (standup, weekly recap)
5. **Code Scaffolding** — boilerplate generation with natural language requirements
6. **Code Quality & Review** — enforce standards; run via hooks or GitHub Actions
7. **CI/CD & Deployment** — fetch, push, deploy; reference other skills
8. **Runbooks** — symptom → multi-tool investigation → structured report
9. **Infrastructure Ops** — routine maintenance with guardrails for destructive actions

**Writing great skills:**
- **Skills are folders, not files.** Use subdirectories for references/, scripts/, examples/.
- **Description = trigger condition** for the model. Write it for Claude, not for humans.
- **Build a Gotchas section** — highest-signal content. Update it when Claude fails.
- **Don't railroad Claude.** Give goals and constraints, not step-by-step prescriptions.
- **On-demand hooks** — skills can activate hooks that last for the session (e.g., `/careful` blocks rm -rf).
- Use `${CLAUDE_PLUGIN_DATA}` as stable storage per skill (not skill dir — gets deleted on upgrade).
- Store scripts in skills — lets Claude compose rather than reconstruct boilerplate.

**Distributing skills:**
- For small teams: check into repo under `.claude/skills/`
- For orgs: build an internal plugin marketplace. Every installed skill adds a bit to context — curation matters.

---

## Hooks — Lifecycle Automation

**22 hook events available.** Most useful ones:
- `SessionStart` — load context dynamically at session start
- `PreCompact` — snapshot what you're working on before context compression
- `PostToolUse` — auto-format code after edits (`bun run format || true`)
- `Stop` — poke Claude to keep going, or verify its work
- `PreToolUse` — log every bash command; block dangerous ops
- `PermissionRequest` — route to Slack/WhatsApp for remote approval

**Key patterns:**
- Use `PostToolUse` with `matcher: "Write|Edit"` to auto-format after every file change.
- Route permission requests to Opus via a hook to auto-approve safe ones.
- Use `PreToolUse` to block `rm -rf`, `DROP TABLE`, force-push when in sensitive contexts.

---

## Verification — The Most Important Thing

> "Give Claude a way to verify its work. It will 2–3x the quality of the final result." — Boris Cherny

- Give Claude a browser (Chrome extension) for frontend work — it will iterate until it looks right.
- Say "Prove to me this works" and have Claude diff behavior between main and your branch.
- Say "Go fix the failing CI tests" without micromanaging how.
- Use a Stop hook to trigger a verification agent after long-running tasks.
- Multiple uncorrelated context windows find more bugs than one — use subagents for review.

---

## Prompting Upgrades

- **Challenge Claude:** "Grill me on these changes and don't make a PR until I pass your test."
- **After a mediocre fix:** "Knowing everything you know now, scrap this and implement the elegant solution."
- **Append "use subagents"** to any request where you want more compute thrown at it.
- Write detailed specs before handing work off — specificity drives quality.

---

## Workflow Patterns

- **`/loop` and `/schedule`** — run Claude automatically at intervals for up to a week. High-value automations: babysit PRs, sweep for stale branches, sync Slack feedback.
- **Squash merge always** — keeps history clean and linear. Each PR = one revertable commit.
- **Keep PRs small** — Boris's median PR is 118 lines. Small PRs reduce conflict risk and are reviewable.
- **`/btw`** — ask a side question without interrupting the agent's current task.
- **`/branch`** — fork the current session to explore an alternative approach.
- **`--add-dir`** — give Claude access to a second repo without restarting the session.
- **`--bare`** — skip CLAUDE.md/settings discovery for SDK/scripted use; up to 10x faster startup.

---

## Terminal & Environment

- Use `/statusline` to show context %, cost, and model below the composer (already wired in this setup).
- Use voice input (`/voice` or fn×2 on macOS) — you speak 3× faster than you type.
- Set effort level to **High** for everything. Bigger token budget = better results.
- Use "Explanatory" output style when learning a new codebase.

---

## Source

- Boris Cherny tips: Jan 3, Feb 1, Feb 12, Mar 10, Mar 25, Mar 30, 2026
- Thariq skills guide: Mar 17, 2026
- Repo: `~/pm/claude-code-best-practice/tips/`
