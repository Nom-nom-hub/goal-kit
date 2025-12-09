"""Analytics engine for burndown, velocity, trends, and forecasting.

This module provides comprehensive analytics capabilities for goals, including:
- Burndown chart generation (ideal vs actual progress)
- Velocity tracking (tasks completed per period)
- Trend analysis (momentum and trajectory)
- Completion forecasting (estimated completion dates)
- Bottleneck identification (blockers and slow tasks)
- Automated insights (recommendations based on data)

All data is persisted in .goalkit/analytics_history.json for historical tracking.
"""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from goalkeeper_cli.models import Goal, Task, TaskStatus


@dataclass
class BurndownData:
    """Burndown chart data for visualization.

    Attributes:
        dates: Timeline dates (str, YYYY-MM-DD format)
        ideal_remaining: Ideal tasks remaining (linear decline)
        actual_remaining: Actual tasks remaining from history
        completed_count: Cumulative tasks completed
        chart_ascii: ASCII art burndown chart
    """

    dates: List[str]
    ideal_remaining: List[int]
    actual_remaining: List[int]
    completed_count: List[int]
    chart_ascii: str


@dataclass
class VelocityMetrics:
    """Velocity metrics for productivity tracking.

    Attributes:
        periods: Period identifiers (week 1, week 2, etc.)
        tasks_completed: Tasks completed in each period
        average_velocity: Average tasks per period
        trend: Direction of velocity ('improving', 'stable', 'declining')
        momentum: Rate of change in velocity (-1.0 to 1.0)
    """

    periods: List[str]
    tasks_completed: List[int]
    average_velocity: float
    trend: str
    momentum: float


@dataclass
class TrendAnalysis:
    """Trend analysis for goal progress.

    Attributes:
        slope: Linear regression slope (tasks/day)
        intercept: Linear regression y-intercept
        r_squared: Goodness of fit (0-1)
        direction: 'positive', 'negative', or 'flat'
        velocity_change: Percent change in velocity
        momentum_score: Overall momentum score (-1 to 1)
    """

    slope: float
    intercept: float
    r_squared: float
    direction: str
    velocity_change: float
    momentum_score: float


@dataclass
class CompletionForecast:
    """Forecast for goal completion.

    Attributes:
        estimated_date: Expected completion date
        confidence: Confidence level (0-1)
        probability: Probability of on-time completion (0-1)
        low_estimate: Conservative estimate (lower bound)
        high_estimate: Optimistic estimate (upper bound)
        days_remaining: Days until current deadline
        tasks_remaining: Tasks left to complete
        required_velocity: Tasks/day needed to meet deadline
    """

    estimated_date: str
    confidence: float
    probability: float
    low_estimate: str
    high_estimate: str
    days_remaining: int
    tasks_remaining: int
    required_velocity: float


@dataclass
class Bottleneck:
    """Identified bottleneck or blocker.

    Attributes:
        task_id: ID of blocking task
        task_title: Title of blocking task
        blocked_count: Number of tasks blocked by this
        blocked_since: Date when blocking started
        severity: 'critical', 'high', 'medium', 'low'
    """

    task_id: str
    task_title: str
    blocked_count: int
    blocked_since: str
    severity: str


@dataclass
class AnalyticsPoint:
    """Single point in analytics history.

    Attributes:
        date: Date of the data point (YYYY-MM-DD)
        completed: Tasks completed by this date
        total: Total tasks in goal at this date
        blocked: Tasks blocked at this date
        in_progress: Tasks in progress at this date
    """

    date: str
    completed: int
    total: int
    blocked: int
    in_progress: int

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AnalyticsPoint":
        """Create from dictionary (JSON deserialization)."""
        return cls(**data)


