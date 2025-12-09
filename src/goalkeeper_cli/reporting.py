"""Reporting and insights generation for Goalkeeper projects.

This module provides comprehensive reporting capabilities including project
summaries, trend analysis, velocity metrics, and actionable insights.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from enum import Enum

from .tasks import TaskTracker
from .analyzer import ProjectAnalyzer
from .models import Task, TaskStatus


# Lightweight helper functions that don't require external dependencies
def _calculate_simple_health_score(tasks: List[Task]) -> float:
    """Calculate health score from tasks without external dependencies.
    
    Args:
        tasks: List of tasks to analyze.
        
    Returns:
        Health score 0-100.
    """
    if not tasks:
        return 50.0
    
    completed_count = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
    in_progress_count = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)
    total = len(tasks)
    
    completion_rate = (completed_count / total) * 100 if total > 0 else 0
    in_progress_rate = (in_progress_count / total) * 100 if total > 0 else 0
    
    # 70% completion weight + 20% momentum weight + 10% health margin
    score = (completion_rate * 0.7) + (in_progress_rate * 0.2) + 10.0
    return min(100.0, max(0.0, score))


def _calculate_simple_velocity(tasks: List[Task], days: int = 7) -> float:
    """Calculate task completion velocity without external dependencies.
    
    Args:
        tasks: List of tasks to analyze.
        days: Number of days to look back.
        
    Returns:
        Tasks completed per day.
    """
    if not tasks or days <= 0:
        return 0.0
    
    cutoff = datetime.now() - timedelta(days=days)
    completed_in_period = sum(
        1 for t in tasks 
        if t.status == TaskStatus.COMPLETED 
        and t.completed_at 
        and t.completed_at >= cutoff
    )
    return completed_in_period / days


class ReportType(Enum):
    """Report type enumeration."""

    WEEKLY = "weekly"
    MONTHLY = "monthly"
    SUMMARY = "summary"


class InsightSeverity(Enum):
    """Insight severity level."""

    INFO = "info"
    WARNING = "warning"
    ALERT = "alert"


class InsightType(Enum):
    """Insight type enumeration."""

    VELOCITY = "velocity"
    RISK = "risk"
    COMPLETION = "completion"
    MOMENTUM = "momentum"
    QUALITY = "quality"


@dataclass
class Insight:
    """A single insight or finding."""

    type: InsightType
    title: str
    description: str
    severity: InsightSeverity
    value: float | str
    recommendation: Optional[str] = None


@dataclass
class Report:
    """Project report with metrics and insights."""

    title: str
    report_type: ReportType
    period_start: datetime
    period_end: datetime
    summary: Dict[str, Any] = field(default_factory=dict)
    insights: List[Insight] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.now)


class ReportGenerator:
    """Generate comprehensive reports and insights for projects.

    Aggregates data from ExecutionTracker, MetricsTracker, TaskTracker, and
    ProjectAnalyzer to provide actionable insights and trend analysis.
    """

    def __init__(self, project_path: Path):
        """Initialize ReportGenerator.

        Args:
            project_path: Path to the project root directory.
        """
        self.project_path = Path(project_path)
        self.task_tracker = TaskTracker(project_path)
        self.analyzer = ProjectAnalyzer(project_path)

    def generate_weekly_report(
        self, week_start: Optional[datetime] = None
    ) -> Report:
        """Generate a weekly report.

        Args:
            week_start: Start of week (defaults to 7 days ago).

        Returns:
            Weekly report with metrics and insights.
        """
        if week_start is None:
            week_start = datetime.now() - timedelta(days=7)

        week_end = week_start + timedelta(days=7)

        # Get task stats for the week
        task_stats = self._get_task_stats_for_period(week_start, week_end)
        milestone_stats = self._get_milestone_stats_for_period(week_start, week_end)

        # Calculate metrics
        task_velocity = self._calculate_task_velocity(week_start, week_end)
        all_tasks = self.task_tracker.get_all_tasks()
        milestone_velocity = sum(
            1 for t in all_tasks
            if t.status == TaskStatus.COMPLETED
            and t.completed_at
            and week_start <= t.completed_at <= week_end
        ) / max((week_end - week_start).days, 1)

        # Get current health score
        health_score = _calculate_simple_health_score(all_tasks)

        summary = {
            "period": f"Week of {week_start.strftime('%b %d')}",
            "tasks_completed": task_stats["completed"],
            "tasks_in_progress": task_stats["in_progress"],
            "tasks_todo": task_stats["todo"],
            "task_completion_rate": task_stats["completion_rate"],
            "milestones_completed": milestone_stats["completed"],
            "milestone_completion_rate": milestone_stats["completion_rate"],
            "task_velocity": round(task_velocity, 2),
            "milestone_velocity": round(milestone_velocity, 2),
            "health_score": round(health_score, 1),
        }

        insights = self._generate_weekly_insights(summary, week_start)

        return Report(
            title=f"Weekly Report: {week_start.strftime('%B %d, %Y')}",
            report_type=ReportType.WEEKLY,
            period_start=week_start,
            period_end=week_end,
            summary=summary,
            insights=insights,
            metrics={
                "task_velocity": task_velocity,
                "milestone_velocity": milestone_velocity,
            },
        )

    def generate_monthly_report(
        self, month: Optional[int] = None, year: Optional[int] = None
    ) -> Report:
        """Generate a monthly report.

        Args:
            month: Month number (1-12), defaults to current month.
            year: Year, defaults to current year.

        Returns:
            Monthly report with metrics and insights.
        """
        now = datetime.now()
        if month is None:
            month = now.month
        if year is None:
            year = now.year

        month_start = datetime(year, month, 1)
        if month == 12:
            month_end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            month_end = datetime(year, month + 1, 1) - timedelta(seconds=1)

        # Get stats for the month
        task_stats = self._get_task_stats_for_period(month_start, month_end)
        milestone_stats = self._get_milestone_stats_for_period(month_start, month_end)

        task_velocity = self._calculate_task_velocity(month_start, month_end)
        all_tasks = self.task_tracker.get_all_tasks()
        milestone_velocity = sum(
            1 for t in all_tasks
            if t.status == TaskStatus.COMPLETED
            and t.completed_at
            and month_start <= t.completed_at <= month_end
        ) / max((month_end - month_start).days, 1)

        # Get current health score
        health_score = _calculate_simple_health_score(all_tasks)

        summary = {
            "period": month_start.strftime("%B %Y"),
            "tasks_completed": task_stats["completed"],
            "tasks_in_progress": task_stats["in_progress"],
            "task_completion_rate": task_stats["completion_rate"],
            "milestones_completed": milestone_stats["completed"],
            "milestone_completion_rate": milestone_stats["completion_rate"],
            "task_velocity": round(task_velocity, 2),
            "milestone_velocity": round(milestone_velocity, 2),
            "health_score": round(health_score, 1),
        }

        insights = self._generate_monthly_insights(summary, month_start, month_end)

        return Report(
            title=f"Monthly Report: {month_start.strftime('%B %Y')}",
            report_type=ReportType.MONTHLY,
            period_start=month_start,
            period_end=month_end,
            summary=summary,
            insights=insights,
            metrics={
                "task_velocity": task_velocity,
                "milestone_velocity": milestone_velocity,
            },
        )

    def generate_summary_report(self) -> Report:
        """Generate overall project summary report.

        Returns:
            Summary report with overall metrics and insights.
        """
        task_stats = self.task_tracker.get_task_stats()
        all_tasks = self.task_tracker.get_all_tasks()
        metrics_stats = _calculate_simple_health_score(all_tasks)

        # Try to load project info, fallback to defaults
        try:
            analysis = self.analyzer.analyze()
            project_name = analysis.project.name if analysis.project else "Unknown"
            all_goals = analysis.goals
            created_at = analysis.project.created_at if analysis.project else datetime.now()
        except Exception:
            project_name = "Unknown"
            all_goals = []
            created_at = datetime.now()

        # Identify at-risk goals
        at_risk_goals = []
        for goal in all_goals:
            if goal.completion_percent < 50 and (
                goal.phase == "execute" or goal.phase == "done"
            ):
                at_risk_goals.append(goal.id)

        # Calculate basic execution estimate
        estimated_completion = None
        if task_stats.total_tasks > 0 and task_stats.completed_tasks > 0:
            days_elapsed = (datetime.now() - created_at).days or 1
            velocity = task_stats.completed_tasks / days_elapsed
            if velocity > 0:
                remaining = task_stats.total_tasks - task_stats.completed_tasks
                days_remaining = remaining / velocity
                estimated_completion = datetime.now() + timedelta(days=days_remaining)

        summary = {
            "project_name": project_name,
            "total_tasks": task_stats.total_tasks,
            "completed_tasks": task_stats.completed_tasks,
            "task_completion_rate": task_stats.completion_percent,
            "health_score": round(metrics_stats, 1),
            "active_goals": len([g for g in all_goals if g.completion_percent < 100]),
            "at_risk_goals": len(at_risk_goals),
            "completion_estimate": estimated_completion.isoformat()
            if estimated_completion
            else None,
        }

        insights = self._generate_summary_insights(summary, all_goals)

        return Report(
            title="Project Summary",
            report_type=ReportType.SUMMARY,
            period_start=created_at,
            period_end=datetime.now(),
            summary=summary,
            insights=insights,
            metrics={
                "task_velocity": (task_stats.completed_tasks / max((datetime.now() - created_at).days, 1))
                if task_stats.completed_tasks > 0
                else 0.0,
                "completion_rate": task_stats.completion_percent,
                "health_score": metrics_stats,
            },
        )

    def get_burndown_data(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get burndown chart data.

        Args:
            days: Number of days to include.

        Returns:
            List of daily burndown data points.
        """
        burndown = []
        end_date = datetime.now()

        for i in range(days, -1, -1):
            date = end_date - timedelta(days=i)
            tasks = self.task_tracker.get_all_tasks()

            # Count tasks completed by this date
            completed_by_date = sum(
                1
                for t in tasks
                if t.completed_at and t.completed_at <= date
            )

            burndown.append(
                {
                    "date": date.isoformat(),
                    "remaining": len(tasks) - completed_by_date,
                    "completed": completed_by_date,
                    "total": len(tasks),
                }
            )

        return burndown

    def get_completion_trend(self, days: int = 30) -> List[float]:
        """Get completion percentage trend.

        Args:
            days: Number of days to include.

        Returns:
            List of completion percentages over time.
        """
        trend = []
        end_date = datetime.now()

        for i in range(days, -1, -1):
            date = end_date - timedelta(days=i)
            tasks = self.task_tracker.get_all_tasks()

            if len(tasks) == 0:
                trend.append(0.0)
            else:
                completed_by_date = sum(
                    1
                    for t in tasks
                    if t.completed_at and t.completed_at <= date
                )
                percent = (completed_by_date / len(tasks)) * 100
                trend.append(percent)

        return trend

    def _get_task_stats_for_period(
        self, start: datetime, end: datetime
    ) -> Dict[str, Any]:
        """Get task statistics for a date range.

        Args:
            start: Period start.
            end: Period end.

        Returns:
            Dictionary with task stats for the period.
        """
        all_tasks = self.task_tracker.get_all_tasks()

        completed = sum(
            1
            for t in all_tasks
            if t.status == TaskStatus.COMPLETED
            and t.completed_at
            and start <= t.completed_at <= end
        )

        in_progress = sum(
            1
            for t in all_tasks
            if t.status == TaskStatus.IN_PROGRESS
            and start <= t.updated_at <= end
        )

        todo = sum(
            1
            for t in all_tasks
            if t.status == TaskStatus.TODO and start <= t.created_at <= end
        )

        total = completed + in_progress + todo
        completion_rate = (completed / total * 100) if total > 0 else 0.0

        return {
            "completed": completed,
            "in_progress": in_progress,
            "todo": todo,
            "completion_rate": completion_rate,
        }

    def _get_milestone_stats_for_period(
        self, start: datetime, end: datetime
    ) -> Dict[str, Any]:
        """Get milestone statistics for a date range.

        Args:
            start: Period start.
            end: Period end.

        Returns:
            Dictionary with milestone stats for the period.
        """
        # Use task-based milestone calculation instead of ExecutionTracker
        all_tasks = self.task_tracker.get_all_tasks()
        completed = sum(
            1
            for t in all_tasks
            if t.status == TaskStatus.COMPLETED
            and t.completed_at
            and start <= t.completed_at <= end
        )

        total = len(all_tasks)
        completion_rate = (completed / total * 100) if total > 0 else 0.0

        return {
            "completed": completed,
            "completion_rate": completion_rate,
        }

    def _calculate_task_velocity(self, start: datetime, end: datetime) -> float:
        """Calculate task completion velocity (tasks per day).

        Args:
            start: Period start.
            end: Period end.

        Returns:
            Tasks completed per day.
        """
        all_tasks = self.task_tracker.get_all_tasks()

        completed = sum(
            1
            for t in all_tasks
            if t.status == TaskStatus.COMPLETED
            and t.completed_at
            and start <= t.completed_at <= end
        )

        days = max((end - start).days, 1)
        return completed / days

    def _calculate_milestone_velocity(
        self, start: datetime, end: datetime
    ) -> float:
        """Calculate milestone completion velocity (milestones per day).

        Args:
            start: Period start.
            end: Period end.

        Returns:
            Milestones completed per day.
        """
        # Use task-based velocity calculation instead of ExecutionTracker
        all_tasks = self.task_tracker.get_all_tasks()
        completed = sum(
            1
            for t in all_tasks
            if t.status == TaskStatus.COMPLETED
            and t.completed_at
            and start <= t.completed_at <= end
        )

        days = max((end - start).days, 1)
        return completed / days

    def _generate_weekly_insights(
        self, summary: Dict[str, Any], week_start: datetime
    ) -> List[Insight]:
        """Generate insights from weekly report.

        Args:
            summary: Weekly summary data.
            week_start: Start of the week.

        Returns:
            List of insights.
        """
        insights = []

        # Velocity insight
        if summary["task_velocity"] > 3.0:
            insights.append(
                Insight(
                    type=InsightType.VELOCITY,
                    title="Strong Task Velocity",
                    description=f"Completing {summary['task_velocity']:.1f} tasks per day",
                    severity=InsightSeverity.INFO,
                    value=summary["task_velocity"],
                    recommendation="Maintain current pace and team morale",
                )
            )
        elif summary["task_velocity"] < 1.0 and summary["task_velocity"] > 0:
            insights.append(
                Insight(
                    type=InsightType.VELOCITY,
                    title="Low Task Velocity",
                    description=f"Only {summary['task_velocity']:.1f} tasks per day",
                    severity=InsightSeverity.WARNING,
                    value=summary["task_velocity"],
                    recommendation="Review blockers and team capacity",
                )
            )

        # Completion insight
        if summary["task_completion_rate"] > 80:
            insights.append(
                Insight(
                    type=InsightType.COMPLETION,
                    title="High Completion Rate",
                    description=f"{summary['task_completion_rate']:.0f}% of weekly tasks completed",
                    severity=InsightSeverity.INFO,
                    value=summary["task_completion_rate"],
                )
            )

        # Health insight
        if summary["health_score"] < 60:
            insights.append(
                Insight(
                    type=InsightType.QUALITY,
                    title="Low Project Health",
                    description=f"Health score: {summary['health_score']:.0f}/100",
                    severity=InsightSeverity.ALERT,
                    value=summary["health_score"],
                    recommendation="Review metrics and address quality issues",
                )
            )

        return insights

    def _generate_monthly_insights(
        self, summary: Dict[str, Any], month_start: datetime, month_end: datetime
    ) -> List[Insight]:
        """Generate insights from monthly report.

        Args:
            summary: Monthly summary data.
            month_start: Start of month.
            month_end: End of month.

        Returns:
            List of insights.
        """
        insights = []

        # Task completion insight
        if summary["task_completion_rate"] > 75:
            insights.append(
                Insight(
                    type=InsightType.COMPLETION,
                    title="Excellent Monthly Progress",
                    description=f"Completed {summary['task_completion_rate']:.0f}% of tasks",
                    severity=InsightSeverity.INFO,
                    value=summary["task_completion_rate"],
                    recommendation="Document practices for continued success",
                )
            )

        # Velocity trend
        if summary["task_velocity"] > 4.0:
            insights.append(
                Insight(
                    type=InsightType.MOMENTUM,
                    title="Strong Monthly Momentum",
                    description=f"{summary['task_velocity']:.1f} tasks per day",
                    severity=InsightSeverity.INFO,
                    value=summary["task_velocity"],
                )
            )

        return insights

    def _generate_summary_insights(
        self, summary: Dict[str, Any], goals: List[Any]
    ) -> List[Insight]:
        """Generate insights from summary report.

        Args:
            summary: Summary data.
            goals: List of all goals.

        Returns:
            List of insights.
        """
        insights = []

        # Overall completion
        if summary["task_completion_rate"] > 90:
            insights.append(
                Insight(
                    type=InsightType.COMPLETION,
                    title="Near Project Completion",
                    description=f"{summary['task_completion_rate']:.0f}% complete",
                    severity=InsightSeverity.INFO,
                    value=summary["task_completion_rate"],
                )
            )

        # At-risk goals
        if summary["at_risk_goals"] > 0:
            insights.append(
                Insight(
                    type=InsightType.RISK,
                    title="At-Risk Goals",
                    description=f"{summary['at_risk_goals']} goal(s) at risk",
                    severity=InsightSeverity.WARNING,
                    value=summary["at_risk_goals"],
                    recommendation="Review and re-prioritize at-risk goals",
                )
            )

        # Health score
        health = summary["health_score"]
        if health > 80:
            severity = InsightSeverity.INFO
            title = "Excellent Project Health"
        elif health > 60:
            severity = InsightSeverity.INFO
            title = "Good Project Health"
        else:
            severity = InsightSeverity.WARNING
            title = "Low Project Health"

        insights.append(
            Insight(
                type=InsightType.QUALITY,
                title=title,
                description=f"Health score: {health:.0f}/100",
                severity=severity,
                value=health,
            )
        )

        return insights
