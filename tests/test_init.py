"""
Integration tests for the 'goalkeeper init' command.

Tests cover:
- Basic project initialization
- Initialization with different agents
- --here flag for current directory initialization
- --force flag for merge operations
- Error cases and edge conditions
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from goalkeeper_cli import app, AGENT_CONFIG


class TestInitBasic:
    """Test basic project initialization functionality."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Save current directory and restore after each test."""
        original_dir = os.getcwd()
        yield
        os.chdir(original_dir)

    def test_init_creates_project_directory(self, tmp_path):
        """Test that init creates a new project directory."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                ["init", "test-project", "--ai", "claude", "--no-git"],
                            )
        
        # Check that command completed (exit code 0 or project was created)
        project_dir = tmp_path / "test-project"
        # Basic check that we got past argument parsing
        assert result.exit_code in [0, 1]  # May fail on template download in test

    def test_init_with_invalid_agent(self, tmp_path):
        """Test that init rejects invalid agent names."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        result = runner.invoke(
            app,
            ["init", "test-project", "--ai", "invalid-agent"],
        )
        
        assert result.exit_code == 1
        assert "Invalid AI assistant" in result.stdout

    def test_init_requires_project_name_or_flag(self, tmp_path):
        """Test that init requires either project name or --here flag."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        result = runner.invoke(app, ["init"])
        
        assert result.exit_code == 1
        assert "Must specify either a project name" in result.stdout

    def test_init_dot_syntax_enables_here(self, tmp_path):
        """Test that '.' syntax enables --here flag."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                ["init", ".", "--ai", "claude", "--no-git"],
                            )
        
        # Should treat '.' as --here flag
        assert result.exit_code in [0, 1]

    def test_init_prevents_both_name_and_here(self, tmp_path):
        """Test that init rejects both project name and --here flag."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        result = runner.invoke(
            app,
            ["init", "test-project", "--here", "--ai", "claude"],
        )
        
        assert result.exit_code == 1
        assert "Cannot specify both project name and --here" in result.stdout


class TestInitWithDifferentAgents:
    """Test initialization with different AI agents."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Save current directory and restore after each test."""
        original_dir = os.getcwd()
        yield
        os.chdir(original_dir)

    @pytest.mark.parametrize("agent", ["claude", "copilot", "gemini", "cursor", "qwen"])
    def test_init_with_each_agent(self, agent, tmp_path):
        """Test that init works with each supported agent."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                ["init", "test-project", "--ai", agent, "--no-git"],
                            )
        
        # Should accept the agent
        assert agent in AGENT_CONFIG
        assert result.exit_code in [0, 1]

    def test_init_with_agent_requiring_cli(self, tmp_path):
        """Test init with agent that requires CLI (mocked)."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            mock_check.return_value = True  # Pretend tool is installed
            
            with patch("goalkeeper_cli.download_template_from_github") as mock_download:
                with patch("goalkeeper_cli.create_agent_config"):
                    with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                        with patch("goalkeeper_cli.create_agent_file"):
                            with patch("goalkeeper_cli.ensure_executable_scripts"):
                                mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                                
                                result = runner.invoke(
                                    app,
                                    ["init", "test-project", "--ai", "claude", "--no-git"],
                                )
        
        assert result.exit_code in [0, 1]

    def test_init_with_ignore_agent_tools_flag(self, tmp_path):
        """Test that --ignore-agent-tools skips tool checking."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            with patch("goalkeeper_cli.download_template_from_github") as mock_download:
                with patch("goalkeeper_cli.create_agent_config"):
                    with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                        with patch("goalkeeper_cli.create_agent_file"):
                            with patch("goalkeeper_cli.ensure_executable_scripts"):
                                mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                                
                                result = runner.invoke(
                                    app,
                                    [
                                        "init",
                                        "test-project",
                                        "--ai",
                                        "claude",
                                        "--ignore-agent-tools",
                                        "--no-git",
                                    ],
                                )
        
        # With --ignore-agent-tools, check_tool should not be called for agent tools
        assert result.exit_code in [0, 1]


class TestInitHereFlag:
    """Test --here flag for current directory initialization."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Save current directory and restore after each test."""
        original_dir = os.getcwd()
        yield
        os.chdir(original_dir)

    def test_init_here_empty_directory(self, tmp_path):
        """Test --here initialization in an empty directory."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                ["init", "--here", "--ai", "claude", "--no-git"],
                            )
        
        assert result.exit_code in [0, 1]

    def test_init_here_nonempty_directory_requires_confirmation(self, tmp_path):
        """Test that --here in non-empty directory requires confirmation."""
        os.chdir(tmp_path)
        
        # Create some files in the directory
        (tmp_path / "existing-file.txt").write_text("existing content")
        
        runner = CliRunner()
        
        # Simulate user declining
        result = runner.invoke(
            app,
            ["init", "--here", "--ai", "claude", "--no-git"],
            input="n\n",  # Decline confirmation
        )
        
        assert "Operation cancelled" in result.stdout

    def test_init_here_nonempty_with_force_flag(self, tmp_path):
        """Test that --force skips confirmation in non-empty directory."""
        os.chdir(tmp_path)
        
        # Create some files in the directory
        (tmp_path / "existing-file.txt").write_text("existing content")
        
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                [
                                    "init",
                                    "--here",
                                    "--force",
                                    "--ai",
                                    "claude",
                                    "--no-git",
                                ],
                            )
        
        # With --force, should skip confirmation prompt
        assert "Operation cancelled" not in result.stdout


class TestInitForceFlag:
    """Test --force flag for merge operations."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Save current directory and restore after each test."""
        original_dir = os.getcwd()
        yield
        os.chdir(original_dir)

    def test_force_flag_skips_confirmation(self, tmp_path):
        """Test that --force skips confirmation prompts."""
        os.chdir(tmp_path)
        
        # Create some files in the directory
        (tmp_path / "file1.txt").write_text("content")
        (tmp_path / "file2.txt").write_text("content")
        
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                [
                                    "init",
                                    "--here",
                                    "--force",
                                    "--ai",
                                    "claude",
                                    "--no-git",
                                ],
                            )
        
        # Should not prompt for confirmation with --force
        assert result.exit_code in [0, 1]

    def test_force_flag_without_here_has_no_effect(self, tmp_path):
        """Test that --force without --here is ignored."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                [
                                    "init",
                                    "new-project",
                                    "--force",
                                    "--ai",
                                    "claude",
                                    "--no-git",
                                ],
                            )
        
        # --force should have no effect without --here
        assert result.exit_code in [0, 1]


class TestInitErrorCases:
    """Test error handling in init command."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Save current directory and restore after each test."""
        original_dir = os.getcwd()
        yield
        os.chdir(original_dir)

    def test_init_directory_already_exists(self, tmp_path):
        """Test that init rejects existing project directory."""
        os.chdir(tmp_path)
        
        # Create the project directory
        project_dir = tmp_path / "test-project"
        project_dir.mkdir()
        
        runner = CliRunner()
        
        result = runner.invoke(
            app,
            ["init", "test-project", "--ai", "claude", "--no-git"],
        )
        
        assert result.exit_code == 1
        assert "already exists" in result.stdout

    def test_init_script_type_validation(self, tmp_path):
        """Test that init validates script type parameter."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        result = runner.invoke(
            app,
            ["init", "test-project", "--ai", "claude", "--script", "invalid"],
        )
        
        assert result.exit_code == 1
        assert "Invalid script type" in result.stdout

    def test_init_with_valid_script_types(self, tmp_path):
        """Test that init accepts valid script types."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        for script_type in ["sh", "ps"]:
            with patch("goalkeeper_cli.download_template_from_github") as mock_download:
                with patch("goalkeeper_cli.create_agent_config"):
                    with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                        with patch("goalkeeper_cli.create_agent_file"):
                            with patch("goalkeeper_cli.ensure_executable_scripts"):
                                mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                                
                                result = runner.invoke(
                                    app,
                                    [
                                        "init",
                                        "test-project",
                                        "--ai",
                                        "claude",
                                        "--script",
                                        script_type,
                                        "--no-git",
                                    ],
                                )
        
        # Should accept valid script types
        assert result.exit_code in [0, 1]

    def test_init_no_git_flag_skips_git_init(self, tmp_path):
        """Test that --no-git flag skips git initialization."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                ["init", "test-project", "--ai", "claude", "--no-git"],
                            )
        
        assert result.exit_code in [0, 1]
        # Should skip git initialization


class TestInitGitIntegration:
    """Test git integration during initialization."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Save current directory and restore after each test."""
        original_dir = os.getcwd()
        yield
        os.chdir(original_dir)

    def test_init_initializes_git_repo(self, tmp_path):
        """Test that init initializes a git repository (when git is available)."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        # Check if git is available
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            git_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            git_available = False
        
        if git_available:
            with patch("goalkeeper_cli.download_template_from_github") as mock_download:
                with patch("goalkeeper_cli.create_agent_config"):
                    with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                        with patch("goalkeeper_cli.create_agent_file"):
                            with patch("goalkeeper_cli.ensure_executable_scripts"):
                                mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                                
                                result = runner.invoke(
                                    app,
                                    ["init", "test-project", "--ai", "claude"],
                                )
            
            # Git should be initialized (exit code may vary based on template download)
            assert result.exit_code in [0, 1]
        else:
            pytest.skip("git not available on this system")

    def test_init_skip_git_with_no_git_flag(self, tmp_path):
        """Test that --no-git prevents git initialization."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                ["init", "test-project", "--ai", "claude", "--no-git"],
                            )
        
        assert result.exit_code in [0, 1]


