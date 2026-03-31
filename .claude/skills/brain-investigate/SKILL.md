---
name: brain-investigate
version: 1.0.0
description: This skill should be used when the user wants to "debug this error", "investigate a bug", "root cause this", "understand why X is failing", or provides an error message, stack trace, or Jira bug ticket key. Pulls knowledge base context, Jira ticket details, past incidents, and codebase context to produce a root cause analysis with a concrete fix.
allowed-tools: Read, Glob, Grep, Bash, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_search, Write, Task
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`
- Current directory: !`pwd`

## Instructions

You are running /brain-investigate. Your job is to produce a root cause analysis — not a guess. Evidence first, hypothesis second, fix third.

**Iron Law: No fixes without investigation.** Do not propose a fix until you have identified the root cause with evidence. A fix without root cause understanding is a patch that will recur.

### Step 1: Parse the input

From $ARGUMENTS, determine what you're investigating:
- **Jira ticket key** (e.g. `WFM-1234`) → load the ticket
- **Error message or stack trace** → treat as the symptom to trace
- **Description** (e.g. "task assignment is timing out on bulk operations") → extract keywords

### Step 2: Jira ticket lookup

If a ticket key is present: call `mcp__atlassian__jira_get_issue` for full detail — description, steps to reproduce, comments, linked issues, labels.

If no ticket key but the description sounds like a known issue: search `mcp__atlassian__jira_search` with JQL `project = WFM AND text ~ "{keywords}" AND issuetype = Bug ORDER BY created DESC` to find any existing bug reports.

### Step 3: Brain knowledge lookup

Search for prior knowledge on this topic:

```bash
# Check for past incidents with similar symptoms
sqlite3 ~/brain/data/brain.db "
SELECT title, file_path, summary
FROM knowledge_items
WHERE category = 'oncall'
AND (title LIKE '%{term}%' OR tags LIKE '%{term}%' OR summary LIKE '%{term}%')
ORDER BY updated_at DESC
LIMIT 5;
" 2>/dev/null

# Check domain knowledge (SLA, service behavior)
sqlite3 ~/brain/data/brain.db "
SELECT title, file_path, summary
FROM knowledge_items
WHERE category IN ('domain', 'decisions')
AND (title LIKE '%{term}%' OR tags LIKE '%{term}%')
LIMIT 5;
" 2>/dev/null
```

Read the matching oncall files in full — they contain past root causes, mitigations, and "what we learned" sections that are directly relevant.

### Step 4: Load debug patterns

Read `~/brain/.claude/skills/brain-investigate/references/debug-patterns.md` for Blinkhealth-specific patterns to watch for.

### Step 5: Codebase investigation

Identify the most likely affected service from context. Search the codebase:

```bash
# Find the error message in code
grep -r "{error_string}" ~/Documents/blinkhealth/ --include="*.py" --include="*.ts" --include="*.tsx" -l 2>/dev/null | head -10

# Find related functions
grep -r "{relevant_function_name}" ~/Documents/blinkhealth/ --include="*.py" -n 2>/dev/null | head -20
```

Read the relevant files — trace the call stack from the symptom back toward the root cause. Look for:
- The specific code path that produces the error
- Any recent changes to that code path (`git log --oneline -20 -- {file}`)
- Configuration or environment dependencies
- Race conditions, missing locks, improper error handling

### Step 6: Formulate root cause analysis

Structure your analysis:

```
## Investigation: {title}

**Ticket:** {KEY} — {summary}
**Date:** {today}
**Service:** {service}

### Symptom
{What is actually happening — observable behavior}

### Root Cause
{The actual underlying cause — be specific. Bad: "there's a race condition". 
Good: "task_assignment/services.py:142 acquires the Redis lock after reading the 
current assignment count, so two concurrent requests can both see count=0 and both 
assign the same task."}

### Evidence
- Code: `{file}:{line}` — {what the code does that causes this}
- Prior incident: {link to knowledge/oncall/ file if applicable}
- Jira: {ticket comment or description that confirms this}
- Logs: {log pattern to look for}

### Steps to Reproduce
1. {step 1}
2. {step 2}

### Proposed Fix
{Concrete fix with code}

**File:** `{file}:{line}`
```python
# Before
{existing code}

# After  
{fixed code}
```

### Prevention
{What should be added to docs/tests/monitoring to prevent recurrence}
```

### Step 7: Offer to write an incident note

Ask: "Should I write this investigation to ~/brain/knowledge/oncall/ for future reference?"

If yes, write `~/brain/knowledge/oncall/{YYYY-MM-DD}-{slug}.md` and upsert into brain.db:

```bash
sqlite3 ~/brain/data/brain.db "
INSERT OR REPLACE INTO knowledge_items (file_path, category, title, summary, tags, created_at, updated_at, indexed_at)
VALUES ('knowledge/oncall/{YYYY-MM-DD}-{slug}.md', 'oncall', '{title}', '{1-sentence summary}', '{service},{error_type},{component}', '{today}', '{today}', datetime('now'));
"
```
