"""Unit tests for analytics engine.

Tests cover:
- Burndown chart generation
- Velocity metrics calculation
- Trend analysis
- Completion forecasting
- Bottleneck identification
- Insight generation
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from goalkeeper_cli.analytics import (
    AnalyticsEngine,
    AnalyticsPoint,
    BurndownData,
    VelocityMetrics,
)


@pytest.fixture
def analytics_engine(tmp_path):
    """Create analytics engine with temporary directory."""
    goalkit_dir = tmp_path / ".goalkit"
    goalkit_dir.mkdir()
    return AnalyticsEngine(goalkit_dir)


@pytest.fixture
def sample_history(analytics_engine):
    """Create sample analytics history."""
    # Record 30 days of progress
    base_date = datetime.now() - timedelta(days=30)

    for i in range(30):
        date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        completed = min(i // 2, 20)  # Gradual progress
        analytics_engine.record_snapshot(
            "goal-1",
            completed=completed,
            total=20,
            blocked=max(0, 5 - i // 6),
            in_progress=max(0, 10 - i // 3),
        )

    return analytics_engine


class TestAnalyticsPoint:
    """Test AnalyticsPoint data class."""

    def test_create_point(self):
        """Test creating an analytics point."""
        point = AnalyticsPoint(
            date="2024-12-08",
            completed=5,
            total=20,
            blocked=2,
            in_progress=3,
        )

        assert point.date == "2024-12-08"
        assert point.completed == 5
        assert point.total == 20
        assert point.blocked == 2

    def test_to_dict(self):
        """Test conversion to dictionary."""
        point = AnalyticsPoint(
            date="2024-12-08",
            completed=5,
            total=20,
            blocked=2,
            in_progress=3,
        )

        data = point.to_dict()
        assert data["date"] == "2024-12-08"
        assert data["completed"] == 5

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "date": "2024-12-08",
            "completed": 5,
            "total": 20,
            "blocked": 2,
            "in_progress": 3,
        }

        point = AnalyticsPoint.from_dict(data)
        assert point.completed == 5
        assert point.total == 20


class TestRecordSnapshot:
    """Test snapshot recording."""

    def test_record_first_snapshot(self, analytics_engine):
        """Test recording first snapshot."""
        analytics_engine.record_snapshot(
            "goal-1",
            completed=5,
            total=20,
            blocked=2,
            in_progress=3,
        )

        history = analytics_engine._load_history()
        assert "goal-1" in history
        assert len(history["goal-1"]) == 1
        assert history["goal-1"][0].completed == 5

    def test_record_multiple_snapshots(self, analytics_engine):
        """Test recording multiple snapshots."""
        for i in range(5):
            analytics_engine.record_snapshot(
                "goal-1",
                completed=i,
                total=20,
            )

        history = analytics_engine._load_history()
        assert len(history["goal-1"]) == 5

    def test_update_same_day_snapshot(self, analytics_engine):
        """Test updating snapshot recorded same day."""
        analytics_engine.record_snapshot("goal-1", completed=5, total=20)
        analytics_engine.record_snapshot("goal-1", completed=6, total=20)

        history = analytics_engine._load_history()
        assert len(history["goal-1"]) == 1
        assert history["goal-1"][0].completed == 6

    def test_multiple_goals(self, analytics_engine):
        """Test recording snapshots for multiple goals."""
        analytics_engine.record_snapshot("goal-1", completed=5, total=20)
        analytics_engine.record_snapshot("goal-2", completed=3, total=15)

        history = analytics_engine._load_history()
        assert len(history) == 2
        assert len(history["goal-1"]) == 1
        assert len(history["goal-2"]) == 1


class TestBurndownData:
    """Test burndown chart generation."""

    def test_burndown_insufficient_data(self, analytics_engine):
        """Test burndown with insufficient data."""
        result = analytics_engine.get_burndown_data("nonexistent-goal")
        assert result is None

    def test_burndown_single_point(self, analytics_engine):
        """Test burndown with single data point."""
        analytics_engine.record_snapshot("goal-1", completed=5, total=20)
        result = analytics_engine.get_burndown_data("goal-1")
        assert result is None  # Need at least 2 points

    def test_burndown_data_structure(self, sample_history):
        """Test burndown data structure."""
        result = sample_history.get_burndown_data("goal-1")

        assert result is not None
        assert isinstance(result, BurndownData)
        assert len(result.dates) > 0
        assert len(result.ideal_remaining) == len(result.actual_remaining)
        assert len(result.completed_count) > 0
        assert result.chart_ascii  # Should have ASCII art

    def test_burndown_ideal_line(self, sample_history):
        """Test ideal burndown line calculation."""
        result = sample_history.get_burndown_data("goal-1")

        # Ideal line should start high and decrease to 0
        assert result.ideal_remaining[0] > 0
        # Line should be monotonically decreasing
        for i in range(len(result.ideal_remaining) - 1):
            assert result.ideal_remaining[i] >= result.ideal_remaining[i + 1]

    def test_burndown_date_range(self, sample_history):
        """Test burndown with custom date range."""
        today = datetime.now().strftime("%Y-%m-%d")
        ten_days_ago = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

        result = sample_history.get_burndown_data(
            "goal-1",
            start_date=ten_days_ago,
            end_date=today,
        )

        assert result is not None
        assert result.dates[0] >= ten_days_ago
        assert result.dates[-1] <= today


class TestVelocityMetrics:
    """Test velocity metrics calculation."""

    def test_velocity_insufficient_data(self, analytics_engine):
        """Test velocity with insufficient data."""
        analytics_engine.record_snapshot("goal-1", completed=5, total=20)
        result = analytics_engine.get_velocity_metrics("goal-1")
        assert result is None

    def test_velocity_metrics_structure(self, sample_history):
        """Test velocity metrics data structure."""
        result = sample_history.get_velocity_metrics("goal-1", periods=4)

        assert result is not None
        assert isinstance(result, VelocityMetrics)
        assert len(result.periods) > 0
        assert len(result.tasks_completed) == len(result.periods)
        assert result.average_velocity > 0
        assert result.trend in ["improving", "stable", "declining"]
        assert -1.0 <= result.momentum <= 1.0

    def test_velocity_trend_improving(self, analytics_engine):
        """Test velocity with improving trend."""
        base_date = datetime.now() - timedelta(days=20)

        # First period: 2 tasks
        for i in range(5):
            date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            analytics_engine.record_snapshot("goal-1", completed=i, total=20)

        # Second period: 4 tasks (velocity increasing)
        for i in range(5, 10):
            date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            analytics_engine.record_snapshot("goal-1", completed=2 + (i - 5) * 2, total=20)

        result = analytics_engine.get_velocity_metrics("goal-1", periods=2)
        assert result.trend == "improving"

    def test_velocity_custom_periods(self, sample_history):
        """Test velocity with custom period count."""
        result = sample_history.get_velocity_metrics("goal-1", periods=6)

        assert len(result.periods) == 6
        assert all(f"Period {i+1}" in result.periods for i in range(6))


class TestTrendAnalysis:
    """Test trend analysis."""

    def test_trend_insufficient_data(self, analytics_engine):
        """Test trend with insufficient data."""
        analytics_engine.record_snapshot("goal-1", completed=5, total=20)
        analytics_engine.record_snapshot("goal-1", completed=6, total=20)
        result = analytics_engine.get_trend_analysis("goal-1")
        assert result is None  # Need at least 3 points

    def test_trend_positive_direction(self, analytics_engine):
        """Test trend with positive direction."""
        base_date = datetime.now() - timedelta(days=10)

        for i in range(10):
            date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            analytics_engine.record_snapshot("goal-1", completed=i, total=20)

        result = analytics_engine.get_trend_analysis("goal-1")

        assert result is not None
        assert result.direction == "positive"
        assert result.slope > 0
        assert result.momentum_score > 0

    def test_trend_negative_direction(self, analytics_engine):
        """Test trend with negative direction."""
        base_date = datetime.now() - timedelta(days=10)

        for i in range(10, 0, -1):
            date = (base_date + timedelta(days=10 - i)).strftime("%Y-%m-%d")
            analytics_engine.record_snapshot("goal-1", completed=i, total=20)

        result = analytics_engine.get_trend_analysis("goal-1")

        assert result.direction == "negative"
        assert result.slope < 0

    def test_trend_r_squared(self, sample_history):
        """Test R-squared calculation."""
        result = sample_history.get_trend_analysis("goal-1")

        assert 0 <= result.r_squared <= 1


class TestCompletionForecast:
    """Test completion forecasting."""

    def test_forecast_insufficient_data(self, analytics_engine):
        """Test forecast with insufficient data."""
        result = analytics_engine.forecast_completion("nonexistent-goal")
        assert result is None

    def test_forecast_already_completed(self, analytics_engine):
        """Test forecast when goal is already completed."""
        analytics_engine.record_snapshot("goal-1", completed=20, total=20)
        result = analytics_engine.forecast_completion("goal-1")

        assert result is not None
        assert result.tasks_remaining == 0
        assert result.probability == 1.0

    def test_forecast_completion_date(self, sample_history):
        """Test completion date estimation."""
        result = sample_history.forecast_completion("goal-1")

        assert result is not None
        assert result.estimated_date
        assert result.tasks_remaining >= 0
        assert 0 <= result.probability <= 1

    def test_forecast_confidence_range(self, sample_history):
        """Test forecast confidence interval."""
        result = sample_history.forecast_completion("goal-1")

        # Low estimate should be later than estimate
        # High estimate should be earlier than estimate
        assert result.low_estimate >= result.estimated_date
        assert result.high_estimate <= result.estimated_date

    def test_forecast_with_deadline(self, sample_history):
        """Test forecast with deadline."""
        deadline = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        result = sample_history.forecast_completion("goal-1", deadline)

        assert result is not None
        assert result.days_remaining > 0
        assert result.required_velocity > 0

    def test_forecast_deadline_passed(self, sample_history):
        """Test forecast with past deadline."""
        deadline = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        result = sample_history.forecast_completion("goal-1", deadline)

        assert result is not None
        assert result.days_remaining < 0
        assert result.probability == 0.0


class TestBottlenecks:
    """Test bottleneck identification."""

    def test_bottlenecks_empty(self, analytics_engine):
        """Test bottlenecks with no data."""
        result = analytics_engine.get_bottlenecks("nonexistent-goal")
        assert result == []

    def test_bottlenecks_none(self, sample_history):
        """Test bottlenecks when none exist."""
        # Sample history has no serious bottlenecks
        result = sample_history.get_bottlenecks("goal-1")
        # Should not have critical bottlenecks
        assert all(b.severity != "critical" for b in result)

    def test_bottlenecks_blocked_tasks(self, analytics_engine):
        """Test bottleneck detection for blocked tasks."""
        base_date = datetime.now() - timedelta(days=10)

        for i in range(10):
            date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            analytics_engine.record_snapshot(
                "goal-1",
                completed=i,
                total=20,
                blocked=5,  # Consistently blocked
            )

        result = analytics_engine.get_bottlenecks("goal-1")

        # Should identify blocked tasks bottleneck
        blocked_bottlenecks = [b for b in result if b.task_id == "blocked"]
        assert len(blocked_bottlenecks) > 0

    def test_bottleneck_severity(self, analytics_engine):
        """Test bottleneck severity levels."""
        base_date = datetime.now() - timedelta(days=10)

        for i in range(10):
            date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            analytics_engine.record_snapshot(
                "goal-1",
                completed=i,
                total=20,
                blocked=6,  # High number of blocked tasks
            )

        result = analytics_engine.get_bottlenecks("goal-1")

        # Should have high severity for many blocked tasks
        assert any(b.severity in ["high", "critical"] for b in result)


class TestInsights:
    """Test insight generation."""

    def test_insights_empty(self, analytics_engine):
        """Test insights with no data."""
        result = analytics_engine.generate_insights("nonexistent-goal")
        assert len(result) > 0  # Should have default message

    def test_insights_structure(self, sample_history):
        """Test insights are strings."""
        result = sample_history.generate_insights("goal-1")

        assert isinstance(result, list)
        assert all(isinstance(i, str) for i in result)
        assert all(len(i) > 0 for i in result)

    def test_insights_with_velocity(self, sample_history):
        """Test that velocity insights are included."""
        result = sample_history.generate_insights("goal-1")

        # Should have velocity-related insight
        velocity_insights = [i for i in result if "Velocity" in i or "📈" in i or "📉" in i]
        assert len(velocity_insights) > 0

    def test_insights_with_forecast(self, sample_history):
        """Test that forecast insights are included."""
        result = sample_history.generate_insights("goal-1")

        # Should have forecast-related insight
        forecast_insights = [
            i for i in result
            if "track" in i.lower() or "risk" in i.lower() or "🎯" in i or "⏰" in i
        ]
        assert len(forecast_insights) > 0


class TestHistoryPersistence:
    """Test history file persistence."""

    def test_save_and_load(self, analytics_engine):
        """Test saving and loading history."""
        analytics_engine.record_snapshot("goal-1", completed=5, total=20)
        analytics_engine.record_snapshot("goal-2", completed=3, total=15)

        # Load from file
        history = analytics_engine._load_history()

        assert len(history) == 2
        assert "goal-1" in history
        assert "goal-2" in history

    def test_history_file_format(self, analytics_engine):
        """Test history file is valid JSON."""
        analytics_engine.record_snapshot("goal-1", completed=5, total=20)

        with open(analytics_engine.history_file) as f:
            data = json.load(f)

        assert isinstance(data, dict)
        assert "goal-1" in data

    def test_load_empty_history(self, analytics_engine):
        """Test loading when no history exists."""
        result = analytics_engine._load_history()
        assert result == {}

    def test_load_corrupted_history(self, analytics_engine):
        """Test loading corrupted history file."""
        # Write invalid JSON
        with open(analytics_engine.history_file, "w") as f:
            f.write("invalid json {")

        result = analytics_engine._load_history()
        assert result == {}


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_zero_velocity(self, analytics_engine):
        """Test handling zero velocity."""
        base_date = datetime.now() - timedelta(days=5)

        for i in range(5):
            date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            analytics_engine.record_snapshot("goal-1", completed=0, total=20)

        # Should handle gracefully
        result = analytics_engine.get_velocity_metrics("goal-1")
        assert result is not None
        assert result.average_velocity == 0

    def test_all_tasks_completed(self, analytics_engine):
        """Test when all tasks are completed."""
        analytics_engine.record_snapshot("goal-1", completed=20, total=20)

        result = analytics_engine.forecast_completion("goal-1")
        assert result is not None
        assert result.tasks_remaining == 0
        assert result.probability == 1.0

    def test_negative_dates(self, analytics_engine):
        """Test handling of dates."""
        past_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        # Should handle old dates
        analytics_engine.record_snapshot("goal-1", completed=5, total=20)
        result = analytics_engine.get_burndown_data("goal-1")

        assert result is not None

    def test_large_dataset(self, analytics_engine):
        """Test with large dataset."""
        base_date = datetime.now() - timedelta(days=365)

        for i in range(365):
            date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            analytics_engine.record_snapshot(
                "goal-1",
                completed=min(i // 18, 20),
                total=20,
            )

        # Should handle large history
        result = analytics_engine.get_trend_analysis("goal-1")
        assert result is not None

        result = analytics_engine.forecast_completion("goal-1")
        assert result is not None
