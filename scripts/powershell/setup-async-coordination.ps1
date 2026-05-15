# Setup async coordination for a goal in a Goal Kit project

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalDirectory,

    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-AsyncCoordinationFile {
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
        $coordinationFile = Join-Path -Path $GoalDirectory -ChildPath "async-coordination.md"
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

    $coordinationFile = Join-Path -Path $GoalDirectory -ChildPath "async-coordination.md"
    if ((Test-Path $coordinationFile) -and (-not $DryRun)) {
        Write-Warning "Async coordination file already exists: $coordinationFile"
        if (-not $Force) {
            $response = Read-Host "Overwrite existing async coordination file? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Info "Operation cancelled"
                return
            }
        }
    }

    if ($DryRun) {
        Write-Info "[DRY RUN] Would create async coordination file: $coordinationFile"
        return
    }

    $goalDirName = Split-Path -Leaf $GoalDirectory
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

    $coordinationContent = @"
# Async Coordination Plan for $goalDirName

**Created**: $timestamp
**Status**: Draft

## Overview
Async-first collaboration plan for goal: $goalDirName

## Communication Rituals
- **Daily Async Standup**: [Format, channel, cadence]
- **Weekly Async Updates**: [Summary format, recipients]
- **Decision Process**: [How async decisions are made]

## Milestone Handoffs
- **Handoff Points**: [Key transitions between phases]
- **Ownership Transfer**: [Who hands off to whom]
- **Acceptance Criteria**: [How handoffs are validated]

## Escalation Path
- **Decision Authority**: [Who decides what]
- **Escalation Triggers**: [When decisions escalate]
- **Resolution Timeline**: [Expected resolution time]

## Learning Capture
- **Ritual**: [How learnings are captured]
- **Frequency**: [When insights are shared]
- **Format**: [Template for documenting learnings]

## Sync Exceptions
- **Required Sync Points**: [When real-time discussion is needed]
- **Duration**: [How long sync sessions run]
- **Attendees**: [Who participates]
"@

    Set-Content -Path $coordinationFile -Value $coordinationContent -Encoding UTF8

    Write-Success "Created async coordination file: $coordinationFile"

    if (-not (Set-GoalEnvironment $GoalDirectory)) {
        Write-Error-Custom "Failed to setup goal environment for $GoalDirectory"
        exit 1
    }
}

# Main execution
New-AsyncCoordinationFile -GoalDirectory $GoalDirectory -DryRun $DryRun -Force $Force -JsonMode $Json
