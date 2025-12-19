# Strategy Plan: [GOAL]

**Goal Alignment**: Links to `/goals/[###-goal-name]/goal.md`  
**Goal Branch**: `[###-goal-name]` | **Date**: [DATE]

**Note**: This template is filled in by the `/goalkit.strategies` command. See `.goalkit/templates/commands/strategies.md` for the execution workflow.

## Summary

Extract from goal definition: primary outcome + strategic approach. Keep to 2-3 sentences.

*Example: "Enable live code review comments in the editor by implementing WebSocket-based comment sync. Risk is network reliability; benefit is 40% faster reviews."*

## Strategic Context

**Goal Priority**: [e.g., P1-Critical, P2-High, P3-Medium]
**Strategic Alignment**: [e.g., User Experience, Business Growth, Technical Infrastructure]
**Resource Budget**: [e.g., 2 person-months, 200 hours or N/A]
**Target Timeline**: [e.g., 6 weeks, Q1 2024]
**Team Structure**: [single/multi-person]
**Risk Tolerance**: [low/medium/high - with specific risks]

## Vision Check

*GATE: Must pass before exploring strategies. Validates alignment with project vision.*

Link to vision success scenario and confirm this strategy supports it.
*Example: "Supports Vision Scenario 1 (Code Review Efficiency) by reducing context switching."*

## Strategy Structure

### Documentation (this goal)

```markdown
.goalkit/
├── goals/
│   └── [###-goal-name]/
│       ├── strategies.md        # This file (/goalkit.strategies command output)
│       ├── research.md          # Strategy 0 output (/goalkit.strategies command)
│       ├── data-model.md        # Strategy 1 output (/goalkit.strategies command)
│       ├── quickstart.md        # Strategy 1 output (/goalkit.strategies command)
│       ├── contracts/           # Strategy 1 output (/goalkit.strategies command)
│       └── actions.md           # Strategy 2 output - detailed implementation tasks
```

### Strategy Options

**Option 1: WebSocket-Based Live Comments (SELECTED)**
- **Approach**: Real-time comment sync via persistent WebSocket connection
- **Resources**: 2 engineers, 6 weeks (backend + frontend)
- **Timeline**: 4 weeks dev + 2 weeks testing/refinement
- **Risk**: Medium - Network reliability, fallback to polling required
- **Cost**: ~$500/month server infrastructure (WebSocket servers)
- **Benefit**: <2s latency, best UX, highest adoption potential

**Option 2: Polling-Based Comments**
- **Approach**: Client polls server every 2-3 seconds for new comments
- **Resources**: 1 engineer, 3 weeks
- **Timeline**: 2 weeks dev + 1 week testing
- **Risk**: Low - Simple, battle-tested
- **Cost**: Minimal infrastructure
- **Downside**: 2-3s latency, higher server load, worse UX

**Option 3: Hybrid (Polling + WebSocket)**
- **Approach**: WebSocket for active reviews, polling for background updates
- **Resources**: 2 engineers, 8 weeks
- **Timeline**: 5 weeks dev + 3 weeks testing
- **Risk**: Low-Medium - More complex implementation
- **Benefit**: Balances UX with reliability
- **Cost**: $200-300/month server infrastructure

### Decision Rationale

**Selected**: Option 1 (WebSocket-Based)

**Why this approach**:
- Goal requires <2s latency; polling can't meet this
- Research shows reviewers (P1 beneficiary) need instant feedback for flow state
- Our infrastructure team has WebSocket expertise
- Customer interviews confirmed <2s is adoption threshold

**Why alternatives rejected**:
- Polling doesn't meet SC-001 success criteria (2s latency requirement)
- Hybrid approach adds complexity without proportional benefit for initial launch
- Vision Scenario 1 explicitly requires "immediate feedback" experience

**Key assumptions**:
- WebSocket infrastructure is operationally mature in our company
- Fallback to HTTP polling will be sufficient during outages
- 2 engineers available for full duration

## Complexity Tracking

### **Fill ONLY if Vision Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., High complexity strategy] | [current need] | [why simple approach insufficient] |
| [e.g., Multi-team coordination] | [specific problem] | [why single-team approach insufficient] |

## Rollout & Onboarding Strategy

*GATE: Strategy is incomplete without a plan for how users will adopt it. (Mitigates Mistake 11)*

**Discovery Plan**:
- [ ] How will users find this features? (e.g., In-app tour, email, changelog, auto-redirect)
- [ ] [Specific item]

**Adoption Plan**:
- [ ] What materials are needed? (e.g., Documentation, training video, FAQ)
- [ ] [Specific item]
