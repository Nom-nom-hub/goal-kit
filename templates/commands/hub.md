---
description: Manage collaboration hub for multi-agent coordination and project synchronization
scripts:
  sh: .goalkit/scripts/python/collaboration_hub.py --format text
  ps: .goalkit/scripts/python/collaboration_hub.py --format text
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

## Collaboration Hub Command

**Purpose**: Coordinate multi-agent collaboration, synchronize project state across agents, and manage distributed development activities

**When to Use**:
- When coordinating work between multiple agents or AI systems
- To synchronize project state and progress across different agent sessions
- When managing dependencies between different development activities
- To establish communication protocols for multi-agent workflows

## Quick Prerequisites Check

**BEFORE INITIALIZING COLLABORATION HUB**:
1. **Goal Kit project exists**: Verify `.goalkit/` directory structure
2. **Multiple agents involved**: Have actual need for multi-agent coordination
3. **Shared project state**: Have components requiring synchronization
4. **Coordination requirements**: Have dependencies or shared activities to manage

**If missing**: Single-agent workflow may be sufficient without hub coordination.

## Quick Hub Setup Steps

**STEP 1**: Analyze current project state and active components

**STEP 2**: Identify collaboration requirements and dependencies

**STEP 3**: Establish synchronization protocols for shared components

**STEP 4**: Set up communication channels for agent coordination

**STEP 5**: Configure coordination protocols for distributed work

**STEP 6**: Monitor and manage ongoing collaboration activities

## Collaboration Hub Features

**Coordination Capabilities**:
- **Multi-Agent Synchronization**: Keep project state consistent across agents
- **Dependency Management**: Track and manage dependencies between activities
- **Conflict Resolution**: Handle conflicting changes or decisions
- **Communication Protocols**: Establish agent-to-agent communication

**Hub Management**:
- **Activity Tracking**: Monitor active development activities
- **State Consistency**: Ensure project state coherence across sessions
- **Progress Coordination**: Synchronize progress across different agents
- **Resource Management**: Coordinate shared resources and artifacts

## Input Format

```
/goalkit.hub [options]
```

### Command Options

```
/goalkit.hub                      # Initialize or connect to collaboration hub
/goalkit.hub --status             # Check current hub status and connections
/goalkit.hub --sync               # Synchronize project state across agents
/goalkit.hub --report             # Generate collaboration activity report
/goalkit.hub --json               # Output in JSON format for integration
```

## Agent Script Execution Guide

**CRITICAL**: When processing `/goalkit.hub` commands, agents MUST:

### **STEP 1**: Run the collaboration hub script
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/collaboration_hub.py --format text
```

### **STEP 2**: If status check requested
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/collaboration_hub.py --status --format text
```

### **STEP 3**: Parse hub results
- **Extract connection status** and active agents
- **Identify synchronization needs** and coordination requirements
- **Note coordination conflicts** that need resolution
- **Document collaboration opportunities** for better coordination

### **STEP 4**: Assess collaboration readiness
- **Agent Availability**: Which agents are available for coordination
- **State Consistency**: Current level of synchronization across agents
- **Dependency Status**: Active dependencies requiring coordination
- **Conflict Monitoring**: Issues that require resolution

