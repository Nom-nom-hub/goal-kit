# [PROJECT NAME] Goal-Driven Development Guidelines

Auto-generated from all goals. Last updated: [DATE]

## Active Goal(s)
[EXTRACTED FROM ALL GOAL.MD FILES]

## Project Structure
```
[ACTUAL STRUCTURE FROM GOALS]
```

## Core Methodology Commands
- **`/goalkit.vision`** - Establish project vision and principles
- **`/goalkit.goal`** - Define goals and success criteria  
- **`/goalkit.strategies`** - Explore implementation strategies
- **`/goalkit.milestones`** - Create measurable milestones
- **`/goalkit.execute`** - Execute with learning and adaptation

## Methodology Adherence Guidelines

### Must Follow the 5-Step Process
**ALWAYS follow this sequence for complex goals:**
1. `/goalkit.vision` - Establish vision and principles
2. `/goalkit.goal` - Define measurable goals with outcomes
3. `/goalkit.strategies` - Explore multiple approaches
4. `/goalkit.milestones` - Create measurable progress checkpoints
5. `/goalkit.execute` - Execute with learning and adaptation

### When to Use Each Command

#### Skip Full Process (Simple Tasks)
For simple tasks that don't require measurable outcomes, you may implement directly:
- Visual enhancements (e.g., "enhanced header", "better styling")
- Minor fixes (e.g., "fix button color", "add margin")
- Small improvements without measurable success criteria

#### Use Full Process (Complex Goals)
For complex goals with measurable success criteria, **ALWAYS** follow the complete 5-step methodology:
- New features with measurable outcomes (%,$,timeframes,user counts)
- System changes with defined success metrics
- User workflows requiring success measurements
- Any goal that impacts multiple parts of the system

### Critical Adherence Rules

#### For `/goalkit.goal`:
- All goals must have quantifiable success metrics with specific targets (%,$,timeframes,user counts)
- No implementation details (languages, frameworks, APIs) allowed in goal definitions
- Focus on measurable user/business outcomes instead

#### For `/goalkit.strategies`:
- Explore multiple valid approaches (not just one "correct" solution)
- Each strategy must be testable with clear validation criteria
- Compare strategies across relevant dimensions (feasibility, effort, risk, learning potential)

#### For `/goalkit.milestones`:
- Create measurable progress checkpoints with specific success indicators
- Each milestone should validate learning and progress toward the goal
- Include clear value delivered at each milestone

#### For `/goalkit.execute`:
- Focus on learning and adaptation rather than rigid plan execution
- Implement with continuous measurement and validation
- Document insights and knowledge gained throughout execution

### Next Step Reminders
After completing each command, **ALWAYS** remind the user of the next required step:

- After `/goalkit.goal`: "Now use `/goalkit.strategies` to explore multiple approaches"
- After `/goalkit.strategies`: "Now use `/goalkit.milestones` to create measurable checkpoints"
- After `/goalkit.milestones`: "Now use `/goalkit.execute` to implement with learning loops"

## Strategy Principles
[EXTRACTED FROM STRATEGIES.MD]

## Milestone Tracking
[EXTRACTED FROM MILESTONES.MD]

## Execution Focus
[EXTRACTED FROM EXECUTION.MD]

## Recent Progress
[LAST 3 COMPLETED MILESTONES AND OUTCOMES]

## Agent Development Guidelines
When working with bash scripts and code in this project, AI agents should follow these critical guidelines to avoid common mistakes:

### 1. Verify Before Modifying
- Always check current repository state: `git status`, `git diff`
- Test syntax before making changes: `bash -n script_name.sh`
- Understand file structure before modifying complex elements like heredocs or multi-line strings

### 2. Safe Editing Practices
- Use targeted `edit` operations when possible instead of overwriting entire files
- For complex files with heredocs (`<< EOF`), be especially careful with structure and command substitution
- Always verify conditional blocks remain properly balanced (`if/fi`, `for/done`, etc.)

### 3. Thorough Validation After Changes
- Immediately validate syntax after each change: `bash -n script_name.sh`
- Test functionality before moving on to next tasks
- Verify all related files (bash and PowerShell equivalents) have consistent changes

### 4. Systematic Conflict Resolution
- Resolve merge conflicts one at a time, not all at once
- Verify each conflict resolution before proceeding
- Look for special characters or encoding issues introduced during merges

### 5. Cross-Platform Consistency
- When fixing an issue in one language/script type, check for similar patterns in others (bash vs PowerShell)
- Maintain consistent validation logic across implementations

### 6. Verification Checklist for Bash Scripts
- [ ] `bash -n script_name.sh` returns no errors
- [ ] All variables are properly defined before use
- [ ] All conditional blocks are properly closed
- [ ] Heredoc structures are intact
- [ ] No special characters from merge conflicts remain

### 7. Critical Warning Signs
If you see syntax errors like "unexpected token" or "unexpected EOF", check for:
- Unbalanced parentheses in command substitutions
- Special characters from merge conflicts
- Broken heredoc structures
- Missing closing brackets or quotes

Following these guidelines will help prevent the syntax errors, merge conflict issues, and validation problems that can occur during development.

<!-- MANUAL ADDITIONS START -->
<!-- Add any manual context, constraints, or guidelines here -->
<!-- MANUAL ADDITIONS END -->