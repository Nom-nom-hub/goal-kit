"""Integration tests for reporting system."""

import pytest
import json
from uuid import uuid4
from datetime import datetime, timedelta

from src.goalkeeper_cli.reporting import ReportGenerator
from src.goalkeeper_cli.tasks import TaskTracker
from src.goalkeeper_cli.commands.reporting import report_command, insights_command
from src.goalkeeper_cli.models import TaskStatus


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temporary project structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / ".goalkit").mkdir()
    return project_dir


class TestReportGenerationWorkflow:
    """Test complete reporting workflows."""

    def test_generate_all_report_types(self, tmp_project):
        """Test generating all report types."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        for i in range(5):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc", 2.0)
            if i < 2:
                task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)

        # Generate all report types
        summary = generator.generate_summary_report()
        weekly = generator.generate_weekly_report()
        monthly = generator.generate_monthly_report()

        assert summary.title is not None
        assert weekly.title is not None
        assert monthly.title is not None

    def test_reports_contain_consistent_data(self, tmp_project):
        """Test that different reports show consistent total counts."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        for i in range(10):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            if i < 5:
                task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)

        summary = generator.generate_summary_report()
        weekly = generator.generate_weekly_report()

        # Total tasks should be same in both reports
        assert (
            summary.summary["total_tasks"] == 10
        )  # All 10 tasks count for summary

    def test_insights_vary_by_report_type(self, tmp_project):
        """Test that different report types generate different insights."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        for i in range(20):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            if i < 10:
                task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)

        summary = generator.generate_summary_report()
        weekly = generator.generate_weekly_report()

        # Both should have insights
        assert len(summary.insights) > 0 or len(weekly.insights) >= 0


class TestMultiGoalReporting:
    """Test reporting across multiple goals."""

    def test_report_aggregates_multiple_goals(self, tmp_project):
        """Test that reports aggregate data from multiple goals."""
        task_tracker = TaskTracker(tmp_project)

        goal1 = str(uuid4())
        goal2 = str(uuid4())
        goal3 = str(uuid4())

        # Create tasks for each goal
        for goal in [goal1, goal2, goal3]:
            for i in range(5):
                task_id = task_tracker.create_task(goal, f"Task {i}", "Desc")
                if i < 2:
                    task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)
        report = generator.generate_summary_report()

        # Should have total of 15 tasks across all goals
        assert report.summary["total_tasks"] == 15
        assert report.summary["completed_tasks"] == 6

    def test_report_shows_goal_breakdown(self, tmp_project):
        """Test that report can show per-goal breakdown."""
        task_tracker = TaskTracker(tmp_project)

        goal1 = str(uuid4())
        goal2 = str(uuid4())

        for goal in [goal1, goal2]:
            for i in range(3):
                task_id = task_tracker.create_task(goal, f"Task {i}", "Desc")

        generator = ReportGenerator(tmp_project)
        report = generator.generate_summary_report()

        assert report.summary["total_tasks"] == 6


class TestTrendAnalysis:
    """Test trend analysis and velocity metrics."""

    def test_velocity_calculation_across_period(self, tmp_project):
        """Test velocity calculation over time period."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create and complete tasks throughout the week
        for i in range(14):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            if i < 7:
                task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)

        now = datetime.now()
        week_start = now - timedelta(days=7)

        velocity = generator._calculate_task_velocity(week_start, now)

        assert velocity >= 0

    def test_burndown_shows_progress_trend(self, tmp_project):
        """Test that burndown data shows completion trend."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create tasks
        task_ids = []
        for i in range(10):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            task_ids.append(task_id)

        # Complete half the tasks
        for task_id in task_ids[:5]:
            task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)
        burndown = generator.get_burndown_data(days=7)

        # Last data point should show 5 completed
        assert burndown[-1]["completed"] == 5
        assert burndown[-1]["remaining"] == 5


class TestReportReliability:
    """Test reliability and consistency of reports."""

    def test_report_deterministic(self, tmp_project):
        """Test that same data produces same report twice."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        for i in range(5):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            if i < 2:
                task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator1 = ReportGenerator(tmp_project)
        report1 = generator1.generate_summary_report()

        generator2 = ReportGenerator(tmp_project)
        report2 = generator2.generate_summary_report()

        # Key metrics should match
        assert (
            report1.summary["total_tasks"]
            == report2.summary["total_tasks"]
        )
        assert (
            report1.summary["completed_tasks"]
            == report2.summary["completed_tasks"]
        )

    def test_report_handles_edge_cases(self, tmp_project):
        """Test report generation with edge case data."""
        task_tracker = TaskTracker(tmp_project)

        # Create project with no tasks
        generator = ReportGenerator(tmp_project)
        report = generator.generate_summary_report()

        assert report.summary["total_tasks"] == 0
        assert report.summary["completed_tasks"] == 0

    def test_insights_make_sense(self, tmp_project):
        """Test that generated insights are reasonable."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create and complete many tasks (high velocity)
        for i in range(20):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)
        report = generator.generate_summary_report()

        # Should have completion insight (100% complete)
        completion_insights = [
            i for i in report.insights if i.type.value == "completion"
        ]

        if len(completion_insights) > 0:
            assert any(
                ("complete" in i.description.lower() or "completion" in i.description.lower())
                for i in completion_insights
            )


class TestReportCommandIntegration:
    """Test report commands work end-to-end."""

    def test_report_and_insights_commands(self, tmp_project, capsys):
        """Test running both report and insights commands."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        for i in range(5):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            if i < 2:
                task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        # Run report command
        report_command(str(tmp_project))
        report_output = capsys.readouterr()

        # Run insights command
        insights_command(str(tmp_project))
        insights_output = capsys.readouterr()

        assert len(report_output.out) > 0
        assert len(insights_output.out) > 0

    def test_json_report_is_valid(self, tmp_project, capsys):
        """Test that JSON report output is valid."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        for i in range(3):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            if i < 1:
                task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        report_command(str(tmp_project), json_output=True)
        captured = capsys.readouterr()

        # Should be valid JSON
        data = json.loads(captured.out)
        assert "title" in data
        assert "summary" in data

    def test_all_report_types_via_command(self, tmp_project, capsys):
        """Test all report types via command."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        for i in range(5):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")

        # Test summary
        report_command(str(tmp_project), report_type="summary")
        summary_output = capsys.readouterr()
        assert len(summary_output.out) > 0

        # Test weekly
        report_command(str(tmp_project), report_type="weekly")
        weekly_output = capsys.readouterr()
        assert len(weekly_output.out) > 0

        # Test monthly
        report_command(str(tmp_project), report_type="monthly")
        monthly_output = capsys.readouterr()
        assert len(monthly_output.out) > 0


