#!/usr/bin/env python3
"""
Test file for the automated documentation generation
"""

import os
import shutil
import sys
from pathlib import Path
from typing import Any

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from goal_cli.documentation import DocumentationGenerator


def test_documentation_generation():
    """Test the automated documentation generation"""
    print("Testing Automated Documentation Generation...")
    
    # Create a temporary project directory for testing
    test_project = Path(__file__).parent / "test_project"
    test_project.mkdir(exist_ok=True)
    
    # Create required .goal directory structure
    goal_dir = test_project / ".goal"
    goal_dir.mkdir(exist_ok=True)
    
    # Create a basic goal.yaml file
    goal_yaml = goal_dir / "goal.yaml"
    with open(goal_yaml, 'w') as f:
        f.write("project:\n  name: test-project\n  version: 0.1.0\n  description: A test project for documentation generation\n")
    
    # Initialize documentation generator
    doc_generator = DocumentationGenerator(test_project)
    
    # Test 1: Generate README documentation
    print("\n1. Generating README documentation...")
    readme_vars = {
        "project_name": "Test Project",
        "project_description": "A test project for documentation generation",
        "features": "- Feature 1\n- Feature 2\n- Feature 3",
        "installation": "```bash\npip install test-project\n```",
        "usage": "```python\nimport test_project\n# Use the project\n```"
    }
    
    readme_id = doc_generator.generate_documentation(
        ".",
        "readme",
        "README.md",
        readme_vars
    )
    print(f"Created README generation request: {readme_id}")
    
    # Check status
    readme_status = doc_generator.get_doc_status(readme_id)
    print(f"README Status: {readme_status['status']}")
    
    # Test 2: Generate API documentation
    print("\n2. Generating API documentation...")
    api_vars = {
        "project_description": "API documentation for the test project",
        "endpoints": "### GET /api/test\n\nTest endpoint",
        "data_models": "### TestModel\n\nA test data model"
    }
    
    api_id = doc_generator.generate_documentation(
        "src",
        "api",
        "docs/api.md",
        api_vars
    )
    print(f"Created API generation request: {api_id}")
    
    # Check status
    api_status = doc_generator.get_doc_status(api_id)
    print(f"API Status: {api_status['status']}")
    
    # Test 3: Generate user guide
    print("\n3. Generating user guide...")
    user_guide_vars = {
        "introduction": "User guide for the test project",
        "getting_started": "Follow these steps to get started",
        "installation": "Install the project using pip",
        "usage": "Use the project as follows"
    }
    
    user_guide_id = doc_generator.generate_documentation(
        ".",
        "user_guide",
        "docs/user_guide.md",
        user_guide_vars
    )
    print(f"Created user guide generation request: {user_guide_id}")
    
    # Check status
    user_guide_status = doc_generator.get_doc_status(user_guide_id)
    print(f"User Guide Status: {user_guide_status['status']}")
    
    # Test 4: List all requests
    print("\n4. Listing all documentation requests...")
    requests = doc_generator.list_doc_requests()
    print(f"Found {len(requests)} documentation requests")
    
    # Test 5: Generate project documentation
    print("\n5. Generating comprehensive project documentation...")
    project_info = {
        "name": "Test Project",
        "description": "A comprehensive test project",
        "version": "1.0.0"
    }
    
    project_requests = doc_generator.generate_project_docs(project_info)
    print(f"Generated {len(project_requests)} project documentation files")
    
    for req_id in project_requests:
        status = doc_generator.get_doc_status(req_id)
        if status:
            print(f"  - {status['output_path']} ({status['doc_type']}): {status['status']}")
    
    # Test 6: Check final statuses
    print("\n6. Checking final statuses...")
    for req_id in [readme_id, api_id, user_guide_id] + project_requests:
        status = doc_generator.get_doc_status(req_id)
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
    test_documentation_generation()