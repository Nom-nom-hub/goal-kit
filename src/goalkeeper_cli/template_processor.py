#!/usr/bin/env python3
"""
Template Processor for Enhanced Goal Templates

This module provides the core class to handle enhanced template processing and validation,
integrating with the schema validator and A/B testing framework.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Literal
from datetime import datetime
from dataclasses import dataclass, asdict
import logging
import uuid

from .schema_validator import SchemaValidator, ValidationResult
from .ab_test_manager import ABTestManager
from .enhanced_metrics import EnhancedInteractionMetrics

@dataclass
class TemplateProcessingResult:
    """Result of template processing operation."""
    success: bool
    template_id: str
    validation_result: ValidationResult
    processing_timestamp: str
    ab_test_id: Optional[str] = None
    enhancement_applied: bool = False
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class ProgressiveDisclosurePhase:
    """Defines a phase in the progressive disclosure system."""
    phase_id: str
    name: str
    description: str
    required_fields: List[str]
    optional_fields: List[str]
    user_guidance: str
    estimated_completion_time: str

class TemplateProcessor:
    """Core class for processing and validating enhanced goal templates."""

    def __init__(self, project_path: Path, ab_test_manager: Optional[ABTestManager] = None):
        """Initialize the template processor.

        Args:
            project_path: Path to the project directory
            ab_test_manager: Optional A/B test manager for integration
        """
        self.project_path = project_path
        self.templates_path = project_path / ".goalkit" / "templates"
        self.templates_path.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(__name__)
        self.schema_validator = SchemaValidator()
        self.ab_test_manager = ab_test_manager

        # Initialize progressive disclosure phases
        self.phases = self._initialize_progressive_phases()

        # Processing statistics
        self.processing_stats = {
            "total_processed": 0,
            "successful_validations": 0,
            "enhancement_applications": 0,
            "ab_test_integrations": 0
        }

    def _initialize_progressive_phases(self) -> Dict[str, ProgressiveDisclosurePhase]:
        """Initialize the progressive disclosure phases."""
        return {
            "phase_1_basic": ProgressiveDisclosurePhase(
                phase_id="phase_1_basic",
                name="Foundation",
                description="Establish core goal fundamentals",
                required_fields=[
                    "goal_statement",
                    "problem_context",
                    "success_outcome"
                ],
                optional_fields=[
                    "success_criteria_framework"
                ],
                user_guidance="Start with the essential elements that define your goal's purpose and desired outcome.",
                estimated_completion_time="5-10 minutes"
            ),
            "phase_2_intermediate": ProgressiveDisclosurePhase(
                phase_id="phase_2_intermediate",
                name="Strategy & Impact",
                description="Define success criteria and stakeholder impact",
                required_fields=[
                    "primary_criteria",
                    "stakeholder_impact_analysis"
                ],
                optional_fields=[
                    "secondary_criteria",
                    "hypothesis_framework"
                ],
                user_guidance="Now let's define how we'll measure success and who will be impacted by this goal.",
                estimated_completion_time="10-15 minutes"
            ),
            "phase_3_advanced": ProgressiveDisclosurePhase(
                phase_id="phase_3_advanced",
                name="Execution & Validation",
                description="Plan milestones and validation approach",
                required_fields=[
                    "milestone_structure",
                    "validation_framework"
                ],
                optional_fields=[
                    "dependency_structure",
                    "supporting_assumptions"
                ],
                user_guidance="Finally, let's break down the execution plan and establish validation methods.",
                estimated_completion_time="15-20 minutes"
            )
        }

    def process_template(self, template_data: Dict[str, Any],
                        user_id: str = "anonymous",
                        enable_ab_testing: bool = True,
                        enhancement_mode: Literal["none", "auto", "interactive"] = "auto") -> TemplateProcessingResult:
        """Process a template with validation and optional enhancement.

        Args:
            template_data: The template data to process
            user_id: ID of the user creating the template
            enable_ab_testing: Whether to integrate with A/B testing
            enhancement_mode: How to handle template enhancement

        Returns:
            TemplateProcessingResult with processing details
        """
        template_id = str(uuid.uuid4())
        processing_timestamp = datetime.now().isoformat()

        try:
            # Step 1: Validate the template
            validation_result = self.schema_validator.validate_template(template_data)

            # Step 2: Apply enhancement if needed
            enhancement_applied = False
            if enhancement_mode != "none" and validation_result.quality_score < 80:
                if enhancement_mode == "auto":
                    template_data, enhancement_applied = self._auto_enhance_template(template_data, validation_result)
                    # Re-validate after enhancement
                    validation_result = self.schema_validator.validate_template(template_data)
                elif enhancement_mode == "interactive":
                    # For interactive mode, would need user input - placeholder for now
                    pass

            # Step 3: Integrate with A/B testing if enabled
            ab_test_id = None
            if enable_ab_testing and self.ab_test_manager:
                ab_test_id = self._integrate_with_ab_testing(user_id, template_data, validation_result)

            # Step 4: Save the processed template
            self._save_processed_template(template_id, template_data, validation_result)

            # Step 5: Update processing statistics
            self._update_processing_stats(validation_result.is_valid, enhancement_applied,
                                        ab_test_id is not None)

            return TemplateProcessingResult(
                success=True,
                template_id=template_id,
                validation_result=validation_result,
                processing_timestamp=processing_timestamp,
                ab_test_id=ab_test_id,
                enhancement_applied=enhancement_applied
            )

        except Exception as e:
            self.logger.error(f"Error processing template: {e}")
            return TemplateProcessingResult(
                success=False,
                template_id=template_id,
                validation_result=ValidationResult(
                    is_valid=False,
                    quality_score=0.0,
                    errors=[str(e)],
                    warnings=[],
                    suggestions=["Check template format and try again"],
                    completeness_score=0.0,
                    field_scores={},
                    validation_timestamp=processing_timestamp
                ),
                processing_timestamp=processing_timestamp,
                error_message=str(e)
            )

    def _auto_enhance_template(self, template_data: Dict[str, Any], validation_result: ValidationResult) -> Tuple[Dict[str, Any], bool]:
        """Automatically enhance a template based on validation results."""
        enhanced_data = template_data.copy()
        enhancement_applied = False

        # Enhance goal statement if needed
        if "goal_statement" in enhanced_data and validation_result.field_scores.get("goal_statement", 0) < 70:
            enhanced_data["goal_statement"] = self._enhance_goal_statement(enhanced_data["goal_statement"])
            enhancement_applied = True

        # Add missing primary criteria if needed
        if "primary_criteria" not in enhanced_data or not enhanced_data["primary_criteria"]:
            enhanced_data["primary_criteria"] = self._generate_primary_criteria(enhanced_data)
            enhancement_applied = True

        # Enhance stakeholder analysis if missing or incomplete
        if ("stakeholder_impact_analysis" not in enhanced_data or
            validation_result.field_scores.get("stakeholder_impact_analysis", 0) < 70):
            enhanced_data["stakeholder_impact_analysis"] = self._enhance_stakeholder_analysis(enhanced_data)
            enhancement_applied = True

        # Add basic milestone structure if missing
        if "milestone_structure" not in enhanced_data:
            enhanced_data["milestone_structure"] = self._generate_basic_milestones(enhanced_data)
            enhancement_applied = True

        return enhanced_data, enhancement_applied

    def _enhance_goal_statement(self, goal_statement: str) -> str:
        """Enhance a goal statement to be more specific and outcome-focused."""
        enhanced = goal_statement

        # Add specificity if too generic
        if len(enhanced) < 50:
            enhanced += " with measurable outcomes and clear success criteria."

        # Ensure outcome-focused language
        outcome_indicators = ["enable", "achieve", "deliver", "create", "build", "establish"]
        has_outcome_focus = any(indicator in enhanced.lower() for indicator in outcome_indicators)

        if not has_outcome_focus:
            enhanced = enhanced.replace(
                "I want to",
                "Enable [user_type] to [specific_action] resulting in [measurable_benefit] to"
            )

        return enhanced

    def _generate_primary_criteria(self, template_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic primary criteria based on template content."""
        criteria = []

        # Extract key elements from goal statement
        goal_statement = template_data.get("goal_statement", "")

        # Generate criteria based on common patterns
        if "reduce" in goal_statement.lower():
            criteria.append({
                "criterion": "Reduction in target metric",
                "target": "20% reduction within 3 months",
                "measurement_method": "Track metric before and after implementation",
                "validation": "Compare baseline measurements with post-implementation data"
            })
        elif "increase" in goal_statement.lower() or "improve" in goal_statement.lower():
            criteria.append({
                "criterion": "Improvement in target metric",
                "target": "30% improvement within 2 months",
                "measurement_method": "Monitor key performance indicators",
                "validation": "Validate improvement through statistical analysis"
            })
        else:
            # Default criteria
            criteria.append({
                "criterion": "Successful goal achievement",
                "target": "100% completion within specified timeframe",
                "measurement_method": "Track milestone completion and final outcomes",
                "validation": "Verify all success criteria are met"
            })

        # Add second criterion for balance
        criteria.append({
            "criterion": "User satisfaction with outcomes",
            "target": "80% satisfaction rate within 1 month",
            "measurement_method": "Collect feedback from affected users",
            "validation": "Survey participants and analyze satisfaction scores"
        })

        return criteria

    def _enhance_stakeholder_analysis(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance or create stakeholder impact analysis."""
        return {
            "primary_users": [
                {
                    "user_type": "End users",
                    "current_pain_point": "Identified problem from goal context",
                    "goal_benefit": "Direct benefit from goal achievement",
                    "success_impact": "Measurable improvement in user experience"
                }
            ],
            "key_stakeholders": [
                {
                    "stakeholder": "Project team",
                    "interest": "Successful delivery of goal outcomes",
                    "influence": "High - directly responsible for implementation",
                    "success_criteria": "Meet all milestones and quality standards"
                }
            ]
        }

    def _generate_basic_milestones(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate basic milestone structure."""
        return {
            "milestones": [
                {
                    "title": "Planning & Setup",
                    "priority": "P1",
                    "focus": "Define detailed requirements and approach",
                    "success_indicators": ["Requirements documented", "Approach approved"],
                    "hypothesis_validation": {
                        "tests": "Validate understanding of requirements",
                        "validation_method": "Review with stakeholders"
                    },
                    "value_delivered": {
                        "user_value": "Clear direction and scope definition",
                        "learning_value": "Requirements validation and approach confirmation"
                    },
                    "effort_estimate": "1-2 weeks",
                    "timeline": "Week 1-2"
                },
                {
                    "title": "Core Implementation",
                    "priority": "P1",
                    "focus": "Build and deliver core functionality",
                    "success_indicators": ["Core features working", "Basic validation passed"],
                    "hypothesis_validation": {
                        "tests": "Core functionality meets requirements",
                        "validation_method": "Testing and stakeholder review"
                    },
                    "value_delivered": {
                        "user_value": "Functional solution addressing key needs",
                        "learning_value": "Implementation effectiveness and user feedback"
                    },
                    "effort_estimate": "3-4 weeks",
                    "timeline": "Week 3-6"
                },
                {
                    "title": "Validation & Launch",
                    "priority": "P1",
                    "focus": "Final validation and deployment",
                    "success_indicators": ["All criteria met", "User acceptance confirmed"],
                    "hypothesis_validation": {
                        "tests": "Solution meets all success criteria",
                        "validation_method": "Comprehensive testing and user validation"
                    },
                    "value_delivered": {
                        "user_value": "Complete solution ready for use",
                        "learning_value": "Success validation and lessons learned"
                    },
                    "effort_estimate": "1-2 weeks",
                    "timeline": "Week 7-8"
                }
            ]
        }

    def _integrate_with_ab_testing(self, user_id: str, template_data: Dict[str, Any],
                                 validation_result: ValidationResult) -> Optional[str]:
        """Integrate template processing with A/B testing framework."""
        if not self.ab_test_manager:
            return None

        try:
            # Record template creation in A/B testing framework
            enhanced_metrics = EnhancedInteractionMetrics(
                timestamp=datetime.now().isoformat(),
                command="template_create",
                user_input_length=len(json.dumps(template_data)),
                response_length=0,
                clarification_needed=False,
                response_quality_score=validation_result.quality_score,
                context_retained=True,
                template_used=True,
                test_group="A",  # Default group
                test_id="template_validation_test",
                variant_name="enhanced_templates",
                user_id=user_id,
                session_id=str(uuid.uuid4()),
                template_validation_score=validation_result.quality_score,
                success_criteria_met=validation_result.is_valid
            )

            # Record the interaction
            self.ab_test_manager.record_interaction(
                user_id=user_id,
                command="template_create",
                user_input=json.dumps(template_data),
                ai_response="Template processed successfully",
                test_id="template_validation_test"
            )

            return "template_validation_test"

        except Exception as e:
            self.logger.error(f"Error integrating with A/B testing: {e}")
            return None

    def _save_processed_template(self, template_id: str, template_data: Dict[str, Any],
                               validation_result: ValidationResult) -> None:
        """Save the processed template with validation results."""
        template_file = self.templates_path / f"template_{template_id}.json"

        # Combine template data with validation results
        template_record = {
            "template_id": template_id,
            "template_data": template_data,
            "validation_result": validation_result.to_dict(),
            "created_at": datetime.now().isoformat(),
            "version": "2.0"
        }

        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(template_record, f, indent=2)

    def _update_processing_stats(self, validation_success: bool, enhancement_applied: bool,
                               ab_test_integration: bool) -> None:
        """Update processing statistics."""
        self.processing_stats["total_processed"] += 1

        if validation_success:
            self.processing_stats["successful_validations"] += 1

        if enhancement_applied:
            self.processing_stats["enhancement_applications"] += 1

        if ab_test_integration:
            self.processing_stats["ab_test_integrations"] += 1

    def get_progressive_disclosure_plan(self, current_template: Dict[str, Any]) -> Dict[str, Any]:
        """Get a progressive disclosure plan based on current template state."""
        current_fields = set(current_template.keys())
        plan = {
            "current_phase": self._determine_current_phase(current_fields),
            "completed_phases": [],
            "next_steps": [],
            "estimated_total_time": "30-45 minutes"
        }

        # Determine completed phases
        for phase_id, phase in self.phases.items():
            phase_fields = set(phase.required_fields + phase.optional_fields)
            if phase_fields.issubset(current_fields):
                plan["completed_phases"].append(phase_id)

        # Determine next steps
        current_phase = plan["current_phase"]
        if current_phase in self.phases:
            phase = self.phases[current_phase]
            missing_required = set(phase.required_fields) - current_fields
            if missing_required:
                plan["next_steps"] = [f"Complete required fields: {', '.join(missing_required)}"]
            else:
                # Move to next phase
                next_phase_id = self._get_next_phase(current_phase)
                if next_phase_id:
                    next_phase = self.phases[next_phase_id]
                    plan["next_steps"] = [f"Move to {next_phase.name}: {next_phase.description}"]
                    plan["current_phase"] = next_phase_id

        return plan

    def _determine_current_phase(self, current_fields: set) -> str:
        """Determine which phase the template is currently in."""
        # Check phases in order
        for phase_id in ["phase_1_basic", "phase_2_intermediate", "phase_3_advanced"]:
            phase = self.phases[phase_id]
            phase_fields = set(phase.required_fields)
            if phase_fields.issubset(current_fields):
                return phase_id

        # Default to first phase if no fields completed
        return "phase_1_basic"

    def _get_next_phase(self, current_phase: str) -> Optional[str]:
        """Get the next phase after the current one."""
        phase_order = ["phase_1_basic", "phase_2_intermediate", "phase_3_advanced"]
        try:
            current_index = phase_order.index(current_phase)
            if current_index < len(phase_order) - 1:
                return phase_order[current_index + 1]
        except ValueError:
            pass
        return None

    def process_template_file(self, template_path: Path, user_id: str = "anonymous",
                            enhancement_mode: Literal["none", "auto", "interactive"] = "auto") -> TemplateProcessingResult:
        """Process a template from a file."""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            return self.process_template(template_data, user_id, True, enhancement_mode)
        except FileNotFoundError:
            return TemplateProcessingResult(
                success=False,
                template_id="",
                validation_result=ValidationResult(
                    is_valid=False,
                    quality_score=0.0,
                    errors=[f"Template file not found: {template_path}"],
                    warnings=[],
                    suggestions=[],
                    completeness_score=0.0,
                    field_scores={},
                    validation_timestamp=datetime.now().isoformat()
                ),
                processing_timestamp=datetime.now().isoformat(),
                error_message=f"Template file not found: {template_path}"
            )
        except json.JSONDecodeError as e:
            return TemplateProcessingResult(
                success=False,
                template_id="",
                validation_result=ValidationResult(
                    is_valid=False,
                    quality_score=0.0,
                    errors=[f"Invalid JSON in template file: {e}"],
                    warnings=[],
                    suggestions=["Fix JSON syntax errors"],
                    completeness_score=0.0,
                    field_scores={},
                    validation_timestamp=datetime.now().isoformat()
                ),
                processing_timestamp=datetime.now().isoformat(),
                error_message=f"Invalid JSON: {e}"
            )

    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics and performance metrics."""
        return {
            "statistics": self.processing_stats,
            "phases": {k: v.__dict__ for k, v in self.phases.items()},
            "schema_version": "2.0",
            "last_updated": datetime.now().isoformat()
        }

    def validate_template_real_time(self, template_data: Dict[str, Any],
                                  field_name: str, field_value: Any) -> Dict[str, Any]:
        """Perform real-time validation as user fills out template fields."""
        # Create a copy of template data with the new field
        temp_template = template_data.copy()
        temp_template[field_name] = field_value

        # Validate the current state
        validation_result = self.schema_validator.validate_template(temp_template)

        # Get progressive disclosure guidance
        current_phase = self._determine_current_phase(set(temp_template.keys()))
        phase_guidance = self.phases.get(current_phase, self.phases["phase_1_basic"])

        return {
            "validation_result": validation_result.to_dict(),
            "current_phase": current_phase,
            "phase_guidance": phase_guidance.__dict__,
            "field_score": validation_result.field_scores.get(field_name, 0.0),
            "completion_percentage": validation_result.completeness_score,
            "next_suggestions": validation_result.suggestions[:3]  # Top 3 suggestions
        }