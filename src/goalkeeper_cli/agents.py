"""Agent configuration and management for Goalkeeper CLI.

Provides a clean abstraction for AI agent configurations, replacing the
monolithic AGENT_CONFIG dict in __init__.py.
"""

from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class Agent:
    """Configuration for a supported AI agent.
    
    Attributes:
        key: Unique identifier (e.g., 'claude', 'copilot')
        name: Display name (e.g., 'Claude Code')
        folder: Agent-specific folder in project (e.g., '.claude/')
        install_url: URL with installation instructions (None if IDE-based)
        requires_cli: Whether agent requires CLI tool to be installed
    """
    
    key: str
    name: str
    folder: str
    install_url: Optional[str]
    requires_cli: bool


class AgentRegistry:
    """Registry of supported AI agents.
    
    Maintains the complete list of supported agents and provides
    convenient access methods for validation and discovery.
    """
    
    def __init__(self):
        """Initialize registry with default agents."""
        self._agents: Dict[str, Agent] = {}
        self._init_defaults()
    
    def _init_defaults(self) -> None:
        """Initialize registry with all supported agents."""
        # Based on AGENT_CONFIG from original __init__.py
        agents_data = [
            ("copilot", "GitHub Copilot", ".github/", None, False),
            ("claude", "Claude Code", ".claude/", "https://docs.anthropic.com/en/docs/claude-code/setup", True),
            ("gemini", "Gemini CLI", ".gemini/", "https://github.com/google-gemini/gemini-cli", True),
            ("cursor", "Cursor", ".cursor/", None, False),
            ("qwen", "Qwen Code", ".qwen/", "https://github.com/QwenLM/qwen-code", True),
            ("opencode", "opencode", ".opencode/", "https://opencode.ai", True),
            ("codex", "Codex CLI", ".codex/", "https://github.com/openai/codex", True),
            ("windsurf", "Windsurf", ".windsurf/", None, False),
            ("kilocode", "Kilo Code", ".kilocode/", None, False),
            ("auggie", "Auggie CLI", ".augment/", "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli", True),
            ("codebuddy", "CodeBuddy", ".codebuddy/", "https://www.codebuddy.ai/cli", True),
            ("roo", "Roo Code", ".roo/", None, False),
            ("q", "Amazon Q Developer CLI", ".amazonq/", "https://aws.amazon.com/developer/learning/q-developer-cli/", True),
        ]
        
        for key, name, folder, install_url, requires_cli in agents_data:
            self._agents[key] = Agent(
                key=key,
                name=name,
                folder=folder,
                install_url=install_url,
                requires_cli=requires_cli
            )
    
    def get(self, key: str) -> Optional[Agent]:
        """Get agent by key.
        
        Args:
            key: Agent key (e.g., 'claude')
            
        Returns:
            Agent instance if found, None otherwise
        """
        return self._agents.get(key)
    
    def list_all(self) -> List[Agent]:
        """List all available agents.
        
        Returns:
            List of all Agent instances in registry
        """
        return list(self._agents.values())
    
    def validate(self, key: str) -> bool:
        """Check if agent key is valid.
        
        Args:
            key: Agent key to validate
            
        Returns:
            True if agent exists, False otherwise
        """
        return key in self._agents


# Module-level convenience functions using default registry
_default_registry = AgentRegistry()


def get_agent(key: str) -> Optional[Agent]:
    """Get agent by key.
    
    Args:
        key: Agent key (e.g., 'claude', 'copilot')
        
    Returns:
        Agent instance if found, None otherwise
        
    Example:
        >>> agent = get_agent('claude')
        >>> print(agent.name)
        Claude Code
    """
    return _default_registry.get(key)


def list_agents() -> List[Agent]:
    """List all available agents.
    
    Returns:
        List of all supported Agent instances
        
    Example:
        >>> agents = list_agents()
        >>> print(len(agents))
        13
    """
    return _default_registry.list_all()


def validate_agent(key: str) -> bool:
    """Validate agent key.
    
    Args:
        key: Agent key to validate
        
    Returns:
        True if agent is valid, False otherwise
        
    Example:
        >>> validate_agent('claude')
        True
        >>> validate_agent('invalid')
        False
    """
    return _default_registry.validate(key)
