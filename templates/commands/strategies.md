---
description: Explore multiple implementation strategies for achieving goals.
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

## Task Complexity Assessment

**CRITICAL**: This command is for exploring multiple strategies for complex goals. For simple tasks that don't require multiple approaches, consider if direct implementation would be more efficient:

- If the user wants to implement a simple enhancement (e.g., "enhanced header", "style improvements"), suggest `/goalkit.execute` for direct implementation instead
- Only proceed with strategy exploration for complex goals requiring multiple approaches

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
   - First find the git repository root by looking for `.git` directory or using git command to locate it
   - Change to the repository root directory before executing the script
   - Ensure the script path is resolved from the repository root (path should not contain duplicate `.goalkit/` prefixes. Scripts are in `{PROJECT_ROOT}/.goalkit/scripts/[platform]/[script-name]`)
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

7. Report completion with branch name, strategy file path, checklist results, and readiness for the next phase (`/goalkit.milestones` or `/goalkit.execute`).

**NOTE:** The script creates and checks out the new branch and initializes the strategy file before writing.

## Key rules

- Explore multiple valid approaches (not just one "correct" solution)
- Evaluate strategies against goal success criteria and vision principles
- Frame strategies as testable hypotheses with clear validation criteria
- Focus on measurable outcomes and learning potential

## Overview

The `/goalkit.strategies` command explores multiple implementation approaches for achieving your defined goals. Unlike planning that focuses on a single solution, strategies emphasize exploration and comparison of different approaches.

## Purpose

This command creates a comprehensive strategy exploration document that:
- Identifies multiple valid approaches to achieve each goal
- Compares strategies across technical, UX, and business dimensions
- Evaluates risks and mitigation approaches
- Provides foundation for informed strategy selection

## When to Use

Use `/goalkit.strategies` when:
- You have a well-defined goal with clear success criteria
- You want to explore different approaches before committing
- You need to evaluate trade-offs between different strategies
- You're ready to select an approach for milestone planning

## Input Format

```
/goalkit.strategies [description of different approaches to consider and dimensions to explore]
```

### Example Input

```
/goalkit.strategies For the task management goal, explore these strategies:
1. Technical: Progressive Web App vs Native Mobile vs Desktop Application
2. UX: Kanban-style vs Time-blocking vs AI-powered organization
3. Implementation: Big bang release vs Iterative feature rollout vs MVP-first
Consider trade-offs in development complexity, user adoption barriers, and maintenance overhead.
```

## Output

The command generates:
- `goals/[###-goal-name]/strategies.md` - Comprehensive strategy analysis
- Strategy comparison framework for informed decision-making
- Risk assessment and mitigation plans for each strategy
- Foundation for milestone planning and execution

### Agent File Creation Instructions

When processing `/goalkit.strategies` commands, AI agents should:
1. Locate the appropriate goal directory in the `goals/` folder (the most recently created or specified goal)
2. Create the `strategies.md` file inside that goal directory
3. Use the current date in YYYY-MM-DD format for the "Date" field
4. Write the complete strategy analysis using the template structure below
5. Reference the associated goal in the document header
6. After creating the strategies file, inform the user that the strategy analysis has been completed and suggest next steps using `/goalkit.milestones`

### File Creation Process
- **Locate Directory**: `goals/[###-goal-name]/` (most recent goal or specified goal)
- **Create File**: `goals/[###-goal-name]/strategies.md` with the strategy content
- **Template**: Use the structure provided in the "Strategy Components" section below

## Strategy Components

### 1. Strategy Exploration Framework
- **Technical Strategy Options**: Different technologies and architectures
- **User Experience Strategies**: Various approaches to user interaction
- **Implementation Strategies**: Different development and rollout approaches

### 2. Strategy Comparison Matrix
- **Technical Feasibility**: How practical each strategy is to implement
- **User Experience Quality**: How well each strategy serves users
- **Development Effort**: Resources required for each strategy
- **Risk Level**: Potential issues and their likelihood
- **Learning Potential**: What each strategy can teach

### 3. Recommended Starting Strategy
- **Primary Recommendation**: Which strategy to try first
- **Rationale**: Evidence-based reasoning for the choice
- **Success Criteria**: How to validate if the strategy works
- **Fallback Options**: Alternative strategies if primary fails

