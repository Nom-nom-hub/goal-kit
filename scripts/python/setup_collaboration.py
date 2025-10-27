#!/usr/bin/env python3
"""
Create a new collaboration plan in a Goal Kit project
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


def create_collaboration_plan(collaboration_description, dry_run=False, verbose=False, json_mode=False):
    """
    Create a new collaboration plan
    """
    collaboration_description = ' '.join(collaboration_description) if isinstance(collaboration_description, list) else collaboration_description

    # Validate arguments
    if not collaboration_description or not collaboration_description.strip():
        write_error("Collaboration description is required")
        print("Usage: setup-collaboration.py [--dry-run] [--verbose] <collaboration_description>")
        sys.exit(1)

    if verbose:
        write_info("Collaboration script started")

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

    # Check if this is a Goal Kit project
    vision_file_path = os.path.join(project_root, ".goalkit", "vision.md")
    if not os.path.exists(vision_file_path):
        write_error("Not a Goal Kit project")
        write_info("Please run 'goalkeeper init' first to set up the project")
        sys.exit(1)

    # If JSON mode, output JSON and exit early
    if json_mode or os.environ.get('JSON_MODE') == 'true':
        # Find the next collaboration number (use same numbering as goals)
        next_number = 1
        collabs_dir = "collaborations"
        collabs_path = os.path.join(project_root, collabs_dir)

        if os.path.exists(collabs_path):
            collab_dirs = [d for d in os.listdir(collabs_path) 
                          if os.path.isdir(os.path.join(collabs_path, d)) and d[0].isdigit()]
            for collab_dir in collab_dirs:
                try:
                    match = re.match(r'^(\d+)-', collab_dir)
                    if match:
                        num = int(match.group(1))
                        if num >= next_number:
                            next_number = num + 1
                except (AttributeError, ValueError):
                    continue

        # Create collaboration directory name
        collab_number = f"{next_number:03d}"
        clean_description = re.sub(r'[^a-zA-Z0-9\s-]', '', collaboration_description)
        clean_description = re.sub(r'\s+', '-', clean_description).strip('-').lower()
        collab_dir_name = f"{collab_number}-{clean_description}"
        collab_dir = os.path.join(collabs_dir, collab_dir_name)
        collab_file = os.path.join(collab_dir, "collaboration.md")

        # Output JSON with required variables
        json_data = {
            "COLLAB_DIR": collab_dir,
            "COLLAB_FILE": collab_file,
            "COLLAB_DESCRIPTION": collaboration_description,
            "BRANCH_NAME": collab_dir_name
        }

        print(json.dumps(json_data, separators=(',', ':')))
        return

    # Check if collaborations directory exists
    collabs_dir = "collaborations"
    collabs_path = os.path.join(project_root, collabs_dir)

    if not os.path.exists(collabs_path):
        if dry_run:
            write_info(f"[DRY RUN] Would create collaborations directory: {collabs_dir}")
        else:
            os.makedirs(collabs_path, exist_ok=True)
            write_success(f"Created collaborations directory: {collabs_dir}")

    # Find the next collaboration number (use same numbering as goals)
    next_number = 1
    if os.path.exists(collabs_path):
        collab_dirs = [d for d in os.listdir(collabs_path) 
                      if os.path.isdir(os.path.join(collabs_path, d)) and d[0].isdigit()]
        for collab_dir in collab_dirs:
            try:
                match = re.match(r'^(\d+)-', collab_dir)
                if match:
                    num = int(match.group(1))
                    if num >= next_number:
                        next_number = num + 1
            except (AttributeError, ValueError):
                continue

    # Create collaboration directory name
    collab_number = f"{next_number:03d}"
    clean_description = re.sub(r'[^a-zA-Z0-9\s-]', '', collaboration_description)
    clean_description = re.sub(r'\s+', '-', clean_description).strip('-').lower()
    collab_dir_name = f"{collab_number}-{clean_description}"
    collab_dir = os.path.join(collabs_dir, collab_dir_name)

    # Check if collaboration directory already exists
    full_collab_dir = os.path.join(project_root, collab_dir)
    if os.path.exists(full_collab_dir):
        write_error(f"Collaboration directory already exists: {collab_dir}")
        write_info("Use a different collaboration description or remove the existing directory")
        sys.exit(1)

    if dry_run:
        write_info(f"[DRY RUN] Would create collaboration directory: {collab_dir}")
        write_info(f"[DRY RUN] Would create collaboration.md with description: {collaboration_description}")
        write_info(f"[DRY RUN] Would create branch: {collab_dir_name}")
        return

    # Create collaboration directory
    os.makedirs(full_collab_dir, exist_ok=True)
    write_success(f"Created collaboration directory: {collab_dir}")

    # Create collaboration.md file with coordination structure
    collaboration_content = f"""# Collaboration Plan: {collaboration_description}

**Branch**: `{collab_dir_name}`
**Created**: {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}
**Mode**: [Single-Agent/Multi-Agent/Self-Coordination]
**Status**: Draft

