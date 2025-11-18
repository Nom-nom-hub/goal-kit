# Create a new goal in a Goal Kit project

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalDescription,
    
    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false,
    [switch]$Verbose = $false
)

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "common.ps1")

function New-Goal {
    param(
        [string]$GoalDescription,
        [bool]$DryRun,
        [bool]$Force,
        [bool]$JsonMode,
        [bool]$VerboseMode
    )
    
    # Validate arguments
    if ([string]::IsNullOrEmpty($GoalDescription)) {
        Write-Error-Custom "Goal description is required"
        exit 1
    }
    
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
    
    # Check if this is a Goal Kit project
    $visionFile = Join-Path ".goalkit" "vision.md"
    if (-not (Test-Path $visionFile)) {
        Write-Error-Custom "Not a Goal Kit project"
        Write-Info "Please run 'goalkeeper init' first to set up the project"
        exit 1
    }
    
    # If JSON mode, output JSON and exit early
    if ($JsonMode) {
        $goalsDir = Join-Path ".goalkit" "goals"
        $nextNumber = 1
        
        if (Test-Path $goalsDir) {
            $goalDirs = Get-ChildItem -Path $goalsDir -Directory -ErrorAction SilentlyContinue
            foreach ($dir in $goalDirs) {
                if ($dir.Name -match '^(\d+)-') {
                    $num = [int]$matches[1]
                    if ($num -ge $nextNumber) {
                        $nextNumber = $num + 1
                    }
                }
            }
        }
        
        # Create goal directory name
        $goalNumber = "{0:D3}" -f $nextNumber
        $cleanDescription = $GoalDescription -replace '[^a-zA-Z0-9 -]', ''
        $cleanDescription = $cleanDescription -replace '\s+', '-' -replace '-$', ''
        $cleanDescription = $cleanDescription.ToLower()
        $goalDirName = "$goalNumber-$cleanDescription"
        $goalDir = Join-Path ".goalkit" "goals" $goalDirName
        $goalFile = Join-Path $goalDir "goal.md"
        
        # Output JSON with required variables
        $jsonOutput = @{
            "GOAL_DIR" = $goalDir
            "GOAL_FILE" = $goalFile
            "GOAL_DESCRIPTION" = $GoalDescription
            "BRANCH_NAME" = $goalDirName
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }
    
    # Check if goals directory exists
    $goalsDir = Join-Path ".goalkit" "goals"
    if (-not (Test-Path $goalsDir)) {
        if ($DryRun) {
            Write-Info "[DRY RUN] Would create goals directory: $goalsDir"
        } else {
            New-Item -ItemType Directory -Path $goalsDir -Force | Out-Null
            Write-Success "Created goals directory: $goalsDir"
        }
    }
    
    # Find the next goal number
    $nextNumber = 1
    if (Test-Path $goalsDir) {
        $goalDirs = Get-ChildItem -Path $goalsDir -Directory -ErrorAction SilentlyContinue
        foreach ($dir in $goalDirs) {
            if ($dir.Name -match '^(\d+)-') {
                $num = [int]$matches[1]
                if ($num -ge $nextNumber) {
                    $nextNumber = $num + 1
                }
            }
        }
    }
    
    # Create goal directory name
    $goalNumber = "{0:D3}" -f $nextNumber
    $cleanDescription = $GoalDescription -replace '[^a-zA-Z0-9 -]', ''
    $cleanDescription = $cleanDescription -replace '\s+', '-' -replace '-$', ''
    $cleanDescription = $cleanDescription.ToLower()
    $goalDirName = "$goalNumber-$cleanDescription"
    $goalDir = Join-Path ".goalkit" "goals" $goalDirName
    $fullGoalDir = Join-Path $projectRoot $goalDir
    
    # Check if goal directory already exists
    if (Test-Path $fullGoalDir) {
        if (-not $Force) {
            Write-Error-Custom "Goal directory already exists: $goalDir"
            Write-Info "Use a different goal description or remove the existing directory"
            exit 1
        } else {
            if ($VerboseMode) {
                Write-Info "Overwriting existing goal directory: $goalDir"
            }
        }
    }
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would create goal directory: $goalDir"
        Write-Info "[DRY RUN] Would create goal.md with description: $GoalDescription"
        Write-Info "[DRY RUN] Would create branch: $goalDirName"
        return
    }
    
    # Create goal directory
    New-Item -ItemType Directory -Path $fullGoalDir -Force | Out-Null
    Write-Success "Created goal directory: $goalDir"
    
    # Get current timestamp
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    
    # Create goal.md file with goal structure
    $goalContent = @"
# Goal Statement: $GoalDescription

**Branch**: \`$goalDirName\`
**Created**: $timestamp
**Status**: Draft
**Methodology**: Goal-Driven Development

## 🎯 Goal Definition

**Goal Statement**: $GoalDescription

**Context**: [Why is this goal important? What problem does it solve?]

**Success Level**: [What "successful goal achievement" looks like]

## 📊 Success Metrics

### Primary Metrics (Must achieve for successful goal completion)

- **Metric 1**: [Measurable outcome 1] - Target: [specific, quantifiable target]
- **Metric 2**: [Measurable outcome 2] - Target: [specific, quantifiable target] 
- **Metric 3**: [Measurable outcome 3] - Target: [specific, quantifiable target]

### Secondary Metrics (Valuable but not required)

- **Metric 1**: [Nice-to-have outcome 1] - Target: [aspirational target]
- **Metric 2**: [Nice-to-have outcome 2] - Target: [aspirational target]

## 🔍 Validation Strategy

### Measurement Approach
- **Data Sources**: [Where to collect metrics from]
- **Measurement Frequency**: [How often to measure progress]
- **Success Thresholds**: [When to consider the goal achieved]

### Learning Objectives
- **What to Learn**: [Key insights to gain from achieving this goal]
- **Adaptation Points**: [When to reconsider the approach]
- **Documentation**: [What information to document for future reference]

## 📝 Goal Breakdown

### Critical Path Activities
- **Activity 1**: [Key activity 1 to achieve the goal]
- **Activity 2**: [Key activity 2 to achieve the goal]
- **Activity 3**: [Key activity 3 to achieve the goal]

### Dependencies
- **Dependency 1**: [What this goal depends on]
- **Dependency 2**: [What this goal depends on]

### Risk Assessment
- **Risk 1**: [Potential risk] - Mitigation: [how to mitigate]
- **Risk 2**: [Potential risk] - Mitigation: [how to mitigate]

## 🔄 Review Process

### Review Schedule
- **Check-ins**: [Regular assessment schedule]
- **Milestone Reviews**: [When to evaluate progress]

### Success Validation
- **[Validation 1]**: [How to confirm goal is achieved]
- **[Validation 2]**: [How to confirm goal is achieved]

## 🏁 Completion Criteria

### Success Indicators
- [ ] Primary metrics achieved at target levels
- [ ] Goal objectives validated through measurement
- [ ] Learning objectives accomplished
- [ ] No major unforeseen issues discovered

### Success Validation
- **[Validation 1]**: [How to confirm goal was successful]
- **[Validation 2]**: [How to confirm goal was successful]

## 🔁 Adaptation Framework

### Regular Review Schedule
- **Weekly**: [Goal effectiveness assessment]
- **When Metrics Diverge**: [How to adjust approach]
- **When Learning Occurs**: [How to incorporate new information]

### Adaptation Triggers
- **Pivot Trigger 1**: [When to change approach]
- **Pause Trigger**: [When to temporarily adjust]
- **Realign Trigger**: [When to reconsider entirely]

---

*This goal definition serves as the foundation for all work related to achieving this objective. All strategies, milestones, and execution should align with these defined success metrics.*
"@
    
    $goalFile = Join-Path $fullGoalDir "goal.md"
    Set-Content -Path $goalFile -Value $goalContent -Encoding UTF8
    
    Write-Success "Created goal.md with description: $GoalDescription"
    
    # Create git branch for this goal
    if ($VerboseMode) {
        Write-Info "Setting up git branch for this goal..."
    }
    
    Set-Location $projectRoot | Out-Null
    $branchName = New-GoalBranch $goalDirName
    
    # Add and commit the new goal
    git add $goalDir 2>$null | Out-Null
    git commit -m "Add goal: $GoalDescription

- Created goal definition in $goalDir/goal.md
- Branch: $branchName" 2>$null | Out-Null
    
    Write-Success "Goal committed to branch: $branchName"
    
    # Update agent context
    Update-AgentContext | Out-Null
    
    # Print summary
    Write-Success "Goal created successfully!"
    Write-Host ""
    Write-Info "Goal Details:"
    Write-Host "  Directory: $goalDir"
    Write-Host "  Branch: $branchName"
    Write-Host "  Description: $GoalDescription"
    Write-Host ""
    Write-Info "Next Steps:"
    Write-Host "  1. Navigate to goal directory: cd $goalDir"
    Write-Host "  2. Complete the goal definition with specific details"
    Write-Host "  3. Use /goalkit.strategies to explore implementation strategies"
    Write-Host "  4. Use /goalkit.milestones to create measurable milestones" 
    Write-Host "  5. Use /goalkit.execute to implement with learning and adaptation"
    Write-Host ""
    git branch --show-current 2>$null
}

# Main execution
New-Goal -GoalDescription $GoalDescription -DryRun $DryRun -Force $Force -JsonMode $Json -VerboseMode $Verbose
