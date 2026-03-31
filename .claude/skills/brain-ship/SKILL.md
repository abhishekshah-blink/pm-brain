---
name: brain-ship
version: 1.0.0
description: This skill should be used when the user wants to "ship this feature", "commit and push", "create a PR", "deploy to review", or "ship my changes". Runs the full Blinkhealth shipping pipeline — tests, lint, review, commit, push, PR creation, and Jira ticket transition.
allowed-tools: Read, Glob, Bash, Task, mcp__github__create_pull_request, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_get_transitions, mcp__atlassian__jira_transition_issue, mcp__atlassian__jira_add_comment
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`
- Current directory: !`pwd`
- Current branch: !`git branch --show-current 2>/dev/null || echo "not a git repo"`
- Git status: !`git status --short 2>/dev/null`
- Git diff: !`git diff HEAD 2>/dev/null | head -300`

## Instructions

You are running /brain-ship. You will run the full shipping pipeline for the current branch. This has real side effects — it pushes code and creates a GitHub PR. Confirm before the push step if anything looks unexpected.

**Order of operations:** tests → lint → review → commit → push → PR → Jira transition

### Step 1: Guard check

```bash
git status --short
```

If no changes (clean working tree and no staged files): stop and report "Nothing to ship — working tree is clean."

If changes exist on `main` or `master` branch directly: warn "You are on the main branch. Did you mean to create a feature branch first?" and pause for confirmation.

### Step 2: Identify project and load rules

From `pwd`, determine the project. Read `~/Documents/your-company/{project}/CLAUDE.md` for the correct test command, lint command, and any ship requirements.

Default commands by project:
- **task-assignment-service:** `poetry run pytest --tb=short .` / lint: `poetry run black --check .`
- **rx-os-backend:** `poetry run pytest --tb=short .` / lint: `poetry run black --check .`
- **rx-os-frontend:** `npm test -- --watchAll=false --passWithNoTests` / lint: `npm run lint`
- **wfm-microfrontends:** `npm test -- --watchAll=false --passWithNoTests` / lint: `npm run lint`

If the project CLAUDE.md specifies different commands, use those instead.

### Step 3: Run tests

Run the test command. If tests fail:
- Show the failure output
- Stop — do not proceed to lint or ship
- Report: "Tests failed. Fix the failures before shipping."

### Step 4: Run lint

Run the lint check. If lint fails:
- Attempt auto-fix: `poetry run black .` (Django) or `npm run prettier -- --write .` (frontend)
- Re-stage the auto-fixed files: `git add -u`
- Re-run lint check to confirm it passes
- If lint still fails after auto-fix: stop and report what needs manual attention

### Step 5: Brain review (inline)

Run /brain-review logic inline (do not spawn a separate skill). Load the diff and apply the Blink Checklist from `~/brain/.claude/skills/brain-review/references/blink-checklist.md`.

- If **Critical** issues found: stop and report them. Do not proceed to commit.
- If **Important** issues found: list them and ask "There are Important-level review findings. Ship anyway or fix first?"
- If no issues: proceed.

### Step 6: Commit

Extract the Jira ticket key from the branch name (e.g. `WFM-1234-feature-slug` → `WFM-1234`):
```bash
git branch --show-current | grep -oE '[A-Z]+-[0-9]+'
```

Stage all tracked modified files:
```bash
git add -u
```

Create the commit with message format `{KEY}: {descriptive summary}`:
```bash
git commit -m "WFM-1234: <summary of what this commit does>"
```

If no Jira key found in branch: use descriptive message without prefix.

### Step 7: Push

```bash
git push -u origin $(git branch --show-current)
```

If push fails (e.g. remote has newer commits): report the error and suggest `git pull --rebase` then retry. Do not force push.

### Step 8: Create GitHub PR

Call `mcp__github__create_pull_request` with:
- **title:** `{KEY}: {summary}` (same as commit message)
- **head:** current branch name
- **base:** `main` (or `master` if that's the default — check `git remote show origin`)
- **body:** structured PR template (below)

PR body template:
```markdown
## Summary
{1-3 bullet points describing what this PR does}

## Jira Ticket
{KEY}: {ticket summary}
{Jira ticket URL: https://your-workspace.atlassian.net/browse/{KEY}}

## Test Plan
- [ ] Unit tests pass (`poetry run pytest --tb=short .` or `npm test`)
- [ ] Lint passes
- [ ] {Any manual test steps specific to this feature}

## Notes
{Any deployment considerations, migration steps, or reviewer callouts}

🤖 Shipped with [Claude Code](https://claude.com/claude-code) + /brain-ship
```

### Step 9: Transition Jira ticket

Call `mcp__atlassian__jira_get_transitions` for the ticket key to get available transitions.

Find the transition that moves to "In Review" (or equivalent status — look for "Review", "Code Review", "PR Open").

Call `mcp__atlassian__jira_transition_issue` to move the ticket.

Add a comment to the ticket via `mcp__atlassian__jira_add_comment`:
```
PR opened: {PR URL}
```

### Step 10: Report

```
Shipped successfully!

  Branch:  {branch}
  Commit:  {sha} — "{commit message}"
  PR:      {PR URL}
  Jira:    {KEY} → In Review

Tests: {X passed}
Lint:  passed
Review: {N important findings noted — see above / clean}
```
