param(
    [switch]$Verbose = $false,
    [switch]$DryRun = $false,
    [switch]$Json = $false,
    [string]$GoalDescription = ""
)

# Create a new goal in a Goal Kit project

# Load common utilities
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. "$scriptDir\common.ps1"

# Function to display usage information
function Show-Usage {
    Write-Host "Usage: $($MyInvocation.MyCommand.Name) [OPTIONS] GOAL_DESCRIPTION" -ForegroundColor Cyan
    ""
    "Create a new goal in the current Goal Kit project."
    ""
    "OPTIONS:"
    "    -Verbose          Enable verbose output"
    "    -DryRun          Show what would be created without creating it"
    "    -h, -?           Show this help message"
    ""
    "ARGUMENTS:"
    "    GOAL_DESCRIPTION       Description of the goal to create"
    ""
    "EXAMPLES:"
    "    $($MyInvocation.MyCommand.Name) 'Improve user onboarding experience'"
    "    $($MyInvocation.MyCommand.Name) -DryRun 'Add user authentication system'"
    "    $($MyInvocation.MyCommand.Name) -Verbose 'Build analytics dashboard for user behavior'"
    ""
}

# Show help if requested
if ($args -contains "-h" -or $args -contains "-?") {
    Show-Usage
    exit 0
}

