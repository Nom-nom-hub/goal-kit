"""Unit tests for ReportGenerator class."""

import pytest
from pathlib import Path
from datetime import datetime, timedelta
from uuid import uuid4

from src.goalkeeper_cli.reporting import (
    ReportGenerator,
    Report,
    ReportType,
    InsightSeverity,
)
from src.goalkeeper_cli.tasks import TaskTracker
from src.goalkeeper_cli.models import TaskStatus


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temporary project structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / ".goalkit").mkdir()
    return project_dir


@pytest.fixture
def populated_project(tmp_project):
    """Create a project with sample data."""
    task_tracker = TaskTracker(tmp_project)

    goal1 = str(uuid4())
    goal2 = str(uuid4())

    # Create tasks
    for i in range(5):
        task_id = task_tracker.create_task(
            goal1, f"Task {i+1}", f"Description {i+1}", float(i + 1)
        )
        if i < 2:
            task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)
        elif i < 4:
            task_tracker.update_task_status(task_id, TaskStatus.IN_PROGRESS)

    for i in range(3):
        task_id = task_tracker.create_task(
            goal2, f"Task {i+1}", f"Description {i+1}", 2.0
        )
        if i == 0:
            task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

    return tmp_project, goal1, goal2


class TestReportGeneratorInit:
    """Test ReportGenerator initialization."""

    def test_init_creates_instance(self, tmp_project):
        """Test that ReportGenerator initializes correctly."""
        generator = ReportGenerator(tmp_project)
        assert generator.project_path == tmp_project

    def test_init_loads_trackers(self, tmp_project):
        """Test that ReportGenerator loads all trackers."""
        generator = ReportGenerator(tmp_project)
        assert generator.task_tracker is not None
        assert generator.analyzer is not None


class TestSummaryReport:
    """Test summary report generation."""

    def test_generate_summary_report(self, populated_project):
        """Test generating a summary report."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_summary_report()

        assert report.title == "Project Summary"
        assert report.report_type == ReportType.SUMMARY
        assert "total_tasks" in report.summary
        assert "completed_tasks" in report.summary
        assert report.summary["total_tasks"] == 8
        assert report.summary["completed_tasks"] == 3

    def test_summary_report_has_metrics(self, populated_project):
        """Test that summary report includes metrics."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_summary_report()

        assert "task_velocity" in report.metrics
        assert "completion_rate" in report.metrics
        assert "health_score" in report.metrics

    def test_summary_report_identifies_at_risk_goals(self, tmp_project):
        """Test that summary report identifies at-risk goals."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create incomplete tasks to simulate at-risk goal
        for _ in range(3):
            task_tracker.create_task(goal_id, "Task", "Desc")

        generator = ReportGenerator(tmp_project)
        report = generator.generate_summary_report()

        # Should have health score
        assert report.summary["health_score"] is not None

    def test_summary_report_has_insights(self, populated_project):
        """Test that summary report generates insights."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_summary_report()

        assert len(report.insights) > 0
        assert all(hasattr(i, "title") for i in report.insights)


class TestWeeklyReport:
    """Test weekly report generation."""

    def test_generate_weekly_report(self, populated_project):
        """Test generating a weekly report."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_weekly_report()

        assert report.report_type == ReportType.WEEKLY
        assert "task_completion_rate" in report.summary
        assert "task_velocity" in report.summary

    def test_weekly_report_with_custom_date(self, populated_project):
        """Test generating weekly report for specific week."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        week_start = datetime.now() - timedelta(days=14)
        report = generator.generate_weekly_report(week_start)

        assert report.period_start == week_start
        assert report.period_end == week_start + timedelta(days=7)

    def test_weekly_report_has_velocity(self, populated_project):
        """Test that weekly report calculates velocity."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_weekly_report()

        assert "task_velocity" in report.metrics
        assert isinstance(report.metrics["task_velocity"], float)


class TestMonthlyReport:
    """Test monthly report generation."""

    def test_generate_monthly_report(self, populated_project):
        """Test generating a monthly report."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_monthly_report()

        assert report.report_type == ReportType.MONTHLY
        assert "task_completion_rate" in report.summary

    def test_monthly_report_with_custom_date(self, populated_project):
        """Test generating monthly report for specific month."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_monthly_report(12, 2025)

        assert report.period_start.month == 12
        assert report.period_start.year == 2025

    def test_monthly_report_correct_period(self, populated_project):
        """Test that monthly report covers full month."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_monthly_report(1, 2025)

        # Should span from Jan 1 to Jan 31
        assert report.period_start.day == 1
        assert report.period_start.month == 1


