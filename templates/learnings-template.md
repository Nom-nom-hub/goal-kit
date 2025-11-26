# Learnings & Retrospective: [GOAL]

**Goal Branch**: `[###-goal-name]` | **Date**: [DATE] | **Milestone Completed**: [M1/M2/M3]

**Note**: Fill this out after completing each milestone or the full goal. Use this to capture learning for future goals and improvements.

## Milestone Summary

**Planned Outcome**: What was supposed to be delivered in this milestone?

*Example: "Implement live code review comments in the editor with <2s latency."*

**Actual Outcome**: What was actually delivered?

*Example: "Delivered live comments with polling fallback. WebSocket latency achieved 1.8s p95, but decided to keep polling as primary path due to network reliability concerns."*

**Timeline**: Planned vs. Actual

| Phase | Planned | Actual | Variance |
|-------|---------|--------|----------|
| Design/Planning | 2 days | 3 days | +1 day (more edge cases than expected) |
| Implementation | 6 days | 5 days | -1 day (team was experienced with tech stack) |
| Testing | 2 days | 4 days | +2 days (latency optimization took longer) |
| **Total** | **10 days** | **12 days** | **+2 days** |

## What Went Well ✅

1. **Clear acceptance criteria from goal stage**
   - SC-001 and SC-002 metrics made it obvious when we were done
   - Prevented scope creep and unnecessary features
   - Example: "Polling fallback saved us from over-engineering WebSocket reliability."

2. [What exceeded expectations?]

3. [What was done faster/better than expected?]

## What Was Harder Than Expected ⚠️

1. **Latency optimization for mobile clients**
   - Assumption: "Polling every 2-3s would be sufficient"
   - Reality: Mobile networks added 5-8s variance; needed more aggressive caching
   - Impact: Required additional optimization phase
   - Action for next goal: Test on multiple network conditions earlier

2. [What took longer?]

3. [What assumptions were wrong?]

## Validation & Metrics

**Success Criteria Achievement**:

| Criterion | Target | Achieved | Notes |
|-----------|--------|----------|-------|
| SC-001: <2s latency (p95) | <2000ms | 1800ms ✅ | WebSocket path only; polling slower |
| SC-002: 85% reviewer adoption | 85% | 78% ⚠️ | Mobile users still use separate tool |
| SC-003: Review time reduction | 20m → 12m | 20m → 14m ⚠️ | 30% improvement vs. 40% target |

**Key Learning**: Mobile experience was secondary consideration but became blocker for full adoption. Next goal should treat mobile and desktop equally.

## Team Feedback

**What the team said went well**:
- Code review process was smooth (clear acceptance criteria)
- WebSocket infrastructure support was excellent
- Daily standups kept everyone aligned

**What the team said could improve**:
- Need earlier load testing (found issues late in M2)
- Mobile-specific testing should start in M1, not M3
- Documentation of API contracts needed sooner

## Customer/Stakeholder Feedback

**Quantitative**:
- 78% of desktop reviewers adopted feature within first week
- Mobile adoption slow: only 12% using live comments
- Average review time: 20m → 14m (vs. target 12m)
- User satisfaction: 4.1/5 on desktop, 2.8/5 on mobile

**Qualitative**:
- Desktop users love it: "Finally can do reviews without context switching"
- Mobile users frustrated: "Too laggy to be useful on the go"
- Power users wanting: "Show me which reviewers are currently looking at my PR"

## Key Insights & Principles

**What we learned about the problem domain**:

1. **Mobile experience is critical for adoption**
   - We underestimated how many reviews happen on mobile (30% of usage)
   - Latency tolerance is lower on mobile (need <1s, not <2s)
   - Future feature strategy must include mobile from the start

2. **Network reliability matters more than latency for real-time features**
   - Polling is more reliable than WebSocket on our infrastructure
   - Users tolerate slightly higher latency if connection is stable
   - Recommendation: Default to polling, upgrade to WebSocket for premium experience

3. **Clear success criteria are worth more than elegant design**
   - We built a simpler solution than initially planned, but it delivered the goals
   - Power users appreciated measurable feedback over feature richness
   - Lesson: Constrain scope to critical metrics, not feature count

## Assumptions Validated ✅ / Invalidated ❌

| Assumption | Result | Evidence |
|------------|--------|----------|
| Reviewers need <2s latency | ✅ Partially valid | Desktop: yes, Mobile: no (need <1s) |
| WebSocket will improve adoption | ❌ Invalidated | Polling actually more stable; adoption limited by mobile |
| P1 story (live comments in editor) sufficient for MVP | ✅ Validated | Desktop users engaged; mobile users still need more |
| 2-week timeline feasible | ❌ Invalidated | Took 6 weeks with optimization work |

## What Should Change Next Time

### For This Project (Follow-up Goals)

1. **Create mobile-first goal**
   - Current goal was desktop-first; mobile experience needs dedicated goal
   - Accept that mobile and desktop have different success criteria
   - Estimated effort: 4-6 weeks to optimize polling + reduce payload size

2. **Deepen adoption measurement**
   - Track which user segments use the feature (by OS, review style, etc.)
   - Current metrics are team-wide; need per-segment data
   - Estimated effort: Add analytics; 2-3 weeks to instrument

3. **Consider hybrid sync strategy**
   - Polling works, WebSocket helps, but WebSocket adds complexity
   - Test "WebSocket for connected clients, polling fallback" more thoroughly
   - Estimated effort: 2 weeks to A/B test properly

### For Future Goals (Methodology Improvements)

1. **Add "mobile/multi-platform" as explicit dimension to vision**
   - Current vision-driven process doesn't surface platform constraints early
   - Recommendation: Add "Target Platforms" section to vision-template.md
   - Would have caught mobile gap in strategy phase, not execution phase

2. **Expand acceptance criteria with negative cases**
   - Our success criteria only had happy-path metrics
   - Should include: "Works on 4G networks with 50% packet loss"
   - Recommendation: Add "Non-functional criteria" section to goal-template.md

3. **Build in earlier validation loops**
   - We waited until M3 to validate with real users
   - Should validate riskiest assumptions in M1 (not M2/M3)
   - Recommendation: Make user validation explicit in milestone-template.md

## Next Steps

### For This Goal
- ✅ **Complete**: Desktop experience is production-ready
- 🔄 **In Progress**: Gather mobile-specific requirements for follow-up goal
- 📋 **Planned**: Schedule mobile optimization goal for Q2 (4-6 week effort)

### For Project Roadmap
- Add "Mobile Code Review Experience" as P1 goal after this one
- Consider creating a "Mobile-First Development" principle in vision
- Allocate time for mobile-specific load testing in all future goals

## Artifacts & References

- **Goal Document**: `/goals/[###-goal-name]/goal.md`
- **Execution Plan**: `/goals/[###-goal-name]/execution.md`
- **User Feedback**: `/goals/[###-goal-name]/feedback.md` (if exists)
- **Metrics Dashboard**: [Link to analytics/monitoring dashboard]
- **Team Notes**: [Link to meeting notes or wiki]

---

*This learnings document becomes part of the project's knowledge base. Use insights here to improve future goals and the overall development process.*
