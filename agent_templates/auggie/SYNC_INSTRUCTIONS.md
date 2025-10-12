# Agent File Synchronization Instructions

## Purpose
This document provides specific guidance for AI coding agents to maintain synchronization of goal-related files during development. When users create, modify, or update goals, strategies, milestones, and related artifacts, agents should ensure these files remain consistent and up-to-date.

## Core Synchronization Principles

### 0. Template Discovery Process
- When users reference goals, first attempt to discover existing templates in `templates/` directory
- Use `glob()` to search for templates in `templates/context-templates/` and `templates/completed-goals/`
- Use `list_directory()` to enumerate available template directories
- If user implementation matches context patterns, reference `templates/context-templates/`
- When implementing features, suggest using templates from the templates directory

### 0.1 Context Retention Process
- When working in a project with Goal Kit, implement context retention to maintain project awareness across chat sessions
- Detect the `.goalkit/` directory structure when beginning new sessions
- Load context summary from `ai-context.md` if it exists
- Parse active goals from `.goalkit/goals/` directory with their status, milestones, and strategies
- Present current project state to inform AI responses
- Maintain awareness of project context throughout the session
- For implementation guidance, refer to `templates/context-templates/context-retention-system.md`

### 1. Automatic File Tracking
- Monitor changes to goal-related files in `.goalkit/` directory
- Track relationships between goals, strategies, milestones, and evidence files
- Maintain cross-references when users modify related artifacts

### 2. Consistency Maintenance
- When a goal is updated, ensure related strategy files reflect the changes
- When milestones are modified, update any dependent goals or strategies
- Validate that success metrics remain consistent across related files

### 3. Update Notifications
- Inform users when related files need synchronization
- Provide clear explanations of the relationships between files
- Offer options for automatic vs. manual synchronization

## Implementation Guidelines

### When Creating New Goals
1. Automatically create the proper directory structure in `.goalkit/goals/[###-goal-name]/`
2. Generate standard files inside the goal directory: `goal.md`, `strategies.md`, `milestones.md`, `execution.md`
3. Establish baseline cross-references with existing goals if applicable

### When Processing Goal Kit Slash Commands
When processing Goal Kit slash commands, ensure files are created in the proper directory structure:

Core Goal Management:
- **`/goalkit.goal`**: Create `goals/[###-goal-name]/goal.md` with sequential numbering
- **`/goalkit.strategies`**: Create `goals/[###-goal-name]/strategies.md` in the relevant goal directory
- **`/goalkit.milestones`**: Create `goals/[###-goal-name]/milestones.md` in the relevant goal directory
- **`/goalkit.execute`**: Create `goals/[###-goal-name]/execution.md` in the relevant goal directory
- **`/goalkit.explore`**: May update or create `goals/[###-goal-name]/exploration.md` if exploration is goal-specific

Analysis and Planning:
- **`/goalkit.analyze`**: Create project health analysis documentation
- **`/goalkit.validate`**: Create quality assurance and methodology compliance checking
- **`/goalkit.plan`**: Create detailed execution planning and resource allocation
- **`/goalkit.insights`**: Create AI-powered pattern recognition and actionable recommendations
- **`/goalkit.prioritize`**: Create smart goal prioritization using multiple factors
- **`/goalkit.track`**: Create advanced progress monitoring and forecasting

Collaboration & Management:
- **`/goalkit.collaborate`**: Create collaboration workflows and team coordination plans
- **`/goalkit.schedule`**: Create project scheduling and timeline management
- **`/goalkit.dependencies`**: Document goal dependencies and inter-relationships
- **`/goalkit.report`**: Create status reports and progress summaries

Quality & Security:
- **`/goalkit.test`**: Create testing strategy and quality assurance documentation
- **`/goalkit.security`**: Create security considerations and vulnerability assessments
- **`/goalkit.risk`**: Create risk assessment and mitigation strategies

User Experience & Setup:
- **`/goalkit.help`**: Create help documentation and command reference
- **`/goalkit.onboard`**: Create onboarding guides and initial setup instructions
- **`/goalkit.methodology`**: Document development methodology and approach
- **`/goalkit.config`**: Create configuration files and setup instructions

