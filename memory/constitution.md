# Goal-Driven Development (GDD) Constitution

## I. Purpose and Scope
This Constitution establishes the foundational principles and mandatory workflow for all development activities within this project. Its primary objective is to ensure that every technical decision is anchored in measurable business or user outcomes rather than implementation preferences.

## II. Core Pillars of GDD

### 1. Outcome Supremacy
All development efforts MUST begin with a clearly defined outcome. We do not build "features"; we achieve "goals." A goal is only valid if it describes a change in the state of the world (user behavior, system performance, business metric) and NOT the technology used to achieve it.

### 2. Implementation Agnosticism in Planning
Goal definitions and success criteria must remain strictly implementation-agnostic. Language, framework, and architectural choices are secondary to the "What" and "Why." Technical strategies are explored only after the "What" is solidified.

### 3. Divergent Strategy Exploration
For every significant goal, at least three distinct implementation strategies must be explored. This prevents "vibe-coding" and ensures that the chosen path is the result of conscious trade-off analysis (e.g., Speed vs. Scalability vs. Cost).

### 4. Empirical Milestone Validation
Progress is measured through the completion of "Evidence-Based Milestones." A milestone is not complete when code is written; it is complete when the success metric it tracks has been measured and validated against the goal.

### 5. The Learning Loop (Adaptive Execution)
Execution is a series of experiments. If a strategy is failing to move the success metrics, the agent MUST pause, report the findings, and propose a pivot. Failure to achieve a metric is not a failure of the agent, but a signal to adapt the strategy.

## III. Mandatory Workflow
The AI Agent must strictly adhere to the following linear sequence for every new initiative:

1.  **Visioning** (`/goalkit.vision`): Define the "North Star" and guiding principles.
2.  **Goal Setting** (`/goalkit.goal`): Define measurable, technology-free outcomes.
3.  **Strategy Selection** (`/goalkit.strategies`): Compare multiple implementation paths.
4.  **Milestone Planning** (`/goalkit.milestones`): Break down the strategy into measurable steps.
5.  **Adaptive Execution** (`/goalkit.execute`): Build, measure, and learn.

## IV. Governance and Amendments
*   This Constitution is the supreme guide for the AI Agent.
*   Any instruction from the user that directly contradicts these pillars should be flagged by the agent for alignment.
*   Amendments to this Constitution require a formal review of project alignment.

---
**Framework**: Goal-Driven Development (GDD) v1.0
**Status**: Active & Binding
