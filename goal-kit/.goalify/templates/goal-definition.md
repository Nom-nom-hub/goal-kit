# Goal Definition: [GOAL TITLE]

**Goal Branch**: `[###-goal-name]`
**Created**: [DATE]
**Status**: Draft
**Input**: User description: "$ARGUMENTS"

## Execution Flow (main)
```
1. Parse user description from Input
   → If empty: ERROR "No goal description provided"
2. Extract key concepts from description
   → Identify: goal type, objectives, constraints, stakeholders
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill Goal Statement & Success Criteria section
   → If no clear objectives: ERROR "Cannot determine success criteria"
5. Generate Resource Requirements
   → Each requirement must be realistic and achievable
   → Mark ambiguous requirements with [NEEDS CLARIFICATION]
6. Identify Key Stakeholders and Dependencies
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Goal definition has uncertainties"
   → If implementation details found: ERROR "Remove specific solutions"
8. Return: SUCCESS (goal definition ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT needs to be achieved and WHY
- ❌ Avoid HOW to implement (no specific tools, methods, or technologies)
- 👥 Written for goal stakeholders, not implementers

### Section Requirements
- **Mandatory sections**: Must be completed for every goal
- **Optional sections**: Include only when relevant to the goal
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
When creating this goal definition from a user prompt:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption you'd need to make
2. **Don't guess**: If the prompt doesn't specify something (e.g., "build software" without type), mark it
3. **Think like a manager**: Every vague requirement should fail the "measurable and achievable" checklist item
4. **Common underspecified areas**:
   - Success criteria and measurement methods
   - Resource requirements and constraints
   - Stakeholder identification and roles
   - Timeline expectations and deadlines
   - Risk factors and mitigation approaches

---

## Goal Statement *(mandatory)*

### Primary Objective
[Describe the main goal in clear, specific language]

### Success Criteria
1. **Given** [initial state], **When** [goal activities], **Then** [specific, measurable outcome]
2. **Given** [initial state], **When** [goal activities], **Then** [specific, measurable outcome]

### Scope Boundaries
- **In Scope:** [What is included in this goal]
- **Out of Scope:** [What is explicitly not included]
- **Assumptions:** [Key assumptions that must hold true]

## Context and Rationale *(mandatory)*

### Why This Goal Matters
[Explain the importance and impact of achieving this goal]

### Current State Analysis
[Describe the current situation and what needs to change]

### Strategic Alignment
[How this goal supports broader objectives or initiatives]

### Constraints and Limitations
- [Limitation 1]: [Description and impact]
- [Limitation 2]: [Description and impact]

## Success Metrics *(mandatory)*

### Primary Metrics
| Metric | Target | Measurement Method | Frequency |
|--------|--------|-------------------|-----------|
| [Metric 1] | [Target Value] | [How to measure] | [Daily/Weekly/Monthly] |
| [Metric 2] | [Target Value] | [How to measure] | [Daily/Weekly/Monthly] |

### Secondary Metrics
- [Supporting metric 1]: [Target and measurement]
- [Supporting metric 2]: [Target and measurement]

*Example of marking unclear metrics:*
- [Metric 3]: [Target] via [NEEDS CLARIFICATION: measurement method not specified]
- [Metric 4]: [NEEDS CLARIFICATION: target value not specified] via [measurement method]

## Resource Requirements *(mandatory)*

### Team and Skills
**Required Roles:**
- [Role 1]: [Responsibilities and skills needed]
- [Role 2]: [Responsibilities and skills needed]

**Time Commitment:**
- [Role]: [Estimated hours/days]
- [Role]: [Estimated hours/days]

### Budget and Materials
**Budget Allocation:**
- Personnel: $[Amount]
- Materials/Equipment: $[Amount]
- Contingency: $[Amount]
- **Total Budget:** $[Amount]

**Key Resources:**
- [Resource 1]: [Purpose and requirements]
- [Resource 2]: [Purpose and requirements]

### Dependencies
**Internal Dependencies:**
- [Dependency 1]: [What is needed and from whom]
- [Dependency 2]: [What is needed and from whom]

**External Dependencies:**
- [External factor 1]: [Market conditions, vendor delivery, etc.]
- [External factor 2]: [Regulatory requirements, partner commitments]

## Risk Assessment *(mandatory)*

### Potential Risks
| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|-------------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Mitigation approach] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Mitigation approach] |

### Risk Response Plan
- **Risk Threshold:** [Point at which action is required]
- **Contingency Plans:** [Backup strategies if primary approach fails]
- **Risk Monitoring:** [How risks will be tracked and reported]

## Stakeholder Analysis *(mandatory)*

### Key Stakeholders
**Primary Stakeholders:**
- [Stakeholder 1]: [Role, interest, and influence]
- [Stakeholder 2]: [Role, interest, and influence]

**Secondary Stakeholders:**
- [Stakeholder 3]: [Role, interest, and influence]
- [Stakeholder 4]: [Role, interest, and influence]

### Communication Plan
- **Communication Frequency:** [How often stakeholders need updates]
- **Communication Methods:** [Preferred channels and formats]
- **Key Messages:** [Important information to communicate regularly]

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] No implementation details (specific tools, methods, technologies)
- [ ] Focused on goal value and business needs
- [ ] Written for goal stakeholders, not implementers
- [ ] All mandatory sections completed
- [ ] Clear, concise, and professional language

### Goal Definition Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Success criteria are measurable and unambiguous
- [ ] Scope is clearly bounded
- [ ] Resource requirements are realistic
- [ ] Dependencies and assumptions identified
- [ ] Risks have been identified and mitigation planned
- [ ] Stakeholders have been identified and communication planned

### Quality Standards
- [ ] Goal statement is SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
- [ ] Success metrics are quantifiable and trackable
- [ ] Resource requirements are realistic and available
- [ ] Timeline is realistic and accounts for potential delays
- [ ] Risk assessment is comprehensive and realistic

---

## Execution Status
*Updated by main() during processing*

- [ ] User description parsed
- [ ] Key concepts extracted
- [ ] Ambiguities marked
- [ ] Goal statement defined
- [ ] Success criteria established
- [ ] Resource requirements identified
- [ ] Risks assessed
- [ ] Stakeholders analyzed
- [ ] Review checklist passed

---

## Next Steps
*After this goal definition is approved*

1. **Milestone Planning:** Break the goal into manageable milestones
2. **Resource Allocation:** Assign team members and secure resources
3. **Timeline Development:** Create detailed schedule with dependencies
4. **Risk Mitigation:** Develop detailed risk management plans
5. **Stakeholder Alignment:** Get buy-in and approval from key stakeholders

---

*This goal definition serves as the foundation for all planning and execution activities.*