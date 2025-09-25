param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalName,

    [Parameter(Mandatory=$false)]
    [string]$Category = "personal",

    [Parameter(Mandatory=$false)]
    [string]$Priority = "medium",

    [Parameter(Mandatory=$false)]
    [string]$Deadline,

    [Parameter(Mandatory=$false)]
    [string]$Template = "standard",

    [Parameter(Mandatory=$false)]
    [string]$OutputDir = "$env:USERPROFILE\goals",

    [Parameter(Mandatory=$false)]
    [switch]$Verbose,

    [Parameter(Mandatory=$false)]
    [switch]$Help
)

# Goal-Kit PowerShell Goal Creation Script
# Creates new goal projects with proper structure and templates

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$GoalKitDir = Split-Path -Parent $ScriptDir
$TemplatesDir = Join-Path $GoalKitDir "templates"
$DefaultGoalDir = $env:USERPROFILE + "\goals"

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$NC = "White"

# Utility functions
function Write-Info {
    param([string]$Message)
    Write-Host "[$Blue]INFO[$NC] $Message" -ForegroundColor $Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[$Green]SUCCESS[$NC] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[$Yellow]WARNING[$NC] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[$Red]ERROR[$NC] $Message" -ForegroundColor $Red
}

function Show-Help {
    Write-Host "Goal-Kit PowerShell Goal Creation Script" -ForegroundColor $Green
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor $Yellow
    Write-Host "    .\create-goal.ps1 [OPTIONS] GOAL_NAME" -ForegroundColor $White
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor $Yellow
    Write-Host "    -Category CATEGORY    Goal category (personal, business, learning, software, research)" -ForegroundColor $White
    Write-Host "    -Priority PRIORITY    Priority level (low, medium, high, critical)" -ForegroundColor $White
    Write-Host "    -Deadline DEADLINE    Target completion date (YYYY-MM-DD)" -ForegroundColor $White
    Write-Host "    -Template TEMPLATE    Template to use (standard, learning-goal, business-goal, etc.)" -ForegroundColor $White
    Write-Host "    -OutputDir DIR        Output directory (default: ~/goals)" -ForegroundColor $White
    Write-Host "    -Verbose              Verbose output" -ForegroundColor $White
    Write-Host "    -Help                 Show this help message" -ForegroundColor $White
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor $Yellow
    Write-Host "    .\create-goal.ps1 'Learn Python Data Science' -Category learning -Priority high -Deadline 2024-12-31" -ForegroundColor $White
    Write-Host "    .\create-goal.ps1 'Launch SaaS Product' -Category business -Template business-goal -OutputDir ./projects" -ForegroundColor $White
    Write-Host "    .\create-goal.ps1 'Build Mobile App' -Category software -Priority high -Verbose" -ForegroundColor $White
}

# Validate dependencies
function Test-Dependencies {
    $missingDeps = @()

    try {
        $jqVersion = & jq --version 2>$null
        if (-not $jqVersion) {
            $missingDeps += "jq"
        }
    }
    catch {
        $missingDeps += "jq"
    }

    try {
        $gitVersion = & git --version 2>$null
        if (-not $gitVersion) {
            Write-Warning "git not found - version control features will be limited"
        }
    }
    catch {
        Write-Warning "git not found - version control features will be limited"
    }

    if ($missingDeps.Count -gt 0) {
        Write-Error "Missing required dependencies: $($missingDeps -join ', ')"
        Write-Info "Please install the missing dependencies and try again."
        exit 1
    }
}

# Validate input parameters
function Test-Input {
    param([string]$GoalName)

    if (-not $GoalName) {
        Write-Error "Goal name is required"
        Show-Help
        exit 1
    }

    # Validate goal name format (no special characters except spaces, hyphens, underscores)
    if ($GoalName -notmatch "^[a-zA-Z0-9\s_-]+$") {
        Write-Error "Goal name contains invalid characters. Use only letters, numbers, spaces, hyphens, and underscores."
        exit 1
    }
}

# Validate template exists
function Test-Template {
    param([string]$Template)

    $templateFile = Join-Path $TemplatesDir "$Template.json"

    if (-not (Test-Path $templateFile)) {
        Write-Error "Template '$Template' not found in $TemplatesDir"
        Write-Info "Available templates:"
        Get-ChildItem "$TemplatesDir\*.json" | ForEach-Object {
            $templateName = $_.Name -replace '\.json$'
            Write-Host "  - $templateName" -ForegroundColor $Green
        }
        exit 1
    }

    if ($Verbose) {
        Write-Info "Using template: $templateFile"
    }
}

# Create goal directory structure
function New-GoalStructure {
    param(
        [string]$GoalName,
        [string]$OutputDir
    )

    $goalDir = Join-Path $OutputDir $GoalName

    if (Test-Path $goalDir) {
        Write-Error "Goal directory already exists: $goalDir"
        Write-Info "Use a different name or remove the existing directory."
        exit 1
    }

    Write-Info "Creating goal directory structure..."

    # Create main directory
    New-Item -ItemType Directory -Path $goalDir -Force | Out-Null

    # Create subdirectories
    $subdirs = @("milestones", "achievements", "progress", "templates", "docs")
    foreach ($subdir in $subdirs) {
        New-Item -ItemType Directory -Path (Join-Path $goalDir $subdir) -Force | Out-Null
    }

    if ($Verbose) {
        Write-Success "Created directory structure at: $goalDir"
    }
}

