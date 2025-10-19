---
description: Explore multiple implementation strategies for achieving goals. This command ensures agents are following the complete methodology by building on defined goals and strategies.
scripts:
  # Paths are relative to PROJECT ROOT (not relative to .goalkit/)
  sh: .goalkit/scripts/bash/setup-strategy.sh --json "{ARGS}"
  ps: .goalkit/scripts/powershell/setup-strategy.ps1 -Json "{ARGS}"
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

**BEFORE PROCEEDING:** Verify the user has completed the `/goalkit.goal` step:

- **Check if a goal exists**: Search in `.goalkit/goals/` directory for existing goal files
- **If no goals exist**: Inform user they must create a goal first using `/goalkit.goal`
- **If goals exist**: Proceed with strategy exploration for the appropriate goal

## Task Complexity Assessment

**CRITICAL**: This command is for exploring multiple strategies for complex goals. For simple tasks that don't require multiple approaches, go back and ensure the full methodology is being followed:

- If the user is creating simple enhancements without a goal, suggest they first use `/goalkit.goal` to define the goal with measurable outcomes
- Only proceed with strategy exploration for goals that have been properly defined with success metrics

## CRITICAL Implementation Details Warning

**IMPORTANT:** Strategies must NOT contain implementation details (specific languages, frameworks, APIs). Focus on measurable outcomes and learning potential.

## Active Persona Context

**Current Persona**: [Agent determines current active persona]

Consider your specialized role when exploring strategies:
- **General Agent**: Focus on overall strategy landscape and integration with other aspects
- **Strategy Explorer**: Deep dive into technical approaches, architectural patterns, and solution analysis
- **Milestone Planner**: Consider how strategies align with planned milestones
- **QA Specialist**: Evaluate strategies from quality, testability, and maintainability perspectives
- **Documentation Specialist**: Consider documentation implications of different approaches
- **GitHub Specialist**: Consider repository organization and branching implications (if applicable)

## Outline

The text the user typed after `/goalkit.strategies` in the triggering message **is** the strategy exploration description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that strategy exploration, do this:

1. **Locate Associated Goal**: Search for the goal that strategies will support
   - Use `glob(path="PROJECT_ROOT/.goalkit/goals", pattern="**")` to discover goals
   - Use `list_directory(path="PROJECT_ROOT/.goalkit/goals")` to enumerate goal directories
   - If user specified a goal, locate that specific goal directory
   - If multiple goals exist, ask user to clarify which goal needs strategies
   - If no goals exist, inform user that goals must be created first using `/goalkit.goal`

2. Locate the git repository root and run the script `{SCRIPT}` from there **with the strategy description argument**, then parse its JSON output for GOAL_DIR, BRANCH_NAME and STRATEGY_FILE. All file paths must be absolute.

   **IMPORTANT**:
   
   - The strategy description argument is passed as the entire user input from $ARGUMENTS
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\\''m Groot' (or double-quote if possible: "I'm Groot")
   - Execute the script from the current project directory (no directory change needed)  
   - Ensure the script path is resolved from the current directory (path should not contain duplicate `.goalkit/` prefixes. Scripts are in `.goalkit/scripts/[platform]/[script-name]`)
   - Verify the script file exists at the expected path: `{PROJECT_ROOT}/.goalkit/scripts/[platform]/[script-name]` before executing
   - If the file exists at the expected path but the command fails, double-check path resolution
   - You must only ever run this script once
   - The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for

3. Load `.goalkit/templates/strategies-template.md` to understand required sections.

4. Follow this execution flow:

    1. Parse user description from Input
       If empty: ERROR "No strategy exploration provided"
    2. Extract key concepts from description
       Identify: strategy dimensions, technical approaches, UX approaches, implementation approaches
    3. For unclear aspects:
       - Make informed guesses based on context and best practices
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts strategy success or risk
         - Multiple reasonable but conflicting approaches exist
         - No reasonable default exists
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: technical feasibility > user experience > implementation approach
    4. Fill Strategy Exploration Framework
       If no clear approaches: ERROR "Cannot determine strategy options"
    5. Generate Strategy Comparison Matrix
       Each strategy must be evaluated across feasibility, effort, risk, and learning potential
       Use reasonable defaults for unspecified details (document assumptions in Assumptions section)
    6. Define Recommended Starting Strategy
       Identify which strategy to try first with rationale
    7. Outline Validation Experiments
       Define how to validate key assumptions of each strategy
    8. Return: SUCCESS (strategies ready for milestone planning)

