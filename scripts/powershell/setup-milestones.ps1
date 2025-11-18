# Setup milestone planning in a Goal Kit project

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalDirectory,
    
    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "common.ps1")

function New-MilestoneFile {
    param(
        [string]$GoalDirectory,
        [bool]$DryRun,
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
    
    if ($JsonMode) {
        if (-not (Test-Path $GoalDirectory)) {
            Write-Error-Custom "Goal directory does not exist: $GoalDirectory"
            exit 1
        }
        
        $goalDirName = Split-Path -Leaf $GoalDirectory
        $milestoneFile = Join-Path $GoalDirectory "milestones.md"
        $branchName = $goalDirName
        
        # Output JSON with required variables
        $jsonOutput = @{
            "GOAL_DIR" = $GoalDirectory
            "MILESTONE_FILE" = $milestoneFile
            "BRANCH_NAME" = $branchName
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }
    
    # Verify goal directory exists
    if (-not (Test-Path $GoalDirectory)) {
        Write-Error-Custom "Goal directory does not exist: $GoalDirectory"
        exit 1
    }
    
    # Check if milestones.md already exists
    $milestoneFile = Join-Path $GoalDirectory "milestones.md"
    if ((Test-Path $milestoneFile) -and (-not $DryRun)) {
        Write-Warning "Milestone file already exists: $milestoneFile"
        if (-not $Force) {
            $response = Read-Host "Overwrite existing milestone file? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Info "Operation cancelled"
                return
            }
        }
    }
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would create milestone file: $milestoneFile"
        return
    }
    
    # Create milestone file with basic template
    $goalDirName = Split-Path -Leaf $GoalDirectory
    
    $milestoneContent = @"
# Milestone Plan for $goalDirName

## Overview
Milestone plan for goal: $goalDirName

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
"@
    
    Set-Content -Path $milestoneFile -Value $milestoneContent -Encoding UTF8
    
    Write-Success "Created milestone file: $milestoneFile"
    
    # Print summary
    Write-Success "Milestone planning setup completed!"
    Write-Host ""
    Write-Info "Milestone Details:"
    Write-Host "  Goal Directory: $GoalDirectory"
    Write-Host "  Milestone File: $milestoneFile"
    Write-Host ""
    
    Write-Info "Next Steps:"
    Write-Host "  1. Review and enhance the milestone plan"
    Write-Host "  2. Use /goalkit.execute to implement with learning and adaptation"
    
    # Setup goal environment for immediate development
    if (-not (Set-GoalEnvironment $GoalDirectory)) {
        Write-Error-Custom "Failed to setup goal environment for $GoalDirectory"
        exit 1
    }
}

# Main execution
New-MilestoneFile -GoalDirectory $GoalDirectory -DryRun $DryRun -Force $Force -JsonMode $Json 