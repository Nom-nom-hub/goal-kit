"""Integration tests for dependency tracking and CLI commands."""

import pytest
from pathlib import Path
from uuid import uuid4
from typer.testing import CliRunner

from src.goalkeeper_cli.dependencies import DependencyTracker
from src.goalkeeper_cli.commands.dependencies import app
from src.goalkeeper_cli.tasks import TaskTracker
from src.goalkeeper_cli.models import TaskStatus


runner = CliRunner()


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temporary project structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / ".goalkit").mkdir()
    return project_dir


@pytest.fixture
def project_with_tasks(tmp_project):
    """Create a project with tasks in a dependency chain."""
    tracker = TaskTracker(tmp_project)
    goal_id = str(uuid4())
    
    # Create task chain: task0 <- task1 <- task2
    task0_id = tracker.create_task(goal_id, "Write spec", "Design the feature")
    task1_id = tracker.create_task(goal_id, "Implement", "Build the feature")
    task2_id = tracker.create_task(goal_id, "Test", "Test the feature")
    
    # Add dependencies
    dep_tracker = DependencyTracker(tmp_project, tracker)
    dep_tracker.add_dependency(task1_id, task0_id)
    dep_tracker.add_dependency(task2_id, task1_id)
    
    return tmp_project, task0_id, task1_id, task2_id


class TestBlockingCommand:
    """Test the blocking tasks command."""

    def test_blocking_command_no_tasks(self, tmp_project):
        """Test blocking command with no tasks."""
        result = runner.invoke(app, ["blocking", "--project-path", str(tmp_project)])
        
        assert result.exit_code == 0
        assert "No blocking tasks" in result.stdout

    def test_blocking_command_with_dependencies(self, project_with_tasks):
        """Test blocking command shows blocking tasks."""
        tmp_project, task0_id, task1_id, task2_id = project_with_tasks
        
        result = runner.invoke(app, ["blocking", "--project-path", str(tmp_project)])
        
        assert result.exit_code == 0
        assert "Blocking Tasks" in result.stdout

    def test_blocking_command_json(self, project_with_tasks):
        """Test blocking command with JSON output."""
        tmp_project, task0_id, task1_id, task2_id = project_with_tasks
        
        result = runner.invoke(
            app, ["blocking", "--project-path", str(tmp_project), "--output", "json"]
        )
        
        assert result.exit_code == 0
        assert '"blocking_tasks"' in result.stdout