## 🤝 Collaboration Overview

**Coordination Statement**: {collaboration_description}

**Context**: [Why is this coordination important? What coordination challenge does it solve?]

**Participants**: [List of agents, systems, or processes involved in coordination - use \"Self\" for single-agent coordination]

**Success Level**: [What \"successful coordination\" looks like for this collaboration]

## 🎯 Coordination Mode

### Selected Mode: [Single-Agent Mode | Multi-Agent Mode | Self-Coordination Mode]

**Mode Justification**: [Why this coordination mode was selected - detected agents, user input, or default behavior]

### Single-Agent Mode Features
- **Self-Consistency**: Maintaining consistency across different interactions with the same agent
- **State Tracking**: Tracking decision state across different sessions
- **Progress Validation**: Validating previous decisions remain valid

### Multi-Agent Mode Features (If Applicable)
- **Agent Awareness**: Agents aware of work done by other agents
- **Conflict Detection**: Identifying potential conflicts between agent work
- **Task Synchronization**: Coordinating work between agents to avoid conflicts
- **Knowledge Sharing**: Agents can access information created by other agents

### Self-Coordination Mode Features
- **State Consistency**: Ensuring the agent maintains consistency with its own previous work
- **Self-Verification**: Checking if previous decisions are still valid
- **Progress Tracking**: Maintaining awareness of own progress over time

## 📊 Coordination Success Metrics

### Primary Metrics (Must achieve for successful coordination)

- **Metric 1**: [Measurable coordination outcome] - Target: [specific, quantifiable target]
- **Metric 2**: [Measurable coordination outcome] - Target: [specific, quantifiable target]
- **Metric 3**: [Measurable coordination outcome] - Target: [specific, quantifiable target]

### Secondary Metrics (Valuable but not required)

- **Metric 1**: [Nice-to-have coordination outcome] - Target: [aspirational target]
- **Metric 2**: [Nice-to-have coordination outcome] - Target: [aspirational target]

## 👥 Coordination Participants & Roles

### Coordination Participants
- **[Participant 1]**: [Role in coordination - what they do]
- **[Participant 2]**: [Role in coordination - what they do]

### Coordination Responsibilities
- **[Responsibility 1]**: [Who handles this coordination task]
- **[Responsibility 2]**: [Who handles this coordination task]

## 🎯 Coordination Activities

### Activity 1: [Activity Title] (Priority: P1)
**Description**: [What this coordination activity achieves]

**Success Indicators**:
- [Measurable coordination outcome 1]
- [Measurable coordination outcome 2]

**Validation Method**: [How to confirm this coordination activity is achieved]

**Expected Timeline**: [Rough time estimate]

**Owner**: [Who is responsible for this activity]

---

### Activity 2: [Activity Title] (Priority: P2)
**Description**: [What this coordination activity achieves]

**Success Indicators**:
- [Measurable coordination outcome 1]
- [Measurable coordination outcome 2]

**Validation Method**: [How to confirm this coordination activity is achieved]

**Expected Timeline**: [Rough time estimate]

**Owner**: [Who is responsible for this activity]

---

### Activity 3: [Activity Title] (Priority: P3)
**Description**: [What this coordination activity achieves]

**Success Indicators**:
- [Measurable coordination outcome 1]
- [Measurable coordination outcome 2]

**Validation Method**: [How to confirm this coordination activity is achieved]

**Expected Timeline**: [Rough time estimate]

**Owner**: [Who is responsible for this activity]

---

## 🔗 Coordination Dependencies

### Coordination Dependencies
- **[Dependency 1]**: [What this coordination depends on]
- **[Dependency 2]**: [What this coordination depends on]

### Coordination Impacts
- **[Impact 1]**: [What this coordination affects]
- **[Impact 2]**: [What this coordination affects]

## 🗣️ Communication Plan

### Communication Channels
- **[Channel 1]**: [How coordination information is shared]
- **[Channel 2]**: [How coordination information is shared]

### Communication Frequency
- **Status Updates**: [How often coordination status is checked/shared]
- **Conflict Resolution**: [How conflicts are communicated and resolved]

### Communication Protocol
- **[Protocol 1]**: [How coordination information is formatted/shared]
- **[Protocol 2]**: [How coordination information is formatted/shared]

## 🔄 Synchronization Points

### Synchronization Events
- **[Event 1]**: [When coordination alignment happens]
- **[Event 2]**: [When coordination alignment happens]

### Synchronization Process
- **[Process 1]**: [How coordination alignment is achieved]
- **[Process 2]**: [How coordination alignment is achieved]

## ⚠️ Conflict Resolution

### Potential Conflicts
- **[Conflict 1]**: [What could go wrong in coordination]
- **[Conflict 2]**: [What could go wrong in coordination]

### Resolution Approaches
- **[Approach 1]**: [How to resolve this type of conflict]
- **[Approach 2]**: [How to resolve this type of conflict]

## 📈 Coordination Validation Strategy

### Measurement Approach
- **Data Sources**: [Where to collect coordination metrics from]
- **Measurement Frequency**: [How often to measure coordination effectiveness]
- **Success Thresholds**: [When to consider the coordination successful]

### Learning Objectives
- **What to Learn**: [Key insights to gain from coordination]
- **Adaptation Points**: [When to reconsider the coordination approach]
- **Documentation**: [What coordination information to document for future reference]

## 📋 Coordination Checkpoints

### Coordination Milestones
- **[Milestone 1]**: [Coordination achievement to reach]
- **[Milestone 2]**: [Coordination achievement to reach]

### Coordination Verification Points
- **[Verification 1]**: [When to verify coordination is working properly]
- **[Verification 2]**: [When to verify coordination is working properly]

## 🚀 Coordination Implementation

### Setup Requirements
- **[Requirement 1]**: [What needs to be set up for coordination]
- **[Requirement 2]**: [What needs to be set up for coordination]

### Implementation Steps
1. **Step 1**: [First step in coordination implementation]
2. **Step 2**: [Second step in coordination implementation]
3. **Step 3**: [Third step in coordination implementation]

## 🏁 Coordination Completion Criteria

### Success Indicators
- [ ] Primary coordination metrics achieved at target levels
- [ ] Coordination objectives validated through measurement
- [ ] All coordination participants aligned and informed
- [ ] No significant coordination conflicts discovered
- [ ] Coordination learning objectives accomplished

### Success Validation
- **[Validation 1]**: [How to confirm coordination was successful]
- **[Validation 2]**: [How to confirm coordination was successful]

## 🔁 Coordination Review & Adaptation

### Regular Review Schedule
- **After Each Activity**: [What to review and how]
- **Weekly**: [Coordination effectiveness assessment]
- **When Conflicts Arise**: [How to reassess coordination approach]

### Adaptation Triggers
- **Pivot Trigger 1**: [When to change coordination approach]
- **Pause Trigger**: [When to temporarily adjust coordination]
- **Realign Trigger**: [When to reconsider coordination strategy entirely]

## 🔄 Coordination State Management

### State Tracking
- **[State Element 1]**: [What coordination state is tracked]
- **[State Element 2]**: [What coordination state is tracked]

### State Validation
- **[Validation 1]**: [How to ensure coordination state is valid]
- **[Validation 2]**: [How to ensure coordination state is valid]

---

*This collaboration plan serves as the foundation for coordinated work between agents or for maintaining consistency in single-agent environments. It should be reviewed and updated as coordination needs evolve during implementation.*

"""

    collab_file_path = os.path.join(full_collab_dir, "collaboration.md")
    with open(collab_file_path, 'w', encoding='utf-8') as f:
        f.write(collaboration_content)

    write_success(f"Created collaboration.md with description: {collaboration_description}")

    # Get current persona for the collaboration
    current_persona = "general"
    persona_config_dir = os.path.join(project_root, ".goalkit", "personas")
    current_persona_file = os.path.join(persona_config_dir, "current_persona.txt")
    if os.path.exists(current_persona_file):
        with open(current_persona_file, 'r') as f:
            current_persona = f.read().strip()

    # Create git branch for this collaboration (reusing goal branch function)
    if verbose:
        write_info("Setting up git branch for this collaboration...")
    os.chdir(project_root)
    branch_name = new_goal_branch(collab_dir_name)

    # Add and commit the new collaboration
    os.chdir(project_root)
    os.system(f'git add {collab_dir}')
    os.system(f'git commit -m "Add collaboration: {collaboration_description}\\n\\n- Created collaboration definition in {collab_dir}/collaboration.md\\n- Branch: {branch_name}\\n- Active persona: {current_persona}"')

    write_success(f"Collaboration committed to branch: {branch_name}")

    # Update agent context
    update_agent_context()

    # Print summary
    write_success("Collaboration created successfully!")
    print()
    write_info("Collaboration Details:")
    print(f"  Directory: {collab_dir}")
    print(f"  Branch: {branch_name}")
    print(f"  Description: {collaboration_description}")
    print()
    write_info("Next Steps:")
    print(f"  1. Navigate to collaboration directory: cd {collab_dir}")
    print("  2. Complete the collaboration plan with specific details")
    print("  3. Use coordination features as needed during development")
    print()
    result = os.popen('git branch --show-current').read().strip()
    write_info(f"Current branch is: {result}")


def main():
    parser = argparse.ArgumentParser(description='Create a new collaboration plan in a Goal Kit project')
    parser.add_argument('collaboration_description', nargs='+', help='Description of the collaboration to create')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be created without creating it')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()

    create_collaboration_plan(
        collaboration_description=args.collaboration_description,
        dry_run=args.dry_run,
        verbose=args.verbose,
        json_mode=False  # JSON mode would be handled differently in a real implementation
    )


if __name__ == "__main__":
    main()