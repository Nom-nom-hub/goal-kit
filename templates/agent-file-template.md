# Goal Kit Agent Integration Guide

**For**: [AGENT_NAME] (Claude, Cursor, Copilot, Gemini, etc.)
**Version**: 1.0
**Updated**: 2025-11-26

---

## What is Goal Kit?

Goal Kit is a **Goal-Driven Development** methodology that structures projects around measurable outcomes, not feature lists. It helps teams:

1. **Define clear goals** with measurable success criteria
2. **Explore multiple strategies** before committing to implementation
3. **Break work into milestones** with measurable progress
4. **Execute with learning** - treat implementation as hypothesis testing
5. **Capture insights** for continuous improvement

**Key Principle**: Focus on **WHAT** and **WHY** before **HOW**.

---

## Your Role as an Agent

You'll help execute Goal Kit commands by:

1. **Reading** existing documents (vision, goals, strategies, milestones, execution plans)
2. **Understanding** the methodology and traceability
3. **Generating** new documents following templates and principles
4. **Validating** work against gates and quality criteria
5. **Reporting** completion with clear next steps

### Core Responsibilities

- **Outcome-focused thinking**: Always link work back to measurable success criteria
- **Traceability**: Understand how each document connects upstream (Vision → Goal → Strategy → Milestones → Execution → Learnings)
- **Template adherence**: Follow template structure exactly; preserve section order and headings
- **Concrete examples**: Replace placeholders with real examples from context
- **Error on gates**: If validation gates fail, report ERROR and don't proceed
- **Clear reporting**: Always report what was created and what's ready next

---

## Goal Kit Commands

You'll receive requests using these commands. Follow the corresponding guide:

### `/goalkit.vision`
**Create or refine project vision**
- **Input**: Project description or existing vision to improve
- **Output**: vision.md with core mission, vision statement, success criteria
- **Gate**: Vision Check (clarity, measurability)
- **Next**: `/goalkit.goal`
- **Guide**: `templates/commands/vision.md`

### `/goalkit.goal`
**Define goals with success criteria**
- **Input**: Goal description (what outcome is needed and why)
- **Output**: goal.md with definition, success metrics, validation strategy
- **Gate**: Goal Check (completeness, no implementation details)
- **Next**: `/goalkit.strategies`
- **Guide**: `templates/commands/goal.md`

### `/goalkit.strategies`
**Explore multiple implementation strategies**
- **Input**: Goal spec, vision alignment
- **Output**: strategies.md with 3 strategy options and decision rationale
- **Gate**: Strategy Check (rigorous evaluation, clear rationale)
- **Next**: `/goalkit.milestones`
- **Guide**: `templates/commands/strategies.md`

### `/goalkit.milestones`
**Create measurable milestone checkpoints**
- **Input**: Goal, selected strategy
- **Output**: milestones.md with 3+ milestones, KPIs, dependencies
- **Gate**: Milestones Check (measurable, sequenced, realistic)
- **Next**: `/goalkit.execute`
- **Guide**: `templates/commands/milestones.md`

### `/goalkit.execute`
**Plan execution with learning loops**
- **Input**: Goal, strategy, milestones
- **Output**: execution.md with phases, teams, deliverables, success measures
- **Gate**: Milestones Check (fidelity to plan)
- **Next**: `/goalkit.tasks` or `/goalkit.report`
- **Guide**: `templates/commands/execute.md`

### `/goalkit.tasks`
**Break down execution into detailed tasks**
- **Input**: Execution plan
- **Output**: tasks.md with task breakdown, owners, effort, DoD
- **Gate**: Execution Check (completeness, clarity)
- **Next**: `/goalkit.taskstoissues`
- **Guide**: `templates/commands/tasks.md`

### `/goalkit.report`
**Generate progress reports with metrics**
- **Input**: Goal metrics, execution progress
- **Output**: report.md with planned vs actual, trends, recommendations
- **Gate**: Metrics Check (quantified, evidence-based)
- **Next**: Stakeholder communication
- **Guide**: `templates/commands/report.md`

### `/goalkit.review`
**Conduct goal retrospective**
- **Input**: Goal outcomes, execution results
- **Output**: review.md with achievement assessment, process feedback
- **Gate**: Learnings Check (actionable insights)
- **Next**: Improvement goals or next goal
- **Guide**: `templates/commands/review.md`

### `/goalkit.taskstoissues`
**Convert tasks to GitHub issues**
- **Input**: Tasks document
- **Output**: GitHub issues in repository (in dependency order)
- **Gate**: GitHub validation (repository verification, metadata)
- **Next**: Development execution
- **Guide**: `templates/commands/taskstoissues.md`

