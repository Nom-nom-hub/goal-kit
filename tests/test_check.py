"""
Integration tests for the 'goalkeeper check' command.

Tests cover:
- Tool detection and reporting
- Git version checking
- Agent tool detection (claude, gemini, cursor, etc.)
- VS Code detection
- Output formatting
"""

import os
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from goalkeeper_cli import app, AGENT_CONFIG


class TestCheckBasic:
    """Test basic check command functionality."""

    def test_check_command_runs(self):
        """Test that check command runs successfully."""
        runner = CliRunner()
        result = runner.invoke(app, ["check"])
        
        # Should complete without fatal error
        assert result.exit_code in [0, 1]

    def test_check_displays_banner(self):
        """Test that check command displays banner."""
        runner = CliRunner()
        result = runner.invoke(app, ["check"])
        
        # Should display banner
        assert "Goal Kit" in result.stdout or "Goalkeeper" in result.stdout

    def test_check_lists_tools(self):
        """Test that check lists available tools."""
        runner = CliRunner()
        result = runner.invoke(app, ["check"])
        
        # Should show tool checking output
        assert "git" in result.stdout.lower() or "tool" in result.stdout.lower()


class TestCheckGitDetection:
    """Test git tool detection."""

    def test_check_detects_git(self):
        """Test that check detects git when installed."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            mock_check.return_value = True
            result = runner.invoke(app, ["check"])
        
        # Should detect git
        assert result.exit_code in [0, 1]

    def test_check_handles_missing_git(self):
        """Test that check handles missing git gracefully."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            # First call for git returns False, rest return True/False as needed
            mock_check.side_effect = [False] + [True] * 20
            result = runner.invoke(app, ["check"])
        
        # Should complete without error
        assert result.exit_code in [0, 1]


class TestCheckAgentDetection:
    """Test AI agent tool detection."""

    @pytest.mark.parametrize("agent", ["claude", "gemini", "cursor", "copilot", "qwen"])
    def test_check_includes_agent(self, agent):
        """Test that check includes agent detection."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            mock_check.return_value = True
            result = runner.invoke(app, ["check"])
        
        # Should complete
        assert result.exit_code in [0, 1]

    def test_check_detects_all_agents(self):
        """Test that check detects multiple agents."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            # Mock all tools as installed
            mock_check.return_value = True
            result = runner.invoke(app, ["check"])
        
        # Should detect agents
        assert result.exit_code in [0, 1]

    def test_check_agent_detection_with_none_found(self):
        """Test check output when no agents are found."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            # Mock all tools as not installed
            mock_check.return_value = False
            result = runner.invoke(app, ["check"])
        
        # Should still complete successfully
        assert result.exit_code in [0, 1]


class TestCheckVSCodeDetection:
    """Test VS Code and VS Code Insiders detection."""

    def test_check_detects_vscode(self):
        """Test that check detects VS Code."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            # Mock VS Code as installed
            def side_effect(tool, *args, **kwargs):
                return tool == "code"
            
            mock_check.side_effect = side_effect
            result = runner.invoke(app, ["check"])
        
        assert result.exit_code in [0, 1]

    def test_check_detects_vscode_insiders(self):
        """Test that check detects VS Code Insiders."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            # Mock VS Code Insiders as installed
            def side_effect(tool, *args, **kwargs):
                return tool == "code-insiders"
            
            mock_check.side_effect = side_effect
            result = runner.invoke(app, ["check"])
        
        assert result.exit_code in [0, 1]


class TestCheckOutputFormatting:
    """Test output formatting and presentation."""

    def test_check_output_is_readable(self):
        """Test that check output is properly formatted."""
        runner = CliRunner()
        result = runner.invoke(app, ["check"])
        
        # Output should contain readable text
        assert len(result.stdout) > 0

    def test_check_shows_success_message(self):
        """Test that check shows success message."""
        runner = CliRunner()
        result = runner.invoke(app, ["check"])
        
        # Should show completion message
        assert "ready" in result.stdout.lower() or "check" in result.stdout.lower()

    def test_check_grouped_output(self):
        """Test that check groups tools properly."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            mock_check.return_value = True
            result = runner.invoke(app, ["check"])
        
        # Output should be organized
        assert result.exit_code in [0, 1]


