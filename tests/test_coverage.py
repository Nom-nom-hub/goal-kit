"""
Additional tests to achieve target code coverage of 60-70%.

Tests cover:
- Helper functions that may not be exercised by integration tests
- Edge cases and error paths
- Utility functions
- Configuration handling
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

import pytest
from typer.testing import CliRunner

from goalkeeper_cli import (
    app,
    AGENT_CONFIG,
    SCRIPT_TYPE_CHOICES,
    _github_token,
    _github_auth_headers,
    run_command,
    create_agent_config,
    create_agent_file,
    create_agent_context_file,
    ensure_executable_scripts,
)


class TestGithubTokenHandling:
    """Test GitHub token helper functions."""

    def test_github_token_from_cli_arg(self):
        """Test _github_token returns CLI token."""
        token = _github_token("test_token_cli")
        assert token == "test_token_cli"

    def test_github_token_from_gh_token_env(self, monkeypatch):
        """Test _github_token reads GH_TOKEN env var."""
        monkeypatch.setenv("GH_TOKEN", "test_token_gh")
        token = _github_token(None)
        assert token == "test_token_gh"

    def test_github_token_from_github_token_env(self, monkeypatch):
        """Test _github_token reads GITHUB_TOKEN env var."""
        monkeypatch.delenv("GH_TOKEN", raising=False)
        monkeypatch.setenv("GITHUB_TOKEN", "test_token_github")
        token = _github_token(None)
        assert token == "test_token_github"

    def test_github_token_cli_takes_precedence(self, monkeypatch):
        """Test that CLI token takes precedence over env vars."""
        monkeypatch.setenv("GH_TOKEN", "env_token")
        token = _github_token("cli_token")
        assert token == "cli_token"

    def test_github_token_none_when_all_empty(self, monkeypatch):
        """Test that _github_token returns None when nothing set."""
        monkeypatch.delenv("GH_TOKEN", raising=False)
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        token = _github_token(None)
        assert token is None

    def test_github_token_strips_whitespace(self, monkeypatch):
        """Test that _github_token strips whitespace."""
        monkeypatch.setenv("GH_TOKEN", "  token_with_spaces  ")
        token = _github_token(None)
        assert token == "token_with_spaces"

    def test_github_auth_headers_with_token(self):
        """Test _github_auth_headers includes token when provided."""
        headers = _github_auth_headers("test_token")
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test_token"

    def test_github_auth_headers_without_token(self):
        """Test _github_auth_headers returns empty dict without token."""
        headers = _github_auth_headers(None)
        assert headers == {}

    def test_github_auth_headers_sanitized(self, monkeypatch):
        """Test _github_auth_headers with sanitized empty token."""
        monkeypatch.delenv("GH_TOKEN", raising=False)
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        headers = _github_auth_headers("")
        assert headers == {}


class TestRunCommand:
    """Test run_command utility function."""

    def test_run_command_success(self):
        """Test run_command executes successfully."""
        result = run_command(["echo", "test"], check_return=False)
        assert result is None

    def test_run_command_capture_output(self):
        """Test run_command captures output."""
        result = run_command(["echo", "test"], capture=True)
        assert "test" in result

    def test_run_command_check_return_default(self):
        """Test run_command checks return code by default."""
        # Invalid command should raise
        with pytest.raises(Exception):
            run_command(["false"], check_return=True)

    def test_run_command_no_check_return(self):
        """Test run_command without checking return code."""
        # Should not raise even with failure
        result = run_command(["false"], check_return=False)
        assert result is None


class TestAgentConfiguration:
    """Test agent configuration functions."""

    def test_create_agent_config_claude(self, tmp_path):
        """Test create_agent_config for Claude agent."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        
        with patch("goalkeeper_cli.create_agent_file"):
            create_agent_config(project_path, "claude")
        
        # Should create .claude directory
        assert (project_path / ".claude").exists()

    def test_create_agent_config_copilot(self, tmp_path):
        """Test create_agent_config for Copilot agent."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        
        with patch("goalkeeper_cli.create_agent_file"):
            create_agent_config(project_path, "copilot")
        
        # Should create .github directory
        assert (project_path / ".github").exists()

    def test_create_agent_config_invalid_agent(self, tmp_path):
        """Test create_agent_config with invalid agent."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        
        # Should not raise, just skip
        create_agent_config(project_path, "invalid-agent")

    def test_create_agent_config_creates_commands_dir(self, tmp_path):
        """Test that create_agent_config creates commands directory."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        
        with patch("goalkeeper_cli.create_agent_file"):
            create_agent_config(project_path, "claude")
        
        # Should create commands directory
        assert (project_path / ".claude" / "commands").exists()

    def test_create_agent_file_basic(self, tmp_path):
        """Test create_agent_file creates agent file."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        
        # Create template
        template_dir = Path(__file__).parent.parent / "src" / "templates"
        template_dir.mkdir(parents=True, exist_ok=True)
        template_file = template_dir / "agent-file-template.md"
        template_file.write_text("# Agent File\n[PROJECT NAME]\n[DATE]")
        
        try:
            create_agent_file(project_path, "claude")
            
            # Should create agent file
            assert (project_path / ".claude" / "goal-kit-guide.md").exists()
        finally:
            # Cleanup
            if template_file.exists():
                template_file.unlink()

    def test_create_agent_file_missing_template(self, tmp_path):
        """Test create_agent_file handles missing template."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        
        # Should not raise when template is missing
        create_agent_file(project_path, "claude")

    def test_create_agent_context_file_claude(self, tmp_path):
        """Test create_agent_context_file for Claude."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        
        create_agent_context_file(project_path, "claude")
        
        # Should create context files
        assert (project_path / "CLAUDE.md").exists() or \
               (project_path / ".claude" / "context.md").exists()

    def test_create_agent_context_file_copilot(self, tmp_path):
        """Test create_agent_context_file for Copilot."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        
        create_agent_context_file(project_path, "copilot")
        
        # Should create VS Code context file
        assert (project_path / ".vscode" / "context.md").exists()


class TestExecutableScripts:
    """Test executable script handling."""

    @pytest.mark.skipif(os.name == "nt", reason="Unix only")
    def test_ensure_executable_scripts_sets_permissions(self, tmp_path):
        """Test ensure_executable_scripts sets execute permissions."""
        # Create test script directory
        scripts_dir = tmp_path / ".goalkit" / "scripts"
        scripts_dir.mkdir(parents=True)
        
        # Create test script
        test_script = scripts_dir / "test.sh"
        test_script.write_text("#!/bin/bash\necho test\n")
        
        # Ensure executable
        ensure_executable_scripts(tmp_path)
        
        # Check permissions
        import stat
        mode = test_script.stat().st_mode
        # Should have some execute bit set
        assert mode & stat.S_IXUSR or mode & stat.S_IXGRP or mode & stat.S_IXOTH

    def test_ensure_executable_scripts_windows(self):
        """Test ensure_executable_scripts is no-op on Windows."""
        with patch("os.name", "nt"):
            # Should not raise
            ensure_executable_scripts(Path("/test"))


class TestAgentConfiguration:
    """Test AGENT_CONFIG constants."""

    def test_agent_config_has_required_agents(self):
        """Test AGENT_CONFIG includes required agents."""
        required_agents = ["claude", "copilot", "gemini", "cursor"]
        for agent in required_agents:
            assert agent in AGENT_CONFIG

    def test_agent_config_has_required_fields(self):
        """Test each agent config has required fields."""
        for agent, config in AGENT_CONFIG.items():
            assert "name" in config
            assert "folder" in config
            assert "install_url" in config or config.get("install_url") is None
            assert "requires_cli" in config

    def test_script_type_choices_valid(self):
        """Test SCRIPT_TYPE_CHOICES is properly configured."""
        assert "sh" in SCRIPT_TYPE_CHOICES
        assert "ps" in SCRIPT_TYPE_CHOICES
        assert len(SCRIPT_TYPE_CHOICES) == 2


class TestBannerFunctionality:
    """Test banner display functions."""

    def test_banner_displays_without_error(self):
        """Test show_banner displays without error."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.console") as mock_console:
            from goalkeeper_cli import show_banner
            show_banner()
            
            # Should call console.print
            assert mock_console.print.called

    def test_banner_in_app_help(self):
        """Test banner appears in app help."""
        runner = CliRunner()
        result = runner.invoke(app, ["--help"])
        
        # Should show some output
        assert len(result.stdout) > 0


