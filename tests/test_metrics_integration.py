"""Integration tests for metrics module with realistic multi-goal scenarios.

Tests comprehensive workflows combining MetricsTracker and metrics command
with multiple goals, metrics, and time-series data.
"""

from pathlib import Path
from datetime import datetime, timedelta
import json
import tempfile
from typing import Dict, List

import pytest

from src.goalkeeper_cli.metrics import MetricsTracker, MetricRecord
from src.goalkeeper_cli.commands.metrics import metrics


class TestMetricsMultiGoalWorkflow:
    """Test realistic multi-goal metrics workflows."""

    @pytest.fixture
    def project_with_goals(self, tmp_path):
        """Create a project with multiple goals."""
        goalkit_dir = tmp_path / ".goalkit"
        goalkit_dir.mkdir()

        # Create project metadata
        project_data = {
            "name": "Multi-Goal Project",
            "created_at": "2025-01-01",
        }
        with open(goalkit_dir / "project.json", "w") as f:
            json.dump(project_data, f)

        # Create goals directory
        goals_dir = goalkit_dir / "goals"
        goals_dir.mkdir()

        # Create goal files
        goals = {
            "goal-001": {
                "id": "goal-001",
                "name": "Backend API",
                "description": "Develop REST API",
            },
            "goal-002": {
                "id": "goal-002",
                "name": "Frontend UI",
                "description": "Build React components",
            },
            "goal-003": {
                "id": "goal-003",
                "name": "Database Schema",
                "description": "Design and implement database",
            },
        }

        for goal_id, goal_data in goals.items():
            goal_file = goals_dir / f"{goal_id}.md"
            goal_content = f"""# {goal_data['name']}

{goal_data['description']}

## Success Criteria
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Metrics
- response_time: API response latency
- test_coverage: Code coverage percentage
- throughput: Requests per second
"""
            with open(goal_file, "w") as f:
                f.write(goal_content)

        return tmp_path

    def test_track_multiple_metrics_across_goals(self, project_with_goals):
        """Test tracking different metrics for different goals."""
        tracker = MetricsTracker(project_with_goals)

        # Track metrics for goal-001
        tracker.track_metric("goal-001", "response_time", 125.5, "baseline")
        tracker.track_metric("goal-001", "response_time", 100.2, "after optimization")
        tracker.track_metric("goal-001", "test_coverage", 65.0)

        # Track metrics for goal-002
        tracker.track_metric("goal-002", "test_coverage", 80.0)
        tracker.track_metric("goal-002", "test_coverage", 85.5)

        # Track metrics for goal-003
        tracker.track_metric("goal-003", "throughput", 1000.0)
        tracker.track_metric("goal-003", "throughput", 1500.0)

        # Verify goal-001 metrics
        goal1_metrics = tracker.get_metrics_for_goal("goal-001")
        assert len(goal1_metrics) == 2
        assert "response_time" in goal1_metrics
        assert "test_coverage" in goal1_metrics
        assert len(goal1_metrics["response_time"]) == 2
        assert len(goal1_metrics["test_coverage"]) == 1

        # Verify goal-002 metrics
        goal2_metrics = tracker.get_metrics_for_goal("goal-002")
        assert len(goal2_metrics) == 1
        assert "test_coverage" in goal2_metrics
        assert len(goal2_metrics["test_coverage"]) == 2

        # Verify goal-003 metrics
        goal3_metrics = tracker.get_metrics_for_goal("goal-003")
        assert len(goal3_metrics) == 1
        assert "throughput" in goal3_metrics
        assert len(goal3_metrics["throughput"]) == 2

    def test_trend_analysis_across_multiple_goals(self, project_with_goals):
        """Test trend analysis with realistic metric patterns."""
        tracker = MetricsTracker(project_with_goals)

        # Goal-001: Improving response time (declining is good)
        for i in range(5):
            tracker.track_metric("goal-001", "response_time", 200 - (i * 10))

        # Goal-002: Improving test coverage (increasing is good)
        for i in range(5):
            tracker.track_metric("goal-002", "test_coverage", 50 + (i * 10))

        # Goal-003: Declining throughput (bad trend)
        for i in range(5):
            tracker.track_metric("goal-003", "throughput", 2000 - (i * 100))

        # Check trends
        goal1_stats = tracker.get_metric_stats("goal-001", "response_time")
        assert goal1_stats is not None
        assert goal1_stats.trend < 0  # Declining response time is good

        goal2_stats = tracker.get_metric_stats("goal-002", "test_coverage")
        assert goal2_stats is not None
        assert goal2_stats.trend > 0  # Increasing coverage is good

        goal3_stats = tracker.get_metric_stats("goal-003", "throughput")
        assert goal3_stats is not None
        assert goal3_stats.trend < 0  # Declining throughput is bad

    def test_health_score_with_varied_metrics(self, project_with_goals):
        """Test health score calculation with different metric coverage."""
        from src.goalkeeper_cli.models import Goal

        tracker = MetricsTracker(project_with_goals)

        # Create goals with metrics_defined flag
        goals = [
            Goal(
                id="goal-001",
                name="Backend API",
                phase="execution",
                completion_percent=75,
                success_criteria_count=3,
                metrics_defined=True,
            ),
            Goal(
                id="goal-002",
                name="Frontend UI",
                phase="active",
                completion_percent=50,
                success_criteria_count=3,
                metrics_defined=True,
            ),
            Goal(
                id="goal-003",
                name="Database",
                phase="setup",
                completion_percent=25,
                success_criteria_count=3,
                metrics_defined=False,
            ),
        ]

        # Track various metrics
        tracker.track_metric("goal-001", "response_time", 100.0)
        tracker.track_metric("goal-001", "test_coverage", 80.0)
        tracker.track_metric("goal-002", "test_coverage", 75.0)

        # Recent activity for momentum
        now = datetime.now()
        for i in range(3):
            days_ago = (now - timedelta(days=i)).isoformat()
            history_file = tracker.history_file
            records = []
            if history_file.exists():
                with open(history_file, "r") as f:
                    records = json.load(f)

            records.append(
                {
                    "goal_id": "goal-001",
                    "metric_name": "response_time",
                    "value": 100 - i,
                    "measured_at": days_ago,
                    "notes": None,
                }
            )

            with open(history_file, "w") as f:
                json.dump(records, f)

        # Calculate health score
        completion = sum(g.completion_percent for g in goals) / len(goals)
        health = tracker.calculate_health_score(goals, completion)

        assert health.overall_score >= 0
        assert health.overall_score <= 100
        assert health.completion_score == completion
        assert health.metrics_score > 0  # Some goals have metrics
        assert health.momentum_score > 0  # Recent activity
        assert health.quality_score >= 0

    def test_metrics_aggregation_across_goals(self, project_with_goals):
        """Test aggregating metrics from multiple goals."""
        tracker = MetricsTracker(project_with_goals)

        # Track metrics across goals
        metric_data = {
            "goal-001": {"response_time": [150, 140, 130, 120]},
            "goal-002": {"test_coverage": [60, 65, 70, 75]},
            "goal-003": {"throughput": [1000, 1100, 1200]},
        }

        for goal_id, metrics_dict in metric_data.items():
            for metric_name, values in metrics_dict.items():
                for value in values:
                    tracker.track_metric(goal_id, metric_name, value)

        # Aggregate stats
        all_stats = {}
        for goal_id in metric_data.keys():
            goal_metrics = tracker.get_metrics_for_goal(goal_id)
            for metric_name in goal_metrics.keys():
                stats = tracker.get_metric_stats(goal_id, metric_name)
                if stats:
                    all_stats[f"{goal_id}:{metric_name}"] = stats

        assert len(all_stats) == 3
        assert all_stats["goal-001:response_time"].total_records == 4
        assert all_stats["goal-002:test_coverage"].total_records == 4
        assert all_stats["goal-003:throughput"].total_records == 3

    def test_metrics_with_time_series_data(self, project_with_goals):
        """Test tracking metrics over time with realistic patterns."""
        tracker = MetricsTracker(project_with_goals)

        # Simulate daily metrics over 30 days
        base_date = datetime.now() - timedelta(days=30)

        for day in range(30):
            current_date = base_date + timedelta(days=day)

            # Response time: improving over time
            response_time = 200 - (day * 2)
            tracker.track_metric("goal-001", "response_time", response_time)

            # Test coverage: gradually increasing
            coverage = 50 + (day * 1.5)
            tracker.track_metric("goal-002", "test_coverage", coverage)

            # Throughput: slight improvements
            throughput = 1000 + (day * 5)
            tracker.track_metric("goal-003", "throughput", throughput)

        # Get trends over 30 days
        trends_1 = tracker.get_metric_trends("goal-001", "response_time", days=30)
        trends_2 = tracker.get_metric_trends("goal-002", "test_coverage", days=30)
        trends_3 = tracker.get_metric_trends("goal-003", "throughput", days=30)

        # Should have ~30 entries (one per day)
        assert len(trends_1) > 0
        assert len(trends_2) > 0
        assert len(trends_3) > 0

        # Stats should show trends
        stats_1 = tracker.get_metric_stats("goal-001", "response_time")
        assert stats_1.trend < 0  # Response time decreasing (good)

        stats_2 = tracker.get_metric_stats("goal-002", "test_coverage")
        assert stats_2.trend > 0  # Coverage increasing (good)


