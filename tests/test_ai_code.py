#!/usr/bin/env python3
"""
Test file for the AI-powered code generation and refactoring tools
"""

import os
import shutil
import sys
from pathlib import Path
from typing import Any

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from goal_cli.ai_code import AICodeGenerator


def test_ai_code_generation():
    """Test the AI-powered code generation and refactoring tools"""
    print("Testing AI-Powered Code Generation...")
    
    # Create a temporary project directory for testing
    test_project = Path(__file__).parent / "test_project"
    test_project.mkdir(exist_ok=True)
    
    # Create required .goal directory structure
    goal_dir = test_project / ".goal"
    goal_dir.mkdir(exist_ok=True)
    
    # Create a basic goal.yaml file
    goal_yaml = goal_dir / "goal.yaml"
    with open(goal_yaml, 'w') as f:
        f.write("project:\n  name: test-project\n  version: 0.1.0\n")
    
    # Initialize AI code generator
    ai_generator = AICodeGenerator(test_project)
    
    # Test 1: Generate Python/Flask code
    print("\n1. Generating Python/Flask code...")
    request_id = ai_generator.generate_code(
        "Create a simple REST API for managing users",
        "python",
        "flask"
    )
    print(f"Created generation request: {request_id}")
    
    # Check status
    status = ai_generator.get_generation_status(request_id)
    print(f"Status: {status['status']}")
    
    # Test 2: Generate JavaScript/React code
    print("\n2. Generating JavaScript/React code...")
    request_id2 = ai_generator.generate_code(
        "Create a user list component with search functionality",
        "javascript",
        "react",
        "src/components/UserList.js"
    )
    print(f"Created generation request: {request_id2}")
    
    # Check status
    status2 = ai_generator.get_generation_status(request_id2)
    print(f"Status: {status2['status']}")
    
    # Test 3: List all requests
    print("\n3. Listing all requests...")
    gen_requests = ai_generator.list_generation_requests()
    print(f"Found {len(gen_requests)} generation requests")
    
    # Test 4: Analyze code quality
    print("\n4. Analyzing code quality...")
    
    # Create a test file to analyze
    test_file = test_project / "test_script.py"
    with open(test_file, 'w') as f:
        f.write("""
# This is a test script with some issues
def long_function():
    # This function is too long
    x = 1
    y = 2
    z = 3
    a = 4
    b = 5
    c = 6
    d = 7
    e = 8
    f = 9
    g = 10
    h = 11
    i = 12
    j = 13
    k = 14
    l = 15
    m = 16
    n = 17
    o = 18
    p = 19
    q = 20
    r = 21
    s = 22
    t = 23
    u = 24
    v = 25
    w = 26
    x = 27
    y = 28
    z = 29
    return x + y + z

# TODO: Add error handling
# FIXME: This is a fixme comment
""")
    
    analysis = ai_generator.analyze_code_quality("test_script.py")
    print(f"Analyzed file: {analysis['file']}")
    print(f"Lines of code: {analysis['lines_of_code']}")
    print(f"Suggestions: {len(analysis['suggestions'])}")
    for suggestion in analysis['suggestions']:
        print(f"  - {suggestion['type']}: {suggestion['description']}")
    
    # Test 5: Refactor code
    print("\n5. Refactoring code...")
    refactor_id = ai_generator.refactor_code(
        "test_script.py",
        "document",
        "Add comprehensive documentation"
    )
    print(f"Created refactoring request: {refactor_id}")
    
    # Check status
    ref_status = ai_generator.get_refactoring_status(refactor_id)
    print(f"Status: {ref_status['status']}")
    
    # Test 6: List refactoring requests
    print("\n6. Listing refactoring requests...")
    ref_requests = ai_generator.list_refactoring_requests()
    print(f"Found {len(ref_requests)} refactoring requests")
    
    # Clean up test project and generated files
    shutil.rmtree(test_project, ignore_errors=True)
    
    # Clean up any generated automation files
    automation_files = list(Path(__file__).parent.glob("test_project_*"))
    for f in automation_files:
        if f.is_dir():
            shutil.rmtree(f, ignore_errors=True)
    
    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    test_ai_code_generation()