"""Multi-project aggregation and cross-project analysis.

This module provides functionality for discovering multiple Goal Kit projects
within a workspace and aggregating their data for cross-project reporting.
"""

from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from .tasks import TaskTracker
from .reporting import ReportGenerator, Report
from .models import Task, TaskStatus


@dataclass
class ProjectSummary:
    """Summary of a single project."""

    name: str
    path: Path
    task_count: int
    completed_tasks: int
    completion_rate: float
    health_score: float
    created_at: datetime


@dataclass
class AggregatedReport:
    """Report aggregating data from multiple projects."""

    generated_at: datetime
    project_count: int
    projects: List[ProjectSummary] = field(default_factory=list)
    total_tasks: int = 0
    total_completed: int = 0
    overall_completion_rate: float = 0.0
    overall_health_score: float = 0.0
    health_scores: Dict[str, float] = field(default_factory=dict)
    task_distribution: Dict[str, int] = field(default_factory=dict)


class AggregationEngine:
    """Aggregate data from multiple Goal Kit projects.
    
    Discovers projects in a workspace and combines their data for
    cross-project analysis and reporting.
    """

    def __init__(self, workspace_path: Path):
        """Initialize AggregationEngine.

        Args:
            workspace_path: Root directory containing Goal Kit projects.
        """
        self.workspace_path = Path(workspace_path)

    def discover_projects(self) -> List[ProjectSummary]:
        """Discover all Goal Kit projects in the workspace.

        Returns:
            List of ProjectSummary objects for each project found.
        """
        projects = []

        if not self.workspace_path.exists():
            return projects

        # Look for directories with .goalkit subdirectory
        for item in self.workspace_path.iterdir():
            if not item.is_dir():
                continue

            goalkit_dir = item / ".goalkit"
            if not goalkit_dir.exists():
                continue

            # Found a project
            try:
                summary = self._summarize_project(item)
                if summary:
                    projects.append(summary)
            except Exception:
                # Skip projects with errors
                continue

        return sorted(projects, key=lambda p: p.name)

    def aggregate_reports(self, projects: Optional[List[ProjectSummary]] = None) -> AggregatedReport:
        """Aggregate reports from multiple projects.

        Args:
            projects: List of projects to aggregate. If None, discovers all.

        Returns:
            AggregatedReport with combined data from all projects.
        """
        if projects is None:
            projects = self.discover_projects()

        report = AggregatedReport(
            generated_at=datetime.now(),
            project_count=len(projects),
            projects=projects,
        )

        if not projects:
            return report

        # Aggregate metrics
        total_tasks = 0
        total_completed = 0
        health_scores = {}
        task_status_dist = {
            TaskStatus.TODO.value: 0,
            TaskStatus.IN_PROGRESS.value: 0,
            TaskStatus.COMPLETED.value: 0,
        }

        for project in projects:
            total_tasks += project.task_count
            total_completed += project.completed_tasks
            health_scores[project.name] = project.health_score
            
            # Update task distribution
            try:
                tracker = TaskTracker(project.path)
                all_tasks = tracker.get_all_tasks()
                for task in all_tasks:
                    status = task.status.value
                    task_status_dist[status] = task_status_dist.get(status, 0) + 1
            except Exception:
                pass

        report.total_tasks = total_tasks
        report.total_completed = total_completed
        report.health_scores = health_scores
        report.task_distribution = task_status_dist

        # Calculate overall metrics
        if total_tasks > 0:
            report.overall_completion_rate = (total_completed / total_tasks) * 100
        
        if health_scores:
            report.overall_health_score = sum(health_scores.values()) / len(health_scores)

        return report

    def get_project_comparison(self, projects: Optional[List[ProjectSummary]] = None) -> Dict[str, Dict[str, any]]:
        """Get side-by-side comparison of projects.

        Args:
            projects: List of projects to compare. If None, discovers all.

        Returns:
            Dictionary with projects as keys and metrics as values.
        """
        if projects is None:
            projects = self.discover_projects()

        comparison = {}
        for project in projects:
            comparison[project.name] = {
                "path": str(project.path),
                "task_count": project.task_count,
                "completed_tasks": project.completed_tasks,
                "completion_rate": round(project.completion_rate, 1),
                "health_score": round(project.health_score, 1),
                "created_at": project.created_at.isoformat(),
            }

        return comparison

    def get_project_ranking(
        self, 
        projects: Optional[List[ProjectSummary]] = None,
        metric: str = "completion_rate"
    ) -> List[Tuple[str, float]]:
        """Rank projects by a specific metric.

        Args:
            projects: List of projects to rank. If None, discovers all.
            metric: Metric to rank by (completion_rate, health_score, task_count).

        Returns:
            List of (project_name, metric_value) tuples sorted descending.
        """
        if projects is None:
            projects = self.discover_projects()

        if not projects:
            return []

        rankings = []
        for project in projects:
            if metric == "completion_rate":
                value = project.completion_rate
            elif metric == "health_score":
                value = project.health_score
            elif metric == "task_count":
                value = float(project.task_count)
            else:
                continue

            rankings.append((project.name, value))

        return sorted(rankings, key=lambda x: x[1], reverse=True)

    def get_workspace_summary(self) -> Dict[str, any]:
        """Get summary statistics for entire workspace.

        Returns:
            Dictionary with workspace-level metrics.
        """
        projects = self.discover_projects()
        report = self.aggregate_reports(projects)

        return {
            "workspace_path": str(self.workspace_path),
            "project_count": len(projects),
            "total_tasks": report.total_tasks,
            "total_completed": report.total_completed,
            "overall_completion_rate": round(report.overall_completion_rate, 1),
            "overall_health_score": round(report.overall_health_score, 1),
            "task_distribution": report.task_distribution,
            "projects": [p.name for p in projects],
            "generated_at": report.generated_at.isoformat(),
        }

    # Private helper methods

    def _summarize_project(self, project_path: Path) -> Optional[ProjectSummary]:
        """Create a summary of a single project.

        Args:
            project_path: Path to the project directory.

        Returns:
            ProjectSummary or None if project cannot be analyzed.
        """
        try:
            tracker = TaskTracker(project_path)
            stats = tracker.get_task_stats()

            # Determine project name
            name = project_path.name

            # Calculate health score
            health_score = self._calculate_project_health(tracker)

            # Get created_at timestamp
            created_at = self._get_project_created_at(project_path)

            return ProjectSummary(
                name=name,
                path=project_path,
                task_count=stats.total_tasks,
                completed_tasks=stats.completed_tasks,
                completion_rate=stats.completion_percent,
                health_score=health_score,
                created_at=created_at,
            )
        except Exception:
            return None

    def _calculate_project_health(self, tracker: TaskTracker) -> float:
        """Calculate health score for a project.

        Args:
            tracker: TaskTracker for the project.

        Returns:
            Health score 0-100.
        """
        try:
            stats = tracker.get_task_stats()
            all_tasks = tracker.get_all_tasks()

            completion_rate = stats.completion_percent
            in_progress_count = sum(1 for t in all_tasks if t.status == TaskStatus.IN_PROGRESS)
            in_progress_rate = (in_progress_count / stats.total_tasks * 100) if stats.total_tasks > 0 else 0

            # 70% completion weight + 20% momentum + 10% buffer
            health = (completion_rate * 0.7) + (in_progress_rate * 0.2) + 10.0
            return min(100.0, max(0.0, health))
        except Exception:
            return 50.0

    def _get_project_created_at(self, project_path: Path) -> datetime:
        """Get creation timestamp for a project.

        Args:
            project_path: Path to the project directory.

        Returns:
            datetime of project creation or now if not found.
        """
        try:
            goalkit_dir = project_path / ".goalkit"
            if goalkit_dir.exists():
                # Use modification time of .goalkit directory as proxy
                return datetime.fromtimestamp(goalkit_dir.stat().st_mtime)
        except Exception:
            pass

        return datetime.now()