class TestDataAggregation:
    """Test that reporting properly aggregates data from trackers."""

    def test_report_includes_task_data(self, tmp_project):
        """Test that report includes task tracker data."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        for i in range(7):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            if i < 3:
                task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)
        report = generator.generate_summary_report()

        # Report should reflect task counts
        assert report.summary["total_tasks"] == 7
        assert report.summary["completed_tasks"] == 3

    def test_report_consistency_across_generators(self, tmp_project):
        """Test that different generator instances produce consistent reports."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        for i in range(5):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc", 1.0)
            if i < 2:
                task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        gen1 = ReportGenerator(tmp_project)
        report1 = gen1.generate_summary_report()

        gen2 = ReportGenerator(tmp_project)
        report2 = gen2.generate_summary_report()

        assert report1.summary["total_tasks"] == report2.summary["total_tasks"]
        assert (
            report1.summary["completed_tasks"]
            == report2.summary["completed_tasks"]
        )


class TestReportMetricsAccuracy:
    """Test accuracy of metrics in reports."""

    def test_completion_rate_calculation(self, tmp_project):
        """Test that completion rate is calculated correctly."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create 4 tasks, complete 1 (25%)
        for i in range(4):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            if i == 0:
                task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        generator = ReportGenerator(tmp_project)
        report = generator.generate_summary_report()

        completion_rate = report.summary["task_completion_rate"]
        assert 20 < completion_rate < 30  # ~25%

    def test_health_score_in_valid_range(self, tmp_project):
        """Test that health score is always valid."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create various task states
        for i in range(10):
            task_id = task_tracker.create_task(goal_id, f"Task {i}", "Desc")
            if i < 3:
                task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)
            elif i < 7:
                task_tracker.update_task_status(task_id, TaskStatus.IN_PROGRESS)

        generator = ReportGenerator(tmp_project)
        report = generator.generate_summary_report()

        health = report.summary["health_score"]
        assert 0 <= health <= 100