---

## Core Methodology Principles

### 1. Outcome-First Thinking
- Goals describe **user/business outcomes**, not technical solutions
- Success criteria are **measurable** (%, time, count, user satisfaction)
- Implementation details (languages, frameworks, tools) come **later**

### 2. Multiple Strategies
- Always explore **3 different strategic approaches**
- Evaluate against consistent criteria
- Document **decision rationale** explaining why one was chosen
- Record **key assumptions** that must be validated

### 3. Measurable Progress
- Break work into **milestones with KPIs**
- Each milestone should be independently verifiable
- Success metrics from goal must **trace through milestones to execution**

### 4. Learning-Driven Execution
- Implementation is **hypothesis testing**
- Track both what worked and what surprised us
- Capture **learnings after each milestone** for continuous improvement
- Use learnings to improve future goals

### 5. Traceability
Every document connects to upstream sources:

```
vision.md (project mission and success criteria)
    ↓ aligns with
goal.md (measurable outcome tied to vision)
    ↓ aligns with
strategies.md (approach to achieve goal)
    ↓ aligns with
milestones.md (measurable progress toward strategy)
    ↓ aligns with
execution.md (sprint-level implementation detail)
    ↓ produces
tasks.md (work breakdown with owners/effort)
    ↓ converts to
GitHub issues (developer work items)

Parallel:
execution → report.md (progress against goal metrics)
execution → learnings.md (insights for future improvement)
```

---

## Templates & Structure

### Template Format
Each template has consistent sections:

1. **Alignment Header** (shows upstream dependencies)
2. **Key Metrics** (2-3 measurable outcomes only, no vague lists)
3. **Main Content** (specific to artifact type)
4. **Gate Section** (validation criteria)
5. **Key Assumptions** (what must be true for this to work)
6. **Next Steps** (what comes after)

### Quality Rules

**MUST**:
- ✅ Replace **ALL** placeholders with **concrete examples**
- ✅ Follow template structure exactly (preserve section order)
- ✅ Include measurable, not vague, success criteria
- ✅ Link to upstream documents (goals, strategies, etc.)
- ✅ Explain key assumptions and trade-offs
- ✅ Use business/user language, not technical jargon

**MUST NOT**:
- ❌ Leave placeholders like `[PLACEHOLDER]` or `{EXAMPLE}`
- ❌ Use vague terms: "improve", "optimize", "enhance" (without metrics)
- ❌ Include implementation details in goal/vision (save for strategy/execution)
- ❌ Create random lists (limit to 2-3 key items per section)
- ❌ Omit traceability to upstream documents
- ❌ Reorder or rename template sections

### Example: Concrete vs Vague

**VAGUE** (avoid):
```markdown
Success Indicators:
1. [Indicator that shows success has been achieved]
2. [Additional indicator that validates the achievement]
```

**CONCRETE** (do this):
```markdown
Key Metrics (2-3 measurable outcomes):

1. Code review completion time drops from 8+ hours to <2 hours
2. 90% of reviewers complete first review without reopening discussion
3. Senior developers spend <30 mins/day on review coordination
```

---

## Common Tasks & How to Handle Them

### Task: Create Initial Goal
```
User input: "I want to improve code review speed"

You should:
1. Load vision.md to understand project context
2. Ask for clarification on: beneficiaries, specific pain points, timeline
3. Generate goal.md with measurable success criteria
4. Validate against Goal Check gate
5. Report: "Goal created at [path]. Ready for /goalkit.strategies"
```

### Task: Evaluate Strategy Options
```
You should:
1. Load goal.md to understand what success looks like
2. Generate 3 distinct strategy options with different trade-offs
3. Create comparison table (cost, risk, timeline, team requirements)
4. Document decision rationale explaining why one was selected
5. Validate against Strategy Check gate
6. Report: "Strategy selected: [name]. Key assumption: [assumption]. Ready for /goalkit.milestones"
```

### Task: Create Milestones
```
You should:
1. Load goal and strategy to understand direction
2. Define 3+ milestones that sequence toward goal
3. For each milestone: measurable KPI, deliverables, dependencies
4. Show milestone dependencies/critical path visually
5. Validate against Milestones Check gate
6. Report: "3 milestones created. Sequence: [M1] → [M2] → [M3]. Ready for /goalkit.execute"
```

### Task: Generate Progress Report
```
You should:
1. Load goal success metrics
2. Gather actual progress data
3. Create comparison table (planned metric vs actual result)
4. Identify trends (improving, stalled, regressed)
5. Recommend actions tied to metric gaps
6. Validate against Metrics Check gate
7. Report: "Report shows 75% goal achievement. Key gap: [metric]. Recommending: [action]"
```

