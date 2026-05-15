# Generate portfolio overview in a Goal Kit project

param(
    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-PortfolioFile {
    param(
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

    $portfolioFile = ".goalkit/portfolio.md"
    $goalsDir = ".goalkit/goals"

    if ($JsonMode) {
        $jsonOutput = @{
            "PORTFOLIO_FILE" = $portfolioFile
            "GOALS_DIR" = $goalsDir
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }

    if ((Test-Path $portfolioFile) -and (-not $DryRun)) {
        Write-Warning "Portfolio file already exists: $portfolioFile"
        if (-not $Force) {
            $response = Read-Host "Overwrite existing portfolio file? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Info "Operation cancelled"
                return
            }
        }
    }

    if ($DryRun) {
        Write-Info "[DRY RUN] Would create portfolio file: $portfolioFile"
        return
    }

    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

    # Scan for active goals
    $goalCount = 0
    $goalList = ""

    if (Test-Path $goalsDir) {
        $goalDirs = Get-ChildItem -Path $goalsDir -Directory -ErrorAction SilentlyContinue
        foreach ($goalDir in $goalDirs) {
            $goalFile = Join-Path -Path $goalDir.FullName -ChildPath "goal.md"
            if (Test-Path $goalFile) {
                $goalCount++
                $goalName = $goalDir.Name
                $goalList += "- $goalName`n"
            }
        }
    }

    $goalListDisplay = if ([string]::IsNullOrEmpty($goalList)) { "No active goals yet. Use /goalkit.goal to create your first goal." } else { $goalList }

    $portfolioContent = @"
# Portfolio Overview

**Generated**: $timestamp
**Total Goals**: $goalCount
**On Track**: $goalCount | **At Risk**: 0 | **Completed**: 0

## Executive Summary

Portfolio health overview for the current period.

## Active Goals

$goalListDisplay

## Health Metrics
- **Average Completion**: [Calculated from goal files]
- **Average Health Score**: [Calculated from goal files]
- **Velocity**: [Goals completed per month]

## Risks & Opportunities
- **Top Risks**: [Goals at risk and mitigation plans]
- **Opportunities**: [Acceleration opportunities]

## Resource Allocation
- **Team Distribution**: [Goals by team]
- **Over/Under Allocated**: [Resource balance assessment]

## Leadership Actions
- **Decisions Needed**: [What leadership needs to decide]
- **Escalations**: [Items needing attention]
"@

    Set-Content -Path $portfolioFile -Value $portfolioContent -Encoding UTF8

    Write-Success "Created portfolio file: $portfolioFile"
    Write-Host ""
    Write-Info "Portfolio Details:"
    Write-Host "  Goals Found: $goalCount"
    Write-Host "  Portfolio File: $portfolioFile"
    Write-Host ""
    Write-Info "Next Steps:"
    Write-Host "  1. Review the portfolio overview"
    Write-Host "  2. Check goal health and risks"
    Write-Host "  3. Use /goalkit.goal to review specific goals"
    Write-Host "  4. Use /goalkit.report to generate detailed reports"
    Write-Host ""
}

# Main execution
New-PortfolioFile -DryRun $DryRun -Force $Force -JsonMode $Json
