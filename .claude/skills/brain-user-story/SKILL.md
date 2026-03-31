---
name: brain-user-story
version: 1.0.0
description: This skill should be used when the user wants to "create a user story", "write a story", "create a ticket", "write a Jira story", or turn a feature idea into a structured user story ticket. Produces a complete user story with persona, acceptance criteria, story points estimate, epic link, and service labels, then creates it in Jira.
allowed-tools: Read, Glob, Grep, Bash, Write, Task, mcp__atlassian__jira_create_issue, mcp__atlassian__jira_search, mcp__atlassian__jira_get_issue, mcp__atlassian__confluence_search
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`
- ISO week: !`date +%G-W%V`

## Instructions

You are running /brain-user-story. Your job is to produce a complete, engineering-ready user story that an engineer can read and implement without needing to ask clarifying questions.

**A great user story has:** a clear persona, a specific desired action, a meaningful outcome, testable acceptance criteria, and no ambiguity about scope.

### Step 1: Parse the input

If $ARGUMENTS contains a feature description, use it. If empty, ask:
"Describe the feature or user need. Include: who the user is, what they want to do, and why."

Also ask (if not clear from input):
- "Which service does this relate to? (task-assignment-service / wfm-microfrontends / rx-os-frontend / rx-os-backend)"
- "Do you have an epic key to link this to? (e.g. WFM-1234)"

### Step 2: Brain context lookup

Check for related PRDs, decisions, or existing features:
```bash
sqlite3 ~/brain/data/brain.db "
SELECT title, category, file_path, summary
FROM knowledge_items
WHERE (title LIKE '%<term>%' OR tags LIKE '%<term>%')
AND category IN ('prd', 'features', 'decisions', 'domain')
LIMIT 5;
" 2>/dev/null
```

Also search Jira for similar existing stories to avoid duplicates:
```
mcp__atlassian__jira_search JQL: project = WFM AND issuetype = Story AND text ~ "<feature_term>" ORDER BY created DESC
```

### Step 3: Codebase context (if service is known)

Read the relevant service's CLAUDE.md for technical constraints:
- `~/Documents/your-company/<service>/CLAUDE.md`

Do a quick grep to understand if any related code already exists:
```bash
grep -r "<key_feature_term>" ~/Documents/your-company/<service>/ --include="*.py" --include="*.ts" -l 2>/dev/null | head -5
```

### Step 4: Draft the story

**Title format:** `As a <persona>, I want to <action>, so that <benefit>`

Or if that feels forced for the context, use: `[Feature] <concise description>`

**Full story body:**

```markdown
## User Story
**As a** [ops agent / pharmacist / pharmacy manager / patient / admin]
**I want to** [specific action]
**So that** [outcome / benefit]

## Context
[1-3 sentences of background — why this matters, what's happening today without this feature]

## Acceptance Criteria
Given [initial context], when [user action], then [expected result]:

- [ ] AC1: Given [context], when [action], then [system behavior]
- [ ] AC2: Given [context], when [action], then [system behavior]
- [ ] AC3: Given [context], when [action], then [system behavior]
- [ ] AC4: (edge case) Given [context], when [action], then [system behavior]

## Out of Scope
- [explicit thing NOT included in this story]
- [another explicit exclusion]

## Technical Notes
[Implementation hints for engineering based on codebase investigation — optional but helpful]
[Any API endpoints, models, or components likely involved]

## Dependencies
[Other tickets or systems this depends on — or "None"]

## Definition of Done
- [ ] Acceptance criteria above are met
- [ ] Unit tests cover the new behavior
- [ ] No regression in existing [related workflow]
```

**Story points estimate:**

| Complexity | Points |
|---|---|
| Config change, copy update, simple field | 1 |
| Single component or API endpoint, straightforward | 2–3 |
| New workflow component, multi-field form, or moderate API work | 5 |
| Multi-service change, complex state, new data model | 8 |
| Large feature spanning multiple services | 13 (consider breaking down) |

**Priority:** Ask if not clear: "What priority should this be? (High / Medium / Low)"

**Labels:** Service label(s) based on affected codebase.

### Step 5: Confirm before creating

Show the full draft. Ask: "Shall I create this in Jira? Epic key to link? Any changes?"

If confirmed: call `mcp__atlassian__jira_create_issue` with all fields.

If epic key provided: also call `mcp__atlassian__jira_link_to_epic`.

### Step 6: Auto-log + save

Append to weekly activity log:
```bash
echo "- Story created: <JIRA_KEY> — <title> ($(date +%Y-%m-%d))" >> ~/brain/knowledge/scratch/$(date +%G-W%V)-activity.md
```

Save a copy to `~/brain/knowledge/features/<YYYY-MM-DD>-story-<slug>.md` for brain reference.
