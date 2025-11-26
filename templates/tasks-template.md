# Implementation Tasks: [GOAL]

**Execution Alignment**: Links to `/goals/[###-goal-name]/execution.md`  
**Goal Branch**: `[###-goal-name]` | **Date**: [DATE]

**Note**: This template is filled in by the `/goalkit.tasks` command. See `.goalkit/templates/commands/tasks.md` for the execution workflow.

## Summary

Extract from execution plan: detailed work breakdown mapping to phases. Keep to 2-3 sentences.

*Example: "Implement live code review comments across 7 tasks across 3 phases. Phase 1 (Days 1-5): 3 infrastructure tasks. Phase 2 (Days 6-20): 3 client integration tasks. Phase 3 (Days 21-25): 1 testing/refinement task."*

## Task Context

**Goal Priority**: [e.g., P1-Critical, P2-High, P3-Medium]
**Task Approach**: [e.g., Agile sprints, Waterfall phases, Experimental]
**Resource Allocation**: [e.g., 2 engineers, 6 weeks total]
**Success Metrics**: [Key metrics from goal to validate each task batch]
**Target Timeline**: [Sprint schedule with task completion dates]
**Team Structure**: [Who owns what domain - e.g., "Alice (backend), Bob (frontend)"]
**Key Dependencies**: [Tasks that block others - e.g., "API contracts must be defined before client work"]

## Execution Check

*GATE: Confirms task breakdown executes planned execution phases without omissions.*

Validate each task maps to a corresponding execution phase and doesn't introduce scope creep.
*Example: "Phase 1 tasks deliver WebSocket infrastructure; Phase 2 tasks deliver client integration; Phase 3 tasks deliver testing."*

## Task Structure

### Documentation (this goal)

```markdown
.goalkit/
├── goals/
│   └── [###-goal-name]/
│       ├── tasks.md         # This file (/goalkit.tasks command output)
│       ├── research.md      # Task 0 output (/goalkit.tasks command)
│       ├── data-model.md    # Task 1 output (/goalkit.tasks command)
│       ├── quickstart.md    # Task 1 output (/goalkit.tasks command)
│       ├── contracts/       # Task 1 output (/goalkit.tasks command)
│       └── action-items.md  # Task 2 output - detailed work breakdown
```

### Task Breakdown by Phase

**Phase 1: Backend Infrastructure & API** (Days 1-5, 3 tasks)

| Task ID | Task Name | Description | Owner | Effort | DoD | Dependencies |
|---------|-----------|-------------|-------|--------|-----|--------------|
| T-001 | Design WebSocket architecture | Finalize server architecture, scaling strategy | Alice | 8h | Architecture doc approved by infra team | None |
| T-002 | Set up database schema | Create comment storage tables, indexes, migrations | Alice | 6h | Schema reviewed, migrations tested locally | T-001 |
| T-003 | Implement comment API + auth | Build `/api/comments` endpoints, permission layer | Alice | 10h | All endpoints pass load tests (1000 req/sec) | T-002 |

**Critical Path Dependencies**: T-001 → T-002 → T-003 (sequential)

**Parallel Opportunities**: None in Phase 1 (dependency chain)

---

**Phase 2: Client Real-Time Sync** (Days 6-20, 3 tasks)

| Task ID | Task Name | Description | Owner | Effort | DoD | Dependencies |
|---------|-----------|-------------|-------|--------|-----|--------------|
| T-004 | Integrate WebSocket client | Connect editor to WebSocket, handle connection lifecycle | Bob | 10h | Client connects stably, maintains connection | T-003 |
| T-005 | Render comments in editor | Display comments inline, handle threads/replies | Bob | 12h | Comments visible within 2s of posting (SC-001) | T-004 |
| T-006 | Build optimistic UI + polling fallback | Handle offline states, implement HTTP polling fallback | Bob | 8h | Works offline; polling < 3s latency | T-005 |

**Critical Path**: T-003 → T-004 → T-005 → T-006

**Parallel Opportunities**: None (client depends on working API from Phase 1)

---

**Phase 3: Testing & Refinement** (Days 21-25, 1 task)

| Task ID | Task Name | Description | Owner | Effort | DoD | Dependencies |
|---------|-----------|-------------|-------|--------|-----|--------------|
| T-007 | Optimize + monitoring setup | Performance tuning, add latency/error monitoring | Alice & Bob | 10h | <2s p95 latency, monitoring dashboards live | T-006 |

**Critical Path**: T-006 → T-007

---

### Task Blocking & Risk

**Blockers** (if not resolved, can't proceed):
- T-003 (API) blocks all client work (T-004, T-005, T-006)
- Missing API contracts block T-004 start

**Risky Tasks**:
- **T-003** (Load testing under 1000 req/sec) - mitigated by load testing in T-003 itself
- **T-005** (Sub-2s latency) - mitigated by early perf testing in T-004; fallback to polling in T-006
- **T-007** (Optimization) - mitigated by implementing basic performance in T-005

---

### Task Rollout Strategy

**Week 1 (Phase 1)**: Alice builds API infrastructure sequentially (T-001 → T-002 → T-003)

**Week 2-3 (Phase 2)**: Bob integrates client while Alice is available for API fixes (T-004 → T-005 → T-006)
- Days 6-10: T-004 (WebSocket integration)
- Days 11-17: T-005 (Comment rendering)
- Days 18-20: T-006 (Fallback + offline)

**Week 4 (Phase 3)**: Both team members optimize and set up monitoring (T-007)

## Success Criteria Per Task Batch

**Phase 1 Success**: 
- All tasks pass code review
- Load tests confirm 1000 req/sec capacity
- API documentation complete and shared with client team

**Phase 2 Success**:
- SC-001 achieved: Comments visible in <2s (p95)
- SC-002 achieved: 85% of reviewers use live comments in internal testing
- No data loss observed during 1 week of power user testing

**Phase 3 Success**:
- SC-003 achieved: Review time reduced from 20m to 12m+ on average
- Monitoring dashboards operational
- Zero P1 bugs reported in beta