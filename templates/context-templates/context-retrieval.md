# Context Retrieval for Goal Kit

This module outlines how AI agents retrieve project context from the markdown-based Goal Kit system when starting new sessions.

## Purpose

When AI agents begin a new interaction session, they need to quickly access relevant context about:

- Active goals and their current status
- Strategies being pursued
- Current milestones and deadlines
- Project-specific information
- Previous decisions and discussions

## Approach

Context retrieval happens by reading and processing existing markdown files in the Goal Kit structure:

1. **Load context summary** - Read the `ai-context.md` file to understand current project state
2. **Parse active goals** - Load details from active goal files
3. **Review recent interactions** - Process recent AI interaction log files
4. **Aggregate information** - Combine all sources into a coherent context for the AI

## Implementation

### 1. Context Summary File Reading

The AI will read the `ai-context.md` file in the project root to get an overview:

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

### 2. Active Goal File Processing

The AI will then read the active goal files to get detailed information:

```markdown
# Goal: Improve User Onboarding

**Goal Statement**: Reduce new user time-to-value by 50% through improved onboarding experience.

**Created**: 2025-10-10
**Goal Branch**: 001-improve-onboarding

## 1. Goal Overview

### Goal Statement
Reduce new user time-to-value by 50% through improved onboarding experience.

### Context
Current onboarding process is too complex and causes new users to abandon the platform early.

### Success Level
Achieve 50% reduction in time-to-value for new users, measured by time to complete first meaningful action.

## 2. Success Metrics

### Primary Metrics
- Time-to-value reduced by 50% (from 4 days to 2 days)
- User engagement in first week increased by 30%
- User satisfaction scores for onboarding increased to 4.5/5

### Secondary Metrics
- Feature adoption rate for core features increases by 25%
- Support ticket volume for onboarding issues decreases by 40%

### Measurement Approach
- Analytics tracking of user journey through onboarding
- User feedback surveys after onboarding completion
- A/B testing between old and new onboarding flows

## 3. Target Users & Stakeholders

### Primary Users
- New users of the platform (first 7 days)

### Stakeholders
- Product team
- UX designers
- Customer success team
- Engineering team

## 4. Goal Hypotheses

### Key Assumptions
- If we provide guided tutorials, then new users will understand core features faster
- If we personalize onboarding, then user engagement will increase
- If we reduce steps in onboarding, then completion rates will improve

### Risk Factors
- Changes to onboarding may require significant development effort
- Some users may prefer self-guided onboarding
- Measuring time-to-value accurately may be challenging

### Validation Strategy
- A/B testing between current flow and new guided approach
- User interview sessions to validate tutorial effectiveness
- Analytics tracking to validate success metrics

## 5. Goal Milestones

### Milestone 1: Research and Design
- **Description**: Conduct user research and design onboarding flow improvements
- **Acceptance Criteria**: User research report completed, onboarding designs finalized and approved
- **Evidence Requirements**: Research findings documented, design mockups approved by stakeholders
- **Timeline**: 2025-10-15
- **Resource Allocation**: 2 designers, 1 researcher for 2 weeks
- **Success Metrics**: Research report with actionable insights, approved designs

### Milestone 2: Prototype Development
- **Description**: Build interactive prototype of new onboarding flow
- **Acceptance Criteria**: Interactive prototype built and tested with internal team
- **Evidence Requirements**: Working prototype demonstrating guided onboarding experience
- **Timeline**: 2025-10-20
- **Resource Allocation**: 1 frontend developer for 1 week
- **Success Metrics**: Functional prototype with core guided elements

**Context Metadata**:
- **Last AI Interaction**: 2025-10-12T10:30:00Z
- **Active Strategy**: Option 1 - Interactive Tutorials
- **Current Milestone**: Milestone 1 - Research and Design
- **Status**: In Progress
- **Key Stakeholders**: Design Team, Product Team
- **Related Goals**: 002-ux-improvements, 003-analytics-tracking
```

### 3. Interaction Log Processing

The AI will process recent interaction logs to understand recent conversations:

```markdown
# AI Interaction Log - Goal 001-improve-onboarding

**Date**: 2025-10-12
**Participants**: User, AI Assistant

## Summary
User asked for recommendations on onboarding strategies. AI recommended interactive tutorials based on research and previous successful implementations.

## Full Interaction
**User**: "What's the best approach for improving user onboarding?"

**AI**: "Based on research, the most effective approach is interactive tutorials that guide users through core features within the actual interface. This approach has shown to improve user engagement by up to 40% compared to static guides."

**User**: "How should we prioritize features for the tutorial?"

**AI**: "Focus on the 3-5 core actions that drive the most value for users. Typically, these are the actions that lead to the 'aha moment' in your product."

## Decisions Made
- Prioritize interactive tutorials over video-based guides
- Focus on first 3 core features for initial implementation
```

### 4. Context Aggregation

All information from these sources will be aggregated into a structured format that the AI can easily access:

```
Active Project Context:
- Project: Customer Onboarding Platform
- Active Goals: 001-improve-onboarding (In Progress), 002-ux-improvements (Planned)
- Current Focus: Goal 001 - Improve User Onboarding
- Active Strategy: Interactive Tutorials approach
- Current Milestone: Research and Design phase (due 2025-10-15)
- Recent Decisions: Prioritize interactive tutorials, focus on 3 core features
- Team: Frontend Team
- Timeline: Q4 2025
- Budget: $50,000
```

## Context Retrieval Process

When an AI agent starts a new session:

1. **Scan project directory** for `ai-context.md` file
2. **Parse context summary** to understand current state
3. **Identify active goals** from the summary
4. **Load goal files** for detailed information
5. **Read recent interaction logs** to understand recent discussions
6. **Build context model** combining all information sources
7. **Make context available** to AI for generating responses

## Performance Optimization

To ensure quick context retrieval:

- **Selective loading**: Only load context for active goals rather than all goals
- **Caching**: Cache parsed context information between interactions
- **Incremental updates**: Update context based on files that have changed since last session
- **Indexing**: Maintain an index of goal relationships and dependencies