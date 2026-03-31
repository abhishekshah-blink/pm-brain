---
title: "PM Frameworks Overview — When to Use What"
category: domain
tags: [frameworks, pm, reference, overview]
created: 2026-03-30
updated: 2026-03-30
---

# PM Frameworks Overview — When to Use What

Quick-reference index for choosing the right framework at each stage of product work. Check this before starting any discovery, planning, or strategy session.

---

## By Stage

### Problem Definition (Before You Know What to Build)

| Situation | Framework | Where to find it |
|---|---|---|
| "We need to understand the real problem" | Problem Framing Canvas (MITRE) | `domain/problem-framing.md` |
| "We need to frame a user-centered problem statement" | Problem Statement Framework | `domain/problem-framing.md` |
| "We need to understand what users are actually trying to do" | Jobs to Be Done (JTBD) | `domain/jobs-to-be-done.md` |
| "We need to map the full user experience" | Customer Journey Map | `domain/customer-discovery-frameworks.md` |
| "We need a working persona before research is done" | Proto-Persona | `domain/customer-discovery-frameworks.md` |

### Discovery & Validation

| Situation | Framework | Where to find it |
|---|---|---|
| "Should we build X before committing?" | Opportunity Solution Tree (OST) | `domain/opportunity-solution-tree.md` |
| "We need to frame assumptions before building" | Lean UX Canvas | `domain/product-strategy-frameworks.md` |
| "We need to validate an epic before breaking it down" | Epic Hypothesis | `domain/user-story-best-practices.md` |
| "We need to run a discovery interview" | Mom Test / Discovery Interview | `domain/customer-discovery-frameworks.md` |

### Strategy & Positioning

| Situation | Framework | Where to find it |
|---|---|---|
| "Who are we building for and why are we different?" | Positioning Statement (Geoffrey Moore) | `domain/product-strategy-frameworks.md` |
| "What should we build first — define value before building" | Press Release / Working Backwards | `domain/product-strategy-frameworks.md` |
| "Is this feature worth investing in at all?" | Feature Investment Framework | `domain/feature-investment-framework.md` |

### Planning & Prioritization

| Situation | Framework | Where to find it |
|---|---|---|
| "We have too many ideas — how do we pick?" | Prioritization Frameworks (RICE/ICE/Kano) | `domain/prioritization-frameworks.md` |
| "Stakeholders disagree on priorities" | Weighted Scoring / Buy-a-Feature | `domain/prioritization-frameworks.md` |
| "We need to sequence a roadmap" | Cost of Delay, Story Mapping | `domain/prioritization-frameworks.md` |

### Story Writing & Backlog

| Situation | Framework | Where to find it |
|---|---|---|
| "How do we write a good user story?" | Story anatomy + INVEST | `domain/user-story-best-practices.md` |
| "This epic is too big — how do we split it?" | 9 Lawrence Splitting Patterns | `domain/user-story-best-practices.md` |
| "We need to map a full user journey as stories" | User Story Mapping (Jeff Patton) | `domain/user-story-best-practices.md` |

---

## By Question

**"Are we solving the right problem?"** → Problem Framing Canvas, JTBD, Problem Statement

**"Are we building the right solution?"** → OST, Lean UX Canvas, Epic Hypothesis

**"Are we serving the right users?"** → Proto-Persona, CJM, JTBD

**"Are we positioning correctly?"** → Positioning Statement, Press Release / Working Backwards

**"Is this worth building financially?"** → Feature Investment Framework

**"What should we build first?"** → Prioritization Frameworks

**"How do we break down work?"** → Epic Breakdown (Lawrence 9 patterns), User Story Mapping

---

## Anti-Patterns to Avoid

| Anti-Pattern | Better Alternative |
|---|---|
| Jumping to solution before defining problem | Problem Framing Canvas → JTBD |
| Building features without validating the opportunity | OST → Epic Hypothesis → Experiment |
| Prioritizing by loudest voice | RICE/ICE scoring with team input |
| Writing stories as tasks, not outcomes | INVEST + story-as-outcome check |
| Creating elaborate personas before research | Proto-persona (explicitly hypothesis-based) |
| Treating the PRD as a spec document | PRD as alignment + decision document |

---

## Blinkhealth / WFM Application Notes

- **WFM is an internal product** — the "customer" is ops agents, pharmacy managers, and schedulers. Personas are closer than typical B2C.
- **Ops feedback often arrives as feature requests** — always route through JTBD to find the underlying job before accepting the request as stated.
- **Jira is the source of truth for work items** — but the brain knowledge base is the source of truth for decisions, context, and domain knowledge.
- **Cross-team dependencies** (task-assignment-service ↔ rx-os-frontend ↔ wfm-microfrontends) make story splitting especially important — isolate what can be shipped per service.