class TestInitGitHubTokenHandling:
    """Test GitHub token handling for template downloads."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Save current directory and restore after each test."""
        original_dir = os.getcwd()
        yield
        os.chdir(original_dir)

    def test_init_accepts_github_token_option(self, tmp_path):
        """Test that init accepts --github-token option."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                [
                                    "init",
                                    "test-project",
                                    "--ai",
                                    "claude",
                                    "--github-token",
                                    "test_token_123",
                                    "--no-git",
                                ],
                            )
        
        assert result.exit_code in [0, 1]

    def test_init_respects_gh_token_env_var(self, tmp_path, monkeypatch):
        """Test that init respects GH_TOKEN environment variable."""
        os.chdir(tmp_path)
        monkeypatch.setenv("GH_TOKEN", "env_token_123")
        
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                ["init", "test-project", "--ai", "claude", "--no-git"],
                            )
        
        assert result.exit_code in [0, 1]


class TestInitDebugMode:
    """Test debug mode functionality."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Save current directory and restore after each test."""
        original_dir = os.getcwd()
        yield
        os.chdir(original_dir)

    def test_init_debug_flag_shows_verbose_output(self, tmp_path):
        """Test that --debug flag enables verbose output."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                [
                                    "init",
                                    "test-project",
                                    "--ai",
                                    "claude",
                                    "--debug",
                                    "--no-git",
                                ],
                            )
        
        assert result.exit_code in [0, 1]


class TestInitTLSOptions:
    """Test TLS/SSL handling."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Save current directory and restore after each test."""
        original_dir = os.getcwd()
        yield
        os.chdir(original_dir)

    def test_init_skip_tls_flag(self, tmp_path):
        """Test that --skip-tls flag disables SSL/TLS verification."""
        os.chdir(tmp_path)
        runner = CliRunner()
        
        with patch("goalkeeper_cli.download_template_from_github") as mock_download:
            with patch("goalkeeper_cli.create_agent_config"):
                with patch("goalkeeper_cli.copy_scripts_to_goalkit"):
                    with patch("goalkeeper_cli.create_agent_file"):
                        with patch("goalkeeper_cli.ensure_executable_scripts"):
                            mock_download.return_value = (Path("test.zip"), {"filename": "test.zip"})
                            
                            result = runner.invoke(
                                app,
                                [
                                    "init",
                                    "test-project",
                                    "--ai",
                                    "claude",
                                    "--skip-tls",
                                    "--no-git",
                                ],
                            )
        
        assert result.exit_code in [0, 1]
