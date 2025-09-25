# Milestone Planning: [GOAL TITLE]

**Milestone Branch**: `[###-milestone-planning]`
**Created**: [DATE]
**Status**: Draft
**Input**: Goal description: "$ARGUMENTS"

## Execution Flow (main)

```
1. Load goal definition from parent directory
   → If no goal.json: ERROR "No parent goal found"
2. Parse goal scope and objectives
   → Extract: timeline, resources, success criteria
3. Break goal into logical phases
   → Identify: foundation, development, testing, deployment
4. For each phase, create milestones
   → Ensure: clear deliverables, measurable progress, dependencies
5. Define milestone success criteria
   → Each must be testable and achievable
6. Establish dependencies between milestones
   → Mark with [NEEDS CLARIFICATION] if unclear
7. Estimate resources for each milestone
   → Include: time, team, budget, materials
8. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Milestone plan has uncertainties"
   → If milestone too large: ERROR "Break into smaller milestones"
9. Return: SUCCESS (milestone plan ready for execution)
```

---

## ⚡ Quick Guidelines

- ✅ Create milestones that are achievable in 2-6 weeks
- ❌ Don't make milestones longer than 8 weeks without clear justification
- 📏 Each milestone should have 3-7 specific, measurable deliverables

### Milestone Planning Principles

- **Progressive Elaboration:** Start high-level, add detail progressively
- **Balanced Workload:** Distribute effort evenly across timeline
- **Dependency Management:** Clear predecessor/successor relationships
- **Quality Gates:** Each milestone includes validation criteria

---

## Goal Context _(mandatory)_

### Goal Overview

- **Goal:** [Goal Name]
- **Objective:** [Primary goal objective]
- **Timeline:** [Overall goal duration]
- **Success Criteria:** [Key measures of success]

### Resource Constraints

- **Team Size:** [Available team members]
- **Budget Limit:** [Total budget available]
- **Time Frame:** [Hard deadlines or constraints]
- **Other Constraints:** [Technical, regulatory, etc.]

## Milestone Structure _(mandatory)_

### Phase 1: Foundation [Start Date - End Date]

**Milestone 1.1:** [Milestone Name]

- **Duration:** [X weeks]
- **Objective:** [Clear objective for this phase]
- **Status:** [Not Started/In Progress/Completed]

**Key Deliverables:**

- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]
- [ ] [Specific deliverable 3]

**Success Criteria:**

- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Quality standard met]

**Dependencies:** [Previous milestones or external factors]
**Risk Level:** [Low/Medium/High]

**Milestone 1.2:** [Milestone Name]

- **Duration:** [X weeks]
- **Objective:** [Clear objective for this phase]
- **Status:** [Not Started/In Progress/Completed]

**Key Deliverables:**

- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]

**Success Criteria:**

- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

**Dependencies:** [Milestone 1.1, external dependency]
**Risk Level:** [Low/Medium/High]

### Phase 2: Development [Start Date - End Date]

**Milestone 2.1:** [Milestone Name]

- **Duration:** [X weeks]
- **Objective:** [Clear objective for this phase]
- **Status:** [Not Started/In Progress/Completed]

**Key Deliverables:**

- [ ] [Development task 1]
- [ ] [Development task 2]
- [ ] [Development task 3]
- [ ] [Development task 4]

**Success Criteria:**

- [ ] [Quality metric 1 met]
- [ ] [Functionality delivered]
- [ ] [Performance requirement met]

**Dependencies:** [Previous milestone]
**Risk Level:** [Low/Medium/High]

### Phase 3: Validation [Start Date - End Date]

**Milestone 3.1:** [Milestone Name]

- **Duration:** [X weeks]
- **Objective:** [Clear objective for this phase]
- **Status:** [Not Started/In Progress/Completed]

**Key Deliverables:**

- [ ] [Testing completed]
- [ ] [Quality assurance passed]
- [ ] [User acceptance testing]
- [ ] [Documentation updated]

**Success Criteria:**

- [ ] [All tests passing]
- [ ] [Quality gates met]
- [ ] [Stakeholder approval]
- [ ] [Ready for deployment]

**Dependencies:** [All development milestones]
**Risk Level:** [Low/Medium/High]

### Phase 4: Deployment [Start Date - End Date]

**Milestone 4.1:** [Milestone Name]

- **Duration:** [X weeks]
- **Objective:** [Final deployment and handover]
- **Status:** [Not Started/In Progress/Completed]

**Key Deliverables:**

- [ ] [Production deployment]
- [ ] [Training completed]
- [ ] [Handover documentation]
- [ ] [Post-deployment support]

**Success Criteria:**

- [ ] [System operational]
- [ ] [Users trained]
- [ ] [Documentation complete]
- [ ] [Stakeholder sign-off]

**Dependencies:** [All previous milestones]
**Risk Level:** [Low/Medium/High]

## Milestone Tracking Matrix _(mandatory)_

| Milestone | Phase       | Progress | Status      | Start Date | End Date | Owner  | Dependencies |
| --------- | ----------- | -------- | ----------- | ---------- | -------- | ------ | ------------ |
| 1.1       | Foundation  | 0%       | Not Started | [Date]     | [Date]   | [Name] | None         |
| 1.2       | Foundation  | 0%       | Not Started | [Date]     | [Date]   | [Name] | 1.1          |
| 2.1       | Development | 0%       | Not Started | [Date]     | [Date]   | [Name] | 1.2          |
| 3.1       | Validation  | 0%       | Not Started | [Date]     | [Date]   | [Name] | 2.1          |
| 4.1       | Deployment  | 0%       | Not Started | [Date]     | [Date]   | [Name] | 3.1          |

