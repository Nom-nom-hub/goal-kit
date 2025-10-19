---
description: Execute the goal definition workflow by creating a new goal using the goal template to generate a goal definition. This command ensures agents follow the complete methodology by requiring measurable outcomes and success criteria.
scripts:
  # Paths are relative to PROJECT ROOT (not relative to .goalkit/)
  sh: .goalkit/scripts/bash/create-new-goal.sh --json "{ARGS}"
  ps: .goalkit/scripts/powershell/create-new-goal.ps1 -Json "{ARGS}"
agent_scripts:
  # Paths are relative to PROJECT ROOT (not relative to .goalkit/)
  sh: .goalkit/scripts/bash/update-agent-context.sh __AGENT__
  ps: .goalkit/scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## CRITICAL Methodology Adherence Check

**BEFORE PROCEEDING:** Confirm that this is a substantial goal requiring the full methodology (not a simple task suitable for direct implementation):

- **Simple tasks** (use `/goalkit.execute` for direct implementation): visual enhancements, minor fixes, small improvements (e.g., "enhanced header", "fix button color", "add margin", "improve styling")
- **Complex goals** (use full process): new features with measurable outcomes (%,$,timeframes,user counts), system changes, user workflows requiring success metrics

**If this is a simple task, STOP HERE and suggest to the user that they use `/goalkit.execute` for direct implementation instead.**

## CRITICAL Implementation Details Warning

**IMPORTANT:** Goals must NOT contain implementation details (languages, frameworks, APIs). Focus on measurable user/business outcomes instead.

## Outline

The text the user typed after `/goalkit.goal` in the triggering message **is** the goal description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that goal description, do this:

1. **Generate a concise short name** (2-4 words) for the goal:
   - Analyze the goal description and extract the most meaningful keywords
   - Create a 2-4 word short name that captures the essence of the goal
   - Use action-noun format when possible (e.g., "improve-onboarding", "add-authentication")
   - Preserve technical terms and acronyms as appropriate
   - Keep it concise but descriptive enough to understand the goal at a glance
   - Examples:
     - "Improve user onboarding experience" → "user-onboarding"
     - "Add user authentication system" → "user-authentication" 
     - "Build analytics dashboard for user behavior" → "analytics-dashboard"
     - "Reduce application load time" → "reduce-load-time"

2. Locate the git repository root and run the script `{SCRIPT}` from there **with the goal description argument**, then parse its JSON output for GOAL_DIR, BRANCH_NAME and GOAL_FILE. All file paths must be absolute.

   **IMPORTANT**:
   
   - The goal description argument is passed as the entire user input from $ARGUMENTS
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\\''m Groot' (or double-quote if possible: "I'm Groot")
   - First find the git repository root by looking for `.git` directory or using git command to locate it
   - Change to the repository root directory before executing the script  
   - Ensure the script path is resolved from the repository root (path should not contain duplicate `.goalkit/` prefixes.)
   - Verify the script file exists at the expected path: `{PROJECT_ROOT}/.goalkit/scripts/[platform]/[script-name]` before executing
   - If the file exists at the expected path but the command fails, double-check path resolution
   - You must only ever run this script once
   - The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for

3. Load `.goalkit/templates/goal-template.md` to understand required sections.

4. Follow this execution flow:

    1. Parse user description from Input
       If empty: ERROR "No goal description provided"
    2. Extract key concepts from description
       Identify: goal purpose, target users, success outcomes, constraints
    3. For unclear aspects:
       - Make informed guesses based on context and best practices
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts goal scope or success
         - Multiple reasonable interpretations exist with different implications
         - No reasonable default exists
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: success metrics > target users > constraints
    4. Fill Goal Overview (Goal Statement, Context, Success Level)
       If no clear purpose: ERROR "Cannot determine goal purpose"
    5. Generate Success Metrics
       Each metric must be testable, measurable with specific targets (%,$,timeframes,user counts)
       Use reasonable defaults for unspecified details (document assumptions in Assumptions section)
    6. Define Target Users & Stakeholders
       Identify who will benefit and who has interest in the goal
    7. Identify Goal Hypotheses (Key Assumptions and Risk Factors)
    8. Outline Goal Milestones (Measurable progress steps)
    9. Create Validation Strategy (Measurement approach and learning objectives)
    10. Return: SUCCESS (goal ready for strategy exploration)

