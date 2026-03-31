---
name: wins
version: 1.0.0
description: Manually capture and enrich a work win. Use when you want to log something that wasn't auto-captured by hooks — a conversation that led to a key decision, a design you drove, a process you improved. Accepts a raw note or a Jira ticket key.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_search
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`
- ISO week: !`date +%G-W%V`

## Instructions

You are running /wins. Your job is to turn a raw work note into a structured, impact-focused win entry — one that can be reused directly in a performance review, promotion case, or resume.

**The goal is not to log activity. It is to capture impact.**

### Step 1: Get the input

If $ARGUMENTS looks like a Jira key (e.g. `WFM-1234`): call `mcp__atlassian__jira_get_issue` and use the ticket as context.
If $ARGUMENTS is a raw note: use it as-is.
If empty: ask "What did you do? (raw note or Jira key — either works)"

### Step 2: Check for duplicates

```bash
grep -r "<key_term_or_jira_key>" ~/brain/knowledge/wins/ --include="*.md" -l 2>/dev/null | head -3
```

If a win already exists for this work: show it and ask "A win entry already exists for this. Update it or create a new one?"

### Step 3: Load related context from brain

```bash
sqlite3 ~/brain/data/brain.db "
SELECT title, category, file_path, summary
FROM knowledge_items
WHERE (title LIKE '%<term>%' OR tags LIKE '%<term>%')
AND category IN ('wins', 'prd', 'features', 'decisions')
ORDER BY updated_at DESC LIMIT 5;
" 2>/dev/null
```

### Step 4: Enrich

Extract or infer:

**Project / Initiative:** What project, epic, or initiative does this belong to?
**Situation / Problem:** What was the gap or pain before you acted?
**What I did:** Specific action. Strong verb. "Shipped", "Fixed", "Coordinated", "Designed", "Reduced".
**Collaborators:** Who was involved? Other teams, stakeholders, engineers?
**Outcome / Impact:** What got better? What changed?
**Evidence:** Jira links, PR numbers, Confluence docs, data, before/after

**Competency theme** — pick one:
| Theme | When it applies |
|---|---|
| `execution` | Shipped, delivered, closed a bug or feature |
| `ownership` | Drove proactively, beyond assigned scope |
| `leadership` | Influenced people, process, or direction |
| `cross-functional` | Aligned or unblocked another team |
| `customer-impact` | Changed something for customers, partners, or ops |
| `process-improvement` | Made a workflow faster, cleaner, less manual |
| `growth` | New skill, increased scope, visibility, or judgment |

**Impact strength:**
- `strong` — concrete, quantifiable or very specific; evidence is solid
- `moderate` — real and meaningful, but not yet measured
- `needs-evidence` — valuable work but vague outcome; follow-up required

**Write two bullets:**

*Review bullet* — action + outcome + stakeholder context:
> "Improved prior auth handoff operations by creating a standardized tracking process across Ops and Product, increasing issue visibility and reducing coordination overhead"

*Resume bullet* — results-first, external:
> "Drove cross-functional process improvement for prior authorization handoffs by designing a standardized tracking workflow, improving operational visibility and reducing manual follow-up friction"

**Follow-up needed:** What metric or proof would make this bulletproof? Leave blank if strong.

### Step 5: Show and confirm

Display the enriched entry. Call out:
- Impact strength and why
- What follow-up is still needed (if any)
- Which competency theme this maps to and whether it fills a gap in recent wins

Ask: "Save this? Any changes?"

### Step 6: Save

Write to `~/brain/knowledge/wins/<YYYY-MM-DD>-<slug>.md`:

```yaml
---
title: <one-line summary>
category: wins
tags: [<theme>, <project>]
created: <today>
updated: <today>
jira_tickets: [<KEY if applicable>]
theme: <competency_theme>
impact_strength: strong|moderate|needs-evidence
---

## What I did
...

## Situation / Problem
...

## Outcome / Impact
...

## Evidence
...

## Review bullet
...

## Resume bullet
...

## Follow-up needed
...
```

Index in brain.db:
```bash
sqlite3 ~/brain/data/brain.db "
INSERT OR REPLACE INTO knowledge_items (title, category, tags, file_path, summary, created, updated)
VALUES ('<title>', 'wins', '<theme>', '<file_path>', '<review_bullet>', '<today>', '<today>');
" 2>/dev/null || true
```

Print: `Win saved → knowledge/wins/<filename>.md [<theme>] [<impact_strength>]`
