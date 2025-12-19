# Implementation Plan: [GOAL]

**Milestones Alignment**: Links to `/goals/[###-goal-name]/milestones.md`  
**Goal Branch**: `[###-goal-name]` | **Date**: [DATE]

**Note**: This template is filled in by the `/goalkit.execute` command. See `.goalkit/templates/commands/execute.md` for the execution workflow.

## Summary

Extract from goal and milestones: primary outcome + detailed implementation plan. Keep to 2-3 sentences.

*Example: "Implement live code review comments via WebSocket across 3 milestones. Backend API in Weeks 1-2, client integration in Weeks 3-5, user testing and refinement in Week 6. Key risk is network reliability; mitigated with HTTP polling fallback."*

## Implementation Context

**Goal Priority**: [e.g., P1-Critical, P2-High, P3-Medium]
**Implementation Approach**: [e.g., Agile 2-week sprints, Waterfall phases, Experimental MVP]
**Resource Allocation**: [e.g., 2 engineers full-time, 6 weeks total]
**Success Metrics**: [Key metrics from goal to validate during implementation]
**Target Timeline**: [Specific dates or sprint numbers for each milestone]
**Team Structure**: [Who owns what - e.g., "Alice (backend), Bob (frontend)"]
**Communication Plan**: [Rituals - e.g., "Daily async status in #channel, Weekly demo on Fridays"]
**Verification Strategy**: [How we test - e.g., "Unit tests for logic, Manual QA for UI, E2E for critical flows"]
**Key Risks & Mitigations**: [Specific risks from milestones with concrete mitigations]

## Milestones Check

*GATE: Confirms implementation executes planned milestones without scope creep.*

Link each execution phase to corresponding milestone and validate it delivers expected value.
*Example: "Week 1-2 executes Milestone 1 (API & infrastructure); Week 3-5 executes Milestone 2 (client sync)."*

## Implementation Structure

### Documentation (this goal)

```markdown
.goalkit/
├── goals/
│   └── [###-goal-name]/
│       ├── execution.md       # This file (/goalkit.execute command output)
│       ├── research.md        # Implementation 0 output (/goalkit.execute command)
│       ├── data-model.md      # Implementation 1 output (/goalkit.execute command)
│       ├── quickstart.md      # Implementation 1 output (/goalkit.execute command)
│       ├── contracts/         # Implementation 1 output (/goalkit.execute command)
│       └── tasks.md           # Implementation 2 output - detailed implementation tasks
```

### Implementation Phases (EXECUTING MILESTONES)

**Phase 1: Backend Infrastructure & API** (Weeks 1-2, Milestone 1)
- Sprint 1 (Days 1-5): Design WebSocket server architecture, set up database schema
- Sprint 2 (Days 6-10): Implement comment storage API, build auth/permissions layer, load testing
- **Responsible**: Backend team (Alice lead)
- **Deliverables**: `/api/comments`, `/api/comment-threads`, WebSocket server ready for load tests
- **Definition of Done**: Load tests pass (1000 req/sec), code reviewed, documented API contracts

**Phase 2: Client Real-Time Sync** (Weeks 3-5, Milestone 2)
- Sprint 3 (Days 11-15): Integrate WebSocket client, implement comment rendering in editor
- Sprint 4 (Days 16-20): Build optimistic UI updates, handle offline states with polling fallback
- Sprint 5 (Days 21-25): Performance optimization, telemetry for latency monitoring
- **Responsible**: Frontend team (Bob lead), coordinated with backend on contracts
- **Deliverables**: Editor integration complete, <2s latency achieved, 10 power users testing
- **Definition of Done**: SC-001 and SC-002 metrics met in internal testing

**Phase 3: User Testing & Refinement** (Week 6, Milestone 3)
- Sprint 6 (Days 26-30): Bug fixes from power user feedback, performance tuning, monitoring setup
- Sprint 7 (Days 31-35): Beta rollout to 50 users, measure SC-003 (review time reduction)
- **Responsible**: Full team with product lead coordination
- **Deliverables**: Production-ready feature, monitoring dashboards, user education materials
- **Definition of Done**: All success criteria met, zero P1 bugs, rollout plan documented

### Learning & Adaptation Checkpoints

**End of Milestone 1** (Day 10): Does infrastructure meet load requirements? If not, scale up servers or adjust strategy.

**End of Milestone 2** (Day 25): Are power users achieving <2s latency? If not, optimize polling fallback or consider alternative strategy.

**End of Milestone 3** (Day 35): Did review time decrease by target amount? Collect feedback for future enhancements.

## Complexity Tracking

> **Fill ONLY if Vision Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., Complex implementation structure] | [current need] | [why simple approach insufficient] |
| [e.g., Multi-phase validation] | [specific problem] | [why single-phase approach insufficient] |