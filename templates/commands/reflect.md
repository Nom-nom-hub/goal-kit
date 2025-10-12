# /goalkit.reflect Command Template

## Overview

The `/goalkit.reflect` command facilitates deep analysis and learning from completed work to improve future goal achievement outcomes.

## Command Usage

```
/goalkit.reflect [project-goal] [time-period] [focus-area]
```

### Project Goal
- The specific goal, task, or project to reflect on
- Can be referenced by name if it exists in the current project
- Include description if it's a new goal or task

### Time Period
- `last-week`: Reflection on work completed in the last week
- `last-month`: Reflection on work completed in the last month
- `last-quarter`: Reflection on work completed in the last quarter
- `custom`: Custom time period specified (e.g., "since June 1st")

### Focus Area
- `process-effectiveness`: Focus on how work was accomplished
- `outcome-quality`: Focus on the quality of results achieved
- `learning-development`: Focus on skill and knowledge development
- `team-collaboration`: Focus on team dynamics and collaboration
- `resource-utilization`: Focus on how resources were used

## Implementation Guidance

### AI AGENT INSTRUCTIONS

When processing `/goalkit.reflect` requests:

1. **Gather Context**: Collect information about the goal/project and its outcomes
2. **Analyze Patterns**: Identify what worked well and what didn't
3. **Extract Insights**: Surface specific learnings that can inform future work
4. **Document Learnings**: Structure insights in a way that's useful for future reference

### Response Structure

```
# Reflection on "[Project Goal]" ([Time Period])

## What Worked Well
- [Positive aspect 1]
- [Positive aspect 2]
- [Positive aspect 3]

## Challenges Encountered
- [Challenge 1 with brief description]
- [Challenge 2 with brief description]
- [Challenge 3 with brief description]

## Key Learnings
- [Learning 1 with specific insight]
- [Learning 2 with specific insight]
- [Learning 3 with specific insight]

## Future Improvements
- [Improvement 1 with specific action items]
- [Improvement 2 with specific action items]
- [Improvement 3 with specific action items]

## Action Items
1. [Specific action item 1]
2. [Specific action item 2]
3. [Specific action item 3]
```

## Examples

### Example 1: Process Effectiveness Focus
```
/goalkit.reflect "Implement user authentication" "last-month" "process-effectiveness"

# Reflection on "Implement user authentication" (Last Month)

## What Worked Well
- Early stakeholder alignment on requirements
- Good choice of authentication library
- Comprehensive test coverage strategy

## Challenges Encountered
- Delayed decision on password policies causing rework
- Integration complexity with legacy systems
- Underestimated testing time by 40%

## Key Learnings
- Establish security requirements before implementation to avoid rework
- Consider legacy integration needs upfront in planning
- Allocate 20% extra time for authentication systems based on complexity

## Future Improvements
- Create authentication requirements template for future projects
- Establish legacy system assessment checklist
- Build authentication project estimation model with complexity factors

## Action Items
1. Document authentication requirements template
2. Add legacy assessment to project onboarding checklist
3. Update estimation guidelines with authentication factors
```

### Example 2: Outcome Quality Focus
```
/goalkit.reflect "Redesign customer dashboard" "last-month" "outcome-quality"

# Reflection on "Redesign customer dashboard" (Last Month)

## What Worked Well
- Significant improvement in user engagement metrics
- Positive feedback on visual design
- Better information hierarchy than previous version

## Challenges Encountered
- Performance issues with large datasets
- Some users preferred the old interface
- Accessibility compliance took longer than expected

## Key Learnings
- Performance testing with realistic data volumes is critical early in design
- Change resistance is normal but can be mitigated with proper communication
- Accessibility requirements should be factored into timeline from start

## Future Improvements
- Implement performance testing in the design phase
- Include users in design decisions to reduce resistance to change
- Integrate accessibility compliance into initial requirements

## Action Items
1. Add performance testing protocol to design checklist
2. Create user feedback integration plan for future redesigns
3. Update project templates to include accessibility timeline estimates
```

## Integration with Goal Kit Process

The reflection should feed back into:
- `/goalkit.goal`: Improve goal definition based on learnings about feasibility and outcomes
- `/goalkit.strategies`: Consider past learnings when exploring new strategies
- `/goalkit.milestones`: Apply insights to create better milestone definitions
- `/goalkit.execute`: Use learnings to improve execution approaches

## Quality Assurance

Ensure the reflection:
- Is specific and actionable rather than generic advice
- Connects specific cause-and-effect relationships
- Focuses on concrete, changeable factors rather than external constraints
- Provides sufficient detail for future application
- Distinguishes between what worked well and what needs improvement