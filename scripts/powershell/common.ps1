# Common utilities for Goal Kit PowerShell scripts

param(
    [switch]$Verbose = $false
)

# Function to write colored output
function Write-Colored {
    param(
        [string]$Message,
        [string]$Color = "White"
    )

    $colorCodes = @{
        "Red" = [ConsoleColor]::Red
        "Green" = [ConsoleColor]::Green
        "Yellow" = [ConsoleColor]::Yellow
        "Blue" = [ConsoleColor]::Blue
        "Cyan" = [ConsoleColor]::Cyan
        "White" = [ConsoleColor]::White
        "Magenta" = [ConsoleColor]::Magenta
    }

    Write-Host $Message -ForegroundColor $colorCodes[$Color]
}

function Write-Info {
    param([string]$Message)
    Write-Colored "[INFO] $Message" "Blue"
}

function Write-Success {
    param([string]$Message)
    Write-Colored "[SUCCESS] $Message" "Green"
}

function Write-Warning {
    param([string]$Message)
    Write-Colored "[WARNING] $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-Colored "[ERROR] $Message" "Red"
}

function Write-Step {
    param([string]$Message)
    Write-Colored "[STEP] $Message" "Cyan"
}

function Write-Goal {
    param([string]$Message)
    Write-Colored "[GOAL] $Message" "Magenta"
}

# Check if command exists
function Test-CommandExists {
    param([string]$Command)

    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Check if we're in a git repository
function Test-GitRepo {
    try {
        $gitDir = git rev-parse --git-dir 2>$null
        return $null -ne $gitDir
    }
    catch {
        return $false
    }
}

# Get the root directory of the current git repository
function Get-GitRoot {
    try {
        return git rev-parse --show-toplevel
    }
    catch {
        return $null
    }
}

# Check if required tools are installed
function Test-Prerequisites {
    $missingTools = @()

    if (-not (Test-CommandExists "git")) {
        $missingTools += "git"
    }

    if (-not (Test-CommandExists "uv")) {
        $missingTools += "uv"
    }

    if ($missingTools.Count -gt 0) {
        Write-Error "Missing required tools: $($missingTools -join ', ')"
        Write-Info "Please install the missing tools and try again."
        exit 1
    }

    Write-Success "All prerequisites are installed"
}

# Create a new branch for the current goal
function New-GoalBranch {
    param([string]$GoalName)

    $branchName = $GoalName

    # Check if branch already exists
    $existingBranches = git branch -a | Where-Object { $_ -match $branchName }

    if ($existingBranches) {
        Write-Info "Branch $branchName already exists, switching to it"
        git checkout $branchName
    }
    else {
        Write-Info "Creating new branch: $branchName"
        git checkout -b $branchName
    }

    return $branchName
}

# Update the agent context file with current goal information
function Update-AgentContext {
    $projectRoot = Get-GitRoot
    $currentDir = Get-Location
    $goalName = Split-Path $currentDir -Leaf

    # Look for agent-specific context files
    $contextFiles = @(
        "CLAUDE.md",
        ".claude\context.md",
        "GEMINI.md",
        ".gemini\context.md",
        "CURSOR.md",
        ".cursor\context.md"
    )

    foreach ($contextFile in $contextFiles) {
        $fullPath = Join-Path $projectRoot $contextFile
        if (Test-Path $fullPath) {
            Write-Info "Updating context in $contextFile"

            $contextContent = @"
// Goal Kit Project Context

**Project**: $(Split-Path $projectRoot -Leaf)
**Branch**: $(git branch --show-current)
**Active Goals**: $(Get-ChildItem "goals" -Directory | Measure-Object | Select-Object -ExpandProperty Count)
**Updated**: $(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")

## 🎯 Goal-Driven Development Status

This project uses Goal-Driven Development methodology. Focus on:
- Measurable outcomes over feature specifications
- Multiple strategy exploration before implementation
- Learning and adaptation during execution
- Success metrics validation

## 📋 Available Commands

### Core Commands
- **/goalkit.vision** - Establish project vision and principles
- **/goalkit.goal** - Define goals and success criteria
- **/goalkit.strategies** - Explore implementation strategies
- **/goalkit.milestones** - Create measurable milestones
- **/goalkit.execute** - Execute with learning and adaptation



## 🚀 Project Vision

$(if (Test-Path ".goalkit\vision.md") { Get-Content ".goalkit\vision.md" -Head 10 | Where-Object { $_ -notlike "#*" } | Select-Object -First 5 })

## 🎯 Active Goals

$(if (Test-Path "goals") {
    $goals = Get-ChildItem "goals" -Directory
    if ($goals) {
        "Recent goals:"
        $goals | ForEach-Object {
            $goalDir = $_.FullName
            $goalStatement = Get-Content "$goalDir\goal.md" -ErrorAction SilentlyContinue |
                Where-Object { $_ -like "*Goal Statement*" } |
                Select-Object -First 1 |
                ForEach-Object { $_ -replace ".*Goal Statement:\s*", "" }
            $statement = if ($goalStatement) { $goalStatement } else { "Goal definition in progress" }
            "- **$($_.Name)**: $statement"
        } | Select-Object -First 3
    } else {
        "No active goals yet. Use /goalkit.goal to create your first goal."
    }
})

## 📊 Development Principles

Remember these core principles:
1. **Outcome-First**: Prioritize user and business outcomes
2. **Strategy Flexibility**: Multiple valid approaches exist for any goal
3. **Measurement-Driven**: Progress must be measured and validated
4. **Learning Integration**: Treat implementation as hypothesis testing
5. **Adaptive Planning**: Change course based on evidence

## 🔧 Next Recommended Actions

$(if (-not (Test-Path "goals") -or @(Get-ChildItem "goals" -Directory).Count -eq 0) {
    "1. Use /goalkit.vision to establish project vision"
    "2. Use /goalkit.goal to define first goal"
} else {
    "1. Review active goals in goals/ directory"
    "2. Use /goalkit.strategies to explore implementation approaches"
    "3. Use /goalkit.milestones to plan measurable progress steps"
})

---

*This context is automatically updated by update-agent-context.ps1. Last updated: $(Get-Date)*

"@

            $contextContent | Out-File $fullPath -Encoding UTF8
            return
        }
    }

    Write-Warning "No agent context file found to update"
}

# Validate that we're in a goal directory
function Test-GoalContext {
    $currentDir = Get-Location

    # Check if we're in a goals subdirectory
    if ($currentDir.Path -notlike "*goals*") {
        Write-Error "Not in a goal directory"
        Write-Info "Please navigate to a goal directory (e.g., goals/001-user-authentication/)"
        exit 1
    }

    # Check for required goal files
    $requiredFiles = @("goal.md")
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            Write-Error "Missing required file: $file"
            exit 1
        }
    }

    Write-Success "Goal context validated"
}

