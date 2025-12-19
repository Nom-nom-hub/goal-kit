# Progress Report: [GOAL NAME]

**Goal Alignment**: Links to `/goals/[###-goal-name]/goal.md` success criteria  
**Goal Branch**: `[###-goal-name]` | **Date**: [DATE] | **Report Period**: [e.g., Milestone 2, Week 3, Final]

**Note**: This template is filled in by the `/goalkit.report` command. See `.goalkit/templates/commands/report.md` for the execution workflow.

## Summary

Extract from goal and execution: what was planned, what was delivered, how metrics compare. Keep to 2-3 sentences.

*Example: "Milestone 2 (Client Real-Time Sync) completed on Day 20. Achieved SC-001 (1.8s latency p95) and SC-002 (82% reviewer adoption in testing). Currently tracking toward SC-003 (review time reduction) with early indicators positive."*

## Reporting Context

**Reporting Period**: [e.g., Milestone 2, Week 3, Mid-project, Final]
**Goals Being Reported**: [Single goal or multi-goal period]
**Report Type**: [Progress check, Milestone review, Final assessment]
**Team Size**: [Who executed this - e.g., "2 engineers, 1 product manager"]
**Key Stakeholders**: [Who needs this report - e.g., "product lead, customer success"]

## Metrics Check

*GATE: Confirms this report validates goal success criteria (SC-001, SC-002, SC-003, etc.)*

Report must show achievement against goal metrics, not arbitrary metrics.
*Example: "Report shows achievement of SC-001 (<2s latency) and SC-002 (85% adoption); SC-003 (review time reduction) pending final measurement."*

## Report Structure

### Documentation (this goal)

```markdown
.goalkit/
├── goals/
│   └── [###-goal-name]/
│       ├── report.md        # This file (/goalkit.report command output)
│       ├── analysis.md      # Report 0 output (/goalkit.report command)
│       ├── insights.md      # Report 1 output (/goalkit.report command)
│       ├── recommendations.md # Report 1 output (/goalkit.report command)
│       └── action-items.md  # Report 2 output - detailed next steps
```

### The Ask *(Executive Summary)*
*What do you need right now?*
- [ ] **Decisions**: [e.g., Approve scope change]
- [ ] **Help**: [e.g., Unblock dependency]
- [ ] **FYI**: [e.g., We are on track]

### Risks & Blockers
*Top risks that need attention immediately.*
- **🔴 Blocker**: [Description]
- **🟡 Risk**: [Description]

### Success Criteria Achievement

**Metric Performance Table**:

| Success Criterion | Target | Achieved | Status | Gap | Notes |
|-------------------|--------|----------|--------|-----|-------|
| SC-001: <2s latency (p95) | <2000ms | 1800ms | ✅ Pass | -200ms | WebSocket path performs excellently |
| SC-002: Reviewer adoption | 85% | 82% | ⚠️ Near | -3% | Desktop users 90%; mobile users 12% (expected) |
| SC-003: Review time reduction | 20m → 12m | 20m → 14m | ⚠️ Partial | +2m | 30% improvement vs 40% target |

**Key Finding**: Desktop experience exceeds expectations; mobile experience is limiting factor for SC-002 and SC-003.

---

### Quantitative Results

**Usage & Adoption**:
- Desktop reviewers using live comments: 90% (9/10 power users)
- Mobile reviewers using live comments: 12% (1 of 8)
- Average daily active sessions: 145 (vs. 0 baseline)

**Performance Metrics**:
- Comment latency (p50): 450ms
- Comment latency (p95): 1800ms
- Comment latency (p99): 3200ms (mostly due to mobile clients)
- Server uptime: 99.8% (1 incident, 12 min downtime)

**User Satisfaction**:
- Desktop NPS: +45 (9/10 would recommend)
- Mobile NPS: -10 (limited usefulness)
- Overall feature satisfaction: 4.1/5.0

---

### Qualitative Insights

**What's Working Well**:
- Desktop users love the feature; immediate adoption
- WebSocket infrastructure is stable and scalable
- Team collaboration improved; fewer context switches

**Challenges Encountered**:
- Mobile network variability (5G → 4G → 3G transitions)
- Mobile battery impact from WebSocket connections
- UX needs optimization for small screens

**Recommendations for Next Phase**:
1. **Quick win**: Add polling-only mode for mobile users (improves adoption to 50%+)
2. **Medium-term**: Optimize mobile UX (button placement, gesture controls)
3. **Follow-up goal**: "Mobile Code Review Experience" (4-6 week effort)

---

### Trend Analysis

**Compared to Previous Milestone** (M1: Backend Infrastructure):
- Delivery on-time (Days 6-20 as planned)
- Latency better than estimated (1.8s actual vs 2.0s target)
- Adoption slightly below target (82% vs 85%) due to mobile gap

**Variance Analysis**:
- Effort: +2 days on T-005 (comment rendering—more edge cases than expected)
- Scope: Clean (no scope creep)
- Quality: High (zero P1 bugs in testing)

---

### Connected to Learnings Template

For detailed reflection on what the team learned, metrics validation, and improvements for next goals, see `/goals/[###-goal-name]/learnings.md`

## Action Items from This Report

**Immediate** (next 1-2 weeks):
- [ ] Implement polling-only mode toggle for mobile users
- [ ] Add battery optimization documentation
- [ ] Schedule retrospective with team

**Short-term** (next 3-4 weeks):
- [ ] Mobile UX improvements (buttons, gestures)
- [ ] Load test with mobile clients at scale
- [ ] Plan "Mobile Code Review Experience" goal

**Follow-up**:
- [ ] Review learnings-template.md for insights
- [ ] Plan next goal informed by this report's findings