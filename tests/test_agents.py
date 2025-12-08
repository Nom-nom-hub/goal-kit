"""Tests for agents module.

Tests the Agent dataclass, AgentRegistry class, and helper functions.
"""

import pytest
from goalkeeper_cli.agents import Agent, AgentRegistry, get_agent, list_agents, validate_agent


class TestAgent:
    """Test Agent dataclass."""
    
    def test_agent_creation(self):
        """Test creating an Agent instance."""
        agent = Agent(
            key="claude",
            name="Claude Code",
            folder=".claude/",
            install_url="https://docs.anthropic.com/en/docs/claude-code/setup",
            requires_cli=True
        )
        
        assert agent.key == "claude"
        assert agent.name == "Claude Code"
        assert agent.folder == ".claude/"
        assert agent.requires_cli is True
    
    def test_agent_with_none_install_url(self):
        """Test creating an Agent with no install URL (IDE-based)."""
        agent = Agent(
            key="copilot",
            name="GitHub Copilot",
            folder=".github/",
            install_url=None,
            requires_cli=False
        )
        
        assert agent.install_url is None
        assert agent.requires_cli is False
    
    def test_agent_equality(self):
        """Test that identical agents are equal."""
        agent1 = Agent("test", "Test Agent", ".test/", None, False)
        agent2 = Agent("test", "Test Agent", ".test/", None, False)
        
        assert agent1 == agent2


class TestAgentRegistry:
    """Test AgentRegistry class."""
    
    def test_registry_init_loads_agents(self):
        """Test that registry initializes with default agents."""
        registry = AgentRegistry()
        agents = registry.list_all()
        
        assert len(agents) == 13
        assert all(isinstance(a, Agent) for a in agents)
    
    def test_registry_get_valid_agent(self):
        """Test getting an agent by key."""
        registry = AgentRegistry()
        agent = registry.get("claude")
        
        assert agent is not None
        assert agent.key == "claude"
        assert agent.name == "Claude Code"
    
    def test_registry_get_invalid_agent(self):
        """Test getting non-existent agent returns None."""
        registry = AgentRegistry()
        agent = registry.get("nonexistent")
        
        assert agent is None
    
    def test_registry_validate_valid_agent(self):
        """Test validating an existing agent."""
        registry = AgentRegistry()
        
        assert registry.validate("claude") is True
        assert registry.validate("copilot") is True
        assert registry.validate("gemini") is True
    
    def test_registry_validate_invalid_agent(self):
        """Test validating non-existent agent."""
        registry = AgentRegistry()
        
        assert registry.validate("nonexistent") is False
        assert registry.validate("") is False


class TestAgentHelpers:
    """Test module-level helper functions."""
    
    def test_get_agent_helper(self):
        """Test get_agent() helper function."""
        agent = get_agent("claude")
        
        assert agent is not None
        assert agent.key == "claude"
        assert agent.name == "Claude Code"
    
    def test_get_agent_returns_none_for_invalid(self):
        """Test get_agent() returns None for invalid agent."""
        agent = get_agent("invalid_agent")
        
        assert agent is None
    
    def test_list_agents_helper(self):
        """Test list_agents() helper function."""
        agents = list_agents()
        
        assert len(agents) == 13
        assert all(isinstance(a, Agent) for a in agents)
        assert any(a.key == "claude" for a in agents)
        assert any(a.key == "copilot" for a in agents)
    
    def test_validate_agent_helper(self):
        """Test validate_agent() helper function."""
        assert validate_agent("claude") is True
        assert validate_agent("copilot") is True
        assert validate_agent("cursor") is True
        assert validate_agent("invalid") is False


class TestAllAgents:
    """Test that all expected agents are registered."""
    
    def test_all_agents_present(self):
        """Test that all 13 agents are in registry."""
        expected_agents = {
            "copilot", "claude", "gemini", "cursor", "qwen",
            "opencode", "codex", "windsurf", "kilocode", "auggie",
            "codebuddy", "roo", "q"
        }
        
        agents = list_agents()
        registered_keys = {a.key for a in agents}
        
        assert registered_keys == expected_agents
    
    def test_agent_configurations(self):
        """Test specific agent configurations."""
        # Claude should require CLI
        claude = get_agent("claude")
        assert claude.requires_cli is True
        assert claude.install_url is not None
        
        # Copilot is IDE-based (no CLI required)
        copilot = get_agent("copilot")
        assert copilot.requires_cli is False
        assert copilot.install_url is None
        
        # Qwen requires CLI
        qwen = get_agent("qwen")
        assert qwen.requires_cli is True
    
    def test_agent_folders_are_unique(self):
        """Test that each agent has a unique folder path."""
        agents = list_agents()
        folders = [a.folder for a in agents]
        
        # No duplicates
        assert len(folders) == len(set(folders))
