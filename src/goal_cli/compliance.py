"""
Compliance checking module for the goal-dev-spec system.
Provides automated compliance validation against industry standards and regulations.
"""

from pathlib import Path
from typing import Dict
from datetime import datetime

class ComplianceChecker:
    """Checks compliance with industry standards, regulations, and organizational policies."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.compliance_path = project_path / ".goal" / "compliance"
        self.compliance_path.mkdir(exist_ok=True)
        
        # Load compliance standards
        self.standards = self._load_compliance_standards()
        
        # Load organizational policies
        self.policies = self._load_organizational_policies()
    
    def _load_compliance_standards(self) -> Dict:
        """Load compliance standards."""
        return {
            "gdpr": {
                "name": "General Data Protection Regulation",
                "requirements": [
                    "data_minimization",
                    "purpose_limitation",
                    "data_subject_rights",
                    "data_protection_by_design",
                    "privacy_by_default"
                ],
                "check_functions": {
                    "data_minimization": self._check_data_minimization,
                    "purpose_limitation": self._check_purpose_limitation,
                    "data_subject_rights": self._check_data_subject_rights,
                    "data_protection_by_design": self._check_data_protection_by_design,
                    "privacy_by_default": self._check_privacy_by_default
                }
            },
            "iso27001": {
                "name": "ISO/IEC 27001 Information Security Management",
                "requirements": [
                    "access_control",
                    "encryption",
                    "incident_response",
                    "risk_assessment",
                    "security_testing"
                ],
                "check_functions": {
                    "access_control": self._check_access_control,
                    "encryption": self._check_encryption,
                    "incident_response": self._check_incident_response,
                    "risk_assessment": self._check_risk_assessment,
                    "security_testing": self._check_security_testing
                }
            },
            "soc2": {
                "name": "SOC 2 Trust Services Criteria",
                "requirements": [
                    "security",
                    "availability",
                    "processing_integrity",
                    "confidentiality",
                    "privacy"
                ],
                "check_functions": {
                    "security": self._check_security,
                    "availability": self._check_availability,
                    "processing_integrity": self._check_processing_integrity,
                    "confidentiality": self._check_confidentiality,
                    "privacy": self._check_privacy
                }
            }
        }
    
    def _load_organizational_policies(self) -> Dict:
        """Load organizational policies."""
        # In a real implementation, this would load from policy files
        return {
            "coding_standards": {
                "name": "Organizational Coding Standards",
                "rules": [
                    "code_review_required",
                    "test_coverage_minimum",
                    "documentation_required"
                ]
            },
            "data_handling": {
                "name": "Data Handling Policy",
                "rules": [
                    "data_classification_required",
                    "access_logging_required",
                    "data_retention_policy"
                ]
            }
        }
    
    def check_compliance_standard(self, standard: str, project_data: Dict) -> Dict:
        """Check compliance with a specific standard."""
        if standard not in self.standards:
            return {
                "standard": standard,
                "valid": False,
                "error": f"Unknown compliance standard: {standard}"
            }
        
        standard_def = self.standards[standard]
        results = {
            "standard": standard,
            "name": standard_def["name"],
            "compliant": True,
            "requirements": {}
        }
        
        # Check each requirement
        for requirement in standard_def["requirements"]:
            if requirement in standard_def["check_functions"]:
                check_function = standard_def["check_functions"][requirement]
                requirement_result = check_function(project_data)
                results["requirements"][requirement] = requirement_result
                
                # If any requirement fails, the overall standard fails
                if not requirement_result["compliant"]:
                    results["compliant"] = False
            else:
                results["requirements"][requirement] = {
                    "compliant": False,
                    "error": f"No check function for requirement: {requirement}"
                }
                results["compliant"] = False
        
        return results
    
    def check_all_standards(self, project_data: Dict) -> Dict:
        """Check compliance with all applicable standards."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "project": str(self.project_path),
            "standards": {}
        }
        
        overall_compliant = True
        
        for standard in self.standards:
            standard_result = self.check_compliance_standard(standard, project_data)
            results["standards"][standard] = standard_result
            
            if not standard_result["compliant"]:
                overall_compliant = False
        
        results["overall_compliant"] = overall_compliant
        return results
    
    def _check_data_minimization(self, project_data: Dict) -> Dict:
        """Check GDPR data minimization requirement."""
        # Check if project collects only necessary data
        findings = []
        compliant = True
        
        # This is a simplified check - in reality, this would be much more complex
        if "specs" in project_data:
            for spec in project_data["specs"]:
                if "data_requirements" in spec:
                    data_reqs = spec["data_requirements"]
                    if isinstance(data_reqs, list):
                        for req in data_reqs:
                            if isinstance(req, str) and "all user data" in req.lower():
                                findings.append("Potential data over-collection detected")
                                compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_purpose_limitation(self, project_data: Dict) -> Dict:
        """Check GDPR purpose limitation requirement."""
        # Check if data usage is limited to specified purposes
        findings = []
        compliant = True
        
        # This is a simplified check
        if "goals" in project_data:
            for goal in project_data["goals"]:
                if "data_usage" in goal and not goal["data_usage"]:
                    findings.append("Data usage not specified for goal")
                    compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_data_subject_rights(self, project_data: Dict) -> Dict:
        """Check GDPR data subject rights requirement."""
        # Check if project supports data subject rights
        findings = []
        compliant = True
        
        # This is a simplified check
        has_data_subject_support = False
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                if "privacy_features" in spec:
                    has_data_subject_support = True
                    break
        
        if not has_data_subject_support:
            findings.append("No explicit support for data subject rights detected")
            compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_data_protection_by_design(self, project_data: Dict) -> Dict:
        """Check GDPR data protection by design requirement."""
        # Check if security is integrated by design
        findings = []
        compliant = True
        
        # This is a simplified check
        has_security_by_design = False
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                if "security_measures" in spec:
                    has_security_by_design = True
                    break
        
        if not has_security_by_design:
            findings.append("No explicit security by design measures detected")
            compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_privacy_by_default(self, project_data: Dict) -> Dict:
        """Check GDPR privacy by default requirement."""
        # Check if privacy settings are opt-out rather than opt-in
        findings = []
        compliant = True
        
        # This is a simplified check
        findings.append("Privacy by default check not implemented - requires manual verification")
        # In a real implementation, this would check actual privacy settings
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_access_control(self, project_data: Dict) -> Dict:
        """Check ISO 27001 access control requirement."""
        findings = []
        compliant = True
        
        # This is a simplified check
        has_access_control = False
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                if "access_control" in spec:
                    has_access_control = True
                    break
        
        if not has_access_control:
            findings.append("No explicit access control mechanisms specified")
            compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_encryption(self, project_data: Dict) -> Dict:
        """Check ISO 27001 encryption requirement."""
        findings = []
        compliant = True
        
        # This is a simplified check
        has_encryption = False
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                if "encryption" in spec:
                    has_encryption = True
                    break
        
        if not has_encryption:
            findings.append("No explicit encryption requirements specified")
            compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_incident_response(self, project_data: Dict) -> Dict:
        """Check ISO 27001 incident response requirement."""
        findings = []
        compliant = True
        
        # This is a simplified check
        has_incident_response = False
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                if "incident_response" in spec:
                    has_incident_response = True
                    break
        
        if not has_incident_response:
            findings.append("No explicit incident response procedures specified")
            compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_risk_assessment(self, project_data: Dict) -> Dict:
        """Check ISO 27001 risk assessment requirement."""
        findings = []
        compliant = True
        
        # This is a simplified check
        has_risk_assessment = False
        
        if "goals" in project_data:
            for goal in project_data["goals"]:
                if "risk_assessment" in goal:
                    has_risk_assessment = True
                    break
        
        if not has_risk_assessment:
            findings.append("No explicit risk assessment documented")
            compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_security_testing(self, project_data: Dict) -> Dict:
        """Check ISO 27001 security testing requirement."""
        findings = []
        compliant = True
        
        # This is a simplified check
        has_security_testing = False
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                if "security_testing" in spec:
                    has_security_testing = True
                    break
        
        if not has_security_testing:
            findings.append("No explicit security testing requirements specified")
            compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_security(self, project_data: Dict) -> Dict:
        """Check SOC 2 security requirement."""
        findings = []
        compliant = True
        
        # This is a simplified check - similar to ISO 27001 access control
        has_security = False
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                if "security" in spec:
                    has_security = True
                    break
        
        if not has_security:
            findings.append("No explicit security controls specified")
            compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_availability(self, project_data: Dict) -> Dict:
        """Check SOC 2 availability requirement."""
        findings = []
        compliant = True
        
        # This is a simplified check
        has_availability = False
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                if "availability" in spec or "uptime" in spec:
                    has_availability = True
                    break
        
        if not has_availability:
            findings.append("No explicit availability requirements specified")
            compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_processing_integrity(self, project_data: Dict) -> Dict:
        """Check SOC 2 processing integrity requirement."""
        findings = []
        compliant = True
        
        # This is a simplified check
        has_processing_integrity = False
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                if "processing_integrity" in spec or "data_integrity" in spec:
                    has_processing_integrity = True
                    break
        
        if not has_processing_integrity:
            findings.append("No explicit processing integrity requirements specified")
            compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_confidentiality(self, project_data: Dict) -> Dict:
        """Check SOC 2 confidentiality requirement."""
        findings = []
        compliant = True
        
        # This is a simplified check
        has_confidentiality = False
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                if "confidentiality" in spec:
                    has_confidentiality = True
                    break
        
        if not has_confidentiality:
            findings.append("No explicit confidentiality requirements specified")
            compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def _check_privacy(self, project_data: Dict) -> Dict:
        """Check SOC 2 privacy requirement."""
        findings = []
        compliant = True
        
        # This is a simplified check - similar to GDPR privacy checks
        has_privacy = False
        
        if "specs" in project_data:
            for spec in project_data["specs"]:
                if "privacy" in spec:
                    has_privacy = True
                    break
        
        if not has_privacy:
            findings.append("No explicit privacy requirements specified")
            compliant = False
        
        return {
            "compliant": compliant,
            "findings": findings
        }
    
    def generate_compliance_report(self, project_data: Dict) -> str:
        """Generate a compliance report in markdown format."""
        results = self.check_all_standards(project_data)
        
        report = "# Compliance Report\n\n"
        report += f"Generated: {results['timestamp']}\n\n"
        report += f"Project: {results['project']}\n\n"
        
        if results["overall_compliant"]:
            report += "## Overall Status: ✅ COMPLIANT\n\n"
        else:
            report += "## Overall Status: ❌ NON-COMPLIANT\n\n"
        
        for standard, standard_result in results["standards"].items():
            report += f"## {standard_result['name']} ({standard.upper()})\n\n"
            
            if standard_result["compliant"]:
                report += "Status: ✅ COMPLIANT\n\n"
            else:
                report += "Status: ❌ NON-COMPLIANT\n\n"
            
            for requirement, req_result in standard_result["requirements"].items():
                if req_result["compliant"]:
                    report += f"- {requirement}: ✅ COMPLIANT\n"
                else:
                    report += f"- {requirement}: ❌ NON-COMPLIANT\n"
                    if "findings" in req_result:
                        for finding in req_result["findings"]:
                            report += f"  - {finding}\n"
            
            report += "\n"
        
        return report

# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    checker = ComplianceChecker(Path("."))
    print("ComplianceChecker initialized")