### **STEP 5**: Update agent context with collaboration state
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/update_agent_context.py
```

## Output

The command generates:
- **Hub Status**: Current connection and coordination state
- **Active Agents**: List of connected agents and their roles
- **Synchronization Report**: Current state of project synchronization
- **Coordination Needs**: Activities requiring coordination or conflict resolution
- **Activity Log**: Recent collaboration activities and changes

### Hub Management Process

**Collaboration Coordination**:
1. **Agent Discovery**: Identify available agents and their capabilities
2. **State Synchronization**: Align project state across connected agents
3. **Activity Coordination**: Coordinate ongoing development activities
4. **Dependency Management**: Track and manage inter-agent dependencies
5. **Conflict Resolution**: Address inconsistencies or conflicts

## Hub Components

### 1. Agent Coordination
- **Agent Discovery**: Identify and register connected agents
- **Role Management**: Track specialized roles and capabilities
- **Activity Tracking**: Monitor what agents are working on
- **Status Reporting**: Maintain current status across agents

### 2. State Synchronization
- **Project State**: Keep project information consistent across agents
- **Progress Tracking**: Synchronize progress and milestone status
- **Artifact Management**: Coordinate shared project artifacts
- **Change Tracking**: Monitor changes across different agent sessions

### 3. Dependency Management
- **Activity Dependencies**: Track dependencies between development tasks
- **Resource Coordination**: Manage shared resources and components
- **Conflict Detection**: Identify potential conflicts between agents
- **Resolution Protocols**: Handle conflicting changes or decisions

### 4. Communication Protocols
- **Information Sharing**: Establish agent-to-agent information exchange
- **Status Updates**: Maintain awareness across connected agents
- **Coordination Signals**: Protocol for requesting coordination
- **Activity Notifications**: Alert agents to relevant state changes

## Coordination Standards

### Collaboration Quality
- **Consistency**: Project state remains coherent across agents
- **Synchronization**: Agents work with current, consistent information
- **Conflict Prevention**: Proactive management of potential conflicts
- **Communication**: Clear protocols for agent interaction

### Hub Management
- **Agent Registration**: Proper registration and role assignment
- **State Management**: Reliable synchronization mechanisms
- **Activity Monitoring**: Clear visibility into ongoing work
- **Conflict Resolution**: Effective handling of inconsistencies

## Integration with Other Commands

### Hub in Multi-Agent Workflow
- **Before multi-agent work**: Establish coordination hub connection
- **During distributed work**: Maintain synchronization and communication
- **After coordination**: Update project state and document collaboration
- **For status monitoring**: Check coordination effectiveness

### Coordination-Enabled Workflow
```
/goalkit.hub → Establish coordination hub connection
[Multiple agents now coordinated] → /goalkit.goal
[Hub maintains state consistency] → /goalkit.strategies
[Agents coordinate approach selection] → /goalkit.milestones
```

## Best Practices

### Hub Management
- **Clear Protocols**: Establish clear communication and coordination protocols
- **State Consistency**: Maintain consistent project state across all agents
- **Conflict Prevention**: Proactively identify and address potential conflicts
- **Status Visibility**: Maintain clear visibility into coordination status

### Multi-Agent Coordination
- **Role Clarity**: Ensure each agent understands their coordination role
- **Change Communication**: Communicate changes that affect other agents
- **Dependency Awareness**: Track dependencies across different agent work
- **Synchronization Timing**: Coordinate synchronization at appropriate intervals

### Collaboration Quality
- **Consistency First**: Prioritize project state consistency over individual progress
- **Communication Protocol**: Follow established protocols for agent interaction
- **Conflict Resolution**: Address conflicts quickly and transparently
- **Progress Coordination**: Ensure coordinated progress toward common goals

## Common Hub Scenarios

### Multi-Agent Development
- **Role Specialization**: Different agents focus on specialized tasks
- **Dependency Coordination**: Managing interdependent development activities
- **State Synchronization**: Keeping project information consistent
- **Progress Alignment**: Coordinating progress toward common milestones

### Distributed Work Management
- **Activity Distribution**: Appropriate assignment of tasks across agents
- **Progress Monitoring**: Tracking distributed development progress
- **Quality Assurance**: Coordinating quality across different agent work
- **Integration Coordination**: Managing integration of distributed components

### State Management
- **Consistency Maintenance**: Keeping project state coherent across agents
- **Change Propagation**: Ensuring changes propagate to all agents
- **Version Coordination**: Managing different versions of project artifacts
- **Information Sharing**: Sharing relevant information across agents

## Examples

### Example 1: Hub Initialization
```
/goalkit.hub
```
**Output**: Establishes collaboration hub and connects available agents

### Example 2: Status Check
```
/goalkit.hub --status
```
**Output**: Current hub status, connected agents, and coordination state

### Example 3: State Synchronization
```
/goalkit.hub --sync
```
**Output**: Synchronizes project state across all connected agents

### Example 4: Multi-Agent Workflow with Hub
```
/goalkit.hub → Establish coordination hub
[Agent A]: /goalkit.goal Create user authentication system
[Agent B]: /goalkit.hub --sync → Gets updated project state
[Agent B]: /goalkit.strategies → Explores authentication approaches
[Hub coordinates and synchronizes activities between agents]
```

## Agent Integration

### Hub-Aware Collaboration
**CRITICAL**: Agents should coordinate through the hub for multi-agent work:

1. **Hub Connection**: Connect to collaboration hub before multi-agent work
2. **State Awareness**: Maintain awareness of shared project state
3. **Communication Protocol**: Follow established communication protocols
4. **Synchronization**: Keep project state consistent across agents

### Automated Hub Management
- **Automatic Connection**: Connect to hub when multi-agent work is detected
- **Status Monitoring**: Continuously monitor coordination status
- **Conflict Detection**: Automatically detect and report potential conflicts
- **State Synchronization**: Maintain consistent state across sessions

## Hub Applications

### Multi-Agent Workflows
- **Specialized Roles**: Different agents handle different specialized tasks
- **Distributed Development**: Coordinate work across different agents
- **Quality Assurance**: Coordinate quality checks across different perspectives
- **Progress Tracking**: Maintain unified progress across distributed work

### State Management
- **Consistency**: Maintain project state consistency across agents
- **Change Tracking**: Track and coordinate changes across agent sessions
- **Information Sharing**: Enable effective information sharing
- **Activity Coordination**: Coordinate interdependent activities

## Key Benefits

- **Collaboration**: Enable effective multi-agent coordination
- **Consistency**: Maintain project state coherence across agents
- **Efficiency**: Coordinate work to avoid duplication or conflicts
- **Visibility**: Maintain clear visibility into distributed work
- **Quality**: Leverage multiple perspectives for better outcomes

## Critical Rules

✅ **DO**: Connect to hub before engaging in multi-agent work
✅ **DO**: Maintain synchronization with shared project state
✅ **DO**: Follow established communication protocols
✅ **DO**: Report conflicts or inconsistencies to hub
❌ **DON'T**: Make assumptions about state without hub synchronization
❌ **DON'T**: Ignore coordination requirements in multi-agent scenarios
❌ **DON'T**: Make changes that affect others without hub coordination

## Next Steps Integration

**After `/goalkit.hub`**:
- **Check Status**: Verify connection and coordination readiness
- **Synchronize State**: Ensure current project state is consistent
- **Coordinate Activities**: Plan coordinated activities with other agents
- **Monitor Progress**: Track coordinated work through hub visibility
- **Maintain Connection**: Keep hub connection active during multi-agent work