class TestCriticalPathCommand:
    """Test the critical path command."""

    def test_critical_path_no_dependencies(self, tmp_project):
        """Test critical path with no dependencies."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())
        tracker.create_task(goal_id, "Task 1", "Do something")
        
        result = runner.invoke(app, ["critical-path", "--project-path", str(tmp_project)])
        
        assert result.exit_code == 0

    def test_critical_path_with_chain(self, project_with_tasks):
        """Test critical path with dependency chain."""
        tmp_project, task0_id, task1_id, task2_id = project_with_tasks
        
        result = runner.invoke(app, ["critical-path", "--project-path", str(tmp_project)])
        
        assert result.exit_code == 0
        assert "Critical Path" in result.stdout

    def test_critical_path_json(self, project_with_tasks):
        """Test critical path with JSON output."""
        tmp_project, task0_id, task1_id, task2_id = project_with_tasks
        
        result = runner.invoke(
            app, ["critical-path", "--project-path", str(tmp_project), "--output", "json"]
        )
        
        assert result.exit_code == 0
        assert '"critical_path"' in result.stdout


class TestGraphCommand:
    """Test the dependency graph command."""

    def test_graph_command_empty(self, tmp_project):
        """Test graph command with no dependencies."""
        result = runner.invoke(app, ["graph", "--project-path", str(tmp_project)])
        
        assert result.exit_code == 0

    def test_graph_command_with_dependencies(self, project_with_tasks):
        """Test graph command shows dependencies."""
        tmp_project, task0_id, task1_id, task2_id = project_with_tasks
        
        result = runner.invoke(app, ["graph", "--project-path", str(tmp_project)])
        
        assert result.exit_code == 0

    def test_graph_command_single_task(self, project_with_tasks):
        """Test graph command for single task."""
        tmp_project, task0_id, task1_id, task2_id = project_with_tasks
        
        result = runner.invoke(
            app, ["graph", "--project-path", str(tmp_project), "--task", task2_id]
        )
        
        assert result.exit_code == 0

    def test_graph_command_json(self, project_with_tasks):
        """Test graph command with JSON output."""
        tmp_project, task0_id, task1_id, task2_id = project_with_tasks
        
        result = runner.invoke(
            app, ["graph", "--project-path", str(tmp_project), "--output", "json"]
        )
        
        assert result.exit_code == 0


class TestAddCommand:
    """Test the add dependency command."""

    def test_add_dependency_success(self, tmp_project):
        """Test adding a dependency."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())
        
        task1_id = tracker.create_task(goal_id, "Task 1", "Do something")
        task2_id = tracker.create_task(goal_id, "Task 2", "Do something else")
        
        result = runner.invoke(
            app, ["add", task2_id, task1_id, "--project-path", str(tmp_project)]
        )
        
        assert result.exit_code == 0
        assert "depends on" in result.stdout

    def test_add_self_dependency_fails(self, tmp_project):
        """Test that self-dependencies are rejected."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Task 1", "Do something")
        
        result = runner.invoke(
            app, ["add", task_id, task_id, "--project-path", str(tmp_project)]
        )
        
        # Should fail because it would create a cycle
        assert result.exit_code == 1


class TestRemoveCommand:
    """Test the remove dependency command."""

    def test_remove_dependency_success(self, project_with_tasks):
        """Test removing a dependency."""
        tmp_project, task0_id, task1_id, task2_id = project_with_tasks
        
        result = runner.invoke(
            app, ["remove", task1_id, "--project-path", str(tmp_project)]
        )
        
        assert result.exit_code == 0
        assert "Removed dependency" in result.stdout

    def test_remove_nonexistent_dependency(self, tmp_project):
        """Test removing dependency from task without one."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Task 1", "Do something")
        
        result = runner.invoke(
            app, ["remove", task_id, "--project-path", str(tmp_project)]
        )
        
        assert result.exit_code == 0


class TestDependencyWorkflow:
    """Test complete dependency workflows."""

    def test_full_dependency_workflow(self, tmp_project):
        """Test a complete dependency management workflow."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())
        
        # Create tasks
        task1_id = tracker.create_task(goal_id, "Design", "Design phase")
        task2_id = tracker.create_task(goal_id, "Implement", "Implementation phase")
        task3_id = tracker.create_task(goal_id, "Test", "Testing phase")
        
        # Add dependencies: Design -> Implement -> Test
        runner.invoke(app, ["add", task2_id, task1_id, "--project-path", str(tmp_project)])
        runner.invoke(app, ["add", task3_id, task2_id, "--project-path", str(tmp_project)])
        
        # View critical path
        result = runner.invoke(
            app, ["critical-path", "--project-path", str(tmp_project)]
        )
        assert result.exit_code == 0
        
        # View blocking tasks
        result = runner.invoke(
            app, ["blocking", "--project-path", str(tmp_project)]
        )
        assert result.exit_code == 0
        
        # View graph
        result = runner.invoke(
            app, ["graph", "--project-path", str(tmp_project)]
        )
        assert result.exit_code == 0

    def test_dependency_with_task_completion(self, project_with_tasks):
        """Test that completed tasks don't block."""
        tmp_project, task0_id, task1_id, task2_id = project_with_tasks
        tracker = TaskTracker(tmp_project)
        
        # Initially task0 should be blocking
        result = runner.invoke(
            app, ["blocking", "--project-path", str(tmp_project), "--output", "json"]
        )
        assert result.exit_code == 0
        
        # Complete task0
        tracker.update_task_status(task0_id, TaskStatus.COMPLETED)
        
        # Now check blocking again - should be different
        result = runner.invoke(
            app, ["blocking", "--project-path", str(tmp_project), "--output", "json"]
        )
        assert result.exit_code == 0


class TestEdgeCases:
    """Test edge cases in dependency commands."""

    def test_missing_project_directory(self):
        """Test commands on non-existent project."""
        result = runner.invoke(app, ["blocking", "--project-path", "/nonexistent/path"])
        
        assert result.exit_code == 1

    def test_invalid_task_id(self, tmp_project):
        """Test adding dependency with invalid task ID."""
        result = runner.invoke(
            app, ["add", "invalid1", "invalid2", "--project-path", str(tmp_project)]
        )
        
        assert result.exit_code == 1
