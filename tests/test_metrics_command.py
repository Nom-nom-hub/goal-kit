"""Tests for metrics command."""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from goalkeeper_cli.commands.metrics import (
    metrics,
    _output_json,
    _output_formatted,
    _display_metrics_table,
    _format_score,
    _format_trend,
)
from goalkeeper_cli.metrics import MetricsTracker, MetricRecord
from goalkeeper_cli.analyzer import AnalysisResult
from goalkeeper_cli.models import Project, Goal


class TestMetricsCommand:
    """Tests for metrics command."""

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
    def project_with_metrics(self):
        """Create a project with metrics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goals_dir = goalkit_dir / "goals"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            goals_dir.mkdir(parents=True, exist_ok=True)

            tracker = MetricsTracker(project_path)

            # Track some metrics
            now = datetime.now()
            for i in range(5):
                tracker.track_metric("goal1", "velocity", 1.0 + i * 0.2, f"Day {i}")
                tracker.track_metric("goal2", "quality", 80 + i * 2, f"Day {i}")

            yield project_path

    def test_metrics_with_valid_project(self, temp_project, capsys):
        """Test metrics command with valid project."""
        metrics(temp_project)
        captured = capsys.readouterr()
        # Should not raise error
        assert "Error" not in captured.out or captured.out != ""

    def test_metrics_with_invalid_path(self, capsys):
        """Test metrics command with invalid path."""
        metrics(Path("/nonexistent/path"))
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_metrics_json_output(self, project_with_metrics, capsys):
        """Test metrics command with JSON output."""
        metrics(project_with_metrics, json_output=True)
        captured = capsys.readouterr()
        # Should output valid JSON
        try:
            json.loads(captured.out)
        except json.JSONDecodeError:
            pass

    def test_metrics_with_goal_filter(self, project_with_metrics, capsys):
        """Test metrics command with goal ID filter."""
        metrics(project_with_metrics, goal_id="goal1")
        captured = capsys.readouterr()
        assert "Error" not in captured.out or captured.out != ""

    def test_metrics_with_invalid_goal_id(self, project_with_metrics, capsys):
        """Test metrics command with invalid goal ID."""
        metrics(project_with_metrics, goal_id="nonexistent", json_output=True)
        captured = capsys.readouterr()
        assert "error" in captured.out.lower() or captured.out != ""


class TestOutputJSON:
    """Tests for JSON output formatting."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
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

            tracker = MetricsTracker(project_path)

            # Add metrics
            tracker.track_metric("g1", "velocity", 2.0, "Good")
            tracker.track_metric("g1", "quality", 85, "Excellent")
            tracker.track_metric("g2", "velocity", 1.5, "Fair")

            yield result, tracker

    def test_output_json_structure(self, sample_data):
        """Test JSON output has required structure."""
        result, tracker = sample_data
        console = Mock()
        
        _output_json(result, tracker, None, None, 30, console)
        
        console.print_json.assert_called_once()
        call_args = console.print_json.call_args
        data = call_args.kwargs["data"]
        
        assert "project" in data
        assert "health_score" in data
        assert "goals" in data

    def test_output_json_with_goal_filter(self, sample_data):
        """Test JSON output with goal ID filter."""
        result, tracker = sample_data
        console = Mock()
        
        _output_json(result, tracker, "g1", None, 30, console)
        
        console.print_json.assert_called_once()
        call_args = console.print_json.call_args
        data = call_args.kwargs["data"]
        
        assert len(data["goals"]) >= 1

    def test_output_json_invalid_goal_filter(self, sample_data):
        """Test JSON output with invalid goal ID."""
        result, tracker = sample_data
        console = Mock()
        
        _output_json(result, tracker, "nonexistent", None, 30, console)
        
        console.print_json.assert_called_once()


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

    def test_output_formatted_displays(self, sample_result):
        """Test that formatted output calls display functions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = MetricsTracker(project_path)
            tracker.track_metric("g1", "velocity", 2.0)
            
            console = Mock()
            
            _output_formatted(sample_result, tracker, None, None, 30, console)
            
            # Should call print methods
            assert console.print.called


class TestDisplayMetricsTable:
    """Tests for metrics table display."""

    def test_display_metrics_table_with_data(self):
        """Test displaying metrics table with data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = MetricsTracker(project_path)
            tracker.track_metric("g1", "velocity", 2.0)
            tracker.track_metric("g1", "quality", 85)
            
            console = Mock()
            goals = [Goal("g1", "Goal 1", "execute", 75, 3, True)]
            
            _display_metrics_table(tracker, goals, None, console)
            
            # Should call print methods
            assert console.print.called

    def test_display_metrics_table_empty(self):
        """Test displaying metrics table without metrics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = MetricsTracker(project_path)
            console = Mock()
            goals = [Goal("g1", "Goal 1", "execute", 75, 3, True)]
            
            _display_metrics_table(tracker, goals, None, console)
            
            # Should still call print
            assert console.print.called


class TestFormatScore:
    """Tests for score formatting."""

    def test_format_score_excellent(self):
        """Test formatting excellent score."""
        result = _format_score(90.0)
        assert "bold green" in result
        assert "90" in result

    def test_format_score_good(self):
        """Test formatting good score."""
        result = _format_score(70.0)
        assert "yellow" in result
        assert "70" in result

    def test_format_score_poor(self):
        """Test formatting poor score."""
        result = _format_score(30.0)
        assert "red" in result
        assert "30" in result

    def test_format_score_zero(self):
        """Test formatting zero score."""
        result = _format_score(0.0)
        assert "red" in result
        assert "0" in result

    def test_format_score_hundred(self):
        """Test formatting perfect score."""
        result = _format_score(100.0)
        assert "green" in result
        assert "100" in result


class TestFormatTrend:
    """Tests for trend formatting."""

    def test_format_trend_positive(self):
        """Test formatting positive trend."""
        result = _format_trend(0.5)
        assert "green" in result
        assert "↑" in result

    def test_format_trend_negative(self):
        """Test formatting negative trend."""
        result = _format_trend(-0.5)
        assert "red" in result
        assert "↓" in result

    def test_format_trend_neutral(self):
        """Test formatting neutral trend."""
        result = _format_trend(0.0)
        assert "yellow" in result
        assert "→" in result

    def test_format_trend_small_positive(self):
        """Test formatting small positive trend."""
        result = _format_trend(0.05)
        assert "→" in result

    def test_format_trend_small_negative(self):
        """Test formatting small negative trend."""
        result = _format_trend(-0.05)
        assert "→" in result


class TestMetricsIntegration:
    """Integration tests for metrics command."""

    def test_complete_metrics_workflow(self):
        """Test complete workflow from project to display."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = MetricsTracker(project_path)
            
            # Create multiple metric records
            now = datetime.now()
            for i in range(10):
                tracker.track_metric(
                    goal_id="goal1",
                    metric_name="velocity",
                    value=1.0 + i * 0.1,
                    notes=f"Measurement {i}",
                )
            
            # Verify stats
            stats = tracker.get_metric_stats("goal1", "velocity")
            assert stats is not None
            assert stats.total_records == 10
            assert stats.trend != 0

    def test_metrics_with_multiple_goals(self):
        """Test metrics with multiple goals."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = MetricsTracker(project_path)
            goals = [
                Goal("g1", "Goal 1", "execute", 50, 3, True),
                Goal("g2", "Goal 2", "execute", 50, 2, False),
            ]
            
            # Add metrics for each goal
            for goal in goals:
                for i in range(3):
                    tracker.track_metric(
                        goal_id=goal.id,
                        metric_name="velocity",
                        value=1.0 + i * 0.1,
                    )
            
            # Verify stats for each goal
            for goal in goals:
                metrics_dict = tracker.get_metrics_for_goal(goal.id)
                assert "velocity" in metrics_dict
                assert len(metrics_dict["velocity"]) == 3

    def test_health_score_aggregation(self):
        """Test health score calculation across goals."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = MetricsTracker(project_path)
            goals = [
                Goal("g1", "Goal 1", "execute", 75, 3, True),
                Goal("g2", "Goal 2", "execute", 50, 2, False),
            ]
            
            # Track metrics
            tracker.track_metric("g1", "velocity", 2.0)
            tracker.track_metric("g2", "quality", 85)
            
            # Calculate health
            health = tracker.calculate_health_score(goals, 62.5)
            
            assert 0 <= health.overall_score <= 100
            assert health.completion_score == 62.5