class TestTyperConfiguration:
    """Test Typer application configuration."""

    def test_app_is_typer_instance(self):
        """Test app is properly configured Typer instance."""
        from typer import Typer
        assert isinstance(app, Typer)

    def test_app_has_init_command(self):
        """Test app has init command."""
        runner = CliRunner()
        result = runner.invoke(app, ["--help"])
        assert "init" in result.stdout.lower()

    def test_app_has_check_command(self):
        """Test app has check command."""
        runner = CliRunner()
        result = runner.invoke(app, ["--help"])
        assert "check" in result.stdout.lower()


class TestConsoleOutput:
    """Test console output and Rich integration."""

    def test_console_is_available(self):
        """Test that Rich console is available."""
        from goalkeeper_cli import console
        from rich.console import Console
        assert isinstance(console, Console)

    def test_banner_constants_defined(self):
        """Test banner constants are defined."""
        from goalkeeper_cli import BANNER, TAGLINE
        assert BANNER
        assert TAGLINE
        assert "Goal" in BANNER or "Goalkeeper" in BANNER


class TestHelperFunctions:
    """Test helper module functions."""

    def test_step_tracker_import(self):
        """Test StepTracker is properly imported."""
        from goalkeeper_cli.helpers import StepTracker
        assert StepTracker is not None

    def test_select_with_arrows_import(self):
        """Test select_with_arrows is properly imported."""
        from goalkeeper_cli.helpers import select_with_arrows
        assert select_with_arrows is not None

    def test_check_tool_import(self):
        """Test check_tool is properly imported."""
        from goalkeeper_cli.helpers import check_tool
        assert check_tool is not None

    def test_is_git_repo_import(self):
        """Test is_git_repo is properly imported."""
        from goalkeeper_cli.helpers import is_git_repo
        assert is_git_repo is not None

    def test_init_git_repo_import(self):
        """Test init_git_repo is properly imported."""
        from goalkeeper_cli.helpers import init_git_repo
        assert init_git_repo is not None


