#!/usr/bin/env python3
"""
Setup a new goal in a Goal Kit project
"""
import argparse
import os
import sys
import subprocess
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
    new_goal_branch,
    update_agent_context
)


def setup_goal(verbose=False):
    """
    Setup the goal environment in a Goal Kit project
    """
    # Check if we're in a git repository
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    # Get project root
    project_root = get_git_root()
    assert project_root is not None
    os.chdir(project_root)

    # Check if this is a Goal Kit project
    vision_file_path = os.path.join(project_root, ".goalkit", "vision.md")
    if not os.path.exists(vision_file_path):
        write_error("Not a Goal Kit project")
        write_info("Please run 'goalkeeper init' first to set up the project")
        sys.exit(1)

    # Create goals directory if it doesn't exist
    goals_dir = os.path.join(project_root, "goals")
    os.makedirs(goals_dir, exist_ok=True)
    if verbose:
        write_info(f"Ensured goals directory exists: {goals_dir}")

    # Create .goalkit/personas directory if it doesn't exist
    personas_dir = os.path.join(project_root, ".goalkit", "personas")
    os.makedirs(personas_dir, exist_ok=True)
    
    # Create current_persona.txt if it doesn't exist
    current_persona_file = os.path.join(personas_dir, "current_persona.txt")
    if not os.path.exists(current_persona_file):
        with open(current_persona_file, 'w') as f:
            f.write("general\n")
        if verbose:
            write_info("Created default current_persona.txt")

    # Update agent context
    update_agent_context()

    write_success("Goal environment setup completed!")
    print()
    write_info("Environment Details:")
    print(f"  Project: {os.path.basename(project_root)}")
    print(f"  Goals Directory: goals/")
    print(f"  Current Branch: {subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True).stdout.strip()}")
    print()
    write_info("Next Steps:")
    print("  1. Use /goalkit.goal to create your first goal")
    print("  2. Use /goalkit.strategies to explore implementation strategies")
    print("  3. Use /goalkit.milestones to create measurable milestones")
    print("  4. Use /goalkit.execute to implement with learning and adaptation")


def main():
    parser = argparse.ArgumentParser(description='Setup a new goal in a Goal Kit project')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()

    setup_goal(verbose=args.verbose)


if __name__ == "__main__":
    main()