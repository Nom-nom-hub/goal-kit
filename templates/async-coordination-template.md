# Async-First Collaboration: [GOAL]

**Goal**: [Name] | **Goal ID**: [###] | **Created**: [Date]

---

## Summary

*How this goal executes with async-first communication patterns.*

This goal follows **async-first principles**:
- Default to async communication (Slack, docs, email)
- Sync meetings only for decisions that truly need real-time discussion
- Written clarity over lengthy meetings
- Respect for distributed teams and deep focus work

---

## Daily Async Standup

### Format
**When**: Daily at [time] (or EOD if in different time zone)  
**Where**: [#channel or shared doc]  
**Who reports**: All team members on goal  
**Duration**: 2-3 sentences max per person

### Template
```
[Your name] - [Date]
✅ Completed: [What you finished yesterday]
🔄 Working on: [What you're doing today]
🚧 Blockers: [Anything blocking you? (or "None")]
💬 Help needed: [Any assistance needed? (or "None")]
```

### Example
```
Alice - Jan 15
✅ Completed: WebSocket server architecture designed + reviewed
🔄 Working on: Implementing connection pooling logic
🚧 Blockers: None
💬 Help needed: None
```

### Response Expectations
- **Same day** (8 hours) for blockers
- **Next day** (24 hours) for status updates
- **Async only** - no standup meeting

---

## Weekly Async Updates

### Format
**When**: [Day of week, e.g., Friday EOD]  
**Where**: [Channel or shared doc]  
**Who reports**: Goal owner + milestone leads  
**Duration**: ~1-2 paragraphs per update

### Template
```markdown
## Week of [DATE]

### Progress
- Milestone: [completion %] (target [%])
- [Key deliverable]: [Status]
- Metrics: [SC-001: 50% of target], etc.

### What Went Well
- [Win or smooth execution]
- [Team collaboration or quick decision]

### Blockers & Help Needed
- [Blocker 1]: [Impact] - [mitigation in progress]
- [Blocker 2]: [Impact] - [help needed from X]

### Confidence
- Timeline: [On track / 90% confident / At risk]
- Quality: [On track / 90% confident / At risk]
- Team morale: [Good / Neutral / Concerned]
- Next week focus: [Top 3 priorities]
```

### Example
```markdown
## Week of Jan 15-19

### Progress
- Milestone 1: 100% (complete)
- Milestone 2: 40% (target 50%)
- SC-001 latency: 2.5s (target <2s) - on track for optimization

### What Went Well
- Backend infrastructure shipped ahead of schedule
- Integration with frontend started smoothly
- Team energy high, no burnout signals

### Blockers & Help Needed
- API contract feedback from Bob (frontend lead): In progress, expect Tuesday
- DevOps capacity for load testing: Working with Carol on scheduling

### Confidence
- Timeline: On track (M2 on schedule for completion)
- Quality: Good (all code reviewed, tests passing)
- Team morale: Excellent
- Next week focus: Complete M2 frontend integration, begin load testing
```

### Response Expectations
- **Within 48 hours** for blockers requiring response
- **By next weekly update** for general questions

---

## Milestone Handoff Protocol

### Handoff Points in This Goal
| Milestone | Handoff From | Handoff To | Date | Deliverable |
|-----------|---|---|---|---|
| [M1→M2] | [Team/Person A] | [Team/Person B] | [Date] | [What transfers] |
| [M2→M3] | [Team/Person B] | [Team/Person C] | [Date] | [What transfers] |

### Handoff Process

**1 week before handoff**:
- Sending team schedules handoff review
- Document what will be handed off (code, design, specs, data, etc.)
- Identify questions receiving team has

**At handoff date**:
- Sending team completes handoff deliverable
- Receiving team reviews and accepts OR raises concerns
- Escalation if concerns (see Escalation Path below)

**After handoff**:
- Receiving team owns work
- Sending team available for ~1 week questions
- Post-handoff support winds down

### Handoff Acceptance Criteria
Each milestone defines what "done" means:

**Milestone 1 Handoff Acceptance**:
- [ ] API documented and tested (endpoint specs + examples)
- [ ] WebSocket infrastructure stable (passes load tests)
- [ ] Database schema finalized (no breaking changes expected)
- [ ] Code reviewed + merged to main branch
- [ ] Frontend team confirms they have what they need

**Milestone 2 Handoff Acceptance**:
- [ ] Client code working + performance targets met
- [ ] UI/UX flows validated with power users
- [ ] Integration tests passing (frontend + backend together)
- [ ] Monitoring/alerts configured for new feature
- [ ] QA team confirms ready for testing phase

**Milestone 3 Handoff Acceptance**:
- [ ] All bugs from beta testing fixed
- [ ] Documentation complete (user guides, API docs)
- [ ] Performance benchmarks achieved
- [ ] Rollout plan documented + stakeholders aligned
- [ ] Product team confirms ready for launch

---

## Async Decision Framework

### Decision Types & Process

**1. Small decisions** (reversible, local impact)
- **Example**: "Should we use Redis or Memcached?"
- **Process**: Owner decides + async notification
- **Timeline**: Same day
- **Escalation**: None (owner decides)

**2. Medium decisions** (somewhat reversible, team impact)
- **Example**: "Should we prioritize M2 over fixing bugs in M1?"
- **Process**: Owner proposes, team has 24 hours to object
- **Timeline**: 24 hours to decision
- **Escalation**: If objection, go to Escalation Path

**3. Large decisions** (hard to reverse, multi-team impact)
- **Example**: "Should we change the API contract?"
- **Process**: Owner proposes + gets sign-off from affected teams (48 hours)
- **Timeline**: 48 hours minimum
- **Escalation**: If teams disagree, escalate immediately

### Async Decision Template
```markdown
## Decision: [Topic]

**Proposed by**: [Person]
**Decision due**: [Date]
**Affected teams**: [Who's impacted]

### The decision
[What are we deciding?]

### Options considered
- **Option A**: [description] - Pros: [list] - Cons: [list]
- **Option B**: [description] - Pros: [list] - Cons: [list]

### Recommendation
[Which option and why]

### Timeline impact
[If we choose A: ...] [If we choose B: ...]

### Questions for team?
[Anything you want input on?]

**Feedback window**: Until [date]
**Decision date**: [date]
```

### Decision Response Expectations
- **Must respond** if listed in "Affected teams"
- **By decision deadline** (same day for small, 24h for medium, 48h for large)
- **Object or approve** - silence = approval

---

## Learning Capture Ritual

### Ongoing Learning Capture
**When**: During execution, not just at end  
**Where**: [Shared doc or channel]  
**Format**:

```markdown
## Learning: [Topic] - [Date]

**What happened**:
[Describe the situation]

**Why it matters**:
[Why is this a learning?]

**Key insight**:
[The actual learning / pattern observed]

**How it applies**:
[What should we do differently next time?]

**Tags**: [success / failure / process / technical / team]
```

### Examples
```markdown
## Learning: WebSocket stability - Jan 15

**What happened**:
We found that WebSocket connections were dropping during high load testing

**Why it matters**:
This was a risk we identified but underestimated

**Key insight**:
Connection pooling + fallback to HTTP polling is critical. We can't just build for the happy path.

**How it applies**:
Next time we build real-time features, build polling fallback from day 1, not as afterthought.

**Tags**: success, technical, learning


## Learning: Async decision velocity - Jan 18

**What happened**:
We made API contract decision async (48h window) instead of sync meeting

**Why it matters**:
We were concerned async would slow decisions, but it didn't

**Key insight**:
Written proposals + 48h feedback window is actually faster than scheduling sync meetings across time zones

**How it applies**:
Default to async decisions for all non-urgent items. Reserve sync for emergency issues only.

**Tags**: process, success
```

### Learning Capture Cadence
- **Weekly review**: Goal owner reviews learnings from past week
- **Shared in updates**: Include top learnings in weekly async update
- **Captured in review**: Full learnings doc created at goal completion

---

## Sync Meeting Exceptions

### When Sync Meetings Are Needed
Only for these critical decision types:
1. **Emergency escalations** - Production issue or critical blocker
2. **Design debates** - Fundamental architecture disagreement
3. **Onboarding** - Getting new team member up to speed
4. **Demos** - Showing work to stakeholders/customers

### Sync Meeting Protocol

**Scheduling**:
- Minimum 48 hours notice
- Find time across time zones (respect all zones)
- Max 1 hour duration
- Async notes posted within 2 hours

**Attendees**:
- Only people who MUST be in the room
- Others get async notes
- Optional attendance = people don't need to attend

**Agenda**:
- Posted 24 hours before (written)
- Stick to 1-hour limit
- Decisions documented in writing after

**Output**:
- Decision documented in shared doc
- Notes posted to [#channel]
- No "decide in meeting and tell everyone later"

### Example Sync Meetings
- "Emergency: Production WebSocket crash" (30 min)
- "Design decision: Should we redesign message format?" (45 min)
- "Onboarding: Meet new frontend engineer" (30 min)
- "Customer demo: Show real-time collab to 5 key customers" (1 hour)

---

## Escalation Path

### When to Escalate
- **Team can't reach consensus** on a decision (24 hours)
- **Blocker blocking other goals** (immediately)
- **Safety/security concern** (immediately)
- **Quality issue impacting success criteria** (immediately)

### Escalation Steps

**Step 1**: Report to goal owner + affected team leads  
**Response time**: Within 4 hours  
**Decision timeline**: 24 hours max

**Step 2**: If not resolved, escalate to [Title/Person]  
**Response time**: Within 2 hours  
**Decision timeline**: 8 hours max  

**Step 3**: If still not resolved, escalate to [Title/Person]  
**Response time**: Immediate  
**Decision timeline**: 2 hours max  

### Escalation Template
```markdown
## Escalation: [Topic]

**Escalated by**: [Person]
**Date escalated**: [Date/Time]

**Issue**: [What's the problem?]
**Context**: [Why does it matter? Who's affected?]
**Options**: [What are the possible solutions?]
**Recommendation**: [What should we do?]
**Timeline**: [How urgent?]

**Waiting for**: [Decision from whom?]
```

---

## Communication Channels

| Type | Channel | Audience | Response Time |
|------|---------|----------|---|
| Daily standup | #[channel] or doc | Team only | Same day blockers, next day OK |
| Weekly updates | #[channel] or doc | Team + stakeholders | 48 hours to questions |
| Decisions | Shared doc | Affected teams | 24-48 hours by deadline |
| Learnings | Shared doc | All team | Ongoing capture |
| Blockers | @mention in Slack | Needed person | 4 hours |
| Emergencies | Phone call / DM | Immediate | 30 minutes |

---

## FAQ

**Q: What if I need to talk to someone urgently?**  
A: Use Slack @mention for 4-hour response. Phone call if life-or-death (literally).

**Q: What if the async decision window isn't long enough?**  
A: Extend it. Better to delay decision 24 hours than make bad decision fast.

**Q: Can we do a standup meeting instead of async?**  
A: Only if everyone is in same time zone (rare). Async is default.

**Q: What if someone doesn't respond to decision window?**  
A: Silence = approval. But flag with them first that decision matters.

---

## Related Documents

- `templates/cross-goal-coordination-template.md` - Coordinate with other goals
- `templates/team-roles-template.md` - Define team roles and RACI
- `docs/async-collaboration-guide.md` - Full async-first guide
- `execution.md` - This goal's execution plan