# Generate goal ID
function New-GoalId {
    param([string]$GoalName)

    $timestamp = Get-Date -Format "yyyyMMddHHmmss"
    $shortName = $GoalName.ToLower() -replace '[^a-z0-9]', '-' | Select-Object -First 20
    return "goal-${timestamp}-${shortName}"
}

# Create goal configuration file
function New-GoalFile {
    param(
        [string]$GoalName,
        [string]$GoalId,
        [string]$Category,
        [string]$Priority,
        [string]$Deadline,
        [string]$Template,
        [string]$GoalDir
    )

    $goalFile = Join-Path $GoalDir "goal.json"

    Write-Info "Creating goal configuration file..."

    # Read template file
    $templateFile = Join-Path $TemplatesDir "$Template.json"
    $templateContent = Get-Content $templateFile -Raw | ConvertFrom-Json

    # Update template with goal-specific information
    $createdAt = Get-Date -Format "o" -AsUTC
    $definedAt = $createdAt

    # Update the template object
    $templateContent.name = $GoalName
    $templateContent.metadata.template = $Template
    $templateContent.created_at = $createdAt
    $templateContent.defined_at = $definedAt
    $templateContent.deadline = $Deadline
    $templateContent.category = $Category
    $templateContent.priority = $Priority

    # Write the updated content to the goal file
    $templateContent | ConvertTo-Json -Depth 10 | Set-Content $goalFile

    if ($Verbose) {
        Write-Success "Created goal file: $goalFile"
    }
}

# Initialize git repository
function Initialize-GitRepo {
    param(
        [string]$GoalDir,
        [string]$GoalName
    )

    Write-Info "Initializing Git repository..."

    Push-Location $GoalDir

    # Initialize git repo
    & git init --quiet 2>$null

    # Create .gitignore
    @"
# Goal-Kit specific
*.log
*.tmp
.DS_Store
Thumbs.db

# Progress and temporary files
progress/auto-save-*
temp/
cache/

# Sensitive data
.env
.env.local
secrets.json

# OS generated files
*.swp
*.swo
*~
"@ | Set-Content .gitignore

    # Initial commit
    & git add . 2>$null
    & git commit -m "Initial goal setup: $GoalName" --quiet 2>$null

    Pop-Location

    if ($Verbose) {
        Write-Success "Git repository initialized"
    }
}

# Create README file
function New-Readme {
    param(
        [string]$GoalName,
        [string]$GoalDir
    )

    $readmeFile = Join-Path $GoalDir "README.md"

    Write-Info "Creating README file..."

    $readmeContent = @"
# $GoalName

## Goal Overview

**Goal ID:** [Generated ID]
**Category:** $Category
**Priority:** $Priority
**Created:** $(Get-Date -Format 'yyyy-MM-dd')
$(if ($Deadline) { "**Deadline:** $Deadline" })

## Description

[Goal description will be added here]

## Progress Tracking

- **Milestones:** [Number] defined milestones
- **Status:** Active
- **Progress:** 0%

## Getting Started

1. Review the goal definition in `goal.json`
2. Check milestones in the `milestones/` directory
3. Update progress regularly using progress tracking tools
4. Commit changes to track your journey

## Directory Structure

```
$GoalName/
├── goal.json              # Main goal configuration
├── README.md              # This file
├── milestones/            # Milestone definitions
├── achievements/          # Achievement documentation
├── progress/              # Progress reports and metrics
├── templates/             # Goal-specific templates
└── docs/                  # Additional documentation
```

## Quick Commands

```powershell
# Update progress
goal progress update --progress 25

# Add new milestone
goal milestone add "New Milestone" --duration 2

# Generate progress report
goal progress report --format markdown
```

## Notes

- Keep this README updated with important information
- Use the milestones directory to track major achievements
- Regular progress updates help maintain momentum
- Celebrate achievements as you reach them!

---

*Created with Goal-Kit on $(Get-Date -Format 'yyyy-MM-dd')*
"@

    $readmeContent | Set-Content $readmeFile

    if ($Verbose) {
        Write-Success "Created README file: $readmeFile"
    }
}

# Main execution
function Main {
    Write-Info "Goal-Kit PowerShell Goal Creation Script v1.0"
    Write-Info "=============================================="

    # Show help if requested
    if ($Help) {
        Show-Help
        return
    }

    # Validate input
    Test-Input $GoalName

    # Check dependencies
    Test-Dependencies

    # Validate template
    Test-Template $Template

    # Create directory structure
    New-GoalStructure $GoalName $OutputDir

    # Generate goal ID
    $goalId = New-GoalId $GoalName

    # Get full path for goal directory
    $goalDir = Join-Path $OutputDir $GoalName

    # Create goal configuration
    New-GoalFile $GoalName $goalId $Category $Priority $Deadline $Template $goalDir

    # Initialize git repository
    Initialize-GitRepo $goalDir $GoalName

    # Create README
    New-Readme $GoalName $goalDir

    # Success message
    Write-Success "Goal project '$GoalName' created successfully!"
    Write-Info "Location: $goalDir"
    Write-Info "Goal ID: $goalId"
    Write-Host ""
    Write-Info "Next steps:"
    Write-Info "1. Review and customize your goal in: $goalDir\goal.json"
    Write-Info "2. Start working on the first milestone"
    Write-Info "3. Update progress regularly"
    Write-Info "4. Use 'goal progress' commands to track your journey"
    Write-Host ""
    Write-Info "Happy goal achievement! 🎯"
}

# Run main function
Main