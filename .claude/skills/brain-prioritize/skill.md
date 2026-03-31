---
name: brain-prioritize
version: 1.0.0
description: This skill should be used when the user wants to "help me prioritize", "which prioritization framework should I use", "prioritize my backlog", "score these features", "what should we build first", or "how do I decide between X and Y". Guides through framework selection, backlog scoring, and financial validation.
allowed-tools: Read, Glob, Grep, Bash, Write, Task, mcp__atlassian__jira_search, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_get_sprint_issues, mcp__atlassian__jira_get_sprints_from_board
---

## Brain Context
Read ~/brain/.claude/PREAMBLE.md now. Follow all directives within it.
Read ~/brain/knowledge/domain/prioritization-frameworks.md — this is your framework reference.
Read ~/brain/knowledge/domain/feature-investment-framework.md — use for financial validation of top items.
- Current date: !`date +%Y-%m-%d`

## Instructions

You are running /brain-prioritize. Your job is to match the right prioritization framework to the current situation, apply it to the user's backlog or feature list, and surface the top items with clear rationale.

**Iron Law: Scores inform judgment — they don't replace it. Always show the reasoning, not just the number.**

---

### Step 1: Parse arguments

Extract from $ARGUMENTS:
- **Feature list or backlog description** (if provided inline)
- **Specific goal** (e.g., "for Q2 planning", "for this sprint", "between these 5 features")
- **Jira context** (sprint board or ticket keys)

If no arguments: ask "What are you trying to prioritize? Options: (1) current sprint backlog, (2) a specific list of features you'll paste, (3) help me pick a framework for a planning session."

---

### Step 2: Load brain context

Check the brain for existing prioritization decisions and roadmap context:
```bash
sqlite3 ~/brain/data/brain.db "
SELECT category, title, file_path, summary
FROM knowledge_items
WHERE category IN ('decisions', 'features', 'prd', 'operating-plans')
ORDER BY updated_at DESC
LIMIT 8;
" 2>/dev/null
```

**Load Jira backlog** (if applicable):
- If "current sprint" or "sprint backlog": call `mcp__atlassian__jira_get_sprints_from_board`, then `mcp__atlassian__jira_get_sprint_issues` for the active sprint
- If specific ticket keys: call `mcp__atlassian__jira_get_issue` for each
- If searching: call `mcp__atlassian__jira_search` with JQL: `project = WFM AND status != Done AND sprint in openSprints() ORDER BY priority DESC`

---

### Step 3: Framework Selection (4 adaptive questions)

Ask all 4 in one message. Offer numbered options for each.

> "To recommend the right framework, I need to understand your context:
>
> **1. Product stage?**
> (a) Pre-PMF — still finding what works
> (b) Early PMF — validating growth levers
> (c) Mature — optimizing a known product
> (d) Portfolio / multi-product
>
> **2. Team context?**
> (a) Small, mostly aligned team
> (b) Cross-functional, generally aligned
> (c) Multi-stakeholder, some misalignment
> (d) Large org, competing priorities
>
> **3. What's the decision you need to make?**
> (a) Too many ideas, need to narrow down
> (b) Stakeholders disagree — need a shared framework
> (c) Want a data-driven, defensible ranking
> (d) Need to sequence a roadmap or plan releases
>
> **4. How much data do you have?**
> (a) Minimal — mostly intuition and qualitative feedback
> (b) Some — traffic/usage data, a few user interviews
> (c) Rich — revenue impact data, churn analysis, NPS"

---

### Step 4: Recommend a Framework

Based on answers, recommend the best framework with rationale. Reference `domain/prioritization-frameworks.md` for full definitions.

**Decision logic:**
- Pre-PMF + small team + too many ideas + minimal data → **ICE** (fast, low overhead)
- Early/mature PMF + cross-functional + data-driven + some data → **RICE**
- Multi-stakeholder + misalignment + any stage → **Weighted Scoring** or **Buy-a-Feature**
- Mature product + feature investment decisions → **Kano + Feature Investment Framework**
- Release scoping with constrained time → **MoSCoW**
- Portfolio / large org with time-sensitivity → **Cost of Delay / WSJF**

Explain:
1. Why this framework fits their situation
2. What inputs they'll need to score items
3. One alternative framework if they prefer lower overhead

---

### Step 5: Score the Backlog

**Build the scoring table** based on the recommended framework.

For **RICE:**
```markdown
| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---|---|---|---|---|---|
| [Feature 1] | [users/qtr] | [3/2/1/0.5/0.25] | [100/80/50%] | [person-months] | [R×I×C/E] |
```

For **ICE:**
```markdown
| Feature | Impact (1-10) | Confidence (1-10) | Ease (1-10) | ICE Score |
|---|---|---|---|---|
| [Feature 1] | | | | [avg] |
```

For **MoSCoW:**
```markdown
| Feature | MoSCoW | Rationale |
|---|---|---|
| [Feature 1] | Must Have | [why it's essential for this release] |
```

If the user provided features: populate the table with your best estimates and flag which estimates need validation.
If pulling from Jira: populate from ticket data.

Show the scored table. Ask: "Any of these scores feel off? Let's adjust before finalizing."

---

### Step 6: Financial Spot-Check on Top Items

For the top 3 scored items, run a quick Feature Investment check (reference `domain/feature-investment-framework.md`):

```
[Feature name]:
- Revenue connection: [direct / retention / conversion / expansion / none]
- Estimated dev cost: [person-weeks × blended rate]
- Rough ROI: [revenue/cost ratio or LTV impact]
- Strategic value: [high / medium / low — one sentence why]
- Pattern: [Build Now / Build for Strategic Reasons / Build Later / Don't Build]
```

Flag any top-scored item that maps to "Don't Build" — this is a signal that the score is driven by internal preference rather than user value.

---

### Step 7: Output — Prioritized List with Rationale

```markdown
## Prioritized Backlog — {date}

**Framework used:** {framework}
**Optimizing for:** {goal/metric}

### Tier 1: Build Next
1. **{Feature A}** — Score: {X} | {1-sentence rationale — user value + business case}
2. **{Feature B}** — Score: {X} | {rationale}
3. **{Feature C}** — Score: {X} | {rationale}

### Tier 2: Build Soon
4. **{Feature D}** — Score: {X} | {rationale}
5. **{Feature E}** — Score: {X} | {rationale}

### Tier 3: Validate First / Defer
- {Feature F}: Low confidence — needs experiment before committing
- {Feature G}: Low ROI — revisit if signal changes

### Explicitly Deferred
- {Feature H}: {reason — does not meet investment threshold}

### Key Assumptions
- [Assumption 1 that could change the ranking]
- [Assumption 2]

### Recommended Next Actions
1. {Action 1 — who does what by when}
2. {Action 2}
```

---

### Step 8: Save the prioritization decision

Write to `~/brain/knowledge/decisions/{YYYY-MM-DD}-prioritization-{context}.md` and upsert into brain.db.

Ask: "Should I also update the priorities on these Jira tickets? (yes/no)"

If yes: call `mcp__atlassian__jira_update_issue` to set priority field on each Jira ticket in Tier 1.
