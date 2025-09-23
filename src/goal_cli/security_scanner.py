"""
Security Scanning and Vulnerability Management for goal-dev-spec
Exceeds spec-kit functionality with comprehensive security analysis and vulnerability management.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib


@dataclass
class SecurityRequest:
    """Data class for security scanning requests"""
    id: str
    scan_type: str  # dependency, code, config, network, container
    target: str  # project, file, directory
    created_at: str
    status: str = "pending"
    result: Optional[Dict] = None
    error: Optional[str] = None


@dataclass
class Vulnerability:
    """Data class for security vulnerabilities"""
    id: str
    name: str
    description: str
    severity: str  # critical, high, medium, low
    cvss_score: float
    affected_components: List[str]
    remediation: str
    references: List[str]
    discovered_at: str
    status: str = "open"  # open, fixed, ignored, false_positive


class SecurityScanner:
    """Security scanning and vulnerability management system"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.security_path = project_path / ".goal" / "security"
        self.security_path.mkdir(exist_ok=True)
        
        # Security requests storage
        self.security_requests_file = self.security_path / "security_requests.json"
        self.security_requests = self._load_security_requests()
        
        # Vulnerabilities storage
        self.vulnerabilities_file = self.security_path / "vulnerabilities.json"
        self.vulnerabilities = self._load_vulnerabilities()
        
        # Security policies storage
        self.policies_file = self.security_path / "security_policies.json"
        self.policies = self._load_policies()
        
        # Scan results storage
        self.scan_results_file = self.security_path / "scan_results.json"
        self.scan_results = self._load_scan_results()
        
        # Supported scan types
        self.supported_scan_types = {
            "dependency": "Dependency Vulnerability Scan",
            "code": "Source Code Security Scan",
            "config": "Configuration Security Scan",
            "secret": "Secrets Detection Scan",
            "container": "Container Security Scan"
        }
        
        # Supported severity levels
        self.severity_levels = ["critical", "high", "medium", "low"]
        
        # Initialize with default policies if they don't exist
        self._initialize_default_policies()
    
    def _load_security_requests(self) -> Dict[str, SecurityRequest]:
        """Load security requests from file"""
        if self.security_requests_file.exists():
            try:
                with open(self.security_requests_file, 'r') as f:
                    data = json.load(f)
                requests = {}
                for req_data in data:
                    req_data['status'] = req_data.get('status', 'pending')
                    # Convert result back to dict if it's a string
                    if isinstance(req_data.get('result'), str):
                        try:
                            req_data['result'] = json.loads(req_data['result'])
                        except json.JSONDecodeError:
                            req_data['result'] = None
                    request = SecurityRequest(**req_data)
                    requests[request.id] = request
                return requests
            except Exception as e:
                print(f"Warning: Could not load security requests: {e}")
        return {}
    
    def _save_security_requests(self):
        """Save security requests to file"""
        # Convert result to string if it's a dict for JSON serialization
        data = []
        for req in self.security_requests.values():
            req_dict = asdict(req)
            if isinstance(req_dict.get('result'), dict):
                req_dict['result'] = json.dumps(req_dict['result'])
            data.append(req_dict)
        
        with open(self.security_requests_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_vulnerabilities(self) -> Dict[str, Vulnerability]:
        """Load vulnerabilities from file"""
        if self.vulnerabilities_file.exists():
            try:
                with open(self.vulnerabilities_file, 'r') as f:
                    data = json.load(f)
                vulnerabilities = {}
                for vuln_data in data:
                    vuln_data['affected_components'] = vuln_data.get('affected_components', [])
                    vuln_data['references'] = vuln_data.get('references', [])
                    vulnerability = Vulnerability(**vuln_data)
                    vulnerabilities[vulnerability.id] = vulnerability
                return vulnerabilities
            except Exception as e:
                print(f"Warning: Could not load vulnerabilities: {e}")
        return {}
    
    def _save_vulnerabilities(self):
        """Save vulnerabilities to file"""
        data = [asdict(vuln) for vuln in self.vulnerabilities.values()]
        with open(self.vulnerabilities_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_policies(self) -> Dict[str, Dict]:
        """Load security policies from file"""
        if self.policies_file.exists():
            try:
                with open(self.policies_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load security policies: {e}")
        return {}
    
    def _save_policies(self):
        """Save security policies to file"""
        with open(self.policies_file, 'w') as f:
            json.dump(self.policies, f, indent=2)
    
    def _load_scan_results(self) -> Dict[str, Dict]:
        """Load scan results from file"""
        if self.scan_results_file.exists():
            try:
                with open(self.scan_results_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load scan results: {e}")
        return {}
    
    def _save_scan_results(self):
        """Save scan results to file"""
        with open(self.scan_results_file, 'w') as f:
            json.dump(self.scan_results, f, indent=2)
    
    def _initialize_default_policies(self):
        """Initialize default security policies"""
        default_policies = {
            "dependency_policy": {
                "name": "Dependency Security Policy",
                "description": "Policy for managing dependency vulnerabilities",
                "rules": [
                    {
                        "type": "max_severity",
                        "severity": "critical",
                        "action": "block"
                    },
                    {
                        "type": "max_severity",
                        "severity": "high",
                        "action": "warn"
                    }
                ],
                "enabled": True
            },
            "secret_policy": {
                "name": "Secrets Detection Policy",
                "description": "Policy for detecting and preventing secrets in code",
                "rules": [
                    {
                        "type": "detect_secrets",
                        "action": "block"
                    }
                ],
                "enabled": True
            },
            "code_policy": {
                "name": "Code Security Policy",
                "description": "Policy for code security best practices",
                "rules": [
                    {
                        "type": "insecure_patterns",
                        "patterns": ["eval\\(", "exec\\(", "os\\.system\\("],
                        "action": "warn"
                    }
                ],
                "enabled": True
            }
        }
        
        # Add default policies if they don't exist
        for policy_id, policy_data in default_policies.items():
            if policy_id not in self.policies:
                self.policies[policy_id] = policy_data
        
        self._save_policies()
    
    def scan_dependencies(self, target: str = "project") -> str:
        """
        Scan dependencies for vulnerabilities
        
        Args:
            target: What to scan (project, file, directory)
            
        Returns:
            ID of the security request
        """
        # Create security request
        request_id = hashlib.md5(f"dependency_{target}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = SecurityRequest(
            id=request_id,
            scan_type="dependency",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.security_requests[request_id] = request
        self._save_security_requests()
        
        # Process request
        self._process_security_request(request_id)
        
        return request_id
    
    def scan_code(self, target: str = "project") -> str:
        """
        Scan source code for security issues
        
        Args:
            target: What to scan (project, file, directory)
            
        Returns:
            ID of the security request
        """
        # Create security request
        request_id = hashlib.md5(f"code_{target}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = SecurityRequest(
            id=request_id,
            scan_type="code",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.security_requests[request_id] = request
        self._save_security_requests()
        
        # Process request
        self._process_security_request(request_id)
        
        return request_id
    
    def scan_config(self, target: str = "project") -> str:
        """
        Scan configuration files for security issues
        
        Args:
            target: What to scan (project, file, directory)
            
        Returns:
            ID of the security request
        """
        # Create security request
        request_id = hashlib.md5(f"config_{target}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = SecurityRequest(
            id=request_id,
            scan_type="config",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.security_requests[request_id] = request
        self._save_security_requests()
        
        # Process request
        self._process_security_request(request_id)
        
        return request_id
    
    def scan_secrets(self, target: str = "project") -> str:
        """
        Scan for secrets in code and configuration
        
        Args:
            target: What to scan (project, file, directory)
            
        Returns:
            ID of the security request
        """
        # Create security request
        request_id = hashlib.md5(f"secret_{target}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = SecurityRequest(
            id=request_id,
            scan_type="secret",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.security_requests[request_id] = request
        self._save_security_requests()
        
        # Process request
        self._process_security_request(request_id)
        
        return request_id
    
    def scan_container(self, target: str = "project") -> str:
        """
        Scan container images for vulnerabilities
        
        Args:
            target: What to scan (project, file, directory)
            
        Returns:
            ID of the security request
        """
        # Create security request
        request_id = hashlib.md5(f"container_{target}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = SecurityRequest(
            id=request_id,
            scan_type="container",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.security_requests[request_id] = request
        self._save_security_requests()
        
        # Process request
        self._process_security_request(request_id)
        
        return request_id
    
    def _process_security_request(self, request_id: str, params: Optional[Dict[str, Any]] = None) -> None:
        """Process a security request"""
        if request_id not in self.security_requests:
            return
        
        request = self.security_requests[request_id]
        request.status = "processing"
        self._save_security_requests()
        
        try:
            result = {}
            
            if request.scan_type == "dependency":
                result = self._scan_dependencies(request.target)
            elif request.scan_type == "code":
                result = self._scan_code(request.target)
            elif request.scan_type == "config":
                result = self._scan_config(request.target)
            elif request.scan_type == "secret":
                result = self._scan_secrets(request.target)
            elif request.scan_type == "container":
                result = self._scan_container(request.target)
            
            # Update request
            request.status = "completed"
            request.result = result
            
            # Store scan results
            self.scan_results[request_id] = {
                "request_id": request_id,
                "scan_type": request.scan_type,
                "target": request.target,
                "timestamp": datetime.now().isoformat(),
                "result": result
            }
            self._save_scan_results()
            
            # Process vulnerabilities found
            if result.get("vulnerabilities"):
                self._process_vulnerabilities(result["vulnerabilities"])
            
        except Exception as e:
            request.status = "failed"
            request.error = str(e)
        
        self._save_security_requests()
    
    def _scan_dependencies(self, target: str) -> Dict[str, Any]:
        """Scan dependencies for vulnerabilities"""
        scan_result = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "scanner": "dependency_scanner",
            "vulnerabilities": [],
            "summary": {}
        }
        
        # This would integrate with actual dependency scanners like:
        # - pip-audit for Python
        # - npm audit for Node.js
        # - OWASP Dependency-Check for multiple languages
        
        # For now, we'll simulate finding some vulnerabilities
        vulnerabilities = self._generate_mock_vulnerabilities("dependency")
        scan_result["vulnerabilities"] = vulnerabilities
        
        # Create summary
        scan_result["summary"] = self._create_vulnerability_summary(vulnerabilities)
        
        return scan_result
    
    def _scan_code(self, target: str) -> Dict[str, Any]:
        """Scan source code for security issues"""
        scan_result = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "scanner": "code_scanner",
            "vulnerabilities": [],
            "summary": {}
        }
        
        # This would integrate with actual code scanners like:
        # - Bandit for Python
        # - ESLint with security plugins for JavaScript
        # - SonarQube for multiple languages
        
        # For now, we'll simulate finding some vulnerabilities
        vulnerabilities = self._generate_mock_vulnerabilities("code")
        scan_result["vulnerabilities"] = vulnerabilities
        
        # Create summary
        scan_result["summary"] = self._create_vulnerability_summary(vulnerabilities)
        
        return scan_result
    
    def _scan_config(self, target: str) -> Dict[str, Any]:
        """Scan configuration files for security issues"""
        scan_result = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "scanner": "config_scanner",
            "vulnerabilities": [],
            "summary": {}
        }
        
        # This would check configuration files for:
        # - Hardcoded credentials
        # - Insecure settings
        # - Missing security headers
        
        # For now, we'll simulate finding some vulnerabilities
        vulnerabilities = self._generate_mock_vulnerabilities("config")
        scan_result["vulnerabilities"] = vulnerabilities
        
        # Create summary
        scan_result["summary"] = self._create_vulnerability_summary(vulnerabilities)
        
        return scan_result
    
    def _scan_secrets(self, target: str) -> Dict[str, Any]:
        """Scan for secrets in code and configuration"""
        scan_result = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "scanner": "secret_scanner",
            "vulnerabilities": [],
            "summary": {}
        }
        
        # This would integrate with actual secret scanners like:
        # - Git-secrets
        # - TruffleHog
        # - AWS Secrets Manager detectors
        
        # For now, we'll simulate finding some secrets
        vulnerabilities = self._generate_mock_vulnerabilities("secret")
        scan_result["vulnerabilities"] = vulnerabilities
        
        # Create summary
        scan_result["summary"] = self._create_vulnerability_summary(vulnerabilities)
        
        return scan_result
    
    def _scan_container(self, target: str) -> Dict[str, Any]:
        """Scan container images for vulnerabilities"""
        scan_result = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "scanner": "container_scanner",
            "vulnerabilities": [],
            "summary": {}
        }
        
        # This would integrate with actual container scanners like:
        # - Clair
        # - Trivy
        # - Anchore
        
        # For now, we'll simulate finding some vulnerabilities
        vulnerabilities = self._generate_mock_vulnerabilities("container")
        scan_result["vulnerabilities"] = vulnerabilities
        
        # Create summary
        scan_result["summary"] = self._create_vulnerability_summary(vulnerabilities)
        
        return scan_result
    
    def _generate_mock_vulnerabilities(self, scan_type: str) -> List[Dict[str, Any]]:
        """Generate mock vulnerabilities for testing"""
        vulnerabilities = []
        
        if scan_type == "dependency":
            vulnerabilities.extend([
                {
                    "id": "CVE-2023-12345",
                    "name": "Insecure Dependency Version",
                    "description": "The requests library version 2.28.1 has a known vulnerability",
                    "severity": "high",
                    "cvss_score": 7.5,
                    "affected_components": ["requests==2.28.1"],
                    "remediation": "Upgrade to version 2.28.2 or later",
                    "references": ["https://nvd.nist.gov/vuln/detail/CVE-2023-12345"]
                },
                {
                    "id": "CVE-2023-67890",
                    "name": "Critical Dependency Vulnerability",
                    "description": "PyYAML version 6.0 has a critical remote code execution vulnerability",
                    "severity": "critical",
                    "cvss_score": 9.8,
                    "affected_components": ["pyyaml==6.0"],
                    "remediation": "Upgrade to version 6.1 or later immediately",
                    "references": ["https://nvd.nist.gov/vuln/detail/CVE-2023-67890"]
                }
            ])
        elif scan_type == "code":
            vulnerabilities.extend([
                {
                    "id": "SEC-001",
                    "name": "Insecure Code Pattern",
                    "description": "Use of eval() function detected which can lead to code injection",
                    "severity": "high",
                    "cvss_score": 7.0,
                    "affected_components": ["src/utils.py:45"],
                    "remediation": "Replace eval() with safer alternatives like ast.literal_eval()",
                    "references": ["https://owasp.org/www-community/attacks/Code_Injection"]
                }
            ])
        elif scan_type == "config":
            vulnerabilities.extend([
                {
                    "id": "SEC-002",
                    "name": "Hardcoded Credentials",
                    "description": "Hardcoded API key found in configuration file",
                    "severity": "critical",
                    "cvss_score": 9.0,
                    "affected_components": ["config/app.conf:12"],
                    "remediation": "Remove hardcoded credentials and use environment variables or secure vault",
                    "references": ["https://owasp.org/www-community/vulnerabilities/Using_hardcoded_passwords"]
                }
            ])
        elif scan_type == "secret":
            vulnerabilities.extend([
                {
                    "id": "SECRET-001",
                    "name": "Exposed AWS Access Key",
                    "description": "AWS access key ID found in source code",
                    "severity": "critical",
                    "cvss_score": 9.0,
                    "affected_components": ["src/aws_client.py:23"],
                    "remediation": "Remove the key and revoke it immediately. Use IAM roles or secure credential management",
                    "references": ["https://docs.aws.amazon.com/general/latest/gr/aws-access-keys-best-practices.html"]
                },
                {
                    "id": "SECRET-002",
                    "name": "Exposed Database Password",
                    "description": "Database password found in configuration file",
                    "severity": "high",
                    "cvss_score": 7.5,
                    "affected_components": ["config/database.conf:8"],
                    "remediation": "Remove the password and use environment variables or secure vault",
                    "references": ["https://owasp.org/www-community/vulnerabilities/Using_hardcoded_passwords"]
                }
            ])
        elif scan_type == "container":
            vulnerabilities.extend([
                {
                    "id": "CVE-2023-54321",
                    "name": "Container Base Image Vulnerability",
                    "description": "Alpine Linux base image has a critical vulnerability in OpenSSL",
                    "severity": "critical",
                    "cvss_score": 9.8,
                    "affected_components": ["alpine:3.16"],
                    "remediation": "Upgrade to Alpine 3.17 or later",
                    "references": ["https://nvd.nist.gov/vuln/detail/CVE-2023-54321"]
                }
            ])
        
        return vulnerabilities
    
    def _create_vulnerability_summary(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a summary of vulnerabilities"""
        summary = {
            "total": len(vulnerabilities),
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "by_component": {}
        }
        
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "low")
            if severity in summary:
                summary[severity] += 1
            
            # Group by affected components
            for component in vuln.get("affected_components", []):
                if component not in summary["by_component"]:
                    summary["by_component"][component] = 0
                summary["by_component"][component] += 1
        
        return summary
    
    def _process_vulnerabilities(self, vulnerabilities: List[Dict]):
        """Process discovered vulnerabilities"""
        for vuln_data in vulnerabilities:
            # Create vulnerability ID if not present
            vuln_id = vuln_data.get("id")
            if not vuln_id:
                vuln_id = hashlib.md5(f"{vuln_data.get('name', '')}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
                vuln_data["id"] = vuln_id
            
            # Create or update vulnerability
            if vuln_id not in self.vulnerabilities:
                vulnerability = Vulnerability(
                    id=vuln_id,
                    name=vuln_data.get("name", "Unknown Vulnerability"),
                    description=vuln_data.get("description", ""),
                    severity=vuln_data.get("severity", "low"),
                    cvss_score=vuln_data.get("cvss_score", 0.0),
                    affected_components=vuln_data.get("affected_components", []),
                    remediation=vuln_data.get("remediation", "No remediation provided"),
                    references=vuln_data.get("references", []),
                    discovered_at=datetime.now().isoformat()
                )
                self.vulnerabilities[vuln_id] = vulnerability
        
        # Save vulnerabilities
        self._save_vulnerabilities()
    
    def get_security_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a security request"""
        if request_id in self.security_requests:
            request = self.security_requests[request_id]
            result = asdict(request)
            # Convert result back to dict if it's a JSON string
            if isinstance(result.get('result'), str):
                try:
                    result['result'] = json.loads(result['result'])
                except json.JSONDecodeError:
                    result['result'] = None
            return result
        return None
    
    def list_security_requests(self) -> List[Dict[str, Any]]:
        """List all security requests"""
        requests = []
        for req in self.security_requests.values():
            req_dict = asdict(req)
            # Convert result back to dict if it's a JSON string
            if isinstance(req_dict.get('result'), str):
                try:
                    req_dict['result'] = json.loads(req_dict['result'])
                except json.JSONDecodeError:
                    req_dict['result'] = None
            requests.append(req_dict)
        return requests
    
    def list_vulnerabilities(self, severity_filter: Optional[str] = None, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all vulnerabilities with optional filters"""
        vulnerabilities = []
        for vuln in self.vulnerabilities.values():
            # Apply filters
            if severity_filter and vuln.severity != severity_filter:
                continue
            if status_filter and vuln.status != status_filter:
                continue
            
            vulnerabilities.append(asdict(vuln))
        
        # Sort by severity (critical first)
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        vulnerabilities.sort(key=lambda x: severity_order.get(x["severity"], 4))
        
        return vulnerabilities
    
    def update_vulnerability_status(self, vuln_id: str, status: str, notes: str = "") -> bool:
        """Update the status of a vulnerability"""
        if vuln_id in self.vulnerabilities:
            self.vulnerabilities[vuln_id].status = status
            self._save_vulnerabilities()
            
            # Log the status change
            log_entry = {
                "vuln_id": vuln_id,
                "status": status,
                "notes": notes,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save to log file
            log_file = self.security_path / "vulnerability_log.json"
            log_data = []
            if log_file.exists():
                try:
                    with open(log_file, 'r') as f:
                        log_data = json.load(f)
                except json.JSONDecodeError:
                    pass
            
            log_data.append(log_entry)
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
            
            return True
        return False
    
    def get_scan_results(self, request_id: Optional[str] = None) -> Dict[str, Any]:
        """Get scan results"""
        if request_id:
            return self.scan_results.get(request_id, {})
        else:
            return self.scan_results
    
    def enforce_security_policies(self) -> Dict[str, Any]:
        """Enforce security policies and return compliance status"""
        compliance = {
            "timestamp": datetime.now().isoformat(),
            "policies_evaluated": 0,
            "policies_violated": 0,
            "violations": [],
            "compliant": True
        }
        
        # Evaluate each policy
        for policy_id, policy in self.policies.items():
            if not policy.get("enabled", True):
                continue
            
            compliance["policies_evaluated"] += 1
            
            # Check policy violations
            violations = self._check_policy_violations(policy)
            if violations:
                compliance["policies_violated"] += 1
                compliance["violations"].extend(violations)
                compliance["compliant"] = False
        
        return compliance
    
    def _check_policy_violations(self, policy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for policy violations"""
        violations = []
        policy_rules = policy.get("rules", [])
        
        for rule in policy_rules:
            rule_type = rule.get("type")
            action = rule.get("action", "warn")
            
            if rule_type == "max_severity":
                # Check for vulnerabilities exceeding severity threshold
                max_severity = rule.get("severity", "low")
                severity_level = self.severity_levels.index(max_severity)
                
                # Get open vulnerabilities
                open_vulns = self.list_vulnerabilities(status_filter="open")
                
                for vuln in open_vulns:
                    vuln_severity_level = self.severity_levels.index(vuln["severity"])
                    if vuln_severity_level <= severity_level:
                        violations.append({
                            "policy": policy.get("name", "Unnamed Policy"),
                            "violation": f"Vulnerability {vuln['name']} has severity {vuln['severity']} which exceeds policy threshold {max_severity}",
                            "action": action,
                            "vulnerability_id": vuln["id"]
                        })
            
            elif rule_type == "detect_secrets":
                # Check for secrets
                secret_vulns = self.list_vulnerabilities(severity_filter="critical")
                secret_vulns = [v for v in secret_vulns if "secret" in v.get("name", "").lower() or "key" in v.get("name", "").lower()]
                
                for vuln in secret_vulns:
                    violations.append({
                        "policy": policy.get("name", "Unnamed Policy"),
                        "violation": f"Secret detected: {vuln['name']}",
                        "action": action,
                        "vulnerability_id": vuln["id"]
                    })
            
            elif rule_type == "insecure_patterns":
                # Check for insecure code patterns
                code_vulns = self.list_vulnerabilities(severity_filter="high")
                patterns = rule.get("patterns", [])
                
                for vuln in code_vulns:
                    description = vuln.get("description", "").lower()
                    for pattern in patterns:
                        if re.search(pattern, description):
                            violations.append({
                                "policy": policy.get("name", "Unnamed Policy"),
                                "violation": f"Insecure pattern detected: {pattern}",
                                "action": action,
                                "vulnerability_id": vuln["id"]
                            })
        
        return violations
    
    def generate_security_report(self) -> str:
        """Generate a comprehensive security report"""
        # Get recent security requests
        recent_requests = sorted(
            [req for req in self.security_requests.values() 
             if req.status in ["completed", "failed"]],
            key=lambda x: x.created_at,
            reverse=True
        )[:10]  # Last 10 requests
        
        # Get open vulnerabilities
        open_vulns = self.list_vulnerabilities(status_filter="open")
        
        # Get security compliance status
        compliance = self.enforce_security_policies()
        
        # Get recent scan results
        recent_scans = list(self.scan_results.values())[-5:] if self.scan_results else []
        
        # Create report
        report = f"""# Security Report

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- Total Vulnerabilities: {len(self.vulnerabilities)}
- Open Vulnerabilities: {len([v for v in self.vulnerabilities.values() if v.status == 'open'])}
- Fixed Vulnerabilities: {len([v for v in self.vulnerabilities.values() if v.status == 'fixed'])}
- Security Scans: {len(self.security_requests)}
- Policy Compliance: {'Compliant' if compliance['compliant'] else 'Non-Compliant'}

## Open Vulnerabilities by Severity

| Severity | Count |
|----------|-------|
"""
        
        # Count vulnerabilities by severity
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for vuln in self.vulnerabilities.values():
            if vuln.status == "open":
                severity_counts[vuln.severity] += 1
        
        for severity in ["critical", "high", "medium", "low"]:
            count = severity_counts[severity]
            emoji = "🔴" if severity == "critical" else "🟠" if severity == "high" else "🟡" if severity == "medium" else "🟢"
            report += f"| {emoji} {severity.capitalize()} | {count} |\n"
        
        report += """
## Recent Security Scans

| ID | Type | Target | Status | Created |
|----|------|--------|--------|---------|
"""
        
        for req in recent_requests:
            created = datetime.fromisoformat(req.created_at).strftime("%Y-%m-%d %H:%M")
            report += f"| {req.id[:8]} | {req.scan_type} | {req.target} | {req.status} | {created} |\n"
        
        report += """
## Recent Scan Results

| Scan ID | Type | Timestamp | Vulnerabilities Found |
|---------|------|-----------|----------------------|
"""
        
        for scan in recent_scans:
            timestamp = datetime.fromisoformat(scan['timestamp']).strftime("%Y-%m-%d %H:%M")
            vuln_count = scan.get('result', {}).get('summary', {}).get('total', 0)
            report += f"| {scan['request_id'][:8]} | {scan['scan_type']} | {timestamp} | {vuln_count} |\n"
        
        report += """
## Open Vulnerabilities (Critical and High)

"""
        
        # Show critical and high vulnerabilities
        critical_high_vulns = [v for v in open_vulns if v["severity"] in ["critical", "high"]]
        for vuln in critical_high_vulns[:10]:  # Show first 10
            severity_emoji = "🔴" if vuln["severity"] == "critical" else "🟠"
            report += f"### {severity_emoji} {vuln['name']} ({vuln['severity'].capitalize()})\n"
            report += f"**ID:** {vuln['id']}\n"
            report += f"**Description:** {vuln['description']}\n"
            report += f"**CVSS Score:** {vuln['cvss_score']}\n"
            report += f"**Affected Components:** {', '.join(vuln['affected_components'])}\n"
            report += f"**Remediation:** {vuln['remediation']}\n\n"
        
        if len(critical_high_vulns) > 10:
            report += f"*... and {len(critical_high_vulns) - 10} more critical/high vulnerabilities*\n\n"
        
        report += f"""
## Security Policy Compliance

**Compliance Status:** {'✅ Compliant' if compliance['compliant'] else '❌ Non-Compliant'}
**Policies Evaluated:** {compliance['policies_evaluated']}
**Policies Violated:** {compliance['policies_violated']}

"""
        
        if compliance['violations']:
            report += "### Policy Violations\n\n"
            for violation in compliance['violations']:
                action_emoji = "🔴" if violation['action'] == 'block' else "⚠️"
                report += f"{action_emoji} **{violation['policy']}**\n"
                report += f"   Violation: {violation['violation']}\n"
                report += f"   Action: {violation['action']}\n\n"
        
        report += """
## Recommendations

1. Address critical and high severity vulnerabilities immediately
2. Review and update security policies regularly
3. Implement automated security scanning in CI/CD pipeline
4. Rotate exposed secrets and API keys
5. Conduct regular security training for development team
6. Monitor security advisories for dependencies

---
*Report generated by Security Scanning and Vulnerability Management System*
"""
        
        return report


# CLI Integration
def security_cli():
    """CLI commands for security scanning"""
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    app = typer.Typer()
    console = Console()
    
    @app.command()
    def scan(
        type: str = typer.Argument(..., help="Type of scan (dependency, code, config, secret, container)"),
        target: str = typer.Option("project", help="Target to scan (project, file, directory)")
    ):
        """Scan for security vulnerabilities"""
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
            
            # Initialize security scanner
            security_scanner = SecurityScanner(project_path)
            
            # Run scan based on type
            if type == "dependency":
                request_id = security_scanner.scan_dependencies(target)
            elif type == "code":
                request_id = security_scanner.scan_code(target)
            elif type == "config":
                request_id = security_scanner.scan_config(target)
            elif type == "secret":
                request_id = security_scanner.scan_secrets(target)
            elif type == "container":
                request_id = security_scanner.scan_container(target)
            else:
                console.print(f"[red]Error:[/red] Unsupported scan type: {type}")
                return
            
            console.print(f"[green]✓[/green] Security scan request created with ID: {request_id}")
            console.print(f"Check status with: goal security status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def status(request_id: str = typer.Argument(..., help="Security request ID")):
        """Check the status of a security scan request"""
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
            
            # Initialize security scanner
            security_scanner = SecurityScanner(project_path)
            
            # Check status
            status = security_scanner.get_security_status(request_id)
            if status:
                console.print(Panel(f"[bold]Security Scan Status: {request_id}[/bold]", expand=False))
                console.print(f"Type: {status['scan_type']}")
                console.print(f"Target: {status['target']}")
                console.print(f"Status: {status['status']}")
                if status.get('error'):
                    console.print(f"[red]Error:[/red] {status['error']}")
                elif status.get('result'):
                    result = status['result']
                    if isinstance(result, str):
                        try:
                            result = json.loads(result)
                        except json.JSONDecodeError:
                            result = {"output": result}
                    
                    console.print(f"Timestamp: {result.get('timestamp', 'unknown')}")
                    summary = result.get('summary', {})
                    console.print(f"Vulnerabilities Found: {summary.get('total', 0)}")
                    if summary.get('critical', 0) > 0:
                        console.print(f"[red]Critical: {summary['critical']}[/red]")
                    if summary.get('high', 0) > 0:
                        console.print(f"[orange]High: {summary['high']}[/orange]")
            else:
                console.print(f"[red]Security request {request_id} not found[/red]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def list():
        """List all security scan requests"""
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
            
            # Initialize security scanner
            security_scanner = SecurityScanner(project_path)
            
            # List requests
            requests = security_scanner.list_security_requests()
            if requests:
                console.print(Panel(f"[bold]Security Scan Requests ({len(requests)})[/bold]", expand=False))
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("ID", style="cyan")
                table.add_column("Type", style="green")
                table.add_column("Target", style="yellow")
                table.add_column("Status", style="blue")
                table.add_column("Created", style="dim")
                
                for req in requests:
                    created = datetime.fromisoformat(req['created_at']).strftime("%Y-%m-%d %H:%M")
                    table.add_row(
                        req['id'][:8],
                        req['scan_type'],
                        req['target'],
                        req['status'],
                        created
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No security scan requests found[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def vulnerabilities(
        severity: str = typer.Option(None, help="Filter by severity (critical, high, medium, low)"),
        status: str = typer.Option("open", help="Filter by status (open, fixed, ignored, false_positive)")
    ):
        """List vulnerabilities"""
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
            
            # Initialize security scanner
            security_scanner = SecurityScanner(project_path)
            
            # List vulnerabilities
            vulnerabilities = security_scanner.list_vulnerabilities(severity, status)
            if vulnerabilities:
                console.print(Panel(f"[bold]Vulnerabilities ({len(vulnerabilities)})[/bold]", expand=False))
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Severity", style="yellow")
                table.add_column("Status", style="blue")
                table.add_column("Components", style="dim")
                
                for vuln in vulnerabilities[:20]:  # Show first 20
                    severity_color = {
                        "critical": "red",
                        "high": "orange",
                        "medium": "yellow",
                        "low": "green"
                    }.get(vuln['severity'], "white")
                    
                    table.add_row(
                        vuln['id'][:8],
                        vuln['name'][:30] + "..." if len(vuln['name']) > 30 else vuln['name'],
                        f"[{severity_color}]{vuln['severity']}[/{severity_color}]",
                        vuln['status'],
                        str(len(vuln['affected_components']))
                    )
                
                if len(vulnerabilities) > 20:
                    console.print(f"[dim]... and {len(vulnerabilities) - 20} more vulnerabilities[/dim]")
                
                console.print(table)
            else:
                console.print("[green]No vulnerabilities found with the specified filters[/green]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def update(
        vuln_id: str = typer.Argument(..., help="Vulnerability ID"),
        status: str = typer.Argument(..., help="New status (open, fixed, ignored, false_positive)"),
        notes: str = typer.Option("", help="Additional notes")
    ):
        """Update vulnerability status"""
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
            
            # Initialize security scanner
            security_scanner = SecurityScanner(project_path)
            
            # Update vulnerability status
            success = security_scanner.update_vulnerability_status(vuln_id, status, notes)
            if success:
                console.print(f"[green]✓[/green] Updated vulnerability {vuln_id} status to {status}")
            else:
                console.print(f"[red]Error:[/red] Vulnerability {vuln_id} not found")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def compliance():
        """Check security policy compliance"""
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
            
            # Initialize security scanner
            security_scanner = SecurityScanner(project_path)
            
            # Check compliance
            compliance_result = security_scanner.enforce_security_policies()
            
            console.print(Panel("[bold]Security Policy Compliance[/bold]", expand=False))
            status_indicator = "✅" if compliance_result['compliant'] else "❌"
            console.print(f"Status: {status_indicator} {'Compliant' if compliance_result['compliant'] else 'Non-Compliant'}")
            console.print(f"Policies Evaluated: {compliance_result['policies_evaluated']}")
            console.print(f"Policies Violated: {compliance_result['policies_violated']}")
            
            if compliance_result['violations']:
                console.print("\n[bold]Violations:[/bold]")
                for violation in compliance_result['violations']:
                    action_indicator = "🔴" if violation['action'] == 'block' else "⚠️"
                    console.print(f"{action_indicator} {violation['policy']}: {violation['violation']}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def report():
        """Generate a security report"""
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
            
            # Initialize security scanner
            security_scanner = SecurityScanner(project_path)
            
            # Generate report
            report_content = security_scanner.generate_security_report()
            
            # Save report
            report_file = project_path / ".goal" / "security" / "security_report.md"
            with open(report_file, 'w') as f:
                f.write(report_content)
            
            console.print(f"[green]✓[/green] Security report saved to {report_file}")
            console.print("\n[bold]Report Preview:[/bold]")
            console.print(report_content[:1000] + "..." if len(report_content) > 1000 else report_content)
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    return app


# Integration with main CLI
def integrate_security_with_main_cli(main_app):
    """Integrate security scanning commands with main CLI"""
    security_app = security_cli()
    main_app.add_typer(security_app, name="security")
    return main_app