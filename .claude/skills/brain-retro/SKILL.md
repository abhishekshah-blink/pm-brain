---
name: brain-retro
version: 1.0.0
description: This skill should be used when the user wants to "run a retro", "weekly retro", "summarize my week", "write a retrospective", or "reflect on the sprint". Aggregates git commits, Jira sprint status, and new knowledge items from the past 7 days into a structured weekly retrospective written to ~/brain/knowledge/retros/.
allowed-tools: Read, Write, Bash, Glob, mcp__atlassian__jira_search, mcp__atlassian__jira_get_sprints_from_board, mcp__atlassian__jira_get_sprint_issues, Task
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`
- ISO week: !`date +%G-W%V`

## Dynamic Context (collected at skill start)

Git activity across all Blinkhealth repos this week:
!`for d in ~/Documents/blinkhealth/*/; do if git -C "$d" rev-parse --git-dir &>/dev/null 2>&1; then git -C "$d" log --oneline --since="7 days ago" --author="$(git config user.name 2>/dev/null || echo 'Abhishek')" 2>/dev/null | sed "s|^|[$(basename $d)] |"; fi; done`

New knowledge items indexed this week:
!`sqlite3 ~/brain/data/brain.db "SELECT title, category FROM knowledge_items WHERE indexed_at >= date('now', '-7 days') ORDER BY indexed_at DESC;" 2>/dev/null || echo "(brain.db not accessible)"`

## Instructions

You are running /brain-retro. Your job is to generate a structured weekly retrospective that combines what was built, what was learned, and what to focus on next week.

### Step 1: Pull Jira sprint data

Call `mcp__atlassian__jira_search` with JQL:
```
project = WFM AND sprint in openSprints() AND (assignee = currentUser() OR reporter = currentUser()) ORDER BY status ASC
```

Also search for tickets updated this week:
```
project = WFM AND updated >= -7d AND (assignee = currentUser() OR reporter = currentUser()) ORDER BY updated DESC
```

Categorize results into:
- **Completed this week** (status = Done, transitioned in last 7 days)
- **In Progress** (currently active)
- **Blocked** (has impediment flag or "Blocked" label)
- **Created this week** (new tickets opened)

### Step 2: Summarize git activity

From the dynamic context above, group commits by repo and create a readable summary:
- Skip merge commits and automated commits
- Group by repo → list of meaningful changes
- Note any PRs opened or merged (correlate with Jira ticket keys in branch names)

### Step 3: Load the retro template

Read `~/brain/.claude/skills/brain-retro/references/retro-template.md` to get the canonical template structure.

### Step 4: Draft the retrospective

Fill in the template:

```markdown
---
title: "Weekly Retro — {ISO week}"
category: retros
tags: [retro, {YYYY}, sprint]
created: {today}
updated: {today}
---

# Weekly Retro — {ISO week} ({date_range})

## What Shipped
{List completed Jira tickets with links and 1-line description}
{List PRs merged with repo + title}

## What's In Flight
{List in-progress tickets with current status and any blockers}

## Blockers & Friction
{List anything that slowed you down this week}
{Note: what removed the blocker, or what still needs resolution}

## What I Learned
{List new knowledge items added to ~/brain/ this week — with file links}
{Any domain knowledge or decisions captured}

## Top 3 Priorities for Next Week
1. {Highest priority — be specific}
2. {Second priority}
3. {Third priority}

## PM Insight of the Week
{One product observation worth writing down — a pattern noticed, a user insight,
a decision clarified, or a hypothesis validated/invalidated}
```

### Step 5: Write and index

Write the retro to `~/brain/knowledge/retros/{ISO-week}.md` (e.g. `2026-W13.md`).

Upsert into brain.db:
```bash
sqlite3 ~/brain/data/brain.db "
INSERT OR REPLACE INTO knowledge_items (file_path, category, title, summary, tags, created_at, updated_at, indexed_at)
VALUES (
  'knowledge/retros/{ISO-week}.md',
  'retros',
  'Weekly Retro — {ISO-week}',
  '{1-sentence summary of the week}',
  'retro,{year},sprint',
  '{today}',
  '{today}',
  datetime('now')
);
"
```

### Step 6: Report

Print the file path written and the retro content. Ask: "Anything to add before I save this? (PM insight, additional blockers, or next week priorities to update)"
