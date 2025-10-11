#!/usr/bin/env python3
"""
Schema Validator for Enhanced Goal Templates

This module provides JSON schema validation with quality scoring (0-100 points)
for enhanced goal templates based on the enhanced template schema design.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
import logging

@dataclass
class ValidationResult:
    """Result of template validation with quality scoring."""
    is_valid: bool
    quality_score: float  # 0-100 points
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    completeness_score: float  # 0-100 percentage
    field_scores: Dict[str, float]
    validation_timestamp: str

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class QualityMetrics:
    """Quality metrics for template assessment."""
    specificity_score: float  # How specific and detailed the content is
    measurability_score: float  # How measurable the criteria are
    clarity_score: float  # How clear and understandable the content is
    completeness_score: float  # How complete the template is
    structure_score: float  # How well-structured the content is

class SchemaValidator:
    """JSON schema validator with quality scoring for enhanced goal templates."""

    def __init__(self, schema_path: Optional[Path] = None):
        """Initialize the schema validator.

        Args:
            schema_path: Path to the enhanced template schema JSON file
        """
        self.logger = logging.getLogger(__name__)

        if schema_path is None:
            # Default to the enhanced template schema in templates directory
            schema_path = Path(__file__).parent.parent.parent / "templates" / "enhanced-template-schema.json"

        self.schema_path = schema_path
        self.schema = self._load_schema()
        self.field_weights = self._initialize_field_weights()

    def _load_schema(self) -> Dict[str, Any]:
        """Load the enhanced template schema."""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Schema file not found: {self.schema_path}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in schema file: {e}")
            raise

    def _initialize_field_weights(self) -> Dict[str, float]:
        """Initialize weights for different fields in quality scoring."""
        return {
            "goal_statement": 0.15,
            "problem_context": 0.10,
            "success_outcome": 0.10,
            "primary_criteria": 0.20,
            "stakeholder_impact_analysis": 0.15,
            "core_hypotheses": 0.10,
            "milestone_structure": 0.15,
            "validation_framework": 0.05
        }

    def validate_template(self, template_data: Dict[str, Any]) -> ValidationResult:
        """Validate a template against the enhanced schema with quality scoring.

        Args:
            template_data: The template data to validate

        Returns:
            ValidationResult with detailed validation information
        """
        errors = []
        warnings = []
        suggestions = []
        field_scores = {}

        # Basic JSON schema validation
        schema_errors = self._validate_json_schema(template_data)
        errors.extend(schema_errors)

        # Field-level validation and scoring
        for field_name, field_config in self.schema.get("field_definitions", {}).items():
            field_score = self._validate_field(template_data, field_name, field_config)
            field_scores[field_name] = field_score

        # Calculate overall quality metrics
        quality_metrics = self._calculate_quality_metrics(template_data, field_scores)

        # Generate suggestions for improvement
        suggestions = self._generate_improvement_suggestions(template_data, quality_metrics)

        # Calculate completeness score
        completeness_score = self._calculate_completeness_score(template_data, field_scores)

        # Calculate overall quality score (0-100)
        quality_score = self._calculate_overall_quality_score(quality_metrics, completeness_score)

        # Determine if template is valid
        is_valid = len(errors) == 0 and quality_score >= 60  # Minimum 60% for validity

        return ValidationResult(
            is_valid=is_valid,
            quality_score=quality_score,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            completeness_score=completeness_score,
            field_scores=field_scores,
            validation_timestamp=datetime.now().isoformat()
        )

    def _validate_json_schema(self, template_data: Dict[str, Any]) -> List[str]:
        """Basic JSON schema validation."""
        errors = []

        # Check required top-level fields
        required_fields = ["goal_statement", "problem_context", "success_outcome", "primary_criteria"]
        for field in required_fields:
            if field not in template_data or not template_data[field]:
                errors.append(f"Required field '{field}' is missing or empty")

        # Validate field types and formats
        if "goal_statement" in template_data:
            goal_length = len(template_data["goal_statement"])
            if goal_length < 50 or goal_length > 200:
                errors.append("Goal statement must be between 50-200 characters")

        if "primary_criteria" in template_data:
            if not isinstance(template_data["primary_criteria"], list):
                errors.append("Primary criteria must be a list")
            elif len(template_data["primary_criteria"]) < 2:
                errors.append("Must have at least 2 primary criteria")

        return errors

    def _validate_field(self, template_data: Dict[str, Any], field_name: str, field_config: Dict[str, Any]) -> float:
        """Validate a specific field and return its quality score."""
        if field_name not in template_data:
            return 0.0

        field_value = template_data[field_name]
        field_score = 50.0  # Base score

        # Length validation
        if "validation" in field_config:
            validation = field_config["validation"]

            if "min_length" in validation and "max_length" in validation:
                min_len = validation["min_length"]
                max_len = validation["max_length"]

                if isinstance(field_value, str):
                    actual_length = len(field_value)
                    if actual_length < min_len:
                        field_score -= 20
                    elif actual_length > max_len:
                        field_score -= 10
                    else:
                        field_score += 15  # Good length

            # Required elements check
            if "required_elements" in validation:
                for element in validation["required_elements"]:
                    if element.lower() not in field_value.lower():
                        field_score -= 15

        # Content quality checks
        if isinstance(field_value, str):
            # Check for specificity (avoid vague terms)
            vague_terms = ["good", "better", "improve", "enhance", "optimize"]
            if any(term in field_value.lower() for term in vague_terms):
                field_score -= 10

            # Check for measurability indicators
            measurable_terms = ["measure", "track", "count", "percentage", "rate", "score"]
            if any(term in field_value.lower() for term in measurable_terms):
                field_score += 10

        # Structure validation for complex fields
        if field_name == "primary_criteria" and isinstance(field_value, list):
            field_score = self._validate_primary_criteria(field_value)

        elif field_name == "stakeholder_impact_analysis" and isinstance(field_value, dict):
            field_score = self._validate_stakeholder_analysis(field_value)

        return max(0.0, min(100.0, field_score))

    def _validate_primary_criteria(self, criteria: List[Dict[str, Any]]) -> float:
        """Validate primary criteria structure and content."""
        if not criteria:
            return 0.0

        total_score = 0.0
        required_fields = ["criterion", "target", "measurement_method", "validation"]

        for criterion in criteria:
            criterion_score = 100.0

            # Check required fields
            for field in required_fields:
                if field not in criterion or not criterion[field]:
                    criterion_score -= 25

            # Validate target format (should include number and timeframe)
            if "target" in criterion:
                target = criterion["target"]
                if not re.search(r'\d+', target):  # No numbers found
                    criterion_score -= 15
                if not re.search(r'(day|week|month|quarter|year|hour|minute)', target.lower()):
                    criterion_score -= 15

            total_score += criterion_score

        return total_score / len(criteria)

    def _validate_stakeholder_analysis(self, analysis: Dict[str, Any]) -> float:
        """Validate stakeholder impact analysis."""
        score = 80.0  # Base score

        required_sections = ["primary_users", "key_stakeholders"]
        for section in required_sections:
            if section not in analysis or not analysis[section]:
                score -= 20

        # Check stakeholder detail completeness
        if "key_stakeholders" in analysis:
            stakeholders = analysis["key_stakeholders"]
            if isinstance(stakeholders, list):
                for stakeholder in stakeholders:
                    required_fields = ["stakeholder", "interest", "influence", "success_criteria"]
                    for field in required_fields:
                        if field not in stakeholder or not stakeholder[field]:
                            score -= 10

        return max(0.0, score)

    def _calculate_quality_metrics(self, template_data: Dict[str, Any], field_scores: Dict[str, float]) -> QualityMetrics:
        """Calculate comprehensive quality metrics."""
        # Specificity score - based on detail level and concrete language
        specificity_score = self._calculate_specificity_score(template_data)

        # Measurability score - based on quantifiable targets and measurement methods
        measurability_score = self._calculate_measurability_score(template_data)

        # Clarity score - based on clear language and structure
        clarity_score = self._calculate_clarity_score(template_data)

        # Structure score - based on template structure adherence
        structure_score = sum(field_scores.values()) / len(field_scores) if field_scores else 0.0

        # Completeness score - based on field completion
        completeness_score = self._calculate_completeness_score(template_data, field_scores)

        return QualityMetrics(
            specificity_score=specificity_score,
            measurability_score=measurability_score,
            clarity_score=clarity_score,
            completeness_score=completeness_score,
            structure_score=structure_score
        )

    def _calculate_specificity_score(self, template_data: Dict[str, Any]) -> float:
        """Calculate how specific and detailed the template content is."""
        score = 50.0

        # Check for specific details vs generic statements
        generic_terms = ["improve", "enhance", "better", "optimize", "good"]
        specific_terms = ["specific", "detailed", "concrete", "particular", "exact"]

        all_text = json.dumps(template_data).lower()

        # Penalty for generic terms
        for term in generic_terms:
            if term in all_text:
                score -= 5

        # Bonus for specific terms
        for term in specific_terms:
            if term in all_text:
                score += 5

        # Check for numerical targets
        numbers_found = len(re.findall(r'\d+%|\d+\s*(day|week|month|year|hour)', all_text))
        score += min(numbers_found * 5, 20)  # Up to 20 points for numbers

        return max(0.0, min(100.0, score))

    def _calculate_measurability_score(self, template_data: Dict[str, Any]) -> float:
        """Calculate how measurable the template criteria are."""
        score = 50.0

        # Check for measurement methods
        measurement_indicators = ["measure", "track", "count", "percentage", "rate", "metric", "kpi"]
        all_text = json.dumps(template_data).lower()

        for indicator in measurement_indicators:
            if indicator in all_text:
                score += 8

        # Check for timeframes
        timeframes = ["daily", "weekly", "monthly", "quarterly", "annually", "within", "by"]
        for timeframe in timeframes:
            if timeframe in all_text:
                score += 5

        # Check primary criteria structure
        if "primary_criteria" in template_data:
            criteria = template_data["primary_criteria"]
            if isinstance(criteria, list):
                for criterion in criteria:
                    if "measurement_method" in criterion and criterion["measurement_method"]:
                        score += 10

        return max(0.0, min(100.0, score))

    def _calculate_clarity_score(self, template_data: Dict[str, Any]) -> float:
        """Calculate how clear and understandable the template content is."""
        score = 70.0  # Start with decent base score

        # Check for clear, concise language
        all_text = json.dumps(template_data)

        # Bonus for structured content (bullet points, numbered lists)
        if "*" in all_text or "-" in all_text or "1." in all_text:
            score += 10

        # Penalty for overly complex sentences (long sentences)
        sentences = re.split(r'[.!?]+', all_text)
        long_sentences = [s for s in sentences if len(s.split()) > 25]
        if long_sentences:
            score -= min(len(long_sentences) * 2, 15)

        # Bonus for active voice indicators
        active_indicators = ["will", "achieve", "deliver", "create", "build", "implement"]
        for indicator in active_indicators:
            if indicator in all_text.lower():
                score += 3

        return max(0.0, min(100.0, score))

    def _calculate_completeness_score(self, template_data: Dict[str, Any], field_scores: Dict[str, float]) -> float:
        """Calculate template completeness percentage."""
        total_fields = len(self.schema.get("field_definitions", {}))
        completed_fields = sum(1 for field_name in self.schema.get("field_definitions", {})
                             if field_name in template_data and template_data[field_name])

        if total_fields == 0:
            return 100.0

        return (completed_fields / total_fields) * 100.0

    def _calculate_overall_quality_score(self, quality_metrics: QualityMetrics, completeness_score: float) -> float:
        """Calculate overall quality score from all metrics."""
        # Weighted average of quality metrics
        quality_weights = {
            "specificity": 0.25,
            "measurability": 0.30,
            "clarity": 0.20,
            "structure": 0.15,
            "completeness": 0.10
        }

        quality_score = (
            quality_metrics.specificity_score * quality_weights["specificity"] +
            quality_metrics.measurability_score * quality_weights["measurability"] +
            quality_metrics.clarity_score * quality_weights["clarity"] +
            quality_metrics.structure_score * quality_weights["structure"] +
            completeness_score * quality_weights["completeness"]
        )

        return round(quality_score, 1)

    def _generate_improvement_suggestions(self, template_data: Dict[str, Any], quality_metrics: QualityMetrics) -> List[str]:
        """Generate prioritized suggestions for template improvement."""
        suggestions = []

        # Specificity suggestions
        if quality_metrics.specificity_score < 70:
            suggestions.append("Add more specific details and concrete examples to improve clarity")
            suggestions.append("Replace generic terms like 'improve' with specific outcomes")

        # Measurability suggestions
        if quality_metrics.measurability_score < 70:
            suggestions.append("Add quantifiable targets with specific numbers and timeframes")
            suggestions.append("Include clear measurement methods for each success criterion")

        # Clarity suggestions
        if quality_metrics.clarity_score < 70:
            suggestions.append("Use shorter sentences and active voice for better readability")
            suggestions.append("Add bullet points or numbered lists for complex information")

        # Completeness suggestions
        missing_fields = []
        for field_name in self.schema.get("field_definitions", {}):
            if field_name not in template_data or not template_data[field_name]:
                missing_fields.append(field_name)

        if missing_fields:
            suggestions.append(f"Complete missing sections: {', '.join(missing_fields[:3])}")

        # Prioritize suggestions by importance
        priority_order = {
            "Add quantifiable targets": 1,
            "Complete missing sections": 2,
            "Add measurement methods": 3,
            "Improve specificity": 4,
            "Enhance clarity": 5
        }

        # Sort suggestions by priority
        prioritized_suggestions = []
        for suggestion in suggestions:
            priority = 5  # Default priority
            for key, pri in priority_order.items():
                if key.lower() in suggestion.lower():
                    priority = pri
                    break
            prioritized_suggestions.append((priority, suggestion))

        prioritized_suggestions.sort(key=lambda x: x[0])
        return [suggestion for _, suggestion in prioritized_suggestions]

    def validate_template_file(self, template_path: Path) -> ValidationResult:
        """Validate a template file and return validation results.

        Args:
            template_path: Path to the template JSON file

        Returns:
            ValidationResult with validation details
        """
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            return self.validate_template(template_data)
        except FileNotFoundError:
            return ValidationResult(
                is_valid=False,
                quality_score=0.0,
                errors=[f"Template file not found: {template_path}"],
                warnings=[],
                suggestions=["Check that the template file exists"],
                completeness_score=0.0,
                field_scores={},
                validation_timestamp=datetime.now().isoformat()
            )
        except json.JSONDecodeError as e:
            return ValidationResult(
                is_valid=False,
                quality_score=0.0,
                errors=[f"Invalid JSON in template file: {e}"],
                warnings=[],
                suggestions=["Fix JSON syntax errors in the template file"],
                completeness_score=0.0,
                field_scores={},
                validation_timestamp=datetime.now().isoformat()
            )

    def get_validation_summary(self, validation_result: ValidationResult) -> str:
        """Generate a human-readable summary of validation results."""
        summary = f"""
Template Validation Summary
==========================
Quality Score: {validation_result.quality_score:.1f}/100
Completeness: {validation_result.completeness_score:.1f}%
Valid: {'✓' if validation_result.is_valid else '✗'}

"""

        if validation_result.errors:
            summary += "\nErrors:\n"
            for error in validation_result.errors:
                summary += f"  • {error}\n"

        if validation_result.suggestions:
            summary += "\nImprovement Suggestions:\n"
            for i, suggestion in enumerate(validation_result.suggestions[:5], 1):
                summary += f"  {i}. {suggestion}\n"

        summary += f"\nValidated at: {validation_result.validation_timestamp}"

        return summary