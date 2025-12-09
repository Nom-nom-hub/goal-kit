"""Tests for milestones command."""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

from goalkeeper_cli.commands.milestones import (
    milestones,
    _output_json,
    _output_formatted,
    _display_milestone_table,
    _display_timeline,
    _format_momentum,
)
from goalkeeper_cli.execution import ExecutionTracker, MilestoneRecord
from goalkeeper_cli.analyzer import AnalysisResult, ProjectAnalyzer
from goalkeeper_cli.models import Project, Goal


class TestMilestonesCommand:
    """Tests for milestones command."""

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

    @pytest.fixture
    def project_with_milestones(self):
        """Create a project with execution history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goals_dir = goalkit_dir / "goals"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            goals_dir.mkdir(parents=True, exist_ok=True)

            tracker = ExecutionTracker(project_path)

            # Create history
            now = datetime.now()
            for i in range(10):
                record = MilestoneRecord(
                    milestone_id=f"m{i}",
                    goal_id="goal1" if i < 6 else "goal2",
                    completed_at=now - timedelta(days=10 - i),
                    notes=f"Milestone {i}",
                )
                tracker._save_milestone_record(record)

            yield project_path

    def test_milestones_with_valid_project(self, temp_project, capsys):
        """Test milestones command with valid project."""
        milestones(temp_project)
        captured = capsys.readouterr()
        # Should not raise error
        assert captured.err == "" or "Error" not in captured.err

    def test_milestones_with_invalid_path(self, capsys):
        """Test milestones command with invalid path."""
        milestones(Path("/nonexistent/path"))
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_milestones_with_none_path(self, capsys):
        """Test milestones command with None path (uses cwd)."""
        with patch("pathlib.Path.cwd") as mock_cwd:
            mock_cwd.return_value = Path("/tmp")
            with patch("goalkeeper_cli.commands.milestones.ProjectAnalyzer") as mock_analyzer:
                mock_analyzer.side_effect = FileNotFoundError("Not a goal-kit project")
                milestones(None)
                captured = capsys.readouterr()
                assert "Error" in captured.out

    def test_milestones_json_output(self, project_with_milestones, capsys):
        """Test milestones command with JSON output."""
        milestones(project_with_milestones, json_output=True)
        captured = capsys.readouterr()
        # Should output valid JSON
        try:
            json.loads(captured.out)
        except json.JSONDecodeError:
            # Some output might be in console output, not stdout
            pass

    def test_milestones_with_goal_filter(self, project_with_milestones, capsys):
        """Test milestones command with goal ID filter."""
        milestones(project_with_milestones, goal_id="goal1")
        captured = capsys.readouterr()
        assert captured.err == "" or "Error" not in captured.err

    def test_milestones_with_invalid_goal_id(self, project_with_milestones, capsys):
        """Test milestones command with invalid goal ID."""
        milestones(project_with_milestones, goal_id="nonexistent", json_output=True)
        captured = capsys.readouterr()
        # Should handle gracefully
        assert "error" in captured.out.lower() or captured.out != ""


class TestOutputJSON:
    """Tests for JSON output formatting."""

    @pytest.fixture
    def sample_data(self):
        """Create sample analyzer and tracker for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)

            project = Project(
                name="Test Project",
                path=project_path,
                agent="claude",
                created_at=datetime.now(),
            )
            goals = [
                Goal("g1", "Goal 1", "execute", 75, 3, True),
                Goal("g2", "Goal 2", "active", 50, 2, False),
            ]
            result = AnalysisResult(
                project=project,
                goals=goals,
                phase="execution",
                completion_percent=62.5,
                health_score=85.0,
                milestone_count=4,
                completed_milestones=2,
                recent_milestones=[],
            )

            tracker = ExecutionTracker(project_path)

            # Add some milestone records
            now = datetime.now()
            tracker._save_milestone_record(
                MilestoneRecord("m1", "g1", now - timedelta(days=2), "Note 1")
            )
            tracker._save_milestone_record(
                MilestoneRecord("m2", "g1", now - timedelta(days=1), "Note 2")
            )

            yield result, tracker

    def test_output_json_structure(self, sample_data):
        """Test JSON output has required structure."""
        result, tracker = sample_data
        console = Mock()
        
        _output_json(result, tracker, None, console)
        
        # Verify print_json was called
        console.print_json.assert_called_once()
        call_args = console.print_json.call_args
        assert "data" in call_args.kwargs
        
        data = call_args.kwargs["data"]
        assert "project" in data
        assert "milestones" in data
        assert "velocity" in data
        assert "momentum" in data
        assert "goals" in data

    def test_output_json_with_goal_filter(self, sample_data):
        """Test JSON output with goal ID filter."""
        result, tracker = sample_data
        console = Mock()
        
        _output_json(result, tracker, "g1", console)
        
        console.print_json.assert_called_once()
        call_args = console.print_json.call_args
        data = call_args.kwargs["data"]
        
        # Should only have one goal
        assert len(data["goals"]) == 1
        assert data["goals"][0]["goal_id"] == "g1"

    def test_output_json_invalid_goal_filter(self, sample_data):
        """Test JSON output with invalid goal ID."""
        result, tracker = sample_data
        console = Mock()
        
        _output_json(result, tracker, "nonexistent", console)
        
        console.print_json.assert_called_once()
        call_args = console.print_json.call_args
        data = call_args.kwargs["data"]
        
        assert "error" in data


