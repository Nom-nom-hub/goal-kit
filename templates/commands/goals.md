# /goals Command
*Define project goals and objectives before technical implementation*

## Overview
The `/goals` command establishes the high-level objectives and outcomes for your project. This is the foundational step in Goal-Driven Development, ensuring all subsequent work aligns with clear, measurable goals.

## When to Use
- At the beginning of a new project or feature
- When you need to define success criteria
- Before any technical planning or implementation
- When stakeholders need alignment on project direction

## Usage
```
/goals [GOAL_DESCRIPTION]
```

**Examples:**
```
/goals Build a task management app that helps teams organize work, track progress, and meet deadlines efficiently
```

```
/goals Create a customer support system that reduces response time by 50% and improves customer satisfaction scores
```

## What It Does
1. **Parses your goal description** and extracts key objectives
2. **Identifies success metrics** and measurable outcomes
3. **Creates stakeholder analysis** to understand impact areas
4. **Generates a goal document** in `goals/[FEATURE_NAME]/goal.md`
5. **Marks any ambiguities** that need clarification
6. **Provides a review checklist** to ensure goal quality

## Goal Structure
The generated goal document includes:
- **Primary objectives** and success criteria
- **Key Performance Indicators (KPIs)**
- **Stakeholder analysis** and impact assessment
- **Success validation methods**
- **Review checklist** for quality assurance

## Best Practices
- **Be outcome-focused**: Describe what you want to achieve, not how to build it
- **Make goals measurable**: Include specific metrics and success criteria
- **Consider stakeholders**: Think about who benefits and how
- **Keep it high-level**: Avoid technical implementation details
- **Be specific about constraints**: Mention timeframes, budgets, or other limitations

## Examples

### Good Goal Definition
```
/goals Develop a mobile app that helps users track their daily water intake, with reminders, progress visualization, and social features to encourage consistent hydration habits
```

### Poor Goal Definition (too technical)
```
/goals Build a React Native app with Firebase backend, water tracking components, push notifications, and social sharing features
```

### Good Goal with Metrics
```
/goals Create an e-commerce platform that increases conversion rates by 25% and reduces cart abandonment to under 30% through improved UX and personalized recommendations
```

## Next Steps
After defining goals with `/goals`:
1. **Review the generated goal document** for clarity and completeness
2. **Use `/clarify`** if any aspects need further definition
3. **Use `/strategize`** to develop implementation approaches
4. **Use `/plan`** to create detailed technical plans
5. **Use `/tasks`** to break down into actionable items
6. **Use `/implement`** to execute the work

## Troubleshooting
- **Goals seem unclear**: Use `/clarify` to get more specific about requirements
- **Multiple interpretations possible**: The AI will mark ambiguities with [NEEDS CLARIFICATION] tags
- **Too many goals**: Focus on the primary objectives first, break complex projects into phases
- **No clear success metrics**: Ask yourself "How will I know if this is successful?"