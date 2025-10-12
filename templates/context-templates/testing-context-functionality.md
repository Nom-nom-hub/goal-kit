# Testing Context Functionality with Goal Kit Files

This document outlines how to test the AI context retention functionality with existing Goal Kit markdown files.

## Test Approach

Since Goal Kit is primarily a markdown-based system, testing involves:

1. **Validating context extraction** from existing goal files
2. **Verifying context aggregation** across multiple files
3. **Testing context persistence** through file updates
4. **Ensuring proper retrieval** when AI agents start new sessions

## Test Scenarios

### 1. Basic Context Loading Test

**Objective**: Verify that context can be loaded from existing goal files

**Setup**:
- Have at least one goal file in the `.goalkit/goals/` directory
- Ensure the goal file follows the standard Goal Kit format

**Test Steps**:
1. Initialize the ContextLoader with a project directory
2. Call `load_context()` method
3. Verify that the context contains:
   - Goal title and statement
   - Success metrics
   - Milestones information
   - Any context metadata present

**Expected Result**: The context loader should successfully parse the goal file and extract relevant information into a structured format.

### 2. Multiple Goals Context Loading Test

**Objective**: Verify that context can be aggregated from multiple goal files

**Setup**:
- Have multiple goal files in the `.goalkit/goals/` directory
- Include both active and inactive goals

**Test Steps**:
1. Initialize the ContextLoader with a project directory containing multiple goals
2. Call `load_context()` method
3. Verify that the context includes information from all relevant goal files
4. Verify that only active goals are included based on status metadata

**Expected Result**: The context loader should aggregate information from multiple goal files while respecting goal status and relevance.

### 3. Context Summary File Test

**Objective**: Verify that the ai-context.md summary file is properly processed

**Setup**:
- Create an `ai-context.md` file in the project root
- Include active goals, strategies, and milestones sections

**Test Steps**:
1. Ensure `ai-context.md` file exists with sample content
2. Initialize the ContextLoader
3. Call `load_context()` method
4. Verify that summary information is correctly extracted

**Expected Result**: All sections of the ai-context.md file should be properly parsed and included in the overall context.

### 4. Interaction Log Processing Test

**Objective**: Verify that AI interaction logs are properly processed

**Setup**:
- Create a `.goalkit/logs/` directory
- Add sample interaction log files in markdown format

**Test Steps**:
1. Ensure interaction log files exist with sample content
2. Initialize the ContextLoader
3. Call `load_context()` method
4. Verify that interaction log information is correctly extracted

**Expected Result**: Recent interaction logs should be parsed and included in the context data.

### 5. Context Update Test

**Objective**: Verify that context changes are properly persisted to markdown files

**Setup**:
- Have an existing goal with context metadata
- Prepare updates to apply to the context

**Test Steps**:
1. Load existing context using ContextLoader
2. Apply mock updates to the context (e.g., change goal status, add milestone)
3. Implement a method to write updates back to markdown files
4. Verify that the updates are correctly written to the files

**Expected Result**: Context changes should be properly serialized back to markdown format and saved to the appropriate files.

## Test Implementation

### Python Test Script

