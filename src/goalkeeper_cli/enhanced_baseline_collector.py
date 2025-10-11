#!/usr/bin/env python3
"""
Enhanced Baseline Collector with A/B Testing Integration

This module extends the existing BaselineCollector with A/B testing capabilities,
providing enhanced metrics collection and analysis for template validation.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

from .baseline_metrics import BaselineCollector, BaselineMetrics, InteractionMetrics
from .enhanced_metrics import EnhancedInteractionMetrics
from .participant_manager import ParticipantManager
from .statistical_validator import StatisticalValidator
from .feedback_collector import FeedbackCollector

@dataclass
class EnhancedBaselineMetrics:
    """Enhanced baseline metrics with A/B testing support."""
    timestamp: str
    total_interactions: int
    successful_interactions: int
    avg_clarification_requests: float
    avg_response_quality_score: float
    template_usage_rate: float
    context_retention_rate: float
    goal_completion_rate: float

    # A/B testing enhancements
    test_participants: int
    group_A_interactions: int
    group_B_interactions: int
    group_A_success_rate: float
    group_B_success_rate: float
    group_A_avg_satisfaction: float
    group_B_avg_satisfaction: float
    statistical_significance: Dict[str, float]

    def to_dict(self) -> dict:
        return asdict(self)

class EnhancedBaselineCollector:
    """Enhanced baseline collector with A/B testing integration."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.metrics_path = project_path / ".goalkit" / "metrics"
        self.metrics_path.mkdir(parents=True, exist_ok=True)

        # Initialize component managers
        self.baseline_collector = BaselineCollector(project_path)
        self.participant_manager = ParticipantManager(project_path)
        self.statistical_validator = StatisticalValidator()
        self.feedback_collector = FeedbackCollector(project_path)

    def collect_enhanced_interaction_metrics(self, command: str, user_input: str,
                                           ai_response: str, user_id: str = None,
                                           test_id: str = None, success_score: float = None) -> EnhancedInteractionMetrics:
        """Collect enhanced metrics for a single AI interaction with A/B testing support."""

        # Get baseline metrics first
        baseline_metrics = self.baseline_collector.collect_interaction_metrics(
            command, user_input, ai_response, success_score
        )

        # Register participant if user_id provided
        test_group = None
        if user_id and test_id:
            participant = self.participant_manager.register_participant(user_id, test_id)
            test_group = participant.test_group

        # Create enhanced metrics
        enhanced_metrics = EnhancedInteractionMetrics(
            timestamp=baseline_metrics.timestamp,
            command=baseline_metrics.command,
            user_input_length=baseline_metrics.user_input_length,
            response_length=baseline_metrics.response_length,
            clarification_needed=baseline_metrics.clarification_needed,
            response_quality_score=baseline_metrics.response_quality_score,
            context_retained=baseline_metrics.context_retained,
            template_used=baseline_metrics.template_used,
            test_group=test_group,
            test_id=test_id,
            user_id=user_id,
            session_id=f"{user_id}_{int(datetime.now().timestamp())}" if user_id else None,
            user_satisfaction_score=None,  # Will be collected via feedback system
            task_completion_time=None,
            error_encountered=False,
            template_validation_score=self._calculate_template_validation_score(user_input, command),
            success_criteria_met=self._check_success_criteria(user_input, ai_response),
            template_compliance_issues=self._identify_template_issues(user_input)
        )

        # Save enhanced metrics
        self.save_enhanced_interaction_metrics(enhanced_metrics)

        # Collect feedback if user_id provided
        if user_id:
            self.feedback_collector.collect_interaction_feedback(
                user_id, command, ai_response, test_group, enhanced_metrics.session_id
            )

        return enhanced_metrics

    def _calculate_template_validation_score(self, user_input: str, command: str) -> float:
        """Calculate template validation score based on input structure."""
        score = 5.0  # Base score

        # Check for template indicators
        template_indicators = [
            'success criteria', 'measurable outcome', 'acceptance criteria',
            'milestone', 'timeline', 'dependencies', 'deliverables'
        ]

        found_indicators = sum(1 for indicator in template_indicators if indicator in user_input.lower())

        # Score based on template completeness
        completeness_score = min(10.0, 5.0 + (found_indicators * 1.5))

        # Penalty for very short or unstructured input
        if len(user_input) < 50:
            completeness_score -= 2.0
        elif len(user_input) > 500:
            completeness_score += 1.0  # Bonus for detailed input

        return max(0.0, min(10.0, completeness_score))

    def _check_success_criteria(self, user_input: str, ai_response: str) -> bool:
        """Check if success criteria are properly defined and met."""
        # Look for success criteria indicators in user input
        success_indicators = ['success criteria', 'acceptance criteria', 'completion criteria', 'done when']
        has_criteria = any(indicator in user_input.lower() for indicator in success_indicators)

        if not has_criteria:
            return False

        # Check if AI response addresses the criteria
        response_addresses_criteria = any(indicator in ai_response.lower() for indicator in success_indicators)

        return response_addresses_criteria

    def _identify_template_issues(self, user_input: str) -> List[str]:
        """Identify potential template compliance issues."""
        issues = []

        # Check for missing key components
        required_components = {
            'success criteria': ['success criteria', 'acceptance criteria', 'completion criteria'],
            'timeline': ['timeline', 'deadline', 'due date', 'target date'],
            'scope': ['scope', 'deliverables', 'what to build', 'requirements']
        }

        for component, keywords in required_components.items():
            if not any(keyword in user_input.lower() for keyword in keywords):
                issues.append(f"Missing {component}")

        # Check for ambiguous language
        ambiguous_words = ['maybe', 'perhaps', 'might', 'could', 'possibly', 'unclear']
        if any(word in user_input.lower() for word in ambiguous_words):
            issues.append("Contains ambiguous language")

        return issues

    def save_enhanced_interaction_metrics(self, metrics: EnhancedInteractionMetrics) -> None:
        """Save enhanced interaction metrics to file."""
        metrics_file = self.metrics_path / "enhanced_interaction_metrics.jsonl"

        with open(metrics_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(metrics.to_dict()) + '\n')

    def generate_enhanced_baseline_report(self, days: int = 30, test_id: str = None) -> EnhancedBaselineMetrics:
        """Generate enhanced baseline metrics report with A/B testing data."""

        # Get baseline metrics
        baseline = self.baseline_collector.generate_baseline_report(days)

        # Load enhanced interaction data
        enhanced_data = self._load_enhanced_interactions(days, test_id)

        if not enhanced_data:
            # Return enhanced baseline with zero A/B testing data
            return EnhancedBaselineMetrics(
                timestamp=datetime.now().isoformat(),
                total_interactions=baseline.total_interactions,
                successful_interactions=baseline.successful_interactions,
                avg_clarification_requests=baseline.avg_clarification_requests,
                avg_response_quality_score=baseline.avg_response_quality_score,
                template_usage_rate=baseline.template_usage_rate,
                context_retention_rate=baseline.context_retention_rate,
                goal_completion_rate=baseline.goal_completion_rate,
                test_participants=0,
                group_A_interactions=0,
                group_B_interactions=0,
                group_A_success_rate=0.0,
                group_B_success_rate=0.0,
                group_A_avg_satisfaction=0.0,
                group_B_avg_satisfaction=0.0,
                statistical_significance={}
            )

        # Calculate A/B testing metrics
        test_participants = len(set(
            interaction.user_id for interaction in enhanced_data
            if interaction.user_id
        ))

        group_a_interactions = [i for i in enhanced_data if i.test_group == 'A']
        group_b_interactions = [i for i in enhanced_data if i.test_group == 'B']

        group_a_successes = sum(1 for i in group_a_interactions if i.is_successful_interaction())
        group_b_successes = sum(1 for i in group_b_interactions if i.is_successful_interaction())

        group_a_success_rate = group_a_successes / len(group_a_interactions) if group_a_interactions else 0
        group_b_success_rate = group_b_successes / len(group_b_interactions) if group_b_interactions else 0

        # Calculate satisfaction scores from feedback
        group_a_satisfaction = self._calculate_group_satisfaction('A', days)
        group_b_satisfaction = self._calculate_group_satisfaction('B', days)

        # Calculate statistical significance for key metrics
        statistical_significance = self._calculate_statistical_significance(enhanced_data)

        return EnhancedBaselineMetrics(
            timestamp=datetime.now().isoformat(),
            total_interactions=baseline.total_interactions,
            successful_interactions=baseline.successful_interactions,
            avg_clarification_requests=baseline.avg_clarification_requests,
            avg_response_quality_score=baseline.avg_response_quality_score,
            template_usage_rate=baseline.template_usage_rate,
            context_retention_rate=baseline.context_retention_rate,
            goal_completion_rate=baseline.goal_completion_rate,
            test_participants=test_participants,
            group_A_interactions=len(group_a_interactions),
            group_B_interactions=len(group_b_interactions),
            group_A_success_rate=group_a_success_rate,
            group_B_success_rate=group_b_success_rate,
            group_A_avg_satisfaction=group_a_satisfaction,
            group_B_avg_satisfaction=group_b_satisfaction,
            statistical_significance=statistical_significance
        )

    def _load_enhanced_interactions(self, days: int, test_id: str = None) -> List[EnhancedInteractionMetrics]:
        """Load enhanced interaction data."""
        metrics_file = self.metrics_path / "enhanced_interaction_metrics.jsonl"

        if not metrics_file.exists():
            return []

        cutoff_date = datetime.now() - timedelta(days=days)
        interactions = []

        with open(metrics_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    interaction_date = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))

                    if interaction_date >= cutoff_date:
                        if test_id is None or data.get('test_id') == test_id:
                            interactions.append(EnhancedInteractionMetrics(**data))
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue

        return interactions

    def _calculate_group_satisfaction(self, test_group: str, days: int) -> float:
        """Calculate average satisfaction for a test group."""
        feedback_metrics = self.feedback_collector.calculate_feedback_metrics(test_group, days)
        return feedback_metrics.get('average_satisfaction', 0.0)

    def _calculate_statistical_significance(self, interactions: List[EnhancedInteractionMetrics]) -> Dict[str, float]:
        """Calculate statistical significance for key metrics between groups."""

        if len(interactions) < 20:  # Need minimum data for statistical tests
            return {}

        group_a = [i for i in interactions if i.test_group == 'A']
        group_b = [i for i in interactions if i.test_group == 'B']

        if len(group_a) < 10 or len(group_b) < 10:
            return {}

        significance_results = {}

        # Test clarification rate significance
        if group_a and group_b:
            a_clarifications = sum(1 for i in group_a if i.clarification_needed)
            b_clarifications = sum(1 for i in group_b if i.clarification_needed)

            clarification_test = self.statistical_validator.run_proportion_test(
                a_clarifications, len(group_a),
                b_clarifications, len(group_b)
            )
            significance_results['clarification_rate_p_value'] = clarification_test.p_value

        # Test response quality significance
        if group_a and group_b:
            a_quality = [i.response_quality_score for i in group_a]
            b_quality = [i.response_quality_score for i in group_b]

            quality_test = self.statistical_validator.run_means_test(a_quality, b_quality)
            significance_results['response_quality_p_value'] = quality_test.p_value

        return significance_results

    def save_enhanced_baseline_report(self, baseline: EnhancedBaselineMetrics) -> None:
        """Save enhanced baseline report to file."""
        report_file = self.metrics_path / "enhanced_baseline_report.json"

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(baseline.to_dict(), f, indent=2)

    def get_template_validation_insights(self, days: int = 30) -> Dict[str, Any]:
        """Get insights specifically for template validation."""

        enhanced_data = self._load_enhanced_interactions(days)

        if not enhanced_data:
            return {"message": "No enhanced interaction data available"}

        # Analyze template usage patterns
        template_users = [i for i in enhanced_data if i.template_used]
        non_template_users = [i for i in enhanced_data if not i.template_used]

        template_success_rate = sum(1 for i in template_users if i.is_successful_interaction()) / len(template_users) if template_users else 0
        non_template_success_rate = sum(1 for i in non_template_users if i.is_successful_interaction()) / len(non_template_users) if non_template_users else 0

        # Analyze common template issues
        all_issues = []
        for interaction in enhanced_data:
            all_issues.extend(interaction.template_compliance_issues)

        issue_counts = {}
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1

        # Analyze validation score distribution
        validation_scores = [i.template_validation_score for i in enhanced_data if i.template_validation_score]
        avg_validation_score = sum(validation_scores) / len(validation_scores) if validation_scores else 0

        return {
            "total_enhanced_interactions": len(enhanced_data),
            "template_usage_rate": len(template_users) / len(enhanced_data),
            "template_success_rate": template_success_rate,
            "non_template_success_rate": non_template_success_rate,
            "template_advantage": template_success_rate - non_template_success_rate,
            "common_template_issues": sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "average_validation_score": avg_validation_score,
            "validation_score_distribution": {
                "high_performers": len([s for s in validation_scores if s >= 8.0]),
                "medium_performers": len([s for s in validation_scores if 5.0 <= s < 8.0]),
                "low_performers": len([s for s in validation_scores if s < 5.0])
            }
        }

    def generate_ab_test_readiness_report(self) -> Dict[str, Any]:
        """Generate report on readiness for A/B testing."""

        # Get current baseline
        baseline = self.baseline_collector.generate_baseline_report()

        # Get enhanced baseline
        enhanced_baseline = self.generate_enhanced_baseline_report()

        # Calculate sample size requirements
        sample_size_calc = self.statistical_validator.calculate_sample_size(
            'clarification_rate', enhanced_baseline.avg_clarification_requests
        )

        # Check data quality
        recent_interactions = self._load_enhanced_interactions(7)  # Last 7 days
        data_quality_score = self._assess_data_quality(recent_interactions)

        return {
            "baseline_established": baseline.total_interactions > 0,
            "enhanced_tracking_active": enhanced_baseline.test_participants > 0,
            "sample_size_requirement": sample_size_calc.total_sample_size,
            "estimated_duration_days": sample_size_calc.expected_duration_days,
            "current_daily_interactions": len(recent_interactions),
            "projected_days_to_completion": sample_size_calc.total_sample_size / len(recent_interactions) if recent_interactions else 999,
            "data_quality_score": data_quality_score,
            "ready_for_ab_testing": (
                baseline.total_interactions >= 50 and
                data_quality_score >= 7.0 and
                enhanced_baseline.test_participants >= 10
            ),
            "recommendations": self._generate_readiness_recommendations(
                baseline, enhanced_baseline, data_quality_score
            )
        }

    def _assess_data_quality(self, interactions: List[EnhancedInteractionMetrics]) -> float:
        """Assess the quality of collected interaction data."""

        if not interactions:
            return 0.0

        score = 10.0  # Start with perfect score

        # Check for missing data
        missing_fields = 0
        total_fields = len(EnhancedInteractionMetrics.__dataclass_fields__)

        for interaction in interactions:
            interaction_dict = interaction.to_dict()
            missing_fields += sum(1 for v in interaction_dict.values() if v is None or v == [])

        completeness_score = max(0, 10 - (missing_fields / (len(interactions) * total_fields)) * 10)
        score = min(score, completeness_score)

        # Check for data consistency
        consistent_groups = len(set(i.test_group for i in interactions if i.test_group)) <= 2
        if not consistent_groups:
            score -= 2.0

        # Check for reasonable response quality variance
        quality_scores = [i.response_quality_score for i in interactions]
        if quality_scores:
            quality_std = sum((x - sum(quality_scores)/len(quality_scores))**2 for x in quality_scores) / len(quality_scores)
            if quality_std > 5.0:  # Too much variance might indicate data quality issues
                score -= 1.0

        return max(0.0, score)

    def _generate_readiness_recommendations(self, baseline: BaselineMetrics,
                                          enhanced_baseline: EnhancedBaselineMetrics,
                                          data_quality_score: float) -> List[str]:
        """Generate recommendations for A/B testing readiness."""

        recommendations = []

        if baseline.total_interactions < 50:
            recommendations.append("Collect more baseline interaction data (aim for 100+ interactions)")

        if data_quality_score < 7.0:
            recommendations.append("Improve data collection completeness and consistency")

        if enhanced_baseline.test_participants < 10:
            recommendations.append("Increase participant enrollment for A/B testing")

        if enhanced_baseline.group_A_interactions < 20 or enhanced_baseline.group_B_interactions < 20:
            recommendations.append("Need more balanced interaction data across test groups")

        if not recommendations:
            recommendations.append("System ready for comprehensive A/B testing")
            recommendations.append("Consider starting with template validation test")

        return recommendations