---

## Gate Validation Checklist

### Vision Check
- [ ] Core mission is clear and inspiring (not a feature list)
- [ ] All success criteria are measurable with specific targets
- [ ] Guiding principles are actionable (not vague values)
- [ ] No implementation details (no tech stack, tools)

**ERROR if**: Vision lacks clarity or success criteria are unmeasurable

### Goal Check
- [ ] All mandatory sections completed
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Success metrics are measurable and outcome-focused
- [ ] No implementation details leak into goal

**ERROR if**: Goal fails checklist validation or has unresolved clarifications

### Strategy Check
- [ ] Decision rationale clearly explains why this strategy was selected
- [ ] All 3 options were rigorously evaluated against criteria
- [ ] Key assumptions are explicit and justified
- [ ] Alternatives considered and rejected with clear reasoning

**ERROR if**: Strategy selection lacks clear rationale or assumptions are vague

### Milestones Check
- [ ] All 3+ milestones are measurable with specific KPIs
- [ ] Deliverables and dependencies are clearly defined
- [ ] Timeline is realistic and resource-constrained
- [ ] Each milestone traces back to goal success metric

**ERROR if**: Milestones lack measurable success criteria or sequence is unrealistic

### Metrics Check (Report)
- [ ] All planned metrics are measured and documented
- [ ] Actual vs planned comparisons are quantified
- [ ] Trends are identified from historical data
- [ ] Recommendations are tied to metric gaps

**ERROR if**: Critical metrics are missing or unquantified

### Learnings Check (Review)
- [ ] Key insights are documented with specific examples
- [ ] Assumptions are tested against actual outcomes
- [ ] Both successes and failures are analyzed
- [ ] Recommendations for future goals are actionable

**ERROR if**: Learnings are vague or assumptions unvalidated

---

## Key Dos and Don'ts

### DO ✅
- **Read upstream documents** before generating new ones
- **Ask clarifying questions** when goal is ambiguous (max 3 clarifications)
- **Use concrete examples** from the code review domain (default) or provided context
- **Link to upstream** in traceability headers
- **Explain trade-offs** in Decision Rationale sections
- **Validate against gates** before reporting completion
- **Report what's ready next** with clear handoff instructions

### DON'T ❌
- **Leave placeholders** in generated documents
- **Include implementation details** in goal/vision (save for execution)
- **Create vague success criteria** (must be measurable)
- **Ignore traceability** (always show what this aligns with)
- **Proceed without gate validation** (ERROR on failures)
- **Assume context** (read existing docs and ask if unclear)
- **Reorder or rename** template sections

---

## Working with Context

### Files You'll Access
- `templates/[artifact]-template.md` - Template structure to follow
- `templates/commands/[command].md` - Step-by-step execution guide
- `memory/constitution.md` - Project principles and values
- `.goalkit/vision.md` or `vision.md` - Current project vision
- `goals/[goal-dir]/` - Goal documents (goal.md, strategies.md, etc.)

### How to Read Documents
1. **Start with the Alignment header** to understand dependencies
2. **Scan Key Metrics** to see what matters
3. **Review the main sections** to understand current state
4. **Check the Assumptions** for what's being taken as true
5. **Look at Next Steps** to see what comes after

### When You Don't Have Context
- **Ask the user**: "I need to understand the current project scope. Can you provide the vision?"
- **Use defaults**: If no prior work exists, start with template examples
- **Document assumptions**: "Assuming [X] based on common patterns—correct me if different"

---

## Interaction Examples

### Example 1: Creating Initial Goal

**User**: `/goalkit.goal Improve code review speed and quality`

**You should**:
1. Check if vision.md exists (if not, ask user to create it first)
2. Load vision.md to understand project mission
3. Extract key concepts: "improve code review", "speed", "quality"
4. Ask clarifying questions (if needed):
   - Current pain point: Are reviewers overloaded, or is communication slow?
   - Timeline: This quarter, this year, or ongoing?
   - Success measure: Time, defect rate, team satisfaction, or all three?
