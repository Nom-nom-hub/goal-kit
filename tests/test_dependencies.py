"""Tests for DependencyTracker functionality."""

import pytest
from pathlib import Path
from uuid import uuid4

from src.goalkeeper_cli.dependencies import DependencyTracker
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
def task_tracker(tmp_project):
    """Create a task tracker with sample tasks."""
    tracker = TaskTracker(tmp_project)
    return tracker


@pytest.fixture
def sample_tasks(task_tracker):
    """Create sample tasks for testing."""
    goal_id = str(uuid4())
    
    # Create 5 tasks
    task_ids = []
    for i in range(5):
        task_id = task_tracker.create_task(goal_id, f"Task {i}", f"Desc {i}")
        task_ids.append(task_id)
    
    return goal_id, task_ids


class TestDependencyTrackerInit:
    """Test DependencyTracker initialization."""

    def test_init_with_path(self, tmp_project):
        """Test DependencyTracker initializes with project path."""
        tracker = DependencyTracker(tmp_project)
        assert tracker.project_path == tmp_project
        assert tracker.task_tracker is not None

    def test_init_with_task_tracker(self, tmp_project, task_tracker):
        """Test DependencyTracker initializes with existing TaskTracker."""
        tracker = DependencyTracker(tmp_project, task_tracker)
        assert tracker.task_tracker is task_tracker


class TestAddDependency:
    """Test adding dependencies between tasks."""

    def test_add_dependency_success(self, tmp_project, sample_tasks):
        """Test successfully adding a dependency."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        result = dep_tracker.add_dependency(task_ids[1], task_ids[0])
        
        assert result is True
        task = dep_tracker.task_tracker.get_task(task_ids[1])
        assert task.depends_on == task_ids[0]

    def test_add_dependency_nonexistent_task(self, tmp_project, sample_tasks):
        """Test adding dependency with nonexistent task raises error."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        fake_id = str(uuid4())
        
        with pytest.raises(ValueError):
            dep_tracker.add_dependency(fake_id, task_ids[0])

    def test_add_dependency_nonexistent_dependency(self, tmp_project, sample_tasks):
        """Test adding dependency on nonexistent task raises error."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        fake_id = str(uuid4())
        
        with pytest.raises(ValueError):
            dep_tracker.add_dependency(task_ids[0], fake_id)

    def test_add_circular_dependency_rejected(self, tmp_project, sample_tasks):
        """Test that circular dependencies are rejected."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        # Create chain: task1 -> task0
        dep_tracker.add_dependency(task_ids[1], task_ids[0])
        
        # Try to create cycle: task0 -> task1
        result = dep_tracker.add_dependency(task_ids[0], task_ids[1])
        
        assert result is False


class TestRemoveDependency:
    """Test removing dependencies."""

    def test_remove_dependency_success(self, tmp_project, sample_tasks):
        """Test successfully removing a dependency."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        # Add dependency
        dep_tracker.add_dependency(task_ids[1], task_ids[0])
        
        # Remove it
        result = dep_tracker.remove_dependency(task_ids[1])
        
        assert result is True
        task = dep_tracker.task_tracker.get_task(task_ids[1])
        assert task.depends_on is None

    def test_remove_nonexistent_dependency(self, tmp_project, sample_tasks):
        """Test removing dependency from task without one."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        result = dep_tracker.remove_dependency(task_ids[0])
        
        assert result is True  # No error, just no-op


class TestGetDependencies:
    """Test retrieving dependencies."""

    def test_get_dependencies_none(self, tmp_project, sample_tasks):
        """Test getting dependencies for task with no dependencies."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        deps = dep_tracker.get_dependencies(task_ids[0])
        
        assert deps == []

    def test_get_dependencies_one(self, tmp_project, sample_tasks):
        """Test getting dependencies for task with one dependency."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        dep_tracker.add_dependency(task_ids[1], task_ids[0])
        deps = dep_tracker.get_dependencies(task_ids[1])
        
        assert deps == [task_ids[0]]


class TestGetDependents:
    """Test finding tasks that depend on a given task."""

    def test_get_dependents_none(self, tmp_project, sample_tasks):
        """Test getting dependents for task with no dependents."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        dependents = dep_tracker.get_dependents(task_ids[0])
        
        assert dependents == []

    def test_get_dependents_multiple(self, tmp_project, sample_tasks):
        """Test getting multiple dependents."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        # task1 and task2 both depend on task0
        dep_tracker.add_dependency(task_ids[1], task_ids[0])
        dep_tracker.add_dependency(task_ids[2], task_ids[0])
        
        dependents = dep_tracker.get_dependents(task_ids[0])
        
        assert set(dependents) == {task_ids[1], task_ids[2]}


class TestBlockingTasks:
    """Test identifying blocking tasks."""

    def test_no_blocking_tasks(self, tmp_project, sample_tasks):
        """Test when there are no blocking tasks."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        blocking = dep_tracker.get_blocking_tasks()
        
        assert blocking == []

    def test_blocking_task_identified(self, tmp_project, sample_tasks):
        """Test identification of a blocking task."""
        goal_id, task_ids = sample_tasks
        tracker = TaskTracker(tmp_project)
        dep_tracker = DependencyTracker(tmp_project, tracker)
        
        # task1 depends on task0
        dep_tracker.add_dependency(task_ids[1], task_ids[0])
        
        blocking = dep_tracker.get_blocking_tasks()
        
        # task0 blocks task1
        assert task_ids[0] in blocking

    def test_completed_task_not_blocking(self, tmp_project, sample_tasks):
        """Test that completed tasks don't block."""
        goal_id, task_ids = sample_tasks
        tracker = TaskTracker(tmp_project)
        dep_tracker = DependencyTracker(tmp_project, tracker)
        
        # task1 depends on task0
        dep_tracker.add_dependency(task_ids[1], task_ids[0])
        
        # Complete task0
        tracker.update_task_status(task_ids[0], TaskStatus.COMPLETED)
        
        blocking = dep_tracker.get_blocking_tasks()
        
        # task0 no longer blocks (it's completed)
        assert task_ids[0] not in blocking


