"""Prediction engine for goal completion forecasting and risk assessment.

This module provides predictive analytics capabilities including:
- Completion date estimation with confidence intervals
- Deadline risk assessment and probability calculations
- Required velocity calculations to meet deadlines
- Scenario analysis for "what-if" planning
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from goalkeeper_cli.analytics import AnalyticsEngine, AnalyticsPoint


@dataclass
class RiskAssessment:
    """Risk assessment for deadline.

    Attributes:
        at_risk: Whether goal is at risk of missing deadline
        risk_score: Numeric risk score (0-1, where 1 is highest risk)
        days_until_deadline: Days until deadline
        current_velocity: Current task completion rate
        required_velocity: Tasks/day needed to meet deadline
        recommendation: Action recommendation
    """

    at_risk: bool
    risk_score: float
    days_until_deadline: int
    current_velocity: float
    required_velocity: float
    recommendation: str


@dataclass
class RequiredVelocity:
    """Required velocity to meet deadline.

    Attributes:
        tasks_remaining: Tasks left to complete
        days_available: Days until deadline
        required_per_day: Tasks/day needed
        required_per_week: Tasks/week needed
        current_velocity: Current rate
        feasible: Whether goal is achievable
        buffer_days: Extra days for contingency (20%)
    """

    tasks_remaining: int
    days_available: int
    required_per_day: float
    required_per_week: float
    current_velocity: float
    feasible: bool
    buffer_days: int


@dataclass
class ScenarioResult:
    """Result of scenario analysis.

    Attributes:
        scenario_name: Name of the scenario
        completion_date: Projected completion date
        probability: Probability of success
        risk_level: 'low', 'medium', 'high'
        additional_resource_cost: Estimated effort increase needed
    """

    scenario_name: str
    completion_date: str
    probability: float
    risk_level: str
    additional_resource_cost: str


class PredictionEngine:
    """Engine for predictive analytics and goal forecasting.

    Uses historical velocity data to project completion dates,
    assess risk against deadlines, and recommend actions.
    """

    def __init__(self, goalkit_dir: Path) -> None:
        """Initialize prediction engine.

        Args:
            goalkit_dir: Path to .goalkit directory
        """
        self.goalkit_dir = Path(goalkit_dir)
        self.analytics = AnalyticsEngine(goalkit_dir)

    def estimate_completion_date(
        self, goal_id: str, confidence: float = 0.95
    ) -> Optional[str]:
        """Estimate completion date with confidence interval.

        Args:
            goal_id: ID of the goal
            confidence: Confidence level (0-1, default 0.95 = 95%)

        Returns:
            Estimated completion date (YYYY-MM-DD) or None
        """
        forecast = self.analytics.forecast_completion(goal_id)
        if not forecast:
            return None

        if forecast.tasks_remaining <= 0:
            return forecast.estimated_date

        # Apply confidence adjustment
        if confidence < 0.5:
            # High confidence in sooner completion
            days_adjustment = -5
        elif confidence < 0.95:
            # Default
            days_adjustment = 0
        else:
            # High confidence in later completion
            days_adjustment = 5

        est_date = datetime.strptime(
            forecast.estimated_date, "%Y-%m-%d"
        ) + timedelta(days=days_adjustment)
        return est_date.strftime("%Y-%m-%d")

    def assess_deadline_risk(
        self, goal_id: str, deadline: str
    ) -> Optional[RiskAssessment]:
        """Assess risk of missing deadline.

        Args:
            goal_id: ID of the goal
            deadline: Deadline date (YYYY-MM-DD)

        Returns:
            RiskAssessment or None if insufficient data
        """
        forecast = self.analytics.forecast_completion(goal_id, deadline)
        if not forecast:
            return None

        velocity = self.analytics.get_velocity_metrics(goal_id)
        if not velocity:
            current_velocity = 0
        else:
            current_velocity = velocity.average_velocity

        # Calculate risk score
        at_risk = forecast.probability < 0.8
        risk_score = 1.0 - max(0, min(1.0, forecast.probability))

        # Generate recommendation
        if forecast.probability > 0.9:
            recommendation = "✅ On track. Continue current pace."
        elif forecast.probability > 0.7:
            recommendation = "⚠️ Slightly behind. Minor adjustments may help."
        elif forecast.probability > 0.5:
            recommendation = (
                f"⏰ At risk. Need to complete {forecast.required_velocity:.1f} "
                f"tasks/day."
            )
        else:
            recommendation = (
                f"🚨 High risk. Current pace insufficient. "
                f"Deadline unrealistic without significant changes."
            )

        return RiskAssessment(
            at_risk=at_risk,
            risk_score=risk_score,
            days_until_deadline=forecast.days_remaining,
            current_velocity=current_velocity,
            required_velocity=forecast.required_velocity,
            recommendation=recommendation,
        )

    def calculate_required_velocity(
        self, goal_id: str, deadline: str
    ) -> Optional[RequiredVelocity]:
        """Calculate velocity needed to meet deadline.

        Args:
            goal_id: ID of the goal
            deadline: Target deadline (YYYY-MM-DD)

        Returns:
            RequiredVelocity or None if insufficient data
        """
        forecast = self.analytics.forecast_completion(goal_id, deadline)
        if not forecast:
            return None

        velocity = self.analytics.get_velocity_metrics(goal_id)
        current_velocity = (
            velocity.average_velocity if velocity else 1.0
        )

        days_available = forecast.days_remaining
        if days_available <= 0:
            # Deadline has passed
            return RequiredVelocity(
                tasks_remaining=forecast.tasks_remaining,
                days_available=0,
                required_per_day=999,
                required_per_week=999,
                current_velocity=current_velocity,
                feasible=False,
                buffer_days=0,
            )

        # Calculate with 20% buffer (added time for contingency)
        buffer_days = max(1, int(days_available * 0.2))
        effective_days = days_available - buffer_days

        if effective_days <= 0:
            required_per_day = 999
        else:
            required_per_day = forecast.tasks_remaining / effective_days

        required_per_week = required_per_day * 7

        # Feasible if required velocity is close to current (within 2x)
        feasible = current_velocity > 0 and (
            required_per_day <= current_velocity * 1.5
        )

        return RequiredVelocity(
            tasks_remaining=forecast.tasks_remaining,
            days_available=days_available,
            required_per_day=required_per_day,
            required_per_week=required_per_week,
            current_velocity=current_velocity,
            feasible=feasible,
            buffer_days=buffer_days,
        )

    def scenario_analysis(
        self, goal_id: str, deadline: str, scenario_type: str = "increase_velocity"
    ) -> Optional[ScenarioResult]:
        """Analyze "what-if" scenarios.

        Scenarios:
        - increase_velocity: +20% velocity boost
        - reduce_scope: Remove 20% of tasks
        - parallel_work: 2x task parallelization
        - extend_deadline: Add 2 weeks to deadline

        Args:
            goal_id: ID of the goal
            deadline: Current deadline (YYYY-MM-DD)
            scenario_type: Type of scenario to analyze

        Returns:
            ScenarioResult or None if insufficient data
        """
        base_forecast = self.analytics.forecast_completion(goal_id, deadline)
        if not base_forecast:
            return None

        base_date = datetime.strptime(base_forecast.estimated_date, "%Y-%m-%d")
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        base_probability = base_forecast.probability

        velocity = self.analytics.get_velocity_metrics(goal_id)
        current_velocity = (
            velocity.average_velocity if velocity else 1.0
        )

        if scenario_type == "increase_velocity":
            # Increase velocity by 20%
            new_velocity = current_velocity * 1.2
            tasks_remaining = base_forecast.tasks_remaining
            days_to_complete = (
                tasks_remaining / new_velocity
                if new_velocity > 0
                else 999
            )
            new_date = (
                datetime.now() + timedelta(days=days_to_complete)
            ).strftime("%Y-%m-%d")

            days_until_deadline = (deadline_date - datetime.now()).days
            new_probability = min(
                0.95,
                base_probability + 0.2,
            ) if days_to_complete <= days_until_deadline else base_probability

            return ScenarioResult(
                scenario_name="Increase Velocity by 20%",
                completion_date=new_date,
                probability=new_probability,
                risk_level=self._risk_level(new_probability),
                additional_resource_cost="High - need to accelerate work",
            )

        elif scenario_type == "reduce_scope":
            # Remove 20% of tasks
            reduced_tasks = int(base_forecast.tasks_remaining * 0.8)
            days_to_complete = (
                reduced_tasks / current_velocity
                if current_velocity > 0
                else 999
            )
            new_date = (
                datetime.now() + timedelta(days=days_to_complete)
            ).strftime("%Y-%m-%d")

            days_until_deadline = (deadline_date - datetime.now()).days
            new_probability = min(
                1.0,
                base_probability + 0.15,
            ) if days_to_complete <= days_until_deadline else base_probability

            return ScenarioResult(
                scenario_name="Reduce Scope by 20%",
                completion_date=new_date,
                probability=new_probability,
                risk_level=self._risk_level(new_probability),
                additional_resource_cost="Low - fewer tasks to complete",
            )

        elif scenario_type == "parallel_work":
            # 2x parallelization (reduce time by 50%)
            days_to_complete = base_forecast.tasks_remaining / (
                current_velocity * 2
            )
            new_date = (
                datetime.now() + timedelta(days=days_to_complete)
            ).strftime("%Y-%m-%d")

            days_until_deadline = (deadline_date - datetime.now()).days
            new_probability = min(
                1.0,
                base_probability + 0.25,
            ) if days_to_complete <= days_until_deadline else base_probability

            return ScenarioResult(
                scenario_name="2x Parallel Work",
                completion_date=new_date,
                probability=new_probability,
                risk_level=self._risk_level(new_probability),
                additional_resource_cost="Very High - need 2x resources",
            )

        elif scenario_type == "extend_deadline":
            # Extend deadline by 14 days
            new_deadline = deadline_date + timedelta(days=14)
            base_forecast_extended = (
                self.analytics.forecast_completion(goal_id)
            )
            if base_forecast_extended:
                days_until_deadline = (
                    new_deadline - datetime.now()
                ).days
                tasks_remaining = base_forecast_extended.tasks_remaining
                days_to_complete = (
                    tasks_remaining / current_velocity
                    if current_velocity > 0
                    else 999
                )
                new_probability = min(
                    0.95,
                    base_probability + 0.2,
                ) if days_to_complete <= days_until_deadline else base_probability

                return ScenarioResult(
                    scenario_name="Extend Deadline by 2 Weeks",
                    completion_date=new_deadline.strftime("%Y-%m-%d"),
                    probability=new_probability,
                    risk_level=self._risk_level(new_probability),
                    additional_resource_cost="None - just more time",
                )

        return None

    def _risk_level(self, probability: float) -> str:
        """Convert probability to risk level.

        Args:
            probability: Probability of success (0-1)

        Returns:
            Risk level: 'low', 'medium', or 'high'
        """
        if probability > 0.8:
            return "low"
        elif probability > 0.5:
            return "medium"
        else:
            return "high"

    def compare_scenarios(
        self, goal_id: str, deadline: str
    ) -> List[ScenarioResult]:
        """Compare all scenarios side-by-side.

        Args:
            goal_id: ID of the goal
            deadline: Deadline (YYYY-MM-DD)

        Returns:
            List of ScenarioResults for all scenarios
        """
        scenarios = []

        for scenario_type in [
            "increase_velocity",
            "reduce_scope",
            "parallel_work",
            "extend_deadline",
        ]:
            result = self.scenario_analysis(goal_id, deadline, scenario_type)
            if result:
                scenarios.append(result)

        return scenarios
