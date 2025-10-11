#!/usr/bin/env python3
"""
Baseline Metrics System for AI Performance Enhancement (Goal 002)

This module establishes baseline measurements for current AI performance
and provides testing framework for hypothesis validation.
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import re

@dataclass
class BaselineMetrics:
    """Data class for storing baseline AI performance metrics."""
    timestamp: str
    total_interactions: int
    successful_interactions: int
    avg_clarification_requests: float
    avg_response_quality_score: float
    template_usage_rate: float
    context_retention_rate: float
    goal_completion_rate: float

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class InteractionMetrics:
    """Metrics for individual AI interactions."""
    timestamp: str
    command: str
    user_input_length: int
    response_length: int
    clarification_needed: bool
    response_quality_score: float
    context_retained: bool
    template_used: bool

class BaselineCollector:
    """Collects and analyzes baseline AI performance metrics."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.metrics_path = project_path / ".goalkit" / "metrics"
        self.metrics_path.mkdir(parents=True, exist_ok=True)

    def collect_interaction_metrics(self, command: str, user_input: str,
                                  ai_response: str, success_score: float = None) -> InteractionMetrics:
        """Collect metrics for a single AI interaction."""

        # Analyze user input
        user_input_length = len(user_input)

        # Analyze AI response
        response_length = len(ai_response)

        # Check for clarification indicators
        clarification_indicators = [
            "clarify", "clarification", "unclear", "rephrase", "confused",
            "not sure", "please explain", "what do you mean"
        ]
        clarification_needed = any(indicator in ai_response.lower() for indicator in clarification_indicators)

        # Calculate response quality score (enhanced version of existing logic)
        quality_score = self._calculate_response_quality(ai_response, command)

        # Check context retention (simplified - would need session data)
        context_retained = self._assess_context_retention(command, user_input)

        # Check template usage (would need template detection)
        template_used = self._detect_template_usage(user_input)

        return InteractionMetrics(
            timestamp=datetime.now().isoformat(),
            command=command,
            user_input_length=user_input_length,
            response_length=response_length,
            clarification_needed=clarification_needed,
            response_quality_score=quality_score,
            context_retained=context_retained,
            template_used=template_used
        )

    def _calculate_response_quality(self, response: str, command: str) -> float:
        """Calculate quality score for AI response (0-10 scale)."""
        score = 5.0  # Base score

        # Length appropriateness
        if 50 <= len(response) <= 1000:
            score += 1.0
        elif len(response) < 50:
            score -= 1.0
        elif len(response) > 2000:
            score -= 0.5

        # Command relevance
        command_lower = command.lower()
        response_lower = response.lower()

        # Check if response addresses the command
        if command_lower in response_lower:
            score += 1.0

        # Check for structured content (markdown, lists, etc.)
        structure_indicators = ['*', '-', '#', '```', '**']
        if any(indicator in response for indicator in structure_indicators):
            score += 1.0

        # Check for actionable content
        action_words = ['create', 'implement', 'use', 'run', 'execute', 'build', 'develop']
        if any(word in response_lower for word in action_words):
            score += 1.0

        # Penalty for clarification requests
        clarification_words = ['clarify', 'unclear', 'confused', 'rephrase']
        if any(word in response_lower for word in clarification_words):
            score -= 2.0

        return max(0.0, min(10.0, score))

    def _assess_context_retention(self, command: str, user_input: str) -> bool:
        """Assess if AI retained context from previous interactions."""
        # Simplified context retention check
        context_indicators = ['previous', 'earlier', 'before', 'context', 'remember']
        combined_text = f"{command} {user_input}".lower()

        return any(indicator in combined_text for indicator in context_indicators)

    def _detect_template_usage(self, user_input: str) -> bool:
        """Detect if user is following structured template format."""
        template_indicators = [
            'success criteria', 'measurable outcome', 'acceptance criteria',
            'milestone', 'timeline', 'dependencies'
        ]

        return any(indicator in user_input.lower() for indicator in template_indicators)

    def save_interaction_metrics(self, metrics: InteractionMetrics) -> None:
        """Save interaction metrics to file."""
        metrics_file = self.metrics_path / "interaction_metrics.jsonl"

        with open(metrics_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(metrics.to_dict()) + '\n')

    def generate_baseline_report(self, days: int = 30) -> BaselineMetrics:
        """Generate baseline metrics report from collected data."""
        metrics_file = self.metrics_path / "interaction_metrics.jsonl"

        if not metrics_file.exists():
            # Return default baseline if no data available
            return BaselineMetrics(
                timestamp=datetime.now().isoformat(),
                total_interactions=0,
                successful_interactions=0,
                avg_clarification_requests=0.0,
                avg_response_quality_score=5.0,
                template_usage_rate=0.0,
                context_retention_rate=0.0,
                goal_completion_rate=0.0
            )

        # Read recent interactions
        cutoff_date = datetime.now() - timedelta(days=days)
        interactions = []

        with open(metrics_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    interaction_date = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))

                    if interaction_date >= cutoff_date:
                        interactions.append(data)
                except (json.JSONDecodeError, KeyError):
                    continue

        if not interactions:
            return BaselineMetrics(
                timestamp=datetime.now().isoformat(),
                total_interactions=0,
                successful_interactions=0,
                avg_clarification_requests=0.0,
                avg_response_quality_score=5.0,
                template_usage_rate=0.0,
                context_retention_rate=0.0,
                goal_completion_rate=0.0
            )

        # Calculate metrics
        total_interactions = len(interactions)
        clarification_requests = sum(1 for i in interactions if i.get('clarification_needed', False))
        quality_scores = [i.get('response_quality_score', 5.0) for i in interactions]
        template_usage = sum(1 for i in interactions if i.get('template_used', False))
        context_retention = sum(1 for i in interactions if i.get('context_retained', False))

        # Estimate goal completion rate (simplified)
        goal_completion_rate = 0.7  # Placeholder - would need actual goal tracking

        return BaselineMetrics(
            timestamp=datetime.now().isoformat(),
            total_interactions=total_interactions,
            successful_interactions=total_interactions - clarification_requests,
            avg_clarification_requests=clarification_requests / total_interactions,
            avg_response_quality_score=sum(quality_scores) / len(quality_scores),
            template_usage_rate=template_usage / total_interactions,
            context_retention_rate=context_retention / total_interactions,
            goal_completion_rate=goal_completion_rate
        )

    def save_baseline_report(self, baseline: BaselineMetrics) -> None:
        """Save baseline report to file."""
        report_file = self.metrics_path / "baseline_report.json"

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(baseline.to_dict(), f, indent=2)

