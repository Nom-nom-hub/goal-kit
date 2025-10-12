---
layout: default
title: Agent Profile Command - Goal Kit Documentation
---

# Agent Profile Command (`/goalkit.agent-profile`)

## Overview

The Agent Profile command establishes and maintains information about the AI agent's capabilities, preferences, and operational parameters. It allows for customization of the AI's behavior to better align with project needs and user preferences.

## Purpose

The `/goalkit.agent-profile` command is essential for:

- Defining the AI agent's role and capabilities within the development process
- Setting preferences for how the agent should approach goal-driven development
- Configuring operational parameters and constraints for the agent
- Establishing communication and interaction preferences
- Maintaining consistency in the agent's behavior across sessions

## Usage

```
/goalkit.agent-profile [description of agent capabilities, preferences, and operational parameters]
```

## Key Components

### Agent Capabilities
Clear definition of what the AI agent is capable of doing within the goal-driven development framework, including technical skills and domain knowledge.

### Operational Preferences
Preferences for how the agent should interact with users, approach problem-solving, and engage with the goal-driven development process.

### Constraints and Boundaries
Clear boundaries on what the agent should not do, including technical limitations, ethical boundaries, or project-specific constraints.

### Communication Style
Preferred communication style and format for the agent's interactions with users during the development process.

### Learning Preferences
How the agent should approach learning from interactions and adapting its approach based on feedback.

## Best Practices

- Align agent capabilities with the specific needs of the project
- Define clear boundaries to prevent the agent from taking inappropriate actions
- Ensure operational preferences support the goal-driven development methodology
- Regularly update the agent profile as the project evolves
- Document any changes to the agent profile to maintain consistency

## Example

```
/goalkit.agent-profile Configure the AI agent for a security-focused project: prioritize security considerations in all recommendations, emphasize validation and testing in all suggestions, maintain a conservative approach to new technologies, and focus on compliance with industry standards. The agent should ask clarifying questions when security implications are unclear and always suggest security reviews for architecture decisions.
```

## Integration with Goal-Driven Development

The agent profile provides the foundational parameters within which all other Goal Kit commands operate. A properly configured agent profile ensures that the AI's recommendations and guidance align with the project's specific needs, constraints, and goals. This command supports the Goal-Driven Development principle of aligning all activities with desired outcomes by ensuring the AI agent is properly calibrated to support the project's specific objectives.