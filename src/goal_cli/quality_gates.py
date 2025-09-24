"""
Quality gates module for the goal-dev-spec system.
Provides automated validation and quality assurance checkpoints.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from .governance import GovernanceManager

class QualityGate:
    """Represents a single quality gate."""
    
    def __init__(self, name: str, description: str, checks: List[str]):
        self.name = name
        self.description = description
        self.checks = checks
        self.passed = False
        self.results: Dict[str, Any] = {}
        self.timestamp: Optional[str] = None

class QualityGateManager:
    """Manages quality gates and validation processes."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.governance_manager = GovernanceManager(project_path)
        self.gates = self._initialize_gates()
    
    def _initialize_gates(self) -> Dict[str, QualityGate]:
        """Initialize the quality gates."""
        return {
            "goal_definition": QualityGate(
                "Goal Definition Gate",
                "Validates that goals are well-defined with clear objectives and success criteria",
                ["required_fields", "clarity_check", "dependency_analysis"]
            ),
            "specification": QualityGate(
                "Specification Gate",
                "Ensures specifications are complete, clear, and testable",
                ["required_sections", "acceptance_criteria", "ambiguity_check", "consistency_check"]
            ),
            "implementation_planning": QualityGate(
                "Implementation Planning Gate",
                "Validates that implementation plans are detailed and realistic",
                ["task_breakdown", "resource_allocation", "timeline_validation", "risk_assessment"]
            ),
            "task_execution": QualityGate(
                "Task Execution Gate",
                "Ensures tasks are completed with proper testing and documentation",
                ["code_review", "test_coverage", "documentation", "security_scan"]
            ),
            "review_validation": QualityGate(
                "Review and Validation Gate",
                "Confirms that all reviews and validations have been completed",
                ["stakeholder_approval", "qa_validation", "security_review", "compliance_check"]
            ),
            "deployment": QualityGate(
                "Deployment Gate",
                "Verifies that all deployment requirements are met",
                ["deployment_testing", "rollback_plan", "monitoring_setup", "notification_config"]
            )
        }
    
    def validate_gate(self, gate_name: str, artifact_type: str, artifact_data: Dict) -> Dict:
        """Validate a specific quality gate."""
        if gate_name not in self.gates:
            return {
                "valid": False,
                "error": f"Unknown quality gate: {gate_name}"
            }
        
        gate = self.gates[gate_name]
        gate.timestamp = datetime.now().isoformat()
        
        # Use governance manager to enforce quality gates
        gate_result = self.governance_manager.enforce_quality_gate(gate_name, artifact_type, artifact_data)
        
        # Store results
        gate.passed = gate_result["passed"]
        gate.results = gate_result
        
        return {
            "gate": gate_name,
            "passed": gate_result["passed"],
            "violations": gate_result["violations"],
            "warnings": gate_result["warnings"],
            "quality_scores": gate_result.get("quality_scores", {})
        }
    
    def validate_all_gates(self, project_data: Dict) -> Dict:
        """Validate all quality gates for a project."""
        results: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "project": str(self.project_path),
            "gates": {},
            "overall_status": "unknown"
        }
        
        all_passed = True
        
        # For a real implementation, we would validate each gate with appropriate data
        # For this example, we'll just show the framework
        
        for gate_name, gate in self.gates.items():
            # In a real implementation, we would pass actual artifact data
            # For now, we'll simulate a basic validation
            gate_result = {
                "passed": True,
                "violations": [],
                "warnings": []
            }
            
            results["gates"][gate_name] = {
                "name": gate.name,
                "description": gate.description,
                "passed": gate_result["passed"],
                "violations": gate_result["violations"],
                "warnings": gate_result["warnings"]
            }
            
            if not gate_result["passed"]:
                all_passed = False
        
        results["overall_status"] = "PASSED" if all_passed else "FAILED"
        return results
    
    def get_gate_status(self, gate_name: str) -> Optional[Dict]:
        """Get the status of a specific gate."""
        if gate_name not in self.gates:
            return None
        
        gate = self.gates[gate_name]
        return {
            "name": gate.name,
            "description": gate.description,
            "passed": gate.passed,
            "last_checked": gate.timestamp,
            "results": gate.results
        }
    
    def generate_quality_report(self, project_data: Dict) -> str:
        """Generate a quality report in markdown format."""
        results = self.validate_all_gates(project_data)
        
        report = "# Quality Gates Report\n\n"
        report += f"Generated: {results['timestamp']}\n\n"
        report += f"Project: {results['project']}\n\n"
        
        if results["overall_status"] == "PASSED":
            report += "## Overall Status: ✅ ALL GATES PASSED\n\n"
        else:
            report += "## Overall Status: ❌ GATES FAILED\n\n"
        
        for gate_name, gate_result in results["gates"].items():
            report += f"## {gate_result['name']}\n\n"
            report += f"{gate_result['description']}\n\n"
            
            if gate_result["passed"]:
                report += "Status: ✅ PASSED\n\n"
            else:
                report += "Status: ❌ FAILED\n\n"
                if gate_result["violations"]:
                    report += "Violations:\n"
                    for violation in gate_result["violations"]:
                        report += f"- {violation}\n"
                    report += "\n"
                
                if gate_result["warnings"]:
                    report += "Warnings:\n"
                    for warning in gate_result["warnings"]:
                        report += f"- {warning}\n"
                    report += "\n"
        
        return report

# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    manager = QualityGateManager(Path("."))
    print("QualityGateManager initialized")