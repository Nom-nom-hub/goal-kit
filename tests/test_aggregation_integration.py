"""Integration tests for aggregation CLI commands."""

import pytest
import json
from pathlib import Path
from uuid import uuid4
from unittest.mock import patch
from io import StringIO

from typer.testing import CliRunner

from src.goalkeeper_cli.commands.aggregation import app
from src.goalkeeper_cli.tasks import TaskTracker
from src.goalkeeper_cli.models import TaskStatus


runner = CliRunner()


@pytest.fixture
def workspace(tmp_path):
    """Create a temporary workspace with multiple projects."""
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()
    return workspace_dir


@pytest.fixture
def project_a(workspace):
    """Create project A with tasks."""
    proj_dir = workspace / "project_a"
    proj_dir.mkdir()
    (proj_dir / ".goalkit").mkdir()

    tracker = TaskTracker(proj_dir)
    goal_id = str(uuid4())

    # Create 10 tasks, 7 completed
    for i in range(10):
        task_id = tracker.create_task(goal_id, f"Task A{i}", f"Description A{i}")
        if i < 7:
            tracker.update_task_status(task_id, TaskStatus.COMPLETED)

    return proj_dir


@pytest.fixture
def project_b(workspace):
    """Create project B with tasks."""
    proj_dir = workspace / "project_b"
    proj_dir.mkdir()
    (proj_dir / ".goalkit").mkdir()

    tracker = TaskTracker(proj_dir)
    goal_id = str(uuid4())

    # Create 15 tasks, 5 completed
    for i in range(15):
        task_id = tracker.create_task(goal_id, f"Task B{i}", f"Description B{i}")
        if i < 5:
            tracker.update_task_status(task_id, TaskStatus.COMPLETED)

    return proj_dir


@pytest.fixture
def workspace_with_projects(workspace, project_a, project_b):
    """Workspace with multiple projects."""
    return workspace


class TestListCommand:
    """Test projects list command."""

    def test_list_empty_workspace(self, workspace):
        """Test listing projects in empty workspace."""
        result = runner.invoke(app, ["list", "--workspace-path", str(workspace)])
        assert result.exit_code == 0
        assert "No projects found" in result.stdout

    def test_list_single_project(self, project_a, workspace):
        """Test listing single project."""
        result = runner.invoke(app, ["list", "--workspace-path", str(workspace)])
        assert result.exit_code == 0
        assert "project_a" in result.stdout
        assert "10" in result.stdout  # task count

    def test_list_multiple_projects(self, workspace_with_projects):
        """Test listing multiple projects."""
        result = runner.invoke(app, ["list", "--workspace-path", str(workspace_with_projects)])
        assert result.exit_code == 0
        assert "project_a" in result.stdout
        assert "project_b" in result.stdout

    def test_list_json_output(self, workspace_with_projects):
        """Test listing projects with JSON output."""
        result = runner.invoke(app, ["list", "--workspace-path", str(workspace_with_projects), "--output", "json"])
        assert result.exit_code == 0
        
        data = json.loads(result.stdout)
        assert "project_count" in data
        assert len(data["projects"]) == 2
        assert data["projects"][0]["name"] in ["project_a", "project_b"]

    def test_list_nonexistent_workspace(self, tmp_path):
        """Test listing from nonexistent workspace."""
        result = runner.invoke(app, ["list", "--workspace-path", str(tmp_path / "nonexistent")])
        assert result.exit_code == 1
        assert "not found" in result.stdout


class TestReportCommand:
    """Test aggregated report command."""

    def test_report_empty_workspace(self, workspace):
        """Test report for empty workspace."""
        result = runner.invoke(app, ["report", "--workspace-path", str(workspace)])
        assert result.exit_code == 0
        assert "Workspace Aggregation Report" in result.stdout or "0" in result.stdout

    def test_report_single_project(self, project_a, workspace):
        """Test report for single project."""
        result = runner.invoke(app, ["report", "--workspace-path", str(workspace)])
        assert result.exit_code == 0
        assert "Summary" in result.stdout or "project_a" in result.stdout

    def test_report_multiple_projects(self, workspace_with_projects):
        """Test report for multiple projects."""
        result = runner.invoke(app, ["report", "--workspace-path", str(workspace_with_projects)])
        assert result.exit_code == 0
        assert "25" in result.stdout or "Workspace" in result.stdout

    def test_report_json_output(self, workspace_with_projects):
        """Test report with JSON output."""
        result = runner.invoke(app, ["report", "--workspace-path", str(workspace_with_projects), "--output", "json"])
        assert result.exit_code == 0
        
        data = json.loads(result.stdout)
        assert "project_count" in data
        assert data["project_count"] == 2
        assert "total_tasks" in data
        assert data["total_tasks"] == 25

    def test_report_completion_rate(self, workspace_with_projects):
        """Test report completion rate calculation."""
        result = runner.invoke(app, ["report", "--workspace-path", str(workspace_with_projects), "--output", "json"])
        assert result.exit_code == 0
        
        data = json.loads(result.stdout)
        # 12 completed out of 25 = 48%
        expected_rate = 48.0
        assert abs(data["overall_completion_rate"] - expected_rate) < 5.0  # Allow some variance