### 4. Validation Experiments
- **Critical Assumption Tests**: Experiments to validate strategy assumptions
- **Measurement Plan**: How to evaluate strategy effectiveness
- **Success Thresholds**: When strategy is considered successful

## Key Differences from Spec-Driven Development

| Spec-Driven | Goal-Driven |
|-------------|-------------|
| Single technical implementation plan | Multiple strategy exploration |
| Detailed technical specifications | Strategy comparison and evaluation |
| One "correct" architectural approach | Multiple valid technical strategies |
| Implementation-focused planning | Learning-focused strategy testing |

## Integration with Other Commands

### Before Using `/goalkit.strategies`
- **`/goalkit.vision`**: Provides guiding principles for strategy evaluation
- **`/goalkit.goal`**: Defines the goal and success criteria for strategies

### After Using `/goalkit.strategies`
- **`/goalkit.milestones`**: Create measurable milestones for chosen strategy
- **`/goalkit.execute`**: Implement chosen strategy with adaptation framework

## Best Practices

### Strategy Exploration
- **Multiple Perspectives**: Consider technical, UX, and business viewpoints
- **Trade-off Analysis**: Explicitly evaluate pros and cons
- **Risk Assessment**: Identify potential failure modes upfront
- **Learning Focus**: Frame strategies as learning opportunities

### Strategy Selection
- **Evidence-Based Choice**: Use goal metrics to evaluate strategies
- **Start Simple**: Begin with lowest-risk, highest-learning strategy
- **Fallback Planning**: Always have alternative strategies ready
- **Adaptation Readiness**: Plan how to pivot if strategy fails

### Strategy Documentation
- **Clear Rationale**: Document why each strategy was considered
- **Comparison Criteria**: Make evaluation framework explicit
- **Risk Documentation**: Capture potential issues and mitigations
- **Learning Capture**: Document what was learned from each strategy

## Common Strategy Patterns

### Technical Strategy Patterns
- **Progressive Enhancement**: Start simple, add complexity based on user feedback
- **Platform Prioritization**: Web-first, then native mobile/desktop
- **Integration vs Build**: Use existing tools vs custom development
- **Monolith vs Microservices**: Single system vs distributed architecture

### UX Strategy Patterns
- **Guided vs Free-form**: Structured workflows vs user customization
- **Automation vs Manual**: AI assistance vs user control
- **Social vs Individual**: Community features vs personal focus
- **Simple vs Feature-rich**: Minimal interface vs comprehensive tools

### Implementation Strategy Patterns
- **MVP vs Full Feature**: Start with core functionality vs complete solution
- **Iterative vs Big Bang**: Gradual rollout vs single launch
- **Internal vs External**: Build in-house vs use external services
- **Custom vs Off-the-shelf**: Custom development vs existing solutions

## Strategy Validation

### Validation Experiments
- **Technical Validation**: Prove technical approach feasibility
- **UX Validation**: Test user experience effectiveness
- **Business Validation**: Confirm business model viability
- **Integration Validation**: Ensure strategy works in real environment

### Measurement and Learning
- **Strategy Metrics**: Track strategy-specific success indicators
- **Comparative Analysis**: Evaluate strategies against each other
- **Learning Documentation**: Capture insights for future strategies
- **Pivot Triggers**: Define when to switch strategies

## Examples

### Example 1: E-commerce Strategy Exploration
```
/goalkit.strategies For improving product discovery, explore:
1. Technical: Elasticsearch vs AI recommendations vs Hybrid approach
2. UX: Search-first vs Browse-first vs Guided discovery
3. Implementation: Gradual rollout vs Feature flags vs A/B testing
Focus on conversion impact, user satisfaction, and technical scalability.
```

### Example 2: Developer Tool Strategy Exploration
```
/goalkit.strategies For reducing context switching, consider:
1. Technical: VS Code extension vs Standalone app vs Browser extension
2. UX: Always-visible vs On-demand vs AI-triggered assistance
3. Implementation: Open source vs Commercial vs Freemium model
Evaluate based on developer adoption, productivity impact, and maintenance effort.
```

### Example 3: Mobile App Strategy Exploration
```
/goalkit.strategies For habit building app, explore:
1. Technical: React Native vs Flutter vs Native iOS/Android
2. UX: Gamification vs Social accountability vs Data-driven insights
3. Implementation: Mobile-first vs Web companion vs API-first
Consider user engagement, retention, and cross-platform compatibility.