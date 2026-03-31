---
name: brain-ops-bug
version: 1.0.0
description: This skill should be used when the user pastes Slack messages from ops describing a bug, unexpected behavior, system error, or service disruption. It investigates the codebase and past incidents, assesses severity, and creates a structured Jira bug ticket. Trigger phrases: "ops reported a bug", "ops bug", "bug from ops", paste of ops Slack describing broken behavior.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__atlassian__jira_create_issue, mcp__atlassian__jira_search, Task
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`
- ISO week: !`date +%G-W%V`

## Instructions

You are running /brain-ops-bug. Ops have reported something that isn't working. Your job is to understand the bug, find evidence in the codebase and past incidents, assess severity, and produce a ticket that gives engineering enough context to fix it fast.

**Iron Law: Evidence before severity.** Don't guess P1 vs P3 — infer from impact signals and codebase context.

### Step 1: Read the bug report

If $ARGUMENTS is empty, ask: "Paste the Slack message(s) from ops describing the bug:"

Parse to extract:
- **What broke:** The specific behavior that's wrong
- **What was expected:** What should have happened
- **When it started:** Any time signals ("since yesterday", "since deploy", "always")
- **Who is affected:** All ops? One person? A specific workflow?
- **Frequency:** Intermittent or consistent?
- **Any error messages:** Exact wording if ops shared it

### Step 2: Identify the affected service

Map the bug to the most likely service (same mapping as brain-ops-feedback):
- Task assignment, routing, queues → task-assignment-service
- Scheduling UI, workforce dashboard → wfm-microfrontends
- Prescriptions, orders, patient-facing → rx-os-frontend / rx-os-backend

### Step 3: Check past incidents in brain

Search for similar past incidents:
```bash
sqlite3 ~/brain/data/brain.db "
SELECT title, file_path, summary
FROM knowledge_items
WHERE category = 'oncall'
AND (title LIKE '%<term>%' OR tags LIKE '%<term>%' OR summary LIKE '%<term>%')
ORDER BY updated_at DESC
LIMIT 5;
" 2>/dev/null
```

Read any matching oncall files. Note: has this bug happened before? What was the root cause last time? Did we fully fix it or just mitigate?

Also search Jira for similar past bugs:
```bash
# mcp__atlassian__jira_search JQL:
# project = WFM AND issuetype = Bug AND text ~ "<error_term>" ORDER BY created DESC
```

### Step 4: Investigate the codebase

Search for the error message or affected code path:
```bash
grep -r "<error_string_or_key_term>" ~/Documents/blinkhealth/<service>/ \
  --include="*.py" --include="*.ts" --include="*.tsx" -n 2>/dev/null | head -20
```

Read relevant files. Look for:
- The code path that handles this workflow
- Any error handling that would produce this symptom
- Recent git changes to this area: `git -C ~/Documents/blinkhealth/<service>/ log --oneline -10 -- <relevant_file>`

Load the debug patterns reference:
Read `~/brain/.claude/skills/brain-investigate/references/debug-patterns.md` for Blinkhealth-specific patterns that match this bug type.

### Step 5: Assess severity

| Signal | Severity |
|---|---|
| Ops cannot do their core job / data loss / patient impact | P1 — Critical |
| Major workflow broken, no workaround available | P2 — High |
| Feature broken but workaround exists | P3 — Medium |
| Minor UI issue, cosmetic, edge case | P4 — Low |

Also consider frequency: "happens every time" → higher severity than "happened once".

### Step 6: Draft the Jira bug ticket

**Summary:** `[Bug] <service>: <concise description>` (max 80 chars)

**Description:**
```
## Bug Report (from Ops)
<quote the Slack text verbatim>

## Expected Behavior
<what should happen>

## Actual Behavior
<what is happening>

## Steps to Reproduce
1. <step 1>
2. <step 2>

## Investigation Findings
<What you found in the codebase — suspected code path, any relevant recent changes>

## Past Incidents
<Link to any similar incidents found in knowledge/oncall/ or past Jira bugs>

## Affected Users
<Who is impacted and how broadly>
```

**Issue type:** Bug
**Priority:** P1/P2/P3/P4 based on severity assessment
**Labels:** Service label + `ops-reported`

### Step 7: Confirm before creating

Show the drafted ticket and ask: "Shall I create this in Jira? Any changes to severity or description?"

If confirmed: call `mcp__atlassian__jira_create_issue`.

If P1/P2: ask "This looks urgent — do you want me to also send a Jira comment to the on-call engineer or transition to the current sprint?"

### Step 8: Auto-log + knowledge capture

Append to weekly activity log:
```bash
echo "- Bug triaged → <JIRA_KEY> (P<N>): <title> ($(date +%Y-%m-%d))" >> ~/brain/knowledge/scratch/$(date +%G-W%V)-activity.md
```

If a new root cause or pattern was found, offer to write to `~/brain/knowledge/oncall/`:
"Should I save the investigation findings to knowledge/oncall/ for future reference?"
