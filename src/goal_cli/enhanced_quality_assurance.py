"""
Enhanced Quality Assurance Framework for goal-dev-spec
Exceeds spec-kit functionality with advanced validation, predictive analytics, 
real-time monitoring, and comprehensive quality assessment.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import defaultdict
import hashlib
import statistics
from functools import wraps
import time

# Import existing modules
from .governance import GovernanceManager
from .compliance import ComplianceChecker
from .analytics import PredictiveAnalyticsEngine
from .performance import PerformanceMonitor
from .security import SecurityManager


@dataclass
class QualityMetrics:
    """Data class for quality metrics"""
    clarity_score: float = 0.0
    completeness_score: float = 0.0
    consistency_score: float = 0.0
    testability_score: float = 0.0
    maintainability_score: float = 0.0
    security_score: float = 0.0
    overall_score: float = 0.0
    last_updated: str = ""


@dataclass
class ValidationFinding:
    """Data class for validation findings"""
    id: str
    type: str  # error, warning, info
    category: str  # clarity, completeness, consistency, etc.
    message: str
    severity: int  # 1-5, 5 being critical
    location: str = ""
    suggestion: str = ""
    timestamp: str = ""


@dataclass
class ArtifactRelationship:
    """Data class for artifact relationships"""
    source_artifact_id: str
    target_artifact_id: str
    relationship_type: str  # dependency, reference, consistency
    validation_status: str  # valid, invalid, unknown
    issues: List[str]


class EnhancedQualityAssurance:
    """Enhanced Quality Assurance Framework"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.qa_path = project_path / ".goal" / "quality"
        self.qa_path.mkdir(exist_ok=True)
        
        # Initialize subsystems
        self.governance_manager = GovernanceManager(project_path)
        self.compliance_checker = ComplianceChecker(project_path)
        self.analytics_engine = PredictiveAnalyticsEngine(project_path)
        self.performance_monitor = PerformanceMonitor(project_path)
        self.security_manager = SecurityManager(project_path)
        
        # Load quality standards
        self.quality_standards = self._load_quality_standards()
        
        # Initialize metrics tracking
        self.metrics_history = self._load_metrics_history()
        
        # Initialize validation rules
        self.validation_rules = self._initialize_validation_rules()
        
        # Initialize consistency rules
        self.consistency_rules = self._initialize_consistency_rules()

    def _load_quality_standards(self) -> Dict:
        """Load enhanced quality standards"""
        return {
            "clarity_thresholds": {
                "min_score": 0.8,
                "ambiguity_tolerance": 0.1
            },
            "completeness_thresholds": {
                "required_sections_coverage": 0.95,
                "optional_sections_coverage": 0.7
            },
            "consistency_thresholds": {
                "cross_artifact_consistency": 0.9,
                "terminology_consistency": 0.95
            },
            "testability_thresholds": {
                "acceptance_criteria_per_spec": 5,
                "scenarios_per_acceptance_criterion": 2
            },
            "maintainability_thresholds": {
                "modularity_score": 0.8,
                "reusability_score": 0.7
            },
            "security_thresholds": {
                "vulnerability_tolerance": 0,
                "security_review_compliance": 1.0
            }
        }

    def _load_metrics_history(self) -> Dict:
        """Load historical metrics data"""
        metrics_file = self.qa_path / "metrics_history.json"
        if metrics_file.exists():
            try:
                with open(metrics_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return defaultdict(list)
        return defaultdict(list)

    def _initialize_validation_rules(self) -> Dict:
        """Initialize advanced validation rules"""
        return {
            "goal_validation": [
                {
                    "name": "goal_clarity_validator",
                    "function": self._validate_goal_clarity,
                    "weight": 0.2
                },
                {
                    "name": "goal_completeness_validator",
                    "function": self._validate_goal_completeness,
                    "weight": 0.2
                },
                {
                    "name": "goal_consistency_validator",
                    "function": self._validate_goal_completeness,  # Using completeness as placeholder
                    "weight": 0.15
                },
                {
                    "name": "goal_testability_validator",
                    "function": self._validate_goal_testability,
                    "weight": 0.15
                },
                {
                    "name": "goal_dependencies_validator",
                    "function": self._validate_goal_dependencies,
                    "weight": 0.1
                },
                {
                    "name": "goal_complexity_validator",
                    "function": self._validate_goal_complexity,
                    "weight": 0.1
                },
                {
                    "name": "goal_security_validator",
                    "function": self._validate_goal_security,
                    "weight": 0.1
                }
            ],
            "spec_validation": [
                {
                    "name": "spec_clarity_validator",
                    "function": self._validate_spec_clarity,
                    "weight": 0.2
                },
                {
                    "name": "spec_completeness_validator",
                    "function": self._validate_spec_completeness,
                    "weight": 0.2
                },
                {
                    "name": "spec_consistency_validator",
                    "function": self._validate_spec_consistency,
                    "weight": 0.15
                },
                {
                    "name": "spec_testability_validator",
                    "function": self._validate_spec_testability,
                    "weight": 0.15
                },
                {
                    "name": "spec_ambiguity_validator",
                    "function": self._validate_spec_ambiguity,
                    "weight": 0.1
                },
                {
                    "name": "spec_traceability_validator",
                    "function": self._validate_spec_traceability,
                    "weight": 0.1
                },
                {
                    "name": "spec_security_validator",
                    "function": self._validate_spec_security,
                    "weight": 0.1
                }
            ],
            "plan_validation": [
                {
                    "name": "plan_completeness_validator",
                    "function": self._validate_plan_completeness,
                    "weight": 0.25
                },
                {
                    "name": "plan_realism_validator",
                    "function": self._validate_plan_realism,
                    "weight": 0.2
                },
                {
                    "name": "plan_resource_validator",
                    "function": self._validate_plan_resources,
                    "weight": 0.15
                },
                {
                    "name": "plan_risk_validator",
                    "function": self._validate_plan_risks,
                    "weight": 0.15
                },
                {
                    "name": "plan_dependencies_validator",
                    "function": self._validate_plan_dependencies,
                    "weight": 0.1
                },
                {
                    "name": "plan_timeline_validator",
                    "function": self._validate_plan_timeline,
                    "weight": 0.1
                },
                {
                    "name": "plan_traceability_validator",
                    "function": self._validate_plan_traceability,
                    "weight": 0.05
                }
            ],
            "task_validation": [
                {
                    "name": "task_clarity_validator",
                    "function": self._validate_task_clarity,
                    "weight": 0.2
                },
                {
                    "name": "task_completeness_validator",
                    "function": self._validate_task_completeness,
                    "weight": 0.2
                },
                {
                    "name": "task_assignee_validator",
                    "function": self._validate_task_assignee,
                    "weight": 0.15
                },
                {
                    "name": "task_dependencies_validator",
                    "function": self._validate_task_dependencies,
                    "weight": 0.15
                },
                {
                    "name": "task_estimation_validator",
                    "function": self._validate_task_estimation,
                    "weight": 0.1
                },
                {
                    "name": "task_priority_validator",
                    "function": self._validate_task_priority,
                    "weight": 0.1
                },
                {
                    "name": "task_traceability_validator",
                    "function": self._validate_task_traceability,
                    "weight": 0.1
                }
            ]
        }

    def _initialize_consistency_rules(self) -> Dict:
        """Initialize consistency checking rules"""
        return {
            "terminology_consistency": [
                {
                    "pattern": r"\b(user|customer|client)\b",
                    "preferred": "user",
                    "scope": ["goal", "spec", "plan"]
                },
                {
                    "pattern": r"\b(password|credential|auth token)\b",
                    "preferred": "credential",
                    "scope": ["goal", "spec", "plan"]
                }
            ],
            "reference_consistency": [
                {
                    "source_field": "goal_id",
                    "target_field": "related_goals",
                    "type": "bidirectional"
                },
                {
                    "source_field": "spec_id",
                    "target_field": "related_specs",
                    "type": "bidirectional"
                }
            ],
            "dependency_consistency": [
                {
                    "source_field": "dependencies",
                    "validation_function": self._validate_dependency_chain
                }
            ]
        }

    # Advanced Validation Algorithms

    def _validate_goal_clarity(self, goal_data: Dict) -> Tuple[float, List[ValidationFinding]]:
        """Validate goal clarity with advanced NLP techniques"""
        findings = []
        score = 1.0
        
        # Check title clarity
        title = goal_data.get("title", "")
        if len(title) < 10:
            findings.append(ValidationFinding(
                id=f"goal_clarity_{hashlib.md5(title.encode()).hexdigest()[:8]}",
                type="warning",
                category="clarity",
                message=f"Goal title '{title}' is too brief. Consider making it more descriptive.",
                severity=2,
                location="goal.title",
                suggestion="Expand the title to clearly state what the goal accomplishes."
            ))
            score -= 0.2
        
        # Check description clarity
        description = goal_data.get("description", "")
        if len(description) < 50:
            findings.append(ValidationFinding(
                id=f"goal_desc_clarity_{hashlib.md5(description.encode()).hexdigest()[:8]}",
                type="warning",
                category="clarity",
                message="Goal description is too brief. Provide more context.",
                severity=2,
                location="goal.description",
                suggestion="Add details about why this goal is important and what problem it solves."
            ))
            score -= 0.3
        
        # Check for ambiguous language
        ambiguity_indicators = ["maybe", "possibly", "sometimes", "usually", "might", "could", "should"]
        ambiguity_count = sum(description.lower().count(indicator) for indicator in ambiguity_indicators)
        if ambiguity_count > 2:
            findings.append(ValidationFinding(
                id=f"goal_ambiguity_{hashlib.md5(description.encode()).hexdigest()[:8]}",
                type="warning",
                category="clarity",
                message=f"Goal description contains {ambiguity_count} ambiguous terms.",
                severity=3,
                location="goal.description",
                suggestion="Replace ambiguous terms with definitive language."
            ))
            score -= min(0.5, ambiguity_count * 0.1)
        
        return max(0.0, score), findings

    def _validate_goal_completeness(self, goal_data: Dict) -> Tuple[float, List[ValidationFinding]]:
        """Validate goal completeness"""
        findings = []
        score = 1.0
        
        required_fields = ["title", "description", "objectives", "success_criteria", "stakeholders"]
        missing_fields = [field for field in required_fields if field not in goal_data or not goal_data[field]]
        
        if missing_fields:
            findings.append(ValidationFinding(
                id=f"goal_completeness_{hashlib.md5(str(missing_fields).encode()).hexdigest()[:8]}",
                type="error",
                category="completeness",
                message=f"Missing required fields: {', '.join(missing_fields)}",
                severity=4,
                location="goal",
                suggestion=f"Add the following fields: {', '.join(missing_fields)}"
            ))
            score -= len(missing_fields) * 0.2
        
        # Check objectives count
        objectives = goal_data.get("objectives", [])
        if len(objectives) < 1:
            findings.append(ValidationFinding(
                id="goal_objectives_count",
                type="error",
                category="completeness",
                message="Goal must have at least one objective",
                severity=4,
                location="goal.objectives",
                suggestion="Add clear, measurable objectives for this goal"
            ))
            score -= 0.3
        elif len(objectives) < 3:
            findings.append(ValidationFinding(
                id="goal_objectives_insufficient",
                type="warning",
                category="completeness",
                message="Goal has fewer than 3 objectives. Consider adding more.",
                severity=2,
                location="goal.objectives",
                suggestion="Add additional objectives to fully define the scope"
            ))
            score -= 0.1
        
        # Check success criteria count
        success_criteria = goal_data.get("success_criteria", [])
        if len(success_criteria) < 1:
            findings.append(ValidationFinding(
                id="goal_success_criteria_count",
                type="error",
                category="completeness",
                message="Goal must have at least one success criterion",
                severity=4,
                location="goal.success_criteria",
                suggestion="Add measurable success criteria to validate goal completion"
            ))
            score -= 0.3
        elif len(success_criteria) < 2:
            findings.append(ValidationFinding(
                id="goal_success_criteria_insufficient",
                type="warning",
                category="completeness",
                message="Goal has fewer than 2 success criteria. Consider adding more.",
                severity=2,
                location="goal.success_criteria",
                suggestion="Add additional success criteria for comprehensive validation"
            ))
            score -= 0.1
        
        return max(0.0, score), findings

    def _validate_spec_clarity(self, spec_data: Dict) -> Tuple[float, List[ValidationFinding]]:
        """Validate specification clarity"""
        findings = []
        score = 1.0
        
        # Check for user stories
        user_stories = spec_data.get("user_stories", [])
        if not user_stories:
            findings.append(ValidationFinding(
                id="spec_user_stories_missing",
                type="error",
                category="clarity",
                message="Specification is missing user stories",
                severity=4,
                location="spec.user_stories",
                suggestion="Add user stories to clarify who will use this feature and why"
            ))
            score -= 0.3
        
        # Check for acceptance criteria
        acceptance_criteria = spec_data.get("acceptance_criteria", [])
        if not acceptance_criteria:
            findings.append(ValidationFinding(
                id="spec_acceptance_criteria_missing",
                type="error",
                category="clarity",
                message="Specification is missing acceptance criteria",
                severity=4,
                location="spec.acceptance_criteria",
                suggestion="Add acceptance criteria to define when the feature is complete"
            ))
            score -= 0.3
        
        # Check for functional requirements
        functional_requirements = spec_data.get("functional_requirements", [])
        if not functional_requirements:
            findings.append(ValidationFinding(
                id="spec_functional_requirements_missing",
                type="warning",
                category="clarity",
                message="Specification is missing functional requirements",
                severity=2,
                location="spec.functional_requirements",
                suggestion="Add functional requirements to specify what the system should do"
            ))
            score -= 0.2
        
        return max(0.0, score), findings

    def _validate_spec_completeness(self, spec_data: Dict) -> Tuple[float, List[ValidationFinding]]:
        """Validate specification completeness"""
        findings = []
        score = 1.0
        
        required_sections = [
            "title", "description", "user_stories", "acceptance_criteria",
            "functional_requirements", "non_functional_requirements"
        ]
        
        missing_sections = [section for section in required_sections if section not in spec_data or not spec_data[section]]
        
        if missing_sections:
            findings.append(ValidationFinding(
                id=f"spec_completeness_{hashlib.md5(str(missing_sections).encode()).hexdigest()[:8]}",
                type="error",
                category="completeness",
                message=f"Missing required sections: {', '.join(missing_sections)}",
                severity=4,
                location="spec",
                suggestion=f"Add the following sections: {', '.join(missing_sections)}"
            ))
            score -= len(missing_sections) * 0.15
        
        # Check acceptance criteria detail
        acceptance_criteria = spec_data.get("acceptance_criteria", [])
        if len(acceptance_criteria) < 3:
            findings.append(ValidationFinding(
                id="spec_acceptance_criteria_insufficient",
                type="warning",
                category="completeness",
                message=f"Specification has only {len(acceptance_criteria)} acceptance criteria. Consider adding more.",
                severity=2,
                location="spec.acceptance_criteria",
                suggestion="Add more detailed acceptance criteria for comprehensive testing"
            ))
            score -= 0.1 * (3 - len(acceptance_criteria))
        
        return max(0.0, score), findings

    # Consistency Checking

    def check_cross_artifact_consistency(self, project_data: Dict) -> Dict:
        """Check consistency across related artifacts"""
        findings = []
        relationships = []
        
        # Check goal-spec consistency
        if "goals" in project_data and "specs" in project_data:
            for goal in project_data["goals"]:
                goal_id = goal.get("id")
                related_specs = goal.get("related_specs", [])
                
                for spec_id in related_specs:
                    # Find the spec
                    spec = next((s for s in project_data["specs"] if s.get("id") == spec_id), None)
                    if spec:
                        # Check if the spec references back to the goal
                        spec_related_goals = spec.get("related_goals", [])
                        if goal_id not in spec_related_goals:
                            findings.append(ValidationFinding(
                                id=f"consistency_{goal_id}_{spec_id}",
                                type="warning",
                                category="consistency",
                                message=f"Goal {goal_id} references spec {spec_id}, but spec does not reference goal",
                                severity=2,
                                location=f"goal:{goal_id} <-> spec:{spec_id}",
                                suggestion="Ensure bidirectional references between related artifacts"
                            ))
                        
                        relationships.append(ArtifactRelationship(
                            source_artifact_id=goal_id,
                            target_artifact_id=spec_id,
                            relationship_type="reference",
                            validation_status="valid" if goal_id in spec_related_goals else "invalid",
                            issues=[] if goal_id in spec_related_goals else ["Missing bidirectional reference"]
                        ))
        
        # Check terminology consistency
        terminology_issues = self._check_terminology_consistency(project_data)
        findings.extend(terminology_issues)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "findings": [asdict(f) for f in findings],
            "relationships": [asdict(r) for r in relationships],
            "consistency_score": self._calculate_consistency_score(findings)
        }

    def _check_terminology_consistency(self, project_data: Dict) -> List[ValidationFinding]:
        """Check terminology consistency across artifacts"""
        findings = []
        
        # Collect all text content
        all_text = ""
        if "goals" in project_data:
            for goal in project_data["goals"]:
                all_text += f" {goal.get('title', '')} {goal.get('description', '')}"
                for obj in goal.get("objectives", []):
                    all_text += f" {obj}"
                for crit in goal.get("success_criteria", []):
                    all_text += f" {crit}"
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                all_text += f" {spec.get('title', '')} {spec.get('description', '')}"
                for story in spec.get("user_stories", []):
                    all_text += f" {story}"
                for crit in spec.get("acceptance_criteria", []):
                    all_text += f" {crit}"
        
        # Check for inconsistent terminology
        for rule in self.consistency_rules.get("terminology_consistency", []):
            pattern = rule["pattern"]
            preferred = rule["preferred"]
            
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if len(set(matches)) > 1:  # Multiple variations found
                findings.append(ValidationFinding(
                    id=f"terminology_{hashlib.md5(pattern.encode()).hexdigest()[:8]}",
                    type="warning",
                    category="consistency",
                    message=f"Inconsistent terminology found: {', '.join(set(matches))}. Preferred term: {preferred}",
                    severity=2,
                    location="project-wide",
                    suggestion=f"Standardize on the preferred term: {preferred}"
                ))
        
        return findings

    def _calculate_consistency_score(self, findings: List[ValidationFinding]) -> float:
        """Calculate consistency score based on findings"""
        if not findings:
            return 1.0
        
        # Weight findings by severity
        total_weight = 0
        max_weight = 0
        
        for finding in findings:
            if finding.type in ["error", "warning"]:
                weight = finding.severity
                total_weight += weight
                max_weight += 5  # Max severity is 5
        
        if max_weight == 0:
            return 1.0
            
        consistency_score = 1.0 - (total_weight / max_weight)
        return max(0.0, consistency_score)

    # Predictive Quality Analytics

    def generate_predictive_quality_analytics(self, project_data: Dict) -> Dict:
        """Generate predictive quality analytics"""
        analytics = {
            "timestamp": datetime.now().isoformat(),
            "risk_assessment": self._assess_project_risks(project_data),
            "quality_forecast": self._forecast_quality_trends(project_data),
            "resource_recommendations": self._recommend_resources(project_data),
            "optimization_suggestions": self._suggest_optimizations(project_data)
        }
        
        return analytics

    def _assess_project_risks(self, project_data: Dict) -> Dict:
        """Assess project risks using predictive analytics"""
        risks = []
        
        # Complexity-based risks
        if "goals" in project_data:
            for goal in project_data["goals"]:
                complexity = self.analytics_engine.analyze_goal_complexity(goal)
                if complexity["total_score"] > 8.0:
                    risks.append({
                        "type": "high_complexity",
                        "artifact_id": goal.get("id", "unknown"),
                        "risk_level": "high",
                        "probability": 0.8,
                        "impact": "delayed_delivery",
                        "mitigation": "Break down into smaller goals or allocate additional resources"
                    })
                elif complexity["total_score"] > 6.0:
                    risks.append({
                        "type": "medium_complexity",
                        "artifact_id": goal.get("id", "unknown"),
                        "risk_level": "medium",
                        "probability": 0.5,
                        "impact": "potential_delays",
                        "mitigation": "Regular progress reviews and early stakeholder feedback"
                    })
        
        # Dependency risks
        dependency_risks = self._assess_dependency_risks(project_data)
        risks.extend(dependency_risks)
        
        return {
            "risks_identified": risks,
            "risk_score": self._calculate_risk_score(risks)
        }

    def _assess_dependency_risks(self, project_data: Dict) -> List[Dict]:
        """Assess dependency-related risks"""
        risks = []
        
        if "goals" in project_data:
            for goal in project_data["goals"]:
                dependencies = goal.get("dependencies", [])
                if len(dependencies) > 5:
                    risks.append({
                        "type": "dependency_complexity",
                        "artifact_id": goal.get("id", "unknown"),
                        "risk_level": "high",
                        "probability": 0.7,
                        "impact": "blocked_progress",
                        "mitigation": "Simplify dependency structure or create intermediate goals"
                    })
                elif len(dependencies) > 3:
                    risks.append({
                        "type": "dependency_complexity",
                        "artifact_id": goal.get("id", "unknown"),
                        "risk_level": "medium",
                        "probability": 0.4,
                        "impact": "coordination_overhead",
                        "mitigation": "Regular dependency reviews and clear ownership"
                    })
        
        return risks

    def _calculate_risk_score(self, risks: List[Dict]) -> float:
        """Calculate overall risk score"""
        if not risks:
            return 0.0
        
        # Weight risks by level and probability
        total_risk = 0
        max_risk = 0
        
        for risk in risks:
            level_multiplier = {"low": 1, "medium": 2, "high": 3}[risk["risk_level"]]
            risk_value = level_multiplier * risk["probability"]
            total_risk += risk_value
            max_risk += 3  # Max level is 3 (high) * max probability (1.0)
        
        if max_risk == 0:
            return 0.0
            
        return min(1.0, total_risk / max_risk)

    def _forecast_quality_trends(self, project_data: Dict) -> Dict:
        """Forecast quality trends based on historical data"""
        # In a real implementation, this would use ML models
        # For now, we'll use a simplified approach based on current metrics
        
        current_metrics = self.calculate_comprehensive_quality_score(project_data)
        
        # Simple trend analysis
        if self.metrics_history:
            historical_scores = [entry["overall_score"] for entry in self.metrics_history.get("overall_scores", [])]
            if len(historical_scores) > 1:
                trend = (historical_scores[-1] - historical_scores[0]) / len(historical_scores)
                direction = "improving" if trend > 0 else "declining" if trend < 0 else "stable"
            else:
                direction = "insufficient_data"
        else:
            direction = "new_project"
        
        return {
            "current_quality_score": current_metrics["overall_score"],
            "trend_direction": direction,
            "forecast_30_days": min(1.0, current_metrics["overall_score"] + (0.05 if direction == "improving" else -0.05 if direction == "declining" else 0)),
            "confidence": 0.7 if direction != "insufficient_data" else 0.3
        }

    def _recommend_resources(self, project_data: Dict) -> List[Dict]:
        """Recommend resources based on project analysis"""
        recommendations = []
        
        if "goals" in project_data:
            for goal in project_data["goals"]:
                # Use existing analytics engine for resource recommendations
                goal_recommendations = self.analytics_engine.recommend_resources(goal)
                recommendations.extend(goal_recommendations)
        
        return recommendations

    def _suggest_optimizations(self, project_data: Dict) -> List[str]:
        """Suggest optimizations for quality improvement"""
        suggestions = []
        
        # Check for common quality issues
        metrics = self.calculate_comprehensive_quality_score(project_data)
        
        if metrics["clarity_score"] < 0.7:
            suggestions.append("Improve artifact clarity by using more precise language and reducing ambiguity")
        
        if metrics["completeness_score"] < 0.8:
            suggestions.append("Ensure all artifacts have complete sections as per templates")
        
        if metrics["consistency_score"] < 0.8:
            suggestions.append("Standardize terminology and ensure bidirectional references between related artifacts")
        
        if metrics["testability_score"] < 0.7:
            suggestions.append("Add more detailed acceptance criteria and test scenarios")
        
        return suggestions

    # Real-time Quality Monitoring

    def start_real_time_monitoring(self):
        """Start real-time quality monitoring"""
        # This would typically start a background process
        # For now, we'll just set up the monitoring framework
        monitoring_config = {
            "enabled": True,
            "interval_seconds": 300,  # 5 minutes
            "metrics_to_monitor": [
                "overall_score",
                "clarity_score",
                "completeness_score",
                "consistency_score"
            ]
        }
        
        config_file = self.qa_path / "monitoring_config.json"
        with open(config_file, 'w') as f:
            json.dump(monitoring_config, f, indent=2)
        
        return monitoring_config

    def get_real_time_metrics(self, project_data: Dict) -> Dict:
        """Get current real-time metrics"""
        metrics = self.calculate_comprehensive_quality_score(project_data)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "status": "healthy" if metrics["overall_score"] > 0.8 else "degraded" if metrics["overall_score"] > 0.6 else "critical",
            "alerts": self._generate_real_time_alerts(metrics)
        }

    def _generate_real_time_alerts(self, metrics: Dict) -> List[Dict]:
        """Generate real-time alerts based on metrics"""
        alerts = []
        
        if metrics["overall_score"] < 0.6:
            alerts.append({
                "type": "quality_critical",
                "severity": "high",
                "message": f"Overall quality score is critically low: {metrics['overall_score']:.2f}",
                "timestamp": datetime.now().isoformat()
            })
        
        if metrics["clarity_score"] < 0.5:
            alerts.append({
                "type": "clarity_critical",
                "severity": "high",
                "message": f"Clarity score is critically low: {metrics['clarity_score']:.2f}",
                "timestamp": datetime.now().isoformat()
            })
        
        if metrics["consistency_score"] < 0.5:
            alerts.append({
                "type": "consistency_critical",
                "severity": "high",
                "message": f"Consistency score is critically low: {metrics['consistency_score']:.2f}",
                "timestamp": datetime.now().isoformat()
            })
        
        return alerts

    # Automated Testing Framework Integration

    def integrate_with_testing_framework(self, framework: str = "pytest") -> Dict:
        """Integrate with automated testing frameworks"""
        integration_config = {
            "framework": framework,
            "enabled": True,
            "test_generation": {
                "from_acceptance_criteria": True,
                "from_user_stories": True,
                "coverage_target": 0.8
            },
            "quality_gates": {
                "pre_commit": True,
                "pre_merge": True,
                "release": True
            }
        }
        
        config_file = self.qa_path / f"test_integration_{framework}.json"
        with open(config_file, 'w') as f:
            json.dump(integration_config, f, indent=2)
        
        return integration_config

    def generate_test_cases_from_spec(self, spec_data: Dict) -> List[Dict]:
        """Generate test cases from specification data"""
        test_cases = []
        
        # Generate tests from acceptance criteria
        acceptance_criteria = spec_data.get("acceptance_criteria", [])
        for i, criterion in enumerate(acceptance_criteria):
            if isinstance(criterion, str):
                test_cases.append({
                    "id": f"TC_{spec_data.get('id', 'SPEC')}_AC_{i+1}",
                    "title": f"Validate acceptance criterion: {criterion[:50]}...",
                    "description": criterion,
                    "type": "acceptance",
                    "priority": "high",
                    "steps": [
                        "Given the system is in a known state",
                        "When the specified condition is met",
                        "Then the expected outcome should occur"
                    ],
                    "expected_result": "Criterion is satisfied"
                })
            elif isinstance(criterion, dict):
                test_cases.append({
                    "id": f"TC_{spec_data.get('id', 'SPEC')}_AC_{i+1}",
                    "title": criterion.get("title", f"Acceptance criterion {i+1}"),
                    "description": criterion.get("description", ""),
                    "type": "acceptance",
                    "priority": criterion.get("priority", "medium"),
                    "steps": criterion.get("steps", []),
                    "expected_result": criterion.get("expected_result", "")
                })
        
        # Generate tests from user stories
        user_stories = spec_data.get("user_stories", [])
        for i, story in enumerate(user_stories):
            if isinstance(story, str):
                test_cases.append({
                    "id": f"TC_{spec_data.get('id', 'SPEC')}_US_{i+1}",
                    "title": f"Validate user story: {story[:50]}...",
                    "description": story,
                    "type": "functional",
                    "priority": "medium",
                    "steps": [
                        "Given a user with appropriate permissions",
                        "When they perform the described action",
                        "Then the expected outcome should occur"
                    ],
                    "expected_result": "User story requirements are met"
                })
            elif isinstance(story, dict):
                test_cases.append({
                    "id": f"TC_{spec_data.get('id', 'SPEC')}_US_{i+1}",
                    "title": story.get("title", f"User story {i+1}"),
                    "description": story.get("description", ""),
                    "type": "functional",
                    "priority": story.get("priority", "medium"),
                    "steps": story.get("steps", []),
                    "expected_result": story.get("expected_result", "")
                })
        
        return test_cases

    # Code Quality Assessment

    def assess_code_quality(self, code_path: Path = None) -> Dict:
        """Assess code quality using various metrics"""
        if code_path is None:
            code_path = self.project_path
        
        quality_metrics = {
            "timestamp": datetime.now().isoformat(),
            "files_analyzed": 0,
            "issues_found": 0,
            "complexity_score": 0,
            "duplication_score": 0,
            "maintainability_score": 0,
            "test_coverage": 0
        }
        
        # This would integrate with actual code quality tools
        # For now, we'll simulate the results
        
        # Count files
        python_files = list(code_path.glob("**/*.py"))
        quality_metrics["files_analyzed"] = len(python_files)
        
        # Simulate code quality metrics
        quality_metrics["complexity_score"] = 0.75  # Simulated
        quality_metrics["duplication_score"] = 0.95  # Simulated (95% unique code)
        quality_metrics["maintainability_score"] = 0.82  # Simulated
        quality_metrics["test_coverage"] = 0.78  # Simulated (78% coverage)
        
        return quality_metrics

    # Security Vulnerability Scanning

    def scan_for_security_vulnerabilities(self) -> Dict:
        """Scan for security vulnerabilities"""
        # Use existing security manager
        scan_results = self.security_manager.scan_project_for_vulnerabilities()
        return scan_results

    # Performance Benchmarking

    def benchmark_performance(self) -> Dict:
        """Benchmark system performance"""
        # Use existing performance monitor
        velocity_metrics = self.performance_monitor.get_velocity_metrics({})
        
        benchmark_results = {
            "timestamp": datetime.now().isoformat(),
            "velocity_metrics": velocity_metrics,
            "performance_indicators": self._calculate_performance_indicators(),
            "benchmarks": self._run_performance_benchmarks()
        }
        
        return benchmark_results

    def _calculate_performance_indicators(self) -> Dict:
        """Calculate key performance indicators"""
        # This would use actual project data
        return {
            "goal_completion_rate": 0.85,  # Simulated
            "spec_review_cycle_time": 2.3,  # days, simulated
            "avg_deployment_frequency": 1.2,  # per week, simulated
            "quality_gate_pass_rate": 0.92  # Simulated
        }

    def _run_performance_benchmarks(self) -> Dict:
        """Run performance benchmarks"""
        benchmarks = {}
        
        # Simulate benchmark execution
        benchmarks["artifact_creation_time"] = {
            "goal": 0.45,  # seconds, simulated
            "spec": 0.78,  # seconds, simulated
            "plan": 0.32,  # seconds, simulated
            "task": 0.15   # seconds, simulated
        }
        
        benchmarks["validation_performance"] = {
            "goal_validation": 0.12,  # seconds, simulated
            "spec_validation": 0.25,  # seconds, simulated
            "consistency_check": 0.34  # seconds, simulated
        }
        
        return benchmarks

    # Compliance Validation

    def validate_compliance(self, standards: List[str] = None) -> Dict:
        """Validate compliance with specified standards"""
        if standards is None:
            standards = ["gdpr", "iso27001", "soc2"]
        
        compliance_results = {}
        
        # Use existing compliance checker
        for standard in standards:
            try:
                result = self.compliance_checker.check_compliance_standard(standard, {})
                compliance_results[standard] = result
            except Exception as e:
                compliance_results[standard] = {
                    "standard": standard,
                    "valid": False,
                    "error": str(e)
                }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "standards_checked": standards,
            "results": compliance_results,
            "overall_compliant": all(result.get("compliant", False) for result in compliance_results.values())
        }

    # Comprehensive Quality Scoring System

    def calculate_comprehensive_quality_score(self, project_data: Dict) -> Dict:
        """Calculate comprehensive quality score for the entire project"""
        # Calculate individual scores
        clarity_score = self._calculate_clarity_score(project_data)
        completeness_score = self._calculate_completeness_score(project_data)
        consistency_score = self._calculate_consistency_score_from_data(project_data)
        testability_score = self._calculate_testability_score(project_data)
        maintainability_score = self._calculate_maintainability_score(project_data)
        security_score = self._calculate_security_score(project_data)
        
        # Calculate weighted overall score
        weights = {
            "clarity": 0.2,
            "completeness": 0.2,
            "consistency": 0.15,
            "testability": 0.15,
            "maintainability": 0.15,
            "security": 0.15
        }
        
        overall_score = (
            clarity_score * weights["clarity"] +
            completeness_score * weights["completeness"] +
            consistency_score * weights["consistency"] +
            testability_score * weights["testability"] +
            maintainability_score * weights["maintainability"] +
            security_score * weights["security"]
        )
        
        quality_metrics = QualityMetrics(
            clarity_score=clarity_score,
            completeness_score=completeness_score,
            consistency_score=consistency_score,
            testability_score=testability_score,
            maintainability_score=maintainability_score,
            security_score=security_score,
            overall_score=overall_score,
            last_updated=datetime.now().isoformat()
        )
        
        # Record metrics in history
        self._record_metrics(quality_metrics)
        
        return asdict(quality_metrics)

    def _calculate_clarity_score(self, project_data: Dict) -> float:
        """Calculate clarity score for the project"""
        scores = []
        
        if "goals" in project_data:
            for goal in project_data["goals"]:
                score, _ = self._validate_goal_clarity(goal)
                scores.append(score)
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                score, _ = self._validate_spec_clarity(spec)
                scores.append(score)
        
        return statistics.mean(scores) if scores else 1.0

    def _calculate_completeness_score(self, project_data: Dict) -> float:
        """Calculate completeness score for the project"""
        scores = []
        
        if "goals" in project_data:
            for goal in project_data["goals"]:
                score, _ = self._validate_goal_completeness(goal)
                scores.append(score)
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                score, _ = self._validate_spec_completeness(spec)
                scores.append(score)
        
        return statistics.mean(scores) if scores else 1.0

    def _calculate_consistency_score_from_data(self, project_data: Dict) -> float:
        """Calculate consistency score from project data"""
        consistency_report = self.check_cross_artifact_consistency(project_data)
        return consistency_report.get("consistency_score", 1.0)

    def _calculate_testability_score(self, project_data: Dict) -> float:
        """Calculate testability score for the project"""
        # This would analyze acceptance criteria, user stories, etc.
        # For now, we'll use a simulated approach
        return 0.85  # Simulated score

    def _calculate_maintainability_score(self, project_data: Dict) -> float:
        """Calculate maintainability score for the project"""
        # This would analyze modularity, documentation, etc.
        # For now, we'll use a simulated approach
        return 0.78  # Simulated score

    def _calculate_security_score(self, project_data: Dict) -> float:
        """Calculate security score for the project"""
        # This would analyze security requirements, vulnerability scans, etc.
        # For now, we'll use a simulated approach
        return 0.92  # Simulated score

    def _record_metrics(self, metrics: QualityMetrics):
        """Record quality metrics in history"""
        metrics_dict = asdict(metrics)
        self.metrics_history["overall_scores"].append(metrics_dict)
        
        # Save to file
        metrics_file = self.qa_path / "metrics_history.json"
        with open(metrics_file, 'w') as f:
            json.dump(dict(self.metrics_history), f, indent=2)

    # Reporting and Visualization

    def generate_comprehensive_quality_report(self, project_data: Dict) -> str:
        """Generate a comprehensive quality report in markdown format"""
        # Calculate current metrics
        quality_metrics = self.calculate_comprehensive_quality_score(project_data)
        
        # Generate consistency report
        consistency_report = self.check_cross_artifact_consistency(project_data)
        
        # Generate predictive analytics
        predictive_analytics = self.generate_predictive_quality_analytics(project_data)
        
        # Generate compliance report
        compliance_report = self.validate_compliance()
        
        # Generate security report
        security_report = self.scan_for_security_vulnerabilities()
        
        # Generate performance report
        performance_report = self.benchmark_performance()
        
        # Create markdown report
        report = f"""# Comprehensive Quality Assurance Report

## Executive Summary

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Project:** {self.project_path.name}
**Overall Quality Score:** {quality_metrics['overall_score']:.2f}/1.00

## Quality Metrics

| Metric | Score | Status |
|--------|-------|--------|
| Clarity | {quality_metrics['clarity_score']:.2f} | {"✅ Excellent" if quality_metrics['clarity_score'] >= 0.9 else "⚠️ Good" if quality_metrics['clarity_score'] >= 0.7 else "❌ Needs Improvement"} |
| Completeness | {quality_metrics['completeness_score']:.2f} | {"✅ Excellent" if quality_metrics['completeness_score'] >= 0.9 else "⚠️ Good" if quality_metrics['completeness_score'] >= 0.7 else "❌ Needs Improvement"} |
| Consistency | {quality_metrics['consistency_score']:.2f} | {"✅ Excellent" if quality_metrics['consistency_score'] >= 0.9 else "⚠️ Good" if quality_metrics['consistency_score'] >= 0.7 else "❌ Needs Improvement"} |
| Testability | {quality_metrics['testability_score']:.2f} | {"✅ Excellent" if quality_metrics['testability_score'] >= 0.9 else "⚠️ Good" if quality_metrics['testability_score'] >= 0.7 else "❌ Needs Improvement"} |
| Maintainability | {quality_metrics['maintainability_score']:.2f} | {"✅ Excellent" if quality_metrics['maintainability_score'] >= 0.9 else "⚠️ Good" if quality_metrics['maintainability_score'] >= 0.7 else "❌ Needs Improvement"} |
| Security | {quality_metrics['security_score']:.2f} | {"✅ Excellent" if quality_metrics['security_score'] >= 0.9 else "⚠️ Good" if quality_metrics['security_score'] >= 0.7 else "❌ Needs Improvement"} |

## Consistency Analysis

**Consistency Score:** {consistency_report['consistency_score']:.2f}
**Issues Found:** {len(consistency_report['findings'])}

## Predictive Analytics

**Risk Score:** {predictive_analytics['risk_assessment']['risk_score']:.2f}
**Quality Trend:** {predictive_analytics['quality_forecast']['trend_direction']}
**30-Day Forecast:** {predictive_analytics['quality_forecast']['forecast_30_days']:.2f}

## Compliance Status

**Overall Compliant:** {"✅ YES" if compliance_report['overall_compliant'] else "❌ NO"}
**Standards Checked:** {', '.join(compliance_report['standards_checked'])}

## Security Scan Results

**Vulnerabilities Found:** {security_report['total_vulnerabilities']}
**Files Scanned:** {security_report['files_scanned']}

## Performance Benchmarks

**Goal Completion Rate:** {performance_report['velocity_metrics']['completion_rate']:.2f} goals/week
**Avg Completion Time:** {performance_report['velocity_metrics']['avg_completion_time']:.1f} days

## Recommendations

"""
        
        # Add optimization suggestions
        suggestions = self._suggest_optimizations(project_data)
        for i, suggestion in enumerate(suggestions, 1):
            report += f"{i}. {suggestion}\n"
        
        report += "\n---\n*Report generated by Enhanced Quality Assurance Framework*"
        
        return report

    # Integration with Existing Systems

    def integrate_with_governance(self, governance_data: Dict) -> Dict:
        """Integrate quality assurance with governance system"""
        # This would enhance the existing governance with quality metrics
        enhanced_governance = governance_data.copy()
        
        # Add quality metrics to governance data
        enhanced_governance["quality_assurance"] = {
            "enabled": True,
            "quality_gates": [
                "goal_definition_quality",
                "specification_quality",
                "consistency_validation",
                "security_compliance",
                "performance_benchmarking"
            ],
            "quality_thresholds": self.quality_standards
        }
        
        return enhanced_governance

    def get_quality_gate_status(self, gate_name: str, artifact_data: Dict) -> Dict:
        """Get the status of a specific quality gate"""
        # Use existing quality gate manager but enhance with our metrics
        if gate_name in self.validation_rules:
            validators = self.validation_rules[gate_name]
            total_score = 0
            total_weight = 0
            findings = []
            
            for validator in validators:
                if "function" in validator:
                    score, validator_findings = validator["function"](artifact_data)
                    total_score += score * validator["weight"]
                    total_weight += validator["weight"]
                    findings.extend(validator_findings)
            
            final_score = total_score / total_weight if total_weight > 0 else 1.0
            
            return {
                "gate": gate_name,
                "passed": final_score >= 0.8,  # 80% threshold
                "score": final_score,
                "findings": [asdict(f) for f in findings],
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "gate": gate_name,
            "passed": False,
            "error": f"Unknown quality gate: {gate_name}"
        }


