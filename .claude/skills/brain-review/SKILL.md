---
name: brain-review
version: 1.0.0
description: This skill should be used when the user wants to "review my code", "check my changes", "review before commit", "review this PR", or "check my diff". Runs a Blinkhealth-aware code review using the project's CLAUDE.md rules, the linked Jira ticket's acceptance criteria, and any relevant decisions from the brain knowledge base.
allowed-tools: Read, Glob, Grep, Bash, mcp__atlassian__jira_get_issue, Task
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`
- Current directory: !`pwd`
- Current branch: !`git branch --show-current 2>/dev/null || echo "not a git repo"`
- Git diff (staged + unstaged): !`git diff HEAD 2>/dev/null | head -500`

## Instructions

You are running /brain-review. Your job is to produce a confidence-scored, actionable code review grounded in project-specific rules, ticket acceptance criteria, and accumulated product decisions.

**Iron Law: No vague feedback.** Every issue must include file:line, a concrete fix, and a confidence score (0–100%).

### Step 1: Identify the project

From `pwd`, determine which Blinkhealth project is being reviewed:
- Contains `task-assignment-service` → task-assignment-service (Django 4.2, Python 3.9, DRF)
- Contains `rx-os-backend` → rx-os-backend (Django 3.x, Python 3.10)
- Contains `rx-os-frontend` → rx-os-frontend (React 18, CRA, Flow+TypeScript)
- Contains `wfm-microfrontends` → wfm-microfrontends (React 18, Webpack MF, MUI)

If not in a known project, note it and proceed with general best practices.

### Step 2: Load project CLAUDE.md

Read `~/Documents/your-company/{project}/CLAUDE.md` for project-specific rules, patterns, and anti-patterns.

If the project has its own review checklist or test conventions, note them — they take precedence over the general blink-checklist.

### Step 3: Extract Jira ticket from branch name

```bash
git branch --show-current 2>/dev/null
```

Parse the branch name for a Jira ticket key pattern (e.g. `WFM-1234-feature-slug` → `WFM-1234`).

If found: call `mcp__atlassian__jira_get_issue` to load the ticket's acceptance criteria and description. These become the functional correctness check — does the code actually implement what was specified?

If not found: note "No Jira ticket detected — skipping acceptance criteria check."

### Step 4: Brain knowledge lookup

Check for any relevant decisions that apply to the changed code:
```bash
sqlite3 ~/brain/data/brain.db "
SELECT title, file_path, summary
FROM knowledge_items
WHERE category = 'decisions'
AND (summary LIKE '%{changed_module}%' OR tags LIKE '%{topic}%')
LIMIT 5;
" 2>/dev/null || echo "brain.db not accessible"
```

Note any decisions that are directly relevant (e.g., "we decided to use bulk_create for all batch inserts in TAS").

### Step 5: Run the review

Read the full diff. Apply all checks below and score each finding with confidence (0–100%). Only surface findings with confidence ≥ 80%.

#### Acceptance Criteria Check
- Does the implementation actually fulfill the Jira ticket's acceptance criteria?
- Are edge cases from the AC covered?

#### Blink Checklist (load ~/brain/.claude/skills/brain-review/references/blink-checklist.md)

Apply every item in the checklist. Note which items pass and which fail.

#### General Code Quality
- Logic errors or off-by-one bugs
- Unused imports or dead code introduced
- N+1 query patterns (Django: check for missing `select_related`/`prefetch_related`)
- Exception handling — bare `except:` or swallowing exceptions silently
- Security: no secrets hardcoded, no SQL injection via string formatting, no unsafe `eval`/`exec`

### Step 6: Output the review

Group findings by severity. Only include items with confidence ≥ 80%.

```
## Code Review — {branch} — {date}

**Project:** {project}
**Jira ticket:** {KEY} — {summary}
**Files changed:** {count}

### ✗ Critical (must fix before merge)
- **{file}:{line}** [{confidence}%] {description}
  Fix: {concrete fix with code example if applicable}

### ⚠ Important (should fix)
- **{file}:{line}** [{confidence}%] {description}
  Fix: {concrete fix}

### Acceptance Criteria
- [x] {criterion 1} — covered by {function/file}
- [ ] {criterion 2} — NOT covered — {gap description}

### Blink Checklist
- [x] Tests added
- [x] Black formatting
- [ ] {failed item} — {location}

### Verdict
{APPROVE | REQUEST CHANGES | NEEDS DISCUSSION}
```

If no issues found: output "Review passed. No issues above 80% confidence threshold." and list which checklist items were verified.