class TestCriticalPath:
    """Test critical path calculation."""

    def test_critical_path_no_dependencies(self, tmp_project, sample_tasks):
        """Test critical path with no dependencies."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        path = dep_tracker.get_critical_path()
        
        # Each task is its own path, so longest is just one task
        assert len(path) == 1

    def test_critical_path_linear(self, tmp_project, sample_tasks):
        """Test critical path with linear dependencies."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        # Create chain: task0 -> task1 -> task2
        dep_tracker.add_dependency(task_ids[1], task_ids[0])
        dep_tracker.add_dependency(task_ids[2], task_ids[1])
        
        path = dep_tracker.get_critical_path()
        
        assert len(path) == 3
        assert path[0].id == task_ids[0]
        assert path[1].id == task_ids[1]
        assert path[2].id == task_ids[2]


class TestPathForTask:
    """Test getting dependency path for a specific task."""

    def test_path_for_task_no_deps(self, tmp_project, sample_tasks):
        """Test path for task with no dependencies."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        path = dep_tracker.get_path_for_task(task_ids[0])
        
        assert len(path) == 1
        assert path[0].id == task_ids[0]

    def test_path_for_task_with_deps(self, tmp_project, sample_tasks):
        """Test path for task with dependencies."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        # task0 -> task1 -> task2
        dep_tracker.add_dependency(task_ids[1], task_ids[0])
        dep_tracker.add_dependency(task_ids[2], task_ids[1])
        
        path = dep_tracker.get_path_for_task(task_ids[2])
        
        assert len(path) == 3
        assert [t.id for t in path] == [task_ids[0], task_ids[1], task_ids[2]]


class TestDependencyGraph:
    """Test dependency graph generation."""

    def test_dependency_graph_empty(self, tmp_project, sample_tasks):
        """Test graph with no dependencies."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        graph = dep_tracker.get_dependency_graph()
        
        assert all(len(deps) == 0 for deps in graph.values())

    def test_dependency_graph_with_deps(self, tmp_project, sample_tasks):
        """Test graph with dependencies."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        dep_tracker.add_dependency(task_ids[1], task_ids[0])
        dep_tracker.add_dependency(task_ids[2], task_ids[1])
        
        graph = dep_tracker.get_dependency_graph()
        
        assert graph[task_ids[1]] == [task_ids[0]]
        assert graph[task_ids[2]] == [task_ids[1]]
        assert graph[task_ids[0]] == []


class TestCircularDependencyDetection:
    """Test circular dependency detection."""

    def test_no_cycles(self, tmp_project, sample_tasks):
        """Test detection when there are no cycles."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        dep_tracker.add_dependency(task_ids[1], task_ids[0])
        dep_tracker.add_dependency(task_ids[2], task_ids[1])
        
        cycles = dep_tracker.detect_circular_dependencies()
        
        assert cycles == []

    def test_cycle_detection(self, tmp_project):
        """Test detection of manually created cycle."""
        project_dir = tmp_project
        tracker = TaskTracker(project_dir)
        
        goal_id = str(uuid4())
        task1_id = tracker.create_task(goal_id, "Task 1", "Desc")
        task2_id = tracker.create_task(goal_id, "Task 2", "Desc")
        
        # Manually create a cycle by directly modifying the task
        all_tasks = tracker.get_all_tasks()
        task1 = next(t for t in all_tasks if t.id == task1_id)
        task2 = next(t for t in all_tasks if t.id == task2_id)
        
        task1.depends_on = task2_id
        task2.depends_on = task1_id
        # Update the tracker's internal state and save
        tracker.tasks[task1_id] = task1
        tracker.tasks[task2_id] = task2
        tracker._save_tasks()
        
        dep_tracker = DependencyTracker(project_dir, tracker)
        cycles = dep_tracker.detect_circular_dependencies()
        
        # Should detect the cycle
        assert len(cycles) > 0


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_self_dependency_rejected(self, tmp_project, sample_tasks):
        """Test that self-dependencies are rejected."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        result = dep_tracker.add_dependency(task_ids[0], task_ids[0])
        
        assert result is False

    def test_dependency_with_empty_project(self, tmp_project):
        """Test dependency operations on empty project."""
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        blocking = dep_tracker.get_blocking_tasks()
        path = dep_tracker.get_critical_path()
        graph = dep_tracker.get_dependency_graph()
        
        assert blocking == []
        assert path == []
        assert graph == {}

    def test_multiple_dependency_chains(self, tmp_project, sample_tasks):
        """Test project with multiple independent dependency chains."""
        goal_id, task_ids = sample_tasks
        dep_tracker = DependencyTracker(tmp_project, TaskTracker(tmp_project))
        
        # Chain 1: task0 -> task1
        dep_tracker.add_dependency(task_ids[1], task_ids[0])
        
        # Chain 2: task2 -> task3
        dep_tracker.add_dependency(task_ids[3], task_ids[2])
        
        # task4 is independent
        
        graph = dep_tracker.get_dependency_graph()
        assert graph[task_ids[0]] == []
        assert graph[task_ids[1]] == [task_ids[0]]
        assert graph[task_ids[2]] == []
        assert graph[task_ids[3]] == [task_ids[2]]
        assert graph[task_ids[4]] == []
