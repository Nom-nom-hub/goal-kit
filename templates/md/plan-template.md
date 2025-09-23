# Implementation Plan: [PLAN TITLE]

**Plan ID**: `[PLAN-ID]`  
**Goal ID**: `[GOAL-ID]`  
**Spec ID**: `[SPEC-ID]`  
**Created**: [DATE]  
**Status**: Draft  
**Timeline**: [ESTIMATED TIMELINE]

## Execution Flow (main)
```
1. Parse specification requirements
   → Extract key tasks and dependencies
2. Estimate effort for each task
   → Use [NEEDS CLARIFICATION: specific estimation question] for unclear tasks
3. Sequence tasks based on dependencies
4. Allocate resources and assign owners
5. Define milestones and checkpoints
6. Identify risks and mitigation strategies
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Plan has uncertainties"
8. Return: SUCCESS (plan ready for task breakdown)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT needs to be done and WHY
- ❌ Avoid specific implementation details (code solutions)
- 👥 Written for project team and stakeholders

### Section Requirements
- **Mandatory sections**: Must be completed for every plan
- **Optional sections**: Include only when relevant to the implementation
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
When creating this plan from a specification:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption you'd need to make
2. **Don't guess**: If the spec doesn't specify something (e.g., "database design" without schema), mark it
3. **Think like a project manager**: Every vague task should fail the "estimable and actionable" checklist item
4. **Common underspecified areas**:
   - Resource allocation and team assignments
   - Timeline estimates and milestones
   - Risk assessment and mitigation
   - Integration points and dependencies
   - Testing and quality assurance approach

---

## Tasks & Timeline *(mandatory)*

### Phase 1: [PHASE NAME]
- **[Task 1]**: [Description, estimated effort]
- **[Task 2]**: [Description, estimated effort]

### Phase 2: [PHASE NAME]
- **[Task 3]**: [Description, estimated effort]
- **[Task 4]**: [Description, estimated effort]

### Milestones
1. **[Milestone 1]**: [Description, target date]
2. **[Milestone 2]**: [Description, target date]

---

## Resources & Assignments *(mandatory)*

### Team Members
- **[Role 1]**: [Number of people, required skills]
- **[Role 2]**: [Number of people, required skills]

### Tools & Infrastructure
- **[Tool 1]**: [Purpose and requirements]
- **[Tool 2]**: [Purpose and requirements]

---

## Risks & Mitigation *(mandatory)*

### Identified Risks
- **[Risk 1]**: [Description, probability, impact]
  → **Mitigation**: [Strategy to reduce probability or impact]
- **[Risk 2]**: [Description, probability, impact]
  → **Mitigation**: [Strategy to reduce probability or impact]

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Plan Quality
- [ ] No implementation details (specific code solutions)
- [ ] Focused on outcomes and deliverables
- [ ] Written for project team and stakeholders
- [ ] All mandatory sections completed

### Plan Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Tasks are estimable and actionable
- [ ] Dependencies and sequence are clear
- [ ] Resources and timeline are defined

---

## Execution Status
*Updated by main() during processing*

- [ ] Specification requirements parsed
- [ ] Key tasks extracted
- [ ] Ambiguities marked
- [ ] Timeline estimated
- [ ] Resources allocated
- [ ] Review checklist passed

---