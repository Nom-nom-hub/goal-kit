"""
Security module for the goal-dev-spec system.
Provides security scanning, vulnerability detection, and security policy enforcement.
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Union
from datetime import datetime

class SecurityManager:
    """Manages security scanning, vulnerability detection, and policy enforcement."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.security_path = project_path / ".goal" / "security"
        self.security_path.mkdir(exist_ok=True)
        
        # Load security policies
        self.policies = self._load_security_policies()
        
        # Load vulnerability patterns
        self.vulnerability_patterns = self._load_vulnerability_patterns()
    
    def _load_security_policies(self) -> Dict:
        """Load security policies."""
        return {
            "data_protection": {
                "name": "Data Protection Policy",
                "rules": [
                    "no_hardcoded_secrets",
                    "encryption_at_rest",
                    "encryption_in_transit",
                    "data_minimization"
                ]
            },
            "access_control": {
                "name": "Access Control Policy",
                "rules": [
                    "least_privilege",
                    "authentication_required",
                    "authorization_checks",
                    "audit_logging"
                ]
            },
            "code_security": {
                "name": "Code Security Policy",
                "rules": [
                    "input_validation",
                    "output_encoding",
                    "secure_defaults",
                    "dependency_security"
                ]
            },
            "infrastructure": {
                "name": "Infrastructure Security Policy",
                "rules": [
                    "secure_configuration",
                    "network_segmentation",
                    "monitoring_enabled",
                    "incident_response"
                ]
            }
        }
    
    def _load_vulnerability_patterns(self) -> Dict:
        """Load common vulnerability patterns."""
        return {
            "hardcoded_secrets": [
                r"password\s*=\s*[\"'][^\"']+[\"']",
                r"secret\s*=\s*[\"'][^\"']+[\"']",
                r"api[key]?\s*=\s*[\"'][^\"']+[\"']",
                r"token\s*=\s*[\"'][^\"']+[\"']"
            ],
            "sql_injection": [
                r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|EXEC)\b.*\{.*\}",
                r"=\s*\{.*\}",
                r"\+\s*\{.*\}"
            ],
            "xss": [
                r"<script.*?>.*?</script>",
                r"javascript:",
                r"on\w+\s*=\s*[\"'].*?[\"']"
            ],
            "insecure_deserialization": [
                r"\.deserialize\(",
                r"pickle\.loads\(",
                r"eval\("
            ]
        }
    
    def scan_for_vulnerabilities(self, content: str, file_path: str = "") -> Dict[str, Any]:
        """Scan content for common vulnerabilities."""
        findings = []
        
        for vuln_type, patterns in self.vulnerability_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    findings.append({
                        "type": vuln_type,
                        "pattern": pattern,
                        "match": match.group(),
                        "line": content[:match.start()].count('\n') + 1,
                        "file": file_path
                    })
        
        return {
            "timestamp": datetime.now().isoformat(),
            "file": file_path,
            "vulnerabilities_found": len(findings),
            "findings": findings
        }
    
    def scan_project_for_vulnerabilities(self) -> Dict[str, Any]:
        """Scan the entire project for vulnerabilities."""
        results: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "project": str(self.project_path),
            "files_scanned": 0,
            "total_vulnerabilities": 0,
            "vulnerabilities_by_type": {},
            "findings": []
        }
        
        # Scan common file types for vulnerabilities
        file_patterns = ["*.py", "*.js", "*.ts", "*.java", "*.cs", "*.go", "*.rb", "*.php"]
        
        for pattern in file_patterns:
            for file_path in self.project_path.glob(f"**/{pattern}"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    results["files_scanned"] += 1
                    scan_result = self.scan_for_vulnerabilities(content, str(file_path.relative_to(self.project_path)))
                    
                    if scan_result["vulnerabilities_found"] > 0:
                        results["total_vulnerabilities"] += scan_result["vulnerabilities_found"]
                        results["findings"].extend(scan_result["findings"])
                        
                        # Update vulnerability counts by type
                        for finding in scan_result["findings"]:
                            vuln_type = finding["type"]
                            if vuln_type not in results["vulnerabilities_by_type"]:
                                results["vulnerabilities_by_type"][vuln_type] = 0
                            results["vulnerabilities_by_type"][vuln_type] += 1
                except Exception:
                    # Skip files that can't be read
                    continue
        
        return results
    
    def check_security_policy(self, policy_name: str, project_data: Dict) -> Dict:
        """Check compliance with a specific security policy."""
        if policy_name not in self.policies:
            return {
                "policy": policy_name,
                "valid": False,
                "error": f"Unknown security policy: {policy_name}"
            }
        
        policy = self.policies[policy_name]
        results = {
            "policy": policy_name,
            "name": policy["name"],
            "compliant": True,
            "violations": [],
            "recommendations": []
        }
        
        # Check each rule in the policy
        for rule in policy["rules"]:
            rule_result = self._check_security_rule(rule, project_data)
            if not rule_result["compliant"]:
                results["compliant"] = False
                results["violations"].extend(rule_result["violations"])
                results["recommendations"].extend(rule_result["recommendations"])
        
        return results
    
    def _check_security_rule(self, rule: str, project_data: Dict) -> Dict:
        """Check a specific security rule."""
        violations = []
        recommendations = []
        
        if rule == "no_hardcoded_secrets":
            # Check for hardcoded secrets in specifications and code
            if "specs" in project_data:
                for spec in project_data["specs"]:
                    # This is a simplified check - in reality, we would scan actual files
                    violations.append("Manual check required for hardcoded secrets")
                    recommendations.append("Scan all code files for hardcoded secrets")
        
        elif rule == "input_validation":
            # Check for input validation in specifications
            if "specs" in project_data:
                for spec in project_data["specs"]:
                    if "input_validation" not in spec:
                        violations.append("Input validation not explicitly specified")
                        recommendations.append("Add input validation requirements to specifications")
        
        elif rule == "authentication_required":
            # Check for authentication requirements
            if "specs" in project_data:
                for spec in project_data["specs"]:
                    if "authentication" not in spec:
                        violations.append("Authentication requirements not specified")
                        recommendations.append("Specify authentication requirements in specifications")
        
        else:
            # For other rules, we'll provide generic guidance
            violations.append(f"Manual verification required for: {rule}")
            recommendations.append(f"Review {rule} compliance manually")
        
        return {
            "rule": rule,
            "compliant": len(violations) == 0,
            "violations": violations,
            "recommendations": recommendations
        }
    
    def check_all_policies(self, project_data: Dict) -> Dict[str, Any]:
        """Check compliance with all security policies."""
        results: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "project": str(self.project_path),
            "policies": {},
            "overall_compliant": True
        }
        
        for policy_name, policy in self.policies.items():
            policy_result = self.check_security_policy(policy_name, project_data)
            results["policies"][policy_name] = policy_result
            
            if not policy_result["compliant"]:
                results["overall_compliant"] = False
        
        return results
    
    def generate_security_report(self, project_data: Dict) -> str:
        """Generate a security report in markdown format."""
        policy_results = self.check_all_policies(project_data)
        vulnerability_results = self.scan_project_for_vulnerabilities()
        
        report = "# Security Report\n\n"
        report += f"Generated: {policy_results['timestamp']}\n\n"
        report += f"Project: {policy_results['project']}\n\n"
        
        # Policy compliance section
        report += "## Policy Compliance\n\n"
        
        if policy_results["overall_compliant"]:
            report += "Overall Status: ✅ COMPLIANT\n\n"
        else:
            report += "Overall Status: ❌ NON-COMPLIANT\n\n"
        
        for policy_name, policy_result in policy_results["policies"].items():
            report += f"### {policy_result['name']}\n\n"
            
            if policy_result["compliant"]:
                report += "Status: ✅ COMPLIANT\n\n"
            else:
                report += "Status: ❌ NON-COMPLIANT\n\n"
                if policy_result["violations"]:
                    report += "Violations:\n"
                    for violation in policy_result["violations"]:
                        report += f"- {violation}\n"
                    report += "\n"
                
                if policy_result["recommendations"]:
                    report += "Recommendations:\n"
                    for recommendation in policy_result["recommendations"]:
                        report += f"- {recommendation}\n"
                    report += "\n"
        
        # Vulnerability scan section
        report += "## Vulnerability Scan\n\n"
        report += f"Files Scanned: {vulnerability_results['files_scanned']}\n\n"
        report += f"Total Vulnerabilities Found: {vulnerability_results['total_vulnerabilities']}\n\n"
        
        if vulnerability_results["total_vulnerabilities"] > 0:
            report += "Vulnerabilities by Type:\n"
            for vuln_type, count in vulnerability_results["vulnerabilities_by_type"].items():
                report += f"- {vuln_type}: {count}\n"
            report += "\n"
            
            report += "Detailed Findings:\n"
            for finding in vulnerability_results["findings"]:
                report += f"- {finding['type']} in {finding['file']} at line {finding['line']}: {finding['match']}\n"
        else:
            report += "No vulnerabilities found in scanned files.\n\n"
        
        return report

# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    manager = SecurityManager(Path("."))
    print("SecurityManager initialized")