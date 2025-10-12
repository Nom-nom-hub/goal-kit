# /goalkit.agent-profile Command Template

## Overview

The `/goalkit.agent-profile` command creates and manages profiles for specific AI agents to optimize Goal Kit commands for each agent's unique capabilities.

## Command Usage

```
/goalkit.agent-profile [agent-name] [configuration-options]
```

### Agent Names
- `claude`: Anthropic's Claude model
- `copilot`: GitHub Copilot
- `gemini`: Google's Gemini model
- `cursor`: Cursor IDE
- `qwen`: Qwen Code
- `opencode`: opencode
- `codex`: Codex CLI
- `windsurf`: Windsurf IDE
- `kilocode`: Kilo Code IDE
- `auggie`: Auggie CLI
- `roo`: Roo Code
- `q`: Amazon Q Developer

### Configuration Options
- `reasoning-focus`: Optimize for complex analysis and reasoning (best for Claude)
- `code-assist`: Optimize for coding assistance (best for Copilot, Cursor)
- `creative-solution`: Optimize for creative problem-solving (best for Gemini)
- `direct-implement`: Optimize for direct implementation (best for Cursor)
- `comprehensive-coverage`: Optimize for thorough analysis (best for Qwen)

## Implementation Guidance

### AI AGENT INSTRUCTIONS

When processing `/goalkit.agent-profile` requests:

1. **Identify Agent**: Recognize the specified AI agent and its strengths
2. **Apply Optimization**: Adjust prompting strategy based on configuration
3. **Maintain Consistency**: Ensure optimized approach maintains Goal Kit methodology
4. **Provide Feedback**: Indicate how the profile will enhance future interactions

### Response Structure

```
Agent Profile Created: [Agent Name] ([Configuration])
- [Specific optimization applied]
- [How this will enhance Goal Kit commands]
- [Example of improved interaction]

Selected templates and workflows adjusted for [Agent Name]'s strengths.
```

## Examples

### Example 1: Claude Reasoning Focus
```
/goalkit.agent-profile claude reasoning-focus

Claude Profile Created: Claude (Reasoning Focus)
- Enhanced prompting for complex analysis
- Step-by-step reasoning emphasis
- Critical thinking and evaluation focus
- Longer context retention optimization

Selected templates and workflows adjusted for Claude's reasoning strengths.
```

### Example 2: GitHub Copilot Code Assistance
```
/goalkit.agent-profile copilot code-assist

GitHub Copilot Profile Created: GitHub Copilot (Code Assist)
- Repository context awareness enabled
- Code completion and suggestion optimization
- Technical documentation priority
- Integration with development workflows

Selected templates and workflows adjusted for Copilot's coding strengths.
```

## Integration with Goal Kit Commands

The agent profile will influence how other Goal Kit commands behave:

- `/goalkit.vision`: Adjust prompting for agent's communication style
- `/goalkit.goal`: Optimize goal decomposition based on agent capabilities
- `/goalkit.strategies`: Suggest strategies that leverage agent strengths
- `/goalkit.milestones`: Create milestones appropriate for agent interaction model
- `/goalkit.execute`: Adapt execution approach to agent's working pattern

## Quality Assurance

Ensure the agent profile:
- Accurately reflects the agent's capabilities
- Improves user experience with that agent
- Maintains the integrity of Goal Kit methodology
- Provides measurable improvement in interaction quality