class HypothesisTester:
    """Framework for testing hypotheses about AI performance improvements."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.tests_path = project_path / ".goalkit" / "tests"
        self.tests_path.mkdir(parents=True, exist_ok=True)

    def run_template_hypothesis_test(self) -> Dict[str, Any]:
        """Test hypothesis: 'Structured templates reduce AI clarification needs by 70%'"""
        collector = BaselineCollector(self.project_path)
        baseline = collector.generate_baseline_report()

        test_results = {
            "hypothesis": "Structured templates with measurable success criteria will reduce AI clarification needs by 70%",
            "baseline_clarification_rate": baseline.avg_clarification_requests,
            "baseline_template_usage": baseline.template_usage_rate,
            "current_status": "baseline_established",
            "next_steps": [
                "Implement enhanced goal templates",
                "Collect data with new template system",
                "Compare clarification rates between template and non-template usage",
                "Validate hypothesis with A/B testing"
            ]
        }

        return test_results

    def run_context_hypothesis_test(self) -> Dict[str, Any]:
        """Test hypothesis: 'Enhanced context management will increase goal completion rates by 60%'"""
        collector = BaselineCollector(self.project_path)
        baseline = collector.generate_baseline_report()

        test_results = {
            "hypothesis": "Enhanced context management will increase goal completion rates by 60%",
            "baseline_context_retention": baseline.context_retention_rate,
            "baseline_completion_rate": baseline.goal_completion_rate,
            "current_status": "baseline_established",
            "next_steps": [
                "Enhance AISessionMemory system",
                "Implement session management for decision history",
                "Add context-aware command suggestions",
                "Measure context retention across session transitions"
            ]
        }

        return test_results

    def run_validation_hypothesis_test(self) -> Dict[str, Any]:
        """Test hypothesis: 'Enhanced validation will achieve 90% user satisfaction with AI responses'"""
        collector = BaselineCollector(self.project_path)
        baseline = collector.generate_baseline_report()

        test_results = {
            "hypothesis": "Enhanced validation will achieve 90% user satisfaction with AI responses",
            "baseline_quality_score": baseline.avg_response_quality_score,
            "current_status": "baseline_established",
            "next_steps": [
                "Enhance validate_ai_response function",
                "Create validation standards for each command type",
                "Implement automatic feedback for AI improvement",
                "Measure user satisfaction with enhanced validation"
            ]
        }

        return test_results

    def run_all_hypothesis_tests(self) -> Dict[str, Any]:
        """Run all hypothesis tests and return comprehensive results."""
        return {
            "timestamp": datetime.now().isoformat(),
            "test_results": {
                "template_hypothesis": self.run_template_hypothesis_test(),
                "context_hypothesis": self.run_context_hypothesis_test(),
                "validation_hypothesis": self.run_validation_hypothesis_test()
            },
            "summary": {
                "total_hypotheses": 3,
                "baseline_established": True,
                "ready_for_implementation": True
            }
        }

def initialize_baseline_system(project_path: Path) -> None:
    """Initialize the baseline measurement system."""
    collector = BaselineCollector(project_path)

    # Generate initial baseline report
    baseline = collector.generate_baseline_report()

    # Save baseline report
    collector.save_baseline_report(baseline)

    # Run hypothesis tests
    tester = HypothesisTester(project_path)
    test_results = tester.run_all_hypothesis_tests()

    # Save test results
    tests_file = project_path / ".goalkit" / "tests" / "hypothesis_tests.json"
    with open(tests_file, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, indent=2)

    print("Baseline measurement system initialized")
    print(f"Baseline clarification rate: {baseline.avg_clarification_requests:.2%}")
    print(f"Baseline quality score: {baseline.avg_response_quality_score:.1f}/10")
    print(f"🎯 Ready for hypothesis testing and AI enhancements")

# Convenience functions for CLI integration
def get_baseline_collector(project_path: Path) -> BaselineCollector:
    """Get baseline collector for project."""
    return BaselineCollector(project_path)

def get_hypothesis_tester(project_path: Path) -> HypothesisTester:
    """Get hypothesis tester for project."""
    return HypothesisTester(project_path)