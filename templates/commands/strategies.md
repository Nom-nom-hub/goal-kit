---
description: Explore multiple implementation strategies for goals. Ensures consideration of various approaches before implementation.
scripts:
  sh: scripts/bash/setup-strategy.sh "{GOAL_DIR}" --json
  ps: scripts/powershell/setup-strategy.ps1 "{GOAL_DIR}" -Json
agent_scripts:
  sh: scripts/bash/common.sh && update-agent-context
  ps: . scripts/powershell/common.ps1; Update-AgentContext
---

# Quick Prerequisites Check

**BEFORE EXPLORING STRATEGIES**:

1. **Goal exists**: Check `.goalkit/goals/` directory for goal files
2. **Goal is well-defined**: Verify goal has clear success metrics

**If missing**: Tell user to use `/goalkit.goal` first.

## Quick Strategy Exploration Steps

**STEP 1**: Identify the goal to explore strategies for (most recent or specified)

**STEP 2**: Brainstorm 3-4 different approaches to achieve the goal:

- **Approach A**: [Conservative, proven method]
- **Approach B**: [Innovative, higher risk/higher reward]
- **Approach C**: [Balanced, middle-ground approach]
- **Approach D**: [Alternative perspective or methodology]

**STEP 3**: Compare approaches across key dimensions:

- **Feasibility**: How realistic is implementation?
- **Effort**: How much work is required?
- **Risk**: What could go wrong?
- **Learning Potential**: What insights could be gained?

**STEP 4**: Recommend starting strategy with clear rationale

**STEP 5**: Define validation experiments for key assumptions

**STEP 6**: Create `strategies.md` in the goal directory

**STEP 7**: Report completion and remind user of next steps:

- `/goalkit.milestones` - Create measurable progress checkpoints
- `/goalkit.execute` - Implement with learning and adaptation

**🛑 STOP HERE** - Do NOT proceed to milestones or implementation automatically
**🛑 STOP HERE** - Wait for user to explicitly run `/goalkit.milestones`

## Critical Strategy Rules

✅ **DO**: Explore multiple valid approaches (3-4 options minimum)
✅ **DO**: Evaluate feasibility, effort, risk, and learning potential
✅ **DO**: Frame strategies as testable hypotheses
✅ **DO**: Recommend starting point with clear rationale
❌ **DON'T**: Focus on just one "correct" solution
❌ **DON'T**: Include implementation details (languages, frameworks, APIs)
❌ **DON'T**: Skip validation experiments for key assumptions

## Key Reminders

- **Multiple approaches** → Always explore 3+ strategies
- **Testable hypotheses** → Each strategy should be validatable
- **Learning focus** → Strategies should enable insights
- **Always** end with reminder to use `/goalkit.milestones` next
