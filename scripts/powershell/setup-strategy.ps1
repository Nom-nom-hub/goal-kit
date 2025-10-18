param(
    [switch]$Verbose = $false,
    [switch]$DryRun = $false,
    [switch]$Json = $false,
    [string]$GoalDirectory = ""
)

# Setup strategy analysis in a Goal Kit project

# Load common utilities
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. "$scriptDir\common.ps1"

# Function to display usage information
function Show-Usage {
    Write-Host "Usage: $($MyInvocation.MyCommand.Name) [OPTIONS] GOAL_DIRECTORY" -ForegroundColor Cyan
    ""
    "Setup strategy analysis in the current Goal Kit project."
    ""
    "OPTIONS:"
    "    -Verbose          Enable verbose output"
    "    -DryRun          Show what would be created without creating it"
    "    -Json            Output JSON with strategy details only"
    "    -h, -?           Show this help message"
    ""
    "ARGUMENTS:"
    "    GOAL_DIRECTORY         Path to the goal directory to analyze"
    ""
    "EXAMPLES:"
    "    $($MyInvocation.MyCommand.Name) goals\001-user-authentication"
    "    $($MyInvocation.MyCommand.Name) -DryRun 'goals\001-user-authentication'"
    "    $($MyInvocation.MyCommand.Name) -Json 'goals\001-user-authentication'"
    "    $($MyInvocation.MyCommand.Name) -Verbose 'goals\001-user-authentication'"
    ""
}

# Show help if requested
if ($args -contains "-h" -or $args -contains "-?") {
    Show-Usage
    exit 0
}

# Validate arguments
if ($GoalDirectory -eq "") {
    Write-Error "Goal directory is required"
    Show-Usage
    exit 1
}

# Check if we're in a git repository
if (-not (Test-GitRepo)) {
    Write-Error "Not in a git repository"
    Write-Info "Please run this from the root of a Goal Kit project"
    exit 1
}

# Get project root
$projectRoot = Get-GitRoot
Set-Location $projectRoot

# If JSON mode, output JSON and exit early
if ($Json) {
    # Check if goal directory exists
    if (-not (Test-Path $GoalDirectory)) {
        Write-Error "Goal directory does not exist: $GoalDirectory"
        exit 1
    }
    
    # Get goal directory name without path
    $goalDirName = Split-Path $GoalDirectory -Leaf
    $strategyFile = Join-Path $GoalDirectory "strategies.md"
    $branchName = $goalDirName
    
    # Output JSON with required variables using common function
    $jsonObj = @{
        GOAL_DIR = $GoalDirectory
        STRATEGY_FILE = $strategyFile
        BRANCH_NAME = $branchName
    }
    
    Output-JsonMode $jsonObj
}

# Verify goal directory exists
if (-not (Test-Path $GoalDirectory)) {
    Write-Error "Goal directory does not exist: $GoalDirectory"
    exit 1
}

# Check if strategies.md already exists
$strategyFile = Join-Path $GoalDirectory "strategies.md"
if (Test-Path $strategyFile) {
    Write-Warning "Strategy file already exists: $strategyFile"
    if (-not $DryRun) {
        $response = Read-Host "Overwrite existing strategy file? (y/N)"
        if ($response -ne "y" -and $response -ne "Y") {
            Write-Info "Operation cancelled"
            exit 0
        }
    }
}

if ($DryRun) {
    Write-Info "[DRY RUN] Would create strategy file: $strategyFile"
    exit 0
}

# Create strategy file with basic template
$strategyContent = @"
# Strategy Analysis for $(Split-Path $GoalDirectory -Leaf)

## Overview
Strategy analysis for goal: $(Split-Path $GoalDirectory -Leaf)

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

$strategyContent | Out-File $strategyFile -Encoding UTF8

Write-Success "Created strategy file: $strategyFile"

# Print summary
Write-Success "Strategy analysis setup completed!"
""
Write-Info "Strategy Details:"
"  Goal Directory: $GoalDirectory"
"  Strategy File: $strategyFile"
""
Write-Info "Next Steps:"
"  1. Review and enhance the strategy analysis"
"  2. Use /goalkit.milestones to create measurable milestones" 
"  3. Use /goalkit.execute to implement with learning and adaptation"

# Setup goal environment for immediate development
Set-GoalEnvironment -GoalDir $GoalDirectory