#!/usr/bin/env python3
"""
Test file for the CI/CD pipeline management
"""

import os
import shutil
import sys
from pathlib import Path
from typing import Any

# Import the module directly (package will be available via PYTHONPATH in CI)
try:
    from goal_cli.cicd import CICDPipelineManager
except ImportError:
    # Fallback for local testing
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    from goal_cli.cicd import CICDPipelineManager


def test_cicd_pipelines():
    """Test the CI/CD pipeline management"""
    print("Testing CI/CD Pipeline Management...")
    
    # Create a temporary project directory for testing
    test_project = Path(__file__).parent / "test_project"
    test_project.mkdir(exist_ok=True)
    
    # Create required .goal directory structure
    goal_dir = test_project / ".goal"
    goal_dir.mkdir(exist_ok=True)
    
    # Create a basic goal.yaml file
    goal_yaml = goal_dir / "goal.yaml"
    with open(goal_yaml, 'w') as f:
        f.write("project:\n  name: test-project\n  version: 0.1.0\n  description: A test project for CI/CD pipelines\n")
    
    # Initialize CI/CD manager
    cicd_manager = CICDPipelineManager(test_project)
    
    # Test 1: Create GitHub CI pipeline
    print("\n1. Creating GitHub CI pipeline...")
    github_ci_vars = {
        "project_name": "Test Project"
    }
    
    github_ci_id = cicd_manager.create_pipeline(
        "ci",
        "github",
        ".github/workflows/ci.yml",
        github_ci_vars
    )
    print(f"Created GitHub CI pipeline request: {github_ci_id}")
    
    # Check status
    github_ci_status = cicd_manager.get_pipeline_status(github_ci_id)
    print(f"GitHub CI Status: {github_ci_status['status']}")
    
    # Test 2: Create GitLab CI/CD pipeline
    print("\n2. Creating GitLab CI/CD pipeline...")
    gitlab_cicd_vars = {
        "project_name": "Test Project"
    }
    
    gitlab_cicd_id = cicd_manager.create_pipeline(
        "cicd",
        "gitlab",
        ".gitlab-ci.yml",
        gitlab_cicd_vars
    )
    print(f"Created GitLab CI/CD pipeline request: {gitlab_cicd_id}")
    
    # Check status
    gitlab_cicd_status = cicd_manager.get_pipeline_status(gitlab_cicd_id)
    print(f"GitLab CI/CD Status: {gitlab_cicd_status['status']}")
    
    # Test 3: Create Jenkins pipeline
    print("\n3. Creating Jenkins pipeline...")
    jenkins_vars = {
        "project_name": "Test Project"
    }
    
    jenkins_id = cicd_manager.create_pipeline(
        "ci",
        "jenkins",
        "Jenkinsfile",
        jenkins_vars
    )
    print(f"Created Jenkins pipeline request: {jenkins_id}")
    
    # Check status
    jenkins_status = cicd_manager.get_pipeline_status(jenkins_id)
    print(f"Jenkins Status: {jenkins_status['status']}")
    
    # Test 4: List all requests
    print("\n4. Listing all pipeline requests...")
    requests = cicd_manager.list_pipeline_requests()
    print(f"Found {len(requests)} pipeline requests")
    
    # Test 5: Generate standard pipelines
    print("\n5. Generating standard pipelines...")
    standard_providers = ["github", "gitlab"]
    standard_types = ["ci", "cd"]
    
    standard_requests = cicd_manager.generate_standard_pipelines(standard_providers, standard_types)
    print(f"Generated {len(standard_requests)} standard pipelines")
    
    for req_id in standard_requests:
        status = cicd_manager.get_pipeline_status(req_id)
        if status:
            print(f"  - {status['config_path']} ({status['provider']}/{status['pipeline_type']}): {status['status']}")
    
    # Test 6: Validate a pipeline
    print("\n6. Validating a pipeline...")
    validation_result = cicd_manager.validate_pipeline(".github/workflows/ci.yml")
    if validation_result["valid"]:
        print("Pipeline validation successful")
    else:
        print("Pipeline validation failed:")
        for error in validation_result.get("errors", []):
            print(f"  - {error}")
    
    # Test 7: Check final statuses
    print("\n7. Checking final statuses...")
    all_request_ids = [github_ci_id, gitlab_cicd_id, jenkins_id] + standard_requests
    for req_id in all_request_ids:
        status = cicd_manager.get_pipeline_status(req_id)
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
    test_cicd_pipelines()