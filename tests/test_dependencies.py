#!/usr/bin/env python3
"""
Test file for the intelligent dependency management
"""

import os
import shutil
import sys
from pathlib import Path
from typing import Any

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from goal_cli.dependencies import DependencyManager


def test_dependency_management():
    """Test the intelligent dependency management"""
    print("Testing Intelligent Dependency Management...")
    
    # Create a temporary project directory for testing
    test_project = Path(__file__).parent / "test_project"
    test_project.mkdir(exist_ok=True)
    
    # Create required .goal directory structure
    goal_dir = test_project / ".goal"
    goal_dir.mkdir(exist_ok=True)
    
    # Create a basic goal.yaml file
    goal_yaml = goal_dir / "goal.yaml"
    with open(goal_yaml, 'w') as f:
        f.write("project:\n  name: test-project\n  version: 0.1.0\n  description: A test project for dependency management\n")
    
    # Create a requirements.txt file for testing
    requirements_txt = test_project / "requirements.txt"
    with open(requirements_txt, 'w') as f:
        f.write("# Test requirements\nrequests==2.28.1\npyyaml==6.0\ntyper==0.9.0\n")
    
    # Initialize dependency manager
    dep_manager = DependencyManager(test_project)
    
    # Test 1: Analyze dependencies
    print("\n1. Analyzing dependencies...")
    analyze_id = dep_manager.analyze_dependencies("project")
    print(f"Created analysis request: {analyze_id}")
    
    # Check status
    analyze_status = dep_manager.get_dependency_status(analyze_id)
    print(f"Analysis Status: {analyze_status['status']}")
    
    # Test 2: Update dependencies
    print("\n2. Updating dependencies...")
    update_id = dep_manager.update_dependencies("project", "safe")
    print(f"Created update request: {update_id}")
    
    # Check status
    update_status = dep_manager.get_dependency_status(update_id)
    print(f"Update Status: {update_status['status']}")
    
    # Test 3: Resolve conflicts
    print("\n3. Resolving conflicts...")
    resolve_id = dep_manager.resolve_conflicts("project")
    print(f"Created resolution request: {resolve_id}")
    
    # Check status
    resolve_status = dep_manager.get_dependency_status(resolve_id)
    print(f"Resolution Status: {resolve_status['status']}")
    
    # Test 4: Audit dependencies
    print("\n4. Auditing dependencies...")
    audit_id = dep_manager.audit_dependencies("project")
    print(f"Created audit request: {audit_id}")
    
    # Check status
    audit_status = dep_manager.get_dependency_status(audit_id)
    print(f"Audit Status: {audit_status['status']}")
    
    # Test 5: List all requests
    print("\n5. Listing all dependency requests...")
    requests = dep_manager.list_dependency_requests()
    print(f"Found {len(requests)} dependency requests")
    
    # Test 6: Show current dependencies
    print("\n6. Showing current dependencies...")
    dependencies = dep_manager.get_project_dependencies()
    print(f"Found {len(dependencies)} dependencies")
    for dep in dependencies:
        print(f"  - {dep['name']} ({dep['version']}) from {dep['source']}")
    
    # Test 7: Generate dependency report
    print("\n7. Generating dependency report...")
    report_content = dep_manager.generate_dependency_report()
    print(f"Generated report with {len(report_content)} characters")
    
    # Test 8: Check final statuses
    print("\n8. Checking final statuses...")
    all_request_ids = [analyze_id, update_id, resolve_id, audit_id]
    for req_id in all_request_ids:
        status = dep_manager.get_dependency_status(req_id)
        if status:
            print(f"  - {req_id[:8]}: {status['status']}")
    
    # Clean up test project and generated files
    shutil.rmtree(test_project, ignore_errors=True)
    
    # Clean up any generated automation files
    automation_files = list(Path(__file__).parent.glob("test_project_*"))
    for f in automation_files:
        if f.is_dir():
            shutil.rmtree(f, ignore_errors=True)
    
    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    test_dependency_management()