param(
    [switch]$Verbose = $false,
    [switch]$JsonOutput = $false,
    [string]$ProjectPath = (Get-Location)
)

# Validate all goals in a Goal Kit project and measure methodology adherence

# Load common utilities
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. "$scriptDir\common.ps1"

# Function to display usage information
function Show-Usage {
    Write-Host "Usage: $($MyInvocation.MyCommand.Name) [OPTIONS]" -ForegroundColor Cyan
    ""
    "Validate all goals in a Goal Kit project and measure methodology adherence."
    ""
    "OPTIONS:"
    "    -Verbose          Enable verbose output"
    "    -JsonOutput       Output results in JSON format"
    "    -h, -?           Show this help message"
    ""
    "EXAMPLES:"
    "    $($MyInvocation.MyCommand.Name)"
    "    $($MyInvocation.MyCommand.Name) -JsonOutput"
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

# Initialize tracking variables
$totalGoals = 0
$completedGoals = 0
$totalSteps = 0
$completedSteps = 0
$adherenceDetails = @()

# Check if goals directory exists
if (Test-Path "goals") {
    $goalDirs = Get-ChildItem "goals" -Directory
    
    foreach ($goalDir in $goalDirs) {
        $totalGoals++
        
        $goalName = $goalDir.Name
        $goalPath = $goalDir.FullName
        
        # Check each methodology step
        $steps = @{
            "Goal Definition" = Join-Path $goalPath "goal.md"
            "Strategies" = Join-Path $goalPath "strategies.md"
            "Milestones" = Join-Path $goalPath "milestones.md"
            "Execution" = Join-Path $goalPath "execution.md"
        }
        
        $goalCompletedSteps = 0
        $goalTotalSteps = $steps.Count
        
        foreach ($stepName in $steps.Keys) {
            $stepPath = $steps[$stepName]
            $totalSteps++
            
            if (Test-Path $stepPath) {
                # For strategies, milestones, and execution, verify they have content
                if ($stepName -ne "Goal Definition") {
                    $content = Get-Content $stepPath -Raw
                    if ($content.Length -gt 50) {  # Basic check for substantial content
                        $completedSteps++
                        $goalCompletedSteps++
                        if ($Verbose) {
                            Write-Success "✓ $stepName completed for $goalName"
                        }
                    } else {
                        if ($Verbose) {
                            Write-Warning "⚠ $stepName exists but may lack sufficient content for $goalName"
                        }
                    }
                } else {
                    # For goal definition, check if it has success metrics
                    $content = Get-Content $stepPath -Raw
                    if ($content -match "Success Metrics" -and $content -match "Target:") {
                        $completedSteps++
                        $goalCompletedSteps++
                        if ($Verbose) {
                            Write-Success "✓ Goal Definition completed with metrics for $goalName"
                        }
                    } else {
                        if ($Verbose) {
                            Write-Warning "⚠ Goal Definition exists but lacks specific success metrics for $goalName"
                        }
                    }
                }
            } else {
                if ($Verbose) {
                    Write-Warning "⚠ $stepName not completed for $goalName"
                }
            }
        }
        
        # Calculate completion percentage for this goal
        $goalCompletionPercent = [math]::Round(($goalCompletedSteps / $goalTotalSteps) * 100)
        
        if ($goalCompletionPercent -eq 100) {
            $completedGoals++
        }
        
        # Add to details array
        $adherenceDetails += @{
            "GoalName" = $goalName
            "CompletedSteps" = $goalCompletedSteps
            "TotalSteps" = $goalTotalSteps
            "CompletionPercent" = $goalCompletionPercent
        }
        
        if ($Verbose) {
            Write-Info "Goal '$goalName' completion: $goalCompletionPercent% ($goalCompletedSteps/$goalTotalSteps)"
        }
    }
} else {
    if ($Verbose) {
        Write-Warning "No goals directory found"
    }
}

# Calculate overall adherence
$overallAdherence = if ($totalSteps -gt 0) { [math]::Round(($completedSteps / $totalSteps) * 100) } else { 0 }
$completedGoalsPercent = if ($totalGoals -gt 0) { [math]::Round(($completedGoals / $totalGoals) * 100) } else { 0 }

# Output results
if ($JsonOutput) {
    $result = @{
        "OverallAdherence" = $overallAdherence
        "TotalGoals" = $totalGoals
        "CompletedGoals" = $completedGoals
        "CompletedGoalsPercent" = $completedGoalsPercent
        "TotalSteps" = $totalSteps
        "CompletedSteps" = $completedSteps
        "GoalDetails" = $adherenceDetails
        "Timestamp" = $(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    }
    
    $result | ConvertTo-Json -Depth 3
} else {
    Write-Info "==========================================="
    Write-Info "GOAL KIT METHODOLOGY ADHERENCE REPORT"
    Write-Info "==========================================="
    Write-Info "Project: $(Split-Path $projectRoot -Leaf)"
    Write-Info "Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")"
    Write-Info ""
    
    Write-Info "Overall Methodology Adherence: $overallAdherence% ($completedSteps/$totalSteps steps)"
    Write-Info "Goals with all steps completed: $completedGoalsPercent% ($completedGoals/$totalGoals goals)"
    Write-Info ""
    
    if ($adherenceDetails.Count -gt 0) {
        Write-Info "Goal-by-Goal Breakdown:"
        foreach ($detail in $adherenceDetails) {
            $status = if ($detail.CompletionPercent -eq 100) { "✅" } else { "⏳" }
            Write-Host "  $status $($detail.GoalName): $($detail.CompletionPercent)% ($($detail.CompletedSteps)/$($detail.TotalSteps))" -ForegroundColor $(if ($detail.CompletionPercent -eq 100) { "Green" } else { "Yellow" })
        }
        Write-Info ""
    }
    
    # Provide recommendations based on adherence
    if ($overallAdherence -lt 30) {
        Write-Warning "⚠ Low adherence detected. Consider reviewing /goalkit methodology fundamentals."
        Write-Step "1. Ensure all goals have specific success metrics"
        Write-Step "2. Develop strategy options for each goal"
        Write-Step "3. Define measurable milestones"
    } elseif ($overallAdherence -lt 70) {
        Write-Info "💡 Moderate adherence. Work on completing missing methodology steps."
        Write-Step "1. Review goals with incomplete steps"
        Write-Step "2. Complete any missing strategy, milestone, or execution planning"
    } else {
        Write-Success "🎉 High adherence! Continue following the methodology for consistent results."
    }
    
    Write-Info ""
    Write-Info "==========================================="
}