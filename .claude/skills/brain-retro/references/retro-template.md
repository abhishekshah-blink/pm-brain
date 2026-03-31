# Weekly Retro Template

Used by /brain-retro to generate `~/brain/knowledge/retros/YYYY-WW.md`.

---

```markdown
---
title: "Weekly Retro — {ISO-week}"
category: retros
tags: [retro, {YYYY}, sprint]
created: {today}
updated: {today}
---

# Weekly Retro — {ISO-week} ({Mon date} – {Fri date})

## What Shipped
<!-- Completed Jira tickets + merged PRs this week -->

| Ticket | Title | PR |
|---|---|---|
| [WFM-XXXX](https://blinkhealth.atlassian.net/browse/WFM-XXXX) | {summary} | #{pr_num} |

## What's In Flight
<!-- Tickets currently in progress and their status -->

| Ticket | Title | Status | Notes |
|---|---|---|---|
| [WFM-XXXX](https://blinkhealth.atlassian.net/browse/WFM-XXXX) | {summary} | In Progress | {any blockers or context} |

## Blockers & Friction
<!-- What slowed you down this week? What needs resolution? -->

- **{blocker}** — {how it was resolved or what's needed to resolve it}

## What I Learned
<!-- New knowledge items added to ~/brain/ this week + any key decisions or insights -->

- [{title}](~/brain/knowledge/{path}) — {1-line summary}

## Top 3 Priorities for Next Week

1. **{Priority 1}** — {why it's the top priority, what done looks like}
2. **{Priority 2}** — {brief context}
3. **{Priority 3}** — {brief context}

## PM Insight of the Week
<!-- One product observation worth writing down.
     A pattern you noticed, a user insight, a decision clarified,
     a hypothesis validated or invalidated, or a process improvement spotted. -->

{Your PM insight here}
```

---

## Filling In the Template

**What Shipped:** Pull from Jira tickets transitioned to Done this week + git log PRs that were merged. Correlate Jira keys in branch/commit names.

**What's In Flight:** Pull from open sprint tickets assigned to you. Note any that have been in progress for more than one sprint.

**Blockers & Friction:** Be honest and specific. A vague "things were slow" is not useful. Name the actual blocker (dependency, unclear spec, environment issue, etc.).

**What I Learned:** This section compounds over time. Even small domain knowledge additions are worth noting — they add up to expertise.

**Top 3 Priorities:** Force-rank. If you have 10 things to do, pick 3. The constraint is the point.

**PM Insight:** The most important section for a PM. One real observation about the product, users, or process per week compounds into a strong product intuition over months.
