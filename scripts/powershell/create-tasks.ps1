# Generate implementation tasks for a goal

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$GoalDir,
    
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-Tasks {
    param(
        [string]$GoalDir,
        [bool]$Force,
        [bool]$JsonMode )
    
    # Check if we're in a git repository
    if (-not (Test-GitRepo)) {
        Write-Error-Custom "Not in a git repository"
        Write-Info "Please run this from the root of a Goal Kit project"
        exit 1
    }
    
    # Get project root
    $projectRoot = Get-GitRoot
    if ([string]::IsNullOrEmpty($projectRoot)) {
        Write-Error-Custom "Could not determine git root. Not in a git repository."
        exit 1
    }
    
    Set-Location $projectRoot | Out-Null
    
    # Check if this is a Goal Kit project
    $visionFile = Join-Path -Path ".goalkit" -ChildPath "vision.md"
    if (-not (Test-Path $visionFile)) {
        Write-Error-Custom "Not a Goal Kit project"
        Write-Info "Please run 'goalkeeper init' first to set up the project"
        exit 1
    }
    
    # Determine goal directory
    if ([string]::IsNullOrEmpty($GoalDir)) {
        # If no goal dir specified, use current directory if it's a goal directory
        $currentDir = Get-Location
        if ($currentDir.Path.Contains(".goalkit\goals") -or $currentDir.Path.Contains(".goalkit/goals")) {
            $GoalDir = Split-Path -Leaf $currentDir.Path
        } else {
            Write-Error-Custom "Goal directory not specified and not in a goal directory"
            Write-Info "Usage: Create-Tasks [goal-dir-name] or run from a goal directory"
            exit 1
        }
    }
    
    # Find the goal directory
    $goalsDir = Join-Path -Path ".goalkit" -ChildPath "goals"
    $targetGoalDir = Join-Path $goalsDir $GoalDir
    
    if (-not (Test-Path $targetGoalDir)) {
        Write-Error-Custom "Goal directory not found: $GoalDir"
        exit 1
    }
    
    # Check for goal.md
    $goalFile = Join-Path -Path $targetGoalDir -ChildPath "goal.md"
    if (-not (Test-Path $goalFile)) {
        Write-Error-Custom "goal.md not found in goal directory"
        exit 1
    }
    
    # Define tasks file path
    $tasksFile = Join-Path -Path $targetGoalDir -ChildPath "tasks.md"
    
    # If JSON mode, output JSON
    if ($JsonMode) {
        $jsonOutput = @{
            "GOAL_DIR" = $GoalDir
            "TASKS_FILE" = $tasksFile
            "GOAL_FILE" = $goalFile
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }
    
    # Check if tasks file already exists
    if (Test-Path $tasksFile) {
        if (-not $Force) {
            Write-Warning "Tasks file already exists: $tasksFile"
            Write-Info "Use --force to overwrite"
            exit 0
        }
    }
    
    # Get timestamp
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    
    # Read goal file to get context
    $goalContent = Get-Content -Path $goalFile -Raw
    $goalName = Split-Path -Leaf $targetGoalDir
    
    # Check if template exists
    $templatePath = Join-Path -Path (Join-Path -Path $projectRoot -ChildPath ".goalkit") -ChildPath (Join-Path -Path "templates" -ChildPath "tasks-template.md")
    if (Test-Path $templatePath) {
        $templateContent = Get-Content -Path $templatePath -Raw
        $tasksContent = $templateContent -replace '\[GOAL\]', $goalName
        $tasksContent = $tasksContent -replace '\[DATE\]', $timestamp
    } else {
        # Fallback to default content
        $tasksContent = @"
# Implementation Tasks: $goalName

**Created**: $timestamp
**Last Updated**: $timestamp
**Goal Directory**: $GoalDir

## Overview

This document contains the detailed implementation tasks needed to achieve the goal defined in goal.md.
Tasks should be broken down into:
- Clear, actionable items
- Specific acceptance criteria
- Dependencies and sequencing
- Estimated effort

## Phase 1: Foundation & Setup

### Task 1.1: [Task Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]
- [ ] [Specific criterion 3]

**Dependencies**: [List any dependencies]
**Effort**: [Estimated effort: Small/Medium/Large]

---

### Task 1.2: [Task Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]

**Dependencies**: Task 1.1
**Effort**: [Estimated effort]

---

## Phase 2: Core Implementation

### Task 2.1: [Task Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]
- [ ] [Specific criterion 3]

**Dependencies**: Task 1.1, Task 1.2
**Effort**: [Estimated effort]

---

### Task 2.2: [Task Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]

**Dependencies**: Task 2.1
**Effort**: [Estimated effort]

---

## Phase 3: Testing & Validation

### Task 3.1: [Task Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]

**Dependencies**: [List dependencies]
**Effort**: [Estimated effort]

---

## Phase 4: Deployment & Documentation

### Task 4.1: [Task Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]

**Dependencies**: [List dependencies]
**Effort**: [Estimated effort]

---

## Notes

- Update task status as you progress through implementation
- Use checkboxes to track acceptance criteria completion
- Reference this file in pull requests and commits
"@
    }
    
    # Write tasks file
    Set-Content -Path $tasksFile -Value $tasksContent -Encoding UTF8
    Write-Success "Created tasks.md: $tasksFile"
    
    # Git operations
    git add $tasksFile 2>$null | Out-Null
    git commit -m "Add implementation tasks for goal: $goalName" 2>$null | Out-Null
    
    Write-Success "Tasks committed to repository"
    
    # Print summary
    Write-Host ""
    Write-Info "Tasks file created successfully!"
    Write-Host "  Goal Directory: $GoalDir"
    Write-Host "  Tasks File: $tasksFile"
    Write-Host ""
    Write-Info "Next Steps:"
    Write-Host "  1. Fill in detailed tasks for each phase"
    Write-Host "  2. Break down complex tasks into subtasks"
    Write-Host "  3. Define clear acceptance criteria"
    Write-Host "  4. Use /goalkit.taskstoissues to convert tasks to GitHub issues"
    Write-Host ""
}

# Main execution
New-Tasks -GoalDir $GoalDir -Force $Force -JsonMode $Json 