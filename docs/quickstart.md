# Quick Start Guide

This guide will help you get started with Goal-Driven Development using the Goal Kit.

> NEW: All automation scripts now provide both Bash (`.sh`) and PowerShell (`.ps1`) variants. The `goal` CLI auto-selects based on OS unless you pass `--script sh|ps`.

## The 5-Step Process

### 1. Install Goal CLI

Initialize your project depending on the coding agent you're using:

```bash
uvx --from git+https://github.com/github/goal-dev-kit.git goal init <PROJECT_NAME>
```

Pick script type explicitly (optional):
```bash
uvx --from git+https://github.com/github/goal-dev-kit.git goal init <PROJECT_NAME> --script ps  # Force PowerShell
uvx --from git+https://github.com/github/goal-dev-kit.git goal init <PROJECT_NAME> --script sh  # Force POSIX shell
```

### 2. Define Your Goals

Use the `/goals` command to describe what outcomes you want to achieve. Focus on the **what** and **why**, not the tech stack.

```bash
/goals Build a team productivity platform that helps remote teams collaborate effectively, track project progress, and maintain work-life balance through smart scheduling and workload management
```

### 3. Clarify and Validate Goals

Use the `/clarify` command to resolve any ambiguities and ensure goals are achievable.

```bash
/clarify
```

### 4. Develop Implementation Strategy

Use the `/strategize` command to evaluate different approaches for achieving your goals.

```bash
/strategize We want to use modern web technologies with real-time collaboration features, focusing on user experience and scalability for growing teams
```

### 5. Plan and Implement

Use `/plan` to create detailed technical plans, then `/tasks` and `/implement` to execute.

## Detailed Example: Building TeamSync

Here's a complete example of building a remote team productivity platform:

### Step 1: Define Goals with `/goals`

```text
/goals Develop TeamSync, a remote team productivity platform. It should help distributed teams stay aligned,
track project progress, maintain work-life balance through smart scheduling, and improve collaboration effectiveness.
Teams should be able to set up projects, assign tasks with clear ownership, track progress in real-time,
and get insights into team productivity patterns. The goal is to reduce miscommunication by 40%,
improve project delivery predictability by 25%, and increase team satisfaction scores by 30%.
Success will be measured through user engagement metrics, project completion rates, and team feedback surveys.
```

### Step 2: Refine the Goals

After the initial goals are created, clarify any missing requirements:

```text
For the TeamSync platform, we want to support teams of 5-50 people across different time zones.
The platform should help with both synchronous collaboration (like quick standups) and asynchronous
work (like progress updates and task assignments). Users should be able to set their working hours
preferences and the system should suggest optimal meeting times. We also want to track metrics like
response times to messages, task completion velocity, and meeting effectiveness.
```

Also validate the goals checklist:

```text
Read the review and acceptance checklist, and check off each item in the checklist if the goal definition meets the criteria. Leave it empty if it does not.
```

### Step 3: Develop Strategy with `/strategize`

Evaluate different technical approaches:

```text
For TeamSync, we want to evaluate different technical approaches. Consider: 1) A modern web application
with real-time features using React frontend and Node.js backend, 2) A mobile-first approach with
React Native for cross-platform support, 3) A desktop application using Electron for rich features.
Evaluate based on development speed, user experience, scalability needs, and team capabilities.
```

### Step 4: Plan Technical Implementation with `/plan`

Be specific about your tech stack and technical requirements:

```text
Based on our web application strategy for TeamSync, we want to use React with TypeScript for the frontend,
Node.js with Express for the backend, PostgreSQL for the database, and WebSocket integration for real-time features.
Include authentication with JWT, responsive design, and comprehensive testing strategies.
```

### Step 5: Validate and Implement

Have your AI agent audit the implementation plan:

```text
Now I want you to go and audit the implementation plan and the implementation detail files.
Read through it with an eye on determining whether or not there is a sequence of tasks that you need
to be doing that are obvious from reading this. Because I don't know if there's enough here.
```

Finally, implement the solution:

```text
/implement
```

## Key Principles

- **Be outcome-focused** about what you want to achieve and why
- **Don't focus on tech stack** during goal definition phase
- **Iterate and refine** your goals before implementation
- **Validate** the strategy before coding begins
- **Let the AI agent handle** the implementation details
- **Stay aligned** with your defined goals throughout development

## Next Steps

- Read the complete methodology for in-depth guidance
- Check out more examples in the repository
- Explore the source code on GitHub
- Review the installation guide for detailed setup instructions
- Check the local development guide for contribution guidelines