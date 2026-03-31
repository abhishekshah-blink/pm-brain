---
title: "Customer Discovery Frameworks — Proto-Persona, CJM, Discovery Interviews"
category: domain
tags: [discovery, persona, customer-journey-map, interviews, mom-test, research, frameworks]
created: 2026-03-30
updated: 2026-03-30
---

# Customer Discovery Frameworks

**Sources:** deanpeters/Product-Manager-Skills (proto-persona, customer-journey-map, discovery-interview-prep); Rob Fitzpatrick, *The Mom Test*; Nielsen Norman Group (CJM)
**When to use:** Before writing a PRD, before defining acceptance criteria, when you haven't talked to users in > 4 weeks, when you're making assumptions about user behavior.

---

## Part 1: Proto-Persona

### What It Is
An assumption-based persona created from current research, analytics, market signals, and stakeholder knowledge. A structured placeholder that:
- Prevents design-by-committee (everyone projecting their own preferences)
- Makes assumptions explicit (so they can be validated)
- Aligns the team on who we're building for today

### Proto vs. Validated Persona

| | Proto-Persona | Validated Persona |
|---|---|---|
| **Time to create** | Hours to days | Weeks to months |
| **Data source** | Assumptions + limited research | Extensive user research |
| **Purpose** | Align teams early, start building | Guide detailed design decisions |
| **Stability** | Evolves rapidly as you learn | Relatively stable |
| **Label** | "[ASSUMPTION—VALIDATE]" | Evidence-cited |

### 6-Component Template

```markdown
## [Persona Name — use an alliterative name for memorability]

**Bio:** [3-4 sentences — behavioral characteristics, not just demographics]
[Demographics are secondary. Behaviors and motivations matter more.]

**Voice (quote):** "[A quote that captures their mindset]"
[Use real quotes from research if available. Otherwise: "[PLACEHOLDER—NEEDS RESEARCH]"]

**Pains:**
- [Specific barrier they experience in the context of your product]
- [Another specific pain — grounded in observable behavior]

**What they're trying to accomplish (JTBD):**
- [Observable, outcome-focused job — not a task]
- [Another job — connects to their workflow]

**Goals:**
- Short-term: [What they want to achieve today / this shift]
- Long-term: [What success looks like over time]

**Decision-making:**
- Authority: [Can they decide to use this tool, or do they need approval?]
- Influencers: [Who else shapes their experience or adoption?]
- Beliefs & attitudes: [What assumptions do they hold about tools like this?]
```

### Tag all assumptions: `[ASSUMPTION—VALIDATE]`

Planned research to validate: [ ]

### WFM Personas (Starting Points)

**Ops Agent "Organized Olivia"**
- Manages task queue during shift, peak volume 10am–2pm
- Primary job: ensure all tasks assigned and progressing before EOD
- Pain: no real-time queue visibility; tasks fall through during handoff
- Goal: leave shift confident nothing was missed

**Pharmacy Manager "Manager Marcus"**
- Oversees ops agents + pharmacist availability
- Primary job: identify and resolve blockers before they become patient delays
- Pain: can't see current queue state without asking individual agents
- Goal: operational visibility without micromanaging

---

## Part 2: Customer Journey Map

### What It Is
A visualization of the customer's experience across all touchpoints — from first awareness to ongoing use. Combines customer empathy (emotions, pain points) with business metrics (KPIs, goals per stage).

**Use when:**
- Diagnosing where an experience is broken
- Aligning cross-functional team on the full flow
- Identifying which stage to invest in first

### 5-Stage Framework (NNGroup)

```
Awareness → Consideration → Decision → Service → Loyalty
```

For WFM (internal product): stages map more to:
```
Onboarding → Daily Use → Peak Load → Issue Resolution → Mastery
```

### What to Document per Stage

| Layer | Definition | Example (WFM) |
|---|---|---|
| **Customer Actions** | Observable behaviors (not what they should do) | "Checks Slack for task updates before opening WFM" |
| **Touchpoints** | Digital + physical interaction points | "WFM task list screen, Slack, phone call to pharmacy" |
| **Customer Experience** | Emotional state at this stage (specific, research-based) | "Frustrated — screen doesn't refresh, unsure if data is current" |
| **KPIs** | Stage-appropriate measurable signal | "% of tasks assigned within 15 min of creation" |
| **Business Goals** | What the business needs at this stage | "Reduce manual reassignments at EOD" |
| **Teams Involved** | Which teams own or touch this stage | "WFM product, rx-os-backend, pharmacy ops" |

### Quality Rules
- **Actions:** Must be observable — "Calls the pharmacist to check" not "Coordinates effectively"
- **Experience:** Must be from research — "Frustrated" not "Satisfied" if you haven't asked
- **Touchpoints:** Must include offline/manual steps — most internal tools are 40% Slack + spreadsheet
- **KPIs:** Must be measurable — stage-specific, not just final outcome metrics

### Priority Analysis (After Mapping)
1. Where is experience lowest while KPI importance is highest? → Start here
2. Where do multiple teams' responsibilities overlap without clear ownership? → Ownership risk
3. Where are users working around the product (using Slack instead)? → Product gap

---

## Part 3: Discovery Interviews (Mom Test)

### The Mom Test Principle
Ask questions that even your mom (who wants to make you happy) can't lie about.

**Bad question:** "Would you use a feature that does X?"
**Good question:** "Walk me through the last time you had to handle X. What did you do?"

### 5 Rules for Good Discovery Interviews

1. **Talk about their life, not your idea** — Your job is to learn, not to pitch
2. **Ask about the past, not the future** — "Would you...?" is opinion. "Did you...?" is fact.
3. **Ask for specifics, not generalities** — "Tell me about a time when..." not "Generally how do you..."
4. **Listen for the emotion, not just the answer** — Frustration, workarounds, and complaints are gold
5. **Never mention your solution until you've heard the problem** — Mentioning your solution anchors their feedback

### Question Bank for WFM Discovery

**Opening (last time / real event):**
- "Walk me through what you did last [shift / busy period] when it came to [task area]."
- "When was the last time [problem X] happened? What did you do?"

**Dig for frequency and consequence:**
- "How often does that happen?"
- "What did you do when that happened?"
- "What's the worst case when that goes wrong?"

**Dig for current workarounds:**
- "What do you use today for that?"
- "What do you wish was different about how you handle that?"

**Avoid:**
- "Would you use a tool that...?" → Opinion, not fact
- "How much would you pay for...?" → Hypothetical, not behavioral
- "Do you think this is a common problem?" → They'll say yes to be helpful

### Interview Synthesis

After each interview, capture within 24 hours:
1. **The job they described** (functional + emotional)
2. **The biggest pain they named** (exact words)
3. **The current workaround** (what product gap does this expose?)
4. **The surprising thing** (what you didn't expect)
5. **Confidence update** (did this confirm or challenge your hypothesis?)

After 5 interviews: look for patterns across all 5 in each category.

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Treating proto-persona as validated | Label every assumption; plan validation research |
| CJM from internal perspective ("what users should do") | Interview actual users and map what they actually do |
| Discovery interviews that are really pitches | Don't mention your solution in first 20 minutes |
| Creating 5+ personas before building anything | Start with 1 primary persona; expand as product matures |
| CJM as a one-time artifact | Review and update quarterly; it decays fast |

---

## Related Frameworks

- `domain/jobs-to-be-done.md` — JTBD structures what you listen for in interviews
- `domain/problem-framing.md` — CJM and interviews feed Phase 2 (Look Outward) of MITRE canvas
- `domain/opportunity-solution-tree.md` — Validated pains from interviews become opportunities in OST
