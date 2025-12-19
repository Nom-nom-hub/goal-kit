# Retrospective Review: [GOAL NAME]

**Goal Alignment**: Links to `/goals/[###-goal-name]/goal.md` and success criteria  
**Goal Branch**: `[###-goal-name]` | **Date**: [DATE] | **Review Type**: Milestone/Final

**⚠️ Note on Learnings vs Review**:
- **This Template (Review)**: What did we ACHIEVE? Planned vs actual comparison, performance assessment
- **Learnings Template**: What did we LEARN? Team insights, assumption validation, process improvements
- Both are needed; use both after each milestone

**Note**: This template is filled in by the `/goalkit.review` command. See `.goalkit/templates/commands/review.md` for the execution workflow.

## Summary

Extract from goal and execution: achievement level, what succeeded, what fell short, high-level assessment. Keep to 2-3 sentences.

*Example: "Milestone 2 (Client Real-Time Sync) achieved 2 of 3 success criteria. Latency target exceeded (1.8s vs 2.0s). Adoption target missed (82% vs 85%) due to mobile gap. Overall delivery on-time with high quality (zero P1 bugs)."*

## Review Context

**Review Period**: [Milestone 1/2/3 or Final]
**Goals Reviewed**: [Single goal or multi-goal review]
**Review Type**: [Milestone review, Final retrospective, Interim check]
**Team Size**: [Who executed - e.g., "2 engineers, 1 PM"]
**Participants in Review**: [Who conducted review - e.g., "team + stakeholders"]

## Learnings Check

*GATE: Confirms learnings-template.md was completed separately for future improvement.*

Review focuses on past achievement; learnings focus on future improvement.
Link to learnings template: `/goals/[###-goal-name]/learnings.md`

## Review Structure

### Documentation (this goal)

```markdown
.goalkit/
├── goals/
│   └── [###-goal-name]/
│       ├── review.md        # This file (/goalkit.review command output)
│       ├── analysis.md      # Review 0 output (/goalkit.review command)
│       ├── insights.md      # Review 1 output (/goalkit.review command)
│       ├── recommendations.md # Review 1 output (/goalkit.review command)
│       └── action-items.md  # Review 2 output - detailed improvement steps
```

### Goal Achievement Assessment

**Success Criteria Comparison**:

| Criterion | Planned | Actual | Status | Notes |
|-----------|---------|--------|--------|-------|
| SC-001: <2s latency (p95) | <2000ms | 1800ms | ✅ Exceeded | +200ms better than target |
| SC-002: 85% adoption | 85% | 82% | ⚠️ Missed | Desktop 90%, mobile 12% (platform gap) |
| SC-003: Review time reduction | 20m → 12m | 20m → 14m | ⚠️ Partial | 30% improvement vs 40% target |

**Overall Assessment**: 
- 1 of 3 criteria exceeded
- 2 of 3 criteria partially achieved
- Quality high (zero P1 bugs)
- Delivery on-time

---

### Deliverable Quality Assessment

**Code Quality**:
- All code passed peer review
- Test coverage: 92% (excellent)
- Zero critical bugs, 2 minor bugs found and fixed during beta

**Architecture Quality**:
- WebSocket infrastructure performs stably
- API contracts clear and well-documented
- Fallback to polling works reliably

**User Experience Quality**:
- Desktop experience intuitive and fast
- Mobile experience limited (network/battery concerns)
- Accessibility: WCAG 2.1 AA compliant

---

### Process Assessment

**Strategy Effectiveness**:
- Selected WebSocket strategy was correct for desktop
- Didn't account for mobile platform needs (lesson for next goal)
- Trade-off analysis was thorough in hindsight

**Execution Approach**:
- Phased breakdown worked well
- Task dependencies clear and managed effectively
- Team collaboration smooth (no blocking issues)

### Start / Stop / Continue
*Retrospective actions for the team*
- **Start**: [New practice to begin]
- **Stop**: [Bad habit to end]
- **Continue**: [Good practice to keep]

**Measurement & Validation**:
- Success criteria were measurable and realistic
- Built-in power user validation effective
- SC-003 (review time) should have included mobile separately

**Timeline Performance**:
- Estimated 6 weeks, delivered in 6 weeks
- No schedule slip
- Phase 1 completed early (saved 1 day), reinvested in Phase 2 polish

---

### What We Delivered vs What We Planned

| Aspect | Planned | Delivered | Assessment |
|--------|---------|-----------|------------|
| Core functionality | Live comments in editor | ✅ Live comments desktop + polling mobile | Good |
| Performance | <2s latency | ✅ 1.8s latency desktop; 3.2s p99 mobile | Exceeded for primary platform |
| Adoption target | 85% | ✅ 90% desktop, 12% mobile | Met for desktop; gap for mobile |
| Team velocity | 6 weeks | ✅ 6 weeks | On schedule |
| Bug rate | <5 P1 bugs | ✅ 0 P1 bugs | Better than planned |

**Key Gap**: Desktop/mobile performance difference not anticipated in strategy phase

---

### Recommendations for Next Phase

**For the product**:
1. Create separate P1 goal for mobile experience (estimated 4-6 weeks)
2. Implement polling-only mode as interim improvement

**For the process** (detailed in learnings-template.md):
1. Add "multi-platform" as explicit dimension to vision/goal templates
2. Require separate acceptance scenarios for major platforms
3. Validate platform assumptions earlier in strategy phase

---

### Connection to Learnings

**This review answers**: Did we achieve what we planned?

**For deeper analysis**, see learnings-template.md which answers:
- What did we learn about the problem domain?
- What assumptions were validated/invalidated?
- What should we change in future goals?
- What process improvements are needed?

## Summary Judgment

**Achievement Level**: **2.5/3** (83%)
- Exceeded on latency (SC-001)
- Met on desktop adoption, missed on overall adoption (SC-002)
- Partial on review time reduction (SC-003)

**Quality Level**: **High**
- Zero P1 bugs
- 92% test coverage
- On-time delivery
- Team rated execution as smooth

**Recommendation**: 
✅ **Ship to production** with mobile adoption caveat documented. Plan follow-up mobile goal as high priority based on insights from learnings-template.md.