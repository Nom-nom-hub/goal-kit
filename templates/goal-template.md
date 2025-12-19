# Goal Statement: [GOAL DESCRIPTION]

**Vision Alignment**: Links to `[###-vision-scenario]` from vision.md  
**Goal Branch**: `[###-goal-name]` | **Created**: [DATE] | **Status**: Draft

> **Need a simpler template?** Use the [Lite Template](./lite-goal-template.md) for quick tasks.

## User Stories *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as beneficiary journeys ordered by importance.
  Each user story/journey must be STANDALONE DELIVERABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as independently plannable, validatable, and demonstrable to users.
-->

### Beneficiary Story 1 - [Brief Title] (Priority: P1)

Describe this beneficiary journey in plain language. Who benefits and how?

*Example: "As an engineer, I can see live updates on code review feedback so I can respond to comments without switching windows."*

**Why this priority**: Explain the value and why it has this priority level.

*Example: "Most time is lost context-switching between editor and review tool during active reviews."*

**Standalone Delivery**: How this story can be validated independently.

*Example: "Can be fully validated by implementing live comment polling on code view without async collaboration features."*

**Acceptance Scenarios** *(use Given/When/Then format)*:

1. **Given** a code review is open in the editor, **When** a reviewer posts a comment, **Then** the comment appears within 2 seconds without page refresh
2. **Given** multiple comments on the same line, **When** a user hovers over line numbers, **Then** all comments are visible in a clear thread

---

### Beneficiary Story 2 - [Brief Title] (Priority: P2)

Describe this beneficiary journey in plain language.

**Why this priority**: Explain the value and why it has this priority level.

**Standalone Delivery**: How this story can be validated independently.

**Acceptance Scenarios** *(use Given/When/Then format)*:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

Describe this beneficiary journey in plain language.

**Why this priority**: Explain the value and why it has this priority level.

**Standalone Delivery**: How this story can be validated independently.

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### Edge Cases & Error Handling

- What happens when [boundary condition]? *Example: "Network drops during live comment sync?"*
- How does system handle [error scenario]? *Example: "User's comment fails to post - how does client recover?"*

### Out of Scope *(mandatory)*
*Explicitly list what we are NOT doing to prevent scope creep.*

- [ ] [Feature or requirement specifically excluded]
- [ ] [Feature or requirement specifically excluded]

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST [specific capability]
  - Example: "allow reviewers to see live comment updates in the editor without page refresh"
- **FR-002**: System MUST [specific capability]
- **FR-003**: System MUST [data/persistence requirement]

### Key Entities *(if applicable)*

- **Comment**: Thread identifier, content, timestamp, reviewer ID, line number
- **CodeView**: File content, active reviews, comment threads, user permissions

## Success Criteria *(mandatory)*

### Key Metrics *(2-3 measurable outcomes)*

- **SC-001**: Comments appear in editor within 2 seconds of posting (95th percentile latency)
- **SC-002**: 85% of reviewers use live comments without opening separate review tool
- **SC-003**: Average review time decreases from 20 min to 12 min per PR

### Metric Quality Validation *(use for each success criterion)*

For each metric above, validate quality using this checklist:

**SC-001 Quality Check**:
- [ ] **Measurable**: Can collect via APM/monitoring (specific measurement method defined)
- [ ] **Actionable**: <2s = green (scale), 2-3s = yellow (optimize), >3s = red (pivot)
- [ ] **Leading**: Predicts user satisfaction (latency impacts adoption)
- [ ] **Bounded**: Target <2s, baseline 5s, deadline 6 weeks
- [ ] **Valuable**: Fast feedback improves reviewer experience (links to Vision Scenario 1)

**Baseline Metrics** *(measure before starting work)*:
| Metric | Current Baseline | Measurement Date | Method |
|--------|------------------|------------------|--------|
| SC-001 | 5.2s (p95) | 2024-01-15 | APM dashboard |
| SC-002 | 45% adoption | 2024-01-15 | Analytics |
| SC-003 | 20 min avg | 2024-01-15 | Git metadata |

**Measurement Plan** *(how to track progress)*:
- **Tool**: [Analytics platform, APM, database queries]
- **Frequency**: [Real-time, daily, weekly]
- **Dashboard**: [Link to dashboard when created]
- **Owner**: [Person responsible for tracking]

> **💡 Tip**: Use `/goalkit.metrics` command to create detailed measurement plan. See [Quick Reference](../docs/quick-reference.md) for metric quality guidelines.
