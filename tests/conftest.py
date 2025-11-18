"""
Pytest configuration and shared fixtures for Goal Kit tests.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_project_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing project initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "test-project"
        project_dir.mkdir()
        yield project_dir
        # Cleanup happens automatically with context manager


@pytest.fixture
def git_repo(temp_project_dir: Path) -> Generator[Path, None, None]:
    """Create a temporary git repository for testing."""
    os.chdir(temp_project_dir)
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        check=True,
        capture_output=True,
    )
    yield temp_project_dir


@pytest.fixture
def goalkit_project(git_repo: Path) -> Generator[Path, None, None]:
    """Create a Goal Kit project structure for testing."""
    goalkit_dir = git_repo / ".goalkit"
    goalkit_dir.mkdir(exist_ok=True)

    # Create vision file
    vision_file = goalkit_dir / "vision.md"
    vision_file.write_text(
        """# Project Vision

## Purpose
Test project for Goal Kit testing

## Success Criteria
- All tests pass
- Code is well organized
- Documentation is clear
"""
    )

    # Create goals directory
    goals_dir = goalkit_dir / "goals"
    goals_dir.mkdir(exist_ok=True)

    # Create a sample goal
    goal_001 = goals_dir / "001-test-goal"
    goal_001.mkdir(exist_ok=True)
    (goal_001 / "goal.md").write_text(
        """# Goal: Test Goal

## Success Metrics
- Metric 1: Value
"""
    )

    # Initialize git
    subprocess.run(["git", "add", ".goalkit"], check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initialize Goal Kit"],
        check=True,
        capture_output=True,
    )

    yield git_repo


@pytest.fixture
def mock_agents() -> dict:
    """Mock AI agent configurations for testing."""
    return {
        "claude": {"name": "Claude", "config_file": "CLAUDE.md"},
        "copilot": {"name": "GitHub Copilot", "config_file": ".copilot/context.md"},
        "gemini": {"name": "Google Gemini", "config_file": "GEMINI.md"},
        "cursor": {"name": "Cursor", "config_file": "CURSOR.md"},
        "qwen": {"name": "Qwen Code", "config_file": "QWEN.md"},
    }


@pytest.fixture
def sample_goal_files() -> dict:
    """Sample goal files for testing template operations."""
    return {
        "goal.md": """# Goal Statement: Build User Authentication

**Branch**: `001-build-user-authentication`
**Created**: 2025-01-01T00:00:00Z
**Status**: Draft
**Methodology**: Goal-Driven Development

## 🎯 Goal Definition

**Goal Statement**: Build user authentication with measurable success metrics

**Context**: Users need to create accounts and log in securely

**Success Level**: Authentication works reliably with clear error messages

## 📊 Success Metrics

### Primary Metrics
- Login time < 2 seconds for 95% of users
- Account creation success rate > 99%
- Password recovery success rate > 95%

### Secondary Metrics
- Mobile login success > 98%
""",
        "strategies.md": """# Strategy Analysis for 001-build-user-authentication

## Strategy Exploration Framework
- **OAuth Integration**: Industry standard approach
- **Session-Based**: Custom authentication system
- **JWT Tokens**: Stateless approach

## Recommended Starting Strategy
- **Primary Recommendation**: OAuth Integration
- **Rationale**: Industry standard, well-tested, reduces security risk
""",
        "milestones.md": """# Milestone Plan for 001-build-user-authentication

## Milestone 1: Technical Validation
- Proof of concept OAuth flow
- Success Indicators: OAuth tokens working

## Milestone 2: Core Implementation
- Complete login/register flows
- Success Indicators: Users can authenticate

## Milestone 3: User Testing
- Test with real users
- Success Indicators: User feedback collected
""",
        "execution.md": """# Execution Plan for 001-build-user-authentication

**Created**: 2025-01-01T00:00:00Z
**Status**: In Planning

## Selected Strategy
- **Strategy Name**: OAuth Integration
- **Rationale**: Industry standard, well-tested

## Execution Timeline

### Phase 1: Foundation
- Duration: 1 week
- Key Activities: Set up OAuth provider

### Phase 2: Implementation
- Duration: 2 weeks
- Key Activities: Implement login/register flows
""",
    }


@pytest.fixture
def shell_script_samples() -> dict:
    """Sample shell scripts for testing script execution."""
    return {
        "bash_test.sh": """#!/bin/bash
# Simple test script
echo "Test passed"
exit 0
""",
        "powershell_test.ps1": """# Simple test script
Write-Host "Test passed"
exit 0
""",
    }


@pytest.fixture
def mock_environment(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("GOAL_KIT_TEST", "true")
    monkeypatch.setenv("GH_TOKEN", "test_token_12345")
    return monkeypatch


class TestHelpers:
    """Helper methods for testing."""

    @staticmethod
    def create_goal_directory(base_dir: Path, goal_number: int, name: str) -> Path:
        """Create a goal directory with standard structure."""
        goal_dir = base_dir / ".goalkit" / "goals" / f"{goal_number:03d}-{name}"
        goal_dir.mkdir(parents=True, exist_ok=True)
        return goal_dir

    @staticmethod
    def create_goal_file(goal_dir: Path, content: str = None) -> Path:
        """Create a goal.md file in goal directory."""
        goal_file = goal_dir / "goal.md"
        if content is None:
            content = "# Goal Statement: Test Goal\n\n## 📊 Success Metrics\n- Test Metric 1"
        goal_file.write_text(content)
        return goal_file

    @staticmethod
    def create_strategies_file(goal_dir: Path, content: str = None) -> Path:
        """Create a strategies.md file in goal directory."""
        strategies_file = goal_dir / "strategies.md"
        if content is None:
            content = "# Strategies\n\n## Strategy 1\n- Approach A"
        strategies_file.write_text(content)
        return strategies_file

    @staticmethod
    def create_milestones_file(goal_dir: Path, content: str = None) -> Path:
        """Create a milestones.md file in goal directory."""
        milestones_file = goal_dir / "milestones.md"
        if content is None:
            content = "# Milestones\n\n## Milestone 1\n- Step 1"
        milestones_file.write_text(content)
        return milestones_file

    @staticmethod
    def create_execution_file(goal_dir: Path, content: str = None) -> Path:
        """Create an execution.md file in goal directory."""
        execution_file = goal_dir / "execution.md"
        if content is None:
            content = "# Execution Plan\n\n## Phase 1\n- Activity 1"
        execution_file.write_text(content)
        return execution_file

    @staticmethod
    def assert_goal_structure(goal_dir: Path):
        """Assert that goal directory has all required files."""
        assert (goal_dir / "goal.md").exists(), "goal.md missing"
        assert (goal_dir / "strategies.md").exists(), "strategies.md missing"
        assert (goal_dir / "milestones.md").exists(), "milestones.md missing"
        assert (goal_dir / "execution.md").exists(), "execution.md missing"


@pytest.fixture
def test_helpers():
    """Provide test helper methods."""
    return TestHelpers()