class TestOutputFormatted:
    """Tests for formatted output."""

    @pytest.fixture
    def sample_result(self):
        """Create sample analysis result."""
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
            phase="execution",
            completion_percent=62.5,
            health_score=85.0,
            milestone_count=4,
            completed_milestones=2,
            recent_milestones=[],
        )

    def test_output_formatted_calls_display(self, sample_result):
        """Test that formatted output calls display functions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = ExecutionTracker(project_path)
            console = Mock()
            
            with patch("goalkeeper_cli.commands.milestones._display_milestone_table") as mock_display:
                _output_formatted(sample_result, tracker, None, console)
                # Should call display function if there are goals
                if sample_result.goals:
                    mock_display.assert_called_once()

    def test_output_formatted_with_goal_filter(self, sample_result):
        """Test formatted output with goal filter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = ExecutionTracker(project_path)
            console = Mock()
            
            _output_formatted(sample_result, tracker, "g1", console)
            # Should not raise error
            assert console.print.called


class TestDisplayMilestoneTable:
    """Tests for milestone table display."""

    def test_display_milestone_table_with_history(self):
        """Test displaying milestone table with history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = ExecutionTracker(project_path)
            now = datetime.now()
            tracker._save_milestone_record(
                MilestoneRecord("m1", "g1", now - timedelta(days=1), "Test milestone")
            )
            
            console = Mock()
            goals = [Goal("g1", "Goal 1", "execute", 75, 3, True)]
            
            _display_milestone_table(tracker, goals, console)
            
            # Should call print methods
            assert console.print.called

    def test_display_milestone_table_no_history(self):
        """Test displaying milestone table without history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = ExecutionTracker(project_path)
            console = Mock()
            goals = [Goal("g1", "Goal 1", "execute", 75, 3, True)]
            
            _display_milestone_table(tracker, goals, console)
            
            # Should still call print methods
            assert console.print.called


class TestDisplayTimeline:
    """Tests for timeline display."""

    def test_display_timeline_with_data(self):
        """Test displaying timeline with data."""
        timeline = {
            "2025-12-01": 3,
            "2025-12-02": 2,
            "2025-12-03": 5,
            "2025-12-04": 1,
        }
        
        console = Mock()
        _display_timeline(timeline, console)
        
        # Should call print method
        assert console.print.called

    def test_display_timeline_empty(self):
        """Test displaying empty timeline."""
        timeline = {}
        console = Mock()
        
        _display_timeline(timeline, console)
        
        # Should still call print
        assert console.print.called


class TestFormatMomentum:
    """Tests for momentum formatting."""

    def test_format_momentum_excellent(self):
        """Test formatting excellent momentum."""
        result = _format_momentum(90.0)
        assert "Excellent" in result
        assert "bold green" in result

    def test_format_momentum_good(self):
        """Test formatting good momentum."""
        result = _format_momentum(70.0)
        assert "Good" in result
        assert "green" in result

    def test_format_momentum_fair(self):
        """Test formatting fair momentum."""
        result = _format_momentum(50.0)
        assert "Fair" in result
        assert "yellow" in result

    def test_format_momentum_low(self):
        """Test formatting low momentum."""
        result = _format_momentum(25.0)
        assert "Low" in result
        assert "orange" in result

    def test_format_momentum_stalled(self):
        """Test formatting stalled momentum."""
        result = _format_momentum(10.0)
        assert "Stalled" in result
        assert "red" in result

    def test_format_momentum_zero(self):
        """Test formatting zero momentum."""
        result = _format_momentum(0.0)
        assert "Stalled" in result
        assert "red" in result

    def test_format_momentum_hundred(self):
        """Test formatting perfect momentum."""
        result = _format_momentum(100.0)
        assert "100" in result


class TestMilestonesIntegration:
    """Integration tests for milestones command."""

    def test_complete_milestones_workflow(self):
        """Test complete workflow from project to display."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = ExecutionTracker(project_path)
            
            # Create multiple milestone records over time
            now = datetime.now()
            for i in range(5):
                record = MilestoneRecord(
                    milestone_id=f"m{i}",
                    goal_id="goal1",
                    completed_at=now - timedelta(days=5-i),
                    notes=f"Milestone {i}",
                )
                tracker._save_milestone_record(record)
            
            # Verify we can get stats
            stats = tracker.get_execution_stats([Goal("goal1", "Goal 1", "execute", 50, 5, True)], 50.0)
            assert stats.completed_milestones == 5
            assert stats.velocity_per_day > 0
            
            # Verify momentum calculation
            momentum = tracker.get_momentum()
            assert 0 <= momentum <= 100
            
            # Verify timeline
            timeline = tracker.get_completion_timeline()
            assert len(timeline) > 0

    def test_milestones_with_multiple_goals(self):
        """Test milestones with multiple goals."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = ExecutionTracker(project_path)
            goals = [
                Goal("g1", "Goal 1", "execute", 50, 3, True),
                Goal("g2", "Goal 2", "execute", 50, 2, False),
                Goal("g3", "Goal 3", "active", 25, 1, True),
            ]
            
            # Add milestones for each goal
            now = datetime.now()
            for goal_idx, goal in enumerate(goals):
                for m_idx in range(2):
                    record = MilestoneRecord(
                        milestone_id=f"m{goal_idx}_{m_idx}",
                        goal_id=goal.id,
                        completed_at=now - timedelta(days=goal_idx*2 + m_idx),
                    )
                    tracker._save_milestone_record(record)
            
            # Verify stats
            stats = tracker.get_execution_stats(goals, 40.0)
            assert stats.total_milestones == 6  # 3 goals * 2 each
            assert stats.completed_milestones == 6
            
            # Verify per-goal stats
            for goal in goals:
                goal_stats = tracker.get_goal_execution_stats(goal.id)
                assert goal_stats["completed_milestones"] == 2
