"""Tests for multi-project aggregation functionality."""

import pytest
from pathlib import Path
from uuid import uuid4

from src.goalkeeper_cli.aggregation import AggregationEngine, ProjectSummary
from src.goalkeeper_cli.tasks import TaskTracker
from src.goalkeeper_cli.models import TaskStatus


@pytest.fixture
def workspace(tmp_path):
    """Create a temporary workspace with multiple projects."""
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()
    return workspace_dir


@pytest.fixture
def project_a(workspace):
    """Create project A with some tasks."""
    proj_dir = workspace / "project_a"
    proj_dir.mkdir()
    (proj_dir / ".goalkit").mkdir()

    tracker = TaskTracker(proj_dir)
    goal_id = str(uuid4())

    # Create 10 tasks, 7 completed
    for i in range(10):
        task_id = tracker.create_task(goal_id, f"Task A{i}", f"Desc {i}")
        if i < 7:
            tracker.update_task_status(task_id, TaskStatus.COMPLETED)

    return proj_dir


@pytest.fixture
def project_b(workspace):
    """Create project B with some tasks."""
    proj_dir = workspace / "project_b"
    proj_dir.mkdir()
    (proj_dir / ".goalkit").mkdir()

    tracker = TaskTracker(proj_dir)
    goal_id = str(uuid4())

    # Create 15 tasks, 5 completed
    for i in range(15):
        task_id = tracker.create_task(goal_id, f"Task B{i}", f"Desc {i}")
        if i < 5:
            tracker.update_task_status(task_id, TaskStatus.COMPLETED)

    return proj_dir


@pytest.fixture
def workspace_with_projects(workspace, project_a, project_b):
    """Workspace with multiple projects."""
    return workspace


class TestDiscoverProjects:
    """Test project discovery."""

    def test_discover_empty_workspace(self, workspace):
        """Test discovering projects in empty workspace."""
        engine = AggregationEngine(workspace)
        projects = engine.discover_projects()

        assert projects == []

    def test_discover_single_project(self, project_a, workspace):
        """Test discovering a single project."""
        engine = AggregationEngine(workspace)
        projects = engine.discover_projects()

        assert len(projects) == 1
        assert projects[0].name == "project_a"
        assert projects[0].task_count == 10

    def test_discover_multiple_projects(self, workspace_with_projects):
        """Test discovering multiple projects."""
        engine = AggregationEngine(workspace_with_projects)
        projects = engine.discover_projects()

        assert len(projects) == 2
        assert projects[0].name == "project_a"
        assert projects[1].name == "project_b"

    def test_discover_ignores_non_projects(self, workspace):
        """Test that non-projects are ignored."""
        # Create a directory without .goalkit
        (workspace / "not_a_project").mkdir()

        engine = AggregationEngine(workspace)
        projects = engine.discover_projects()

        assert projects == []

    def test_project_summary_accuracy(self, project_a, workspace):
        """Test that project summary is accurate."""
        engine = AggregationEngine(workspace)
        projects = engine.discover_projects()

        assert len(projects) == 1
        project = projects[0]
        assert project.task_count == 10
        assert project.completed_tasks == 7
        assert project.completion_rate == 70.0


class TestAggregateReports:
    """Test report aggregation."""

    def test_aggregate_empty_workspace(self, workspace):
        """Test aggregating empty workspace."""
        engine = AggregationEngine(workspace)
        report = engine.aggregate_reports()

        assert report.project_count == 0
        assert report.total_tasks == 0

    def test_aggregate_single_project(self, project_a, workspace):
        """Test aggregating single project."""
        engine = AggregationEngine(workspace)
        projects = engine.discover_projects()
        report = engine.aggregate_reports(projects)

        assert report.project_count == 1
        assert report.total_tasks == 10
        assert report.total_completed == 7

    def test_aggregate_multiple_projects(self, workspace_with_projects):
        """Test aggregating multiple projects."""
        engine = AggregationEngine(workspace_with_projects)
        projects = engine.discover_projects()
        report = engine.aggregate_reports(projects)

        assert report.project_count == 2
        assert report.total_tasks == 25  # 10 + 15
        assert report.total_completed == 12  # 7 + 5

    def test_aggregate_completion_rate(self, workspace_with_projects):
        """Test aggregated completion rate calculation."""
        engine = AggregationEngine(workspace_with_projects)
        projects = engine.discover_projects()
        report = engine.aggregate_reports(projects)

        expected_rate = (12 / 25) * 100
        assert abs(report.overall_completion_rate - expected_rate) < 0.1

    def test_aggregate_health_score(self, workspace_with_projects):
        """Test aggregated health score."""
        engine = AggregationEngine(workspace_with_projects)
        projects = engine.discover_projects()
        report = engine.aggregate_reports(projects)

        # Should be average of project health scores
        assert 0 <= report.overall_health_score <= 100

    def test_task_distribution(self, workspace_with_projects):
        """Test task distribution in aggregated report."""
        engine = AggregationEngine(workspace_with_projects)
        projects = engine.discover_projects()
        report = engine.aggregate_reports(projects)

        dist = report.task_distribution
        assert dist.get("completed", 0) == 12
        assert dist.get("todo", 0) == 13
        assert dist.get("in_progress", 0) == 0


