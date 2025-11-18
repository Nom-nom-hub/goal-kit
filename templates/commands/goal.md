---
description: Create or update the goal definition from a natural language goal description.
handoffs:
  - label: Explore Strategy Options
    agent: goalkit.strategies
    prompt: Explore strategies for the goal. I am building with...
  - label: Clarify Goal Requirements
    agent: goalkit.clarify
    prompt: Clarify goal requirements
    send: true
scripts:
  sh: scripts/bash/create-new-goal.sh --json "{ARGS}"
  ps: scripts/powershell/create-new-goal.ps1 -Json "{ARGS}"
---

## User Input

The user's goal description is: **$ARGUMENTS**

You **MUST** consider this user input before proceeding. The text above is the ACTUAL goal description the user provided - do NOT ask them to repeat it.

## Outline

The text the user typed after `/goalkit.goal` command **IS** the goal description. Use it directly without asking for clarification unless it's truly empty (zero characters).

Given that goal description, do this:

1. **Generate a concise short name** (2-4 words) for the branch:
   - Analyze the goal description and extract the most meaningful keywords
   - Create a 2-4 word short name that captures the essence of the goal
   - Use action-noun format when possible (e.g., "increase-user-engagement", "reduce-customer-churn")
   - Preserve technical terms and acronyms (SaaS, API, ROI, etc.)
   - Keep it concise but descriptive enough to understand the goal at a glance
   - Examples:
     - "I want to increase user engagement" → "user-engagement"
     - "Improve customer retention by 20%" → "customer-retention"
     - "Reduce support ticket volume" → "reduce-support-tickets"

2. **Check for existing branches before creating new one**:

   a. First, fetch all remote branches to ensure we have the latest information:
      ```bash
      git fetch --all --prune
      ```

   b. Find the highest goal number across all sources for the short-name:
      - Remote branches: `git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'`
      - Local branches: `git branch | grep -E '^[* ]*[0-9]+-<short-name>$'`
      - Goals directories: Check for directories matching `.goalkit/goals/[0-9]+-<short-name>`

   c. Determine the next available number:
      - Extract all numbers from all three sources
      - Find the highest number N
      - Use N+1 for the new branch number

   d. Run the script `{SCRIPT}` with the calculated number and short-name:
      - Pass `--number N+1` and `--short-name "your-short-name"` along with the goal description
      - Bash example: `{SCRIPT} --json --number 5 --short-name "user-engagement" "Increase user engagement"`
      - PowerShell example: `{SCRIPT} -Json -Number 5 -ShortName "user-engagement" "Increase user engagement"`

   **IMPORTANT**:
   - Check all three sources (remote branches, local branches, goals directories) to find the highest number
   - Only match branches/directories with the exact short-name pattern
   - If no existing branches/directories found with this short-name, start with number 1
   - You must only ever run this script once per goal
   - The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for
   - The JSON output will contain BRANCH_NAME and GOAL_FILE paths
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot")

3. Load `templates/goal-template.md` to understand required sections.

4. Follow this execution flow:

    1. **Parse user description from Input section above**
        - The goal description is explicitly stated after "The user's goal description is:"
        - If it's empty or contains no actual text: ERROR "No goal description provided"
        - Otherwise: PROCEED - you have the goal description
     2. Extract key concepts from the user's description
       Identify: beneficiaries, desired outcomes, success measures
    3. For unclear aspects:
       - Make informed guesses based on context and industry standards
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts goal scope or value
         - Multiple reasonable interpretations exist with different implications
         - No reasonable default exists
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: scope > business value > user experience > technical details
    4. Fill Goal Definition section
       If no clear outcomes: ERROR "Cannot determine measurable outcomes"
    5. Generate Success Metrics
       Each metric must be testable
       Use reasonable defaults for unspecified details (document assumptions in Assumptions section)
    6. Define Validation Strategy
       Create measurable, technology-agnostic outcomes
       Include both quantitative metrics (time, performance, volume) and qualitative measures (user satisfaction, business impact)
       Each criterion must be verifiable without implementation details
    7. Identify Critical Path Activities and Risks (if relevant)
    8. Return: SUCCESS (goal ready for strategy exploration)

