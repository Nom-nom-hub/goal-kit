---
description: Create measurable milestones and progress indicators for achieving goals.
scripts:
  sh: .goalkit/scripts/bash/setup-milestones.sh --json "{ARGS}"
  ps: .goalkit/scripts/powershell/setup-milestones.ps1 -Json "{ARGS}"
agent_scripts:
  sh: .goalkit/scripts/bash/update-agent-context.sh __AGENT__
  ps: .goalkit/scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/goalkit.milestones` in the triggering message **is** the milestone planning description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that milestone planning, do this:

1. **Locate Associated Goal**: Search for the goal that milestones will support
   - Use `glob(path="PROJECT_ROOT/.goalkit/goals", pattern="**")` to discover goals
   - Use `list_directory(path="PROJECT_ROOT/.goalkit/goals")` to enumerate goal directories
   - If user specified a goal, locate that specific goal directory
   - If multiple goals exist, ask user to clarify which goal needs milestones
   - If no goals exist, inform user that goals must be created first using `/goalkit.goal`

2. Locate the git repository root and run the script `{SCRIPT}` from there **with the milestone description argument**, then parse its JSON output for GOAL_DIR, BRANCH_NAME and MILESTONE_FILE. All file paths must be absolute.

   **IMPORTANT**:
   
   - The milestone description argument is passed as the entire user input from $ARGUMENTS
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\\''m Groot' (or double-quote if possible: "I'm Groot")
   - First find the git repository root by looking for `.git` directory or using git command to locate it
   - Change to the repository root directory before executing the script
   - You must only ever run this script once
   - The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for

3. Load `.goalkit/templates/milestones-template.md` to understand required sections.

4. Follow this execution flow:

    1. Parse user description from Input
       If empty: ERROR "No milestone planning provided"
    2. Extract key concepts from description
       Identify: milestone structure, measurement approach, validation points, learning objectives
    3. For unclear aspects:
       - Make informed guesses based on context and best practices
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts milestone validation or learning
         - Multiple reasonable but conflicting measurement approaches exist
         - No reasonable default exists
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: measurement approach > validation criteria > milestone sequence
    4. Fill Milestone Definition Framework
       If no clear progress steps: ERROR "Cannot determine milestone structure"
    5. Generate Progress Tracking Framework
       Each milestone must have clear success indicators and measurement approaches
       Use reasonable defaults for unspecified details (document assumptions in Assumptions section)
    6. Define Review Process
       Establish regular assessment schedule and evaluation framework
    7. Outline Success Validation
       Define how to validate each milestone's achievement
    8. Return: SUCCESS (milestones ready for execution)

5. Write the milestone plan to MILESTONE_FILE using the template structure, replacing placeholders with concrete details derived from the milestone planning (arguments) while preserving section order and headings.

6. **Milestone Quality Validation**: After writing the initial milestone plan, validate it against quality criteria:

   a. **Create Milestone Quality Checklist**: Generate a checklist file at `GOAL_DIR/checklists/milestone-quality.md` using the checklist template structure with these validation items:
   
      ```markdown
      # Milestone Quality Checklist: [MILESTONE NAME]
      
      **Purpose**: Validate milestone completeness and quality before proceeding to execution
      **Created**: [DATE]
      **Goal**: [Link to associated goal]
      **Milestones**: [Link to milestones.md]
      
      ## Content Quality
      
      - [ ] Focuses on learning and validation, not just implementation activities
      - [ ] Focused on measurable progress toward goals
      - [ ] Written for non-technical stakeholders
      - [ ] All mandatory sections completed
      
      ## Milestone Completeness
      
      - [ ] No [NEEDS CLARIFICATION] markers remain
      - [ ] Milestones are testable with clear success indicators
      - [ ] Progress metrics are measurable with specific targets
      - [ ] Learning objectives clearly defined for each milestone
      - [ ] Validation criteria are specific and achievable
      - [ ] Milestones align with goal success criteria from associated goal
      - [ ] Review and adaptation framework is defined
      - [ ] Adaptation triggers are clearly specified
      
      ## Milestone Readiness
      
      - [ ] All milestones have clear success criteria
      - [ ] Progress tracking framework is comprehensive 
      - [ ] Milestones build on each other in logical sequence
      - [ ] No implementation details leak into milestone definition
      
      ## Notes
      
      - Items marked incomplete require milestone updates before `/goalkit.execute`
      ```
      
   b. **Run Validation Check**: Review the milestone plan against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant milestone sections)
      
   c. **Handle Validation Results**:
      
      - **If all items pass**: Mark checklist complete and proceed to step 6
      
      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific issues
        2. Update the milestone plan to address each issue
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining issues in checklist notes and warn user
      
      - **If [NEEDS CLARIFICATION] markers remain**:
        1. Extract all [NEEDS CLARIFICATION: ...] markers from the milestone plan
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by measurement/validation/sequence impact) and make informed guesses for the rest
        3. For each clarification needed (max 3), present options to user in this format:
        
           ```markdown
           ## Question [N]: [Topic]
           
           **Context**: [Quote relevant milestone section]
           
           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]
           
           **Suggested Answers**:
           
           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested answer] | [What this means for the milestone] |
           | B      | [Second suggested answer] | [What this means for the milestone] |
           | C      | [Third suggested answer] | [What this means for the milestone] |
           | Custom | Provide your own answer | [Explain how to provide custom input] |
           
           **Your choice**: _[Wait for user response]_
           ```
        
        4. **CRITICAL - Table Formatting**: Ensure markdown tables are properly formatted:
           - Use consistent spacing with pipes aligned
           - Each cell should have spaces around content: `| Content |` not `|Content|`
           - Header separator must have at least 3 dashes: `|--------|`
           - Test that the table renders correctly in markdown preview
        5. Number questions sequentially (Q1, Q2, Q3 - max 3 total)
        6. Present all questions together before waiting for responses
        7. Wait for user to respond with their choices for all questions (e.g., "Q1: A, Q2: Custom - [details], Q3: B")
        8. Update the milestone plan by replacing each [NEEDS CLARIFICATION] marker with the user's selected or provided answer
        9. Re-run validation after all clarifications are resolved
   
   d. **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

7. Report completion with branch name, milestone file path, checklist results, and readiness for the next phase (`/goalkit.execute`).

**NOTE:** The script creates and checks out the new branch and initializes the milestone file before writing.

## Key rules

- Focus on learning and validation, not just implementation activities
- Create milestones that demonstrate measurable progress toward goals
- Include clear success criteria and measurement approaches for each milestone
- Ensure milestones build on each other and align with chosen strategies

## Overview

The `/goalkit.milestones` command breaks goals into measurable progress steps that demonstrate movement toward goal achievement. Unlike tasks that focus on implementation activities, milestones focus on learning and validation.

## Purpose

This command creates a milestone plan that:
- Breaks goals into measurable progress indicators
- Focuses on learning and hypothesis validation
- Provides clear indicators of goal progress
- Enables adaptive execution based on results

## When to Use

Use `/goalkit.milestones` when:
- You have a well-defined goal with selected strategy
- You need to break the goal into achievable progress steps
- You want to establish clear validation points
- You're ready to plan execution with learning focus

## Input Format

```
/goalkit.milestones [description of milestone structure and measurement approach]
```

### Example Input

```
/goalkit.milestones Create milestones that validate the task management approach:
1. Core concept validation with paper prototypes
2. Technical feasibility with working prototype
3. User value validation with small user group
4. Business model validation with broader rollout
Focus on learning at each step and measurable progress indicators.
```

## Output

The command generates:
- `goals/[###-goal-name]/milestones.md` - Comprehensive milestone plan
- Measurement framework for tracking progress
- Learning objectives for each milestone
- Foundation for adaptive execution

### Agent File Creation Instructions

When processing `/goalkit.milestones` commands, AI agents should:
1. Locate the appropriate goal directory in the `goals/` folder (the most recently created or specified goal)
2. Create the `milestones.md` file inside that goal directory
3. Use the current date in YYYY-MM-DD format for the "Date" field
4. Write the complete milestone plan using the template structure below
5. Reference the associated goal and strategy in the document header
6. After creating the milestones file, inform the user that the milestone plan has been completed and suggest next steps using `/goalkit.execute`

### File Creation Process
- **Locate Directory**: `goals/[###-goal-name]/` (most recent goal or specified goal)
- **Create File**: `goals/[###-goal-name]/milestones.md` with the milestone content
- **Template**: Use the structure provided in the "Milestone Components" section below

## Milestone Components

### 1. Milestone Definition Framework
- **Measurable Outcomes**: Clear indicators of milestone achievement
- **Learning Objectives**: What to discover at each milestone
- **Value Delivery**: User/business value at each step
- **Implementation Approaches**: Different ways to achieve the milestone

### 2. Progress Tracking Framework
- **Overall Progress Metrics**: How to measure goal advancement
- **Milestone Health Indicators**: Signs of milestone success or trouble
- **Adaptation Triggers**: When to adjust approach or sequence

### 3. Review Process
- **Milestone Review Cadence**: Regular assessment schedule
- **Review Framework**: What to evaluate at each review
- **Decision Framework**: How to adapt based on results

### 4. Success Validation
- **Milestone Success Criteria**: When milestone is considered complete
- **Goal Progress Indicators**: How milestone advances the goal
- **Learning Quality Assessment**: How to evaluate insights gained

## Key Differences from Spec-Driven Development

| Spec-Driven | Goal-Driven |
|-------------|-------------|
| Detailed task breakdowns | Measurable milestone definitions |
| Implementation activity focus | Learning and validation focus |
| Linear task execution | Adaptive milestone progression |
| Specification compliance | Outcome and learning validation |

## Integration with Other Commands

### Before Using `/goalkit.milestones`
- **`/goalkit.vision`**: Provides guiding principles for milestone design
- **`/goalkit.goal`**: Defines the goal milestones should advance
- **`/goalkit.strategies`**: Provides strategy context for milestone planning

### After Using `/goalkit.milestones`
- **`/goalkit.execute`**: Implement milestones with learning and adaptation

## Best Practices

### Milestone Design
- **Measurable Outcomes**: Each milestone should have clear success indicators
- **Independent Value**: Milestones should deliver standalone value
- **Learning Focus**: Every milestone should test key hypotheses
- **Progressive Validation**: Early milestones validate riskiest assumptions

### Progress Tracking
- **Multiple Indicators**: Use several metrics to validate each milestone
- **Regular Assessment**: Review progress at appropriate intervals
- **Adaptation Readiness**: Plan how to adjust based on results
- **Stakeholder Communication**: Keep stakeholders informed of progress

### Learning Integration
- **Hypothesis Testing**: Frame milestones as assumption validation
- **Insight Capture**: Document what works and what doesn't
- **Pattern Recognition**: Identify trends across milestones
- **Knowledge Transfer**: Apply learning to subsequent milestones

## Common Milestone Patterns

### Risk-Reduction Milestones
- **Technical Risk Validation**: Prove technical approach feasibility
- **User Experience Validation**: Confirm user interaction patterns
- **Business Model Validation**: Test revenue or adoption assumptions
- **Integration Validation**: Ensure solution works in real environment

### Value-Delivery Milestones
- **Core Value Milestones**: Deliver fundamental user benefit
- **Enhancement Milestones**: Add incremental improvements
- **Scale Milestones**: Expand to broader user base
- **Optimization Milestones**: Improve existing functionality

### Learning Milestones
- **Exploration Milestones**: Test new approaches or technologies
- **Comparison Milestones**: Evaluate different strategy options
- **Optimization Milestones**: Improve based on user feedback
- **Innovation Milestones**: Introduce novel capabilities

## Validation and Adaptation

### Milestone Review Process
- **Completion Review**: Assess if milestone achieved intended outcomes
- **Learning Review**: Document insights and discoveries
- **Strategy Review**: Evaluate if current approach remains valid
- **Planning Review**: Adjust subsequent milestones based on learning

### Adaptation Framework
- **Continue**: When milestones validate current approach
- **Adjust**: When milestones suggest minor modifications
- **Pivot**: When milestones indicate major strategy change needed
- **Pause**: When external factors require reassessment

## Examples

### Example 1: User Onboarding Milestone Plan
```
/goalkit.milestones For user onboarding improvement:
1. Onboarding flow clarity (measure comprehension)
2. Value proposition validation (measure early engagement)
3. Feature discovery optimization (measure feature usage)
4. Long-term retention improvement (measure sustained usage)
Each milestone should validate key onboarding hypotheses.
```

### Example 2: Performance Improvement Milestone Plan
```
/goalkit.milestones For application performance:
1. Baseline measurement and bottleneck identification
2. Critical path optimization (measure core interaction speed)
3. Secondary optimization (measure overall responsiveness)
4. Scale validation (measure performance under load)
Focus on measurable speed and responsiveness improvements.
```

### Example 3: Feature Development Milestone Plan
```
/goalkit.milestones For new feature development:
1. Core concept validation (measure user interest)
2. Technical feasibility demonstration (measure implementation possibility)
3. User experience validation (measure usability and satisfaction)
4. Business value confirmation (measure adoption and retention)
Each milestone should demonstrate clear progress toward feature goals.