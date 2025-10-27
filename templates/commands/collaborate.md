---
description: Coordinate work between agents or maintain consistency for single agent execution using collaboration workflows that track dependencies, communication, and progress across development activities. Includes persona management for specialized agent roles.
scripts:
  # Paths are relative to PROJECT ROOT (not relative to .goalkit/)
  sh: .goalkit/scripts/python/setup_collaboration.py --json "{ARGS}"
  ps: .goalkit/scripts/python/setup_collaboration.py --json "{ARGS}"
agent_scripts:
  # Paths are relative to PROJECT ROOT (not relative to .goalkit/)
  sh: .goalkit/scripts/python/update-agent-context.sh
  ps: .goalkit/scripts/python/update-agent-context.py
---

# User Input

```text
$ARGUMENTS
```

You:MUST** consider the user input before proceeding (if not empty).

## Task Complexity Assessment

**CRITICAL**: Before proceeding, assess if this is truly a substantial collaboration requiring the full methodology or a simple coordination task that should be handled directly:

- **Simple coordination tasks** (skip full process): minor communication adjustments, simple status updates, straightforward task assignments (e.g., "update status", "check in with team", "send notification")
- **Complex collaborations** (use full process): multi-agent coordination with measurable outcomes, dependency tracking, cross-team synchronization with validation requirements

## Coordination Mode Assessment

Before proceeding, determine the appropriate coordination mode:

- **Single-Agent Mode**: When only one agent is available or coordinating with itself across time
- **Multi-Agent Mode**: When multiple agents are present and need to coordinate work
- **Self-Coordination Mode**: When a single agent needs to maintain consistency across different interactions

## Active Persona Context

**Current Persona**: [Agent determines current active persona]

Consider your specialized role when setting up collaboration:

- **General Agent**: Focus on overall coordination structure and integration
- **Strategy Explorer**: Emphasize multiple approach considerations for coordination
- **Milestone Planner**: Focus on measurable coordination outcomes and tracking
- **QA Specialist**: Consider quality validation and consistency requirements
- **Documentation Specialist**: Plan for necessary coordination documentation
- **GitHub Specialist**: Focus on repository and version control aspects of coordination

## Persona Transition Planning

Identify where persona changes would be beneficial during this collaboration:

**When to switch to GitHub Specialist**: [Repository management and version control coordination]
**When to switch to Milestone Planner**: [Milestone and progress tracking coordination]
**When to switch to Strategy Explorer**: [Approach evaluation and decision coordination]
**When to switch to QA Specialist**: [Quality validation and consistency checking]
**When to switch to Documentation Specialist**: [Documentation and knowledge management]

## Outline

The text the user typed after `/goalkit.collaborate` in the triggering message **is** the collaboration description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that collaboration description, do this:

1. **Generate a concise short name** (2-4 words) for the collaboration:
   - Analyze the collaboration description and extract the most meaningful keywords
   - Create a 2-4 word short name that captures the essence of the collaboration
   - Use action-noun format when possible (e.g., "coordinate-work", "align-goals", "sync-progress")
   - Preserve technical terms and acronyms as appropriate
   - Keep it concise but descriptive enough to understand the collaboration at a glance

2. Locate the git repository root and run the script `{SCRIPT}` from there **with the collaboration description argument**, then parse its JSON output for COLLAB_DIR, BRANCH_NAME and COLLAB_FILE. All file paths must be absolute.

   **IMPORTANT**:

   - The collaboration description argument is passed as the entire user input from $ARGUMENTS
   - Execute the script from the current project directory (no directory change needed)  
   - Ensure the script path is resolved from the current directory (path should not contain duplicate `.goalkit/` prefixes.)
   - Verify the script file exists at the expected path: `{PROJECT_ROOT}/.goalkit/scripts/[platform]/[script-name]` before executing
   - If the file exists at the expected path but the command fails, double-check path resolution
   - You must only ever run this script once
   - The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for

3. Load `.goalkit/templates/collaboration-template.md` to understand required sections.

