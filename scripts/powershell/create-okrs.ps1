# Create quarterly OKRs document in a Goal Kit project

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$Quarter,

    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-OkrsFile {
    param(
        [string]$Quarter,
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

    $okrsFile = ".goalkit/okrs.md"

    if ($JsonMode) {
        $jsonOutput = @{
            "OKRS_FILE" = $okrsFile
            "OKRS_DIR" = ".goalkit"
            "QUARTER" = $Quarter
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }

    if ((Test-Path $okrsFile) -and (-not $DryRun)) {
        Write-Warning "OKRs file already exists: $okrsFile"
        if (-not $Force) {
            $response = Read-Host "Overwrite existing OKRs file? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Info "Operation cancelled"
                return
            }
        }
    }

    if ($DryRun) {
        Write-Info "[DRY RUN] Would create OKRs file: $okrsFile"
        return
    }

    $quarterClean = if ([string]::IsNullOrEmpty($Quarter)) { "Current Quarter" } else { $Quarter }
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

    $okrsContent = @"
# OKRs: $quarterClean

**Created**: $timestamp
**Status**: Draft

## Summary
Quarterly OKRs for $quarterClean aligned with organizational vision.

## Objectives

### Objective 1: [Objective Title]

**Confidence**: [1-5]

**Key Results**:
- KR 1.1: [Measurable target]
- KR 1.2: [Measurable target]
- KR 1.3: [Measurable target]

**Strategic Pillar**: [Pillar this objective serves]

**Anticipated Goals**: [Goals planned to achieve this objective]

---

### Objective 2: [Objective Title]

**Confidence**: [1-5]

**Key Results**:
- KR 2.1: [Measurable target]
- KR 2.2: [Measurable target]
- KR 2.3: [Measurable target]

**Strategic Pillar**: [Pillar this objective serves]

**Anticipated Goals**: [Goals planned to achieve this objective]

---

### Objective 3: [Objective Title]

**Confidence**: [1-5]

**Key Results**:
- KR 3.1: [Measurable target]
- KR 3.2: [Measurable target]
- KR 3.3: [Measurable target]

**Strategic Pillar**: [Pillar this objective serves]

**Anticipated Goals**: [Goals planned to achieve this objective]

## Dependencies & Risks
- **Key Dependencies**: [What needs to happen for OKR success]
- **Risks**: [Potential blockers]
- **Mitigations**: [How risks are addressed]

## Review Schedule
- **Mid-Quarter Check-In**: [Date]
- **End-of-Quarter Review**: [Date]
"@

    Set-Content -Path $okrsFile -Value $okrsContent -Encoding UTF8

    Write-Success "Created OKRs file: $okrsFile"

    Write-Success "OKRs setup completed!"
    Write-Host ""
    Write-Info "Next Steps:"
    Write-Host "  1. Fill in objectives and key results"
    Write-Host "  2. Review and set confidence levels"
    Write-Host "  3. Use /goalkit.goal-alignment to create aligned goals"
    Write-Host "  4. Use /goalkit.goal to define specific goals supporting these OKRs"
    Write-Host ""
}

# Main execution
New-OkrsFile -Quarter $Quarter -DryRun $DryRun -Force $Force -JsonMode $Json
