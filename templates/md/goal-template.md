# Goal Specification: [GOAL TITLE]

**Goal ID**: `[GOAL-ID]`  
**Created**: [DATE]  
**Status**: Draft  
**Priority**: Medium  
**Owner**: [OWNER]

## Execution Flow (main)
```
1. Parse goal description
   → Extract key objectives and success criteria
2. Identify dependencies and related goals
   → Mark with [NEEDS CLARIFICATION: specific dependency question]
3. Define measurable success criteria
   → Each criterion must be testable
   → Mark ambiguous criteria
4. Fill Objectives & Success Criteria section
   → If no clear objectives: ERROR "Cannot determine goal objectives"
5. Identify Key Stakeholders
6. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Goal has uncertainties"
7. Return: SUCCESS (goal ready for specification)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT needs to be achieved and WHY
- ❌ Avoid implementation details (no tech stack, specific solutions)
- 👥 Written for project stakeholders, not just developers

### Section Requirements
- **Mandatory sections**: Must be completed for every goal
- **Optional sections**: Include only when relevant to the goal
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
When creating this goal from a user prompt:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption you'd need to make
2. **Don't guess**: If the prompt doesn't specify something (e.g., "improve user experience" without specifics), mark it
3. **Think like a project manager**: Every vague objective should fail the "measurable and unambiguous" checklist item
4. **Common underspecified areas**:
   - Success metrics and KPIs
   - Timeline and milestones
   - Resource requirements
   - Risk factors
   - Stakeholder expectations

---

## Objectives & Success Criteria *(mandatory)*

### Primary Goal
[Describe the main objective in plain language]

### Success Criteria
1. **Measurable Outcome**: [Specific, measurable result]
2. **Business Impact**: [Value delivered to stakeholders]
3. **Quality Standards**: [Acceptance thresholds]

### Key Stakeholders
- **[Stakeholder 1]**: [Role and interest in the goal]
- **[Stakeholder 2]**: [Role and interest in the goal]

---

## Dependencies & Constraints *(mandatory)*

### Dependencies
- **[Dependency 1]**: [What this goal depends on]
- **[Dependency 2]**: [What this goal depends on]

### Constraints
- **[Constraint 1]**: [Limitation or restriction]
- **[Constraint 2]**: [Limitation or restriction]

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] No implementation details (specific technologies, code solutions)
- [ ] Focused on outcomes and business value
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

### Goal Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Success criteria are measurable and unambiguous
- [ ] Scope is clearly bounded
- [ ] Dependencies and constraints identified

---

## Execution Status
*Updated by main() during processing*

- [ ] Goal description parsed
- [ ] Key objectives extracted
- [ ] Ambiguities marked
- [ ] Success criteria defined
- [ ] Stakeholders identified
- [ ] Review checklist passed

---