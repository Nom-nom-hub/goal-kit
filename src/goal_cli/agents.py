"""
AI agent integration module for the goal-dev-spec system.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional

class AgentManager:
    """Manages AI agent integrations and configurations."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.agents_path = project_path / "agents"
        
    def get_agent_config(self, agent_name: str) -> Optional[Dict]:
        """Get configuration for a specific agent."""
        config_file = self.agents_path / agent_name / "config.yaml"
        if not config_file.exists():
            return None
        
        with open(config_file, 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    
    def list_available_agents(self) -> List[str]:
        """List all available agents."""
        if not self.agents_path.exists():
            return []
        
        agents = []
        for item in self.agents_path.iterdir():
            if item.is_dir() and (item / "config.yaml").exists():
                agents.append(item.name)
        
        return agents
    
    def create_agent_command(self, agent_name: str, command_name: str, prompt: str) -> str:
        """Create an agent command file."""
        agent_dir = self.agents_path / agent_name
        agent_dir.mkdir(exist_ok=True)
        
        # Create command file based on agent type
        config = self.get_agent_config(agent_name)
        if not config:
            # Default to YAML format
            command_file = agent_dir / f"{command_name}.yaml"
            command_data = {
                "command": command_name,
                "description": f"Command for {command_name}",
                "prompt": prompt
            }
        else:
            format_type = config.get("format", "yaml")
            if format_type == "yaml":
                command_file = agent_dir / f"{command_name}.yaml"
                command_data = {
                    "command": command_name,
                    "description": f"Command for {command_name}",
                    "prompt": prompt
                }
            elif format_type == "toml":
                command_file = agent_dir / f"{command_name}.toml"
                # TOML format would be different
                command_data = f"""
description = "Command for {command_name}"

prompt = '''
{prompt}
'''
"""
            else:  # markdown
                command_file = agent_dir / f"{command_name}.md"
                command_data = f"""---
description: "Command for {command_name}"
---

{prompt}
"""
        
        # Write command file
        if isinstance(command_data, dict):
            with open(command_file, 'w') as f:
                yaml.dump(command_data, f, default_flow_style=False, sort_keys=False)
        else:
            with open(command_file, 'w') as f:
                f.write(command_data)
        
        return str(command_file)

# Example agent configurations
DEFAULT_AGENT_CONFIGS = {
    "claude": {
        "name": "claude",
        "type": "cli",
        "description": "Anthropic's Claude Code CLI",
        "cli_tool": "claude",
        "directory": ".claude/commands/",
        "format": "md",
        "argument_pattern": "$ARGUMENTS"
    },
    "gemini": {
        "name": "gemini",
        "type": "cli",
        "description": "Google's Gemini CLI",
        "cli_tool": "gemini",
        "directory": ".gemini/commands/",
        "format": "toml",
        "argument_pattern": "{{args}}"
    },
    "qwen": {
        "name": "qwen",
        "type": "cli",
        "description": "Alibaba's Qwen Code CLI",
        "cli_tool": "qwen",
        "directory": ".qwen/commands/",
        "format": "toml",
        "argument_pattern": "{{args}}"
    }
}

def create_default_agent_configs(agents_path: Path):
    """Create default configuration files for supported agents."""
    for agent_name, config in DEFAULT_AGENT_CONFIGS.items():
        agent_dir = agents_path / agent_name
        agent_dir.mkdir(exist_ok=True)
        
        config_file = agent_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    print("AgentManager module loaded")