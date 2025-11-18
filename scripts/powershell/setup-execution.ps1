# Setup execution plan in a Goal Kit project

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalDirectory,
    
    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false,
    [switch]$Verbose = $false
)

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "common.ps1")

function New-ExecutionFile {
    param(
        [string]$GoalDirectory,
        [bool]$DryRun,
        [bool]$Force,
        [bool]$JsonMode,
        [bool]$VerboseMode
    )
    
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
        $executionFile = Join-Path $GoalDirectory "execution.md"
        $branchName = $goalDirName
        
        # Output JSON with required variables
        $jsonOutput = @{
            "GOAL_DIR" = $GoalDirectory
            "EXECUTION_FILE" = $executionFile
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
    
    # Check if execution.md already exists
    $executionFile = Join-Path $GoalDirectory "execution.md"
    if ((Test-Path $executionFile) -and (-not $DryRun)) {
        Write-Warning "Execution file already exists: $executionFile"
        if (-not $Force) {
            $response = Read-Host "Overwrite existing execution file? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Info "Operation cancelled"
                return
            }
        }
    }
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would create execution file: $executionFile"
        return
    }
    
    # Check if template exists, otherwise create default execution.md
    $templatePath = Join-Path $projectRoot ".goalkit" "templates" "execution-template.md"
    if (Test-Path $templatePath) {
        # Read the template
        $templateContent = Get-Content -Path $templatePath -Raw

        # Replace placeholders in the template
        $goalDirName = Split-Path -Leaf $GoalDirectory
        $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
        $executionContent = $templateContent -replace '\[GOAL NAME\]', $goalDirName
        $executionContent = $executionContent -replace '\[DATE\]', $timestamp
    } else {
        # Fallback to default content if template not found
        $goalDirName = Split-Path -Leaf $GoalDirectory
        $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

        $executionContent = @"
# Execution Plan for $goalDirName

**Created**: $timestamp
**Status**: In Planning

## Overview
Execution plan for goal: $goalDirName

## Selected Strategy
- **Strategy Name**: [Which strategy are we implementing]
- **Rationale**: [Why this strategy was selected]
- **Success Criteria**: [How to measure strategy success]

## Execution Timeline

### Phase 1: Foundation
- **Duration**: [Timeline for initial setup]
- **Key Activities**: [What needs to be done first]
- **Dependencies**: [What must be in place]
- **Success Indicators**: [How to know Phase 1 is complete]

### Phase 2: Implementation
- **Duration**: [Timeline for main implementation]
- **Key Activities**: [Core implementation work]
- **Learning Objectives**: [What to learn during this phase]
- **Success Indicators**: [How to know Phase 2 is complete]

### Phase 3: Validation
- **Duration**: [Timeline for testing and validation]
- **Validation Approach**: [How to test success]
- **Measurement Plan**: [How to measure success metrics]
- **Success Indicators**: [How to know Phase 3 is complete]

## Daily/Weekly Execution

### Development Cycle
- **Daily Standups**: [What to check in on daily]
- **Weekly Reviews**: [What to assess weekly]
- **Progress Tracking**: [How to track progress against milestones]

### Decision Framework
- **Adaptation Signals**: [When to consider changing approach]
- **Go/No-Go Criteria**: [When to continue vs. pivot]
- **Escalation Path**: [When to involve others in decisions]

## Learning and Adaptation

### Critical Assumptions
- **Assumption 1**: [What assumption is critical to success]
- **How to Validate**: [How to test if the assumption holds]
- **If Wrong**: [What to do if the assumption fails]

### Learning Loops
- **Learn**: [What insights to gather]
- **Measure**: [How to measure learning]
- **Adapt**: [How to apply learning]

## Risk Management

### Key Risks
- **Risk 1**: [Potential risk to execution]
  - **Likelihood**: [High/Medium/Low]
  - **Impact**: [What happens if this occurs]
  - **Mitigation**: [How to prevent this risk]

### Contingency Plans
- **Plan A**: [Primary execution approach]
- **Plan B**: [Alternative if Plan A stalls]
- **Fallback**: [Emergency fallback approach]

## Communication and Coordination

### Stakeholder Updates
- **Frequency**: [How often to update]
- **Format**: [How to communicate progress]
- **Key Metrics**: [What to highlight in updates]

### Blockers and Escalation
- **Blocker Resolution**: [How to handle blockers]
- **Escalation Path**: [When and how to escalate]

## Completion Criteria

### Execution Success
- [ ] All milestones completed on schedule
- [ ] Success metrics achieved at target levels
- [ ] Primary risks mitigated
- [ ] Learning objectives captured

### Goal Completion
- [ ] Execution complete and validated
- [ ] All success metrics confirmed achieved
- [ ] Documentation complete
- [ ] Ready for post-execution review

---

*This execution plan guides day-to-day work. Review and update regularly based on progress and learning.*
"@
    }

    Set-Content -Path $executionFile -Value $executionContent -Encoding UTF8
    
    Write-Success "Created execution file: $executionFile"
    
    # Print summary
    Write-Success "Execution plan setup completed!"
    Write-Host ""
    Write-Info "Execution Details:"
    Write-Host "  Goal Directory: $GoalDirectory"
    Write-Host "  Execution File: $executionFile"
    Write-Host ""
    
    Write-Info "Next Steps:"
    Write-Host "  1. Review and customize the execution plan"
    Write-Host "  2. Define your first day's work items"
    Write-Host "  3. Begin execution with regular progress checks"
    Write-Host "  4. Document learnings as you progress"
    
    # Setup goal environment for immediate development
    if (-not (Set-GoalEnvironment $GoalDirectory)) {
        Write-Error-Custom "Failed to setup goal environment for $GoalDirectory"
        exit 1
    }
}

# Main execution
New-ExecutionFile -GoalDirectory $GoalDirectory -DryRun $DryRun -Force $Force -JsonMode $Json -VerboseMode $Verbose