4. Follow this execution flow:

    1. Parse user description from Input
       If empty: ERROR "No collaboration description provided"
    2. Extract key concepts from description
       Identify: coordination purpose, participants (if any), desired outcomes, constraints
    3. For unclear aspects:
       - Make informed guesses based on context and best practices
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts coordination scope or success
         - Multiple reasonable interpretations exist with different implications
         - No reasonable default exists
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: coordination outcomes > participants > constraints
    4. Determine coordination mode (Single-Agent, Multi-Agent, or Self-Coordination)
    5. Identify coordination participants (agents, systems, or processes involved)
    6. Define coordination objectives and success metrics
    7. Map existing dependencies or relationships that need coordination
    8. Outline coordination activities and timeline
    9. Create communication and synchronization plan
    10. Return: SUCCESS (coordination plan ready for execution)

5. Write the collaboration definition to COLLAB_FILE using the template structure, replacing placeholders with concrete details derived from the collaboration description (arguments) while preserving section order and headings.

6. **Coordination Quality Validation**: After writing the initial collaboration, validate it against quality criteria:

   a. **Create Coordination Quality Checklist**: Generate a checklist file at `COLLABORATIONS_DIR/checklists/collaboration-quality.md` using the checklist template structure with these validation items:
   - **High Compliance (7.0+)**: Proceed to next methodology step
   - **Medium Compliance (5.0-6.9)**: Address violations, then re-validate
   - **Low Compliance (< 5.0)**: Major revision required before proceeding

      ```markdown
      # Coordination Quality Checklist: [COLLABORATION NAME]
      
      **Purpose**: Validate coordination completeness and quality before proceeding with collaborative work
      **Created**: [DATE]
      **Collaboration**: [Link to collaboration.md]
      
      ## Content Quality
      
      - [ ] Appropriate coordination mode selected (single-agent, multi-agent, or self-coordination)
      - [ ] Clear identification of coordination participants (if applicable)
      - [ ] Focused on coordination outcomes rather than implementation details
      - [ ] Written for all participants to understand
      
      ## Coordination Completeness
      
      - [ ] No [NEEDS CLARIFICATION] markers remain
      - [ ] Coordination objectives are testable and unambiguous
      - [ ] Success metrics are measurable with specific targets
      - [ ] All mandatory sections completed
      - [ ] Dependencies and relationships properly identified
      
      ## Coordination Readiness
      
      - [ ] All coordination activities have clear owners (or self if single-agent)
      - [ ] Communication channels defined for coordination
      - [ ] Synchronization points identified
      - [ ] Conflict resolution approach documented
      
      ## Notes
      
      - Items marked incomplete require coordination updates before execution
      ```

   b. **Run Validation Check**: Review the collaboration against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant collaboration sections)

   c. **Handle Validation Results**:

      - **If all items pass**: Mark checklist complete and proceed to step 7

      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific issues
        2. Update the collaboration to address each issue
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining issues in checklist notes and warn user

      - **If [NEEDS CLARIFICATION] markers remain**:
        1. Extract all [NEEDS CLARIFICATION: ...] markers from the collaboration
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by coordination outcomes/participants/dependencies impact) and make informed guesses for the rest
        3. For each clarification needed (max 3), present options to user in this format:

           ```markdown
           ## Question [N]: [Topic]
           
           **Context**: [Quote relevant collaboration section]
           
           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]
           
           **Suggested Answers**:
           
           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested answer] | [What this means for coordination] |
           | B      | [Second suggested answer] | [What this means for coordination] |
           | C      | [Third suggested answer] | [What this means for coordination] |
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
        8. Update the collaboration by replacing each [NEEDS CLARIFICATION] marker with the user's selected or provided answer
        9. Re-run validation after all clarifications are resolved
       - **High Compliance (7.0+)**: Proceed to next methodology step
       - **Medium Compliance (5.0-6.9)**: Address violations, then re-validate
       - **Low Compliance (< 5.0)**: Major revision required before proceeding
       - **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

7. Report completion with branch name, collaboration file path, checklist results, and readiness for coordination activities.

## Agent Detection and Coordination Setup

The collaboration system supports three coordination modes:

### Single-Agent Mode (Default)

- Agent coordinates with itself across time
- Maintains consistency in state and decisions
- Tracks progress and changes over time
- Uses coordination artifacts to maintain context

### Multi-Agent Mode (When Multiple Agents Present)

- Agents can be aware of each other's work
- Coordination artifacts shared between agents
- Conflict detection and resolution mechanisms
- Communication protocols between agents

### Self-Coordination Mode

- Agent maintains consistency with its own previous work
- Self-validation and verification processes
- State management and dependency tracking

## Key Rules

- Default to Single-Agent mode when multiple agents aren't detected
- Coordination artifacts use consistent naming and structure
- All coordination activities must be trackable and auditable
- Maintain backward compatibility with existing goal processes
- Coordination should enhance rather than replace existing functionality

## Overview

The `/goalkit.collaborate` command establishes coordination frameworks for multi-agent or self-coordination scenarios that track dependencies, communication, and progress across development activities. Unlike simple task assignment, collaboration focuses on structured coordination with clear validation and communication protocols.

## Purpose

This command creates a coordination plan that:

- Establishes clear coordination modes (Single-Agent, Multi-Agent, or Self-Coordination)
- Defines participants, objectives, and success metrics for coordination
- Creates communication and synchronization protocols
- Provides foundation for coordinated development activities
- Integrates persona management for specialized coordination roles

## When to Use

Use `/goalkit.collaborate` when:

- Coordinating work between multiple agents or systems
- Establishing self-coordination protocols for single-agent workflows
- Managing dependencies and communication across development activities
- Creating structured workflows for complex collaborative tasks

## Input Format

```text
/goalkit.collaborate [description of coordination requirements and participants]
```

### Example Input

```text
/goalkit.collaborate Coordinate work between GitHub specialist and milestone planner to implement version control strategy and track progress. Establish communication protocols for code review coordination and milestone validation.
```

## Output

The command generates:

- `.goalkit/collaborations/[###-collaboration-name]/collaboration.md` - Comprehensive coordination plan
- Coordination artifacts for tracking dependencies and progress
- Communication and synchronization protocols
- Foundation for coordinated execution across agents or time

### Agent File Creation Instructions

When processing `/goalkit.collaborate` commands, AI agents should:

1. Use the script to create the collaboration directory structure
2. Create the `collaboration.md` file inside that collaboration directory
3. Use the current date in YYYY-MM-DD format for the "Date" field
4. Write the complete collaboration plan using the template structure below
5. After creating the collaboration file, inform the user that the coordination framework has been established and suggest proceeding with coordinated activities

### File Creation Process

- **Locate Directory**: `.goalkit/collaborations/[###-collaboration-name]/` (created by script)
- **Create File**: `collaboration.md` with the collaboration content
- **Template**: Use the structure preserved from the collaboration template

## Collaboration Components

### 1. Coordination Framework

- **Coordination Mode**: Single-Agent, Multi-Agent, or Self-Coordination
- **Participants**: Agents, systems, or processes involved in coordination
- **Objectives**: Clear coordination goals and success metrics
- **Dependencies**: Relationships and dependencies that need coordination

### 2. Communication Protocol

- **Communication Channels**: How coordination participants will communicate
- **Synchronization Points**: When coordination check-ins occur
- **Status Reporting**: How progress and issues are communicated
- **Conflict Resolution**: How disagreements or conflicts are addressed

### 3. Tracking and Validation

- **Progress Indicators**: How to measure coordination effectiveness
- **Quality Metrics**: Standards for coordination success
- **Adaptation Triggers**: When to adjust coordination approach
- **Documentation Requirements**: What to record for audit trail

### 4. Persona Integration

- **Role Identification**: Which personas are involved in coordination
- **Transition Planning**: When to switch personas during coordination
- **Role Handoffs**: How responsibilities move between personas
- **Consistency Maintenance**: How to maintain context during persona changes

## Key Differences from Spec-Driven Development

| Spec-Driven | Goal-Driven |
|-------------|-------------|
| Individual task assignment | Structured coordination frameworks |
| Linear task execution | Adaptive coordination protocols |
| Implementation-focused | Communication and dependency-focused |
| Individual accountability | Coordinated responsibility |

## Integration with Other Commands

### Before Using `/goalkit.collaborate`

- **`/goalkit.vision`**: Provides coordination principles aligned with project vision
- **`/goalkit.goal`**: Defines what coordination should advance
- **`/goalkit.persona`**: Establishes specialized roles for coordination

### After Using `/goalkit.collaborate`

- **`/goalkit.execute`**: Execute coordinated activities using established protocols
- **`/goalkit.milestones`**: Track coordinated progress through milestones

## Best Practices

### Coordination Design

- **Clear Ownership**: Each coordination activity has clear owner or fallback
- **Communication Protocols**: Establish channels before coordination begins
- **Progress Tracking**: Define how to measure coordination effectiveness
- **Adaptation Plans**: Know how to adjust coordination approach

### Cross-Role Coordination

- **Role Clarity**: Each participant understands their coordination responsibilities
- **Handoff Protocols**: Clear process for transferring work between roles
- **Context Preservation**: Maintain information continuity across coordination
- **Communication Consistency**: Use consistent formats and channels

### Quality Assurance

- **Regular Check-ins**: Scheduled coordination effectiveness reviews
- **Issue Escalation**: Clear process for addressing coordination problems
- **Success Measurement**: Track coordination outcomes versus objectives
- **Continuous Improvement**: Regularly refine coordination protocols

## Common Coordination Patterns

### Single-Agent Self-Coordination

- **Time-Based Coordination**: Coordination across different interaction sessions
- **State Management**: Maintaining context and progress consistency
- **Progress Tracking**: Measuring advancement without external input
- **Self-Validation**: Internal checks for coordination effectiveness

### Multi-Agent Coordination

- **Role-Based Coordination**: Different agents with specialized functions
- **Dependency Management**: Coordinating interdependent tasks and activities
- **Communication Protocols**: Formal channels for agent interaction
- **Conflict Resolution**: Framework for addressing agent disagreements

### Cross-Persona Coordination

- **Persona Handoffs**: Transfer work between different specialized roles
- **Context Preservation**: Maintaining information across persona changes
- **Consistency Checking**: Ensure alignment across different persona perspectives
- **Knowledge Transfer**: Share insights between different specialized approaches

## Coordination Validation

### Coordination Effectiveness Review

- **Objective Achievement**: Assess if coordination goals were met
- **Communication Quality**: Evaluate effectiveness of communication protocols
- **Dependency Management**: Review how well dependencies were coordinated
- **Participant Satisfaction**: Gather feedback on coordination experience

### Adaptation Framework

- **Continue**: When coordination approach proves effective
- **Adjust**: When minor changes would improve coordination
- **Restructure**: When major coordination approach changes needed
- **Discontinue**: When coordination no longer needed or too costly

## Examples

### Example 1: Multi-Agent Feature Development

```text
/goalkit.collaborate Coordinate between strategy explorer and milestone planner to develop new authentication system:
- Strategy explorer evaluates technical approaches
- Milestone planner creates progress tracking framework
- Communication protocols for approach validation and milestone alignment
- Coordination artifacts to track decision rationales and progress indicators
```

### Example 2: Persona-Based Coordination

```text
/goalkit.collaborate Establish coordination between GitHub specialist and QA specialist for code quality:
- GitHub specialist manages repository and branching branch
- QA specialist ensures testing and validation coordination
- Regular sync points for code review and testing alignment
- Handoff protocols for code promotion and quality gates
```

### Example 3: Self-Coordination Framework

```text
/goalkit.collaborate Create self-coordination for solo development workflow:
- Time-based checkpoints for progress validation
- State management for context preservation across sessions
- Progress tracking for goal advancement measurement
- Quality controls for consistency without external input
```
