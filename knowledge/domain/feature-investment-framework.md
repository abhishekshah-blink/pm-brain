---
title: "Feature Investment Framework — Build vs. Don't Build"
category: domain
tags: [feature-investment, roi, build-vs-dont-build, financial, frameworks, strategy]
created: 2026-03-30
updated: 2026-03-30
---

# Feature Investment Framework

**Source:** deanpeters/Product-Manager-Skills (feature-investment-advisor)
**When to use:** Before committing engineering resources to any significant feature. When leadership asks "is this worth it?" When prioritizing between features that have different revenue/cost profiles.

> "If you can't articulate the financial case for a feature in 3 sentences, you don't have one."

---

## The 4-Lens Framework

Evaluate every significant feature across 4 lenses in order:

```
1. Revenue Connection → 2. Cost Structure → 3. ROI → 4. Strategic Value
```

---

## Lens 1: Revenue Connection

**How does this feature connect to revenue?**

| Type | Pattern | Test question |
|---|---|---|
| **Direct monetization** | Feature is a paid tier, add-on, or gating mechanism | "Can we charge for this directly?" |
| **Retention** | Reduces churn — keeps revenue we'd otherwise lose | "Would losing this feature cause cancellations or exits?" |
| **Conversion** | Moves users from free → paid or trial → active | "Does this feature convert hesitant users?" |
| **Expansion** | Enables upsell to higher tier or more seats | "Does this create a reason to pay more?" |
| **No revenue connection** | Internal efficiency, technical debt, compliance | "Is the cost of NOT doing this acceptable?" |

For WFM (internal product), translate to operational revenue:
- "Retention" = preventing ops errors that cause SLA misses or patient impact
- "Conversion" = adoption across pharmacy locations that aren't yet using the tool
- "Expansion" = extending to new pharmacy workflows or teams

---

## Lens 2: Cost Structure

Estimate total cost of ownership, not just development:

| Cost Component | Question | Example |
|---|---|---|
| **Development cost** (one-time) | How many engineering weeks? At what blended rate? | 4 weeks × 2 engineers = 8 person-weeks |
| **COGS** (per-unit ongoing) | Does this feature have infrastructure costs per user? | +$X/month AWS cost at scale |
| **OpEx** (ongoing) | How much support, maintenance, and iteration does this need? | 1 sprint/quarter for maintenance |

Use conservative estimates. Actual development time is typically 1.3–1.5× initial estimate.

---

## Lens 3: ROI Calculation

```
ROI = Revenue Impact / Development Cost
```

Minimum viable ROI:
- **Direct revenue:** Target ≥ 3:1 in Year 1, ≥ 10:1 over 3 years
- **Retention/indirect:** Target ≥ 10:1 LTV impact to cost

**Also calculate:**
- **Payback period:** Development cost / monthly revenue impact
  - Good: < 6 months
  - Acceptable: 6–12 months
  - Needs justification: > 12 months

**Margin check:** Gross margin impact (revenue impact × gross margin %) > COGS added. A feature that adds revenue but dilutes margin is a strategic trap.

---

## Lens 4: Strategic Value

Some features have weak direct ROI but strong strategic justification. Name it explicitly:

| Type | Definition | Honest test |
|---|---|---|
| **Competitive moat** | Prevents a competitor from offering something you don't | "Would users leave for a competitor that has this?" |
| **Platform enabler** | Unlocks future capabilities or integrations | "Does this enable 3+ future features?" |
| **Market positioning** | Signals quality or category leadership | "Does this change how stakeholders perceive the product?" |
| **Risk reduction** | Reduces regulatory, operational, or compliance risk | "What is the cost of NOT doing this?" |

**Warning:** "Strategic" is the most abused word in prioritization. Before using it, answer: "Strategic for which goal, measured how, by when?"

---

## The 4 Recommendation Patterns

After running all 4 lenses, you should land in one of these:

### Pattern 1: Build Now
- ROI ≥ 3:1 direct (Year 1) OR ≥ 10:1 LTV impact
- Positive gross margin impact
- No significant execution risk

**Decision:** Prioritize in next sprint/cycle.

---

### Pattern 2: Build for Strategic Reasons
- Marginal direct ROI (< 3:1) BUT strong strategic value (competitive moat, platform enabler, compliance)
- Must define the metric you'll use to know if the bet paid off

**Decision:** Build, but set a review checkpoint at 90 days. Define the metric now.

---

### Pattern 3: Don't Build
- ROI < 1:1 (will cost more than it generates)
- Dilutes gross margin
- Strategic value is vague or unsubstantiated
- Alternatives: Buy (third-party tool), Partner (integrate with existing solution), or Do Nothing

**Decision:** Remove from roadmap. Document the decision in brain.db so you don't relitigate it in 6 months.

---

### Pattern 4: Build Later / Validate First
- High uncertainty in the revenue estimate (confidence < 50%)
- No existing signal that users want this (< 5 requests, no discovery research)
- OR: high impact if validated but large investment required

**Decision:** Define the minimum experiment to validate. What signal would change this to Pattern 1?
- Prototype + usability test? Landing page? Concierge?
- Set a decision date (30–60 days out).

---

## Quick Reference Table

| Scenario | ROI | Strategic | Recommendation |
|---|---|---|---|
| Time tracking add-on, known demand, low COGS | 2:1 Year 1, 6:1 Year 3 | Medium | Build now (payback < 12mo) |
| Data export for churn analysis | 22:1 LTV impact | High | Build immediately |
| Dark mode (50 requests, no churn evidence) | < 1:1 | Low | Build later / validate first |
| Compliance-required audit logging | Negative direct ROI | Critical (regulatory) | Build for strategic reasons |

---

## Inputs You Need Before Running This

- Current monthly revenue / ARR (for WFM: operational throughput metric or proxy)
- Churn rate (monthly)
- Average lifetime (for LTV calculation)
- Gross margin %
- Engineering cost estimate (rough is fine — within 50%)
- Customer signal: how many users have requested this and how strongly?

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Confusing revenue with profit | Always check gross margin impact |
| Overestimating adoption | Use a conservative adoption rate (20–30% of eligible users in Year 1) |
| Building without validating | Pattern 4 exists for a reason — validate before investing |
| "Strategic" as a proxy for HiPPO preference | Force a measurable strategic outcome statement |
| Ignoring opportunity cost | Every yes is a no to something else — make the tradeoff explicit |
| Loud minorities driving investment | 50 vocal users ≠ the full user base; weight by segment size |

---

## Related Frameworks

- `domain/prioritization-frameworks.md` — Use this lens to inform RICE/ICE scores
- `domain/opportunity-solution-tree.md` — Validate the opportunity before running financial analysis
- `domain/product-strategy-frameworks.md` — Strategic value connects to positioning and press release
