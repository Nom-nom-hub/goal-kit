---
layout: default
title: Goal Kit - Goal-Driven Development Toolkit
---

# Goal Kit - Goal-Driven Development Toolkit

## What is Goal-Driven Development?

Goal-Driven Development **focuses on outcomes over specifications**. While Spec-Driven Development creates detailed specifications that generate specific implementations, Goal-Driven Development starts with high-level goals and explores multiple strategies to achieve them.

### Key Differences from Spec-Driven Development:

| Spec-Driven Development | Goal-Driven Development |
|------------------------|------------------------|
| Detailed specifications upfront | High-level goals and outcomes |
| Single implementation path | Multiple strategies exploration |
| Requirements-focused | Metrics and success-focused |
| Implementation precision | Outcome flexibility |

## Key Commands

### Core Commands

Essential commands for the Goal-Driven Development workflow:

- **`/goalkit.vision`** - Create or update project vision, values, and success criteria
- **`/goalkit.goal`** - Define goals and desired outcomes (focus on why, not how)
- **`/goalkit.strategies`** - Explore multiple implementation strategies for achieving goals
- **`/goalkit.milestones`** - Generate measurable milestones and progress indicators
- **`/goalkit.execute`** - Execute implementation with flexibility to adapt and learn

### Optional Commands

Additional commands for enhanced exploration and validation:



## Supported AI Agents

Goal Kit supports 12 different AI agents:

- Claude Code
- GitHub Copilot
- Gemini CLI
- Cursor
- Qwen Code
- opencode
- Codex CLI
- Windsurf
- Kilo Code
- Auggie CLI
- Roo Code
- Amazon Q Developer CLI

## Development phases

1. **Vision Setting** - Establish purpose
2. **Goal Definition** - Outcomes over specs
3. **Strategy Exploration** - Multiple approaches
4. **Milestone Planning** - Measurable progress
5. **Adaptive Execution** - Learning implementation

## Task Complexity Assessment

Goal Kit includes a task complexity assessment to determine the appropriate approach:

### Simple Tasks (Direct Implementation)
For minor changes and enhancements:
- Visual improvements (e.g., "enhanced header", "better styling")
- Minor bug fixes
- Small UI adjustments
- Use direct implementation without the full methodology

### Complex Goals (Full Methodology) 
For substantial features requiring measurement:
- New major functionality
- System architecture changes
- Complex user workflows
- Features requiring measurable success criteria

## Key Principles

### Goals over Specifications
- Focus on outcomes and success criteria
- Define what success looks like before how to achieve it
- Keep goals high-level and flexible

### Multiple Strategies
- Explore different approaches to achieve each goal
- Consider various technical and user experience patterns
- Evaluate trade-offs and risks openly

### Professional UI/UX Standards
Goal Kit now includes comprehensive UI/UX design standards to ensure professional, accessible interfaces:

#### Visual Consistency
- **Typography**: Use maximum 2 font families with clear heading hierarchy (H1, H2, H3, etc.)
- **Color Palette**: Define consistent color system with primary, secondary, and accent colors
- **Spacing System**: Use consistent spacing scale (4px, 8px, 16px, 24px, 32px) for margins and padding
- **Component Library**: Create reusable components with consistent styling and behavior

#### Accessibility Requirements
- **WCAG Compliance**: Meet WCAG 2.1 AA standards for color contrast, keyboard navigation, and screen reader compatibility
- **Color Usage**: Maintain minimum 4.5:1 contrast ratio for normal text and 3:1 for large text
- **Keyboard Navigation**: All functionality accessible via keyboard
- **Screen Reader Support**: All UI elements with proper semantic markup and ARIA labels

#### Professional Aesthetics
- **Visual Hierarchy**: Use clear typography, appropriate sizing, and strategic color contrast
- **Whitespace**: Apply generous spacing between elements to reduce cognitive load
- **Responsive Design**: Ensure interfaces work well across all screen sizes and devices
- **Performance**: Optimize UI elements for fast loading and smooth interactions

## Quick Installation

```bash
uv tool install goalkeeper-cli --from git+https://github.com/Nom-nom-hub/goal-kit.git
```

Then use the tool directly:

```bash
goalkeeper init <PROJECT_NAME>
goalkeeper check
```

For more detailed information, see the full documentation.