# /clarify Command
*Clarify and validate project goals to ensure clear understanding*

## Overview
The `/clarify` command helps refine and validate project goals to eliminate ambiguity and ensure all stakeholders have a shared understanding. This step is crucial before moving to strategy development.

## When to Use
- When goals seem unclear or ambiguous
- Before developing technical strategies
- When multiple interpretations of goals are possible
- After receiving feedback on initial goal definitions

## Usage
```
/clarify [GOALS_FILE]
```

**Examples:**
```
/clarify goals/user-authentication.md
```

```
/clarify
```

## What It Does
1. **Analyzes existing goals** for clarity and completeness
2. **Identifies ambiguities** and areas needing clarification
3. **Asks targeted questions** to resolve uncertainties
4. **Validates assumptions** about project scope and requirements
5. **Generates clarification notes** in `goals/[FEATURE_NAME]/clarification.md`
6. **Updates goals document** with clarified understanding

## Clarification Process
1. **Ambiguity Detection**: Identify unclear terms, assumptions, or scope
2. **Stakeholder Analysis**: Determine who needs to be involved
3. **Requirement Validation**: Confirm what is and isn't included
4. **Success Criteria**: Ensure measurable outcomes are defined
5. **Constraint Identification**: Surface technical, business, or resource limitations

## Best Practices
- **Be specific**: Ask for concrete examples rather than vague descriptions
- **Challenge assumptions**: Question things that seem obvious
- **Consider edge cases**: Think about unusual scenarios or error conditions
- **Document decisions**: Record why certain interpretations were chosen
- **Involve stakeholders**: Get input from all affected parties

## Examples

### Clarifying Technical Scope
```
Goal: "Build a user authentication system"

Clarification needed:
- What authentication methods (email/password, social login, MFA)?
- Which user roles and permissions are needed?
- What happens during password reset flows?
- Are there any regulatory compliance requirements?
```

### Clarifying Business Requirements
```
Goal: "Increase user engagement by 30%"

Clarification needed:
- What specific metrics define "engagement"?
- Which user segments are we targeting?
- What timeframe for the 30% improvement?
- How will we measure baseline engagement?
```

## Next Steps
After clarifying goals with `/clarify`:
1. **Review clarification notes** for completeness
2. **Update goals document** if needed
3. **Use `/strategize`** to develop implementation approaches
4. **Share with stakeholders** to ensure alignment
5. **Use `/analyze`** to validate overall project consistency

## Troubleshooting
- **Too many questions**: Focus on the most critical ambiguities first
- **Stakeholder disagreement**: Document different perspectives clearly
- **Scope creep**: Use clarification to define firm boundaries
- **Technical vs business ambiguity**: Separate technical clarifications from business ones
- **Unclear success criteria**: Push for specific, measurable outcomes