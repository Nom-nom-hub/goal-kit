# Setup strategy analysis in a Goal Kit project

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalDirectory,
    
    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "common.ps1")

function New-StrategyFile {
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
        $strategyFile = Join-Path $GoalDirectory "strategies.md"
        $branchName = $goalDirName
        
        # Output JSON with required variables
        $jsonOutput = @{
            "GOAL_DIR" = $GoalDirectory
            "STRATEGY_FILE" = $strategyFile
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
    
    # Check if strategies.md already exists
    $strategyFile = Join-Path $GoalDirectory "strategies.md"
    if ((Test-Path $strategyFile) -and (-not $DryRun)) {
        Write-Warning "Strategy file already exists: $strategyFile"
        if (-not $Force) {
            $response = Read-Host "Overwrite existing strategy file? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Info "Operation cancelled"
                return
            }
        } else {
            Write-Info "Overwriting strategy file due to --Force option."
        }
    }
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would create strategy file: $strategyFile"
        return
    }
    
    # Create strategy file with basic template
    $goalDirName = Split-Path -Leaf $GoalDirectory
    
    $strategyContent = @"
# Strategy Analysis for $goalDirName

## Overview
Strategy analysis for goal: $goalDirName

## Strategy Exploration Framework
- **Technical Strategy Options**: Different technologies and architectures
- **User Experience Strategies**: Various approaches to user interaction
- **Implementation Strategies**: Different development and rollout approaches

## Strategy Comparison Matrix
- **Technical Feasibility**: How practical each strategy is to implement
- **User Experience Quality**: How well each strategy serves users
- **Development Effort**: Resources required for each strategy
- **Risk Level**: Potential issues and their likelihood
- **Learning Potential**: What each strategy can teach

## Recommended Starting Strategy
- **Primary Recommendation**: Which strategy to try first
- **Rationale**: Evidence-based reasoning for the choice
- **Success Criteria**: How to validate if the strategy works
- **Fallback Options**: Alternative strategies if primary fails

## Validation Experiments
- **Critical Assumption Tests**: Experiments to validate strategy assumptions
- **Measurement Plan**: How to evaluate strategy effectiveness
- **Success Thresholds**: When strategy is considered successful
"@
    
    Set-Content -Path $strategyFile -Value $strategyContent -Encoding UTF8
    
    Write-Success "Created strategy file: $strategyFile"
    
    # Print summary
    Write-Success "Strategy analysis setup completed!"
    Write-Host ""
    Write-Info "Strategy Details:"
    Write-Host "  Goal Directory: $GoalDirectory"
    Write-Host "  Strategy File: $strategyFile"
    Write-Host ""
    
    Write-Info "Next Steps:"
    Write-Host "  1. Review and enhance the strategy analysis"
    Write-Host "  2. Use /goalkit.milestones to create measurable milestones" 
    Write-Host "  3. Use /goalkit.execute to implement with learning and adaptation"
    
    # Setup goal environment for immediate development
    if (-not (Set-GoalEnvironment $GoalDirectory)) {
        Write-Error-Custom "Failed to setup goal environment for $GoalDirectory"
        exit 1
    }
}

# Main execution
New-StrategyFile -GoalDirectory $GoalDirectory -DryRun $DryRun -Force $Force -JsonMode $Json 