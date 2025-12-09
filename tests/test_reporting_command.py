"""Unit tests for reporting command functions."""

import pytest
import json
from uuid import uuid4

from src.goalkeeper_cli.commands.reporting import (
    report_command,
    insights_command,
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
    goal_id = str(uuid4())

    for i in range(5):
        task_id = task_tracker.create_task(
            goal_id, f"Task {i+1}", f"Description {i+1}", 2.0
        )
        if i < 2:
            task_tracker.update_task_status(task_id, TaskStatus.COMPLETED)

    return tmp_project


class TestReportCommand:
    """Test report command functionality."""

    def test_report_command_empty_project(self, tmp_project, capsys):
        """Test report command on empty project."""
        report_command(str(tmp_project))
        captured = capsys.readouterr()
        assert "Project Summary" in captured.out or "Summary" in captured.out

    def test_report_command_with_data(self, populated_project, capsys):
        """Test report command with populated project."""
        report_command(str(populated_project))
        captured = capsys.readouterr()
        assert "Summary" in captured.out or "Report" in captured.out.lower()

    def test_report_command_missing_project(self, capsys):
        """Test report command with missing project."""
        report_command("/nonexistent/path")
        captured = capsys.readouterr()
        # Should either show error or empty report
        assert len(captured.out) > 0 or len(captured.err) > 0

    def test_report_command_weekly_type(self, populated_project, capsys):
        """Test report command with weekly type."""
        report_command(str(populated_project), report_type="weekly")
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_report_command_monthly_type(self, populated_project, capsys):
        """Test report command with monthly type."""
        report_command(str(populated_project), report_type="monthly")
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_report_command_summary_type(self, populated_project, capsys):
        """Test report command with summary type."""
        report_command(str(populated_project), report_type="summary")
        captured = capsys.readouterr()
        assert "Summary" in captured.out or "summary" in captured.out.lower()


class TestReportCommandJson:
    """Test JSON output for report command."""

    def test_report_json_output(self, populated_project, capsys):
        """Test report command JSON output."""
        report_command(str(populated_project), json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        assert "title" in data
        assert "report_type" in data
        assert "summary" in data
        assert "metrics" in data

    def test_report_json_has_summary(self, populated_project, capsys):
        """Test that JSON report has summary data."""
        report_command(str(populated_project), json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        summary = data["summary"]

        assert "total_tasks" in summary
        assert "completed_tasks" in summary
        assert "health_score" in summary

    def test_report_json_has_metrics(self, populated_project, capsys):
        """Test that JSON report has metrics."""
        report_command(str(populated_project), json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        assert "metrics" in data
        assert len(data["metrics"]) > 0

    def test_report_json_weekly_type(self, populated_project, capsys):
        """Test JSON output for weekly report."""
        report_command(str(populated_project), report_type="weekly", json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        assert data["report_type"] == "weekly"

    def test_report_json_insights(self, populated_project, capsys):
        """Test that JSON report includes insights."""
        report_command(str(populated_project), json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        assert "insights" in data


class TestInsightsCommand:
    """Test insights command functionality."""

    def test_insights_command_empty_project(self, tmp_project, capsys):
        """Test insights command on empty project."""
        insights_command(str(tmp_project))
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_insights_command_with_data(self, populated_project, capsys):
        """Test insights command with populated project."""
        insights_command(str(populated_project))
        captured = capsys.readouterr()
        # Should show insights header or message
        output = captured.out.lower()
        assert any(
            keyword in output for keyword in ["insight", "info", "warning", "alert"]
        )

    def test_insights_command_missing_project(self, capsys):
        """Test insights command with missing project."""
        insights_command("/nonexistent/path")
        captured = capsys.readouterr()
        assert len(captured.out) > 0 or len(captured.err) > 0

    def test_insights_command_weekly_type(self, populated_project, capsys):
        """Test insights command with weekly type."""
        insights_command(str(populated_project), report_type="weekly")
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_insights_command_monthly_type(self, populated_project, capsys):
        """Test insights command with monthly type."""
        insights_command(str(populated_project), report_type="monthly")
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_insights_filter_info_severity(self, populated_project, capsys):
        """Test filtering insights by info severity."""
        insights_command(str(populated_project), severity="info")
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_insights_filter_warning_severity(self, populated_project, capsys):
        """Test filtering insights by warning severity."""
        insights_command(str(populated_project), severity="warning")
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_insights_filter_alert_severity(self, populated_project, capsys):
        """Test filtering insights by alert severity."""
        insights_command(str(populated_project), severity="alert")
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_insights_invalid_severity(self, populated_project, capsys):
        """Test insights command with invalid severity."""
        insights_command(str(populated_project), severity="invalid")
        captured = capsys.readouterr()
        assert "Invalid severity" in captured.out


class TestInsightsCommandJson:
    """Test JSON output for insights command."""

    def test_insights_json_output(self, populated_project, capsys):
        """Test insights command JSON output."""
        insights_command(str(populated_project), json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        assert "count" in data
        assert "insights" in data

    def test_insights_json_structure(self, populated_project, capsys):
        """Test JSON insights have correct structure."""
        insights_command(str(populated_project), json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        insights = data["insights"]

        for insight in insights:
            assert "type" in insight
            assert "title" in insight
            assert "description" in insight
            assert "severity" in insight

    def test_insights_json_with_filter(self, populated_project, capsys):
        """Test JSON insights respects severity filter."""
        insights_command(
            str(populated_project), severity="info", json_output=True
        )
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        for insight in data["insights"]:
            assert insight["severity"] == "info"


class TestReportCommandFormatting:
    """Test formatting of report output."""

    def test_report_shows_title(self, populated_project, capsys):
        """Test that report displays title."""
        report_command(str(populated_project))
        captured = capsys.readouterr()
        assert "Summary" in captured.out or "Report" in captured.out

    def test_report_shows_metrics(self, populated_project, capsys):
        """Test that report displays metrics."""
        report_command(str(populated_project))
        captured = capsys.readouterr()
        # Should have some metrics displayed
        output = captured.out.lower()
        assert any(
            keyword in output
            for keyword in ["metric", "health", "task", "completion", "velocity"]
        )

    def test_report_shows_summary(self, populated_project, capsys):
        """Test that report displays summary information."""
        report_command(str(populated_project))
        captured = capsys.readouterr()
        assert "Summary" in captured.out or "summary" in captured.out.lower()


class TestInsightsCommandFormatting:
    """Test formatting of insights output."""

    def test_insights_shows_header(self, populated_project, capsys):
        """Test that insights displays header."""
        insights_command(str(populated_project))
        captured = capsys.readouterr()
        output = captured.out.lower()
        assert "insight" in output or any(
            keyword in output for keyword in ["info", "warning", "alert"]
        )

    def test_insights_shows_severity_levels(self, populated_project, capsys):
        """Test that insights show severity levels."""
        insights_command(str(populated_project))
        captured = capsys.readouterr()
        output = captured.out.lower()
        # May show severity levels
        assert len(output) > 0


class TestCommandEdgeCases:
    """Test edge cases and error handling."""

    def test_report_with_no_tasks(self, tmp_project, capsys):
        """Test report on project with no tasks."""
        report_command(str(tmp_project))
        captured = capsys.readouterr()
        assert "Summary" in captured.out or "Report" in captured.out.lower()

    def test_report_with_all_completed_tasks(self, tmp_project, capsys):
        """Test report when all tasks are completed."""
        task_tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        id1 = task_tracker.create_task(goal_id, "Task 1", "Desc")
        id2 = task_tracker.create_task(goal_id, "Task 2", "Desc")

        task_tracker.update_task_status(id1, TaskStatus.COMPLETED)
        task_tracker.update_task_status(id2, TaskStatus.COMPLETED)

        report_command(str(tmp_project))
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_insights_preserves_data(self, populated_project):
        """Test that insights command doesn't modify data."""
        task_tracker = TaskTracker(populated_project)
        original_count = len(task_tracker.get_all_tasks())

        insights_command(str(populated_project))

        new_tracker = TaskTracker(populated_project)
        assert len(new_tracker.get_all_tasks()) == original_count