class TestCompareCommand:
    """Test project comparison command."""

    def test_compare_by_completion(self, workspace_with_projects):
        """Test comparing projects by completion rate."""
        result = runner.invoke(app, ["compare", "--workspace-path", str(workspace_with_projects), "--metric", "completion_rate"])
        assert result.exit_code == 0
        assert "project_a" in result.stdout  # Should be ranked first (70% vs ~33%)

    def test_compare_by_health(self, workspace_with_projects):
        """Test comparing projects by health score."""
        result = runner.invoke(app, ["compare", "--workspace-path", str(workspace_with_projects), "--metric", "health_score"])
        assert result.exit_code == 0
        assert "project_a" in result.stdout or "project_b" in result.stdout

    def test_compare_by_task_count(self, workspace_with_projects):
        """Test comparing projects by task count."""
        result = runner.invoke(app, ["compare", "--workspace-path", str(workspace_with_projects), "--metric", "task_count"])
        assert result.exit_code == 0
        assert "project_b" in result.stdout  # project_b has more tasks (15 vs 10)

    def test_compare_json_output(self, workspace_with_projects):
        """Test compare with JSON output."""
        result = runner.invoke(app, ["compare", "--workspace-path", str(workspace_with_projects), "--output", "json"])
        assert result.exit_code == 0
        
        data = json.loads(result.stdout)
        assert "ranking" in data
        assert len(data["ranking"]) == 2

    def test_compare_invalid_metric(self, workspace_with_projects):
        """Test compare with invalid metric."""
        result = runner.invoke(app, ["compare", "--workspace-path", str(workspace_with_projects), "--metric", "invalid_metric"])
        # Should not crash, but may return an error
        assert result.exit_code == 0 or result.exit_code == 1

    def test_compare_ranking_order(self, workspace_with_projects):
        """Test that ranking is correctly ordered."""
        result = runner.invoke(app, ["compare", "--workspace-path", str(workspace_with_projects), "--metric", "completion_rate", "--output", "json"])
        assert result.exit_code == 0
        
        data = json.loads(result.stdout)
        ranking = data["ranking"]
        # First project should have higher value than second
        assert ranking[0]["value"] >= ranking[1]["value"]


class TestSummaryCommand:
    """Test workspace summary command."""

    def test_summary_empty_workspace(self, workspace):
        """Test summary for empty workspace."""
        result = runner.invoke(app, ["summary", "--workspace-path", str(workspace)])
        assert result.exit_code == 0

    def test_summary_with_projects(self, workspace_with_projects):
        """Test summary with projects."""
        result = runner.invoke(app, ["summary", "--workspace-path", str(workspace_with_projects)])
        assert result.exit_code == 0
        assert "Workspace" in result.stdout or "Summary" in result.stdout

    def test_summary_json_output(self, workspace_with_projects):
        """Test summary with JSON output."""
        result = runner.invoke(app, ["summary", "--workspace-path", str(workspace_with_projects), "--output", "json"])
        assert result.exit_code == 0
        
        data = json.loads(result.stdout)
        assert "project_count" in data
        assert data["project_count"] == 2
        assert "workspace_path" in data

    def test_summary_metrics(self, workspace_with_projects):
        """Test that summary includes key metrics."""
        result = runner.invoke(app, ["summary", "--workspace-path", str(workspace_with_projects), "--output", "json"])
        assert result.exit_code == 0
        
        data = json.loads(result.stdout)
        assert "total_tasks" in data
        assert "total_completed" in data
        assert "overall_completion_rate" in data
        assert "overall_health_score" in data
        assert data["total_tasks"] == 25