5. Write the goal to GOAL_FILE using the template structure, replacing placeholders with concrete details derived from the goal description (arguments) while preserving section order and headings.

6. **Goal Quality Validation**: After writing the initial goal, validate it against quality criteria:

   a. **Create Goal Quality Checklist**: Generate a checklist file at `GOAL_DIR/checklists/requirements.md` using the checklist template structure with these validation items:

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
      - [ ] Goals are measurable and unambiguous
      - [ ] Success metrics are quantifiable
      - [ ] Success metrics are outcome-focused (no implementation details)
      - [ ] All validation scenarios are defined
      - [ ] Risks are identified
      - [ ] Scope is clearly bounded
      - [ ] Dependencies and assumptions identified

      ## Goal Readiness

      - [ ] All success metrics have clear validation criteria
      - [ ] Outcomes cover primary business/user value
      - [ ] Goal meets measurable outcomes defined in Success Metrics
      - [ ] No implementation details leak into goal specification

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
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by scope/business value impact) and make informed guesses for the rest
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

7. Report completion with branch name, goal file path, checklist results, and readiness for the next phase (`/goalkit.strategies`).

**NOTE:** The script creates and checks out the new branch and initializes the goal file before writing.

## General Guidelines

## Quick Guidelines

- Focus on **WHAT** outcomes users/businesses need and **WHY**.
- Avoid HOW to implement (no tech stack, APIs, code structure).
- Written for business stakeholders, not developers.
- DO NOT create any checklists that are embedded in the goal. That will be a separate command.

### Section Requirements

- **Mandatory sections**: Must be completed for every goal
- **Optional sections**: Include only when relevant to the goal
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation

When creating this goal from a user prompt:

1. **Make informed guesses**: Use context, industry standards, and common patterns to fill gaps
2. **Document assumptions**: Record reasonable defaults in the Assumptions section
3. **Limit clarifications**: Maximum 3 [NEEDS CLARIFICATION] markers - use only for critical decisions that:
   - Significantly impact goal scope or business value
   - Have multiple reasonable interpretations with different implications
   - Lack any reasonable default
4. **Prioritize clarifications**: scope > business value > user experience > technical details
5. **Think like a validator**: Every vague goal should fail the "measurable and unambiguous" checklist item
6. **Common areas needing clarification** (only if no reasonable default exists):
   - Goal scope and boundaries (include/exclude specific outcomes)
   - Beneficiary groups (if multiple conflicting interpretations possible)
   - Success metrics (when critical for measuring progress)

**Examples of reasonable defaults** (don't ask about these):

- Success metrics: Industry-standard practices for the domain
- Timeline expectations: Standard project delivery times for similar scope
- Performance targets: User-friendly goals that align with business value
- Target beneficiary groups: Primary persona that benefits most from the goal

### Success Metrics Guidelines

Success metrics must be:

1. **Measurable**: Include specific metrics (%, $, time, user counts)
2. **Outcome-focused**: No mention of implementation details or technical approaches
3. **Business/user-focused**: Describe results from user/business perspective, not system internals
4. **Verifiable**: Can be validated without knowing implementation details

**Good examples**:

- "User engagement increases by 25% over 3 months"
- "Customer retention improves by 15% year-over-year"
- "Task completion rate reaches 90% for primary workflow"
- "Revenue from feature increases by $50K in 6 months"

**Bad examples** (implementation-focused):

- "API response time is under 200ms" (too technical, use "Users see results instantly")
- "Database can handle 1000 TPS" (implementation detail, use outcome-focused metric)
- "React components render efficiently" (framework-specific)
- "Redis cache hit rate above 80%" (technology-specific)
