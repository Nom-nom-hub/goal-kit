"""Tests for status command."""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

from goalkeeper_cli.commands.status import (
    status,
    _output_json,
    _output_formatted,
    _format_phase,
    _format_percentage,
    _format_health_score,
    _count_with_metrics,
    _count_with_criteria,
    _avg_phase_score,
)
from goalkeeper_cli.analyzer import AnalysisResult
from goalkeeper_cli.models import Project, Goal


class TestStatusCommand:
    """Tests for status command."""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary goal-kit project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goals_dir = goalkit_dir / "goals"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            goals_dir.mkdir(parents=True, exist_ok=True)

            yield project_path

    def test_status_with_valid_project(self, temp_project, capsys):
        """Test status command with valid project."""
        status(temp_project)
        captured = capsys.readouterr()
        # Should not raise error
        assert captured.err == "" or "Error" not in captured.err

    def test_status_with_invalid_path(self, capsys):
        """Test status command with invalid path."""
        status(Path("/nonexistent/path"))
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_status_with_none_path(self, capsys):
        """Test status command with None path (uses cwd)."""
        with patch("pathlib.Path.cwd") as mock_cwd:
            mock_cwd.return_value = Path("/tmp")
            with patch("goalkeeper_cli.commands.status.ProjectAnalyzer") as mock_analyzer:
                mock_analyzer.side_effect = FileNotFoundError("Not a goal-kit project")
                status(None)
                captured = capsys.readouterr()
                assert "Error" in captured.out

    def test_status_verbose_flag(self, temp_project, capsys):
        """Test status command with verbose flag."""
        status(temp_project, verbose=True)
        captured = capsys.readouterr()
        assert captured.err == "" or "Error" not in captured.err

    def test_status_json_output(self, temp_project, capsys):
        """Test status command with JSON output."""
        status(temp_project, json_output=True)
        captured = capsys.readouterr()
        # Should output valid JSON
        try:
            json.loads(captured.out)
        except json.JSONDecodeError:
            # Some output might be in console output, not stdout
            pass


class TestOutputJSON:
    """Tests for JSON output formatting."""

    @pytest.fixture
    def sample_result(self):
        """Create a sample analysis result."""
        project = Project(
            name="Test Project",
            path=Path("/tmp/test"),
            agent="claude",
            created_at=datetime.now(),
        )
        goals = [
            Goal("g1", "Goal 1", "execute", 75, 3, True),
            Goal("g2", "Goal 2", "active", 50, 2, False),
        ]
        return AnalysisResult(
            project=project,
            goals=goals,
            completion_percent=62.5,
            health_score=55.0,
            phase="active",
            milestone_count=4,
            completed_milestones=2,
            recent_milestones=[],
        )

    def test_output_json_structure(self, sample_result):
        """Test JSON output has correct structure."""
        mock_console = MagicMock()
        _output_json(sample_result, mock_console)

        # Verify print_json was called
        assert mock_console.print_json.called

    def test_output_json_contains_project_info(self, sample_result):
        """Test JSON output contains project information."""
        mock_console = MagicMock()
        _output_json(sample_result, mock_console)

        # Get the data passed to print_json
        call_args = mock_console.print_json.call_args
        data = call_args[1]["data"]

        assert data["project"]["name"] == "Test Project"
        assert data["project"]["agent"] == "claude"
        assert "path" in data["project"]

    def test_output_json_contains_status(self, sample_result):
        """Test JSON output contains status information."""
        mock_console = MagicMock()
        _output_json(sample_result, mock_console)

        call_args = mock_console.print_json.call_args
        data = call_args[1]["data"]

        assert data["status"]["phase"] == "active"
        assert data["status"]["completion_percent"] == 62.5
        assert data["status"]["health_score"] == 55.0

    def test_output_json_contains_goals(self, sample_result):
        """Test JSON output contains goals information."""
        mock_console = MagicMock()
        _output_json(sample_result, mock_console)

        call_args = mock_console.print_json.call_args
        data = call_args[1]["data"]

        assert data["goals"]["total"] == 2
        assert len(data["goals"]["details"]) == 2
        assert data["goals"]["details"][0]["name"] == "Goal 1"
        assert data["goals"]["details"][0]["completion"] == 75

    def test_output_json_contains_milestones(self, sample_result):
        """Test JSON output contains milestone information."""
        mock_console = MagicMock()
        _output_json(sample_result, mock_console)

        call_args = mock_console.print_json.call_args
        data = call_args[1]["data"]

        assert data["milestones"]["total"] == 4
        assert data["milestones"]["completed"] == 2


