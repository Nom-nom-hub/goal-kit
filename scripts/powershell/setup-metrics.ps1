# Setup metrics planning in a Goal Kit project

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalDirectory,
    
    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false
)

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-MetricsFile {
    param(
        [string]$GoalDirectory,
        [bool]$DryRun,
        [bool]$Force,
        [bool]$JsonMode
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
        $metricsFile = Join-Path -Path $GoalDirectory -ChildPath "metrics.md"
        $branchName = $goalDirName
        
        # Output JSON with required variables
        $jsonOutput = @{
            "GOAL_DIR" = $GoalDirectory
            "METRICS_FILE" = $metricsFile
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
    
    # Check if metrics.md already exists
    $metricsFile = Join-Path -Path $GoalDirectory -ChildPath "metrics.md"
    if ((Test-Path $metricsFile) -and (-not $DryRun)) {
        Write-Warning "Metrics file already exists: $metricsFile"
        if (-not $Force) {
            $response = Read-Host "Overwrite existing metrics file? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Info "Operation cancelled"
                return
            }
        }
    }
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would create metrics file: $metricsFile"
        return
    }
    
    # Create metrics file with basic template
    $goalDirName = Split-Path -Leaf $GoalDirectory
    
    $metricsContent = @"
# Metrics Plan for $goalDirName

## Overview
Metrics and measurement plan for goal: $goalDirName

## Success Criteria Review
Extract success criteria from goal.md and validate metric quality.

| Metric ID | Description | Target | Timeframe | Quality Score |
|-----------|-------------|--------|-----------|---------------|
| SC-001 | [Metric description] | [Target value] | [By when] | [See checklist below] |
| SC-002 | [Metric description] | [Target value] | [By when] | [See checklist below] |
| SC-003 | [Metric description] | [Target value] | [By when] | [See checklist below] |

## Metric Quality Validation

For each success criterion, validate against quality checklist:

### SC-001: [Metric Name]

**Metric Description**: [Full description of what's being measured]

#### Quality Checklist
- [ ] **Measurable**: Can we collect this data reliably and objectively?
  - *How measured*: [Specific measurement method]
  - *Data source*: [Where data comes from]
  - *Frequency*: [How often measured]

- [ ] **Actionable**: Will this metric drive specific decisions?
  - *Green zone (≥ target)*: [What action to take]
  - *Yellow zone (near target)*: [What action to take]
  - *Red zone (< threshold)*: [What action to take]

- [ ] **Leading**: Does it predict future success (not just lag)?
  - *Leading indicator*: [Yes/No - explain]
  - *Lag time*: [How long until impact visible]

- [ ] **Bounded**: Is there a clear target and timeframe?
  - *Target*: [Specific number/percentage]
  - *Baseline*: [Current state]
  - *Deadline*: [When to achieve by]

- [ ] **Valuable**: Does it connect to user/business outcomes?
  - *User value*: [How this helps users]
  - *Business value*: [How this helps business]
  - *Alignment*: [Links to vision scenario]

**Quality Score**: [Pass/Needs Improvement/Fail]

**Issues to address**: [Any quality gaps to fix]

## Baseline Measurements

Establish current state before starting work.

| Metric | Current Baseline | Measurement Date | Measurement Method | Notes |
|--------|------------------|------------------|-------------------|-------|
| SC-001 | [Current value] | [Date measured] | [How measured] | [Context] |
| SC-002 | [Current value] | [Date measured] | [How measured] | [Context] |
| SC-003 | [Current value] | [Date measured] | [How measured] | [Context] |

**Baseline validation**:
- [ ] Baselines measured using same method as target measurement
- [ ] Baselines represent typical state (not outliers)
- [ ] Baselines documented with context (time period, conditions)

## Instrumentation Plan

Define how to collect data for each metric.

### SC-001: [Metric Name]

**What to instrument**:
- [Specific events to track]
- [User behaviors to log]
- [System metrics to capture]

**How to collect**:
- **Tool/Platform**: [Analytics tool, logging system, database query]
- **Implementation**: [Code changes needed, tracking setup]
- **Storage**: [Where data is stored]

**When to measure**:
- **Frequency**: [Real-time, daily, weekly]
- **Triggers**: [Events that trigger measurement]
- **Duration**: [How long to collect data]

**Who analyzes**:
- **Responsible person**: [Name/role]
- **Review frequency**: [How often to review]
- **Reporting format**: [Dashboard, report, alert]

**Validation**:
- [ ] Instrumentation tested and working
- [ ] Data collection verified accurate
- [ ] Dashboard/reporting set up

## Decision Thresholds

Define what actions to take based on metric values.

### SC-001: [Metric Name]

| Zone | Threshold | Status | Action |
|------|-----------|--------|--------|
| 🟢 **Green (Success)** | ≥ [target] | Goal met | Scale feature, celebrate, document success |
| 🟡 **Yellow (Warning)** | [X] to [Y] | Needs attention | Investigate root cause, adjust tactics |
| 🔴 **Red (Failure)** | < [threshold] | Goal at risk | Pivot strategy, escalate, consider alternatives |

**Pivot triggers**:
- If metric stays in red zone for [duration] → [specific action]
- If metric trends downward for [duration] → [specific action]

## Measurement Dashboard

Define how metrics will be visualized and monitored.

### Dashboard Design

**Tool/Platform**: [Grafana, Metabase, Tableau, Google Analytics, Custom]

**Dashboard sections**:
1. **Overview**: All metrics at-a-glance with status indicators
2. **Trends**: Time-series charts showing metric evolution
3. **Breakdowns**: Segmentation by user type, platform, etc.
4. **Alerts**: Notifications when metrics cross thresholds

**Access**:
- **Who can view**: [Team members, stakeholders]
- **Update frequency**: [Real-time, hourly, daily]
- **Link**: [URL to dashboard when created]

## Metric Types Classification

Categorize metrics to ensure balanced measurement.

### User Behavior Metrics
Metrics that measure how users actually use the feature:
- **[Metric ID]**: [Description]

### Business Impact Metrics
Metrics that measure business value delivered:
- **[Metric ID]**: [Description]

### Technical Quality Metrics
Metrics that measure system performance/reliability:
- **[Metric ID]**: [Description]

### Learning Metrics
Metrics that measure what we discovered/capabilities built:
- **[Metric ID]**: [Description]

**Balance check**:
- [ ] At least one user behavior metric
- [ ] At least one business impact metric
- [ ] Technical metrics support user/business metrics
- [ ] Learning objectives defined

## Success Criteria

This measurement plan is ready when:

- [ ] All metrics pass quality validation checklist
- [ ] Baselines measured and documented
- [ ] Instrumentation implemented and tested
- [ ] Dashboard created and accessible
- [ ] Decision thresholds defined and agreed
- [ ] Review schedule established
- [ ] Team trained on metric interpretation
"@
    
    Set-Content -Path $metricsFile -Value $metricsContent -Encoding UTF8
    
    Write-Success "Created metrics file: $metricsFile"
    
    # Print summary
    Write-Success "Metrics planning setup completed!"
    Write-Host ""
    Write-Info "Metrics Details:"
    Write-Host "  Goal Directory: $GoalDirectory"
    Write-Host "  Metrics File: $metricsFile"
    Write-Host ""
    
    Write-Info "Next Steps:"
    Write-Host "  1. Extract success criteria from goal.md"
    Write-Host "  2. Validate each metric against quality checklist"
    Write-Host "  3. Define instrumentation and measurement methods"
    Write-Host "  4. Set up baseline measurements before implementation"
    Write-Host "  5. Use /goalkit.strategies to explore implementation approaches"
    
    # Setup goal environment for immediate development
    if (-not (Set-GoalEnvironment $GoalDirectory)) {
        Write-Error-Custom "Failed to setup goal environment for $GoalDirectory"
        exit 1
    }
}

# Main execution
New-MetricsFile -GoalDirectory $GoalDirectory -DryRun $DryRun -Force $Force -JsonMode $Json
