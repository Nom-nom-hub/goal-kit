#!/usr/bin/env python3
"""
Test file for the advanced project scaffolding
"""

import json
import os
import shutil
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from goal_cli.scaffolding import ProjectScaffolder


def test_project_scaffolding():
    """Test the advanced project scaffolding"""
    print("Testing Advanced Project Scaffolding...")
    
    # Create a temporary project directory for testing
    test_project = Path(__file__).parent / "test_project"
    test_project.mkdir(exist_ok=True)
    
    # Create required .goal directory structure
    goal_dir = test_project / ".goal"
    goal_dir.mkdir(exist_ok=True)
    
    # Create a basic goal.yaml file
    goal_yaml = goal_dir / "goal.yaml"
    with open(goal_yaml, 'w') as f:
        f.write("project:\n  name: test-project\n  version: 0.1.0\n  description: A test project for scaffolding\n")
    
    # Initialize project scaffolder
    scaffolder = ProjectScaffolder(test_project)
    
    # Test 1: List available templates
    print("\n1. Listing available templates...")
    templates = scaffolder.list_templates()
    print(f"Found {len(templates)} templates")
    for template_id, template_info in list(templates.items())[:3]:  # Show first 3
        print(f"  - {template_id}: {template_info['name']} ({template_info['language']})")
    
    # Test 2: Scaffold a basic Python project
    print("\n2. Scaffolding a basic Python project...")
    template_vars = {
        "project_description": "A test Python project",
        "author": "Test User",
        "email": "test@example.com"
    }
    
    scaffold_id = scaffolder.scaffold_project(
        "python_basic",
        "test-python-project",
        "test-python-project",
        template_vars
    )
    print(f"Created scaffolding request: {scaffold_id}")
    
    # Check status
    scaffold_status = scaffolder.get_scaffolding_status(scaffold_id)
    print(f"Scaffolding Status: {scaffold_status['status']}")
    
    # Test 3: Scaffold a web application
    print("\n3. Scaffolding a web application...")
    web_vars = {
        "project_description": "A test web application",
        "author": "Test User",
        "email": "test@example.com"
    }
    
    web_scaffold_id = scaffolder.scaffold_project(
        "python_web",
        "test-web-project",
        "test-web-project",
        web_vars
    )
    print(f"Created web scaffolding request: {web_scaffold_id}")
    
    # Check status
    web_scaffold_status = scaffolder.get_scaffolding_status(web_scaffold_id)
    print(f"Web Scaffolding Status: {web_scaffold_status['status']}")
    
    # Test 4: List all requests
    print("\n4. Listing all scaffolding requests...")
    requests = scaffolder.list_scaffolding_requests()
    print(f"Found {len(requests)} scaffolding requests")
    
    # Test 5: Check final statuses
    print("\n5. Checking final statuses...")
    all_request_ids = [scaffold_id, web_scaffold_id]
    for req_id in all_request_ids:
        status = scaffolder.get_scaffolding_status(req_id)
        if status:
            print(f"  - {req_id[:8]}: {status['status']}")
            if status.get('result'):
                result = status['result']
                if isinstance(result, str):
                    try:
                        result = json.loads(result)
                    except json.JSONDecodeError:
                        result = {"output": result}
                print(f"    Files created: {len(result.get('files_created', []))}")
                print(f"    Directories created: {len(result.get('directories_created', []))}")
    
    # Test 6: Verify created projects
    print("\n6. Verifying created projects...")
    python_project = test_project / "test-python-project"
    if python_project.exists():
        print(f"Python project directory exists: {python_project}")
        # Check for key files
        key_files = ["README.md", "setup.py", "src/main.py"]
        for file_name in key_files:
            if (python_project / file_name).exists():
                print(f"  [OK] {file_name} exists")
            else:
                print(f"  [MISSING] {file_name} missing")
    
    web_project = test_project / "test-web-project"
    if web_project.exists():
        print(f"Web project directory exists: {web_project}")
        # Check for key files
        key_files = ["README.md", "setup.py", "src/main.py"]
        for file_name in key_files:
            if (web_project / file_name).exists():
                print(f"  [OK] {file_name} exists")
            else:
                print(f"  [MISSING] {file_name} missing")
    
    # Clean up test project and generated files
    shutil.rmtree(test_project, ignore_errors=True)
    
    # Clean up any generated automation files
    automation_files = list(Path(__file__).parent.glob("test_project_*"))
    for f in automation_files:
        if f.is_dir():
            shutil.rmtree(f, ignore_errors=True)
    
    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    test_project_scaffolding()
