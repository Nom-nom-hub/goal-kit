param(
    [switch]$Verbose = $false,
    [switch]$DryRun = $false,
    [switch]$Json = $false,
    [string]$GoalDirectory = ""
)

# Setup milestone planning in a Goal Kit project

# Load common utilities
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. "$scriptDir\common.ps1"

# Function to display usage information
function Show-Usage {
    Write-Host "Usage: $($MyInvocation.MyCommand.Name) [OPTIONS] GOAL_DIRECTORY" -ForegroundColor Cyan
    ""
    "Setup milestone planning in the current Goal Kit project."
    ""
    "OPTIONS:"
    "    -Verbose          Enable verbose output"
    "    -DryRun          Show what would be created without creating it"
    "    -Json            Output JSON with milestone details only"
    "    -h, -?           Show this help message"
    ""
    "ARGUMENTS:"
    "    GOAL_DIRECTORY         Path to the goal directory to create milestones for"
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
    $milestoneFile = Join-Path $GoalDirectory "milestones.md"
    $branchName = $goalDirName
    
    # Output JSON with required variables using common function
    $jsonObj = @{
        GOAL_DIR = $GoalDirectory
        MILESTONE_FILE = $milestoneFile
        BRANCH_NAME = $branchName
    }
    
    Output-JsonMode $jsonObj
}

# Verify goal directory exists
if (-not (Test-Path $GoalDirectory)) {
    Write-Error "Goal directory does not exist: $GoalDirectory"
    exit 1
}

# Check if milestones.md already exists
$milestoneFile = Join-Path $GoalDirectory "milestones.md"
if (Test-Path $milestoneFile) {
    Write-Warning "Milestone file already exists: $milestoneFile"
    if (-not $DryRun) {
        $response = Read-Host "Overwrite existing milestone file? (y/N)"
        if ($response -ne "y" -and $response -ne "Y") {
            Write-Info "Operation cancelled"
            exit 0
        }
    }
}

if ($DryRun) {
    Write-Info "[DRY RUN] Would create milestone file: $milestoneFile"
    exit 0
}

# Create milestone file with basic template
$milestoneContent = @"
# Milestone Plan for $(Split-Path $GoalDirectory -Leaf)

## Overview
Milestone plan for goal: $(Split-Path $GoalDirectory -Leaf)

## Milestone Definition Framework
- **Measurable Outcomes**: Clear indicators of milestone achievement
- **Learning Objectives**: What to discover at each milestone
- **Value Delivery**: User/business value at each step
- **Implementation Approaches**: Different ways to achieve the milestone

## Progress Tracking Framework
- **Overall Progress Metrics**: How to measure goal advancement
- **Milestone Health Indicators**: Signs of milestone success or trouble
- **Adaptation Triggers**: When to adjust approach or sequence

## Review Process
- **Milestone Review Cadence**: Regular assessment schedule
- **Review Framework**: What to evaluate at each review
- **Decision Framework**: How to adapt based on results

## Success Validation
- **Milestone Success Criteria**: When milestone is considered complete
- **Goal Progress Indicators**: How milestone advances the goal
- **Learning Quality Assessment**: How to evaluate insights gained
"@

$milestoneContent | Out-File $milestoneFile -Encoding UTF8

Write-Success "Created milestone file: $milestoneFile"

# Print summary
Write-Success "Milestone planning setup completed!"
""
Write-Info "Milestone Details:"
"  Goal Directory: $GoalDirectory"
"  Milestone File: $milestoneFile"
""
Write-Info "Next Steps:"
"  1. Review and enhance the milestone plan"
"  2. Use /goalkit.execute to implement with learning and adaptation"

# Setup goal environment for immediate development
Set-GoalEnvironment -GoalDir $GoalDirectory