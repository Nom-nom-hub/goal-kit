#!/usr/bin/env python3
"""
Create a new goal in a Goal Kit project
"""
import argparse
import os
import sys
import json
import re
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


def create_goal(goal_description, dry_run=False, force=False, json_mode=False, verbose=False):
    """
    Create a new goal in the goals directory
    """
    # Validate arguments
    if not goal_description:
        write_error("Goal description is required")
        return

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

    # If JSON mode, output JSON and exit early
    if json_mode:
        # Find the next goal number
        next_number = 1
        goals_dir = os.path.join(project_root, ".goalkit", "goals")
        
        if os.path.exists(goals_dir):
            goal_dirs = [d for d in os.listdir(goals_dir) 
                         if os.path.isdir(os.path.join(goals_dir, d)) and d[0].isdigit()]
            for goal_dir in goal_dirs:
                try:
                    num = int(re.match(r'^(\d+)-', goal_dir).group(1))
                    if num >= next_number:
                        next_number = num + 1
                except (AttributeError, ValueError):
                    continue

        # Create goal directory name
        goal_number = f"{next_number:03d}"
        clean_description = re.sub(r'[^a-zA-Z0-9\s-]', '', goal_description)
        clean_description = re.sub(r'\s+', '-', clean_description).strip('-').lower()
        goal_dir_name = f"{goal_number}-{clean_description}"
        goal_dir = os.path.join(".goalkit", "goals", goal_dir_name)
        goal_file = os.path.join(goal_dir, "goal.md")

        # Output JSON with required variables
        json_data = {
            "GOAL_DIR": goal_dir,
            "GOAL_FILE": goal_file,
            "GOAL_DESCRIPTION": goal_description,
            "BRANCH_NAME": goal_dir_name
        }
        
        print(json.dumps(json_data, separators=(',', ':')))
        return

    # Check if goals directory exists
    goals_dir = os.path.join(project_root, ".goalkit", "goals")
    if not os.path.exists(goals_dir):
        if dry_run:
            write_info(f"[DRY RUN] Would create goals directory: {goals_dir}")
        else:
            os.makedirs(goals_dir, exist_ok=True)
            write_success(f"Created goals directory: {goals_dir}")

    # Find the next goal number
    next_number = 1
    if os.path.exists(goals_dir):
        goal_dirs = [d for d in os.listdir(goals_dir) 
                     if os.path.isdir(os.path.join(goals_dir, d)) and d[0].isdigit()]
        for goal_dir in goal_dirs:
            try:
                num = int(re.match(r'^(\d+)-', goal_dir).group(1))
                if num >= next_number:
                    next_number = num + 1
            except (AttributeError, ValueError):
                continue

    # Create goal directory name
    goal_number = f"{next_number:03d}"
    clean_description = re.sub(r'[^a-zA-Z0-9\s-]', '', goal_description)
    clean_description = re.sub(r'\s+', '-', clean_description).strip('-').lower()
    goal_dir_name = f"{goal_number}-{clean_description}"
    goal_dir = os.path.join(".goalkit", "goals", goal_dir_name)

    # Check if goal directory already exists
    full_goal_dir = os.path.join(project_root, goal_dir)
    if os.path.exists(full_goal_dir):
        if not force:
            write_error(f"Goal directory already exists: {goal_dir}")
            write_info("Use a different goal description or remove the existing directory")
            sys.exit(1)
        else:
            if verbose:
                write_info(f"Overwriting existing goal directory: {goal_dir}")

    if dry_run:
        write_info(f"[DRY RUN] Would create goal directory: {goal_dir}")
        write_info(f"[DRY RUN] Would create goal.md with description: {goal_description}")
        write_info(f"[DRY RUN] Would create branch: {goal_dir_name}")
        return

    # Create goal directory
    os.makedirs(full_goal_dir, exist_ok=True)
    write_success(f"Created goal directory: {goal_dir}")

    # Create goal.md file with goal structure
    goal_content = f"""# Goal Statement: {goal_description}

**Branch**: `{goal_dir_name}`
**Created**: {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}
**Status**: Draft
**Methodology**: Goal-Driven Development

## 🎯 Goal Definition

**Goal Statement**: {goal_description}

**Context**: [Why is this goal important? What problem does it solve?]

**Success Level**: [What \"successful goal achievement\" looks like]

## 📊 Success Metrics

### Primary Metrics (Must achieve for successful goal completion)

- **Metric 1**: [Measurable outcome 1] - Target: [specific, quantifiable target]
- **Metric 2**: [Measurable outcome 2] - Target: [specific, quantifiable target] 
- **Metric 3**: [Measurable outcome 3] - Target: [specific, quantifiable target]

### Secondary Metrics (Valuable but not required)

- **Metric 1**: [Nice-to-have outcome 1] - Target: [aspirational target]
- **Metric 2**: [Nice-to-have outcome 2] - Target: [aspirational target]

## 🔍 Validation Strategy

### Measurement Approach
- **Data Sources**: [Where to collect metrics from]
- **Measurement Frequency**: [How often to measure progress]
- **Success Thresholds**: [When to consider the goal achieved]

### Learning Objectives
- **What to Learn**: [Key insights to gain from achieving this goal]
- **Adaptation Points**: [When to reconsider the approach]
- **Documentation**: [What information to document for future reference]

## 📝 Goal Breakdown

### Critical Path Activities
- **Activity 1**: [Key activity 1 to achieve the goal]
- **Activity 2**: [Key activity 2 to achieve the goal]
- **Activity 3**: [Key activity 3 to achieve the goal]

### Dependencies
- **Dependency 1**: [What this goal depends on]
- **Dependency 2**: [What this goal depends on]

### Risk Assessment
- **Risk 1**: [Potential risk] - Mitigation: [how to mitigate]
- **Risk 2**: [Potential risk] - Mitigation: [how to mitigate]

## 🔄 Review Process

### Review Schedule
- **Check-ins**: [Regular assessment schedule]
- **Milestone Reviews**: [When to evaluate progress]

### Success Validation
- **[Validation 1]**: [How to confirm goal is achieved]
- **[Validation 2]**: [How to confirm goal is achieved]

## 🏁 Completion Criteria

### Success Indicators
- [ ] Primary metrics achieved at target levels
- [ ] Goal objectives validated through measurement
- [ ] Learning objectives accomplished
- [ ] No major unforeseen issues discovered

### Success Validation
- **[Validation 1]**: [How to confirm goal was successful]
- **[Validation 2]**: [How to confirm goal was successful]

## 🔁 Adaptation Framework

### Regular Review Schedule
- **Weekly**: [Goal effectiveness assessment]
- **When Metrics Diverge**: [How to adjust approach]
- **When Learning Occurs**: [How to incorporate new information]

### Adaptation Triggers
- **Pivot Trigger 1**: [When to change approach]
- **Pause Trigger**: [When to temporarily adjust]
- **Realign Trigger**: [When to reconsider entirely]

---

*This goal definition serves as the foundation for all work related to achieving this objective. All strategies, milestones, and execution should align with these defined success metrics.*
"""

    goal_file_path = os.path.join(full_goal_dir, "goal.md")
    with open(goal_file_path, 'w', encoding='utf-8') as f:
        f.write(goal_content)

    write_success(f"Created goal.md with description: {goal_description}")

    # Create git branch for this goal
    if verbose:
        write_info("Setting up git branch for this goal...")
    
    os.chdir(project_root)
    branch_name = new_goal_branch(goal_dir_name)

    # Add and commit the new goal
    os.chdir(project_root)
    os.system(f'git add {goal_dir}')
    os.system(f'git commit -m "Add goal: {goal_description}\\n\\n- Created goal definition in {goal_dir}/goal.md\\n- Branch: {branch_name}"')

    write_success(f"Goal committed to branch: {branch_name}")

    # Update agent context
    update_agent_context()

    # Print summary
    write_success("Goal created successfully!")
    print()
    write_info("Goal Details:")
    print(f"  Directory: {goal_dir}")
    print(f"  Branch: {branch_name}")
    print(f"  Description: {goal_description}")
    print()
    write_info("Next Steps:")
    print(f"  1. Navigate to goal directory: cd {goal_dir}")
    print("  2. Complete the goal definition with specific details")
    print("  3. Use /goalkit.strategies to explore implementation strategies")
    print("  4. Use /goalkit.milestones to create measurable milestones") 
    print("  5. Use /goalkit.execute to implement with learning and adaptation")
    print()
    os.system("git branch --show-current")


def main():
    parser = argparse.ArgumentParser(description='Create a new goal in a Goal Kit project')
    parser.add_argument('goal_description', help='Description of the goal to create')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be created without creating it')
    parser.add_argument('--force', action='store_true', help='Overwrite existing goal directory without prompting')
    parser.add_argument('--json', action='store_true', help='Output JSON with goal details only')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()

    create_goal(
        goal_description=args.goal_description,
        dry_run=args.dry_run,
        force=args.force,
        json_mode=args.json,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()