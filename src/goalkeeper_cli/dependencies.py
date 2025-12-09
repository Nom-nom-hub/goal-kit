"""Task dependency tracking and critical path analysis.

This module provides functionality for managing task dependencies, detecting
circular dependencies, and calculating critical paths.
"""

from pathlib import Path
from typing import List, Dict, Set, Optional
from collections import defaultdict, deque

from .tasks import TaskTracker
from .models import Task, TaskStatus


class DependencyTracker:
    """Manage task dependencies and perform dependency analysis.
    
    Tracks which tasks depend on which other tasks, detects circular
    dependencies, and calculates critical paths.
    """

    def __init__(self, project_path: Path, task_tracker: Optional[TaskTracker] = None):
        """Initialize DependencyTracker.

        Args:
            project_path: Path to the project root directory.
            task_tracker: Optional TaskTracker instance to use (creates one if not provided).
        """
        self.project_path = Path(project_path)
        self.task_tracker = task_tracker or TaskTracker(project_path)

    def add_dependency(self, task_id: str, depends_on_id: str) -> bool:
        """Add a dependency relationship between tasks.

        Args:
            task_id: ID of the task that depends on another.
            depends_on_id: ID of the task that must be completed first.

        Returns:
            True if dependency added, False if invalid (would create cycle).

        Raises:
            ValueError: If either task doesn't exist.
        """
        # Reject self-dependencies
        if task_id == depends_on_id:
            return False
        
        # Verify both tasks exist
        all_tasks = self.task_tracker.get_all_tasks()
        task_ids = {t.id for t in all_tasks}
        
        if task_id not in task_ids:
            raise ValueError(f"Task {task_id} not found")
        if depends_on_id not in task_ids:
            raise ValueError(f"Task {depends_on_id} not found")

        # Check for circular dependency
        if self._would_create_cycle(task_id, depends_on_id):
            return False

        # Update the task
        task = next((t for t in all_tasks if t.id == task_id), None)
        if task:
            task.depends_on = depends_on_id
            # Update the tracker's internal state and save
            self.task_tracker.tasks[task_id] = task
            self.task_tracker._save_tasks()
            return True
        return False

    def remove_dependency(self, task_id: str) -> bool:
        """Remove a dependency from a task.

        Args:
            task_id: ID of the task to remove dependency from.

        Returns:
            True if dependency removed, False if task not found.
        """
        all_tasks = self.task_tracker.get_all_tasks()
        task = next((t for t in all_tasks if t.id == task_id), None)
        
        if task:
            task.depends_on = None
            # Update the tracker's internal state and save
            self.task_tracker.tasks[task_id] = task
            self.task_tracker._save_tasks()
            return True
        return False

    def get_dependencies(self, task_id: str) -> List[str]:
        """Get list of task IDs this task depends on.

        Args:
            task_id: ID of the task.

        Returns:
            List of task IDs this task directly depends on (0 or 1 item).
        """
        task = self.task_tracker.get_task(task_id)
        if task and task.depends_on:
            return [task.depends_on]
        return []

    def get_dependents(self, task_id: str) -> List[str]:
        """Get list of tasks that depend on the given task.

        Args:
            task_id: ID of the task.

        Returns:
            List of task IDs that depend on this task.
        """
        all_tasks = self.task_tracker.get_all_tasks()
        return [t.id for t in all_tasks if t.depends_on == task_id]

    def get_blocking_tasks(self) -> List[str]:
        """Get tasks that are blocking other incomplete tasks.

        Returns:
            List of task IDs that are incomplete and block other tasks.
        """
        all_tasks = self.task_tracker.get_all_tasks()
        blocking = []

        for task in all_tasks:
            if task.status == TaskStatus.COMPLETED:
                continue

            # Check if any other task depends on this one
            has_dependents = any(
                t.depends_on == task.id and t.status != TaskStatus.COMPLETED
                for t in all_tasks
            )
            
            if has_dependents:
                blocking.append(task.id)

        return blocking

    def get_critical_path(self) -> List[Task]:
        """Calculate the critical path (longest dependency chain).

        Returns:
            List of tasks forming the longest dependency chain.
        """
        all_tasks = self.task_tracker.get_all_tasks()
        
        # Find all tasks with no dependencies (starting points)
        starting_tasks = [
            t for t in all_tasks
            if t.depends_on is None
        ]

        if not starting_tasks:
            return []

        # Build longest path from each starting task
        longest_path = []
        
        for start_task in starting_tasks:
            path = self._build_path_from_task(start_task, all_tasks)
            if len(path) > len(longest_path):
                longest_path = path

        return longest_path

    def get_path_for_task(self, task_id: str) -> List[Task]:
        """Get the dependency chain for a specific task.

        Args:
            task_id: ID of the task.

        Returns:
            List of tasks in the dependency chain, ordered from dependency to dependent.
        """
        all_tasks = self.task_tracker.get_all_tasks()
        task_map = {t.id: t for t in all_tasks}
        
        path = []
        current_id = task_id
        
        while current_id:
            if current_id not in task_map:
                break
            current_task = task_map[current_id]
            path.append(current_task)
            current_id = current_task.depends_on

        return list(reversed(path))

    def get_dependency_graph(self) -> Dict[str, List[str]]:
        """Get the complete dependency graph.

        Returns:
            Dictionary mapping task ID to list of task IDs it depends on.
        """
        all_tasks = self.task_tracker.get_all_tasks()
        graph = {}
        
        for task in all_tasks:
            deps = []
            if task.depends_on:
                deps.append(task.depends_on)
            graph[task.id] = deps

        return graph

    def detect_circular_dependencies(self) -> List[List[str]]:
        """Detect any circular dependency chains.

        Returns:
            List of cycles, each cycle is a list of task IDs.
        """
        all_tasks = self.task_tracker.get_all_tasks()
        task_map = {t.id: t for t in all_tasks}
        visited = set()
        cycles = []

        for task in all_tasks:
            if task.id in visited:
                continue

            cycle = self._find_cycle_from_task(task.id, set(), task_map)
            if cycle:
                cycles.append(cycle)
                visited.update(cycle)

        return cycles

    # Private helper methods

    def _would_create_cycle(self, task_id: str, depends_on_id: str) -> bool:
        """Check if adding this dependency would create a cycle.

        Args:
            task_id: ID of task that would depend on depends_on_id.
            depends_on_id: ID of task that would be depended on.

        Returns:
            True if this would create a cycle.
        """
        all_tasks = self.task_tracker.get_all_tasks()
        task_map = {t.id: t for t in all_tasks}

        # Follow the dependency chain from depends_on_id
        current_id = task_map.get(depends_on_id)
        
        while current_id:
            if current_id.depends_on == task_id:
                return True
            current_id = task_map.get(current_id.depends_on) if current_id.depends_on else None

        return False

    def _build_path_from_task(self, task: Task, all_tasks: List[Task]) -> List[Task]:
        """Build a dependency path starting from a task.

        Args:
            task: Starting task.
            all_tasks: All tasks in the project.

        Returns:
            List of tasks in the path.
        """
        task_map = {t.id: t for t in all_tasks}
        path = [task]

        # Find task that depends on this one
        dependent = next(
            (t for t in all_tasks if t.depends_on == task.id),
            None
        )

        if dependent:
            path.extend(self._build_path_from_task(dependent, all_tasks))

        return path

    def _find_cycle_from_task(
        self, 
        task_id: str, 
        visited: Set[str], 
        task_map: Dict[str, Task]
    ) -> Optional[List[str]]:
        """Find a cycle starting from a task using DFS.

        Args:
            task_id: ID of task to start from.
            visited: Set of visited task IDs in current path.
            task_map: Map of task ID to Task object.

        Returns:
            List of task IDs forming a cycle, or None if no cycle.
        """
        if task_id in visited:
            return [task_id]

        if task_id not in task_map:
            return None

        visited.add(task_id)
        task = task_map[task_id]

        if task.depends_on:
            cycle = self._find_cycle_from_task(task.depends_on, visited.copy(), task_map)
            if cycle:
                if task_id not in cycle:
                    cycle.append(task_id)
                return cycle

        return None
