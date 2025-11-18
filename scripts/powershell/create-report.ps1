# Generate progress reports for a project or goal

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$GoalDir,
    
    [switch]$Edit = $false,
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-Report {
    param(
        [string]$GoalDir,
        [bool]$Edit,
        [bool]$Force,
        [bool]$JsonMode )
    
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
    $visionFile = Join-Path -Path ".goalkit" -ChildPath "vision.md"
    if (-not (Test-Path $visionFile)) {
        Write-Error-Custom "Not a Goal Kit project"
        Write-Info "Please run 'goalkeeper init' first to set up the project"
        exit 1
    }
    
    # Define report directory
    $reportDir = Join-Path -Path ".goalkit" -ChildPath "reports"
    if (-not (Test-Path $reportDir)) {
        New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
    }
    
    # Get timestamp for report
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    $reportDate = (Get-Date).ToString('yyyy-MM-dd')
    
    # Determine report file name
    $reportFileName = if ([string]::IsNullOrEmpty($GoalDir)) {
        "progress-report-$reportDate.md"
    } else {
        "report-$GoalDir-$reportDate.md"
    }
    
    $reportFile = Join-Path $reportDir $reportFileName
    
    # If JSON mode, output JSON
    if ($JsonMode) {
        $jsonOutput = @{
            "REPORT_FILE" = $reportFile
            "REPORT_DIR" = $reportDir
            "REPORT_DATE" = $reportDate
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }
    
    # Check if report file already exists
    if (Test-Path $reportFile) {
        if ($Edit) {
            
                Write-Info "Opening report file for editing..."
            
            # Open in default editor
            if (Get-Command code -ErrorAction SilentlyContinue) {
                code $reportFile
            } else {
                notepad $reportFile
            }
            return
        } elseif (-not $Force) {
            Write-Warning "Report file already exists for this date: $reportFile"
            Write-Info "Use --edit to open in editor or --force to create a new report"
            exit 0
        }
    }
    
    # Check if template exists
    $templatePath = Join-Path -Path $projectRoot -ChildPath ".goalkit" "templates" "report-template.md"
    if (Test-Path $templatePath) {
        $reportContent = Get-Content -Path $templatePath -Raw
        $reportContent = $reportContent -replace '\[DATE\]', $timestamp
        $reportContent = $reportContent -replace '\[REPORT_DATE\]', $reportDate
        if (-not [string]::IsNullOrEmpty($GoalDir)) {
            $reportContent = $reportContent -replace '\[GOAL\]', $GoalDir
        }
    } else {
        # Fallback to default content
        $reportContent = @"
# Progress Report - $reportDate

**Report Date**: $timestamp
**Goal**: $(if ([string]::IsNullOrEmpty($GoalDir)) { "Overall Project" } else { $GoalDir })

## Executive Summary

[Provide a high-level overview of progress made in this period]

## Goals & Objectives Status

### Overall Goal Status
- **Status**: [On Track / At Risk / Off Track / Completed]
- **Progress**: [X% complete]
- **Key Achievements**: [List major achievements this period]

---

## Detailed Progress

### Completed Items

- [ ] [Completed item 1]
- [ ] [Completed item 2]
- [ ] [Completed item 3]

### In Progress

- **[Item Name]**: [Progress percentage] - [Brief description]
- **[Item Name]**: [Progress percentage] - [Brief description]

### Upcoming

- [ ] [Planned item 1]
- [ ] [Planned item 2]

---

## Blockers & Challenges

### Current Blockers

1. **[Blocker Title]**: [Description and impact]
   - **Impact**: [How this affects progress]
   - **Mitigation**: [Plan to resolve]

2. **[Blocker Title]**: [Description and impact]

### Lessons Learned

- [What we learned from this period]
- [What went well]
- [What could improve]

---

## Metrics & KPIs

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| [Metric 1] | [Target] | [Actual] | [✓/✗] |
| [Metric 2] | [Target] | [Actual] | [✓/✗] |
| [Metric 3] | [Target] | [Actual] | [✓/✗] |

---

## Resource & Team Status

- **Team Capacity**: [X% utilized / Available]
- **Major Resource Changes**: [Any staffing or resource changes]
- **Skills Gaps**: [Any identified training needs]

---

## Next Period Plan

### Priority Items for Next Period

1. **[High Priority Item]**: [Description and rationale]
2. **[High Priority Item]**: [Description and rationale]
3. **[Medium Priority Item]**: [Description and rationale]

### Success Criteria for Next Period

- [ ] [Specific criterion]
- [ ] [Specific criterion]
- [ ] [Specific criterion]

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| [Risk 1] | [High/Medium/Low] | [High/Medium/Low] | [Plan] |
| [Risk 2] | [High/Medium/Low] | [High/Medium/Low] | [Plan] |

---

## Appendices

### A. Detailed Metrics
[Include any detailed data or charts]

### B. Code Changes Summary
[Brief summary of code commits and changes]

### C. Communication
[Notes on stakeholder communications or decisions made]
"@
    }
    
    # Write report file
    Set-Content -Path $reportFile -Value $reportContent -Encoding UTF8
    Write-Success "Created progress report: $reportFile"
    
    # Git operations
    git add $reportFile 2>$null | Out-Null
    if ([string]::IsNullOrEmpty($GoalDir)) {
        git commit -m "Add progress report for $reportDate" 2>$null | Out-Null
    } else {
        git commit -m "Add progress report for goal $GoalDir on $reportDate" 2>$null | Out-Null
    }
    
    Write-Success "Report committed to repository"
    
    # Print summary
    Write-Host ""
    Write-Info "Progress report created successfully!"
    Write-Host "  Report File: $reportFile"
    Write-Host "  Report Date: $reportDate"
    Write-Host ""
    Write-Info "Next Steps:"
    Write-Host "  1. Fill in progress details and metrics"
    Write-Host "  2. Document blockers and lessons learned"
    Write-Host "  3. Review with team and stakeholders"
    Write-Host "  4. Use this to plan next period's work"
    Write-Host ""
}

# Main execution
New-Report -GoalDir $GoalDir -Edit $Edit -Force $Force -JsonMode $Json 