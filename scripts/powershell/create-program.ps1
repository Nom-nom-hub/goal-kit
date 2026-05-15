# Create a program structure in a Goal Kit project

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$ProgramName,

    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-ProgramFile {
    param(
        [string]$ProgramName,
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

    # Clean program name for directory use
    $cleanName = $ProgramName -replace '[^a-zA-Z0-9 -]', '' -replace '  +', '-' -replace '-$', '' -replace ' ', '-'
    $cleanName = $cleanName.ToLower()
    $programDir = ".goalkit/programs/$cleanName"
    $programFile = Join-Path -Path $programDir -ChildPath "program.md"

    if ($JsonMode) {
        $jsonOutput = @{
            "PROGRAM_DIR" = $programDir
            "PROGRAM_FILE" = $programFile
            "PROGRAM_NAME" = $ProgramName
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }

    if ((Test-Path $programFile) -and (-not $DryRun)) {
        Write-Warning "Program file already exists: $programFile"
        if (-not $Force) {
            $response = Read-Host "Overwrite existing program file? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Info "Operation cancelled"
                return
            }
        }
    }

    if ($DryRun) {
        Write-Info "[DRY RUN] Would create program file: $programFile"
        return
    }

    # Create program directory
    try {
        New-Item -ItemType Directory -Path $programDir -Force -ErrorAction Stop | Out-Null
    } catch {
        Write-Error-Custom "Failed to create program directory: $programDir"
        exit 1
    }

    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

    $programContent = @"
# Program: $ProgramName

**Created**: $timestamp
**Status**: Draft

## Vision
[2-3 sentence vision statement for this program]

## Strategic Context
- **Strategic Pillar**: [Which pillar this program serves]
- **Business Impact**: [Expected business outcomes]
- **Timeline**: [6+ week timeline]

## Goals in Program

### Goal 1: [Goal Name]
- **Owner**: [Goal owner]
- **Timeline**: [Start - End]
- **Success Criteria**: [Measurable outcomes]
- **Dependencies**: [What blocks this goal]

### Goal 2: [Goal Name]
- **Owner**: [Goal owner]
- **Timeline**: [Start - End]
- **Success Criteria**: [Measurable outcomes]
- **Dependencies**: [What blocks this goal]

[Add additional goals as needed]

## Timeline
```
[ASCII timeline showing goal sequence and dependencies]
```

## Governance
- **Exec Sponsor**: [Executive sponsor name]
- **Program Manager**: [Program manager name]
- **Review Cadence**: [How often the program is reviewed]
- **Decision Authority**: [Who decides scope/timeline/resources]

## Resource Allocation
- **Teams**: [Teams involved]
- **Allocation**: [Percentage per team]
- **Budget**: [Estimated budget if applicable]

## Success Criteria
- **Functional**: [What gets built]
- **Business**: [Revenue/cost/market impact]
- **Quality**: [Uptime/reliability targets]
- **Team**: [Skills/morale/retention goals]
"@

    Set-Content -Path $programFile -Value $programContent -Encoding UTF8

    Write-Success "Created program file: $programFile"
    Write-Host ""
    Write-Info "Program Details:"
    Write-Host "  Name: $ProgramName"
    Write-Host "  Directory: $programDir"
    Write-Host "  File: $programFile"
    Write-Host ""
    Write-Info "Next Steps:"
    Write-Host "  1. Define the program vision and goals"
    Write-Host "  2. Map dependencies between goals"
    Write-Host "  3. Use /goalkit.goal-alignment to create goals in this program"
    Write-Host "  4. Use /goalkit.execute to begin execution"
    Write-Host ""
}

# Main execution
New-ProgramFile -ProgramName $ProgramName -DryRun $DryRun -Force $Force -JsonMode $Json