## Resource Allocation _(mandatory)_

### Time Allocation by Milestone

| Phase   | Milestone | Estimated Hours | Team Members | Complexity     |
| ------- | --------- | --------------- | ------------ | -------------- |
| Phase 1 | 1.1       | [X hours]       | [X members]  | [Low/Med/High] |
| Phase 1 | 1.2       | [X hours]       | [X members]  | [Low/Med/High] |
| Phase 2 | 2.1       | [X hours]       | [X members]  | [Low/Med/High] |
| Phase 3 | 3.1       | [X hours]       | [X members]  | [Low/Med/High] |
| Phase 4 | 4.1       | [X hours]       | [X members]  | [Low/Med/High] |

### Budget Allocation by Milestone

| Milestone | Budget    | Resource Type       | Justification |
| --------- | --------- | ------------------- | ------------- |
| 1.1       | $[Amount] | [Internal/External] | [Rationale]   |
| 1.2       | $[Amount] | [Internal/External] | [Rationale]   |
| 2.1       | $[Amount] | [Internal/External] | [Rationale]   |
| 3.1       | $[Amount] | [Internal/External] | [Rationale]   |
| 4.1       | $[Amount] | [Internal/External] | [Rationale]   |

### Team Assignment

| Team Member | Role   | Milestones | Availability     | Expertise    |
| ----------- | ------ | ---------- | ---------------- | ------------ |
| [Name]      | [Role] | [1.1, 2.1] | [Full/Part-time] | [Key skills] |
| [Name]      | [Role] | [1.2, 3.1] | [Full/Part-time] | [Key skills] |

---

## Quality Gates and Validation _(mandatory)_

### Entry Criteria (for each milestone)

- [ ] [Prerequisite condition 1]
- [ ] [Prerequisite condition 2]
- [ ] [Required resources available]
- [ ] [Previous milestones completed]

### Exit Criteria (for each milestone)

- [ ] [Deliverables completed]
- [ ] [Quality standards met]
- [ ] [Testing requirements satisfied]
- [ ] [Stakeholder review completed]
- [ ] [Documentation updated]

### Validation Methods

**Testing Requirements:**

- [ ] Unit testing completed
- [ ] Integration testing passed
- [ ] User acceptance testing done
- [ ] Performance testing completed

**Review Requirements:**

- [ ] Code review completed
- [ ] Design review passed
- [ ] Stakeholder approval obtained
- [ ] Documentation review done

---

## Risk and Contingency Planning _(mandatory)_

### Milestone-Specific Risks

| Milestone   | Risk Description   | Probability    | Impact         | Mitigation            |
| ----------- | ------------------ | -------------- | -------------- | --------------------- |
| [Milestone] | [Risk description] | [High/Med/Low] | [High/Med/Low] | [Mitigation strategy] |
| [Milestone] | [Risk description] | [High/Med/Low] | [High/Med/Low] | [Mitigation strategy] |

### Contingency Budget

- **Total Contingency:** [X% of total budget]
- **Trigger Points:** [Conditions that activate contingency plans]
- **Approval Process:** [How contingency funds are accessed]

### Risk Mitigation Strategies

- **Buffer Time:** [X]% buffer added to milestone durations
- **Parallel Paths:** Alternative approaches identified
- **Early Validation:** Critical assumptions tested early
- **Stakeholder Involvement:** Regular milestone reviews

---

## Communication and Reporting _(mandatory)_

### Milestone Reviews

- **Frequency:** [Weekly/Bi-weekly/Monthly]
- **Format:** [Meeting, email update, dashboard]
- **Attendees:** [Required and optional participants]
- **Agenda:** [Standard review topics]

### Progress Reporting

- **Template:** [Standard reporting format]
- **Metrics:** [KPIs and progress indicators]
- **Distribution:** [Who receives reports]
- **Escalation Process:** [When and how to escalate issues]

### Status Communication

- **Daily Updates:** [How daily progress is communicated]
- **Weekly Summaries:** [Format and content]
- **Milestone Completion:** [Notification process]

---

## Review & Acceptance Checklist

_GATE: Automated checks run during main() execution_

### Milestone Planning Quality

- [ ] Milestones are appropriately sized (2-6 weeks)
- [ ] Clear deliverables for each milestone
- [ ] Measurable success criteria defined
- [ ] Dependencies clearly identified
- [ ] Resource requirements realistic

### Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] All phases have appropriate milestones
- [ ] Quality gates defined for each milestone
- [ ] Risk assessment completed
- [ ] Stakeholder communication planned

### Feasibility

- [ ] Timeline is realistic
- [ ] Resources are available
- [ ] Budget is adequate
- [ ] Dependencies can be met
- [ ] Risks are manageable

---

## Execution Status

_Updated by main() during processing_

- [ ] Goal context loaded
- [ ] Phases identified
- [ ] Milestones created
- [ ] Dependencies mapped
- [ ] Resources allocated
- [ ] Quality gates defined
- [ ] Risks assessed
- [ ] Communication planned
- [ ] Review checklist passed

---

## Next Steps

_After this milestone plan is approved_

1. **Resource Assignment:** Assign specific team members to milestones
2. **Detailed Scheduling:** Create detailed task breakdowns for each milestone
3. **Risk Mitigation:** Develop detailed risk management plans
4. **Stakeholder Review:** Get approval from all stakeholders
5. **Execution Planning:** Prepare for milestone execution

---

_This milestone plan provides the roadmap for achieving the goal objectives._
