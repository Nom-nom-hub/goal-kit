#!/usr/bin/env python3
"""
Validate goal methodology in a Goal Kit project
"""
import argparse
import os
import sys
import json
import subprocess
from pathlib import Path

# Add the common Python utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common import (
    write_info, 
    write_success, 
    write_error, 
    write_warning,
    test_git_repo,
    get_git_root,
    test_goal_methodology_completion
)


def validate_methodology(verbose=False, json_output=False):
    """
    Validate the goal methodology completion
    """
    # Check if we're in a git repository
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    # Get project root
    project_root = get_git_root()
    os.chdir(project_root)

    # Check if this is a Goal Kit project
    vision_file_path = os.path.join(project_root, ".goalkit", "vision.md")
    if not os.path.exists(vision_file_path):
        write_error("Not a Goal Kit project")
        write_info("Please run 'goalkeeper init' first to set up the project")
        sys.exit(1)

    # Get all goal directories
    goals_dir = os.path.join(project_root, "goals")
    if not os.path.exists(goals_dir):
        write_warning("No goals directory found. Create a goal first using /goalkit.goal")
        if json_output:
            result = {
                "project": os.path.basename(project_root),
                "goals_checked": 0,
                "errors": ["No goals directory found"]
            }
            print(json.dumps(result))
        return

    goal_dirs = [d for d in os.listdir(goals_dir) 
                 if os.path.isdir(os.path.join(goals_dir, d))]
    
    if not goal_dirs:
        write_warning("No goals found in goals directory")
        if json_output:
            result = {
                "project": os.path.basename(project_root),
                "goals_checked": 0,
                "errors": ["No goals found"]
            }
            print(json.dumps(result))
        return

    results = {
        "project": os.path.basename(project_root),
        "goals_checked": len(goal_dirs),
        "completed_goals": 0,
        "total_goals": len(goal_dirs),
        "goals": []
    }

    for goal_dir_name in goal_dirs:
        goal_path = os.path.join(goals_dir, goal_dir_name)
        try:
            # Change to goal directory for validation
            original_dir = os.getcwd()
            os.chdir(goal_path)
            
            if verbose:
                write_info(f"Validating methodology for goal: {goal_dir_name}")
            
            # Test methodology completion
            is_complete = test_goal_methodology_completion(goal_path)
            if is_complete:
                results["completed_goals"] += 1
            
            # Collect goal-specific data
            goal_result = {
                "name": goal_dir_name,
                "completed": is_complete,
                "path": goal_path
            }
            results["goals"].append(goal_result)
            
            # Return to project root
            os.chdir(original_dir)
            
        except Exception as e:
            if verbose:
                write_error(f"Error validating goal {goal_dir_name}: {str(e)}")
            goal_result = {
                "name": goal_dir_name,
                "completed": False,
                "path": goal_path,
                "error": str(e)
            }
            results["goals"].append(goal_result)

    # Output results
    if json_output:
        print(json.dumps(results, indent=2))
    else:
        completed_count = results["completed_goals"]
        total_count = results["total_goals"]
        completion_percent = round((completed_count / total_count) * 100) if total_count > 0 else 0
        
        print()
        write_success(f"Methodology validation completed: {completion_percent}% ({completed_count}/{total_count} goals complete)")
        
        for goal in results["goals"]:
            status = "✓" if goal["completed"] else "✗"
            status_text = "Complete" if goal["completed"] else "Incomplete"
            color = "green" if goal["completed"] else "red"
            # Since our write_colored function doesn't have a direct method for conditional colors
            # we'll just use standard output for now
            print(f"  {status} {goal['name']}: {status_text}")
        
        print()
        write_info("Summary:")
        print(f"  Project: {results['project']}")
        print(f"  Goals checked: {results['goals_checked']}")
        print(f"  Completed: {results['completed_goals']}")
        print(f"  Incomplete: {results['total_goals'] - results['completed_goals']}")
        
        if completed_count == total_count:
            write_success("All goals have completed the methodology! Ready for execution.")
        else:
            write_warning("Some goals have incomplete methodology. Consider completing all steps before execution.")


def main():
    parser = argparse.ArgumentParser(description='Validate goal methodology in a Goal Kit project')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--json-output', action='store_true', help='Output results in JSON format')
    
    args = parser.parse_args()

    validate_methodology(verbose=args.verbose, json_output=args.json_output)


if __name__ == "__main__":
    main()