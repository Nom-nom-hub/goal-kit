# Setup cross-goal coordination in a Goal Kit project

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalDirectory,

    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-CrossGoalCoordinationFile {
    param(
        [string]$GoalDirectory,
        [bool]$DryRun,
        [bool]$Force,
        [bool]$JsonMode )

    if (-not (Test-GitRepo)) {
        Write-Error-Custom "Not in a git repository"
        Write-Info "Please run this from the root of a Goal Kit project"
        exit 1
    }

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
        $coordinationFile = Join-Path -Path $GoalDirectory -ChildPath "cross-goal-coordination.md"
        $branchName = $goalDirName

        $jsonOutput = @{
            "GOAL_DIR" = $GoalDirectory
            "COORDINATION_FILE" = $coordinationFile
            "BRANCH_NAME" = $branchName
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }

    if (-not (Test-Path $GoalDirectory)) {
        Write-Error-Custom "Goal directory does not exist: $GoalDirectory"
        exit 1
    }

    $coordinationFile = Join-Path -Path $GoalDirectory -ChildPath "cross-goal-coordination.md"
    if ((Test-Path $coordinationFile) -and (-not $DryRun)) {
        Write-Warning "Cross-goal coordination file already exists: $coordinationFile"
        if (-not $Force) {
            $response = Read-Host "Overwrite existing cross-goal coordination file? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Info "Operation cancelled"
                return
            }
        }
    }

    if ($DryRun) {
        Write-Info "[DRY RUN] Would create cross-goal coordination file: $coordinationFile"
        return
    }

    $goalDirName = Split-Path -Leaf $GoalDirectory
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

    $coordinationContent = @"
# Cross-Goal Coordination Plan for $goalDirName

**Created**: $timestamp
**Status**: Draft

## Overview
Coordination plan between goal $goalDirName and other active goals.

## Blocking Goals
- **Dependencies**: [What goals must complete before this one]
- **Blocking Deliverables**: [Specific outputs needed]
- **Contingency**: [Fallback if dependencies slip]

## Unblocking Goals
- **Goals Unblocked**: [What goals depend on this one]
- **Deliverables**: [What outputs unblock others]
- **Timeline Impact**: [When dependent goals can start]

## Critical Path
- **If This Goal Slips**: [Impact on dependent goals 1, 2, and 4 weeks]
- **Bottlenecks**: [Where delays are most likely]

## Handoff Protocol
- **Transfer Points**: [When ownership changes between goals]
- **Acceptance Criteria**: [How handoffs are validated]
- **Communication**: [How handoff stakeholders are notified]

## Synchronization Plan
- **Cross-Goal Sync Cadence**: [When teams sync up]
- **Shared Milestones**: [Joint progress checks]
- **Risk Monitoring**: [How cascade risks are tracked]

## Contingency Plan
- **Fallback Strategies**: [What if blocking goals slip]
- **Parallel Work**: [What can proceed independently]
"@

    Set-Content -Path $coordinationFile -Value $coordinationContent -Encoding UTF8

    Write-Success "Created cross-goal coordination file: $coordinationFile"

    if (-not (Set-GoalEnvironment $GoalDirectory)) {
        Write-Error-Custom "Failed to setup goal environment for $GoalDirectory"
        exit 1
    }
}

# Main execution
New-CrossGoalCoordinationFile -GoalDirectory $GoalDirectory -DryRun $DryRun -Force $Force -JsonMode $Json