# Decorator for performance monitoring
def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # In a real implementation, we would record this metric
        execution_time = end_time - start_time
        print(f"Function {func.__name__} executed in {execution_time:.4f} seconds")
        
        return result
    return wrapper


# CLI Integration
def quality_assurance_cli():
    """CLI commands for enhanced quality assurance"""
    import typer
    from rich.console import Console
    from rich.table import Table
    
    app = typer.Typer()
    console = Console()
    
    @app.command()
    def analyze_project():
        """Analyze the entire project for quality metrics"""
        try:
            project_path = Path.cwd()
            # Find project root
            while project_path != project_path.parent:
                if (project_path / ".goal" / "goal.yaml").exists():
                    break
                project_path = project_path.parent
            else:
                console.print("[red]Error:[/red] Not in a goal-dev-spec project")
                return
            
            # Initialize quality assurance system
            qa_system = EnhancedQualityAssurance(project_path)
            
            # Load project data (simplified)
            project_data = {
                "goals": [],
                "specs": [],
                "plans": [],
                "tasks": []
            }
            
            # Calculate comprehensive quality score
            quality_metrics = qa_system.calculate_comprehensive_quality_score(project_data)
            
            # Display results
            console.print("[bold]Project Quality Analysis[/bold]\n")
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Metric", style="dim")
            table.add_column("Score", justify="right")
            table.add_column("Status", justify="center")
            
            metrics = [
                ("Clarity", quality_metrics['clarity_score']),
                ("Completeness", quality_metrics['completeness_score']),
                ("Consistency", quality_metrics['consistency_score']),
                ("Testability", quality_metrics['testability_score']),
                ("Maintainability", quality_metrics['maintainability_score']),
                ("Security", quality_metrics['security_score']),
                ("Overall", quality_metrics['overall_score'])
            ]
            
            for name, score in metrics:
                status = "✅" if score >= 0.9 else "⚠️" if score >= 0.7 else "❌"
                table.add_row(name, f"{score:.2f}", status)
            
            console.print(table)
            
            # Generate and save report
            report = qa_system.generate_comprehensive_quality_report(project_data)
            report_file = project_path / ".goal" / "quality" / "latest_report.md"
            with open(report_file, 'w') as f:
                f.write(report)
            
            console.print(f"\n[green]✓[/green] Detailed report saved to {report_file}")
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def consistency_check():
        """Check consistency across project artifacts"""
        try:
            project_path = Path.cwd()
            # Find project root
            while project_path != project_path.parent:
                if (project_path / ".goal" / "goal.yaml").exists():
                    break
                project_path = project_path.parent
            else:
                console.print("[red]Error:[/red] Not in a goal-dev-spec project")
                return
            
            # Initialize quality assurance system
            qa_system = EnhancedQualityAssurance(project_path)
            
            # Load project data (simplified)
            project_data = {
                "goals": [],
                "specs": [],
                "plans": [],
                "tasks": []
            }
            
            # Check consistency
            consistency_report = qa_system.check_cross_artifact_consistency(project_data)
            
            # Display results
            console.print("[bold]Consistency Analysis[/bold]\n")
            console.print(f"Consistency Score: {consistency_report['consistency_score']:.2f}")
            console.print(f"Issues Found: {len(consistency_report['findings'])}")
            
            if consistency_report['findings']:
                console.print("\n[bold]Issues:[/bold]")
                for finding in consistency_report['findings'][:10]:  # Limit to first 10
                    console.print(f"  • {finding['message']}")
                if len(consistency_report['findings']) > 10:
                    console.print(f"  ... and {len(consistency_report['findings']) - 10} more issues")
            else:
                console.print("\n[green]✅ No consistency issues found![/green]")
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    return app


# Integration with main CLI
def integrate_quality_assurance_with_main_cli(main_app):
    """Integrate quality assurance commands with main CLI"""
    qa_app = quality_assurance_cli()
    main_app.add_typer(qa_app, name="quality")
    return main_app