#!/usr/bin/env python3
"""
Setup milestone planning in a Goal Kit project
"""
import argparse
import os
import sys
import json
from pathlib import Path
import datetime

# Add the common Python utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common import (
    write_info, 
    write_success, 
    write_error, 
    write_warning,
    test_git_repo,
    get_git_root,
    set_goal_environment
)


def create_milestone_file(goal_directory, dry_run=False, force=False, json_mode=False, verbose=False):
    """
    Create a milestone file for a goal directory.
    """
    if json_mode:
        if not os.path.exists(goal_directory):
            write_error(f"Goal directory does not exist: {goal_directory}")
            sys.exit(1)
        
        goal_dir_name = os.path.basename(goal_directory)
        milestone_file = os.path.join(goal_directory, "milestones.md")
        branch_name = goal_dir_name
        
        # Output JSON with required variables
        json_obj = {
            "GOAL_DIR": goal_directory,
            "MILESTONE_FILE": milestone_file,
            "BRANCH_NAME": branch_name
        }
        
        print(json.dumps(json_obj, separators=(',', ':')))
        return

    # Verify goal directory exists
    if not os.path.exists(goal_directory):
        write_error(f"Goal directory does not exist: {goal_directory}")
        sys.exit(1)

    # Check if milestones.md already exists
    milestone_file = os.path.join(goal_directory, "milestones.md")
    if os.path.exists(milestone_file) and not dry_run:
        write_warning(f"Milestone file already exists: {milestone_file}")
        if not force:
            response = input("Overwrite existing milestone file? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                write_info("Operation cancelled")
                return

    if dry_run:
        write_info(f"[DRY RUN] Would create milestone file: {milestone_file}")
        return

    # Create milestone file with basic template
    goal_dir_name = os.path.basename(goal_directory)
    milestone_content = f"""# Milestone Plan for {goal_dir_name}

## Overview
Milestone plan for goal: {goal_dir_name}

## Milestone Definition Framework
- **Measurable Outcomes**: Clear indicators of milestone achievement
- **Learning Objectives**: What to discover at each milestone
- **Value Delivery**: User/business value at each step
- **Implementation Approaches**: Different ways to achieve the milestone

## Progress Tracking Framework
- **Overall Progress Metrics**: How to measure goal advancement
- **Milestone Health Indicators**: Signs of milestone success or trouble
- **Adaptation Triggers**: When to adjust approach or sequence

## Review Process
- **Milestone Review Cadence**: Regular assessment schedule
- **Review Framework**: What to evaluate at each review
- **Decision Framework**: How to adapt based on results

## Success Validation
- **Milestone Success Criteria**: When milestone is considered complete
- **Goal Progress Indicators**: How milestone advances the goal
- **Learning Quality Assessment**: How to evaluate insights gained
"""

    # Ensure the directory exists
    os.makedirs(os.path.dirname(milestone_file), exist_ok=True)
    
    # Write the content to the file
    with open(milestone_file, 'w', encoding='utf-8') as f:
        f.write(milestone_content)

    write_success(f"Created milestone file: {milestone_file}")

    # Print summary
    write_success("Milestone planning setup completed!")
    
    print()
    write_info("Milestone Details:")
    print(f"  Goal Directory: {goal_directory}")
    print(f"  Milestone File: {milestone_file}")
    print()
    
    write_info("Next Steps:")
    print("  1. Review and enhance the milestone plan")
    print("  2. Use /goalkit.execute to implement with learning and adaptation")

    # Setup goal environment for immediate development
    try:
        set_goal_environment(goal_directory)
    except Exception as e:
        write_error(f"Failed to setup goal environment for {goal_directory}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Setup milestone planning in a Goal Kit project')
    parser.add_argument('goal_directory', help='Path to the goal directory to create milestones for')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be created without creating it')
    parser.add_argument('--force', action='store_true', help='Overwrite existing milestone file without prompting')
    parser.add_argument('--json', action='store_true', help='Output JSON with milestone details only')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.goal_directory:
        write_error("Goal directory is required")
        parser.print_help()
        sys.exit(1)

    # Check if we're in a git repository
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    # Get project root
    project_root = get_git_root()
    assert project_root is not None
    os.chdir(project_root)

    # Execute the main function
    create_milestone_file(
        goal_directory=args.goal_directory,
        dry_run=args.dry_run,
        force=args.force,
        json_mode=args.json,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()