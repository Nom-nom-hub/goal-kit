#!/usr/bin/env python3
"""
Manage personas in a Goal Kit project
"""
import argparse
import os
import sys
import json
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
    update_agent_context
)


def manage_personas(command, persona=None, verbose=False):
    """
    Manage personas in the Goal Kit project
    """
    # Check if we're in a git repository
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    # Get project root
    project_root = get_git_root()
    if not project_root:
        write_error("Could not determine git root directory")
        sys.exit(1)
    os.chdir(project_root)

    # Define persona directory and file paths
    personas_dir = os.path.join(project_root, ".goalkit", "personas")
    current_persona_file = os.path.join(personas_dir, "current_persona.txt")
    
    # Ensure personas directory exists
    os.makedirs(personas_dir, exist_ok=True)
    
    if command == "list":
        list_personas(personas_dir, current_persona_file, verbose)
    elif command == "switch":
        switch_persona(personas_dir, current_persona_file, persona, verbose)
    elif command == "current":
        show_current_persona(current_persona_file, verbose)
    else:
        write_error(f"Unknown command: {command}")
        write_info("Available commands: list, switch, current")
        sys.exit(1)


def list_personas(personas_dir, current_persona_file, verbose):
    """
    List all available personas
    """
    # Get current persona
    current_persona = "general"
    if os.path.exists(current_persona_file):
        with open(current_persona_file, 'r') as f:
            current_persona = f.read().strip()
    
    # Get all persona files
    personas = []
    for file in os.listdir(personas_dir):
        if file.endswith('.json') and file not in ['current_persona.txt']:
            personas.append(file[:-5])  # Remove .json extension
    
    # Add default personas if they don't exist as files
    default_personas = ["general", "developer", "architect", "tester", "product-owner", "researcher"]
    all_personas = list(set(personas + default_personas))
    
    write_info("Available personas:")
    for persona in sorted(all_personas):
        marker = " *" if persona == current_persona else "  "
        print(f"  {marker} {persona}")
    
    if verbose:
        write_info(f"Current persona is marked with '*'")
    
    write_info(f"\nCurrent persona: {current_persona}")


def switch_persona(personas_dir, current_persona_file, persona_name, verbose):
    """
    Switch to a different persona
    """
    if not persona_name:
        write_error("Persona name is required for switch command")
        sys.exit(1)
    
    # Validate persona name (basic validation)
    if not persona_name.replace('-', '').replace('_', '').isalnum():
        write_error(f"Invalid persona name: {persona_name}")
        sys.exit(1)
    
    # Write the new persona to the current persona file
    with open(current_persona_file, 'w') as f:
        f.write(f"{persona_name}\n")
    
    write_success(f"Switched to persona: {persona_name}")
    
    if verbose:
        write_info(f"Updated {current_persona_file}")
    
    # Update agent context to reflect the change
    update_agent_context()


def show_current_persona(current_persona_file, verbose):
    """
    Show the current persona
    """
    current_persona = "general"
    if os.path.exists(current_persona_file):
        with open(current_persona_file, 'r') as f:
            current_persona = f.read().strip()
    
    print(current_persona)
    
    if verbose:
        write_info(f"Current persona is: {current_persona}")


def main():
    parser = argparse.ArgumentParser(description='Manage personas in a Goal Kit project')
    parser.add_argument('command', choices=['list', 'switch', 'current'], help='Command to execute')
    parser.add_argument('persona', nargs='?', help='Persona name (required for switch command)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()

    manage_personas(
        command=args.command,
        persona=args.persona,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()