# Check if the current goal has completed all required methodology steps
function Test-GoalMethodologyCompletion {
    param(
        [string]$GoalDir = (Get-Location)
    )
    
    $goalFile = Join-Path $GoalDir "goal.md"
    $strategiesFile = Join-Path $GoalDir "strategies.md"
    $milestonesFile = Join-Path $GoalDir "milestones.md"
    $executionFile = Join-Path $GoalDir "execution.md"
    
    $completedSteps = 0
    $totalSteps = 4  # goal, strategies, milestones, execution
    
    Write-Info "Checking methodology completion for goal: $(Split-Path $GoalDir -Leaf)"
    
    # Check if goal.md exists and has content
    if (Test-Path $goalFile) {
        $goalContent = Get-Content $goalFile -Raw
        # Basic check: does the goal have success metrics defined?
        if ($goalContent -match "Success Metrics" -and $goalContent -match "Target:") {
            Write-Success "`u{2714} Goal definition complete with success metrics"
            $completedSteps++
        } else {
            Write-Warning "`u{26A0} Goal definition needs success metrics with specific targets"
        }
    } else {
        Write-Error "Missing goal.md file"
    }
    
    # Check if strategies.md exists and has content
    if (Test-Path $strategiesFile) {
        $strategiesContent = Get-Content $strategiesFile -Raw
        if ($strategiesContent -match "Strategy" -and $strategiesContent -match "Validation") {
            Write-Success "`u{2714} Strategies defined with validation approaches"
            $completedSteps++
        } else {
            Write-Warning "`u{26A0} Strategies need validation approaches and success criteria"
        }
    } else {
        Write-Warning "`u{26A0} No strategies.md found - consider using /goalkit.strategies"
    }
    
    # Check if milestones.md exists and has content
    if (Test-Path $milestonesFile) {
        $milestonesContent = Get-Content $milestonesFile -Raw
        if ($milestonesContent -match "Milestone" -and $milestonesContent -match "Success Indicators") {
            Write-Success "`u{2714} Milestones defined with success indicators"
            $completedSteps++
        } else {
            Write-Warning "`u{26A0} Milestones need success indicators and measurement approaches"
        }
    } else {
        Write-Warning "`u{26A0} No milestones.md found - consider using /goalkit.milestones"
    }
    
    # Check if execution.md exists and has content
    if (Test-Path $executionFile) {
        $executionContent = Get-Content $executionFile -Raw
        if ($executionContent -match "Execution" -and $executionContent -match "Strategy") {
            Write-Success "`u{2714} Execution plan defined with strategy"
            $completedSteps++
        } else {
            Write-Warning "`u{26A0} Execution plan may need more detail"
        }
    } else {
        Write-Warning "`u{26A0} No execution.md found - consider using /goalkit.execute"
    }
    
    $completionPercent = [math]::Round(($completedSteps / $totalSteps) * 100)
    Write-Info "Methodology completion: $completionPercent% ($completedSteps of $totalSteps steps)"
    
    if ($completedSteps -eq $totalSteps) {
        Write-Success "[CHECK] All methodology steps completed! Ready for execution."
        return $true
    } else {
        Write-Warning "[WARN] Some methodology steps are incomplete. We recommend completing all steps before execution."
        Write-Info "Consider using the following commands to complete missing steps:"
        
        if (!(Test-Path $strategiesFile)) {
            Write-Step "1. /goalkit.strategies - Explore implementation strategies"
        }
        
        if (!(Test-Path $milestonesFile)) {
            Write-Step "2. /goalkit.milestones - Create measurable milestones"
        }
        
        if (!(Test-Path $executionFile)) {
            Write-Step "3. /goalkit.execute - Execute with learning and adaptation"
        }
        
        return $false
    }
}

