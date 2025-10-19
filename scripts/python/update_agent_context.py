#!/usr/bin/env python3
"""
Update agent context files in a Goal Kit project
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
    update_agent_context
)


def update_agent_context_cmd(verbose=False):
    """
    Update the agent context
    """
    # Check if we're in a git repository
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    # Get project root
    project_root = get_git_root()
    os.chdir(project_root)

    # Update agent context using the common function
    update_agent_context()
    
    if verbose:
        write_info("Agent context updated successfully")


def main():
    parser = argparse.ArgumentParser(description='Update agent context files in a Goal Kit project')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()

    update_agent_context_cmd(verbose=args.verbose)


if __name__ == "__main__":
    main()