class AnalyticsEngine:
    """Engine for goal analytics, burndown, velocity, and forecasting.

    This class processes task history data to provide insights into:
    - Progress visualization (burndown charts)
    - Productivity metrics (velocity tracking)
    - Trend analysis (momentum and trajectory)
    - Future estimates (completion date forecasting)
    - Risk identification (bottlenecks and blockers)

    Data is persisted in .goalkit/analytics_history.json for historical tracking.
    """

    def __init__(self, goalkit_dir: Path) -> None:
        """Initialize analytics engine.

        Args:
            goalkit_dir: Path to .goalkit directory
        """
        self.goalkit_dir = Path(goalkit_dir)
        self.history_file = self.goalkit_dir / "analytics_history.json"

    def _load_history(self) -> dict:
        """Load analytics history from file.

        Returns:
            Dictionary mapping goal IDs to lists of AnalyticsPoints
        """
        if not self.history_file.exists():
            return {}

        try:
            with open(self.history_file) as f:
                data = json.load(f)
                # Convert dicts back to AnalyticsPoint objects
                result = {}
                for goal_id, points in data.items():
                    result[goal_id] = [
                        AnalyticsPoint.from_dict(p) for p in points
                    ]
                return result
        except (json.JSONDecodeError, ValueError):
            return {}

    def _save_history(self, history: dict) -> None:
        """Save analytics history to file.

        Args:
            history: Dictionary mapping goal IDs to lists of AnalyticsPoints
        """
        self.goalkit_dir.mkdir(parents=True, exist_ok=True)

        # Convert AnalyticsPoints to dicts for JSON serialization
        data = {}
        for goal_id, points in history.items():
            data[goal_id] = [p.to_dict() for p in points]

        with open(self.history_file, "w") as f:
            json.dump(data, f, indent=2)

    def record_snapshot(
        self,
        goal_id: str,
        completed: int,
        total: int,
        blocked: int = 0,
        in_progress: int = 0,
    ) -> None:
        """Record a snapshot of goal progress.

        Args:
            goal_id: ID of the goal
            completed: Number of completed tasks
            total: Total tasks in goal
            blocked: Number of blocked tasks
            in_progress: Number of in-progress tasks
        """
        history = self._load_history()

        if goal_id not in history:
            history[goal_id] = []

        # Create point for today
        today = datetime.now().strftime("%Y-%m-%d")

        # Check if already recorded today
        if history[goal_id] and history[goal_id][-1].date == today:
            history[goal_id][-1] = AnalyticsPoint(
                date=today,
                completed=completed,
                total=total,
                blocked=blocked,
                in_progress=in_progress,
            )
        else:
            history[goal_id].append(
                AnalyticsPoint(
                    date=today,
                    completed=completed,
                    total=total,
                    blocked=blocked,
                    in_progress=in_progress,
                )
            )

        self._save_history(history)

    def get_burndown_data(
        self,
        goal_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Optional[BurndownData]:
        """Generate burndown chart data.

        Args:
            goal_id: ID of the goal
            start_date: Start date (YYYY-MM-DD), defaults to 14 days ago
            end_date: End date (YYYY-MM-DD), defaults to today

        Returns:
            BurndownData with chart information or None if insufficient data
        """
        history = self._load_history()
        if goal_id not in history or not history[goal_id]:
            return None

        points = history[goal_id]

        # Parse dates
        if not start_date:
            start = datetime.now() - timedelta(days=14)
            start_date = start.strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        # Filter to date range
        filtered = [
            p
            for p in points
            if start_date <= p.date <= end_date
        ]

        if not filtered:
            return None

        # Calculate ideal burndown (linear from first to last point)
        first_total = filtered[0].total
        last_completed = filtered[-1].completed
        num_days = len(filtered)

        dates = [p.date for p in filtered]
        actual_remaining = [max(0, p.total - p.completed) for p in filtered]
        completed_count = [p.completed for p in filtered]

        # Ideal line from first point to completion
        ideal_remaining = [
            max(0, first_total - int(i * last_completed / (num_days - 1)))
            for i in range(num_days)
        ]

        # Generate ASCII chart
        chart = self._generate_ascii_chart(
            dates, ideal_remaining, actual_remaining
        )

        return BurndownData(
            dates=dates,
            ideal_remaining=ideal_remaining,
            actual_remaining=actual_remaining,
            completed_count=completed_count,
            chart_ascii=chart,
        )

    def _generate_ascii_chart(
        self, dates: List[str], ideal: List[int], actual: List[int]
    ) -> str:
        """Generate ASCII art burndown chart.

        Args:
            dates: List of date strings
            ideal: Ideal remaining tasks
            actual: Actual remaining tasks

        Returns:
            ASCII chart as string
        """
        if not dates or len(dates) < 2:
            return ""

        max_val = max(max(ideal or [1]), max(actual or [1]))
        if max_val == 0:
            return "All tasks completed!"

        # Scale to 20 rows
        height = 20
        width = min(len(dates), 60)

        lines = []
        lines.append("Burndown Chart (--ideal vs actual)")
        lines.append("")

        # Chart body
        for row in range(height, 0, -1):
            line = f"{max_val * row // height:3d}|"

            for i in range(0, len(ideal), max(1, len(ideal) // width)):
                ideal_val = ideal[i] if i < len(ideal) else ideal[-1]
                actual_val = actual[i] if i < len(actual) else actual[-1]

                char = " "
                if actual_val * height / max_val >= row:
                    char = "█" if actual_val * height / max_val > row else "▓"
                elif ideal_val * height / max_val >= row:
                    char = "·"

                line += char

            lines.append(line)

        # X-axis
        lines.append("  +" + "-" * (width or 1))

        return "\n".join(lines)

    def get_velocity_metrics(
        self, goal_id: str, periods: int = 4
    ) -> Optional[VelocityMetrics]:
        """Calculate velocity metrics (tasks completed per period).

        Args:
            goal_id: ID of the goal
            periods: Number of periods to analyze (default 4 weeks)

        Returns:
            VelocityMetrics or None if insufficient data
        """
        history = self._load_history()
        if goal_id not in history or not history[goal_id]:
            return None

        points = sorted(history[goal_id], key=lambda p: p.date)

        if len(points) < 2:
            return None

        # Calculate period boundaries (week-based)
        period_length = max(1, len(points) // periods)
        period_velocities = []
        period_labels = []

        for i in range(0, len(points), period_length):
            period_end = min(i + period_length, len(points))
            period_points = points[i:period_end]

            if period_points:
                start_completed = period_points[0].completed
                end_completed = period_points[-1].completed
                completed_this_period = max(0, end_completed - start_completed)
                period_velocities.append(completed_this_period)
                period_labels.append(f"Period {len(period_labels) + 1}")

        if len(period_velocities) < 2:
            return None

        avg_velocity = sum(period_velocities) / len(period_velocities)

        # Calculate trend
        if period_velocities[-1] > period_velocities[0] * 1.1:
            trend = "improving"
        elif period_velocities[-1] < period_velocities[0] * 0.9:
            trend = "declining"
        else:
            trend = "stable"

        # Calculate momentum
        momentum = (period_velocities[-1] - period_velocities[0]) / (
            period_velocities[0] + 1
        )
        momentum = max(-1.0, min(1.0, momentum))

        return VelocityMetrics(
            periods=period_labels,
            tasks_completed=period_velocities,
            average_velocity=avg_velocity,
            trend=trend,
            momentum=momentum,
        )

    def get_trend_analysis(self, goal_id: str) -> Optional[TrendAnalysis]:
        """Analyze trend in progress using linear regression.

        Args:
            goal_id: ID of the goal

        Returns:
            TrendAnalysis or None if insufficient data
        """
        history = self._load_history()
        if goal_id not in history or not history[goal_id]:
            return None

        points = sorted(history[goal_id], key=lambda p: p.date)

        if len(points) < 3:
            return None

        # Convert dates to numeric values
        start_date = datetime.strptime(points[0].date, "%Y-%m-%d")
        x_values = [
            (
                datetime.strptime(p.date, "%Y-%m-%d") - start_date
            ).days
            for p in points
        ]
        y_values = [p.completed for p in points]

        # Simple linear regression
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x ** 2 for x in x_values)

        denominator = n * sum_x2 - sum_x ** 2
        if denominator == 0:
            return None

        slope = (n * sum_xy - sum_x * sum_y) / denominator
        intercept = (sum_y - slope * sum_x) / n

        # Calculate R-squared
        mean_y = sum_y / n
        ss_tot = sum((y - mean_y) ** 2 for y in y_values)
        ss_res = sum(
            (y - (slope * x + intercept)) ** 2
            for x, y in zip(x_values, y_values)
        )
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        # Determine direction
        if slope > 0.1:
            direction = "positive"
        elif slope < -0.1:
            direction = "negative"
        else:
            direction = "flat"

        # Velocity change
        velocity_change = (slope * len(x_values) - slope * 0) / (
            slope * 0 + 1
        ) if slope > 0 else 0

        # Momentum score
        momentum_score = min(1.0, max(-1.0, slope / (max(y_values) + 1)))

        return TrendAnalysis(
            slope=slope,
            intercept=intercept,
            r_squared=r_squared,
            direction=direction,
            velocity_change=velocity_change,
            momentum_score=momentum_score,
        )

    def forecast_completion(
        self, goal_id: str, deadline: Optional[str] = None
    ) -> Optional[CompletionForecast]:
        """Forecast completion date based on velocity.

        Args:
            goal_id: ID of the goal
            deadline: Optional deadline date (YYYY-MM-DD) for risk assessment

        Returns:
            CompletionForecast or None if insufficient data
        """
        history = self._load_history()
        if goal_id not in history or not history[goal_id]:
            return None

        points = sorted(history[goal_id], key=lambda p: p.date)

        if len(points) < 2:
            return None

        last_point = points[-1]
        tasks_remaining = last_point.total - last_point.completed

        if tasks_remaining <= 0:
            today = datetime.now().strftime("%Y-%m-%d")
            return CompletionForecast(
                estimated_date=today,
                confidence=1.0,
                probability=1.0,
                low_estimate=today,
                high_estimate=today,
                days_remaining=0,
                tasks_remaining=0,
                required_velocity=0,
            )

        # Get velocity
        velocity_metrics = self.get_velocity_metrics(goal_id)
        if not velocity_metrics:
            return None

        avg_velocity = velocity_metrics.average_velocity
        if avg_velocity <= 0:
            return None

        # Calculate forecast
        days_to_complete = tasks_remaining / avg_velocity
        estimated_date = (
            datetime.now() + timedelta(days=days_to_complete)
        ).strftime("%Y-%m-%d")

        # Conservative/optimistic bounds (±20%)
        low_days = days_to_complete * 1.2
        high_days = days_to_complete * 0.8
        low_estimate = (
            datetime.now() + timedelta(days=low_days)
        ).strftime("%Y-%m-%d")
        high_estimate = (
            datetime.now() + timedelta(days=high_days)
        ).strftime("%Y-%m-%d")

        # Deadline assessment
        days_remaining = 0
        probability = 0.5
        required_velocity = avg_velocity
        confidence = min(0.95, velocity_metrics.average_velocity / (
            tasks_remaining + 1
        ))

        if deadline:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
            days_remaining = (deadline_date - datetime.now()).days
            required_velocity = (
                tasks_remaining / days_remaining if days_remaining > 0 else 999
            )

            # Probability calculation
            if days_remaining <= 0:
                probability = 0.0
            elif days_to_complete <= days_remaining:
                probability = 0.9
            else:
                ratio = days_to_complete / days_remaining
                probability = max(0.0, 1.0 - ratio + 1.0)

        return CompletionForecast(
            estimated_date=estimated_date,
            confidence=confidence,
            probability=probability,
            low_estimate=low_estimate,
            high_estimate=high_estimate,
            days_remaining=days_remaining,
            tasks_remaining=tasks_remaining,
            required_velocity=required_velocity,
        )

    def get_bottlenecks(self, goal_id: str) -> List[Bottleneck]:
        """Identify bottlenecks and blocking tasks.

        Args:
            goal_id: ID of the goal

        Returns:
            List of Bottleneck objects
        """
        history = self._load_history()
        if goal_id not in history or not history[goal_id]:
            return []

        points = sorted(history[goal_id], key=lambda p: p.date)

        if not points:
            return []

        # Identify tasks with high blocking
        bottlenecks = []

        # Check for tasks that stay blocked too long
        last_point = points[-1]
        blocked_since_days = (
            (datetime.now() - datetime.strptime(points[0].date, "%Y-%m-%d"))
            .days
        )

        if last_point.blocked > 0 and blocked_since_days > 2:
            bottlenecks.append(
                Bottleneck(
                    task_id="blocked",
                    task_title=f"{last_point.blocked} tasks blocked",
                    blocked_count=last_point.blocked,
                    blocked_since=points[0].date,
                    severity="high" if last_point.blocked > 3 else "medium",
                )
            )

        # Check for stalled progress
        if len(points) >= 3:
            recent = points[-3:]
            completions = [
                recent[i].completed - recent[i - 1].completed
                for i in range(1, len(recent))
            ]

            if all(c == 0 for c in completions):
                bottlenecks.append(
                    Bottleneck(
                        task_id="stalled",
                        task_title="Progress stalled",
                        blocked_count=len(recent),
                        blocked_since=recent[0].date,
                        severity="critical",
                    )
                )

        return bottlenecks

    def generate_insights(self, goal_id: str) -> List[str]:
        """Generate automated insights about goal progress.

        Args:
            goal_id: ID of the goal

        Returns:
            List of insight strings
        """
        insights = []

        velocity = self.get_velocity_metrics(goal_id)
        if velocity:
            if velocity.trend == "improving":
                insights.append(
                    f"📈 Velocity improving! Completing {velocity.average_velocity:.1f} "
                    f"tasks/period."
                )
            elif velocity.trend == "declining":
                insights.append(
                    f"📉 Velocity declining. Current rate: {velocity.average_velocity:.1f} "
                    f"tasks/period."
                )

        trend = self.get_trend_analysis(goal_id)
        if trend:
            if trend.direction == "positive":
                insights.append(
                    f"✅ Strong positive momentum ({trend.momentum_score:.2f} score)."
                )
            elif trend.direction == "negative":
                insights.append(
                    f"⚠️ Negative momentum - may need intervention."
                )

        forecast = self.forecast_completion(goal_id)
        if forecast:
            if forecast.probability > 0.8:
                insights.append(
                    f"🎯 On track for completion by {forecast.estimated_date}."
                )
            elif forecast.probability < 0.3:
                insights.append(
                    f"⏰ At risk of missing deadline. "
                    f"Need {forecast.required_velocity:.1f} tasks/day."
                )

        bottlenecks = self.get_bottlenecks(goal_id)
        if bottlenecks:
            for bottleneck in bottlenecks[:2]:
                insights.append(
                    f"🚧 {bottleneck.severity.upper()}: {bottleneck.task_title}"
                )

        return insights if insights else ["No significant insights at this time."]
