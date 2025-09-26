# Agent-Specific Packaging Analysis: Spec-Kit vs Goal-Kit

## Overview

This document analyzes the differences between how spec-kit and goal-kit handle agent-specific packaging, providing recommendations for goal-kit to adopt spec-kit's approach.

## Current Approaches

### Spec-Kit Packaging Approach

- Uses YAML frontmatter in command templates with script variants (sh/ps) defined in the template
- Supports dynamic command generation with the `generate_commands()` function
- Creates agent-specific packages with tailored command files for each AI agent
- Uses `.specify/` as base directory with agent-specific subdirectories
- Includes both bash and PowerShell script variants in template definitions
- Supports 11 different agents (claude, gemini, copilot, cursor, qwen, opencode, windsurf, codex, kilocode, auggie, roo)

### Goal-Kit Packaging Approach

- Uses static command files in agent-specific directories (`.qwen/commands/`, `.cursor/commands/`)
- Currently only supports cursor but the GitHub release script indicates support for multiple agents
- Uses `.goalify/` as base directory
- Has separate packaging script (`package-releases.sh`) but limited agent support
- Supports both bash and PowerShell scripts but with manual packaging

## Key Differences

1. **Template Structure**:
   - Spec-Kit: Templates with YAML frontmatter containing both bash and PowerShell script definitions
   - Goal-Kit: Static command files with hardcoded script paths

2. **Command Generation**:
   - Spec-Kit: Dynamic generation of agent-specific command files using `generate_commands()` function
   - Goal-Kit: Pre-existing agent-specific command files

3. **Packaging Logic**:
   - Spec-Kit: Agent-specific inclusion with conditional copying based on agent type
   - Goal-Kit: Static copy approach with fixed directory structure

4. **Agent Support**:
   - Spec-Kit: Comprehensive support for 11 agents with consistent approach
   - Goal-Kit: Limited support but potential for expansion

## Recommendations for Goal-Kit

### 1. Implement Dynamic Command Generation

Goal-Kit should implement a `generate_commands()` function similar to spec-kit to dynamically create agent-specific command files from a single template:

```bash
generate_commands() {
  local agent=$1 ext=$2 arg_format=$3 output_dir=$4 script_variant=$5
  # Implementation similar to spec-kit
}
```

### 2. Update Template Structure

Convert static command files to templates with YAML frontmatter that define both bash and PowerShell variants:

```yaml
---
description: Create comprehensive goal definitions with structured planning, milestones, and success criteria.
scripts:
  sh: scripts/bash/create-goal.sh --json "{ARGS}"
  ps: scripts/powershell/create-goal.ps1 -Json "{ARGS}"
---
# Command content with placeholders
```

### 3. Enhance Packaging Script

Modify the packaging script to support agent-specific inclusion like spec-kit does, with support for all major AI agents:

- Claude: `.claude/commands/` (Markdown format)
- Gemini: `.gemini/commands/` (TOML format)
- Copilot: `.github/prompts/` (Markdown format)
- Cursor: `.cursor/commands/` (Markdown format)
- Qwen: `.qwen/commands/` (TOML format)
- And other supported agents

### 4. Implement Agent-Specific Path Rewriting

Use a `rewrite_paths()` function to ensure paths are correctly rewritten for each agent's expected directory structure:

```bash
rewrite_paths() {
  sed -E \
    -e 's@(/?)templates/@.goalify/templates/@g' \
    -e 's@(/?)scripts/@.goalify/scripts/@g' \
    -e 's@(/?)memory/@.goalify/memory/@g'
}
```

### 5. Standardize Argument Placeholders

Ensure consistent use of agent-appropriate argument placeholders:

- Markdown-based agents: `$ARGUMENTS`
- TOML-based agents: `{{args}}`

### 6. Support Both Script Variants

Like spec-kit, provide both bash (sh) and PowerShell (ps) script variants in the same template, allowing the packaging script to select the appropriate one during package creation.

## Expected Benefits

1. **Reduced Maintenance**: Single template source for all agents instead of multiple agent-specific files
2. **Consistency**: All agents get the same functionality with consistent implementation
3. **Easier Expansion**: Adding new agents requires minimal changes
4. **Flexibility**: Ability to target specific agents or script types during packaging

## Implementation Steps

1. Convert existing static command files to templates with YAML frontmatter
2. Update the packaging script with dynamic command generation
3. Test with multiple agents to ensure compatibility
4. Update documentation to reflect new approach

## Conclusion

Goal-Kit should adopt spec-kit's approach of dynamic agent-specific packaging to provide a more maintainable and scalable solution. This will allow for consistent functionality across all supported agents while reducing maintenance overhead and enabling easier expansion to support new agents in the future.
