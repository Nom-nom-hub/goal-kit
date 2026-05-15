# Create OKR mapping document for a goal in a Goal Kit project

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalDirectory,

    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-OkrMappingFile {
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
        $mappingFile = Join-Path -Path $GoalDirectory -ChildPath "okr-mapping.md"
        $branchName = $goalDirName

        $jsonOutput = @{
            "GOAL_DIR" = $GoalDirectory
            "MAPPING_FILE" = $mappingFile
            "BRANCH_NAME" = $branchName
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }

    if (-not (Test-Path $GoalDirectory)) {
        Write-Error-Custom "Goal directory does not exist: $GoalDirectory"
        exit 1
    }

    $mappingFile = Join-Path -Path $GoalDirectory -ChildPath "okr-mapping.md"
    if ((Test-Path $mappingFile) -and (-not $DryRun)) {
        Write-Warning "OKR mapping file already exists: $mappingFile"
        if (-not $Force) {
            $response = Read-Host "Overwrite existing OKR mapping file? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Info "Operation cancelled"
                return
            }
        }
    }

    if ($DryRun) {
        Write-Info "[DRY RUN] Would create OKR mapping file: $mappingFile"
        return
    }

    $goalDirName = Split-Path -Leaf $GoalDirectory
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

    $mappingContent = @"
# OKR Mapping: $goalDirName

**Created**: $timestamp
**Status**: Draft

## Mapping Summary
- **Goal**: $goalDirName
- **Supporting KRs**: [Which OKR key results this goal supports]
- **Contribution %**: [Estimated contribution to each KR]

## Goal-KR Connections
### KR 1: [KR Title]
- **Success Criteria Link**: [How goal metrics prove KR achievement]
- **Contribution**: [Estimated percentage]

### KR 2: [KR Title]
- **Success Criteria Link**: [How goal metrics prove KR achievement]
- **Contribution**: [Estimated percentage]

## Timeline Alignment
- **Goal Completion Date**: [When goal finishes]
- **OKR Measurement Date**: [When OKR progress is measured]
- **Risk**: [If goal finishes after OKR measurement]

## Confidence & Risk
- **Confidence Level**: [1-5 assessment]
- **Key Risks**: [What could prevent goal from driving KRs]
- **Mitigations**: [How risks are addressed]

## OKR Check-In Integration
- **Mid-Quarter Review**: [How goal progress feeds OKR review]
- **End-of-Quarter**: [How goal impact on KRs is measured]
"@

    Set-Content -Path $mappingFile -Value $mappingContent -Encoding UTF8

    Write-Success "Created OKR mapping file: $mappingFile"

    if (-not (Set-GoalEnvironment $GoalDirectory)) {
        Write-Error-Custom "Failed to setup goal environment for $GoalDirectory"
        exit 1
    }
}

# Main execution
New-OkrMappingFile -GoalDirectory $GoalDirectory -DryRun $DryRun -Force $Force -JsonMode $Json
