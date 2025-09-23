#!/usr/bin/env python3
"""
Test file for the advanced automation framework
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from goal_cli.automation import (
    AdvancedAutomationFramework, 
    TaskPriority, 
    TaskStatus,
    AutomationTask
)
from datetime import datetime, timedelta


def test_automation_framework():
    """Test the advanced automation framework"""
    print("Testing Advanced Automation Framework...")
    
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
    
    # Initialize automation framework
    automation = AdvancedAutomationFramework(test_project)
    
    # Test 1: Create tasks
    print("\n1. Creating tasks...")
    
    task1_id = automation.create_task(
        name="Test Task 1",
        command="echo 'Hello World'",
        description="A simple test task",
        priority="HIGH",
        estimated_duration=1000,  # 1 second
        resource_requirements={"cpu": 20.0, "memory": 100.0}
    )
    print(f"Created task 1 with ID: {task1_id}")
    
    task2_id = automation.create_task(
        name="Test Task 2",
        command="echo 'Task 2'",
        description="Another test task",
        priority="NORMAL",
        dependencies=[task1_id],  # Depends on task 1
        estimated_duration=500,  # 0.5 seconds
        resource_requirements={"cpu": 10.0, "memory": 50.0}
    )
    print(f"Created task 2 with ID: {task2_id}")
    
    # Test 2: Check task status
    print("\n2. Checking task status...")
    
    status1 = automation.get_task_status(task1_id)
    print(f"Task 1 status: {status1['status'] if status1 else 'Not found'}")
    
    status2 = automation.get_task_status(task2_id)
    print(f"Task 2 status: {status2['status'] if status2 else 'Not found'}")
    
    # Test 3: Resource utilization
    print("\n3. Checking resource utilization...")
    
    resources = automation.get_resource_utilization()
    for resource, utilization in resources.items():
        print(f"{resource}: {utilization:.1f}%")
    
    # Test 4: Schedule efficiency
    print("\n4. Checking schedule efficiency...")
    
    efficiency = automation.get_schedule_efficiency()
    print(f"Schedule efficiency: {efficiency:.2f}")
    
    # Test 5: Generate report
    print("\n5. Generating automation report...")
    
    report = automation.generate_automation_report()
    print("Report generated successfully")
    print(f"Report length: {len(report)} characters")
    
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
    test_automation_framework()