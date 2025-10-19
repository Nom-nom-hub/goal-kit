param(
    [switch]$Verbose = $false,
    [switch]$CheckOnly = $false,
    [string]$GoalPath = (Get-Location)
)

# Guide user through Goal Kit methodology steps and track completion

# Load common utilities
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. "$scriptDir\common.ps1"

# Function to display usage information
function Show-Usage {
    Write-Host "Usage: $($MyInvocation.MyCommand.Name) [OPTIONS]" -ForegroundColor Cyan
    ""
    "Guide through Goal Kit methodology steps and track completion."
    ""
    "OPTIONS:"
    "    -Verbose          Enable verbose output"
    "    -CheckOnly        Only check status without guiding through steps"
    "    -h, -?           Show this help message"
    ""
    "EXAMPLES:"
    "    $($MyInvocation.MyCommand.Name)"
    "    $($MyInvocation.MyCommand.Name) -CheckOnly"
    "    $($MyInvocation.MyCommand.Name) -Verbose"
    ""
}

# Show help if requested
if ($args -contains "-h" -or $args -contains "-?") {
    Show-Usage
    exit 0
}

# Validate we're in a git repository
if (-not (Test-GitRepo)) {
    Write-Error "Not in a git repository"
    Write-Info "Please run this from the root of a Goal Kit project"
    exit 1
}

# Get project information
$projectRoot = Get-GitRoot
Set-Location $projectRoot

# Check if this is a Goal Kit project
if (-not (Test-Path ".goalkit")) {
    Write-Error "Not a Goal Kit project"
    Write-Info "Please run 'goalkeeper init' first to set up the project"
    exit 1
}

if ($Verbose) {
    Write-Info "Starting methodology guide in $projectRoot"
}

# Check if we're in a goal directory
$inGoalDir = $false
$currentDir = Get-Location
if ($currentDir.Path -like "*goals*") {
    $inGoalDir = $true
    $goalDir = $currentDir
} else {
    # Find all goals and let user select one
    if (Test-Path "goals") {
        $goalDirs = Get-ChildItem "goals" -Directory
        if ($goalDirs.Count -gt 0) {
            Write-Info "Available goals:"
            for ($i = 0; $i -lt $goalDirs.Count; $i++) {
                Write-Host "  $i. $($goalDirs[$i].Name)" -ForegroundColor Yellow
            }
            
            if ($goalDirs.Count -eq 1) {
                $selection = 0
                Write-Info "Only one goal found, selecting: $($goalDirs[$selection].Name)"
            } else {
                Write-Host "`nEnter the number of the goal to work on (or 'q' to quit): " -ForegroundColor Cyan -NoNewline
                $selection = Read-Host
                
                if ($selection -eq 'q') {
                    Write-Info "Quitting methodology guide."
                    exit 0
                }
                
                if (-not ($selection -match "^\d+$" -and [int]$selection -ge 0 -and [int]$selection -lt $goalDirs.Count)) {
                    Write-Error "Invalid selection"
                    exit 1
                }
                
                $selection = [int]$selection
            }
            
            $goalDir = $goalDirs[$selection].FullName
        } else {
            Write-Error "No goals found in this project"
            Write-Info "Use /goalkit.goal to create a goal first"
            exit 1
        }
    } else {
        Write-Error "No goals directory found"
        Write-Info "Use /goalkit.goal to create a goal first"
        exit 1
    }
}

# Check methodology completion
$methodologyComplete = Test-GoalMethodologyCompletion -GoalDir $goalDir

# If check only, exit after showing status
if ($CheckOnly) {
    Write-Info "Check completed. Exiting."
    exit 0
}

# If methodology is complete, suggest execution
if ($methodologyComplete) {
    Write-Success "[TADA] All methodology steps are complete! Ready for execution."
    Write-Info "You can now proceed with /goalkit.execute for implementation."
    exit 0
}

# If methodology is not complete, guide through remaining steps
Write-Info "Let's continue with the Goal Kit methodology for: $(Split-Path $goalDir -Leaf)"

# Check each step and guide user if incomplete
$goalFile = Join-Path $goalDir "goal.md"
$strategiesFile = Join-Path $goalDir "strategies.md"
$milestonesFile = Join-Path $goalDir "milestones.md"

# Check if goal.md is properly defined
if (Test-Path $goalFile) {
    $goalContent = Get-Content $goalFile -Raw
    if ($goalContent -match "Success Metrics" -and $goalContent -match "Target:") {
        Write-Success "[CHECK] Goal definition is properly completed"
    } else {
        Write-Warning "[WARN] Goal needs success metrics with specific targets"
        Write-Info "Open $goalFile and add specific, measurable success metrics with targets (%, $, timeframes, user counts)"
    }
} else {
    Write-Error "Goal file not found"
    exit 1
}

# Check if strategies.md exists, if not, guide user
if (-not (Test-Path $strategiesFile)) {
    Write-Step "Next Step: Create strategies for your goal"
    $createStrategies = Read-Host "`nWould you like to create strategies now? (Y/N)"
    if ($createStrategies -match "^[Yy]") {
        Write-Info "Navigate to your goal directory and run: /goalkit.strategies"
        Set-Location $goalDir
        Write-Info "Current directory: $(Get-Location)"
        Write-Goal "Run: /goalkit.strategies to explore different approaches for your goal"
    }
} else {
    $strategiesContent = Get-Content $strategiesFile -Raw
    if ($strategiesContent -match "Strategy" -and $strategiesContent -match "Validation") {
        Write-Success "[CHECK] Strategies are properly defined"
    } else {
        Write-Warning "[WARN] Strategies need validation approaches and success criteria"
    }
}

# Check if milestones.md exists, if not, guide user
if (-not (Test-Path $milestonesFile)) {
    if (Test-Path $strategiesFile) {
        Write-Step "Next Step: Create milestones for your goal"
        $createMilestones = Read-Host "`nWould you like to create milestones now? (Y/N)"
        if ($createMilestones -match "^[Yy]") {
            Write-Info "Navigate to your goal directory and run: /goalkit.milestones"
            Set-Location $goalDir
            Write-Info "Current directory: $(Get-Location)"
            Write-Goal "Run: /goalkit.milestones to create measurable progress steps"
        }
    }
} else {
    $milestonesContent = Get-Content $milestonesFile -Raw
    if ($milestonesContent -match "Milestone" -and $milestonesContent -match "Success Indicators") {
        Write-Success "[CHECK] Milestones are properly defined"
    } else {
        Write-Warning "[WARN] Milestones need success indicators and measurement approaches"
    }
}

Write-Info "`nMethodology guide completed. Use this script again to check your progress."
Write-Info "Remember to complete all steps before proceeding to execution (/goalkit.execute)."