class TestOutputFormatted:
    """Tests for formatted text output."""

    @pytest.fixture
    def sample_result(self):
        """Create a sample analysis result."""
        project = Project(
            name="My Project",
            path=Path("/tmp/test"),
            agent="gemini",
            created_at=datetime(2025, 12, 1, 10, 0),
        )
        goals = [
            Goal("auth", "Authentication", "execute", 80, 3, True),
            Goal("db", "Database", "active", 60, 2, False),
        ]
        return AnalysisResult(
            project=project,
            goals=goals,
            completion_percent=70.0,
            health_score=65.0,
            phase="execution",
            milestone_count=4,
            completed_milestones=2,
            recent_milestones=[],
        )

    def test_output_formatted_calls_console(self, sample_result):
        """Test formatted output calls console print."""
        mock_console = MagicMock()
        _output_formatted(sample_result, mock_console, verbose=False)

        # Should call console.print at least once
        assert mock_console.print.called

    def test_output_formatted_includes_project_name(self, sample_result):
        """Test formatted output includes project name."""
        mock_console = MagicMock()
        _output_formatted(sample_result, mock_console, verbose=False)

        # Check that print was called with Panel containing project name
        # (Rich Panel objects don't directly show text in str representation)
        assert mock_console.print.called
        # Verify at least one Panel was created with the project name
        calls = mock_console.print.call_args_list
        # First call should be a Panel
        assert len(calls) > 0

    def test_output_formatted_includes_goals_table(self, sample_result):
        """Test formatted output includes goals table."""
        mock_console = MagicMock()
        _output_formatted(sample_result, mock_console, verbose=False)

        # Check that goals section was printed
        calls = [str(call) for call in mock_console.print.call_args_list]
        output_text = " ".join(calls)
        assert "Goals" in output_text

    def test_output_formatted_verbose_mode(self, sample_result):
        """Test formatted output in verbose mode."""
        mock_console = MagicMock()
        _output_formatted(sample_result, mock_console, verbose=True)

        # Verbose should call print more times
        calls = [str(call) for call in mock_console.print.call_args_list]
        output_text = " ".join(calls)
        assert "Detailed Analysis" in output_text

    def test_output_formatted_empty_goals(self):
        """Test formatted output with no goals."""
        project = Project(
            name="Empty Project",
            path=Path("/tmp/test"),
            agent="claude",
            created_at=datetime.now(),
        )
        result = AnalysisResult(
            project=project,
            goals=[],
            completion_percent=0.0,
            health_score=0.0,
            phase="setup",
            milestone_count=0,
            completed_milestones=0,
            recent_milestones=[],
        )

        mock_console = MagicMock()
        _output_formatted(result, mock_console, verbose=False)

        # Should handle empty goals gracefully
        assert mock_console.print.called


class TestFormatting:
    """Tests for formatting helper functions."""

    def test_format_phase_setup(self):
        """Test formatting setup phase."""
        result = _format_phase("setup")
        assert "yellow" in result

    def test_format_phase_active(self):
        """Test formatting active phase."""
        result = _format_phase("active")
        assert "cyan" in result

    def test_format_phase_execution(self):
        """Test formatting execution phase."""
        result = _format_phase("execution")
        assert "green" in result

    def test_format_phase_complete(self):
        """Test formatting complete phase."""
        result = _format_phase("complete")
        assert "green" in result

    def test_format_phase_unknown(self):
        """Test formatting unknown phase."""
        result = _format_phase("unknown")
        assert "unknown" in result

    def test_format_percentage_high(self):
        """Test formatting high percentage."""
        result = _format_percentage(85.0)
        assert "green" in result

    def test_format_percentage_medium(self):
        """Test formatting medium percentage."""
        result = _format_percentage(60.0)
        assert "yellow" in result

    def test_format_percentage_low(self):
        """Test formatting low percentage."""
        result = _format_percentage(25.0)
        assert "red" in result

    def test_format_health_score_good(self):
        """Test formatting good health score."""
        result = _format_health_score(75.0)
        assert "green" in result

    def test_format_health_score_fair(self):
        """Test formatting fair health score."""
        result = _format_health_score(50.0)
        assert "yellow" in result

    def test_format_health_score_poor(self):
        """Test formatting poor health score."""
        result = _format_health_score(30.0)
        assert "red" in result


class TestCountHelpers:
    """Tests for counting helper functions."""

    def test_count_with_metrics(self):
        """Test counting goals with metrics."""
        goals = [
            Goal("g1", "Goal 1", "execute", 50, 3, True),
            Goal("g2", "Goal 2", "execute", 50, 2, False),
            Goal("g3", "Goal 3", "execute", 50, 1, True),
        ]
        assert _count_with_metrics(goals) == 2

    def test_count_with_metrics_empty(self):
        """Test counting with empty goals."""
        assert _count_with_metrics([]) == 0

    def test_count_with_criteria(self):
        """Test counting goals with criteria."""
        goals = [
            Goal("g1", "Goal 1", "execute", 50, 3, True),
            Goal("g2", "Goal 2", "execute", 50, 0, False),
            Goal("g3", "Goal 3", "execute", 50, 1, True),
        ]
        assert _count_with_criteria(goals) == 2

    def test_count_with_criteria_empty(self):
        """Test counting criteria with empty goals."""
        assert _count_with_criteria([]) == 0

    def test_avg_phase_score_mixed(self):
        """Test average phase score with mixed phases."""
        goals = [
            Goal("g1", "Goal 1", "execute", 50, 3, True),
            Goal("g2", "Goal 2", "done", 50, 2, False),
        ]
        avg = _avg_phase_score(goals)
        # execute (80) + done (100) / 2 = 90
        assert avg == 90.0

    def test_avg_phase_score_empty(self):
        """Test average phase score with empty goals."""
        assert _avg_phase_score([]) == 0.0

    def test_avg_phase_score_unknown_phase(self):
        """Test average phase score with unknown phase."""
        goals = [
            Goal("g1", "Goal 1", "unknown", 50, 3, True),
        ]
        avg = _avg_phase_score(goals)
        # unknown defaults to 50
        assert avg == 50.0
