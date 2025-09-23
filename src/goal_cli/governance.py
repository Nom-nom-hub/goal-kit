"""
Governance module for the goal-dev-spec system.
Provides automated compliance checking, quality gates, and governance enforcement.
"""

from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

class GovernanceManager:
    """Manages project governance, compliance, and quality assurance."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.governance_path = project_path / ".goal" / "governance"
        self.governance_path.mkdir(exist_ok=True)
        
        # Load constitution if it exists
        self.constitution = self._load_constitution()
        
        # Load governance rules
        self.rules = self._load_governance_rules()
        
        # Load quality standards
        self.quality_standards = self._load_quality_standards()
        
        # Load compliance requirements
        self.compliance_requirements = self._load_compliance_requirements()
    
    def _load_constitution(self) -> Optional[Dict]:
        """Load project constitution."""
        constitution_path = self.governance_path / "constitution.md"
        if constitution_path.exists():
            # For now, we'll just acknowledge the constitution exists
            # In a full implementation, we would parse and enforce it
            return {"exists": True, "path": str(constitution_path)}
        return None
    
    def _load_governance_rules(self) -> Dict:
        """Load governance rules."""
        # Default governance rules
        return {
            "required_fields": {
                "goal": ["title", "description", "objectives", "success_criteria"],
                "spec": ["title", "description", "user_stories", "acceptance_criteria"],
                "plan": ["title", "description", "tasks", "timeline"],
                "task": ["title", "description", "status", "priority"]
            },
            "allowed_values": {
                "priority": ["low", "medium", "high", "critical"],
                "status": ["draft", "planned", "in_progress", "completed", "blocked"]
            },
            "validation_rules": {
                "goal_title_length": {"max": 100},
                "description_min_length": {"min": 10},
                "objectives_min_count": {"min": 1},
                "success_criteria_min_count": {"min": 1}
            }
        }
    
    def _load_quality_standards(self) -> Dict:
        """Load quality standards."""
        return {
            "specification_quality": {
                "min_acceptance_criteria": 3,
                "max_ambiguity_score": 0.3,  # 30% ambiguity threshold
                "min_clarity_score": 0.7,    # 70% clarity threshold
                "required_sections": ["user_stories", "acceptance_criteria", "functional_requirements"]
            },
            "implementation_quality": {
                "test_coverage_threshold": 0.8,  # 80% test coverage
                "code_review_required": True,
                "security_scan_required": True
            }
        }
    
    def _load_compliance_requirements(self) -> Dict:
        """Load compliance requirements."""
        return {
            "security": {
                "required_security_review": True,
                "vulnerability_scan_required": True,
                "data_protection_compliance": True
            },
            "documentation": {
                "change_log_required": True,
                "api_documentation_required": True,
                "user_documentation_required": True
            },
            "process": {
                "peer_review_required": True,
                "qa_validation_required": True,
                "deployment_approval_required": True
            }
        }
    
    def validate_goal(self, goal_data: Dict) -> Dict:
        """Validate a goal against governance rules."""
        violations = []
        warnings = []
        
        # Check required fields
        for field in self.rules["required_fields"]["goal"]:
            if field not in goal_data or not goal_data[field]:
                violations.append(f"Missing required field: {field}")
        
        # Check allowed values
        if "priority" in goal_data:
            if goal_data["priority"] not in self.rules["allowed_values"]["priority"]:
                violations.append(f"Invalid priority value: {goal_data['priority']}")
        
        if "status" in goal_data:
            if goal_data["status"] not in self.rules["allowed_values"]["status"]:
                violations.append(f"Invalid status value: {goal_data['status']}")
        
        # Check validation rules
        if "title" in goal_data:
            if len(goal_data["title"]) > self.rules["validation_rules"]["goal_title_length"]["max"]:
                violations.append(f"Goal title exceeds maximum length of {self.rules['validation_rules']['goal_title_length']['max']}")
        
        if "description" in goal_data:
            if len(goal_data["description"]) < self.rules["validation_rules"]["description_min_length"]["min"]:
                violations.append(f"Goal description must be at least {self.rules['validation_rules']['description_min_length']['min']} characters")
        
        if "objectives" in goal_data:
            if len(goal_data["objectives"]) < self.rules["validation_rules"]["objectives_min_count"]["min"]:
                violations.append(f"Goal must have at least {self.rules['validation_rules']['objectives_min_count']['min']} objective(s)")
        
        if "success_criteria" in goal_data:
            if len(goal_data["success_criteria"]) < self.rules["validation_rules"]["success_criteria_min_count"]["min"]:
                violations.append(f"Goal must have at least {self.rules['validation_rules']['success_criteria_min_count']['min']} success criterion/criteria")
        
        # Quality checks
        if "objectives" in goal_data and goal_data["objectives"]:
            # Check if objectives are sufficiently detailed
            for i, objective in enumerate(goal_data["objectives"]):
                if isinstance(objective, str) and len(objective) < 10:
                    warnings.append(f"Objective {i+1} may be too brief: '{objective}'")
        
        if "success_criteria" in goal_data and goal_data["success_criteria"]:
            # Check if success criteria are measurable
            for i, criterion in enumerate(goal_data["success_criteria"]):
                if isinstance(criterion, str) and len(criterion) < 15:
                    warnings.append(f"Success criterion {i+1} may not be measurable: '{criterion}'")
        
        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "warnings": warnings
        }
    
    def validate_spec(self, spec_data: Dict) -> Dict:
        """Validate a specification against governance rules."""
        violations = []
        warnings = []
        
        # Check required fields
        for field in self.rules["required_fields"]["spec"]:
            if field not in spec_data or not spec_data[field]:
                violations.append(f"Missing required field: {field}")
        
        # Quality checks
        quality_score = self._assess_specification_quality(spec_data)
        
        if quality_score["ambiguity_score"] > self.quality_standards["specification_quality"]["max_ambiguity_score"]:
            violations.append(f"Specification ambiguity score ({quality_score['ambiguity_score']:.2f}) exceeds threshold ({self.quality_standards['specification_quality']['max_ambiguity_score']})")
        
        if quality_score["clarity_score"] < self.quality_standards["specification_quality"]["min_clarity_score"]:
            violations.append(f"Specification clarity score ({quality_score['clarity_score']:.2f}) below threshold ({self.quality_standards['specification_quality']['min_clarity_score']})")
        
        # Check required sections
        for section in self.quality_standards["specification_quality"]["required_sections"]:
            if section not in spec_data or not spec_data[section]:
                violations.append(f"Missing required section: {section}")
        
        # Check acceptance criteria count
        if "acceptance_criteria" in spec_data:
            if len(spec_data["acceptance_criteria"]) < self.quality_standards["specification_quality"]["min_acceptance_criteria"]:
                violations.append(f"Specification must have at least {self.quality_standards['specification_quality']['min_acceptance_criteria']} acceptance criteria")
        
        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "quality_score": quality_score
        }
    
    def _assess_specification_quality(self, spec_data: Dict) -> Dict:
        """Assess the quality of a specification."""
        # This is a simplified quality assessment
        # In a real implementation, this would use NLP and ML techniques
        
        ambiguity_indicators = ["maybe", "possibly", "sometimes", "usually", "might", "could", "should"]
        clarity_indicators = ["must", "shall", "will", "guaranteed", "ensured", "verified"]
        
        text_content = ""
        if "description" in spec_data:
            text_content += spec_data["description"] + " "
        if "user_stories" in spec_data:
            for story in spec_data["user_stories"]:
                if isinstance(story, str):
                    text_content += story + " "
                elif isinstance(story, dict) and "description" in story:
                    text_content += story["description"] + " "
        if "acceptance_criteria" in spec_data:
            for criterion in spec_data["acceptance_criteria"]:
                if isinstance(criterion, str):
                    text_content += criterion + " "
                elif isinstance(criterion, dict) and "description" in criterion:
                    text_content += criterion["description"] + " "
        
        # Count ambiguity indicators
        ambiguity_count = sum(text_content.lower().count(indicator) for indicator in ambiguity_indicators)
        clarity_count = sum(text_content.lower().count(indicator) for indicator in clarity_indicators)
        
        total_indicators = ambiguity_count + clarity_count
        if total_indicators > 0:
            ambiguity_score = ambiguity_count / total_indicators
            clarity_score = clarity_count / total_indicators
        else:
            ambiguity_score = 0.0
            clarity_score = 1.0
        
        return {
            "ambiguity_score": ambiguity_score,
            "clarity_score": clarity_score,
            "total_words": len(text_content.split())
        }
    
    def check_compliance(self, artifact_type: str, artifact_data: Dict) -> Dict:
        """Check compliance for an artifact."""
        violations = []
        warnings = []
        
        # Security compliance
        if self.compliance_requirements["security"]["required_security_review"]:
            if "metadata" in artifact_data and "security_reviewed" not in artifact_data["metadata"]:
                violations.append("Security review required but not performed")
        
        # Documentation compliance
        if self.compliance_requirements["documentation"]["change_log_required"]:
            if "metadata" in artifact_data and "changelog" not in artifact_data["metadata"]:
                warnings.append("Change log recommended for tracking changes")
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "warnings": warnings
        }
    
    def enforce_quality_gate(self, stage: str, artifact_type: str, artifact_data: Dict) -> Dict:
        """Enforce quality gates for a specific stage."""
        gate_results = {
            "passed": True,
            "violations": [],
            "warnings": [],
            "quality_scores": {}
        }
        
        # Validate based on artifact type
        if artifact_type == "goal":
            validation_result = self.validate_goal(artifact_data)
        elif artifact_type == "spec":
            validation_result = self.validate_spec(artifact_data)
            if "quality_score" in validation_result:
                gate_results["quality_scores"] = validation_result["quality_score"]
        else:
            validation_result = {"valid": True, "violations": [], "warnings": []}
        
        # Add validation results
        if not validation_result["valid"]:
            gate_results["passed"] = False
            gate_results["violations"].extend(validation_result["violations"])
        
        if validation_result["warnings"]:
            gate_results["warnings"].extend(validation_result["warnings"])
        
        # Check compliance
        compliance_result = self.check_compliance(artifact_type, artifact_data)
        if not compliance_result["compliant"]:
            gate_results["passed"] = False
            gate_results["violations"].extend(compliance_result["violations"])
        
        if compliance_result["warnings"]:
            gate_results["warnings"].extend(compliance_result["warnings"])
        
        return gate_results
    
    def generate_governance_report(self) -> Dict:
        """Generate a governance compliance report."""
        report = {
            "generated_at": datetime.now().isoformat(),
            "project_path": str(self.project_path),
            "constitution": self.constitution,
            "compliance_status": "unknown",
            "violations": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Check if constitution exists
        if not self.constitution:
            report["violations"].append("Project constitution not found")
            report["recommendations"].append("Create a project constitution using the constitution template")
        
        # In a full implementation, we would check all artifacts for compliance
        # For now, we'll just provide the framework
        
        return report

# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    manager = GovernanceManager(Path("."))
    print("GovernanceManager initialized")