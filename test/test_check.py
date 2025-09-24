import sys
import os
import subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from goal_kit.cli import main
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
import pytest


def test_check_command_success():
    """Test that the check command runs successfully and produces expected output."""
    runner = CliRunner()
    result = runner.invoke(main, ['check'])
    
    # Should exit successfully
    assert result.exit_code == 0
    
    # Should contain system check messages
    assert "[INFO] Checking system requirements and installed tools..." in result.output
    assert "[INFO] Checking AI agent tools:" in result.output
    assert "[INFO] Python:" in result.output
    assert "[INFO] OS:" in result.output
    
    # Should end with either success or warning message
    assert "[SUCCESS] System check completed!" in result.output or "[WARNING] System check completed with errors." in result.output


@patch('subprocess.run')
def test_check_command_missing_tools(mock_subprocess_run):
    """Test that the check command properly handles missing tools."""
    # Mock subprocess to simulate missing tools
    mock_subprocess_run.side_effect = FileNotFoundError()
    
    runner = CliRunner()
    result = runner.invoke(main, ['check'])
    
    # Should exit successfully even when tools are missing
    assert result.exit_code == 0
    
    # Should contain error messages for missing tools
    assert "[ERROR] Git: Not found" in result.output
    assert "[ERROR] uv: Not found" in result.output
    assert "[WARNING] System check completed with errors." in result.output


@patch('subprocess.run')
def test_check_command_timeout(mock_subprocess_run):
    """Test that the check command handles timeouts gracefully."""
    # Mock subprocess to simulate timeout
    mock_subprocess_run.side_effect = subprocess.TimeoutExpired(cmd=['git', '--version'], timeout=5)
    
    runner = CliRunner()
    result = runner.invoke(main, ['check'])
    
    # Should exit successfully even when commands timeout
    assert result.exit_code == 0
    
    # Should contain timeout error messages
    assert "[ERROR] Git: Not found" in result.output
    assert "[WARNING] System check completed with errors." in result.output


def test_check_command_registered():
    """Test that the check command is properly registered."""
    assert 'check' in main.commands
    assert callable(main.commands['check'])


if __name__ == '__main__':
    # Run the tests
    pytest.main([__file__, '-v'])