# Get the goal name from current directory
function Get-CurrentGoalName {
    return Split-Path (Get-Location) -Leaf
}

# Print a summary of the current goal
function Show-GoalSummary {
    param([string]$GoalDir)

    if (Test-Path "$GoalDir\goal.md") {
        Write-Info "Current Goal Summary:"
        ""

        # Extract and display key information from goal.md
        Get-Content "$GoalDir\goal.md" | Where-Object {
            $_ -like "*Goal Statement*" -or $_ -like "*Success Metrics*"
        } | Select-Object -First 10
        ""
    }
}

# Check if a command is available in the current agent
function Test-AgentCommand {
    param([string]$Command)

    # This would need to be implemented based on the specific agent
    # For now, we'll assume the command is available if we're in a goal-kit project
    return $true
}

# Setup environment variables for goal development
function Set-GoalEnvironment {
    param([string]$GoalDir)

    $env:GOAL_KIT_PROJECT_ROOT = Get-GitRoot
    $env:GOAL_KIT_GOAL_DIR = $GoalDir
    $env:GOAL_KIT_GOAL_NAME = Split-Path $GoalDir -Leaf

    Write-Info "Goal environment configured"
    Write-Info "  Project Root: $env:GOAL_KIT_PROJECT_ROOT"
    Write-Info "  Goal Directory: $env:GOAL_KIT_GOAL_DIR"
    Write-Info "  Goal Name: $env:GOAL_KIT_GOAL_NAME"
}

# Cleanup function for error handling
function Cleanup-OnError {
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) {
        Write-Error "Script failed with exit code $exitCode"
        # Add any cleanup logic here
    }
    exit $exitCode
}

# Set up error handling
trap {
    Cleanup-OnError
}

# Common function for JSON mode output
function Output-JsonMode {
    param([object]$JsonData)
    
    $jsonOutput = $JsonData | ConvertTo-Json -Compress
    Write-Output $jsonOutput
    exit 0
}

Write-Info "Goal Kit PowerShell utilities loaded"