# Milestone Plan: [GOAL]

**Strategy Alignment**: Links to `/goals/[###-goal-name]/strategies.md`  
**Goal Branch**: `[###-goal-name]` | **Date**: [DATE]

**Note**: This template is filled in by the `/goalkit.milestones` command. See `.goalkit/templates/commands/milestones.md` for the execution workflow.

## Summary

Extract from goal and strategy: primary outcome + milestone progression. Keep to 2-3 sentences.

*Example: "Implement live code review comments via WebSocket. Milestones: 1) Backend infrastructure + API, 2) Client real-time sync, 3) User testing & refinement."*

## Progress Tracking Context

**Goal Priority**: [e.g., P1-Critical, P2-High, P3-Medium]
**Milestone Focus**: [What is being validated or delivered in each milestone?]
**Success Metrics**: [Key metrics from goal that milestones must satisfy]
**Target Timeline**: [Overall timeline and milestone schedule]
**Team Structure**: [Who is responsible for each milestone?]

## Strategy Check

*GATE: Confirms this milestone plan aligns with selected strategy.*

Validate milestones execute selected strategy (from strategies.md) and don't diverge.
*Example: "Milestones execute WebSocket strategy by 1) building infrastructure, 2) client integration, 3) validation."*

## Milestone Structure

### Documentation (this goal)

```markdown
.goalkit/
├── goals/
│   └── [###-goal-name]/
│       ├── milestones.md      # This file (/goalkit.milestones command output)
│       ├── research.md        # Milestone 0 output (/goalkit.milestones command)
│       ├── data-model.md      # Milestone 1 output (/goalkit.milestones command)
│       ├── quickstart.md      # Milestone 1 output (/goalkit.milestones command)
│       ├── contracts/         # Milestone 1 output (/goalkit.milestones command)
│       └── actions.md         # Milestone 2 output - detailed milestone tasks
```

### Milestones (SELECTED APPROACH)

**Milestone 1: Backend Infrastructure & API** (Weeks 1-2)
- **Deliverable**: WebSocket server infrastructure, comment storage API, auth/permissions
- **Value**: Enables backend to support real-time comments; foundation for all future work
- **Success Criteria**: API serves 1000 req/sec, WebSocket connections stable
- **Validation**: Internal testing with load tests; infrastructure team sign-off
- **Risk**: Network reliability - mitigation includes HTTP polling fallback

**Milestone 2: Client Real-Time Sync** (Weeks 3-5)
- **Deliverable**: Editor integration, live comment rendering, optimistic UI updates
- **Value**: Reviewers see comments without page refresh; experience meets P1 story
- **Success Criteria**: Comments appear in <2s (SC-001), 85% of reviewers use feature (SC-002)
- **Validation**: Internal reviewer testing; 10 power users test for 1 week
- **Risk**: UX complexity - mitigation includes telemetry to catch issues

**Milestone 3: User Testing & Refinement** (Weeks 6)
- **Deliverable**: Bug fixes, performance optimization, monitoring dashboards
- **Value**: Production-ready feature; meets all success criteria
- **Success Criteria**: 95th percentile latency <2s, zero data loss in testing
- **Validation**: Beta test with 50 users; measure SC-003 (review time reduction)
- **Risk**: Adoption slower than expected - mitigation includes user education

### Milestone Rationale

Each milestone delivers **standalone value** while building toward the full goal:
- M1 enables backend team to work in parallel on other features
- M2 delivers P1 user story (live comments in editor)
- M3 validates complete feature works at scale

Sequence matches selected WebSocket strategy and validates riskiest assumption (latency requirement) in M2.

## Complexity Tracking

> **Fill ONLY if Vision Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., Complex milestone structure] | [current need] | [why simple approach insufficient] |
| [e.g., Multi-phase validation] | [specific problem] | [why single-phase approach insufficient] |