5. Write the goal definition to GOAL_FILE using the template structure, replacing placeholders with concrete details derived from the goal description (arguments) while preserving section order and headings.

6. **Goal Quality Validation**: After writing the initial goal, validate it against quality criteria:

   a. **Create Goal Quality Checklist**: Generate a checklist file at `GOALS_DIR/checklists/goal-quality.md` using the checklist template structure with these validation items:
   
      ```markdown
      # Goal Quality Checklist: [GOAL NAME]
      
      **Purpose**: Validate goal completeness and quality before proceeding to strategy exploration
      **Created**: [DATE]
      **Goal**: [Link to goal.md]
      
      ## Content Quality
      
      - [ ] No implementation details (languages, frameworks, APIs)
      - [ ] Focused on user value and business outcomes
      - [ ] Written for non-technical stakeholders
      - [ ] All mandatory sections completed
      
      ## Goal Completeness
      
      - [ ] No [NEEDS CLARIFICATION] markers remain
      - [ ] Success metrics are testable and unambiguous
      - [ ] Success metrics are measurable with specific targets (%,$,timeframes,user counts)
      - [ ] Target users clearly identified
      - [ ] Key assumptions identified and testable
      - [ ] Risk factors identified with mitigation approaches
      - [ ] Goal aligns with project vision in .goalkit/vision.md
      - [ ] Validation strategy is clear and achievable
      
      ## Goal Readiness
      
      - [ ] All success metrics have clear, quantifiable targets
      - [ ] Goal hypotheses can be validated through experiments
      - [ ] Goal meets measurable outcomes defined in Success Metrics
      - [ ] No implementation details leak into goal definition
      
      ## Next Steps Required
      
      - [ ] Use `/goalkit.strategies` to explore multiple approaches to achieve this goal
      - [ ] Use `/goalkit.milestones` to create measurable progress checkpoints
      - [ ] Use `/goalkit.execute` to implement with learning and adaptation
      
      ## Notes
      
      - Items marked incomplete require goal updates before `/goalkit.strategies` or `/goalkit.milestones`
      ```
      
   b. **Run Validation Check**: Review the goal against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant goal sections)
      
   c. **Handle Validation Results**:
      
      - **If all items pass**: Mark checklist complete and proceed to step 6
      
      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific issues
        2. Update the goal to address each issue
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining issues in checklist notes and warn user
      
      - **If [NEEDS CLARIFICATION] markers remain**:
        1. Extract all [NEEDS CLARIFICATION: ...] markers from the goal
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by success metrics/target users/alignment impact) and make informed guesses for the rest
        3. For each clarification needed (max 3), present options to user in this format:
        
           ```markdown
           ## Question [N]: [Topic]
           
           **Context**: [Quote relevant goal section]
           
           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]
           
           **Suggested Answers**:
           
           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested answer] | [What this means for the goal] |
           | B      | [Second suggested answer] | [What this means for the goal] |
           | C      | [Third suggested answer] | [What this means for the goal] |
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
        8. Update the goal by replacing each [NEEDS CLARIFICATION] marker with the user's selected or provided answer
        9. Re-run validation after all clarifications are resolved
   
   d. **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

7. Report completion with branch name, goal file path, checklist results, and **MANDATORY REMINDER** to user about next steps: `/goalkit.strategies`, `/goalkit.milestones`, and `/goalkit.execute`.

**NOTE:** The script creates and checks out the new branch and initializes the goal file before writing.

## Key rules

- All metrics must be quantifiable with specific targets (%, $, timeframes, user counts)
- Each goal must include testable hypotheses with validation methods
- Goal should align with existing project vision in `.goalkit/vision.md`
- Focus on measurable outcomes rather than implementation details
- **CRITICAL**: After goal creation, remind user to use `/goalkit.strategies` to explore approaches, then `/goalkit.milestones` to create checkpoints, then `/goalkit.execute` to implement with learning loops