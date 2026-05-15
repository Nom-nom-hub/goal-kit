# Setup team roles for a goal in a Goal Kit project

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalDirectory,

    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-TeamRolesFile {
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
        $rolesFile = Join-Path -Path $GoalDirectory -ChildPath "team-roles.md"
        $branchName = $goalDirName

        $jsonOutput = @{
            "GOAL_DIR" = $GoalDirectory
            "ROLES_FILE" = $rolesFile
            "BRANCH_NAME" = $branchName
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }

    if (-not (Test-Path $GoalDirectory)) {
        Write-Error-Custom "Goal directory does not exist: $GoalDirectory"
        exit 1
    }

    $rolesFile = Join-Path -Path $GoalDirectory -ChildPath "team-roles.md"
    if ((Test-Path $rolesFile) -and (-not $DryRun)) {
        Write-Warning "Team roles file already exists: $rolesFile"
        if (-not $Force) {
            $response = Read-Host "Overwrite existing team roles file? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Info "Operation cancelled"
                return
            }
        }
    }

    if ($DryRun) {
        Write-Info "[DRY RUN] Would create team roles file: $rolesFile"
        return
    }

    $goalDirName = Split-Path -Leaf $GoalDirectory
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

    $rolesContent = @"
# Team Roles: $goalDirName

**Created**: $timestamp
**Status**: Draft

## Role Definitions

### Goal Owner
- **Name**: [Goal owner name]
- **Responsibility**: Overall goal success and decision making
- **Authority**: Scope, timeline, and resource decisions
- **Accountability**: Goal completion and success criteria

### Technical Lead
- **Name**: [Technical lead name]
- **Responsibility**: Technical direction and architecture
- **Authority**: Technical decisions and implementation approach
- **Accountability**: Technical quality and delivery

### Product Owner
- **Name**: [Product owner name]
- **Responsibility**: Requirements and stakeholder management
- **Authority**: Priority and scope decisions
- **Accountability**: Value delivery and user satisfaction

### QA Owner
- **Name**: [QA owner name]
- **Responsibility**: Quality standards and testing
- **Authority**: Quality gates and release sign-off
- **Accountability**: Product quality

## RACI Matrix

| Milestone | Goal Owner | Tech Lead | Product | QA | DevOps |
|-----------|-----------|-----------|---------|-----|--------|
| Planning | A/R | C | C | I | I |
| Implementation | A/I | R | C | I | C |
| Testing | A/I | C | C | R | I |
| Deployment | A/I | I | I | C | R |

## Role Interactions
- **Goal Owner ↔ Tech Lead**: Weekly tech review
- **Product ↔ Goal Owner**: Priority alignment as needed
- **QA ↔ Tech Lead**: Test plan review before testing phase

## Escalation Path
- **Technical Disagreements**: Tech Lead decides, escalate to Goal Owner
- **Scope Changes**: Product Owner decides, escalate to Goal Owner
- **Resource Conflicts**: Goal Owner decides, escalate to Program Manager
"@

    Set-Content -Path $rolesFile -Value $rolesContent -Encoding UTF8

    Write-Success "Created team roles file: $rolesFile"

    if (-not (Set-GoalEnvironment $GoalDirectory)) {
        Write-Error-Custom "Failed to setup goal environment for $GoalDirectory"
        exit 1
    }
}

# Main execution
New-TeamRolesFile -GoalDirectory $GoalDirectory -DryRun $DryRun -Force $Force -JsonMode $Json