```python
# test_context_functionality.py
import os
import tempfile
import shutil
from context_loader import ContextLoader

def test_basic_context_loading():
    """Test that context can be loaded from a basic goal file"""
    
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        goals_dir = os.path.join(temp_dir, ".goalkit", "goals", "001-test-goal")
        os.makedirs(goals_dir)
        
        # Create a basic goal file
        goal_content = """# Goal: Test Goal
        
**Goal Statement**: This is a test goal to verify context loading functionality.

**Created**: 2025-10-12
**Goal Branch**: 001-test-goal

## 1. Goal Overview

### Goal Statement
This is a test goal to verify context loading functionality.

### Context
Testing the goal kit context retention system.

### Success Level
Successfully load context from this goal file.

## 2. Success Metrics

### Primary Metrics
- Context loads successfully
- All key information is extracted

### Secondary Metrics
- Performance is acceptable
- Error handling works correctly

## 5. Goal Milestones

### Milestone 1: Context Loading
- **Description**: Load context from this goal
- **Acceptance Criteria**: Context is loaded successfully
- **Timeline**: 2025-10-12

**Context Metadata**:
- **Last AI Interaction**: 2025-10-12T10:30:00Z
- **Active Strategy**: Test Strategy
- **Current Milestone**: Milestone 1 - Context Loading
- **Status**: In Progress
"""
        
        with open(os.path.join(goals_dir, "goal.md"), "w") as f:
            f.write(goal_content)
        
        # Test context loading
        loader = ContextLoader(temp_dir)
        context = loader.load_context()
        
        # Verify the context was loaded correctly
        assert context is not None
        assert len(context['goals']) == 1
        assert context['goals'][0]['goal_title'] == "Test Goal"
        assert context['goals'][0]['status'] == "In Progress"
        
        print("✓ Basic context loading test passed")

def test_multiple_goals():
    """Test that context can be aggregated from multiple goal files"""
    
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create first goal
        goal1_dir = os.path.join(temp_dir, ".goalkit", "goals", "001-goal-one")
        os.makedirs(goal1_dir)
        
        goal1_content = """# Goal: Goal One
        
**Goal Statement**: First test goal.

**Created**: 2025-10-12
**Goal Branch**: 001-goal-one

**Context Metadata**:
- **Status**: In Progress
"""
        with open(os.path.join(goal1_dir, "goal.md"), "w") as f:
            f.write(goal1_content)
            
        # Create second goal
        goal2_dir = os.path.join(temp_dir, ".goalkit", "goals", "002-goal-two")
        os.makedirs(goal2_dir)
        
        goal2_content = """# Goal: Goal Two
        
**Goal Statement**: Second test goal.

**Created**: 2025-10-12
**Goal Branch**: 002-goal-two

**Context Metadata**:
- **Status**: Planned
"""
        with open(os.path.join(goal2_dir, "goal.md"), "w") as f:
            f.write(goal2_content)
        
        # Test context loading
        loader = ContextLoader(temp_dir)
        context = loader.load_context()
        
        # Verify both goals were loaded
        assert len(context['goals']) == 2
        goal_titles = [g['goal_title'] for g in context['goals']]
        assert "Goal One" in goal_titles
        assert "Goal Two" in goal_titles
        
        print("✓ Multiple goals loading test passed")

def test_context_summary_file():
    """Test that ai-context.md summary file is properly processed"""
    
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ai-context.md file
        context_content = """# AI Context Summary

**Date**: 2025-10-12

## Active Goals
- [001-goal-one](goals/001-goal-one/goal.md) - In Progress
- [002-goal-two](goals/002-goal-two/goal.md) - Planned

## Active Strategies
- **Goal 001**: Test Strategy approach
- **Goal 002**: Alternative approach

## Current Milestones
- 001: Complete Testing (due 2025-10-20)
- 002: Review Results (due 2025-10-25)

## Key Information
- **Project**: Test Project
- **Team**: Test Team

## Recent Decisions
1. Approved testing approach
2. Scheduled review meeting
"""
        
        with open(os.path.join(temp_dir, "ai-context.md"), "w") as f:
            f.write(context_content)
        
        # Test context loading
        loader = ContextLoader(temp_dir)
        context = loader.load_context()
        
        # Verify summary was loaded correctly
        assert context['summary'] is not None
        assert context['summary']['date'] == "2025-10-12"
        assert len(context['summary']['active_goals']) == 2
        assert context['summary']['key_information'].find('Test Project') != -1
        
        print("✓ Context summary file test passed")

if __name__ == "__main__":
    test_basic_context_loading()
    test_multiple_goals()
    test_context_summary_file()
    print("All tests passed!")
```

## Testing with Real Goal Kit Projects

To test with actual Goal Kit projects:

1. **Select an existing project** that uses Goal Kit
2. **Run the context loader** on that project directory
3. **Verify that relevant information** is extracted correctly
4. **Check for any parsing errors** with non-standard markdown
5. **Validate that the context** makes sense for AI assistance

### Example Test Command

```bash
# Test with a real project
python test_context_functionality.py --project-path /path/to/existing/goal/kit/project
```

## Success Criteria

A successful test of the context functionality will show:

- Context is loaded quickly (within a few seconds)
- All relevant information from goal files is extracted
- Multiple goals are properly aggregated
- Context summary information is accurate
- Interaction history is properly included
- No errors during parsing of valid Goal Kit markdown files