class TestProjectComparison:
    """Test project comparison."""

    def test_comparison_empty_workspace(self, workspace):
        """Test comparison with no projects."""
        engine = AggregationEngine(workspace)
        comparison = engine.get_project_comparison()

        assert comparison == {}

    def test_comparison_single_project(self, project_a, workspace):
        """Test comparison with single project."""
        engine = AggregationEngine(workspace)
        projects = engine.discover_projects()
        comparison = engine.get_project_comparison(projects)

        assert "project_a" in comparison
        assert comparison["project_a"]["task_count"] == 10
        assert comparison["project_a"]["completion_rate"] == 70.0

    def test_comparison_multiple_projects(self, workspace_with_projects):
        """Test comparison of multiple projects."""
        engine = AggregationEngine(workspace_with_projects)
        projects = engine.discover_projects()
        comparison = engine.get_project_comparison(projects)

        assert len(comparison) == 2
        assert "project_a" in comparison
        assert "project_b" in comparison


class TestProjectRanking:
    """Test project ranking."""

    def test_rank_by_completion(self, workspace_with_projects):
        """Test ranking projects by completion rate."""
        engine = AggregationEngine(workspace_with_projects)
        projects = engine.discover_projects()
        ranking = engine.get_project_ranking(projects, metric="completion_rate")

        assert len(ranking) == 2
        # project_a (70%) should rank higher than project_b (~33%)
        assert ranking[0][0] == "project_a"
        assert ranking[1][0] == "project_b"

    def test_rank_by_health_score(self, workspace_with_projects):
        """Test ranking projects by health score."""
        engine = AggregationEngine(workspace_with_projects)
        projects = engine.discover_projects()
        ranking = engine.get_project_ranking(projects, metric="health_score")

        assert len(ranking) == 2
        assert ranking[0][0] == "project_a"  # Higher health

    def test_rank_by_task_count(self, workspace_with_projects):
        """Test ranking projects by task count."""
        engine = AggregationEngine(workspace_with_projects)
        projects = engine.discover_projects()
        ranking = engine.get_project_ranking(projects, metric="task_count")

        assert len(ranking) == 2
        # project_b (15 tasks) ranks higher than project_a (10 tasks)
        assert ranking[0][0] == "project_b"
        assert ranking[1][0] == "project_a"

    def test_invalid_metric_ignored(self, workspace_with_projects):
        """Test that invalid metrics are ignored."""
        engine = AggregationEngine(workspace_with_projects)
        projects = engine.discover_projects()
        ranking = engine.get_project_ranking(projects, metric="invalid_metric")

        assert ranking == []


class TestWorkspaceSummary:
    """Test workspace-level summary."""

    def test_summary_empty_workspace(self, workspace):
        """Test summary of empty workspace."""
        engine = AggregationEngine(workspace)
        summary = engine.get_workspace_summary()

        assert summary["project_count"] == 0
        assert summary["total_tasks"] == 0

    def test_summary_with_projects(self, workspace_with_projects):
        """Test summary with multiple projects."""
        engine = AggregationEngine(workspace_with_projects)
        summary = engine.get_workspace_summary()

        assert summary["project_count"] == 2
        assert summary["total_tasks"] == 25
        assert summary["total_completed"] == 12
        assert "projects" in summary
        assert len(summary["projects"]) == 2

    def test_summary_has_timestamp(self, workspace_with_projects):
        """Test that summary includes generation timestamp."""
        engine = AggregationEngine(workspace_with_projects)
        summary = engine.get_workspace_summary()

        assert "generated_at" in summary


class TestEdgeCases:
    """Test edge cases in aggregation."""

    def test_workspace_with_corrupted_project(self, workspace, project_a):
        """Test handling of corrupted project directory."""
        # Create a .goalkit directory without proper structure
        bad_proj = workspace / "bad_project"
        bad_proj.mkdir()
        (bad_proj / ".goalkit").mkdir()

        engine = AggregationEngine(workspace)
        projects = engine.discover_projects()

        # Should discover both projects (bad_project gets default values)
        assert len(projects) == 2
        project_names = [p.name for p in projects]
        assert "project_a" in project_names
        assert "bad_project" in project_names
        
        # Bad project should have graceful defaults
        bad = next(p for p in projects if p.name == "bad_project")
        assert bad.task_count == 0
        assert bad.completed_tasks == 0

    def test_nonexistent_workspace(self, tmp_path):
        """Test with nonexistent workspace path."""
        engine = AggregationEngine(tmp_path / "nonexistent")
        projects = engine.discover_projects()

        assert projects == []

    def test_sorted_project_names(self, workspace):
        """Test that projects are returned in sorted order."""
        # Create projects in non-alphabetical order
        proj_z = workspace / "zproject"
        proj_z.mkdir()
        (proj_z / ".goalkit").mkdir()

        proj_a = workspace / "aproject"
        proj_a.mkdir()
        (proj_a / ".goalkit").mkdir()

        engine = AggregationEngine(workspace)
        projects = engine.discover_projects()

        assert projects[0].name == "aproject"
        assert projects[1].name == "zproject"