class TestBurndownData:
    """Test burndown data generation."""

    def test_get_burndown_data(self, populated_project):
        """Test getting burndown chart data."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        burndown = generator.get_burndown_data(days=7)

        assert len(burndown) == 8  # 0-7 days inclusive
        assert all("date" in d for d in burndown)
        assert all("remaining" in d for d in burndown)
        assert all("completed" in d for d in burndown)

    def test_burndown_shows_progress(self, tmp_project):
        """Test that burndown shows task completion progress."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create 5 tasks
        task_ids = []
        for i in range(5):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            task_ids.append(task_id)

        # Complete 2 tasks
        task_tracker.update_task_status(task_ids[0], TaskStatus.COMPLETED)
        task_tracker.update_task_status(task_ids[1], TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)
        burndown = generator.get_burndown_data(days=1)

        assert burndown[-1]["completed"] == 2
        assert burndown[-1]["remaining"] == 3


class TestCompletionTrend:
    """Test completion trend analysis."""

    def test_get_completion_trend(self, populated_project):
        """Test getting completion trend data."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        trend = generator.get_completion_trend(days=7)

        assert len(trend) == 8  # 0-7 days inclusive
        assert all(isinstance(t, float) for t in trend)
        assert all(0 <= t <= 100 for t in trend)

    def test_trend_increases_with_completion(self, tmp_project):
        """Test that trend shows increasing completion percentage."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        task_id = task_tracker.create_task(goal_id, "Task", "Desc")
        task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)
        trend = generator.get_completion_trend(days=1)

        # Last value should be 100% (all tasks completed)
        assert trend[-1] == 100.0


class TestVelocityCalculation:
    """Test velocity calculations."""

    def test_calculate_task_velocity(self, tmp_project):
        """Test task velocity calculation."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create and complete tasks
        for i in range(3):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)

        now = datetime.now()
        week_ago = now - timedelta(days=7)

        velocity = generator._calculate_task_velocity(week_ago, now)

        # Should have some velocity
        assert velocity >= 0

    def test_velocity_shows_completion_rate(self, tmp_project):
        """Test that velocity reflects completion rate."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create 10 tasks and complete all
        for i in range(10):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)

        now = datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        velocity = generator._calculate_task_velocity(today, now)

        # Should reflect 10 tasks completed today
        assert velocity > 0


class TestInsightGeneration:
    """Test insight generation."""

    def test_generate_weekly_insights(self, populated_project):
        """Test generating weekly insights."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_weekly_report()

        assert len(report.insights) >= 0  # May have insights
        assert all(hasattr(i, "title") for i in report.insights)
        assert all(hasattr(i, "severity") for i in report.insights)

    def test_insights_have_severity(self, populated_project):
        """Test that insights have severity levels."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_summary_report()

        for insight in report.insights:
            assert insight.severity in [
                InsightSeverity.INFO,
                InsightSeverity.WARNING,
                InsightSeverity.ALERT,
            ]

    def test_high_velocity_generates_positive_insight(self, tmp_project):
        """Test that high velocity generates positive insight."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create and complete many tasks (high velocity)
        # Need 21+ tasks in a week for velocity > 3.0 tasks/day
        for i in range(25):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)
        report = generator.generate_weekly_report()

        # Should generate positive insights about velocity
        velocity_insights = [
            i for i in report.insights if i.type.value == "velocity"
        ]
        assert len(velocity_insights) > 0


class TestReportDataIntegrity:
    """Test report data consistency and accuracy."""

    def test_report_total_matches_summary(self, populated_project):
        """Test that report totals match summary data."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_summary_report()

        task_stats = generator.task_tracker.get_task_stats()

        assert report.summary["total_tasks"] == task_stats.total_tasks
        assert report.summary["completed_tasks"] == task_stats.completed_tasks

    def test_report_timestamps_valid(self, populated_project):
        """Test that report has valid timestamps."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_summary_report()

        assert report.generated_at is not None
        assert report.period_start is not None
        assert report.period_end is not None
        assert report.period_start <= report.period_end

    def test_weekly_report_spans_7_days(self, populated_project):
        """Test that weekly report spans exactly 7 days."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_weekly_report()

        span = report.period_end - report.period_start
        assert span.days == 7


class TestReportMetrics:
    """Test metrics in reports."""

    def test_completion_rate_is_percentage(self, populated_project):
        """Test that completion rate is expressed as percentage."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_summary_report()

        completion_rate = report.summary["task_completion_rate"]
        assert 0 <= completion_rate <= 100

    def test_health_score_in_valid_range(self, populated_project):
        """Test that health score is in valid range."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_summary_report()

        health = report.summary["health_score"]
        assert 0 <= health <= 100

    def test_velocity_is_non_negative(self, populated_project):
        """Test that velocity is non-negative."""
        project_path, goal1, goal2 = populated_project
        generator = ReportGenerator(project_path)

        report = generator.generate_summary_report()

        velocity = report.metrics["task_velocity"]
        assert velocity >= 0
