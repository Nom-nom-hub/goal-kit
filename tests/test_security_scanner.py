#!/usr/bin/env python3
"""
Test file for the security scanning and vulnerability management system
"""

import sys
import os
import json
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from goal_cli.security_scanner import SecurityScanner


def test_security_scanning():
    """Test the security scanning and vulnerability management system"""
    print("Testing Security Scanning and Vulnerability Management System...")
    
    # Create a temporary project directory for testing
    test_project = Path(__file__).parent / "test_project"
    test_project.mkdir(exist_ok=True)
    
    # Create required .goal directory structure
    goal_dir = test_project / ".goal"
    goal_dir.mkdir(exist_ok=True)
    
    # Create a basic goal.yaml file
    goal_yaml = goal_dir / "goal.yaml"
    with open(goal_yaml, 'w') as f:
        f.write("project:\n  name: test-project\n  version: 0.1.0\n  description: A test project for security scanning\n")
    
    # Create some test files for scanning
    src_dir = test_project / "src"
    src_dir.mkdir(exist_ok=True)
    
    # Create a test Python file with potential security issues
    with open(src_dir / "test_app.py", 'w') as f:
        f.write('''"""Test application with potential security issues."""
import os
import yaml

def load_config(config_file):
    """Load configuration file."""
    # Security issue: Using unsafe yaml loading
    with open(config_file, 'r') as f:
        return yaml.load(f)  # Vulnerable to arbitrary code execution

def execute_command(cmd):
    """Execute system command."""
    # Security issue: Using os.system
    return os.system(cmd)  # Vulnerable to command injection

def main():
    """Main function."""
    config = load_config("config.yaml")
    print("Configuration loaded:", config)
    
    # This might be a hardcoded secret
    api_key = "AKIAIOSFODNN7EXAMPLE"  # AWS access key
    
    result = execute_command("echo 'Hello World'")
    print("Command result:", result)

if __name__ == "__main__":
    main()
''')
    
    # Create a test config file\n    with open(test_project / "config.yaml", 'w') as f:\n        f.write('# Test configuration\ndatabase:\n  host: localhost\n  port: 5432\n  password: "supersecretpassword"  # Hardcoded password\n')
    
    # Initialize security scanner
    security_scanner = SecurityScanner(test_project)
    
    # Test 1: List security policies
    print("\n1. Listing security policies...")
    policies = security_scanner.policies
    print(f"Found {len(policies)} security policies")
    for policy_id, policy in list(policies.items())[:3]:  # Show first 3
        print(f"  - {policy_id}: {policy.get('name', 'unnamed')}")
    
    # Test 2: Scan dependencies
    print("\n2. Scanning dependencies...")
    dep_scan_id = security_scanner.scan_dependencies("project")
    print(f"Created dependency scan request: {dep_scan_id}")
    
    # Check status
    dep_scan_status = security_scanner.get_security_status(dep_scan_id)
    print(f"Dependency Scan Status: {dep_scan_status['status']}")
    
    # Test 3: Scan code
    print("\n3. Scanning code...")
    code_scan_id = security_scanner.scan_code("src")
    print(f"Created code scan request: {code_scan_id}")
    
    # Check status
    code_scan_status = security_scanner.get_security_status(code_scan_id)
    print(f"Code Scan Status: {code_scan_status['status']}")
    
    # Test 4: Scan for secrets
    print("\n4. Scanning for secrets...")
    secret_scan_id = security_scanner.scan_secrets("project")
    print(f"Created secret scan request: {secret_scan_id}")
    
    # Check status
    secret_scan_status = security_scanner.get_security_status(secret_scan_id)
    print(f"Secret Scan Status: {secret_scan_status['status']}")
    
    # Test 5: Scan configuration
    print("\n5. Scanning configuration...")
    config_scan_id = security_scanner.scan_config("config.yaml")
    print(f"Created config scan request: {config_scan_id}")
    
    # Check status
    config_scan_status = security_scanner.get_security_status(config_scan_id)
    print(f"Config Scan Status: {config_scan_status['status']}")
    
    # Test 6: List all security requests
    print("\n6. Listing all security requests...")
    requests = security_scanner.list_security_requests()
    print(f"Found {len(requests)} security requests")
    
    # Test 7: List vulnerabilities
    print("\n7. Listing vulnerabilities...")
    vulnerabilities = security_scanner.list_vulnerabilities()
    print(f"Found {len(vulnerabilities)} vulnerabilities")
    for vuln in vulnerabilities[:3]:  # Show first 3
        print(f"  - {vuln['id'][:8]}: {vuln['name']} ({vuln['severity']})")
    
    # Test 8: Check security compliance
    print("\n8. Checking security compliance...")
    compliance = security_scanner.enforce_security_policies()
    print(f"Compliance Status: {'Compliant' if compliance['compliant'] else 'Non-Compliant'}")
    print(f"Policies Evaluated: {compliance['policies_evaluated']}")
    print(f"Policies Violated: {compliance['policies_violated']}")
    
    # Test 9: Get scan results
    print("\n9. Getting scan results...")
    scan_results = security_scanner.get_scan_results()
    print(f"Found {len(scan_results)} scan results")
    
    # Test 10: Generate security report
    print("\n10. Generating security report...")
    report_content = security_scanner.generate_security_report()
    print(f"Generated report with {len(report_content)} characters")
    
    # Test 11: Update vulnerability status
    print("\n11. Updating vulnerability status...")
    if vulnerabilities:
        first_vuln_id = vulnerabilities[0]['id']
        success = security_scanner.update_vulnerability_status(first_vuln_id, "fixed", "Fixed in latest update")
        print(f"Updated vulnerability status: {'Success' if success else 'Failed'}")
    
    # Test 12: Check final statuses
    print("\n12. Checking final statuses...")
    all_request_ids = [dep_scan_id, code_scan_id, secret_scan_id, config_scan_id]
    for req_id in all_request_ids:
        status = security_scanner.get_security_status(req_id)
        if status:
            print(f"  - {req_id[:8]}: {status['status']}")
            if status.get('result'):
                result = status['result']
                if isinstance(result, str):
                    try:
                        result = json.loads(result)
                    except:
                        result = {"output": result}
                summary = result.get('summary', {})
                print(f"    Vulnerabilities Found: {summary.get('total', 0)}")
    
    # Clean up test project and generated files
    import shutil
    shutil.rmtree(test_project, ignore_errors=True)
    
    # Clean up any generated automation files
    automation_files = list(Path(__file__).parent.glob("test_project_*"))
    for f in automation_files:
        if f.is_dir():
            shutil.rmtree(f, ignore_errors=True)
    
    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    test_security_scanning()