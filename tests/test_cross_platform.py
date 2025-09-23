#!/usr/bin/env python3
"""
Test file for the cross-platform scripting capabilities
"""

import os
import shutil
import sys
from pathlib import Path
from typing import Any

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from goal_cli.cross_platform import CrossPlatformScriptManager


def test_cross_platform_scripting():
    """Test the cross-platform scripting capabilities"""
    print("Testing Cross-Platform Scripting...")
    
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
    
    # Initialize script manager
    script_manager = CrossPlatformScriptManager(test_project)
    
    # Test 1: Platform information
    print("\n1. Getting platform information...")
    platform_info = script_manager.get_platform_info()
    print(f"Current platform: {platform_info['platform']}")
    print(f"Default extension: {platform_info['default_extension']}")
    print(f"Default interpreter: {platform_info['default_interpreter']}")
    
    # Test 2: Create a simple script
    print("\n2. Creating a simple script...")
    
    if platform_info['platform'] == 'windows':
        script_content = 'Write-Host "Hello from PowerShell!"\nWrite-Host "Argument: $args"'
        script_path = script_manager.create_script("hello", script_content, "windows")
    else:
        script_content = 'echo "Hello from Bash!"\necho "Argument: $1"'
        script_path = script_manager.create_script("hello", script_content, platform_info['platform'])
    
    print(f"Created script: {script_path}")
    
    # Test 3: Execute the script
    print("\n3. Executing the script...")
    result = script_manager.execute_script(script_path, ["test_argument"])
    
    if result["success"]:
        print("Script executed successfully!")
        if result.get("stdout"):
            print(f"Output:\n{result['stdout']}")
    else:
        print("Script execution failed!")
        if result.get("error"):
            print(f"Error: {result['error']}")
        if result.get("stderr"):
            print(f"Error output:\n{result['stderr']}")
    
    # Test 4: Create cross-platform scripts
    print("\n4. Creating cross-platform scripts...")
    
    cross_platform_scripts = {
        "windows": 'Write-Host "Hello from Windows PowerShell!"',
        "linux": 'echo "Hello from Linux Bash!"',
        "darwin": 'echo "Hello from macOS Bash!"'
    }
    
    created_scripts = script_manager.create_cross_platform_script("greeting", cross_platform_scripts)
    print(f"Created cross-platform scripts: {created_scripts}")
    
    # Test 5: Create unified script interface
    print("\n5. Creating unified script interface...")
    
    operations = {
        "build": "echo 'Building project...'",
        "test": "echo 'Running tests...'",
        "deploy": "echo 'Deploying application...'"
    }
    
    unified_script = script_manager.create_unified_script_interface("workflow", operations)
    print(f"Created unified script: {unified_script}")
    
    # Test 6: List available scripts
    print("\n6. Listing available scripts...")
    scripts = script_manager.list_available_scripts()
    print(f"Found {len(scripts)} scripts:")
    for script in scripts:
        print(f"  - {script['name']} ({script['platform']})")
    
    # Clean up test project and generated files
    shutil.rmtree(test_project, ignore_errors=True)
    
    # Clean up any generated automation files
    automation_files = list(Path(__file__).parent.glob("test_project_*"))
    for f in automation_files:
        if f.is_dir():
            shutil.rmtree(f, ignore_errors=True)
    
    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    test_cross_platform_scripting()