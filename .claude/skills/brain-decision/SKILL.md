---
name: brain-decision
version: 1.0.0
description: Log a product, technical, or process decision with context, alternatives, rationale, and a revisit trigger. Fills knowledge/decisions/ — the most referenced but most neglected folder for PMs. Use whenever a non-obvious call was made that someone might question later.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_search
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`
- ISO week: !`date +%G-W%V`

## Instructions

You are running /brain-decision. Your job is to turn a messy "we decided X" note into a clean, searchable decision record that future-you will actually find useful.

**A good decision log is not a meeting summary. It is the answer to: "Why did we do it this way?"**

### Step 1: Get the input

If $ARGUMENTS contains a Jira key → call `mcp__atlassian__jira_get_issue` for context.
If $ARGUMENTS is a description → use it as the starting point.
If empty → ask: "What decision was made? (one sentence is fine to start)"

### Step 2: Check for duplicates

```bash
sqlite3 ~/brain/data/brain.db "
SELECT title, file_path FROM knowledge_items
WHERE category = 'decisions'
AND (title LIKE '%<key_term>%' OR tags LIKE '%<key_term>%')
ORDER BY updated_at DESC LIMIT 3;
" 2>/dev/null
```

If a related decision exists: show it and ask "Update this existing record or log a new separate decision?"

### Step 3: Classify the decision type

| Type | When to use |
|---|---|
| `product` | Feature scope, what to build vs. cut, UX tradeoffs, prioritization calls |
| `technical` | Architecture, tech stack, data model, implementation approach |
| `process` | How the team operates, workflow changes, tooling |
| `strategic` | Product direction, make vs. buy, resourcing, roadmap sequencing |

### Step 4: Gather the key fields

Ask only what you don't already know from the input. Be efficient — one focused question if needed, not a form.

**Decision** (required): One clear sentence. "We decided to X."

**Context** (required): Why did this come up? What was the situation or problem forcing a choice?

**Alternatives considered**: What else was on the table? At minimum two options. If the user only gives you one, prompt: "What was the alternative you ruled out?"

**Rationale**: Why this option? Key factors that tipped the decision. Be honest — "faster to ship" is a legitimate reason.

**Stakeholders**: Who made or agreed to this decision?

**Tradeoffs / risks**: What was given up or accepted? Every real decision has a cost.

**Revisit when**: What specific signal would cause you to revisit this? This is the most important field — it turns a decision into a living record instead of a permanent accident.

If the user can't articulate a revisit trigger, suggest one based on the tradeoffs.

### Step 5: Write the decision record

Save to `~/brain/knowledge/decisions/<YYYY-MM-DD>-<slug>.md`:

```markdown
---
title: Decision: <one-line summary>
category: decisions
tags: [<decision_type>, <project_tag>]
created: <today>
updated: <today>
jira_tickets: [<KEY if applicable>]
decision_type: product|technical|process|strategic
---

## Decision
<One clear sentence: "We decided to X.">

## Context
<Why this came up. The situation or constraint that forced a choice.>

## Alternatives considered
1. **<Option A>** — <brief description and why it was ruled out>
2. **<Option B>** — <brief description and why it was ruled out>

## Rationale
<Why this option. The 2-3 key factors. Be direct.>

## Stakeholders
<Who made or signed off on this.>

## Tradeoffs / risks
<What was accepted or given up. Be honest.>

## Revisit when
<Specific signal that would trigger revisiting: a user complaint threshold, a metric, a capability becoming available, a constraint being removed.>

## Related
<Jira tickets, Confluence pages, related decisions>
```

### Step 6: Index and confirm

```bash
sqlite3 ~/brain/data/brain.db "
INSERT OR REPLACE INTO knowledge_items (title, category, tags, file_path, summary, created, updated)
VALUES ('<title>', 'decisions', '<decision_type>,<project_tag>', '<file_path>', '<rationale_one_sentence>', '<today>', '<today>');
" 2>/dev/null || true
```

Print: `Decision logged → knowledge/decisions/<filename>.md [<decision_type>]`

Then show the user the "Revisit when" field specifically:
> "Saved. Revisit trigger: <revisit_when>"

This is the field most people forget — surfacing it confirms it was captured.
