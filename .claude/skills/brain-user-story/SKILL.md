---
name: brain-user-story
version: 1.0.0
description: This skill should be used when the user wants to "create a user story", "write a story", "create a ticket", "write a Jira story", or turn a feature idea into a structured user story ticket. Produces a complete user story with persona, acceptance criteria, story points estimate, epic link, and service labels, then creates it in Jira.
allowed-tools: Read, Glob, Grep, Bash, Write, Task, mcp__atlassian__jira_create_issue, mcp__atlassian__jira_search, mcp__atlassian__jira_get_issue, mcp__atlassian__confluence_search
---

## Brain Context
Read ~/pm/brain/.claude/PREAMBLE.md now. Follow all directives within it.
Read ~/pm/brain/knowledge/domain/jobs-to-be-done.md — used in Step 1.5.
Read ~/pm/brain/knowledge/domain/user-story-best-practices.md — used for INVEST check and splitting.
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

### Step 1.5: JTBD Framing

Before writing the story, clarify the job. Ask:

> "What job is the user hiring this feature to do?
> - Functional job: What specific task are they trying to complete? (verb + object + context)
> - Emotional job: How do they want to feel when it works? What feeling do they want to avoid?"

From the answer, write:
```
Functional job: [verb + object + context — solution-agnostic]
Emotional job: [state to achieve / avoid]
```

This becomes the "so that" clause of the story. A story without a grounded job statement is a task, not a story.

Reference: `~/pm/brain/knowledge/domain/jobs-to-be-done.md`

### Step 2: Brain context lookup

Check for related PRDs, decisions, or existing features:
```bash
sqlite3 ~/pm/brain/data/brain.db "
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
- `~/Documents/blinkhealth/<service>/CLAUDE.md`

Do a quick grep to understand if any related code already exists:
```bash
grep -r "<key_feature_term>" ~/Documents/blinkhealth/<service>/ --include="*.py" --include="*.ts" -l 2>/dev/null | head -5
```

### Step 4: Draft the story

Read the company ticket template: `~/.claude/blink-ai-tools/report_templates/roadmap_ticket.md`

**Title format:** `As a <persona>, I want to <action>, so that <benefit>`

Or if that feels forced for the context, use: `[Feature] <concise description>`

**Jira description body** (follow the company template structure):

```markdown
## Note: This is an AI generated document. Stakeholders are required to review the content before publishing the final version.

## Description

### Overview
[As a [persona], I want to [action], so that [outcome].

2-3 sentences of background — why this matters, what's happening today without this feature. Ground in the JTBD from Step 1.5.]

### Acceptance Criteria
- [ ] AC1: Given [context], when [action], then [system behavior]
- [ ] AC2: Given [context], when [action], then [system behavior]
- [ ] AC3: Given [context], when [action], then [system behavior]
- [ ] AC4: (edge case) Given [context], when [action], then [system behavior]

### Technical Requirements
- **Dependencies:** [other tickets or systems this depends on — or "None"]
- **Estimated Story Points:** [use table below]

### Additional Context
[Out of scope items, implementation hints from codebase investigation, API endpoints or models likely involved. Remove section if empty.]

---
*This ticket was created using the automated roadmap ticket creation process.*
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

### Step 4.5: INVEST Validation

Run the INVEST check before finalizing. Flag any criterion that fails.

| Criterion | Check | Pass? |
|---|---|---|
| **Independent** | Can this be built without waiting for another unfinished story? | |
| **Negotiable** | Is the solution open, or only the outcome locked? | |
| **Valuable** | Does this deliver value to a user or business by itself? | |
| **Estimable** | Can engineering estimate it without more unknowns? | |
| **Small** | Can it be completed in one sprint? | |
| **Testable** | Do the ACs allow a QA engineer to write a test without asking questions? | |

If **Small** fails (estimate ≥ 8 points): offer to split the story. Apply Lawrence's 9 patterns in order:
1. Workflow steps (thin end-to-end slice)
2. Operations (CRUD — separate Create/Read/Update/Delete)
3. Business rule variations
4. Data variations
5. Data entry methods (simple UI first)
6. Major effort (core + remaining)
7. Simple/complex
8. Defer performance
9. Spike (last resort — only if there's genuine technical unknowns)

Reference: `~/pm/brain/knowledge/domain/user-story-best-practices.md`

### Step 4.6: Epic Hypothesis (for new epics only)

If this story is defining a brand new epic (not a child of an existing one), write an epic hypothesis before creating:

```
Epic Hypothesis:
If we [specific action for this epic] for [target persona]
Then we will [measurable outcome]

We will test this assumption by:
- [Smallest experiment — prototype / concierge / A/B test]

We know it's valid if within [2-4 weeks] we observe:
- [Quantitative signal]
- [Qualitative signal]
```

Ask: "Should I save this as an epic hypothesis in brain.db before creating the story?"

### Step 5: Confirm before creating

Show the full draft. Ask: "Shall I create this in Jira? Epic key to link? Any changes?"

If confirmed: call `mcp__atlassian__jira_create_issue` with all fields.

If epic key provided: also call `mcp__atlassian__jira_link_to_epic`.

### Step 6: Auto-log + save

Append to weekly activity log:
```bash
echo "- Story created: <JIRA_KEY> — <title> ($(date +%Y-%m-%d))" >> ~/pm/brain/knowledge/scratch/$(date +%G-W%V)-activity.md
```

Save a copy to `~/pm/brain/knowledge/features/<YYYY-MM-DD>-story-<slug>.md` for brain reference.
