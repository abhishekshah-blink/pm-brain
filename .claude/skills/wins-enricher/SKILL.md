---
name: wins-enricher
version: 1.0.0
description: Background enrichment skill — processes ~/brain/knowledge/wins/pending.jsonl into structured win entries. Run nightly by cron. Safe to run manually. Idempotent.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_search, mcp__github__get_file_contents
---

## Instructions

You are the wins enricher. Your job is to process raw work signals from `~/brain/knowledge/wins/pending.jsonl` into structured, impact-focused win entries that can be used in performance reviews and promotion cases.

**This runs unattended. Be decisive. Do not ask for input. Use your best judgment on impact and framing.**

### Step 1: Check for pending entries

```bash
cat ~/brain/knowledge/wins/pending.jsonl 2>/dev/null
```

If the file is empty or missing: print "No pending wins to process." and stop.

### Step 2: Parse and group entries

Read all lines from pending.jsonl. Each line is a JSON object with fields like:
- `source`: `jira_transition` | `jira_created` | `github_pr_created` | `github_pr_merged` | `skill_brain_ship`
- `issue_key`: Jira ticket key (if applicable)
- `title`: PR title or ticket summary
- `transition`: transition name (for jira_transition entries)
- `date`: ISO date when captured

**Group related entries:** If the same `issue_key` appears across multiple entries within 7 days, treat them as one win (e.g., a PR creation + Jira transition to "In Review" for the same ticket = one shipment win).

**Skip noise:**
- `jira_transition` entries where transition is only "In Progress" or "To Do" — these are not wins yet
- Entries with no issue_key AND no meaningful title (blank or whitespace)

### Step 3: Deduplicate against existing wins

For each grouped entry, check if a win already exists:
```bash
grep -r "<issue_key>" ~/brain/knowledge/wins/ --include="*.md" -l 2>/dev/null | head -3
```

If a win file already references this issue_key: skip it (already processed).

### Step 4: Fetch context from Jira

For each entry with an `issue_key`, call `mcp__atlassian__jira_get_issue` to get:
- Summary (ticket title)
- Description (what was the work)
- Issue type (Bug, Story, Task, Epic)
- Labels
- Sprint name
- Resolution (if Done)
- Any linked PRs in comments

If no issue_key (e.g., a raw GitHub PR with no Jira link): use the PR title and repo as context.

### Step 5: Enrich each entry

For each valid, non-duplicate entry, produce:

**Project / Initiative:** Infer from Jira epic, ticket labels, or repo name.

**Situation / Problem:** What was the pain or gap? Infer from the ticket description.

**What I did:** Specific action. Lead with a strong verb. "Shipped", "Fixed", "Designed", "Coordinated", "Built", "Reduced". Be concrete.

**Outcome / Impact:** What changed because of this work? Infer from resolution notes, PR description, or ticket type. Be honest — if impact is unclear, say so in `follow_up_needed`.

**Evidence:** Jira link, PR number, branch, any numbers mentioned in the ticket.

**Competency theme** — pick one:
- `execution` — shipped, delivered, closed a bug/feature
- `ownership` — drove something proactively, beyond assigned scope
- `leadership` — influenced people, process, or direction
- `cross-functional` — aligned or unblocked another team
- `customer-impact` — changed something for customers, partners, or ops
- `process-improvement` — made a workflow faster, cleaner, less manual
- `growth` — new skill, increased scope, visibility, or judgment

**Impact strength** — be honest:
- `strong` — impact is concrete, quantifiable evidence exists or can be cited
- `moderate` — impact is real but not yet measured
- `needs-evidence` — valuable work but outcome is vague; must follow up

**Write two bullets:**

*Review bullet:* Action + concrete outcome + team/stakeholder context. Present tense.
> "Fixed claim rejection workflow bug in task-assignment-service, restoring correct task routing for partner ops and eliminating manual rework"

*Resume bullet:* Results-first, external. Metric or scope first, then action.
> "Resolved task routing failure in claim rejection workflow (Python/Django), improving processing accuracy for partner ops agents"

**Follow-up needed:** What number, outcome, or proof would make this entry stronger?
> "Quantify: how many tasks mis-routed per day? What was the manual rework time saved?"

Leave blank if impact is already strong.

### Step 6: Write win files

For each enriched entry, write to `~/brain/knowledge/wins/YYYY-MM-DD-<slug>.md`:

```yaml
---
title: <one-line summary of the work>
category: wins
tags: [<theme>, <project_label>]
created: <date from entry>
updated: <today>
jira_tickets: [<KEY if applicable>]
theme: <competency_theme>
impact_strength: strong|moderate|needs-evidence
---

## What I did
<specific action>

## Situation / Problem
<what was the gap or pain before>

## Outcome / Impact
<what changed>

## Evidence
- <Jira link, PR, numbers>

## Review bullet
<performance review version>

## Resume bullet
<resume/external version>

## Follow-up needed
<what proof or metric is still missing — or "None" if strong>
```

Slug format: lowercase, hyphens, max 6 words. e.g. `fix-claim-rejection-workflow-bug`

### Step 7: Update brain.db index

```bash
sqlite3 ~/brain/data/brain.db "
INSERT OR REPLACE INTO knowledge_items (title, category, tags, file_path, summary, created, updated)
VALUES ('<title>', 'wins', '<theme>', '<file_path>', '<review_bullet>', '<created_date>', '<today>');
" 2>/dev/null || true
```

### Step 8: Clear pending.jsonl

After all entries are processed:
```bash
> ~/brain/knowledge/wins/pending.jsonl
```

This truncates the file. The structured win files are now the source of truth.

### Step 9: Print summary

```
Wins enricher complete.

  Processed: N entries
  Wins saved: N files
  Skipped (duplicate): N
  Skipped (noise): N
  Needs follow-up evidence: N entries (listed below)

  Follow-up needed:
  - <title> → <what to chase>
```