# Validate arguments
if ($GoalDescription -eq "") {
    Write-Error "Goal description is required"
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

# Check if this is a Goal Kit project
if (-not (Test-Path ".goalkit/vision.md")) {
    Write-Error "Not a Goal Kit project"
    Write-Info "Please run 'goalkeeper init' first to set up the project"
    exit 1
}

# If JSON mode, output JSON and exit early
if ($Json) {
    # Check if goals directory exists
    $goalsDir = "goals"
    if (-not (Test-Path $goalsDir)) {
        # Goals directory doesn't exist, so first goal will be 001
        $nextNumber = 1
    } else {
        # Find the next goal number
        $nextNumber = 1
        $existingGoals = Get-ChildItem $goalsDir -Directory | Where-Object {
            $_.Name -match '^\d+-'
        }

        if ($existingGoals) {
            $maxNum = $existingGoals | ForEach-Object {
                $num = $_.Name.Split('-')[0]
                [int]$num
            } | Measure-Object -Maximum | Select-Object -ExpandProperty Maximum

            $nextNumber = $maxNum + 1
        }
    }

    # Create goal directory name
    $goalNumber = "{0:D3}" -f $nextNumber
    $goalDirName = $goalNumber + "-" + ($GoalDescription.ToLower() -replace ' ', '-' -replace '[^a-z0-9-]', '')
    $goalDir = Join-Path $goalsDir $goalDirName
    $goalFile = Join-Path $goalDir "goal.md"
    
    # Output JSON with required variables using common function
    $jsonObj = @{
        GOAL_DIR = $goalDir
        GOAL_FILE = $goalFile
        GOAL_DESCRIPTION = $GoalDescription
        BRANCH_NAME = $goalDirName
    }
    
    Output-JsonMode $jsonObj
}

# Check if goals directory exists
$goalsDir = "goals"
if (-not (Test-Path $goalsDir)) {
    if ($DryRun) {
        Write-Info "[DRY RUN] Would create goals directory: $goalsDir"
    }
    else {
        New-Item -ItemType Directory -Path $goalsDir | Out-Null
        Write-Success "Created goals directory: $goalsDir"
    }
}

# Find the next goal number
$nextNumber = 1
if (Test-Path $goalsDir) {
    $existingGoals = Get-ChildItem $goalsDir -Directory | Where-Object {
        $_.Name -match '^\d+-'
    }

    if ($existingGoals) {
        $maxNum = $existingGoals | ForEach-Object {
            $num = $_.Name.Split('-')[0]
            [int]$num
        } | Measure-Object -Maximum | Select-Object -ExpandProperty Maximum

        $nextNumber = $maxNum + 1
    }
}

# Create goal directory name
$goalNumber = "{0:D3}" -f $nextNumber
$goalDirName = $goalNumber + "-" + ($GoalDescription.ToLower() -replace ' ', '-' -replace '[^a-z0-9-]', '')
$goalDir = Join-Path $goalsDir $goalDirName

# Check if goal directory already exists
if (Test-Path $goalDir) {
    Write-Error "Goal directory already exists: $goalDir"
    Write-Info "Use a different goal description or remove the existing directory"
    exit 1
}

if ($DryRun) {
    Write-Info "[DRY RUN] Would create goal directory: $goalDir"
    Write-Info "[DRY RUN] Would create goal.md with description: $GoalDescription"
    Write-Info "[DRY RUN] Would create branch: $goalDirName"
    exit 0
}

# Create goal directory
New-Item -ItemType Directory -Path $goalDir | Out-Null
Write-Success "Created goal directory: $goalDir"

# Create goal.md file
$goalContent = @"
// Goal Definition: $GoalDescription

**Goal Branch**: \`$goalDirName\`
**Created**: $(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
**Status**: Draft
**Vision**: [link to vision document]

## 🎯 Goal Overview

**Goal Statement**: $GoalDescription

**Context**: [Why is this goal important? What problem does it solve?]

**Success Level**: [What "success" looks like for this goal]

## 📊 Success Metrics

### Primary Metrics (Must achieve for success)

- **Metric 1**: [Measurable outcome] - Target: [specific, quantifiable target]
- **Metric 2**: [Measurable outcome] - Target: [specific, quantifiable target]
- **Metric 3**: [Measurable outcome] - Target: [specific, quantifiable target]

### Secondary Metrics (Valuable but not required)

- **Metric 1**: [Nice-to-have outcome] - Target: [aspirational target]
- **Metric 2**: [Nice-to-have outcome] - Target: [aspirational target]

## 👥 Target Users & Stakeholders

### Primary Users
- **[User Type 1]**: [How they benefit from this goal]
- **[User Type 2]**: [How they benefit from this goal]

### Stakeholders
- **[Stakeholder 1]**: [Their interest in this goal]
- **[Stakeholder 2]**: [Their interest in this goal]

## 🎯 Goal Hypotheses

### Key Assumptions
- **Hypothesis 1**: [Testable assumption about user behavior or outcome]
- **Hypothesis 2**: [Testable assumption about technical feasibility]
- **Hypothesis 3**: [Testable assumption about business value]

### Risk Factors
- **Risk 1**: [Potential issue] - Mitigation: [how to address]
- **Risk 2**: [Potential issue] - Mitigation: [how to address]

## 🚀 Goal Milestones

### Milestone 1: [Milestone Title] (Priority: P1)
**Description**: [What this milestone achieves]

**Success Indicators**:
- [Measurable outcome 1]
- [Measurable outcome 2]

**Validation Method**: [How to confirm this milestone is achieved]

**Expected Timeline**: [Rough time estimate]

---

### Milestone 2: [Milestone Title] (Priority: P2)
**Description**: [What this milestone achieves]

**Success Indicators**:
- [Measurable outcome 1]
- [Measurable outcome 2]

**Validation Method**: [How to confirm this milestone is achieved]

**Expected Timeline**: [Rough time estimate]

---

### Milestone 3: [Milestone Title] (Priority: P3)
**Description**: [What this milestone achieves]

**Success Indicators**:
- [Measurable outcome 1]
- [Measurable outcome 2]

**Validation Method**: [How to confirm this milestone is achieved]

**Expected Timeline**: [Rough time estimate]

---

## 🔍 Validation Strategy

### Measurement Approach
- **Data Sources**: [Where to collect metrics from]
- **Measurement Frequency**: [How often to measure]
- **Success Thresholds**: [When to consider the goal achieved]

### Learning Objectives
- **What to Learn**: [Key insights to gain from pursuing this goal]
- **Pivot Points**: [When to reconsider the goal or approach]
- **Documentation**: [What to document for future reference]

## 🎯 Goal Dependencies

### Supports These Goals
- **[Goal 1]**: [How this goal contributes to another goal]
- **[Goal 2]**: [How this goal contributes to another goal]

### Depends on These Goals
- **[Goal 1]**: [What this goal needs from another goal]
- **[Goal 2]**: [What this goal needs from another goal]

## 💡 Strategy Exploration Areas

### Technical Strategies to Explore
- **[Strategy 1]**: [Alternative approach to consider]
- **[Strategy 2]**: [Alternative approach to consider]

### User Experience Strategies to Explore
- **[UX Approach 1]**: [Different way users could achieve this goal]
- **[UX Approach 2]**: [Different way users could achieve this goal]

### Implementation Strategies to Explore
- **[Implementation 1]**: [Different development approach]
- **[Implementation 2]**: [Different development approach]

## 📈 Success Criteria Validation

### Goal Achievement Checklist
- [ ] Primary metrics achieved at target levels
- [ ] User feedback validates the outcome
- [ ] Business impact confirmed through measurement
- [ ] Learning objectives accomplished
- [ ] No significant negative consequences discovered

### Goal Failure Indicators
- [ ] Primary metrics not achievable despite multiple strategies
- [ ] User feedback indicates different needs
- [ ] Business case no longer valid
- [ ] Technical constraints make goal unachievable

## 🔄 Review & Adaptation Points

### Regular Review Schedule
- **After Each Milestone**: [What to review and how]
- **Monthly**: [Strategic review of goal relevance]
- **Quarterly**: [Overall goal effectiveness assessment]

### Adaptation Triggers
- **Pivot Trigger 1**: [When to consider changing approach]
- **Pause Trigger**: [When to temporarily stop pursuing this goal]
- **Abandon Trigger**: [When to stop pursuing this goal entirely]

---

*This goal definition serves as the foundation for strategy exploration and milestone planning. It should be reviewed and updated as learning occurs during implementation.*
"@

$goalContent | Out-File "$goalDir\goal.md" -Encoding UTF8
Write-Success "Created goal.md with description: $GoalDescription"

# Create git branch for this goal
Write-Info "Setting up git branch for this goal..."
Set-Location $projectRoot
$branchName = New-GoalBranch -GoalName $goalDirName

# Add and commit the new goal
Set-Location $projectRoot
git add $goalDir
git commit -m "Add goal: $GoalDescription

- Created goal definition in $goalDir/goal.md
- Branch: $branchName"

Write-Success "Goal committed to branch: $branchName"

# Update agent context
Update-AgentContext

# Print summary
Write-Success "Goal created successfully!"
""
Write-Info "Goal Details:"
"  Directory: $goalDir"
"  Branch: $branchName"
"  Description: $GoalDescription"
""
Write-Info "Next Steps:"
"  1. Navigate to goal directory: cd $goalDir"
"  2. Use /goalkit.strategies to explore implementation approaches"
"  3. Use /goalkit.milestones to create measurable milestones"
"  4. Use /goalkit.execute to implement with learning and adaptation"
""
Write-Info "Current branch is: $(git branch --show-current)"

# Setup goal environment for immediate development
Set-GoalEnvironment -GoalDir $goalDir

# Run the methodology guide to help complete the methodology
Write-Info "`nRunning methodology guide to help complete the goal methodology..."
Set-Location $goalDir
& "$scriptDir\guide-methodology.ps1" -CheckOnly