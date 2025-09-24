# Project Goals: [PROJECT NAME]

**Project**: `[PROJECT_NAME]`
**Created**: [DATE]
**Status**: Draft
**Input**: User goals: "$ARGUMENTS"

## Execution Flow (main)
```
1. Parse user goals from Input
   → If empty: ERROR "No goals provided"
2. Extract key objectives and outcomes from goals
   → Identify: primary goals, success metrics, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill Goal Breakdown & Success Metrics section
   → If no clear objectives: ERROR "Cannot determine success criteria"
5. Generate Success Criteria and Validation
   → Each criterion must be measurable
   → Mark ambiguous requirements
6. Identify Key Stakeholders and Impact Areas
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Goals have uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (goals ready for strategizing)
```

---

## 🎯 Quick Guidelines
- ✅ Focus on WHAT outcomes we want to achieve and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for stakeholders, not developers
- 📊 Define measurable success criteria

### Section Requirements
- **Mandatory sections**: Must be completed for every project
- **Optional sections**: Include only when relevant to the goals
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
When creating goals from user input:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption you'd need to make
2. **Don't guess**: If the goals don't specify something (e.g., "user base size" without scale), mark it
3. **Think like a product manager**: Every vague goal should fail the "measurable success criteria" checklist item
4. **Common underspecified areas**:
   - Target user segments and scale
   - Success metrics and measurement methods
   - Timeframes and milestones
   - Resource constraints
   - Business impact and ROI expectations

---

## Goal Breakdown & Success Metrics *(mandatory)*

### Primary Project Objectives
[Describe the main outcomes and value proposition in plain language]

### Key Performance Indicators (KPIs)
1. **KPI-001**: [Measurable metric, e.g., "User engagement rate of 70%"]
2. **KPI-002**: [Measurable metric, e.g., "Task completion time reduced by 50%"]
3. **KPI-003**: [Measurable metric, e.g., "Error rate below 1%"]

### Success Criteria *(must be measurable)*
1. **Given** [baseline state], **When** [goal achieved], **Then** [measurable outcome]
2. **Given** [baseline state], **When** [goal achieved], **Then** [measurable outcome]

### Edge Cases & Constraints
- What happens when [boundary condition]?
- How does the solution handle [constraint scenario]?

## Stakeholder Analysis *(mandatory)*

### Primary Stakeholders
- **[Stakeholder Type]**: [Their goals, needs, and how this project serves them]

### Impact Assessment
- **Business Impact**: [How does this achieve business objectives?]
- **User Impact**: [How does this improve user experience?]
- **Technical Impact**: [What technical debt or improvements result?]

### Success Validation *(include if validation methods are specific)*
- **[Validation Method]**: [How to verify the goal is met, e.g., "A/B testing with 1000 users"]
- **[Validation Method]**: [How to verify the goal is met, e.g., "Performance benchmarking against current system"]

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on outcomes and business value
- [ ] Written for business stakeholders
- [ ] All mandatory sections completed

### Goal Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Goals are achievable with clear success criteria
- [ ] Success criteria are measurable and testable
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified
- [ ] Stakeholders and impact areas defined

---

## Execution Status
*Updated by main() during processing*

- [ ] User goals parsed
- [ ] Key objectives extracted
- [ ] Ambiguities marked
- [ ] Success metrics defined
- [ ] Stakeholders identified
- [ ] Review checklist passed

---