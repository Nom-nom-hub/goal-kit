"""Tests for metrics tracker module."""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta

from goalkeeper_cli.metrics import MetricsTracker, MetricRecord, MetricStats, HealthScore
from goalkeeper_cli.models import Goal


@pytest.fixture
def temp_project():
    """Create a temporary goal-kit project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        goalkit_dir = project_path / ".goalkit"
        metrics_dir = goalkit_dir / "metrics"
        goalkit_dir.mkdir(parents=True, exist_ok=True)
        metrics_dir.mkdir(parents=True, exist_ok=True)

        yield project_path


class TestMetricsTracker:
    """Tests for MetricsTracker class."""

    def test_tracker_init_valid_project(self, temp_project):
        """Test initializing tracker with valid project."""
        tracker = MetricsTracker(temp_project)
        assert tracker.project_path == temp_project
        assert tracker.goalkit_dir == temp_project / ".goalkit"
        assert tracker.metrics_dir == temp_project / ".goalkit" / "metrics"

    def test_tracker_init_missing_project_path(self):
        """Test initializing tracker with non-existent path."""
        with pytest.raises(FileNotFoundError):
            MetricsTracker(Path("/nonexistent/project"))

    def test_tracker_init_missing_goalkit(self, temp_project):
        """Test initializing tracker without .goalkit directory."""
        import shutil

        goalkit_dir = temp_project / ".goalkit"
        if goalkit_dir.exists():
            shutil.rmtree(goalkit_dir)

        with pytest.raises(FileNotFoundError):
            MetricsTracker(temp_project)

    def test_track_metric(self, temp_project):
        """Test tracking a metric."""
        tracker = MetricsTracker(temp_project)
        tracker.track_metric("goal1", "velocity", 2.5, "Good progress")

        # Verify history file was created
        assert tracker.history_file.exists()

        # Verify record was saved
        metrics = tracker.get_metrics_for_goal("goal1")
        assert "velocity" in metrics
        assert len(metrics["velocity"]) == 1
        assert metrics["velocity"][0].value == 2.5

    def test_track_multiple_metrics(self, temp_project):
        """Test tracking multiple metrics."""
        tracker = MetricsTracker(temp_project)

        tracker.track_metric("goal1", "velocity", 2.0)
        tracker.track_metric("goal1", "quality", 85)
        tracker.track_metric("goal2", "velocity", 1.5)

        g1_metrics = tracker.get_metrics_for_goal("goal1")
        assert len(g1_metrics) == 2
        assert "velocity" in g1_metrics
        assert "quality" in g1_metrics

        g2_metrics = tracker.get_metrics_for_goal("goal2")
        assert len(g2_metrics) == 1
        assert "velocity" in g2_metrics

    def test_get_metrics_for_goal_empty(self, temp_project):
        """Test getting metrics from goal with no metrics."""
        tracker = MetricsTracker(temp_project)
        metrics = tracker.get_metrics_for_goal("nonexistent")
        assert len(metrics) == 0

    def test_metric_record_creation(self):
        """Test creating a metric record."""
        now = datetime.now()
        record = MetricRecord(
            metric_name="velocity",
            goal_id="g1",
            value=2.5,
            measured_at=now,
            notes="Good velocity",
        )

        assert record.metric_name == "velocity"
        assert record.goal_id == "g1"
        assert record.value == 2.5
        assert record.notes == "Good velocity"

    def test_get_metric_stats(self, temp_project):
        """Test getting statistics for a metric."""
        tracker = MetricsTracker(temp_project)
        now = datetime.now()

        # Track multiple values over time
        for i in range(5):
            value = 1.0 + i * 0.5
            tracker.track_metric(
                "goal1", "velocity", value, f"Measurement {i}"
            )

        stats = tracker.get_metric_stats("goal1", "velocity")

        assert stats is not None
        assert stats.metric_name == "velocity"
        assert stats.total_records == 5
        assert stats.current_value == 3.0  # Last recorded (most recent)
        assert stats.min_value == 1.0
        assert stats.max_value == 3.0
        assert stats.average_value == 2.0

    def test_get_metric_stats_nonexistent(self, temp_project):
        """Test getting stats for non-existent metric."""
        tracker = MetricsTracker(temp_project)
        stats = tracker.get_metric_stats("goal1", "nonexistent")
        assert stats is None

    def test_calculate_trend_improving(self, temp_project):
        """Test trend calculation for improving metric."""
        tracker = MetricsTracker(temp_project)
        now = datetime.now()

        # Track improving values
        for i in range(6):
            # First 3: low values, last 3: high values
            value = 1.0 if i < 3 else 5.0
            record = MetricRecord(
                metric_name="quality",
                goal_id="goal1",
                value=value,
                measured_at=now - timedelta(days=6 - i),
            )
            tracker._save_metric_record(record)

        records = tracker.get_metrics_for_goal("goal1")["quality"]
        trend = tracker._calculate_trend(records)

        # Trend should be positive (improving)
        assert trend > 0

    def test_calculate_trend_declining(self, temp_project):
        """Test trend calculation for declining metric."""
        tracker = MetricsTracker(temp_project)
        now = datetime.now()

        # Track declining values
        for i in range(6):
            # First 3: high values, last 3: low values
            value = 5.0 if i < 3 else 1.0
            record = MetricRecord(
                metric_name="quality",
                goal_id="goal1",
                value=value,
                measured_at=now - timedelta(days=6 - i),
            )
            tracker._save_metric_record(record)

        records = tracker.get_metrics_for_goal("goal1")["quality"]
        trend = tracker._calculate_trend(records)

        # Trend should be negative (declining)
        assert trend < 0

    def test_calculate_health_score(self, temp_project):
        """Test calculating health score."""
        tracker = MetricsTracker(temp_project)
        goals = [
            Goal("g1", "Goal 1", "execute", 75, 3, True),
            Goal("g2", "Goal 2", "execute", 50, 2, False),
        ]

        # Track some metrics
        tracker.track_metric("g1", "velocity", 2.0)
        tracker.track_metric("g2", "quality", 85)

        health = tracker.calculate_health_score(goals, 62.5)

        assert health.overall_score > 0
        assert health.completion_score == 62.5
        assert 0 <= health.metrics_score <= 100
        assert 0 <= health.momentum_score <= 100
        assert 0 <= health.quality_score <= 100

    def test_health_score_empty_project(self, temp_project):
        """Test health score for empty project."""
        tracker = MetricsTracker(temp_project)
        health = tracker.calculate_health_score([], 0.0)

        assert health.overall_score >= 0
        assert health.completion_score == 0.0

    def test_get_metric_trends(self, temp_project):
        """Test getting metric trends."""
        tracker = MetricsTracker(temp_project)
        now = datetime.now()

        # Track metrics over several days
        for i in range(7):
            value = 1.0 + i * 0.2
            record = MetricRecord(
                metric_name="velocity",
                goal_id="goal1",
                value=value,
                measured_at=now - timedelta(days=6 - i),
            )
            tracker._save_metric_record(record)

        trends = tracker.get_metric_trends("goal1", "velocity", days=30)

        # Should have entries for multiple days
        assert len(trends) > 0


class TestMetricRecord:
    """Tests for MetricRecord dataclass."""

    def test_record_creation(self):
        """Test creating a metric record."""
        now = datetime.now()
        record = MetricRecord(
            metric_name="velocity",
            goal_id="g1",
            value=2.5,
            measured_at=now,
        )

        assert record.metric_name == "velocity"
        assert record.goal_id == "g1"
        assert record.value == 2.5
        assert record.notes is None

    def test_record_with_notes(self):
        """Test creating record with notes."""
        record = MetricRecord(
            metric_name="quality",
            goal_id="g1",
            value=85,
            measured_at=datetime.now(),
            notes="Excellent quality",
        )

        assert record.notes == "Excellent quality"


class TestMetricStats:
    """Tests for MetricStats dataclass."""

    def test_stats_creation(self):
        """Test creating metric stats."""
        now = datetime.now()
        stats = MetricStats(
            metric_name="velocity",
            total_records=10,
            current_value=2.5,
            average_value=2.0,
            min_value=1.0,
            max_value=3.5,
            trend=0.25,
            last_measured=now,
        )

        assert stats.metric_name == "velocity"
        assert stats.total_records == 10
        assert stats.current_value == 2.5


class TestHealthScore:
    """Tests for HealthScore dataclass."""

    def test_health_score_creation(self):
        """Test creating health score."""
        score = HealthScore(
            overall_score=75.0,
            completion_score=80.0,
            metrics_score=70.0,
            momentum_score=75.0,
            quality_score=70.0,
        )

        assert score.overall_score == 75.0
        assert score.completion_score == 80.0

    def test_health_score_with_breakdown(self):
        """Test health score with breakdown."""
        breakdown = {
            "completion": 80.0,
            "metrics": 70.0,
            "momentum": 75.0,
            "quality": 70.0,
        }
        score = HealthScore(
            overall_score=75.0,
            completion_score=80.0,
            metrics_score=70.0,
            momentum_score=75.0,
            quality_score=70.0,
            breakdown=breakdown,
        )

        assert score.breakdown["completion"] == 80.0


class TestMetricsTrackerEnhanced:
    """Tests for enhanced MetricsTracker methods."""

    @pytest.fixture
    def temp_project_with_metrics(self):
        """Create a project with metric history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            metrics_dir = goalkit_dir / "metrics"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            metrics_dir.mkdir(parents=True, exist_ok=True)

            tracker = MetricsTracker(project_path)

            # Create history over 14 days
            now = datetime.now()
            for i in range(10):
                record = MetricRecord(
                    metric_name="velocity",
                    goal_id="goal1" if i < 6 else "goal2",
                    value=1.0 + i * 0.1,
                    measured_at=now - timedelta(days=10 - i),
                    notes=f"Metric {i}",
                )
                tracker._save_metric_record(record)

            yield project_path, tracker

    def test_momentum_score_calculation(self, temp_project_with_metrics):
        """Test momentum score calculation."""
        _, tracker = temp_project_with_metrics

        momentum = tracker._calculate_momentum_score()

        assert 0 <= momentum <= 100
        assert isinstance(momentum, float)

    def test_quality_score_calculation(self, temp_project_with_metrics):
        """Test quality score calculation."""
        _, tracker = temp_project_with_metrics
        goals = [
            Goal("goal1", "Goal 1", "execute", 50, 3, True),
            Goal("goal2", "Goal 2", "execute", 50, 2, False),
        ]

        quality = tracker._calculate_quality_score(goals)

        assert 0 <= quality <= 100
        assert isinstance(quality, float)

    def test_multiple_goals_metrics(self, temp_project_with_metrics):
        """Test that metrics correctly separate goals."""
        _, tracker = temp_project_with_metrics

        goal1_metrics = tracker.get_metrics_for_goal("goal1")
        goal2_metrics = tracker.get_metrics_for_goal("goal2")

        # Goal 1 should have more metrics
        assert len(goal1_metrics.get("velocity", [])) >= len(
            goal2_metrics.get("velocity", [])
        )
