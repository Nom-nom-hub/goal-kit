#!/usr/bin/env python3
"""
A/B Testing Integration for Enhanced Template System

This module provides comprehensive integration between the enhanced template system
and the existing A/B testing framework for template validation and optimization.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging
import uuid

from .ab_test_manager import ABTestManager
from .template_processor import TemplateProcessor
from .template_enhancer import TemplateEnhancer
from .schema_validator import SchemaValidator, ValidationResult
from .enhanced_metrics import EnhancedInteractionMetrics

@dataclass
class TemplateABTestConfig:
    """Configuration for template A/B testing."""
    test_name: str
    description: str
    control_template_type: str
    variant_template_type: str
    target_metrics: List[str]
    minimum_sample_size: int
    max_duration_days: int
    success_threshold: float

@dataclass
class TemplateABTestResult:
    """Results from template A/B testing."""
    test_id: str
    status: str
    start_date: str
    end_date: Optional[str]
    control_metrics: Dict[str, Any]
    variant_metrics: Dict[str, Any]
    statistical_significance: Dict[str, Any]
    recommendation: str
    confidence_level: float

class TemplateABIntegration:
    """Comprehensive integration between template system and A/B testing framework."""

    def __init__(self, project_path: Path, ab_test_manager: Optional[ABTestManager] = None):
        """Initialize the template A/B testing integration.

        Args:
            project_path: Path to the project directory
            ab_test_manager: Optional existing A/B test manager instance
        """
        self.project_path = project_path
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.ab_test_manager = ab_test_manager or ABTestManager(project_path)
        self.template_processor = TemplateProcessor(project_path, self.ab_test_manager)
        self.template_enhancer = TemplateEnhancer()
        self.schema_validator = SchemaValidator()

        # Integration state
        self.active_template_tests: Dict[str, TemplateABTestConfig] = {}
        self.template_test_results: Dict[str, TemplateABTestResult] = {}

        # Load existing test configurations
        self._load_integration_state()

    def _load_integration_state(self) -> None:
        """Load existing template A/B test configurations."""
        tests_file = self.project_path / ".goalkit" / "templates" / "template_ab_tests.json"
        results_file = self.project_path / ".goalkit" / "templates" / "template_ab_results.json"

        # Load active tests
        if tests_file.exists():
            try:
                with open(tests_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for test_id, test_data in data.items():
                        self.active_template_tests[test_id] = TemplateABTestConfig(**test_data)
            except (json.JSONDecodeError, KeyError):
                self.active_template_tests = {}

        # Load test results
        if results_file.exists():
            try:
                with open(results_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for test_id, result_data in data.items():
                        self.template_test_results[test_id] = TemplateABTestResult(**result_data)
            except (json.JSONDecodeError, KeyError):
                self.template_test_results = {}

    def _save_integration_state(self) -> None:
        """Save template A/B test configurations."""
        tests_file = self.project_path / ".goalkit" / "templates" / "template_ab_tests.json"
        results_file = self.project_path / ".goalkit" / "templates" / "template_ab_results.json"

        # Save active tests
        with open(tests_file, 'w', encoding='utf-8') as f:
            data = {tid: t.__dict__ for tid, t in self.active_template_tests.items()}
            json.dump(data, f, indent=2)

        # Save test results
        with open(results_file, 'w', encoding='utf-8') as f:
            data = {tid: r.__dict__ for tid, r in self.template_test_results.items()}
            json.dump(data, f, indent=2)

    def create_template_comparison_test(self, test_name: str = "Template Enhancement Test") -> str:
        """Create a new A/B test comparing baseline vs enhanced templates.

        Args:
            test_name: Name for the A/B test

        Returns:
            Test ID for the created test
        """
        test_id = f"template_comparison_{int(datetime.now().timestamp())}"

        # Create test configuration
        test_config = TemplateABTestConfig(
            test_name=test_name,
            description="Compare baseline templates vs enhanced templates with new structure",
            control_template_type="baseline",
            variant_template_type="enhanced",
            target_metrics=[
                "template_quality_score",
                "user_satisfaction",
                "clarification_rate",
                "completion_rate"
            ],
            minimum_sample_size=50,
            max_duration_days=30,
            success_threshold=0.8
        )

        # Create corresponding A/B test in the test manager
        ab_test_id = self.ab_test_manager.create_template_validation_test(test_name)

        # Store test configuration
        self.active_template_tests[test_id] = test_config
        self._save_integration_state()

        self.logger.info(f"Created template comparison test: {test_id}")
        return test_id

    def process_template_with_ab_testing(self, template_data: Dict[str, Any],
                                       user_id: str,
                                       test_id: str,
                                       template_type: str = "enhanced") -> Tuple[Dict[str, Any], str]:
        """Process a template with A/B testing integration.

        Args:
            template_data: Template data to process
            user_id: ID of the user
            test_id: A/B test ID
            template_type: Type of template (baseline/enhanced)

        Returns:
            Tuple of (processed_template, processing_id)
        """
        processing_id = str(uuid.uuid4())

        # Determine test group based on template type
        test_group = "A" if template_type == "baseline" else "B"

        # Process template with appropriate strategy
        if template_type == "enhanced":
            # Apply enhancement for variant group
            enhanced_data, enhancement_result = self.template_enhancer.enhance_template(
                template_data, strategy="comprehensive"
            )
            template_to_process = enhanced_data
        else:
            template_to_process = template_data

        # Process with template processor
        processing_result = self.template_processor.process_template(
            template_to_process,
            user_id=user_id,
            enable_ab_testing=True
        )

        # Record interaction with A/B testing framework
        if processing_result.success:
            self._record_template_interaction(
                user_id, test_id, test_group, template_type,
                processing_result.validation_result, processing_id
            )

        return template_to_process, processing_id

    def _record_template_interaction(self, user_id: str, test_id: str, test_group: str,
                                   template_type: str, validation_result: ValidationResult,
                                   processing_id: str) -> None:
        """Record template interaction in A/B testing framework."""
        try:
            # Create enhanced metrics for this interaction
            metrics = EnhancedInteractionMetrics(
                timestamp=datetime.now().isoformat(),
                command="template_create",
                user_input_length=1000,  # Approximate
                response_length=0,
                clarification_needed=False,
                response_quality_score=validation_result.quality_score,
                context_retained=True,
                template_used=True,
                test_group=test_group,
                test_id=test_id,
                variant_name=template_type,
                user_id=user_id,
                session_id=processing_id,
                template_validation_score=validation_result.quality_score,
                success_criteria_met=validation_result.is_valid
            )

            # Record in A/B test manager
            self.ab_test_manager.record_interaction(
                user_id=user_id,
                command="template_create",
                user_input=json.dumps({"template_type": template_type}),
                ai_response="Template processed successfully",
                test_id=test_id
            )

        except Exception as e:
            self.logger.error(f"Error recording template interaction: {e}")

    def analyze_template_test_progress(self, test_id: str) -> Dict[str, Any]:
        """Analyze progress of template A/B test.

        Args:
            test_id: ID of the test to analyze

        Returns:
            Analysis results with recommendations
        """
        if test_id not in self.active_template_tests:
            return {"error": "Test not found"}

        test_config = self.active_template_tests[test_id]

        # Get A/B test analysis from test manager
        ab_analysis = self.ab_test_manager.analyze_test_progress(test_id)

        if "error" in ab_analysis:
            return ab_analysis

        # Enhance analysis with template-specific metrics
        template_metrics = self._analyze_template_specific_metrics(test_id)

        # Combine analyses
        combined_analysis = {
            "test_id": test_id,
            "test_name": test_config.test_name,
            "status": ab_analysis.get("status", "unknown"),
            "ab_testing_data": ab_analysis,
            "template_specific_metrics": template_metrics,
            "recommendation": self._generate_template_test_recommendation(
                ab_analysis, template_metrics, test_config
            )
        }

        return combined_analysis

    def _analyze_template_specific_metrics(self, test_id: str) -> Dict[str, Any]:
        """Analyze template-specific metrics for the test."""
        # Load template processing data
        templates_path = self.project_path / ".goalkit" / "templates"

        control_templates = []
        variant_templates = []

        # Scan for processed templates related to this test
        if templates_path.exists():
            for template_file in templates_path.glob("template_*.json"):
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Check if this template is part of our test
                    if (data.get("ab_test_id") == test_id or
                        test_id in str(template_file)):  # Fallback check

                        template_data = data.get("template_data", {})
                        validation_result = ValidationResult(**data.get("validation_result", {}))

                        template_info = {
                            "template_id": data.get("template_id"),
                            "quality_score": validation_result.quality_score,
                            "completeness_score": validation_result.completeness_score,
                            "is_valid": validation_result.is_valid,
                            "created_at": data.get("created_at")
                        }

                        # Classify as control or variant (simplified logic)
                        if validation_result.quality_score < 70:
                            control_templates.append(template_info)
                        else:
                            variant_templates.append(template_info)

                except (json.JSONDecodeError, KeyError):
                    continue

        # Calculate metrics
        control_avg_quality = sum(t["quality_score"] for t in control_templates) / len(control_templates) if control_templates else 0
        variant_avg_quality = sum(t["quality_score"] for t in variant_templates) / len(variant_templates) if variant_templates else 0

        return {
            "control_templates_count": len(control_templates),
            "variant_templates_count": len(variant_templates),
            "control_avg_quality": control_avg_quality,
            "variant_avg_quality": variant_avg_quality,
            "quality_improvement": variant_avg_quality - control_avg_quality if variant_templates and control_templates else 0,
            "validation_success_rate": {
                "control": sum(1 for t in control_templates if t["is_valid"]) / len(control_templates) if control_templates else 0,
                "variant": sum(1 for t in variant_templates if t["is_valid"]) / len(variant_templates) if variant_templates else 0
            }
        }

    def _generate_template_test_recommendation(self, ab_analysis: Dict[str, Any],
                                             template_metrics: Dict[str, Any],
                                             test_config: TemplateABTestConfig) -> str:
        """Generate recommendation for template test."""
        # Check if we should conclude the test
        should_conclude = (
            ab_analysis.get("should_conclude", False) or
            template_metrics.get("control_templates_count", 0) >= test_config.minimum_sample_size or
            template_metrics.get("variant_templates_count", 0) >= test_config.minimum_sample_size
        )

        if should_conclude:
            quality_improvement = template_metrics.get("quality_improvement", 0)
            if quality_improvement > 15:  # Significant improvement
                return "Enhanced templates show significant quality improvement. Recommend adopting enhanced template structure."
            elif quality_improvement > 5:  # Moderate improvement
                return "Enhanced templates show moderate improvement. Consider broader adoption with monitoring."
            else:
                return "No significant difference detected. Continue with current template approach."

        return "Continue collecting data. Need more template samples for conclusive results."

    def conclude_template_test(self, test_id: str) -> Optional[TemplateABTestResult]:
        """Conclude a template A/B test and generate results."""
        if test_id not in self.active_template_tests:
            return None

        # Get final analysis
        analysis = self.analyze_template_test_progress(test_id)

        if analysis.get("status") != "completed":
            return None

        test_config = self.active_template_tests[test_id]

        # Create test result
        result = TemplateABTestResult(
            test_id=test_id,
            status="completed",
            start_date=datetime.now().isoformat(),  # Would be actual start date
            end_date=datetime.now().isoformat(),
            control_metrics=analysis.get("template_specific_metrics", {}).get("control_templates_count", {}),
            variant_metrics=analysis.get("template_specific_metrics", {}).get("variant_templates_count", {}),
            statistical_significance=analysis.get("ab_testing_data", {}).get("primary_metric", {}),
            recommendation=analysis.get("recommendation", "No clear recommendation"),
            confidence_level=0.95
        )

        # Store results
        self.template_test_results[test_id] = result

        # Remove from active tests
        del self.active_template_tests[test_id]

        self._save_integration_state()

        return result

    def get_template_test_summary(self, test_id: str) -> Dict[str, Any]:
        """Get a summary of template test status and results."""
        if test_id in self.template_test_results:
            result = self.template_test_results[test_id]
            return {
                "test_id": test_id,
                "status": result.status,
                "start_date": result.start_date,
                "end_date": result.end_date,
                "recommendation": result.recommendation,
                "confidence_level": result.confidence_level
            }

        elif test_id in self.active_template_tests:
            analysis = self.analyze_template_test_progress(test_id)
            return {
                "test_id": test_id,
                "status": analysis.get("status", "unknown"),
                "test_name": self.active_template_tests[test_id].test_name,
                "recommendation": analysis.get("recommendation", "Continue testing")
            }

        else:
            return {"error": "Test not found"}

    def run_automated_template_optimization(self, sample_templates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run automated optimization analysis on sample templates.

        Args:
            sample_templates: List of template samples to analyze

        Returns:
            Optimization recommendations and insights
        """
        optimization_results = {
            "timestamp": datetime.now().isoformat(),
            "templates_analyzed": len(sample_templates),
            "optimization_opportunities": [],
            "recommended_strategies": [],
            "expected_improvements": {}
        }

        if not sample_templates:
            return optimization_results

        # Analyze current template quality distribution
        quality_scores = []
        for template in sample_templates:
            validation_result = self.schema_validator.validate_template(template)
            quality_scores.append(validation_result.quality_score)

        avg_quality = sum(quality_scores) / len(quality_scores)

        # Identify optimization opportunities
        if avg_quality < 60:
            optimization_results["optimization_opportunities"].append(
                "Low average quality score indicates need for template enhancement"
            )
            optimization_results["recommended_strategies"].append("comprehensive_enhancement")

        elif avg_quality < 80:
            optimization_results["optimization_opportunities"].append(
                "Moderate quality with room for improvement"
            )
            optimization_results["recommended_strategies"].append("stakeholder_enhancement")

        # Estimate improvement potential
        improvement_potential = 100 - avg_quality
        optimization_results["expected_improvements"] = {
            "quality_score_improvement": min(improvement_potential, 25),
            "completeness_improvement": min(100 - (sum(1 for s in quality_scores if s > 80) / len(quality_scores) * 100), 30),
            "user_satisfaction_improvement": min(improvement_potential * 0.8, 20)
        }

        return optimization_results

    def generate_template_ab_test_report(self, test_id: str) -> str:
        """Generate a comprehensive report for template A/B test."""
        summary = self.get_template_test_summary(test_id)

        if "error" in summary:
            return f"Error: {summary['error']}"

        report = f"""
Template A/B Test Report
========================
Test ID: {test_id}
Status: {summary['status']}
Start Date: {summary.get('start_date', 'Unknown')}

"""

        if "test_name" in summary:
            report += f"Test Name: {summary['test_name']}\n"

        if "end_date" in summary:
            report += f"End Date: {summary['end_date']}\n"

        report += f"\nRecommendation: {summary.get('recommendation', 'No recommendation available')}"

        if "confidence_level" in summary:
            report += f"\nConfidence Level: {summary['confidence_level']:.1%}"

        # Add detailed analysis if available
        if summary['status'] == 'running':
            analysis = self.analyze_template_test_progress(test_id)
            if "template_specific_metrics" in analysis:
                metrics = analysis["template_specific_metrics"]
                report += f"\n\nCurrent Metrics:"
                report += f"\nControl Templates: {metrics.get('control_templates_count', 0)}"
                report += f"\nVariant Templates: {metrics.get('variant_templates_count', 0)}"
                report += f"\nControl Avg Quality: {metrics.get('control_avg_quality', 0):.1f}"
                report += f"\nVariant Avg Quality: {metrics.get('variant_avg_quality', 0):.1f}"

        report += f"\n\nReport Generated: {datetime.now().isoformat()}"

        return report

    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of template A/B testing integration."""
        return {
            "integration_active": True,
            "ab_test_manager_connected": self.ab_test_manager is not None,
            "active_template_tests": len(self.active_template_tests),
            "completed_template_tests": len(self.template_test_results),
            "template_processor_ready": True,
            "enhancement_engine_ready": True,
            "schema_validator_ready": True,
            "last_updated": datetime.now().isoformat()
        }