#!/usr/bin/env python3
"""
Template Enhancement Engine for Enhanced Goal Templates

This module provides logic to enhance existing templates with the new enhanced structure,
including migration utilities and enhancement algorithms.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Literal
from datetime import datetime
from dataclasses import dataclass, asdict
import logging

from .schema_validator import SchemaValidator, ValidationResult

@dataclass
class EnhancementResult:
    """Result of template enhancement operation."""
    success: bool
    original_template_id: str
    enhanced_template_id: str
    enhancement_actions: List[str]
    quality_improvement: float
    fields_added: List[str]
    fields_enhanced: List[str]
    enhancement_timestamp: str
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class EnhancementStrategy:
    """Strategy for enhancing different types of templates."""
    strategy_id: str
    name: str
    description: str
    target_template_types: List[str]
    enhancement_priority: int
    estimated_effort: str

class TemplateEnhancer:
    """Engine for enhancing existing templates with new enhanced structure."""

    def __init__(self, schema_path: Optional[Path] = None):
        """Initialize the template enhancer.

        Args:
            schema_path: Path to the enhanced template schema
        """
        self.logger = logging.getLogger(__name__)
        self.schema_validator = SchemaValidator(schema_path)

        # Enhancement strategies
        self.strategies = self._initialize_enhancement_strategies()

        # Enhancement patterns and templates
        self.enhancement_patterns = self._initialize_enhancement_patterns()

    def _initialize_enhancement_strategies(self) -> Dict[str, EnhancementStrategy]:
        """Initialize available enhancement strategies."""
        return {
            "basic_enhancement": EnhancementStrategy(
                strategy_id="basic_enhancement",
                name="Basic Structure Enhancement",
                description="Add missing core fields and basic structure",
                target_template_types=["goal", "vision", "milestone"],
                enhancement_priority=1,
                estimated_effort="5-10 minutes"
            ),
            "comprehensive_enhancement": EnhancementStrategy(
                strategy_id="comprehensive_enhancement",
                name="Comprehensive Enhancement",
                description="Full enhancement with all advanced features",
                target_template_types=["goal", "vision"],
                enhancement_priority=2,
                estimated_effort="15-20 minutes"
            ),
            "stakeholder_focused": EnhancementStrategy(
                strategy_id="stakeholder_focused",
                name="Stakeholder-Focused Enhancement",
                description="Emphasize stakeholder analysis and impact assessment",
                target_template_types=["goal", "vision"],
                enhancement_priority=3,
                estimated_effort="10-15 minutes"
            ),
            "validation_focused": EnhancementStrategy(
                strategy_id="validation_focused",
                name="Validation-Focused Enhancement",
                description="Emphasize measurement and validation frameworks",
                target_template_types=["goal", "milestone"],
                enhancement_priority=4,
                estimated_effort="10-15 minutes"
            )
        }

    def _initialize_enhancement_patterns(self) -> Dict[str, Any]:
        """Initialize patterns and templates for enhancement."""
        return {
            "success_criteria_patterns": [
                "Reduce [metric] by [percentage]% within [timeframe]",
                "Increase [metric] by [percentage]% within [timeframe]",
                "Achieve [target] [metric] by [date]",
                "Maintain [metric] above [threshold] for [duration]"
            ],
            "stakeholder_templates": {
                "primary_users": [
                    {
                        "user_type": "End Users",
                        "current_pain_point": "Current challenge or problem",
                        "goal_benefit": "Specific benefit from goal achievement",
                        "success_impact": "Measurable impact on user experience"
                    }
                ],
                "key_stakeholders": [
                    {
                        "stakeholder": "Project Team",
                        "interest": "Successful project delivery",
                        "influence": "High - direct responsibility",
                        "success_criteria": "Meet project objectives and quality standards"
                    }
                ]
            },
            "milestone_templates": {
                "planning": {
                    "title": "Planning & Requirements",
                    "priority": "P1",
                    "focus": "Define detailed requirements and approach",
                    "success_indicators": ["Requirements documented", "Approach validated"],
                    "effort_estimate": "1-2 weeks",
                    "timeline": "Week 1-2"
                },
                "implementation": {
                    "title": "Core Implementation",
                    "priority": "P1",
                    "focus": "Build and deliver core functionality",
                    "success_indicators": ["Core features implemented", "Testing completed"],
                    "effort_estimate": "3-4 weeks",
                    "timeline": "Week 3-6"
                },
                "validation": {
                    "title": "Validation & Deployment",
                    "priority": "P1",
                    "focus": "Final validation and launch preparation",
                    "success_indicators": ["All criteria met", "User acceptance confirmed"],
                    "effort_estimate": "1-2 weeks",
                    "timeline": "Week 7-8"
                }
            }
        }

    def enhance_template(self, template_data: Dict[str, Any],
                        strategy: Literal["basic", "comprehensive", "stakeholder", "validation"] = "basic",
                        preserve_original: bool = True) -> Tuple[Dict[str, Any], EnhancementResult]:
        """Enhance a template using the specified strategy.

        Args:
            template_data: The original template data
            strategy: Enhancement strategy to use
            preserve_original: Whether to preserve original field values

        Returns:
            Tuple of (enhanced_template_data, enhancement_result)
        """
        original_id = template_data.get("id", "unknown")
        enhanced_data = template_data.copy() if preserve_original else {}

        enhancement_actions = []
        fields_added = []
        fields_enhanced = []

        try:
            # Get the appropriate strategy
            strategy_key = f"{strategy}_enhancement"
            if strategy_key not in self.strategies:
                raise ValueError(f"Unknown enhancement strategy: {strategy}")

            enhancement_strategy = self.strategies[strategy_key]

            # Apply enhancements based on strategy
            if strategy == "basic":
                enhanced_data, actions, added, enhanced = self._apply_basic_enhancement(enhanced_data)
            elif strategy == "comprehensive":
                enhanced_data, actions, added, enhanced = self._apply_comprehensive_enhancement(enhanced_data)
            elif strategy == "stakeholder":
                enhanced_data, actions, added, enhanced = self._apply_stakeholder_enhancement(enhanced_data)
            elif strategy == "validation":
                enhanced_data, actions, added, enhanced = self._apply_validation_enhancement(enhanced_data)

            enhancement_actions.extend(actions)
            fields_added.extend(added)
            fields_enhanced.extend(enhanced)

            # Validate the enhanced template
            validation_result = self.schema_validator.validate_template(enhanced_data)

            # Calculate quality improvement
            original_quality = self._estimate_original_quality(template_data)
            quality_improvement = validation_result.quality_score - original_quality

            result = EnhancementResult(
                success=True,
                original_template_id=original_id,
                enhanced_template_id=f"{original_id}_enhanced",
                enhancement_actions=enhancement_actions,
                quality_improvement=quality_improvement,
                fields_added=fields_added,
                fields_enhanced=fields_enhanced,
                enhancement_timestamp=datetime.now().isoformat()
            )

            return enhanced_data, result

        except Exception as e:
            self.logger.error(f"Error enhancing template: {e}")
            return template_data, EnhancementResult(
                success=False,
                original_template_id=original_id,
                enhanced_template_id="",
                enhancement_actions=[],
                quality_improvement=0.0,
                fields_added=[],
                fields_enhanced=[],
                enhancement_timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )

    def _apply_basic_enhancement(self, template_data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str], List[str], List[str]]:
        """Apply basic enhancement strategy."""
        enhanced_data = template_data.copy()
        actions = []
        fields_added = []
        fields_enhanced = []

        # Enhance goal statement if present
        if "goal_statement" in enhanced_data:
            original_statement = enhanced_data["goal_statement"]
            enhanced_data["goal_statement"] = self._enhance_goal_statement_basic(original_statement)
            if enhanced_data["goal_statement"] != original_statement:
                fields_enhanced.append("goal_statement")
                actions.append("Enhanced goal statement with outcome-focused language")

        # Add problem context if missing
        if "problem_context" not in enhanced_data:
            enhanced_data["problem_context"] = self._generate_problem_context(enhanced_data)
            fields_added.append("problem_context")
            actions.append("Added problem context based on goal analysis")

        # Add success outcome if missing
        if "success_outcome" not in enhanced_data:
            enhanced_data["success_outcome"] = self._generate_success_outcome(enhanced_data)
            fields_added.append("success_outcome")
            actions.append("Added success outcome definition")

        # Add basic primary criteria if missing
        if "primary_criteria" not in enhanced_data:
            enhanced_data["primary_criteria"] = self._generate_basic_primary_criteria(enhanced_data)
            fields_added.append("primary_criteria")
            actions.append("Added basic primary success criteria")

        return enhanced_data, actions, fields_added, fields_enhanced

    def _apply_comprehensive_enhancement(self, template_data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str], List[str], List[str]]:
        """Apply comprehensive enhancement strategy."""
        # Start with basic enhancement
        enhanced_data, basic_actions, basic_added, basic_enhanced = self._apply_basic_enhancement(template_data)

        actions = basic_actions
        fields_added = basic_added
        fields_enhanced = basic_enhanced

        # Add stakeholder analysis
        if "stakeholder_impact_analysis" not in enhanced_data:
            enhanced_data["stakeholder_impact_analysis"] = self._generate_comprehensive_stakeholder_analysis(enhanced_data)
            fields_added.append("stakeholder_impact_analysis")
            actions.append("Added comprehensive stakeholder impact analysis")

        # Add hypothesis framework
        if "hypothesis_framework" not in enhanced_data:
            enhanced_data["hypothesis_framework"] = self._generate_hypothesis_framework(enhanced_data)
            fields_added.append("hypothesis_framework")
            actions.append("Added hypothesis framework with core hypotheses")

        # Add milestone structure
        if "milestone_structure" not in enhanced_data:
            enhanced_data["milestone_structure"] = self._generate_comprehensive_milestones(enhanced_data)
            fields_added.append("milestone_structure")
            actions.append("Added comprehensive milestone structure")

        # Add validation framework
        if "validation_framework" not in enhanced_data:
            enhanced_data["validation_framework"] = self._generate_validation_framework(enhanced_data)
            fields_added.append("validation_framework")
            actions.append("Added validation framework with measurement strategy")

        return enhanced_data, actions, fields_added, fields_enhanced

    def _apply_stakeholder_enhancement(self, template_data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str], List[str], List[str]]:
        """Apply stakeholder-focused enhancement strategy."""
        enhanced_data, actions, fields_added, fields_enhanced = self._apply_basic_enhancement(template_data)

        # Enhance stakeholder analysis specifically
        if "stakeholder_impact_analysis" in enhanced_data:
            original_analysis = enhanced_data["stakeholder_impact_analysis"]
            enhanced_data["stakeholder_impact_analysis"] = self._enhance_stakeholder_analysis_detailed(original_analysis)
            fields_enhanced.append("stakeholder_impact_analysis")
            actions.append("Enhanced stakeholder analysis with detailed impact assessment")
        else:
            enhanced_data["stakeholder_impact_analysis"] = self._generate_detailed_stakeholder_analysis(enhanced_data)
            fields_added.append("stakeholder_impact_analysis")
            actions.append("Added detailed stakeholder impact analysis")

        return enhanced_data, actions, fields_added, fields_enhanced

    def _apply_validation_enhancement(self, template_data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str], List[str], List[str]]:
        """Apply validation-focused enhancement strategy."""
        enhanced_data, actions, fields_added, fields_enhanced = self._apply_basic_enhancement(template_data)

        # Enhance validation framework
        if "validation_framework" in enhanced_data:
            original_validation = enhanced_data["validation_framework"]
            enhanced_data["validation_framework"] = self._enhance_validation_framework_detailed(original_validation)
            fields_enhanced.append("validation_framework")
            actions.append("Enhanced validation framework with detailed measurement strategy")
        else:
            enhanced_data["validation_framework"] = self._generate_detailed_validation_framework(enhanced_data)
            fields_added.append("validation_framework")
            actions.append("Added detailed validation framework")

        # Enhance primary criteria with detailed measurement methods
        if "primary_criteria" in enhanced_data:
            original_criteria = enhanced_data["primary_criteria"]
            enhanced_data["primary_criteria"] = self._enhance_primary_criteria_detailed(original_criteria)
            fields_enhanced.append("primary_criteria")
            actions.append("Enhanced primary criteria with detailed measurement methods")

        return enhanced_data, actions, fields_added, fields_enhanced

    def _enhance_goal_statement_basic(self, goal_statement: str) -> str:
        """Apply basic enhancement to goal statement."""
        enhanced = goal_statement.strip()

        # Ensure minimum length and structure
        if len(enhanced) < 50:
            enhanced += " with clear success criteria and measurable outcomes."

        # Add outcome-focused language if missing
        outcome_words = ["achieve", "deliver", "create", "build", "establish", "enable"]
        has_outcome = any(word in enhanced.lower() for word in outcome_words)

        if not has_outcome:
            enhanced = f"Achieve: {enhanced}"

        return enhanced

    def _generate_problem_context(self, template_data: Dict[str, Any]) -> str:
        """Generate problem context based on existing template data."""
        goal_statement = template_data.get("goal_statement", "")

        # Extract problem indicators from goal statement
        if "reduce" in goal_statement.lower():
            return "Current processes are inefficient and need optimization to reduce time and resource usage."
        elif "increase" in goal_statement.lower() or "improve" in goal_statement.lower():
            return "Current performance levels are below desired standards and need enhancement."
        else:
            return "There is an opportunity to improve current practices and achieve better outcomes."

    def _generate_success_outcome(self, template_data: Dict[str, Any]) -> str:
        """Generate success outcome based on template data."""
        goal_statement = template_data.get("goal_statement", "")

        # Create outcome-focused success definition
        if "system" in goal_statement.lower():
            return "A fully functional and validated system that meets all specified requirements and user needs."
        elif "process" in goal_statement.lower():
            return "Streamlined and efficient processes that deliver consistent, high-quality results."
        else:
            return "Successful achievement of all defined objectives with measurable positive impact."

    def _generate_basic_primary_criteria(self, template_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic primary criteria."""
        return [
            {
                "criterion": "Successful completion of core objectives",
                "target": "100% completion within specified timeframe",
                "measurement_method": "Track progress against milestones and deliverables",
                "validation": "Verify all requirements are met and objectives achieved"
            },
            {
                "criterion": "Quality standards met",
                "target": "Meet or exceed defined quality thresholds",
                "measurement_method": "Regular quality assessments and reviews",
                "validation": "Quality metrics show achievement of standards"
            }
        ]

    def _generate_comprehensive_stakeholder_analysis(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive stakeholder analysis."""
        return {
            "primary_users": [
                {
                    "user_type": "End Users",
                    "current_pain_point": "Challenges identified in current state",
                    "goal_benefit": "Direct benefits from goal achievement",
                    "success_impact": "Measurable improvement in user satisfaction and productivity"
                },
                {
                    "user_type": "Support Staff",
                    "current_pain_point": "Operational inefficiencies",
                    "goal_benefit": "Improved tools and processes",
                    "success_impact": "Reduced support burden and increased efficiency"
                }
            ],
            "key_stakeholders": [
                {
                    "stakeholder": "Project Sponsor",
                    "interest": "Business value and ROI",
                    "influence": "High - funding and strategic direction",
                    "success_criteria": "Achieve targeted business outcomes and ROI"
                },
                {
                    "stakeholder": "Development Team",
                    "interest": "Technical success and quality delivery",
                    "influence": "High - implementation responsibility",
                    "success_criteria": "Deliver high-quality solution on time and within budget"
                },
                {
                    "stakeholder": "End User Representatives",
                    "interest": "Usability and effectiveness",
                    "influence": "Medium - feedback and validation",
                    "success_criteria": "Solution meets user needs and expectations"
                }
            ]
        }

    def _generate_hypothesis_framework(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate hypothesis framework."""
        return {
            "core_hypotheses": [
                {
                    "hypothesis": "If we implement the defined solution, then we will achieve the targeted outcomes",
                    "why_critical": "This hypothesis validates the core approach and expected benefits",
                    "validation_approach": "Measure outcomes against baseline and success criteria",
                    "success_threshold": "Achieve at least 80% of targeted outcomes"
                }
            ],
            "supporting_assumptions": [
                {
                    "assumption": "Required resources will be available",
                    "impact_if_wrong": "Project delays and potential failure",
                    "validation_method": "Confirm resource availability early in project"
                }
            ]
        }

    def _generate_comprehensive_milestones(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive milestone structure."""
        patterns = self.enhancement_patterns["milestone_templates"]

        return {
            "milestones": [
                {
                    **patterns["planning"],
                    "hypothesis_validation": {
                        "tests": "Requirements are well-defined and achievable",
                        "validation_method": "Stakeholder review and technical assessment"
                    },
                    "value_delivered": {
                        "user_value": "Clear project direction and scope",
                        "learning_value": "Requirements validation and feasibility confirmation"
                    }
                },
                {
                    **patterns["implementation"],
                    "hypothesis_validation": {
                        "tests": "Implementation approach is effective",
                        "validation_method": "Progress reviews and quality testing"
                    },
                    "value_delivered": {
                        "user_value": "Functional solution addressing core needs",
                        "learning_value": "Implementation effectiveness and user feedback"
                    }
                },
                {
                    **patterns["validation"],
                    "hypothesis_validation": {
                        "tests": "Solution meets all success criteria",
                        "validation_method": "Comprehensive testing and user acceptance"
                    },
                    "value_delivered": {
                        "user_value": "Complete, validated solution ready for use",
                        "learning_value": "Success validation and lessons learned"
                    }
                }
            ]
        }

    def _generate_validation_framework(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate validation framework."""
        return {
            "measurement_strategy": {
                "data_sources": "Project metrics, user feedback, and system measurements",
                "measurement_frequency": "Weekly during implementation, monthly post-launch",
                "progress_indicators": "Milestone completion, quality metrics, user satisfaction"
            },
            "learning_capture_points": {
                "after_each_milestone": "Document lessons learned and improvement opportunities",
                "monthly_reviews": "Assess progress and adjust approach as needed",
                "success_validation": "Comprehensive review of all success criteria achievement"
            },
            "adaptation_triggers": {
                "pivot_indicators": "Major deviations from success criteria or stakeholder dissatisfaction",
                "acceleration_signals": "Faster-than-expected progress or positive feedback",
                "pause_conditions": "Critical blockers or resource constraints"
            }
        }

    def _enhance_stakeholder_analysis_detailed(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance existing stakeholder analysis with more detail."""
        enhanced = analysis.copy()

        # Add more stakeholder categories if missing
        if "secondary_stakeholders" not in enhanced:
            enhanced["secondary_stakeholders"] = [
                {
                    "stakeholder": "Operations Team",
                    "interest": "Smooth implementation and minimal disruption",
                    "influence": "Medium - operational impact",
                    "success_criteria": "Minimal operational disruption during implementation"
                }
            ]

        # Enhance existing stakeholders with more detail
        for user in enhanced.get("primary_users", []):
            if "quantified_benefit" not in user:
                user["quantified_benefit"] = "20-30% improvement in key metrics"

        return enhanced

    def _generate_detailed_stakeholder_analysis(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed stakeholder analysis."""
        base_analysis = self._generate_comprehensive_stakeholder_analysis(template_data)

        # Add additional detail
        for stakeholder in base_analysis["key_stakeholders"]:
            stakeholder["communication_frequency"] = "Weekly during project, monthly post-launch"
            stakeholder["engagement_level"] = "High - active participation required"

        return base_analysis

    def _enhance_validation_framework_detailed(self, framework: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance existing validation framework with more detail."""
        enhanced = framework.copy()

        # Add detailed measurement methods
        if "measurement_strategy" in enhanced:
            strategy = enhanced["measurement_strategy"]
            if "detailed_metrics" not in strategy:
                strategy["detailed_metrics"] = [
                    "Quantitative: response times, error rates, completion rates",
                    "Qualitative: user satisfaction scores, feedback analysis",
                    "Business: ROI, productivity gains, cost savings"
                ]

        return enhanced

    def _generate_detailed_validation_framework(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed validation framework."""
        base_framework = self._generate_validation_framework(template_data)

        # Add additional detail
        if "measurement_strategy" in base_framework:
            strategy = base_framework["measurement_strategy"]
            strategy["baseline_establishment"] = "Establish pre-implementation baselines for all metrics"
            strategy["comparison_methodology"] = "Statistical comparison of before/after measurements"

        return base_framework

    def _enhance_primary_criteria_detailed(self, criteria: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhance existing primary criteria with more detail."""
        enhanced_criteria = []

        for criterion in criteria:
            enhanced = criterion.copy()

            # Add detailed measurement methodology if missing
            if "detailed_measurement" not in enhanced:
                enhanced["detailed_measurement"] = f"Detailed methodology for measuring {criterion.get('criterion', 'this criterion')}"

            # Add data collection frequency if missing
            if "measurement_frequency" not in enhanced:
                enhanced["measurement_frequency"] = "Weekly during implementation, monthly post-launch"

            enhanced_criteria.append(enhanced)

        return enhanced_criteria

    def _estimate_original_quality(self, template_data: Dict[str, Any]) -> float:
        """Estimate the quality score of original template before enhancement."""
        # Simple heuristic based on field count and content
        field_count = len([k for k, v in template_data.items() if v])

        if field_count <= 2:
            return 30.0  # Very basic template
        elif field_count <= 4:
            return 50.0  # Basic template
        elif field_count <= 6:
            return 65.0  # Moderate template
        else:
            return 75.0  # Well-structured template

    def migrate_legacy_template(self, legacy_template: Dict[str, Any]) -> Tuple[Dict[str, Any], EnhancementResult]:
        """Migrate a legacy template to enhanced structure."""
        return self.enhance_template(legacy_template, strategy="comprehensive", preserve_original=False)

    def batch_enhance_templates(self, template_files: List[Path],
                              strategy: Literal["basic", "comprehensive", "stakeholder", "validation"] = "basic") -> List[EnhancementResult]:
        """Enhance multiple templates in batch."""
        results = []

        for template_file in template_files:
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)

                _, result = self.enhance_template(template_data, strategy)
                results.append(result)

            except Exception as e:
                self.logger.error(f"Error enhancing template {template_file}: {e}")
                results.append(EnhancementResult(
                    success=False,
                    original_template_id=str(template_file),
                    enhanced_template_id="",
                    enhancement_actions=[],
                    quality_improvement=0.0,
                    fields_added=[],
                    fields_enhanced=[],
                    enhancement_timestamp=datetime.now().isoformat(),
                    error_message=str(e)
                ))

        return results

    def get_enhancement_preview(self, template_data: Dict[str, Any],
                              strategy: Literal["basic", "comprehensive", "stakeholder", "validation"] = "basic") -> Dict[str, Any]:
        """Get a preview of what enhancement would do without applying it."""
        original_quality = self._estimate_original_quality(template_data)

        # Simulate enhancement
        temp_data, temp_result = self.enhance_template(template_data.copy(), strategy)

        validation_result = self.schema_validator.validate_template(temp_data)

        return {
            "original_quality_score": original_quality,
            "enhanced_quality_score": validation_result.quality_score,
            "expected_improvement": validation_result.quality_score - original_quality,
            "fields_to_add": temp_result.fields_added,
            "fields_to_enhance": temp_result.fields_enhanced,
            "enhancement_actions": temp_result.enhancement_actions,
            "estimated_effort": self.strategies[f"{strategy}_enhancement"].estimated_effort
        }