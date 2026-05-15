# Create goal alignment document in a Goal Kit project

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalDirectory,

    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-GoalAlignmentFile {
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
        $alignmentFile = Join-Path -Path $GoalDirectory -ChildPath "goal-alignment.md"
        $branchName = $goalDirName

        $jsonOutput = @{
            "GOAL_DIR" = $GoalDirectory
            "ALIGNMENT_FILE" = $alignmentFile
            "BRANCH_NAME" = $branchName
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }

    if (-not (Test-Path $GoalDirectory)) {
        Write-Error-Custom "Goal directory does not exist: $GoalDirectory"
        exit 1
    }

    $alignmentFile = Join-Path -Path $GoalDirectory -ChildPath "goal-alignment.md"
    if ((Test-Path $alignmentFile) -and (-not $DryRun)) {
        Write-Warning "Goal alignment file already exists: $alignmentFile"
        if (-not $Force) {
            $response = Read-Host "Overwrite existing goal alignment file? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Info "Operation cancelled"
                return
            }
        }
    }

    if ($DryRun) {
        Write-Info "[DRY RUN] Would create goal alignment file: $alignmentFile"
        return
    }

    $goalDirName = Split-Path -Leaf $GoalDirectory
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

    $alignmentContent = @"
# Goal Alignment: $goalDirName

**Created**: $timestamp
**Status**: Draft

## Strategic Pillar
- **Primary Pillar**: [Which strategic pillar this goal advances]
- **Connection**: [Explicit link between goal and pillar]

## 3-Year Objectives Supported
- **Objective 1**: [How this goal advances the objective]
- **Objective 2**: [How this goal advances the objective]

## Values Alignment
- **Value 1**: [How goal approach demonstrates this value]
- **Value 2**: [How goal approach demonstrates this value]
- **Value 3**: [How goal approach demonstrates this value]

## Business Impact
- **Revenue**: [Expected revenue impact]
- **Cost**: [Expected cost impact]
- **Risk**: [Risk reduction or mitigation]
- **Capability**: [New capabilities built]
- **Stakeholder**: [Stakeholder impact]

## Dependencies
- **Internal Dependencies**: [What else needs to succeed]
- **External Dependencies**: [Outside factors required]

## Metrics Alignment
- **Goal Metrics**: [Success criteria from goal.md]
- **Org Metrics**: [How they feed organizational metrics]
- **Linkage**: [Explicit connection between goal and org metrics]

## Stakeholder Alignment
- **Stakeholders**: [Who has been consulted]
- **Status**: [Aligned / Pending / Concerns]
"@

    Set-Content -Path $alignmentFile -Value $alignmentContent -Encoding UTF8

    Write-Success "Created goal alignment file: $alignmentFile"

    if (-not (Set-GoalEnvironment $GoalDirectory)) {
        Write-Error-Custom "Failed to setup goal environment for $GoalDirectory"
        exit 1
    }
}

# Main execution
New-GoalAlignmentFile -GoalDirectory $GoalDirectory -DryRun $DryRun -Force $Force -JsonMode $Json