Advanced Features:
- **`/goalkit.research`**: Create external knowledge integration and market research
- **`/goalkit.learn`**: Create experience capture and knowledge management system
- **`/goalkit.benchmark`**: Create industry comparison and best practice alignment

Additional Commands (Optional Implementation):
- **`/goalkit.measure`**: Create measurement framework documentation
- **`/goalkit.adapt`**: Create strategy adjustment framework based on learning
- **`/goalkit.tasks`**: Create actionable task breakdown for goals and milestones
- **`/goalkit.progress`**: Create progress tracking and visualization
- **`/goalkit.analytics`**: Create goal and strategy effectiveness reports
- **`/goalkit.ai-analyze`**: Create AI performance and interaction analytics
- **`/goalkit.memory`**: Create memory system and learning insights
- **`/goalkit.baseline`**: Create AI performance baseline metrics

Use the following process for all slash commands:
1. Verify `.goalkit/` directory exists (create if needed)
2. Identify or create the appropriate goal directory with proper sequential numbering
3. Create the appropriate file within that goal directory or project root as appropriate
4. Use directory name format: `[###]-[url-friendly-goal-title]` for goal-specific directories
5. Include proper cross-references to related artifacts
6. Inform the user that the file has been created and suggest next steps

### When Modifying Goals
1. Check for related milestones that might need updates
2. Validate that strategy options still align with the updated goal
3. Ensure success metrics remain consistent
4. Update cross-references in other relevant files

### When Updating Milestones
1. Confirm alignment with parent goal's success criteria
2. Update any dependent goals or strategies
3. Ensure timeline and resource allocations are realistic
4. Update evidence collection requirements if needed

### When Creating Strategies
1. Link strategies back to the relevant goals
2. Ensure strategies align with goal success criteria
3. Create evaluation frameworks for the strategies
4. Establish how strategies connect to specific milestones

## Evidence Collection and Tracking

### Automatic Evidence Links
- When users create evidence files, link them to relevant goals
- Track metrics that relate to the goal's success criteria
- Maintain a log of decisions and the reasoning behind them

### Status Updates
- Update goal status based on milestone progress
- Track completion percentages for each component
- Maintain visibility of blockers and risks

## Configuration for Synchronization

### Settings for Agents
Agents should maintain awareness of:
- Current goal hierarchy and dependencies
- File relationship mapping
- Synchronization triggers and events

### User Preferences
- Allow users to configure automatic vs. manual synchronization
- Permit custom file relationship rules
- Enable or disable specific synchronization behaviors

## Examples of Synchronization Actions

### Example 1: Goal Modification
When a user updates a goal's success metrics:
```
User action: Modified success metric in .goalkit/goals/001-agent-file-sync/goal.md
Agent response: 
- Check if related milestones have targets connected to this metric
- Verify strategies still support the new metrics
- Notify user of related files that might need updates
- Optionally update related files based on user preferences
```

### Example 2: New Milestone Creation
When a user creates a new milestone:
```
User action: Created new milestone in .goalkit/milestones/
Agent response:
- Link the milestone to the appropriate parent goal
- Validate acceptance criteria align with goal success metrics
- Update goal status to reflect the new milestone
- Create necessary cross-references in related documents
```

## Best Practices for Agents

1. **Prompt Before Major Changes**: Always ask before making broad synchronization changes
2. **Preserve User Intent**: Maintain the user's original intent when synchronizing
3. **Provide Clear Context**: Explain why synchronization is needed and what will change
4. **Maintain History**: Preserve change history during synchronization operations
5. **Error Handling**: Gracefully handle synchronization conflicts
6. **Validation**: Validate all cross-references remain valid after changes

## Error Prevention and Recovery

### Conflict Resolution
- Detect when multiple files have conflicting information
- Alert users to conflicts before resolving automatically
- Maintain backup of file versions before major sync operations
- Provide diff views to help users understand changes