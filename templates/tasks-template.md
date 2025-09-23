# Task Breakdown: [TASK TITLE]

**Task ID**: `[TASK-ID]`  
**Plan ID**: `[PLAN-ID]`  
**Created**: [DATE]  
**Status**: Todo  
**Priority**: Medium  
**Assignee**: [ASSIGNEE]

## Execution Flow (main)
```
1. Parse task requirements from plan
   → Extract key acceptance criteria
2. Define implementation approach
   → Use [NEEDS CLARIFICATION: specific approach question] for unclear requirements
3. Break down into subtasks (if needed)
4. Estimate effort and set due date
5. Identify dependencies
6. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Task has uncertainties"
7. Return: SUCCESS (task ready for execution)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT needs to be done and acceptance criteria
- ❌ Avoid deep implementation details (specific code structure)
- 👥 Written for task assignees and project managers

### Section Requirements
- **Mandatory sections**: Must be completed for every task
- **Optional sections**: Include only when relevant to the task
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
When creating this task from a plan:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption you'd need to make
2. **Don't guess**: If the plan doesn't specify something (e.g., "implement authentication" without method), mark it
3. **Think like a developer**: Every vague requirement should fail the "actionable and testable" checklist item
4. **Common underspecified areas**:
   - Acceptance criteria and success conditions
   - Dependencies on other tasks or systems
   - Required inputs and expected outputs
   - Testing and validation approach
   - Integration requirements

---

## Description & Acceptance Criteria *(mandatory)*

### Task Description
[Detailed description of what needs to be accomplished]

### Acceptance Criteria
1. **[Criterion 1]**: [Specific, testable condition]
2. **[Criterion 2]**: [Specific, testable condition]

### Dependencies
- **[Dependency 1]**: [What this task depends on]
- **[Dependency 2]**: [What this task depends on]

---

## Effort & Timeline *(mandatory)*

### Estimated Effort
- **Development**: [Hours/Days]
- **Testing**: [Hours/Days]
- **Documentation**: [Hours/Days]

### Due Date
[TARGET COMPLETION DATE]

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Task Quality
- [ ] No implementation details (specific code solutions)
- [ ] Focused on outcomes and deliverables
- [ ] Written for task assignee and project manager
- [ ] All mandatory sections completed

### Task Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are actionable and testable
- [ ] Dependencies are identified
- [ ] Effort and timeline are defined

---

## Execution Status
*Updated by main() during processing*

- [ ] Task requirements parsed
- [ ] Key criteria extracted
- [ ] Ambiguities marked
- [ ] Effort estimated
- [ ] Dependencies identified
- [ ] Review checklist passed

---