5. Write the strategy analysis to STRATEGY_FILE using the template structure, replacing placeholders with concrete details derived from the strategy exploration (arguments) while preserving section order and headings.

6. **Strategy Quality Validation**: After writing the initial strategy analysis, validate it against quality criteria:

   a. **Create Strategy Quality Checklist**: Generate a checklist file at `GOAL_DIR/checklists/strategy-quality.md` using the checklist template structure with these validation items:
   
      ```markdown
      # Strategy Quality Checklist: [STRATEGY NAME]
      
      **Purpose**: Validate strategy analysis completeness and quality before proceeding to milestone planning
      **Created**: [DATE]
      **Goal**: [Link to associated goal]
      **Strategy**: [Link to strategy.md]
      
      ## Content Quality
      
      - [ ] Explores multiple valid approaches (not just one "correct" solution)
      - [ ] Focused on measurable outcomes and learning potential
      - [ ] Written for non-technical stakeholders
      - [ ] All mandatory sections completed
      
      ## Strategy Completeness
      
      - [ ] No [NEEDS CLARIFICATION] markers remain
      - [ ] Strategies are testable with clear validation criteria
      - [ ] Strategy comparison is comprehensive across relevant dimensions
      - [ ] Recommended starting strategy has clear rationale
      - [ ] Validation experiments are defined for key assumptions
      - [ ] Risk assessments are identified with mitigation approaches
      - [ ] Strategies align with goal success criteria from associated goal
      - [ ] Learning objectives are clearly defined
      
      ## Strategy Readiness
      
      - [ ] All strategies have clear evaluation framework
      - [ ] Strategy success criteria are measurable
      - [ ] Fallback options are defined if primary strategy fails
      - [ ] No implementation details leak into strategy analysis
      
      ## Next Steps Required
      
      - [ ] Use `/goalkit.milestones` to create measurable progress checkpoints
      - [ ] Use `/goalkit.execute` to implement with learning and adaptation
      
      ## Notes
      
      - Items marked incomplete require strategy updates before `/goalkit.milestones` or `/goalkit.execute`
      ```
      
   b. **Run Validation Check**: Review the strategy analysis against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant strategy sections)
      
   c. **Handle Validation Results**:
      
      - **If all items pass**: Mark checklist complete and proceed to step 6
      
      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific issues
        2. Update the strategy analysis to address each issue
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining issues in checklist notes and warn user
      
      - **If [NEEDS CLARIFICATION] markers remain**:
        1. Extract all [NEEDS CLARIFICATION: ...] markers from the strategy analysis
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by feasibility/UX/implementation impact) and make informed guesses for the rest
        3. For each clarification needed (max 3), present options to user in this format:
        
           ```markdown
           ## Question [N]: [Topic]
           
           **Context**: [Quote relevant strategy section]
           
           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]
           
           **Suggested Answers**:
           
           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested answer] | [What this means for the strategy] |
           | B      | [Second suggested answer] | [What this means for the strategy] |
           | C      | [Third suggested answer] | [What this means for the strategy] |
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
        8. Update the strategy analysis by replacing each [NEEDS CLARIFICATION] marker with the user's selected or provided answer
        9. Re-run validation after all clarifications are resolved
   
   d. **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

7. Report completion with branch name, strategy file path, checklist results, and **MANDATORY REMINDER** to user about next steps: `/goalkit.milestones` and `/goalkit.execute`.

**NOTE:** The script creates and checks out the new branch and initializes the strategy file before writing.

## Key rules

- Explore multiple valid approaches (not just one "correct" solution)
- Evaluate strategies against goal success criteria and vision principles
- Frame strategies as testable hypotheses with clear validation criteria
- Focus on measurable outcomes and learning potential
- **CRITICAL**: After strategy creation, remind user to use `/goalkit.milestones` to create checkpoints, then `/goalkit.execute` to implement with learning loops