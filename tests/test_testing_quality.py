#!/usr/bin/env python3
"""
Test file for the automated testing and quality gates system
"""

import json
import os
import shutil
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from goal_cli.testing_quality import TestingAndQualityManager


def test_testing_and_quality():
    """Test the automated testing and quality gates system"""
    print("Testing Automated Testing and Quality Gates System...")
    
    # Create a temporary project directory for testing
    test_project = Path(__file__).parent / "test_project"
    test_project.mkdir(exist_ok=True)
    
    # Create required .goal directory structure
    goal_dir = test_project / ".goal"
    goal_dir.mkdir(exist_ok=True)
    
    # Create a basic goal.yaml file
    goal_yaml = goal_dir / "goal.yaml"
    with open(goal_yaml, 'w') as f:
        f.write("project:\n  name: test-project\n  version: 0.1.0\n  description: A test project for testing and quality\n")
    
    # Create a simple test file for testing
    tests_dir = test_project / "tests"
    tests_dir.mkdir(exist_ok=True)
    
    with open(tests_dir / "test_example.py", 'w') as f:
        f.write('''"""Example test file."""
import unittest

class TestExample(unittest.TestCase):
    """Example test case."""
    
    def test_example(self):
        """Example test."""
        self.assertEqual(1 + 1, 2)

if __name__ == "__main__":
    unittest.main()
''')
    
    # Initialize testing and quality manager
    test_manager = TestingAndQualityManager(test_project)
    
    # Test 1: List quality gates
    print("\n1. Listing quality gates...")
    gates = test_manager.list_quality_gates()
    print(f"Found {len(gates)} quality gates")
    for gate in gates[:3]:  # Show first 3
        print(f"  - {gate['id']}: {gate['name']}")
    
    # Test 2: Run unit tests
    print("\n2. Running unit tests...")
    test_id = test_manager.run_tests("unit", "tests", "unittest")
    print(f"Created test request: {test_id}")
    
    # Check status
    test_status = test_manager.get_test_status(test_id)
    print(f"Test Status: {test_status['status']}")
    
    # Test 3: Evaluate a quality gate
    print("\n3. Evaluating a quality gate...")
    gate_id = "code_coverage"
    gate_evaluation_id = test_manager.evaluate_quality_gate(gate_id)
    print(f"Evaluated quality gate: {gate_evaluation_id}")
    
    # Check gate status
    gate_status = test_manager.get_quality_gate_status(gate_id)
    print(f"Gate Status: {gate_status['status']}")
    if gate_status.get('result'):
        result = gate_status['result']
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                result = {"output": result}
        print(f"Gate Passed: {result.get('passed', 'unknown')}")
    
    # Test 4: Run all quality gates
    print("\n4. Running all quality gates...")
    all_gates_result = test_manager.run_all_quality_gates()
    print(f"Total Gates: {all_gates_result['total_gates']}")
    print(f"Passed Gates: {all_gates_result['passed_gates']}")
    print(f"Failed Gates: {all_gates_result['failed_gates']}")
    
    # Test 5: List all test requests
    print("\n5. Listing all test requests...")
    requests = test_manager.list_test_requests()
    print(f"Found {len(requests)} test requests")
    
    # Test 6: List all quality gates
    print("\n6. Listing all quality gates...")
    all_gates = test_manager.list_quality_gates()
    print(f"Found {len(all_gates)} quality gates")
    
    # Test 7: Generate test report
    print("\n7. Generating test report...")
    report_content = test_manager.generate_test_report()
    print(f"Generated report with {len(report_content)} characters")
    
    # Test 8: Check final statuses
    print("\n8. Checking final statuses...")
    # Check test status
    final_test_status = test_manager.get_test_status(test_id)
    if final_test_status:
        print(f"  Test {test_id[:8]}: {final_test_status['status']}")
        if final_test_status.get('result'):
            result = final_test_status['result']
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    result = {"output": result}
            print(f"    Success: {result.get('success', 'unknown')}")
    
    # Check gate status
    final_gate_status = test_manager.get_quality_gate_status(gate_id)
    if final_gate_status:
        print(f"  Gate {gate_id}: {final_gate_status['status']}")
        if final_gate_status.get('result'):
            result = final_gate_status['result']
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    result = {"output": result}
            print(f"    Passed: {result.get('passed', 'unknown')}")
    
    # Clean up test project and generated files
    shutil.rmtree(test_project, ignore_errors=True)
    
    # Clean up any generated automation files
    automation_files = list(Path(__file__).parent.glob("test_project_*"))
    for f in automation_files:
        if f.is_dir():
            shutil.rmtree(f, ignore_errors=True)
    
    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    test_testing_and_quality()