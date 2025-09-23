"""
Main governance module for the goal-dev-spec system.
Integrates all governance components into a unified system.
"""

from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from .governance import GovernanceManager
from .compliance import ComplianceChecker
from .quality_gates import QualityGateManager
from .security import SecurityManager
from .performance import PerformanceMonitor
from .reviews import ReviewManager
from .versioning import VersionManager

class GovernanceSystem:
    """Main governance system that integrates all governance components."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        
        # Initialize all governance components
        self.governance_manager = GovernanceManager(project_path)
        self.compliance_checker = ComplianceChecker(project_path)
        self.quality_gate_manager = QualityGateManager(project_path)
        self.security_manager = SecurityManager(project_path)
        self.performance_monitor = PerformanceMonitor(project_path)
        self.review_manager = ReviewManager(project_path)
        self.version_manager = VersionManager(project_path)
        
        # Ensure governance directory exists
        self.governance_dir = project_path / ".goal" / "governance"
        self.governance_dir.mkdir(exist_ok=True)
    
    def initialize_project_constitution(self, project_name: str = None) -> str:
        """
        Initialize a project constitution from the template.
        
        Args:
            project_name: Name of the project to include in the constitution
            
        Returns:
            Path to the created constitution file
        """
        # Load the constitution template
        template_path = self.project_path / "templates" / "constitution-template.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Constitution template not found at {template_path}")
        
        with open(template_path, 'r') as f:
            constitution_content = f.read()
        
        # Replace placeholder with actual project name
        if project_name:
            constitution_content = constitution_content.replace("[PROJECT_NAME]", project_name)
        
        # Save the constitution
        constitution_path = self.governance_dir / "constitution.md"
        with open(constitution_path, 'w') as f:
            f.write(constitution_content)
        
        return str(constitution_path)
    
    def validate_artifact(self, artifact_type: str, artifact_data: Dict) -> Dict:
        """
        Validate an artifact against governance rules.
        
        Args:
            artifact_type: Type of artifact (goal, spec, plan, task)
            artifact_data: The artifact data to validate
            
        Returns:
            Validation results
        """
        return self.governance_manager.enforce_quality_gate("artifact_validation", artifact_type, artifact_data)
    
    def check_compliance(self, project_data: Dict) -> Dict:
        """
        Check project compliance with standards and regulations.
        
        Args:
            project_data: The project data to check
            
        Returns:
            Compliance check results
        """
        return self.compliance_checker.check_all_standards(project_data)
    
    def validate_quality_gate(self, gate_name: str, artifact_type: str, artifact_data: Dict) -> Dict:
        """
        Validate a specific quality gate.
        
        Args:
            gate_name: Name of the quality gate
            artifact_type: Type of artifact
            artifact_data: The artifact data to validate
            
        Returns:
            Quality gate validation results
        """
        return self.quality_gate_manager.validate_gate(gate_name, artifact_type, artifact_data)
    
    def scan_for_security_vulnerabilities(self) -> Dict:
        """
        Scan the project for security vulnerabilities.
        
        Returns:
            Security scan results
        """
        # For now, we'll create mock project data
        # In a real implementation, this would scan actual project files
        return self.security_manager.scan_project_for_vulnerabilities()
    
    def check_security_policies(self, project_data: Dict) -> Dict:
        """
        Check compliance with security policies.
        
        Args:
            project_data: The project data to check
            
        Returns:
            Security policy check results
        """
        return self.security_manager.check_all_policies(project_data)
    
    def record_performance_metric(self, metric_name: str, value: float, context: Dict = None):
        """
        Record a performance metric.
        
        Args:
            metric_name: Name of the metric
            value: Value of the metric
            context: Additional context for the metric
        """
        self.performance_monitor.record_metric(metric_name, value, context)
    
    def get_performance_stats(self, metric_name: str) -> Dict:
        """
        Get performance statistics for a metric.
        
        Args:
            metric_name: Name of the metric
            
        Returns:
            Performance statistics
        """
        return self.performance_monitor.get_metric_stats(metric_name)
    
    def create_review(self, review_type: str, artifact_id: str, artifact_data: Dict) -> str:
        """
        Create a new review for an artifact.
        
        Args:
            review_type: Type of review
            artifact_id: ID of the artifact to review
            artifact_data: The artifact data to review
            
        Returns:
            ID of the created review
        """
        from .reviews import ReviewType
        try:
            review_type_enum = ReviewType(review_type)
        except ValueError:
            raise ValueError(f"Invalid review type: {review_type}")
        
        return self.review_manager.create_review(review_type_enum, artifact_id, artifact_data)
    
    def add_review_comment(self, review_id: str, reviewer: str, comment: str, approved: Optional[bool] = None) -> bool:
        """
        Add a comment to a review.
        
        Args:
            review_id: ID of the review
            reviewer: Name of the reviewer
            comment: Comment text
            approved: Approval status
            
        Returns:
            True if successful, False otherwise
        """
        return self.review_manager.add_comment(review_id, reviewer, comment, approved)
    
    def bump_project_version(self, bump_type: str, breaking_changes: List[str] = None, 
                           new_features: List[str] = None, bug_fixes: List[str] = None) -> str:
        """
        Bump the project version.
        
        Args:
            bump_type: Type of version bump (major, minor, patch)
            breaking_changes: List of breaking changes
            new_features: List of new features
            bug_fixes: List of bug fixes
            
        Returns:
            New version string
        """
        return self.version_manager.bump_version(bump_type, breaking_changes, new_features, bug_fixes)
    
    def detect_breaking_changes(self, old_spec: Dict, new_spec: Dict) -> List[str]:
        """
        Detect breaking changes between specifications.
        
        Args:
            old_spec: Old specification
            new_spec: New specification
            
        Returns:
            List of breaking changes
        """
        return self.version_manager.detect_breaking_changes(old_spec, new_spec)
    
    def generate_governance_report(self, project_data: Dict) -> str:
        """
        Generate a comprehensive governance report.
        
        Args:
            project_data: The project data to analyze
            
        Returns:
            Governance report in markdown format
        """
        report = "# Governance Report\n\n"
        report += f"Generated: {datetime.now().isoformat()}\n\n"
        report += f"Project: {self.project_path}\n\n"
        
        # Add governance status
        governance_report = self.governance_manager.generate_governance_report()
        report += "## Governance Status\n\n"
        if governance_report.get("constitution"):
            report += "✅ Project constitution exists\n\n"
        else:
            report += "❌ Project constitution missing\n\n"
            report += "Recommendation: Initialize project constitution using `goal governance init`\n\n"
        
        # Add compliance status
        compliance_results = self.check_compliance(project_data)
        report += "## Compliance Status\n\n"
        if compliance_results["overall_compliant"]:
            report += "✅ All compliance standards met\n\n"
        else:
            report += "❌ Compliance issues detected\n\n"
            for standard, result in compliance_results["standards"].items():
                if not result["compliant"]:
                    report += f"- {result['name']}: NON-COMPLIANT\n"
            report += "\n"
        
        # Add security status
        security_results = self.check_security_policies(project_data)
        report += "## Security Status\n\n"
        if security_results["overall_compliant"]:
            report += "✅ All security policies compliant\n\n"
        else:
            report += "❌ Security policy violations detected\n\n"
            for policy, result in security_results["policies"].items():
                if not result["compliant"]:
                    report += f"- {result['name']}: NON-COMPLIANT\n"
            report += "\n"
        
        # Add quality gate status
        quality_results = self.quality_gate_manager.validate_all_gates(project_data)
        report += "## Quality Gates\n\n"
        if quality_results["overall_status"] == "PASSED":
            report += "✅ All quality gates passed\n\n"
        else:
            report += "❌ Quality gate failures detected\n\n"
            for gate_name, gate_result in quality_results["gates"].items():
                if not gate_result["passed"]:
                    report += f"- {gate_result['name']}: FAILED\n"
            report += "\n"
        
        # Add performance metrics
        report += "## Performance Metrics\n\n"
        # This would show actual metrics in a real implementation
        report += "Performance metrics tracking is configured.\n\n"
        
        # Add review status
        reviews = self.review_manager.list_reviews()
        report += "## Review Status\n\n"
        report += f"Total reviews: {len(reviews)}\n"
        # Count reviews by status
        status_counts = {}
        for review in reviews:
            status = review["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in status_counts.items():
            report += f"- {status.replace('_', ' ').title()}: {count}\n"
        report += "\n"
        
        # Add version information
        report += "## Version Information\n\n"
        report += f"Current version: {self.version_manager.current_version}\n"
        report += f"Version history entries: {len(self.version_manager.version_history)}\n\n"
        
        return report
    
    def generate_all_reports(self, project_data: Dict) -> Dict[str, str]:
        """
        Generate all governance-related reports.
        
        Args:
            project_data: The project data to analyze
            
        Returns:
            Dictionary of report names and their content
        """
        reports = {}
        
        # Main governance report
        reports["governance"] = self.generate_governance_report(project_data)
        
        # Compliance report
        reports["compliance"] = self.compliance_checker.generate_compliance_report(project_data)
        
        # Quality report
        reports["quality"] = self.quality_gate_manager.generate_quality_report(project_data)
        
        # Security report
        reports["security"] = self.security_manager.generate_security_report(project_data)
        
        # Performance report
        reports["performance"] = self.performance_monitor.generate_performance_report()
        
        # Review report
        reports["reviews"] = self.review_manager.generate_review_report()
        
        # Version changelog
        reports["changelog"] = self.version_manager.generate_changelog()
        
        return reports

# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    system = GovernanceSystem(Path("."))
    print("GovernanceSystem initialized")