# Context Capture for Goal Kit

This module provides functionality for AI agents to capture and maintain context about goals, strategies, and milestones within the markdown-based Goal Kit system.

## Purpose

When AI agents interact with users about their goals, strategies, and milestones, this module helps capture relevant context and store it in a way that persists across sessions. This allows AI agents to maintain awareness of:

- Current goals and their status
- Active strategies being explored
- Milestones being worked on
- Relevant project information
- Previous conversations and decisions

## Approach

Rather than using external storage mechanisms, the context is maintained through:

1. **Enhanced metadata in goal files** - Adding context information directly to existing goal markdown files
2. **Context summary files** - Creating special markdown files that summarize active project context
3. **AI interaction logs** - Recording relevant parts of AI-user interactions in markdown format

## Implementation

### 1. Enhanced goal files with context metadata

Goals will have additional metadata sections to track context:

```markdown
# Goal: Improve User Onboarding

**Goal Statement**: Reduce new user time-to-value by 50% through improved onboarding experience.

**Created**: 2025-10-12
**Goal Branch**: 001-improve-onboarding

**Context Metadata**:
- **Last AI Interaction**: 2025-10-12T10:30:00Z
- **Active Strategy**: Option 1 - Interactive Tutorials
- **Current Milestone**: Milestone 1 - Prototype Interactive Elements
- **Status**: In Progress
- **Key Stakeholders**: Design Team, Product Team
- **Related Goals**: 002-ux-improvements, 003-analytics-tracking
```

### 2. Context summary files

A special `ai-context.md` file in the project root will summarize active context:

```markdown
# AI Context Summary

**Date**: 2025-10-12

## Active Goals
- [001-improve-onboarding](goals/001-improve-onboarding/goal.md) - In Progress
- [002-ux-improvements](goals/002-ux-improvements/goal.md) - Planned

## Active Strategies
- **Goal 001**: Interactive Tutorials approach
- **Goal 002**: User Research approach

## Current Milestones
- 001: Prototype Interactive Elements (due 2025-10-20)
- 002: Complete User Research (due 2025-10-25)

## Key Information
- **Project**: Customer Onboarding Platform
- **Team**: Frontend Team
- **Timeline**: Q4 2025
- **Budget**: $50,000

## Recent Decisions
1. Approved Interactive Tutorials approach for onboarding
2. Postponed analytics tracking to next quarter
```

### 3. AI interaction logs

Interactions with AI about goals will be recorded in markdown files:

```markdown
# AI Interaction Log - Goal 001-improve-onboarding

**Date**: 2025-10-12
**Participants**: User, AI Assistant

## Summary
User asked for recommendations on onboarding strategies. AI recommended interactive tutorials based on research and previous successful implementations.

## Full Interaction
**User**: "What's the best approach for improving user onboarding?"

**AI**: "Based on research, the most effective approach is interactive tutorials that guide users through core features within the actual interface..."

**User**: "How should we prioritize features for the tutorial?"

**AI**: "Focus on the 3-5 core actions that drive the most value for users..."

## Decisions Made
- Prioritize interactive tutorials over video-based guides
- Focus on first 3 core features for initial implementation
```

## Context Capture Process

When AI agents interact with users about their goals:

1. **Identify relevant goal files** - Determine which goals are being discussed
2. **Update metadata** - Update context metadata in relevant goal files
3. **Update summary** - Update the ai-context.md summary file
4. **Record interaction** - Log key interactions in dated markdown files
5. **Link related content** - Create cross-links between related goals and strategies

## Context Retrieval Process

When AI agents start a new session:

1. **Read summary** - Load context from ai-context.md
2. **Load active goals** - Read details from active goal files
3. **Review recent interactions** - Read from interaction logs
4. **Present context** - Make context available to AI for responses