5. Generate goal.md with:
   - Clear beneficiary story (who benefits and how)
   - 2-3 measurable success metrics (not 10 vague ones)
   - Validation strategy (how we'll know we succeeded)
6. Validate against Goal Check gate
7. Report: "✅ Goal created: /goals/1-code-review-speed/goal.md. Next: /goalkit.strategies to explore implementation approaches"

### Example 2: Generating Strategy Options

**User**: `/goalkit.strategies` (with goal already created)

**You should**:
1. Load goal.md and vision.md
2. Generate 3 strategy options with real trade-offs:
   - **Option 1**: Real-time notifications (WebSocket-based)
     - Cost: $X infrastructure, Y engineering hours
     - Risk: Complexity, vendor lock-in
     - Timeline: 6 weeks
   - **Option 2**: Batch notifications (polling every N minutes)
     - Cost: Lower infrastructure, fewer engineers
     - Risk: Latency, user experience degradation
     - Timeline: 3 weeks
   - **Option 3**: Hybrid approach (real-time + fallback)
     - Cost: Medium infrastructure, 8+ weeks
     - Risk: Complexity, more moving parts
     - Timeline: 8 weeks
3. Create evaluation table against criteria from goal
4. Document decision rationale:
   - "Selected Option 1 because goal requires <2s latency"
   - "Key assumption: WebSocket infrastructure is mature in our stack"
   - "Option 2 rejected because it can't meet SC-001 (2s latency)"
5. Validate against Strategy Check gate
6. Report: "✅ Strategies evaluated. Selected: Option 1 (Real-time WebSocket). Key assumption: Infrastructure maturity. Ready: /goalkit.milestones"

### Example 3: Creating Progress Report

**User**: `/goalkit.report 3-month milestone review`

**You should**:
1. Load goal.md and execution.md
2. Gather actual metrics (from logs, user feedback, etc.)
3. Create comparison table:
   | Metric | Planned | Actual | Status |
   | --- | --- | --- | --- |
   | Review time | <2 hours | 1.8 hours | ✅ Met |
   | First review % | 90% | 87% | ⚠️ Close |
   | Coordination time | <30 min | 45 min | ❌ Miss |
4. Analyze trends: Is performance improving week-over-week?
5. Identify gaps: Why is coordination time higher? What can change?
6. Recommend actions: "Increase bot automation to reduce coordination overhead"
7. Validate against Metrics Check gate
8. Report: "✅ Report generated. Achievement: 2/3 metrics on track. Gap: Coordination overhead. Action: Increase automation. Ready: Stakeholder review"

---

## Troubleshooting

### "I don't have the upstream document"
→ Ask user to provide it or create it first: "Please run `/goalkit.goal` first"

### "Goal is too vague to measure"
→ Ask for specifics: "What does 'improve' mean? Is it 20% faster, 50%, or 10x?"

### "There are too many success criteria"
→ Limit to 2-3: "Let's focus on the 3 most critical metrics"

### "User wants implementation details in goal"
→ Redirect to execution phase: "That's a great technical approach—let's explore it in strategies"

### "Gate validation failed"
→ Report ERROR clearly: "❌ Strategy Check failed: Decision rationale missing. Please clarify why Option X was selected."

### "I don't understand the traceability"
→ Draw it: "This goal traces to vision.md (success scenario), which traces to strategies.md (implementation approach), which traces to milestones.md (progress steps)"

---

## Tips for Success

1. **Always start with reading** - Understand what exists before generating new work
2. **Ask one clarifying question at a time** - Don't overwhelm user with 10 questions
3. **Show your thinking** - Explain why you're recommending something
4. **Link everything** - Make traceability explicit in headers and references
5. **Validate before reporting** - Run through gate checklist before saying "complete"
6. **Be concrete** - Replace ALL placeholders with real examples
7. **Respect the methodology** - Don't skip steps or gates
8. **Report clearly** - Tell user what's done and what's ready next

---

## Quick Reference Commands

```
/goalkit.vision <description>     → Create or refine vision
/goalkit.goal <description>       → Define goal with metrics
/goalkit.strategies               → Explore 3 implementation approaches
/goalkit.milestones               → Plan measurable milestones
/goalkit.execute                  → Detailed execution plan
/goalkit.tasks                    → Task breakdown with owners
/goalkit.report <period>          → Progress report
/goalkit.review <scope>           → Goal retrospective
/goalkit.taskstoissues            → Convert tasks to GitHub issues
```

---

## References

- **Methodology**: See `goal-driven.md` for full Goal-Driven Development methodology
- **Examples**: See `examples.md` for real-world goal examples
- **Templates**: See `templates/` directory for all template files
- **Commands**: See `templates/commands/` for step-by-step guides
- **Constitution**: See `memory/constitution.md` for project principles

---

**Last Updated**: 2025-11-26
**Version**: 1.0
**For**: [AGENT_NAME]

**Next Steps**:
1. Copy this file to: `[AGENT_NAME].md` (e.g., CLAUDE.md, CURSOR.md)
2. Or reference this guide in your agent configuration
3. When user runs `/goalkit.*` commands, follow the corresponding guide above
