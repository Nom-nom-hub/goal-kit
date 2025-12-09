"""Task tracking and management for Goalkeeper projects.

This module provides task management capabilities including task creation,
status tracking, and aggregated statistics.
"""

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
from datetime import datetime
from uuid import uuid4

from .models import Task, TaskStatus


@dataclass
class TaskStats:
    """Statistics for tasks."""

    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    todo_tasks: int
    completion_percent: float
    total_estimated_hours: float
    completed_hours: float
    in_progress_hours: float
    tasks_by_goal: Dict[str, int] = field(default_factory=dict)
    tasks_by_status: Dict[str, int] = field(default_factory=dict)


class TaskTracker:
    """Track goal-related tasks and their completion status.

    Provides methods to:
    - Create and manage tasks within goals
    - Track task status (todo, in_progress, completed)
    - Calculate task statistics and completion metrics
    - Retrieve task history and filtered views
    """

    def __init__(self, project_path: Path):
        """Initialize TaskTracker.

        Args:
            project_path: Path to the project root directory.
        """
        self.project_path = Path(project_path)
        self.goalkit_dir = self.project_path / ".goalkit"
        self.tasks_file = self.goalkit_dir / "tasks.json"
        self.tasks: Dict[str, Task] = {}
        self._load_tasks()

    def create_task(
        self,
        goal_id: str,
        title: str,
        description: str,
        estimated_hours: float = 0.0,
    ) -> str:
        """Create a new task within a goal.

        Args:
            goal_id: ID of the goal this task belongs to.
            title: Task title.
            description: Task description.
            estimated_hours: Estimated hours to complete task.

        Returns:
            The task ID (UUID).
        """
        task_id = str(uuid4())
        now = datetime.now()

        task = Task(
            id=task_id,
            goal_id=goal_id,
            title=title,
            description=description,
            status=TaskStatus.TODO,
            estimated_hours=estimated_hours,
            created_at=now,
            updated_at=now,
            completed_at=None,
        )

        self.tasks[task_id] = task
        self._save_tasks()
        return task_id

    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """Update a task's status.

        Args:
            task_id: ID of the task to update.
            status: New status for the task.

        Returns:
            True if successful, False if task not found.
        """
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        task.status = status
        task.updated_at = datetime.now()

        if status == TaskStatus.COMPLETED:
            task.completed_at = datetime.now()
        elif status != TaskStatus.COMPLETED and task.completed_at:
            task.completed_at = None

        self._save_tasks()
        return True

    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        estimated_hours: Optional[float] = None,
    ) -> bool:
        """Update task details.

        Args:
            task_id: ID of the task to update.
            title: New title (optional).
            description: New description (optional).
            estimated_hours: New estimated hours (optional).

        Returns:
            True if successful, False if task not found.
        """
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if estimated_hours is not None:
            task.estimated_hours = estimated_hours

        task.updated_at = datetime.now()
        self._save_tasks()
        return True

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: ID of the task to retrieve.

        Returns:
            Task object or None if not found.
        """
        return self.tasks.get(task_id)

    def get_tasks_by_goal(self, goal_id: str) -> List[Task]:
        """Get all tasks for a specific goal.

        Args:
            goal_id: ID of the goal.

        Returns:
            List of tasks for the goal.
        """
        return [task for task in self.tasks.values() if task.goal_id == goal_id]

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get all tasks with a specific status.

        Args:
            status: The status to filter by.

        Returns:
            List of tasks with the given status.
        """
        return [task for task in self.tasks.values() if task.status == status]

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks in the project.

        Returns:
            List of all tasks.
        """
        return list(self.tasks.values())

    def delete_task(self, task_id: str) -> bool:
        """Delete a task.

        Args:
            task_id: ID of the task to delete.

        Returns:
            True if successful, False if task not found.
        """
        if task_id not in self.tasks:
            return False

        del self.tasks[task_id]
        self._save_tasks()
        return True

    def get_task_stats(self) -> TaskStats:
        """Calculate overall task statistics.

        Returns:
            TaskStats object with aggregated metrics.
        """
        tasks = self.tasks.values()

        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
        in_progress_tasks = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)
        todo_tasks = sum(1 for t in tasks if t.status == TaskStatus.TODO)

        completion_percent = (
            (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0
        )

        total_estimated_hours = sum(t.estimated_hours for t in tasks)
        completed_hours = sum(
            t.estimated_hours for t in tasks if t.status == TaskStatus.COMPLETED
        )
        in_progress_hours = sum(
            t.estimated_hours for t in tasks if t.status == TaskStatus.IN_PROGRESS
        )

        tasks_by_goal = {}
        tasks_by_status = {}

        for task in tasks:
            tasks_by_goal[task.goal_id] = tasks_by_goal.get(task.goal_id, 0) + 1

            status_key = task.status.value
            tasks_by_status[status_key] = tasks_by_status.get(status_key, 0) + 1

        return TaskStats(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            in_progress_tasks=in_progress_tasks,
            todo_tasks=todo_tasks,
            completion_percent=completion_percent,
            total_estimated_hours=total_estimated_hours,
            completed_hours=completed_hours,
            in_progress_hours=in_progress_hours,
            tasks_by_goal=tasks_by_goal,
            tasks_by_status=tasks_by_status,
        )

    def get_task_stats_by_goal(self, goal_id: str) -> TaskStats:
        """Calculate task statistics for a specific goal.

        Args:
            goal_id: ID of the goal.

        Returns:
            TaskStats object for the goal's tasks.
        """
        goal_tasks = self.get_tasks_by_goal(goal_id)

        total_tasks = len(goal_tasks)
        completed_tasks = sum(1 for t in goal_tasks if t.status == TaskStatus.COMPLETED)
        in_progress_tasks = sum(
            1 for t in goal_tasks if t.status == TaskStatus.IN_PROGRESS
        )
        todo_tasks = sum(1 for t in goal_tasks if t.status == TaskStatus.TODO)

        completion_percent = (
            (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0
        )

        total_estimated_hours = sum(t.estimated_hours for t in goal_tasks)
        completed_hours = sum(
            t.estimated_hours
            for t in goal_tasks
            if t.status == TaskStatus.COMPLETED
        )
        in_progress_hours = sum(
            t.estimated_hours
            for t in goal_tasks
            if t.status == TaskStatus.IN_PROGRESS
        )

        tasks_by_status = {}
        for task in goal_tasks:
            status_key = task.status.value
            tasks_by_status[status_key] = tasks_by_status.get(status_key, 0) + 1

        return TaskStats(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            in_progress_tasks=in_progress_tasks,
            todo_tasks=todo_tasks,
            completion_percent=completion_percent,
            total_estimated_hours=total_estimated_hours,
            completed_hours=completed_hours,
            in_progress_hours=in_progress_hours,
            tasks_by_goal={goal_id: total_tasks},
            tasks_by_status=tasks_by_status,
        )

    def _load_tasks(self) -> None:
        """Load tasks from JSON file.

        Handles missing file gracefully.
        """
        if not self.tasks_file.exists():
            self.tasks = {}
            return

        try:
            with open(self.tasks_file, "r") as f:
                data = json.load(f)

            self.tasks = {}
            for task_id, task_data in data.items():
                task_data["status"] = TaskStatus(task_data["status"])

                if task_data.get("created_at"):
                    task_data["created_at"] = datetime.fromisoformat(
                        task_data["created_at"]
                    )
                if task_data.get("updated_at"):
                    task_data["updated_at"] = datetime.fromisoformat(
                        task_data["updated_at"]
                    )
                if task_data.get("completed_at"):
                    task_data["completed_at"] = datetime.fromisoformat(
                        task_data["completed_at"]
                    )

                self.tasks[task_id] = Task(**task_data)

        except (json.JSONDecodeError, KeyError, ValueError):
            self.tasks = {}

    def _save_tasks(self) -> None:
        """Save tasks to JSON file.

        Creates .goalkit directory if needed.
        """
        self.goalkit_dir.mkdir(parents=True, exist_ok=True)

        data = {}
        for task_id, task in self.tasks.items():
            task_dict = asdict(task)
            task_dict["status"] = task.status.value
            task_dict["created_at"] = task.created_at.isoformat()
            task_dict["updated_at"] = task.updated_at.isoformat()
            if task.completed_at:
                task_dict["completed_at"] = task.completed_at.isoformat()
            else:
                task_dict["completed_at"] = None

            data[task_id] = task_dict

        with open(self.tasks_file, "w") as f:
            json.dump(data, f, indent=2)
