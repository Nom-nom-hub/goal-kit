# Conduct project reviews and retrospectives

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$ReviewType,
    
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-Review {
    param(
        [string]$ReviewType,
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
    
    # Define review directory
    $reviewDir = Join-Path -Path ".goalkit" -ChildPath "reviews"
    if (-not (Test-Path $reviewDir)) {
        New-Item -ItemType Directory -Path $reviewDir -Force | Out-Null
    }
    
    # Get timestamp for review
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    $reviewDate = (Get-Date).ToString('yyyy-MM-dd')
    
    # Determine review type and file name
    if ([string]::IsNullOrEmpty($ReviewType)) {
        $ReviewType = "general"
    }
    
    $reviewFileName = "review-$ReviewType-$reviewDate.md"
    $reviewFile = Join-Path $reviewDir $reviewFileName
    
    # If JSON mode, output JSON
    if ($JsonMode) {
        $jsonOutput = @{
            "REVIEW_FILE" = $reviewFile
            "REVIEW_DIR" = $reviewDir
            "REVIEW_DATE" = $reviewDate
            "REVIEW_TYPE" = $ReviewType
        }
        Write-Output ($jsonOutput | ConvertTo-Json -Compress)
        return
    }
    
    # Check if review file already exists
    if (Test-Path $reviewFile) {
        if (-not $Force) {
            Write-Warning "Review file already exists for this date: $reviewFile"
            Write-Info "Use --force to create a new review"
            exit 0
        }
    }
    
    # Check if template exists
    $templatePath = Join-Path -Path $projectRoot -ChildPath ".goalkit/templates/review-template.md"
    if (Test-Path $templatePath) {
        $reviewContent = Get-Content -Path $templatePath -Raw
        $reviewContent = $reviewContent -replace '\[DATE\]', $timestamp
        $reviewContent = $reviewContent -replace '\[REVIEW_DATE\]', $reviewDate
        $reviewContent = $reviewContent -replace '\[REVIEW_TYPE\]', $ReviewType
    } else {
        # Fallback to default content based on review type
        if ($ReviewType -eq "retrospective") {
            $reviewContent = @"
# Retrospective Review - $reviewDate

**Review Date**: $timestamp
**Review Type**: Retrospective

## What Went Well

- [Positive aspect 1]
- [Positive aspect 2]
- [Positive aspect 3]
- [Positive aspect 4]

## What Could Be Improved

- [Area for improvement 1]
  - **Action**: [Specific action to improve]
- [Area for improvement 2]
  - **Action**: [Specific action to improve]
- [Area for improvement 3]
  - **Action**: [Specific action to improve]

## What Surprised Us

- [Unexpected discovery or learning]
- [Unexpected discovery or learning]

## Action Items

| Action | Owner | Target Date | Status |
|--------|-------|-------------|--------|
| [Action 1] | [Owner] | [Date] | [ ] |
| [Action 2] | [Owner] | [Date] | [ ] |
| [Action 3] | [Owner] | [Date] | [ ] |

## Metrics from This Period

| Metric | Value | Trend |
|--------|-------|-------|
| [Metric 1] | [Value] | [↑/↓/-] |
| [Metric 2] | [Value] | [↑/↓/-] |
| [Metric 3] | [Value] | [↑/↓/-] |

## Commitments for Next Period

- [ ] [Specific commitment 1]
- [ ] [Specific commitment 2]
- [ ] [Specific commitment 3]
"@
        } else {
            $reviewContent = @"
# Project Review - $reviewDate

**Review Date**: $timestamp
**Review Type**: $ReviewType

## Overall Assessment

### Project Health
- **Status**: [On Track / At Risk / Off Track / Completed]
- **Overall Progress**: [X% complete]

### Key Achievements
1. [Major achievement 1]
2. [Major achievement 2]
3. [Major achievement 3]

---

## Goal Progress Review

### Vision Alignment
- Are we staying true to the original vision? [Yes / Partially / No]
- Are we still aligned with project principles? [Yes / Partially / No]

### Goal Status
- **Goal 1**: [Status] - [Progress %]
- **Goal 2**: [Status] - [Progress %]
- **Goal 3**: [Status] - [Progress %]

---

## Technical & Quality Review

### Code Quality
- **Test Coverage**: [X%]
- **Build Status**: [Passing / Failing]
- **Code Review Process**: [Assessment]

### Architecture & Design
- **Design Quality**: [Good / Acceptable / Needs Work]
- **Scalability Concerns**: [List any concerns]
- **Technical Debt**: [Assessment]

---

## Team & Resource Review

### Team Performance
- **Team Morale**: [High / Good / Fair / Low]
- **Productivity**: [Assessment]
- **Collaboration**: [Assessment]

### Learning & Development
- **Skills Growth**: [Areas of growth]
- **Training Needs**: [Identified needs]

---

## Risk & Issue Review

### Outstanding Risks
| Risk | Probability | Impact | Status |
|------|-------------|--------|--------|
| [Risk 1] | [High/Medium/Low] | [High/Medium/Low] | [Mitigating] |
| [Risk 2] | [High/Medium/Low] | [High/Medium/Low] | [Monitoring] |

### Resolved Issues
- [Issue 1 - Resolution]
- [Issue 2 - Resolution]

---

## Recommendations & Next Steps

### Immediate Actions (Next 1-2 weeks)
1. [Action with owner and due date]
2. [Action with owner and due date]

### Medium-term Focus (Next Month)
1. [Focus area]
2. [Focus area]

### Strategic Considerations
- [Long-term consideration]
- [Long-term consideration]

---

## Sign-off

- **Reviewed By**: [Name]
- **Review Date**: $reviewDate
- **Next Review**: [Scheduled date]
"@
        }
    }
    
    # Write review file
    Set-Content -Path $reviewFile -Value $reviewContent -Encoding UTF8
    Write-Success "Created review document: $reviewFile"
    
    # Git operations
    git add $reviewFile 2>$null | Out-Null
    git commit -m "Add $ReviewType review for $reviewDate" 2>$null | Out-Null
    
    Write-Success "Review committed to repository"
    
    # Print summary
    Write-Host ""
    Write-Info "Review document created successfully!"
    Write-Host "  Review File: $reviewFile"
    Write-Host "  Review Type: $ReviewType"
    Write-Host "  Review Date: $reviewDate"
    Write-Host ""
    Write-Info "Review Types:"
    Write-Host "  - retrospective: Team retrospective and lessons learned"
    Write-Host "  - general: Overall project health and progress review"
    Write-Host "  - goal: Individual goal milestone review"
    Write-Host ""
    Write-Info "Next Steps:"
    Write-Host "  1. Complete the review document with detailed assessments"
    Write-Host "  2. Identify action items and assign owners"
    Write-Host "  3. Share with team and stakeholders"
    Write-Host "  4. Use insights to inform next period's planning"
    Write-Host ""
}

# Main execution
New-Review -ReviewType $ReviewType -Force $Force -JsonMode $Json 