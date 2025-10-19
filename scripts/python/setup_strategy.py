#!/usr/bin/env python3
"""
Setup strategy analysis in a Goal Kit project
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


def create_strategy_file(goal_directory, dry_run=False, force=False, json_mode=False, verbose=False):
    """
    Create a strategy file for a goal directory.
    """
    if json_mode:
        if not os.path.exists(goal_directory):
            write_error(f"Goal directory does not exist: {goal_directory}")
            sys.exit(1)
        
        goal_dir_name = os.path.basename(goal_directory)
        strategy_file = os.path.join(goal_directory, "strategies.md")
        branch_name = goal_dir_name
        
        # Output JSON with required variables
        json_obj = {
            "GOAL_DIR": goal_directory,
            "STRATEGY_FILE": strategy_file,
            "BRANCH_NAME": branch_name
        }
        
        print(json.dumps(json_obj, separators=(',', ':')))
        return

    # Verify goal directory exists
    if not os.path.exists(goal_directory):
        write_error(f"Goal directory does not exist: {goal_directory}")
        sys.exit(1)

    # Check if strategies.md already exists
    strategy_file = os.path.join(goal_directory, "strategies.md")
    if os.path.exists(strategy_file) and not dry_run and not force:
        write_warning(f"Strategy file already exists: {strategy_file}")
        response = input("Overwrite existing strategy file? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            write_info("Operation cancelled")
            return
    elif os.path.exists(strategy_file) and not dry_run and force:
        write_info("Overwriting strategy file due to -Force option.")

    if dry_run:
        write_info(f"[DRY RUN] Would create strategy file: {strategy_file}")
        return

    # Create strategy file with basic template
    goal_dir_name = os.path.basename(goal_directory)
    strategy_content = f"""# Strategy Analysis for {goal_dir_name}

## Overview
Strategy analysis for goal: {goal_dir_name}

## Strategy Exploration Framework
- **Technical Strategy Options**: Different technologies and architectures
- **User Experience Strategies**: Various approaches to user interaction
- **Implementation Strategies**: Different development and rollout approaches

## Strategy Comparison Matrix
- **Technical Feasibility**: How practical each strategy is to implement
- **User Experience Quality**: How well each strategy serves users
- **Development Effort**: Resources required for each strategy
- **Risk Level**: Potential issues and their likelihood
- **Learning Potential**: What each strategy can teach

## Recommended Starting Strategy
- **Primary Recommendation**: Which strategy to try first
- **Rationale**: Evidence-based reasoning for the choice
- **Success Criteria**: How to validate if the strategy works
- **Fallback Options**: Alternative strategies if primary fails

## Validation Experiments
- **Critical Assumption Tests**: Experiments to validate strategy assumptions
- **Measurement Plan**: How to evaluate strategy effectiveness
- **Success Thresholds**: When strategy is considered successful
"""

    # Ensure the directory exists
    os.makedirs(os.path.dirname(strategy_file), exist_ok=True)
    
    # Write the content to the file
    with open(strategy_file, 'w', encoding='utf-8') as f:
        f.write(strategy_content)

    write_success(f"Created strategy file: {strategy_file}")

    # Print summary
    write_success("Strategy analysis setup completed!")
    
    print()
    write_info("Strategy Details:")
    print(f"  Goal Directory: {goal_directory}")
    print(f"  Strategy File: {strategy_file}")
    print()
    
    write_info("Next Steps:")
    print("  1. Review and enhance the strategy analysis")
    print("  2. Use /goalkit.milestones to create measurable milestones") 
    print("  3. Use /goalkit.execute to implement with learning and adaptation")

    # Setup goal environment for immediate development
    try:
        set_goal_environment(goal_directory)
    except Exception as e:
        write_error(f"Failed to setup goal environment for {goal_directory}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Setup strategy analysis in a Goal Kit project')
    parser.add_argument('goal_directory', help='Path to the goal directory to analyze')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be created without creating it')
    parser.add_argument('--force', action='store_true', help='Overwrite existing strategy file without prompting')
    parser.add_argument('--json', action='store_true', help='Output JSON with strategy details only')
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
    os.chdir(project_root)

    # Execute the main function
    create_strategy_file(
        goal_directory=args.goal_directory,
        dry_run=args.dry_run,
        force=args.force,
        json_mode=args.json,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()