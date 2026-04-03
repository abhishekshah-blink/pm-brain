---
name: brain-ops-feedback
version: 1.0.0
description: This skill should be used when the user pastes Slack messages or text from ops describing a feature request, workflow gap, or improvement idea. It reads the relevant codebase, checks the knowledge base for context, and creates a well-structured Jira story ticket in the backlog. Trigger phrases: "ops feedback", "ops wants", "feature request from ops", paste from Slack.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__atlassian__jira_create_issue, mcp__atlassian__jira_search, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_get_project_components, Task
---

## Brain Context
Read ~/pm/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`
- ISO week: !`date +%G-W%V`

## Instructions

You are running /brain-ops-feedback. Ops teams are internal Blinkhealth staff using WFM tools (task assignment, scheduling, workforce management). Their feedback comes via Slack and describes feature gaps, workflow frustrations, or new capabilities they need.

**Your output is a Jira story ticket that an engineer can pick up and act on.**

### Step 1: Read the ops feedback

If $ARGUMENTS is empty, ask: "Paste the Slack message(s) from ops below:"

Parse the pasted text to extract:
- **Core request:** What do ops want to be able to do?
- **Current friction:** What's broken or missing today?
- **Affected workflow:** Which part of the WFM/TAS/rx-os workflow is this about?
- **Urgency signals:** Words like "urgent", "blocking", "every day", "can't" indicate higher priority

### Step 2: Identify the affected service

Determine which codebase(s) are involved:

| Ops workflow area | Likely service |
|---|---|
| Task assignment, task queues, agent routing | task-assignment-service |
| Scheduling UI, workforce dashboard, shift management | wfm-microfrontends |
| Prescription fulfillment, order status, patient UI | rx-os-frontend / rx-os-backend |
| Cross-service data or APIs | Multiple |

### Step 3: Search the codebase for context

Search the identified service for relevant code:
```bash
grep -r "<key_term>" ~/Documents/blinkhealth/<service>/ --include="*.py" --include="*.ts" --include="*.tsx" -l 2>/dev/null | head -10
```

Read 1-2 relevant files to understand the current implementation well enough to:
- Confirm the feature is actually missing (not just undiscovered)
- Identify where the change would likely be made
- Note any constraints or dependencies

### Step 4: Brain context lookup

Check if this feedback relates to existing knowledge:
```bash
sqlite3 ~/pm/brain/data/brain.db "
SELECT title, category, file_path, summary
FROM knowledge_items
WHERE (title LIKE '%<term>%' OR tags LIKE '%<term>%' OR summary LIKE '%<term>%')
AND category IN ('prd', 'features', 'decisions', 'domain')
LIMIT 5;
" 2>/dev/null
```

Also check if a similar story or epic already exists in Jira:
```bash
# via mcp__atlassian__jira_search with JQL:
# project = WFM AND text ~ "<feature_term>" AND issuetype in (Story, Epic) ORDER BY created DESC
```

If a duplicate exists, report it and ask whether to still create a new ticket or link to the existing one.

### Step 5: Draft the Jira story

Structure the story:

**Summary (title):** `[Ops Request] <concise feature description>` (max 80 chars)

**Description:**
```
## Ops Feedback
<quote the relevant Slack text verbatim>

## Problem Statement
<1-2 sentences: what ops can't do today and the impact>

## Proposed Solution
<what the feature should do — written from the user's perspective>

## Current Implementation Context
<1-2 sentences from your codebase investigation: where this would be built and any constraints>

## Related Knowledge
<links to any relevant PRDs, decisions, or features found in brain>
```

**Issue type:** Story
**Priority:** Assess from signals:
- "blocking" / "can't work" / affects every daily workflow → High
- Frequent friction but workaround exists → Medium  
- Nice to have → Low

**Labels:** Add the service label (e.g. `task-assignment-service`, `wfm-microfrontends`)

**Acceptance criteria:** Write 3-5 specific, testable criteria:
- Given [context], when [action], then [expected result]

**Story points:** Suggest an estimate:
- 1-2 pts: UI text change, config flag, simple field addition
- 3-5 pts: New UI component or API endpoint
- 8+ pts: New workflow, multi-service change

### Step 6: Confirm before creating

Show the drafted ticket and ask: "Shall I create this in Jira? Any changes?"

If confirmed: call `mcp__atlassian__jira_create_issue` with:
- project: WFM
- issuetype: Story
- summary, description, priority, labels

### Step 7: Auto-log

Append to the weekly activity log:
```bash
echo "- Ops feedback → Story: <JIRA_KEY> — <title> ($(date +%Y-%m-%d))" >> ~/pm/brain/knowledge/scratch/$(date +%G-W%V)-activity.md
```

Write the Slack feedback text + ticket link to `~/pm/brain/knowledge/features/<YYYY-MM-DD>-ops-<slug>.md` for future reference.

Report the Jira ticket key and URL.
