#!/usr/bin/env python3
"""
A/B Test Manager for Template Validation Framework

This module provides the main orchestrator for A/B testing of template validation,
extending the existing HypothesisTester with comprehensive testing capabilities.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Literal
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import uuid

from .baseline_metrics import BaselineCollector, HypothesisTester
from .enhanced_metrics import EnhancedInteractionMetrics
from .participant_manager import ParticipantManager
from .statistical_validator import StatisticalValidator
from .feedback_collector import FeedbackCollector

@dataclass
class ABTestConfig:
    """Configuration for an A/B test."""
    test_id: str
    name: str
    description: str
    hypothesis: str
    control_config: Dict[str, Any]
    variant_config: Dict[str, Any]
    primary_metric: str
    secondary_metrics: List[str]
    minimum_sample_size: int
    max_duration_days: int
    control_percentage: float = 50.0

@dataclass
class ABTestResult:
    """Results from a completed A/B test."""
    test_id: str
    status: Literal['running', 'completed', 'stopped']
    start_date: str
    end_date: Optional[str]
    primary_metric_result: Dict[str, Any]
    secondary_metrics_results: Dict[str, Any]
    recommendation: str
    confidence_level: float
    practical_significance: bool

class ABTestManager(HypothesisTester):
    """Main orchestrator for A/B testing framework extending HypothesisTester."""

    def __init__(self, project_path: Path):
        super().__init__(project_path)

        # Initialize A/B testing components
        self.participant_manager = ParticipantManager(project_path)
        self.statistical_validator = StatisticalValidator()
        self.feedback_collector = FeedbackCollector(project_path)

        # Test management
        self.active_tests: Dict[str, ABTestConfig] = {}
        self.test_results: Dict[str, ABTestResult] = {}

        self._load_test_data()

    def _load_test_data(self) -> None:
        """Load test configuration and results data."""
        tests_file = self.tests_path / "ab_tests.json"
        results_file = self.tests_path / "ab_test_results.json"

        # Load active tests
        if tests_file.exists():
            try:
                with open(tests_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for test_id, test_data in data.items():
                        self.active_tests[test_id] = ABTestConfig(**test_data)
            except (json.JSONDecodeError, KeyError):
                self.active_tests = {}

        # Load test results
        if results_file.exists():
            try:
                with open(results_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for test_id, result_data in data.items():
                        self.test_results[test_id] = ABTestResult(**result_data)
            except (json.JSONDecodeError, KeyError):
                self.test_results = {}

    def _save_test_data(self) -> None:
        """Save test configuration and results data."""
        tests_file = self.tests_path / "ab_tests.json"
        results_file = self.tests_path / "ab_test_results.json"

        # Save active tests
        with open(tests_file, 'w', encoding='utf-8') as f:
            data = {tid: t.__dict__ for tid, t in self.active_tests.items()}
            json.dump(data, f, indent=2)

        # Save test results
        with open(results_file, 'w', encoding='utf-8') as f:
            data = {tid: r.__dict__ for tid, r in self.test_results.items()}
            json.dump(data, f, indent=2)

    def create_template_validation_test(self, test_name: str = "Template Validation Test") -> str:
        """Create a new A/B test for template validation."""

        test_id = f"template_validation_{int(datetime.now().timestamp())}"

        # Define control and variant configurations
        control_config = {
            "template_system": "baseline",
            "validation_enabled": False,
            "feedback_collection": "minimal"
        }

        variant_config = {
            "template_system": "enhanced",
            "validation_enabled": True,
            "feedback_collection": "comprehensive",
            "enhanced_prompts": True,
            "success_criteria_validation": True
        }

        # Create test configuration
        test_config = ABTestConfig(
            test_id=test_id,
            name=test_name,
            description="A/B test comparing baseline vs enhanced template validation system",
            hypothesis="Enhanced template validation will reduce clarification requests by 30% while improving user satisfaction",
            control_config=control_config,
            variant_config=variant_config,
            primary_metric="clarification_rate",
            secondary_metrics=["response_quality", "user_satisfaction", "template_usage"],
            minimum_sample_size=100,
            max_duration_days=30
        )

        # Create test groups in participant manager
        self.participant_manager.create_test_groups(
            test_id,
            control_config,
            variant_config,
            control_percentage=50.0
        )

        # Store test configuration
        self.active_tests[test_id] = test_config
        self._save_test_data()

        return test_id

    def start_test(self, test_id: str) -> bool:
        """Start an A/B test."""
        if test_id not in self.active_tests:
            return False

        test_config = self.active_tests[test_id]

        # Update test status (would be stored in test config)
        print(f"Starting A/B test: {test_config.name}")
        print(f"Hypothesis: {test_config.hypothesis}")
        print(f"Target sample size: {test_config.minimum_sample_size} per group")

        return True

    def record_interaction(self, user_id: str, command: str, user_input: str,
                          ai_response: str, test_id: str = None) -> EnhancedInteractionMetrics:
        """Record an interaction with A/B testing data."""

        # Register participant if not already registered
        participant = self.participant_manager.register_participant(user_id, test_id or "default_test")

        # Determine test group and configuration
        test_group = participant.test_group
        test_config = None

        if test_id and test_id in self.active_tests:
            test_config = self.active_tests[test_id]

        # Create enhanced baseline collector for this interaction
        baseline_collector = BaselineCollector(self.project_path)

        # Collect baseline metrics (extending existing functionality)
        baseline_metrics = baseline_collector.collect_interaction_metrics(
            command, user_input, ai_response
        )

        # Create enhanced metrics with A/B testing fields
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
            variant_name=test_config.variant_config.get('template_system') if test_config else None,
            user_id=user_id,
            session_id=str(uuid.uuid4()),
            user_satisfaction_score=None,  # Will be collected via feedback
            task_completion_time=None,
            error_encountered=False,
            template_validation_score=None,
            success_criteria_met=False
        )

        # Collect feedback for this interaction
        self.feedback_collector.collect_interaction_feedback(
            user_id, command, ai_response, test_group, enhanced_metrics.session_id
        )

        # Save enhanced metrics
        self._save_enhanced_metrics(enhanced_metrics)

        return enhanced_metrics

    def _save_enhanced_metrics(self, metrics: EnhancedInteractionMetrics) -> None:
        """Save enhanced interaction metrics."""
        metrics_file = self.project_path / ".goalkit" / "metrics" / "enhanced_interaction_metrics.jsonl"

        with open(metrics_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(metrics.to_dict()) + '\n')

    def analyze_test_progress(self, test_id: str) -> Dict[str, Any]:
        """Analyze the progress of an A/B test."""

        if test_id not in self.active_tests:
            return {"error": "Test not found"}

        test_config = self.active_tests[test_id]

        # Get participants for this test
        participants = self.participant_manager.get_participants_for_test(test_id)
        group_a_participants = self.participant_manager.get_group_participants(test_id, 'A')
        group_b_participants = self.participant_manager.get_group_participants(test_id, 'B')

        # Load interaction data for analysis
        interaction_data = self._load_test_interactions(test_id)

        if not interaction_data:
            return {
                "test_id": test_id,
                "status": "insufficient_data",
                "participants": len(participants),
                "group_A_count": len(group_a_participants),
                "group_B_count": len(group_b_participants),
                "message": "Need more interaction data for analysis"
            }

        # Analyze primary metric
        primary_results = self._analyze_metric_for_groups(
            interaction_data, test_config.primary_metric, 'A', 'B'
        )

        # Analyze secondary metrics
        secondary_results = {}
        for metric in test_config.secondary_metrics:
            secondary_results[metric] = self._analyze_metric_for_groups(
                interaction_data, metric, 'A', 'B'
            )

        # Get feedback metrics
        feedback_metrics_a = self.feedback_collector.calculate_feedback_metrics('A')
        feedback_metrics_b = self.feedback_collector.calculate_feedback_metrics('B')

        # Determine if test should be concluded
        should_conclude = self._should_conclude_test(
            primary_results, test_config, len(participants)
        )

        analysis = {
            "test_id": test_id,
            "test_name": test_config.name,
            "status": "completed" if should_conclude else "running",
            "participants": len(participants),
            "group_A_count": len(group_a_participants),
            "group_B_count": len(group_b_participants),
            "primary_metric": primary_results,
            "secondary_metrics": secondary_results,
            "feedback_metrics": {
                "group_A": feedback_metrics_a,
                "group_B": feedback_metrics_b
            },
            "should_conclude": should_conclude,
            "recommendation": self._generate_progress_recommendation(
                primary_results, should_conclude
            )
        }

        return analysis

    def _load_test_interactions(self, test_id: str) -> List[EnhancedInteractionMetrics]:
        """Load interaction data for a specific test."""
        metrics_file = self.project_path / ".goalkit" / "metrics" / "enhanced_interaction_metrics.jsonl"

        if not metrics_file.exists():
            return []

        interactions = []
        with open(metrics_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    if data.get('test_id') == test_id:
                        interactions.append(EnhancedInteractionMetrics(**data))
                except (json.JSONDecodeError, KeyError):
                    continue

        return interactions

    def _analyze_metric_for_groups(self, interactions: List[EnhancedInteractionMetrics],
                                 metric_name: str, group_a: str, group_b: str) -> Dict[str, Any]:
        """Analyze a specific metric for two test groups."""

        group_a_data = []
        group_b_data = []

        for interaction in interactions:
            if interaction.test_group == group_a:
                if metric_name == "clarification_rate":
                    group_a_data.append(1 if interaction.clarification_needed else 0)
                elif metric_name == "response_quality":
                    group_a_data.append(interaction.response_quality_score)
                elif metric_name == "user_satisfaction":
                    if interaction.user_satisfaction_score:
                        group_a_data.append(interaction.user_satisfaction_score)
                elif metric_name == "template_usage":
                    group_a_data.append(1 if interaction.template_used else 0)

            elif interaction.test_group == group_b:
                if metric_name == "clarification_rate":
                    group_b_data.append(1 if interaction.clarification_needed else 0)
                elif metric_name == "response_quality":
                    group_b_data.append(interaction.response_quality_score)
                elif metric_name == "user_satisfaction":
                    if interaction.user_satisfaction_score:
                        group_b_data.append(interaction.user_satisfaction_score)
                elif metric_name == "template_usage":
                    group_b_data.append(1 if interaction.template_used else 0)

        if not group_a_data or not group_b_data:
            return {"error": "Insufficient data for analysis"}

        # Use statistical validator for analysis
        return self.statistical_validator.analyze_test_results(
            group_a_data, group_b_data, metric_name
        )

    def _should_conclude_test(self, primary_results: Dict[str, Any],
                            test_config: ABTestConfig, total_participants: int) -> bool:
        """Determine if a test should be concluded."""

        # Check if we have minimum sample size
        if total_participants < test_config.minimum_sample_size:
            return False

        # Check if results are statistically significant
        if "statistical_test" in primary_results:
            stat_test = primary_results["statistical_test"]
            if stat_test.is_significant:
                return True

        # Check if we've reached maximum duration
        # (This would need to be implemented with actual start date tracking)

        return False

    def _generate_progress_recommendation(self, primary_results: Dict[str, Any],
                                       should_conclude: bool) -> str:
        """Generate recommendation for test progress."""

        if should_conclude:
            if "recommendation" in primary_results:
                return primary_results["recommendation"]
            else:
                return "Test shows significant results - consider concluding and implementing findings"
        else:
            return "Continue collecting data - test needs more participants or time"

    def conclude_test(self, test_id: str) -> Optional[ABTestResult]:
        """Conclude an A/B test and generate results."""

        if test_id not in self.active_tests:
            return None

        # Get final analysis
        analysis = self.analyze_test_progress(test_id)

        if analysis.get("status") != "completed":
            return None

        test_config = self.active_tests[test_id]

        # Create test result
        result = ABTestResult(
            test_id=test_id,
            status="completed",
            start_date=datetime.now().isoformat(),  # Would be actual start date
            end_date=datetime.now().isoformat(),
            primary_metric_result=analysis["primary_metric"],
            secondary_metrics_results=analysis["secondary_metrics"],
            recommendation=analysis["recommendation"],
            confidence_level=0.95,  # Would be calculated from statistical test
            practical_significance=analysis["primary_metric"].get("is_practically_significant", False)
        )

        # Store results
        self.test_results[test_id] = result

        # Remove from active tests
        del self.active_tests[test_id]

        self._save_test_data()

        return result

    def get_test_summary(self, test_id: str) -> Dict[str, Any]:
        """Get a summary of test status and results."""

        if test_id in self.test_results:
            result = self.test_results[test_id]
            return {
                "test_id": test_id,
                "status": result.status,
                "start_date": result.start_date,
                "end_date": result.end_date,
                "recommendation": result.recommendation,
                "confidence_level": result.confidence_level,
                "practical_significance": result.practical_significance
            }

        elif test_id in self.active_tests:
            analysis = self.analyze_test_progress(test_id)
            return {
                "test_id": test_id,
                "status": analysis.get("status", "unknown"),
                "participants": analysis.get("participants", 0),
                "recommendation": analysis.get("recommendation", "Continue testing")
            }

        else:
            return {"error": "Test not found"}

    def run_comprehensive_hypothesis_tests(self) -> Dict[str, Any]:
        """Run comprehensive hypothesis tests with A/B testing framework."""

        # Run original hypothesis tests
        original_results = super().run_all_hypothesis_tests()

        # Add A/B testing enhancements
        ab_testing_status = {
            "active_tests": len(self.active_tests),
            "completed_tests": len(self.test_results),
            "total_participants": sum(
                len(self.participant_manager.get_participants_for_test(test_id))
                for test_id in list(self.active_tests.keys()) + list(self.test_results.keys())
            )
        }

        return {
            "timestamp": datetime.now().isoformat(),
            "original_hypothesis_tests": original_results,
            "ab_testing_status": ab_testing_status,
            "enhanced_capabilities": [
                "A/B testing framework active",
                "Participant management system",
                "Statistical validation",
                "Feedback collection",
                "Real-time progress tracking"
            ]
        }