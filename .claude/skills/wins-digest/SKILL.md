---
name: wins-digest
version: 1.0.0
description: Synthesizes wins entries into review materials. Accepts scope argument: weekly (default for cron), monthly, quarterly, or promo. Weekly runs automatically every Friday. quarterly and promo are the high-value outputs for review season and promotion cases.
allowed-tools: Read, Glob, Grep, Bash, Write
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
- Current date: !`date +%Y-%m-%d`
- ISO week: !`date +%G-W%V`

## Instructions

You are running /wins-digest. Your job is to synthesize accumulated work wins into polished materials for review season, 1:1s, and promotion cases.

**Scope from $ARGUMENTS:** `weekly` | `monthly` | `quarterly` | `promo`
Default to `weekly` if called by cron with no scope. Default to `quarterly` if run interactively with no argument.

### Step 1: Load wins in scope

Determine date range:
- `weekly` → last 7 days
- `monthly` → last 30 days
- `quarterly` → last 90 days
- `promo` → last 180 days (6 months)

```bash
# Find wins files in scope
find ~/brain/knowledge/wins/ -name "*.md" -not -path "*/digests/*" -newer /dev/null 2>/dev/null
```

Then filter by `created` date in the frontmatter. Read each file in full.

If no wins exist in scope:
- `weekly`: "No wins captured this week. Check if pending.jsonl has unprocessed entries."
- Others: "No wins found for this period. Run `/brain-sync sprint` to pull Jira context, or add wins manually with `/wins`."

### Step 2: Analyze

Across all entries in scope, extract:

**By impact strength:**
- Strong entries (cite by title)
- Moderate entries
- Needs-evidence entries (flag these — evidence still missing)

**By competency theme:**
Count entries per theme: execution, ownership, leadership, cross-functional, customer-impact, process-improvement, growth

**Patterns:**
- What types of work dominate this period?
- Any consistent collaborators or teams?
- Any emerging narrative? (e.g., "5 of 8 wins involve cross-team unblocking")

---

### WEEKLY OUTPUT

Save to `~/brain/knowledge/wins/digests/<YYYY-WW>.md`.

```markdown
# Wins: <YYYY-WW>

## Top wins this week
<3-5 bullet points, one per strong/moderate win>
- <review bullet from win entry>

## Theme breakdown
<text bar chart>
execution      ████████ (4)
cross-functional ████ (2)
ownership      ██ (1)

## Evidence to chase
<All entries where impact_strength = needs-evidence OR follow_up_needed is not blank.
For each, read the win entry's Collaborators and Evidence fields to suggest a specific action.
Format as checkboxes so this is a real to-do list, not a passive note.>
- [ ] **<title>** — <follow_up_needed>
      → <specific action: who to ask, which Jira ticket to update, what system to pull data from>

<If no entries need evidence: "All wins this week have sufficient evidence.">

## 1:1 talking point
<One sentence summarizing the week's most impactful work — ready to say in a 1:1>
```

---

### MONTHLY OUTPUT

Show in conversation + save to `~/brain/knowledge/wins/digests/<YYYY-MM>.md`.

```markdown
# Wins: <Month YYYY>

## Top 5 accomplishments
<Ranked by impact_strength, then by theme variety>

## Theme distribution
<text bar chart across all themes>

## Strongest bullets
<The 3-5 entries with strong impact_strength — review bullets ready to use>

## Evidence gaps
<All entries where follow_up_needed is not blank>

## Patterns emerging
<1-2 sentences on what your work this month signals about your strengths>
```

---

### QUARTERLY OUTPUT

Show in conversation + save to `~/brain/knowledge/wins/digests/<YYYY-QN>.md`.

This is the primary review prep output.

```markdown
# Wins: Q<N> <YYYY>

## Executive summary
<2-3 sentences: what you shipped, who it helped, what the impact was. Write this as if opening a performance review conversation.>

## Top 10 accomplishments
<Ranked. For each: date, one-line summary, impact_strength indicator>
1. [strong] <review bullet>
2. [moderate] <review bullet>
...

## By competency

### Execution
<2-4 review bullets>

### Ownership
<bullets or "No entries this quarter — consider noting proactive work next quarter">

### Leadership
<bullets>

### Cross-functional impact
<bullets>

### Customer / partner impact
<bullets>

### Process improvement
<bullets>

### Growth
<bullets>

## Draft self-review
<2-3 sentences per competency where you have strong entries. Write in first person, specific, action-oriented.>

## Manager talking points
<5 bullets your manager could use when advocating for you:>
- Shipped X, which did Y
- Unblocked Z team by doing W
- ...

## Resume update suggestions
<The 3-5 strongest resume bullets from this quarter — external-facing, results-first>

## Evidence gaps to close before review
<Any needs-evidence entries + what to chase>

## Theme distribution
<text bar chart>
```

---

### PROMO OUTPUT

Show in conversation + save to `~/brain/knowledge/wins/digests/<YYYY>-promo.md`.

This is a promotion case, not a self-review. Different structure.

```markdown
# Promotion Case: <YYYY>

## Narrative arc
<3-5 sentences telling the story of your growth: where you started, what you drove, what impact you created, how your scope or influence grew. This is the opening paragraph of a promo doc.>

## Strongest examples by competency
<For each theme where you have strong entries: 1-2 bullets with the most promotable examples.
Prioritize: leadership, ownership, cross-functional, customer-impact over pure execution.>

### Leadership
- <strongest example>

### Ownership
- <strongest example>

### Cross-functional impact
- <strongest example>

[continue for themes with entries]

## What's missing from a promotion case
<Honest assessment: which competencies are under-evidenced? What types of work would strengthen the case?
e.g. "Strong on execution and cross-functional. Thin on leadership and strategic impact. 0 entries showing direction-setting or influence without authority.">

## Evidence gaps
<All entries where follow_up_needed is not blank — these weaken the case>

## Suggested promo talking points
<5 bullets for a promo conversation with your manager or skip-level>
```

### Step 3: Save and confirm

Save the digest to the appropriate path. Print the output in full to the conversation.

End with:
```
DONE — <scope> digest saved to knowledge/wins/digests/<filename>.md
<N> wins analyzed | <N> strong | <N> needs-evidence
```