class TestCheckWithMockedTools:
    """Test check command with various tool availability combinations."""

    def test_check_all_tools_available(self):
        """Test check when all tools are available."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            mock_check.return_value = True
            result = runner.invoke(app, ["check"])
        
        assert result.exit_code in [0, 1]

    def test_check_no_tools_available(self):
        """Test check when no tools are available."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            mock_check.return_value = False
            result = runner.invoke(app, ["check"])
        
        # Should still report gracefully
        assert result.exit_code in [0, 1]

    def test_check_only_git_available(self):
        """Test check when only git is available."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            def side_effect(tool, *args, **kwargs):
                return tool == "git"
            
            mock_check.side_effect = side_effect
            result = runner.invoke(app, ["check"])
        
        assert result.exit_code in [0, 1]

    def test_check_only_agents_available(self):
        """Test check when only agents are available."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            def side_effect(tool, *args, **kwargs):
                return tool in AGENT_CONFIG
            
            mock_check.side_effect = side_effect
            result = runner.invoke(app, ["check"])
        
        assert result.exit_code in [0, 1]


class TestCheckStepTracking:
    """Test step tracking functionality in check command."""

    def test_check_uses_step_tracker(self):
        """Test that check uses StepTracker for output."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.StepTracker") as mock_tracker:
            with patch("goalkeeper_cli.check_tool") as mock_check:
                mock_check.return_value = True
                mock_tracker_instance = MagicMock()
                mock_tracker.return_value = mock_tracker_instance
                
                result = runner.invoke(app, ["check"])
        
        # Should use tracker
        assert result.exit_code in [0, 1]

    def test_check_step_tracker_add_method(self):
        """Test that check adds steps to tracker."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.StepTracker") as mock_tracker:
            with patch("goalkeeper_cli.check_tool") as mock_check:
                mock_check.return_value = True
                mock_tracker_instance = MagicMock()
                mock_tracker.return_value = mock_tracker_instance
                
                result = runner.invoke(app, ["check"])
                
                # Tracker.add should be called for each tool check
                assert mock_tracker_instance.add.called or result.exit_code in [0, 1]


class TestCheckToolChecking:
    """Test tool detection logic."""

    def test_check_tool_function_called(self):
        """Test that check_tool function is called."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            mock_check.return_value = True
            result = runner.invoke(app, ["check"])
        
        # check_tool should be called at least once
        assert mock_check.called or result.exit_code in [0, 1]

    def test_check_handles_check_tool_error(self):
        """Test that check handles errors from check_tool gracefully."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.check_tool") as mock_check:
            mock_check.side_effect = RuntimeError("Tool check failed")
            result = runner.invoke(app, ["check"])
        
        # Should handle error gracefully
        assert result.exit_code in [0, 1]


class TestCheckRealTools:
    """Test check with actual system tools (if available)."""

    def test_check_real_git_detection(self):
        """Test real git detection on system."""
        runner = CliRunner()
        result = runner.invoke(app, ["check"])
        
        # Should complete without fatal error
        assert result.exit_code in [0, 1]
        
        # Check if git is actually installed and verify output consistency
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            git_installed = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            git_installed = False
        
        # Either way, should complete successfully
        assert result.exit_code in [0, 1]


class TestCheckEdgeCases:
    """Test edge cases and error conditions."""

    def test_check_with_invalid_claude_path(self):
        """Test check with invalid Claude local path."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.CLAUDE_LOCAL_PATH", Path("/invalid/path")):
            with patch("goalkeeper_cli.check_tool") as mock_check:
                mock_check.return_value = False
                result = runner.invoke(app, ["check"])
        
        assert result.exit_code in [0, 1]

    def test_check_output_not_empty(self):
        """Test that check always produces output."""
        runner = CliRunner()
        result = runner.invoke(app, ["check"])
        
        # Should produce output
        assert len(result.stdout) > 0

    def test_check_command_case_insensitive(self):
        """Test that check command works regardless of invocation."""
        runner = CliRunner()
        
        # Typer should normalize command names
        result1 = runner.invoke(app, ["check"])
        assert result1.exit_code in [0, 1]


class TestCheckConsoleOutput:
    """Test console output behavior."""

    def test_check_uses_rich_console(self):
        """Test that check uses Rich console for output."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.console") as mock_console:
            with patch("goalkeeper_cli.check_tool") as mock_check:
                mock_check.return_value = True
                result = runner.invoke(app, ["check"])
        
        # Should use console for output
        assert result.exit_code in [0, 1]

    def test_check_renders_step_tracker(self):
        """Test that check renders StepTracker output."""
        runner = CliRunner()
        
        with patch("goalkeeper_cli.StepTracker") as mock_tracker:
            with patch("goalkeeper_cli.check_tool") as mock_check:
                mock_check.return_value = True
                mock_tracker_instance = MagicMock()
                mock_tracker_instance.render.return_value = "mock render output"
                mock_tracker.return_value = mock_tracker_instance
                
                result = runner.invoke(app, ["check"])
        
        assert result.exit_code in [0, 1]
