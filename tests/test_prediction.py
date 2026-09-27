"""Unit tests for the prediction engine.

Tests cover:
- Completion date estimation with confidence levels
- Deadline risk assessment
- Required velocity calculations
- Scenario analysis and comparison
"""

from datetime import datetime, timedelta

import pytest

from goalkit.analytics import AnalyticsEngine
from goalkit.prediction import PredictionEngine


@pytest.fixture
def engine(tmp_path):
    """Create a prediction engine with sample analytics history."""
    goalkit_dir = tmp_path / ".goalkit"
    goalkit_dir.mkdir()

    analytics = AnalyticsEngine(goalkit_dir)
    base_date = datetime.now() - timedelta(days=10)
    for i in range(10):
        analytics.record_snapshot(
            "goal-1",
            completed=i + 1,
            total=20,
            blocked=0,
            in_progress=max(0, 5 - i // 2),
            date=(base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
        )

    return PredictionEngine(goalkit_dir)


class TestEstimateCompletionDate:
    """Test completion date estimation."""

    def test_returns_date_with_history(self, engine):
        result = engine.estimate_completion_date("goal-1")
        assert result is not None
        # 10 tasks done in 10 days, 10 remaining -> ~10 days out
        assert result >= datetime.now().strftime("%Y-%m-%d")

    def test_higher_confidence_shifts_later(self, engine):
        low = engine.estimate_completion_date("goal-1", confidence=0.25)
        high = engine.estimate_completion_date("goal-1", confidence=0.99)
        assert low is not None and high is not None
        assert high > low

    def test_unknown_goal_returns_none(self, engine):
        assert engine.estimate_completion_date("nonexistent") is None


class TestAssessDeadlineRisk:
    """Test deadline risk assessment."""

    def test_far_deadline_not_at_risk(self, engine):
        deadline = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        result = engine.assess_deadline_risk("goal-1", deadline)
        assert result is not None
        assert result.at_risk is False
        assert result.risk_score < 0.3

    def test_near_deadline_is_risky(self, engine):
        deadline = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        result = engine.assess_deadline_risk("goal-1", deadline)
        assert result is not None
        assert result.at_risk is True
        assert result.recommendation  # always provides guidance

    def test_unknown_goal_returns_none(self, engine):
        deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        assert engine.assess_deadline_risk("nonexistent", deadline) is None


class TestRequiredVelocity:
    """Test required velocity calculations."""

    def test_computes_required_pace(self, engine):
        deadline = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        result = engine.calculate_required_velocity("goal-1", deadline)
        assert result is not None
        assert 13 <= result.days_available <= 14
        assert result.tasks_remaining == 10
        # ~14 days minus ~20% buffer (~2 days) -> ~10/12 tasks/day
        assert 0.5 < result.required_per_day < 2.0
        assert result.buffer_days >= 1

    def test_past_deadline_infeasible(self, engine):
        deadline = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        result = engine.calculate_required_velocity("goal-1", deadline)
        assert result is not None
        assert result.feasible is False
        assert result.days_available == 0

    def test_unknown_goal_returns_none(self, engine):
        deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        assert engine.calculate_required_velocity("nonexistent", deadline) is None


class TestScenarioAnalysis:
    """Test what-if scenario analysis."""

    def test_all_scenarios_return_results(self, engine):
        deadline = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        results = engine.compare_scenarios("goal-1", deadline)
        assert len(results) == 4
        names = {r.scenario_name for r in results}
        assert "Increase Velocity by 20%" in names
        assert "Reduce Scope by 20%" in names
        assert "2x Parallel Work" in names
        assert "Extend Deadline by 2 Weeks" in names

    def test_scenario_probabilities_bounded(self, engine):
        deadline = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        results = engine.compare_scenarios("goal-1", deadline)
        for r in results:
            assert 0.0 <= r.probability <= 1.0
            assert r.risk_level in ("low", "medium", "high")

    def test_single_scenario(self, engine):
        deadline = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        result = engine.scenario_analysis("goal-1", deadline, "reduce_scope")
        assert result is not None
        assert result.scenario_name == "Reduce Scope by 20%"

    def test_unknown_scenario_type(self, engine):
        deadline = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        assert engine.scenario_analysis("goal-1", deadline, "bogus") is None

    def test_unknown_goal_returns_empty(self, engine):
        deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        assert engine.compare_scenarios("nonexistent", deadline) == []