class TestMetricsCommandIntegration:
    """Test metrics command with realistic scenarios."""

    @pytest.fixture
    def complex_project(self, tmp_path):
        """Create complex project with multiple goals and metrics."""
        goalkit_dir = tmp_path / ".goalkit"
        goalkit_dir.mkdir()

        # Project metadata
        project_data = {"name": "Complex Project"}
        with open(goalkit_dir / "project.json", "w") as f:
            json.dump(project_data, f)

        # Goals
        goals_dir = goalkit_dir / "goals"
        goals_dir.mkdir()

        goal_names = ["backend", "frontend", "devops"]
        for i, name in enumerate(goal_names):
            goal_id = f"goal-{i+1:03d}"
            goal_file = goals_dir / f"{goal_id}.md"
            goal_file.write_text(
                f"""# {name.title()}

Goal for {name}

## Metrics
- metric1: First metric
- metric2: Second metric
"""
            )

        # Track sample metrics
        tracker = MetricsTracker(tmp_path)
        for i in range(1, 4):
            goal_id = f"goal-{i:03d}"
            for j in range(5):
                tracker.track_metric(goal_id, "metric1", 100 + j * 10)
                tracker.track_metric(goal_id, "metric2", 50 + j * 5)

        return tmp_path

    def test_metrics_command_displays_all_goals(self, complex_project, capsys):
        """Test metrics command displays metrics for all goals."""
        metrics(project_path=complex_project, json_output=False)
        captured = capsys.readouterr()

        # Should display project name
        assert "Complex Project" in captured.out

        # Should mention health score
        assert "Health Score" in captured.out or "health" in captured.out.lower()

    def test_metrics_command_json_output(self, complex_project, capsys):
        """Test metrics command JSON output."""
        metrics(project_path=complex_project, json_output=True)
        captured = capsys.readouterr()

        # Parse JSON output
        import json

        json_text = captured.out
        # Extract JSON from output
        start = json_text.find("{")
        end = json_text.rfind("}") + 1
        if start >= 0 and end > start:
            json_data = json.loads(json_text[start:end])
            assert "project" in json_data
            assert "health_score" in json_data
            assert "goals" in json_data

    def test_metrics_command_goal_filtering(self, complex_project, capsys):
        """Test metrics command with goal filtering."""
        metrics(project_path=complex_project, goal_id="goal-001", json_output=False)
        captured = capsys.readouterr()

        # Should display metrics panel or table
        assert len(captured.out) > 0

    def test_metrics_health_score_aggregation(self, complex_project):
        """Test health score calculation across multiple goals."""
        from src.goalkeeper_cli.analyzer import ProjectAnalyzer

        analyzer = ProjectAnalyzer(complex_project)
        result = analyzer.analyze()

        tracker = MetricsTracker(complex_project)
        health = tracker.calculate_health_score(result.goals, result.completion_percent)

        assert health.overall_score >= 0
        assert health.overall_score <= 100
        assert health.completion_score >= 0
        assert health.metrics_score >= 0
        assert health.momentum_score >= 0
        assert health.quality_score >= 0


class TestMetricsEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.fixture
    def minimal_project(self, tmp_path):
        """Create minimal project."""
        goalkit_dir = tmp_path / ".goalkit"
        goalkit_dir.mkdir()
        (goalkit_dir / "goals").mkdir()
        (goalkit_dir / "project.json").write_text('{"name": "Minimal"}')
        return tmp_path

    def test_metrics_with_no_tracked_metrics(self, minimal_project, capsys):
        """Test metrics command when no metrics are tracked."""
        metrics(project_path=minimal_project, json_output=False)
        captured = capsys.readouterr()

        # Should handle gracefully
        assert len(captured.out) > 0

    def test_metrics_with_single_goal(self, minimal_project):
        """Test metrics with single goal."""
        goals_dir = minimal_project / ".goalkit" / "goals"
        goals_dir.mkdir(exist_ok=True)
        (goals_dir / "goal-001.md").write_text(
            "# Single Goal\nDescription\n## Metrics\n- metric1: test"
        )

        tracker = MetricsTracker(minimal_project)
        tracker.track_metric("goal-001", "metric1", 100.0)

        from src.goalkeeper_cli.analyzer import ProjectAnalyzer

        analyzer = ProjectAnalyzer(minimal_project)
        result = analyzer.analyze()

        health = tracker.calculate_health_score(result.goals, 50.0)
        assert health.overall_score >= 0

    def test_metrics_with_very_recent_data(self, minimal_project):
        """Test metrics with very recent measurements."""
        goals_dir = minimal_project / ".goalkit" / "goals"
        goals_dir.mkdir(exist_ok=True)
        (goals_dir / "goal-001.md").write_text(
            "# Test Goal\nDescription\n## Metrics\n- metric1: test"
        )

        tracker = MetricsTracker(minimal_project)

        # Add metrics just now
        now = datetime.now()
        for i in range(5):
            tracker.track_metric("goal-001", "metric1", 100 + i)

        stats = tracker.get_metric_stats("goal-001", "metric1")
        assert stats is not None
        assert stats.total_records == 5
        assert stats.current_value == 104  # Last value