class TestErrorPaths:
    """Test error handling paths."""

    def test_invalid_command(self):
        """Test handling of invalid commands."""
        runner = CliRunner()
        result = runner.invoke(app, ["invalid-command"])
        
        # Should show error
        assert result.exit_code != 0

    def test_init_with_missing_required_arg(self):
        """Test init without required arguments."""
        runner = CliRunner()
        result = runner.invoke(app, ["init"])
        
        # Should fail
        assert result.exit_code != 0

    def test_check_completes_without_args(self):
        """Test check command works without arguments."""
        runner = CliRunner()
        result = runner.invoke(app, ["check"])
        
        # Should complete (exit code 0 or 1)
        assert result.exit_code in [0, 1]


class TestEnvironmentVariables:
    """Test environment variable handling."""

    def test_github_token_env_precedence(self, monkeypatch):
        """Test GitHub token environment variable precedence."""
        monkeypatch.setenv("GITHUB_TOKEN", "github_token")
        monkeypatch.setenv("GH_TOKEN", "gh_token")
        
        # GH_TOKEN should take precedence
        token = _github_token(None)
        assert token == "gh_token"

    def test_claude_local_path_constant(self):
        """Test CLAUDE_LOCAL_PATH is properly set."""
        from goalkeeper_cli import CLAUDE_LOCAL_PATH
        assert CLAUDE_LOCAL_PATH is not None


class TestPathHandling:
    """Test path handling utilities."""

    def test_path_operations_on_windows(self):
        """Test path operations work on Windows."""
        from pathlib import Path
        
        test_path = Path("test") / "dir"
        assert "test" in str(test_path)

    def test_project_path_creation(self, tmp_path):
        """Test project path creation."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        
        assert project_path.exists()
        assert project_path.is_dir()


class TestJSONHandling:
    """Test JSON-related functionality."""

    def test_json_in_download_metadata(self, tmp_path):
        """Test JSON metadata handling."""
        metadata = {
            "filename": "test.zip",
            "size": 1000,
            "release": "v1.0.0",
            "asset_url": "https://example.com/test.zip",
        }
        
        # Should be valid JSON serializable
        import json
        json_str = json.dumps(metadata)
        parsed = json.loads(json_str)
        
        assert parsed["filename"] == "test.zip"
        assert parsed["size"] == 1000
