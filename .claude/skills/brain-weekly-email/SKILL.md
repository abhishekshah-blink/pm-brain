---
name: brain-weekly-email
version: 1.0.0
description: This skill should be used every Friday (or end of week) when the user wants to "write the weekly email", "draft the status email", "weekly status update", or "compile the week for the VP". Pulls Jira sprint data, brain knowledge items, and the weekly activity log to fill in the Blinkhealth weekly status email template.
allowed-tools: Read, Bash, Write, Glob, mcp__atlassian__jira_search, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_get_sprint_issues, mcp__atlassian__jira_get_sprints_from_board
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`
- ISO week: !`date +%G-W%V`

## Dynamic Context

Weekly activity log (what was done this week):
!`cat ~/brain/knowledge/scratch/$(date +%G-W%V)-activity.md 2>/dev/null || echo "(no activity log yet this week)"`

New decisions captured this week:
!`sqlite3 ~/brain/data/brain.db "SELECT title, file_path FROM knowledge_items WHERE category = 'decisions' AND indexed_at >= date('now', '-7 days');" 2>/dev/null`

## Instructions

You are running /brain-weekly-email. Every Friday you produce the VP status email using the Blinkhealth template. The email has 4 sections: decisions, blockers, what shipped (UX improvements this week), and what's coming next week.

**Read the full template:** `~/brain/.claude/skills/brain-weekly-email/references/email-template.html`

### Step 1: Pull this week's Jira data

**Completed tickets (Section 3 — what shipped):**
Call `mcp__atlassian__jira_search` with JQL:
```
project = WFM AND status changed to Done during (-7d, now()) ORDER BY updated DESC
```
For each ticket: get summary, ticket key, assignee, story points. Call `mcp__atlassian__jira_get_issue` for a brief description.

**In-progress + ready for release (Section 4 — what's coming):**
Call `mcp__atlassian__jira_search` with JQL:
```
project = WFM AND status in ("In Progress", "Ready for Release", "In Review") AND sprint in openSprints() ORDER BY priority ASC
```

### Step 2: Compile Section 1 — Key Decisions

Pull from:
1. Weekly activity log (decisions entries)
2. `knowledge_items` with category = `decisions` indexed this week
3. Ask: "Any key decisions made this week not captured in the brain yet? (or press Enter to skip)"

Format each decision as: **Decision: [title]** → Context: [2-3 sentences explaining what was decided and why]

If no decisions this week: omit this section.

### Step 3: Compile Section 2 — Blockers

Ask: "Any blockers to include this week? (describe or press Enter to skip)"

If yes, format as:
- **Blocker: [title]** → Impact: [who/what is affected] / Root Cause: [if known] / Plan: [resolution timeline]

If no blockers: omit this section.

### Step 4: Compile Section 3 — How UX improved this week

From the completed tickets:
1. Write a 3-5 sentence summary paragraph: what broad themes emerge from what shipped? (e.g., "automation gains", "key friction points removed", "reliability improvements")
2. List 3-5 bullet points highlighting the most impactful improvements
3. Build the completed tickets table: Overview (2-3 sentence context for each ticket), Jira link, comments summary, assignee, story points

For each ticket's "Overview" description: write 2-3 sentences explaining WHY it matters to ops users, not just what it does technically.

### Step 5: Compile Section 4 — How UX will improve next week

From the in-progress/ready tickets:
1. Write a brief summary paragraph of what's expected to ship
2. List 3-5 upcoming improvements as bullets
3. Build the upcoming tickets table: Overview, Jira link, current status, assignee, story points

### Step 6: Produce the filled email

Fill in the HTML template from `references/email-template.html`, replacing all `[PLACEHOLDER]` values with real content.

Save the filled email as:
- Markdown summary: `~/brain/knowledge/retros/$(date +%G-W%V)-weekly-email.md`
- HTML output: `~/brain/knowledge/retros/$(date +%G-W%V)-weekly-email.html`

Also output the **plain text version** directly to the conversation so you can copy-paste it immediately.

### Step 7: Auto-log

```bash
echo "- Weekly email drafted for VP ($(date +%Y-%m-%d))" >> ~/brain/knowledge/scratch/$(date +%G-W%V)-activity.md
```

Ask: "Ready to review. Copy the HTML from `~/brain/knowledge/retros/$(date +%G-W%V)-weekly-email.html` to send."
