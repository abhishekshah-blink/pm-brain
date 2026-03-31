---
title: "Prioritization Frameworks"
category: domain
tags: [prioritization, rice, ice, kano, moscow, frameworks, backlog, roadmap]
created: 2026-03-30
updated: 2026-03-30
---

# Prioritization Frameworks

**Sources:** deanpeters/Product-Manager-Skills (prioritization-advisor); Sean McBride (RICE); Des Traynor / Intercom (ICE); Noriaki Kano; WSJF / Cost of Delay
**When to use:** When the backlog has more items than the team can deliver, when stakeholders disagree, when you need to justify sequencing decisions.

> "A framework without context is just a spreadsheet. The point is to make better decisions faster — not to outsource the thinking."

---

## How to Choose a Framework

Answer these 4 questions first:

**1. Product stage?**
- Pre-PMF (still finding what works) → ICE or Value/Effort Matrix
- Early PMF (validating growth levers) → RICE or ICE
- Mature (optimizing known product) → RICE, Kano, Weighted Scoring
- Multi-product / portfolio → Cost of Delay, Impact Mapping

**2. Team context?**
- Small, aligned team → ICE (fast, low overhead)
- Cross-functional, mostly aligned → RICE
- Multi-stakeholder, misaligned → Weighted Scoring or Buy-a-Feature (involves stakeholders in the process)
- Large org with competing teams → WSJF / Cost of Delay

**3. What's the decision need?**
- Too many ideas → ICE or Value/Effort Matrix
- Stakeholder disagreement → Weighted Scoring, Buy-a-Feature
- Need data-driven justification → RICE
- Roadmap sequencing → Cost of Delay, Story Mapping

**4. Data availability?**
- Minimal data → ICE (intuition + lightweight scoring)
- Some data (traffic, usage, feedback) → RICE
- Rich data (revenue, churn, NPS) → Weighted Scoring with actual metrics

---

## The Frameworks

### RICE

**Best for:** Early PMF to mature products with cross-functional teams and some data.

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

| Factor | Definition | Scale |
|---|---|---|
| **Reach** | How many users affected per quarter? | Number (users/requests/events) |
| **Impact** | How much does it move the metric? | 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal |
| **Confidence** | How confident in R, I, and E estimates? | 100%=high, 80%=medium, 50%=low |
| **Effort** | Total person-months to build + ship | Person-months (1 person for 1 month = 1) |

**Pitfalls:** Don't use RICE pre-PMF (Reach is unknown). Don't let high Confidence mask low evidence. Round Effort to 0.5 increments — false precision is worse than honest ranges.

---

### ICE

**Best for:** Pre-PMF, early discovery, fast backlog sorting. Low overhead.

```
ICE Score = (Impact + Confidence + Ease) / 3
```

Each factor scored 1–10. Average = ICE score.

| Factor | Definition |
|---|---|
| **Impact** | If this works, how much does it move the goal? |
| **Confidence** | How sure are you it will have that impact? |
| **Ease** | How easy is it to build and ship? (10 = trivial, 1 = very hard) |

**When to use ICE over RICE:** When you don't have reliable reach data. When you need to sort 20+ items in a 30-minute session. When the team is small enough that everyone's intuition is roughly calibrated.

---

### Value / Effort Matrix (2×2)

**Best for:** Fast facilitation, early stage, anyone who finds RICE too heavy.

```
           Low Effort    High Effort
High Value  [Do First]   [Big Bets]
Low Value   [Fill-Ins]   [Skip]
```

- **Do First:** High value, low effort — the obvious wins
- **Big Bets:** High value, high effort — sequence carefully, validate first
- **Fill-Ins:** Low value, low effort — do when capacity allows, never over Big Bets
- **Skip:** Low value, high effort — remove from backlog

**Weakness:** "Value" is subjective without further definition. Pair with JTBD or user research to anchor value.

---

### Kano Model

**Best for:** Mature products deciding which features to invest in vs. de-prioritize. Understanding delight vs. hygiene.

Three categories:

| Category | What it means | WFM Example |
|---|---|---|
| **Basic / Must-Have** | Users expect it. Its absence causes dissatisfaction. Its presence is not noticed. | Task list shows accurate counts |
| **Performance / Linear** | More = better. Users appreciate improvements proportionally. | Task assignment speed |
| **Delighter / Exciter** | Unexpected. Causes delight if present, no dissatisfaction if absent. | Proactive alert before queue overflows |

**Note:** Delighters become Performance over time. Performance becomes Basic. A Kano map is not permanent.

**Use Kano when:** You're deciding whether to invest engineering effort in a "nice to have" vs. fixing a Basic expectation. Never deprioritize Basic features to build Delighters.

---

### MoSCoW

**Best for:** Release scoping, stakeholder alignment on MVP, sprint planning with constrained time.

| Category | Definition | Rule |
|---|---|---|
| **Must Have** | Without this, the release fails | Max 60% of total scope |
| **Should Have** | Important but can ship as v1.1 | Max 20% of total scope |
| **Could Have** | Nice to have; first to cut | Rest |
| **Won't Have** | Explicitly out of scope this cycle | Write these down — prevents scope creep |

**Critical rule:** If everything is "Must Have," MoSCoW is not being used honestly. Force the tradeoff.

---

### Weighted Scoring

**Best for:** Multi-stakeholder environments where different people value different things.

1. Define criteria (e.g., user impact, strategic alignment, revenue potential, tech debt reduction)
2. Assign weights to each criterion (must sum to 100%)
3. Score each item 1–5 per criterion
4. Weighted score = sum of (score × weight)

**Strength:** Makes implicit value judgments explicit. Surfaces where stakeholders actually disagree.
**Weakness:** High overhead. Don't use for more than 10 items unless the decision is worth it.

---

### Cost of Delay (WSJF)

**Best for:** Large org, portfolio planning, when sequencing decisions have significant financial consequences.

```
WSJF = Cost of Delay / Job Size (relative)
```

Cost of Delay combines:
- User/business value
- Time criticality (is there a deadline or market window?)
- Risk reduction / opportunity enablement

Sequence by highest WSJF first.

**Use when:** You have real time-sensitivity (compliance deadlines, competitive windows, contract milestones). Overkill for standard sprint prioritization.

---

## Running a Prioritization Session

1. **Agree on the goal metric before scoring** — don't score without knowing what you're optimizing for
2. **Score independently before discussing** — prevents anchoring
3. **Surface disagreements as inputs, not problems** — a 10 vs 2 on Impact means someone has information others don't
4. **Document rationale, not just scores** — the reasoning decays faster than the number
5. **Reassess quarterly** — priorities shift; a frozen backlog is a liability

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Framework whiplash (switching methods each quarter) | Pick one for the team's current stage and commit for ≥2 quarters |
| Treating scores as gospel | Scores inform judgment — they don't replace it |
| Solo PM scoring | At minimum, loop in engineering and design |
| Ignoring opportunity cost | Saying yes to X means saying no to Y — make the tradeoff visible |
| "Strategic" as an excuse | If you can't explain the strategy, "strategic" is a HiPPO override in disguise |

---

## Related Frameworks

- `domain/feature-investment-framework.md` — Financial lens for individual features before scoring
- `domain/opportunity-solution-tree.md` — OST reveals which problems to prioritize solving
- `domain/user-story-best-practices.md` — Story mapping for sequencing post-prioritization
