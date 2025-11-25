# Create a new goal in a Goal Kit project

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$GoalDescription,
    
    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$Json = $false )

# Get the script directory and source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path -Path $scriptDir -ChildPath "common.ps1")

function New-Goal {
    param(
        [string]$GoalDescription,
        [bool]$DryRun,
        [bool]$Force,
        [bool]$JsonMode )
    
    # Validate arguments
    if ([string]::IsNullOrEmpty($GoalDescription)) {
        Write-Error-Custom "Goal description is required"
        exit 1
    }
    
    # Check if we're in a git repository
    if (-not (Test-GitRepo)) {
        Handle-Error "Not in a git repository. Please run this from the root of a Goal Kit project"
    }
    
    # Get project root
    $projectRoot = Get-GitRoot
    if ([string]::IsNullOrEmpty($projectRoot)) {
        Handle-Error "Could not determine git root. Not in a git repository."
    }
    
    try {
        Set-Location $projectRoot -ErrorAction Stop
    } catch {
        Handle-Error "Failed to change to project root: $projectRoot"
    }
    
    # Check if this is a Goal Kit project
    $visionFile = Join-Path -Path ".goalkit" -ChildPath "vision.md"
    if (-not (Test-Path $visionFile)) {
        Handle-Error "Not a Goal Kit project. Please run 'goalkeeper init' first to set up the project"
    }
    
    # If JSON mode, output JSON and exit early
    if ($JsonMode) {
        $goalsDir = Join-Path -Path ".goalkit" -ChildPath "goals"
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
        $goalDir = Join-Path -Path ".goalkit" -ChildPath (Join-Path -Path "goals" -ChildPath $goalDirName)
        $goalFile = Join-Path -Path $goalDir -ChildPath "goal.md"
        
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
    $goalsDir = Join-Path -Path ".goalkit" -ChildPath "goals"
    if (-not (Test-Path $goalsDir)) {
        if ($DryRun) {
            Write-Info "[DRY RUN] Would create goals directory: $goalsDir"
        } else {
            try {
                New-Item -ItemType Directory -Path $goalsDir -Force -ErrorAction Stop | Out-Null
            } catch {
                Handle-Error "Failed to create goals directory: $goalsDir"
            }
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
    $goalDir = Join-Path -Path ".goalkit" -ChildPath (Join-Path -Path "goals" -ChildPath $goalDirName)
    $fullGoalDir = Join-Path -Path $projectRoot -ChildPath $goalDir
    
    # Check if goal directory already exists
    if (Test-Path $fullGoalDir) {
        if (-not $Force) {
            Write-Error-Custom "Goal directory already exists: $goalDir"
            Write-Info "Use a different goal description or remove the existing directory"
            exit 1
        } else {
            
                Write-Info "Overwriting existing goal directory: $goalDir"
            
        }
    }
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would create goal directory: $goalDir"
        Write-Info "[DRY RUN] Would create goal.md with description: $GoalDescription"
        Write-Info "[DRY RUN] Would create branch: $goalDirName"
        return
    }
    
    # Create goal directory
    try {
        New-Item -ItemType Directory -Path $fullGoalDir -Force -ErrorAction Stop | Out-Null
    } catch {
        Handle-Error "Failed to create goal directory: $fullGoalDir"
    }
    Write-Success "Created goal directory: $goalDir"
    
    # Get current timestamp
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    
    # Check if template exists, otherwise create default goal.md
    $templatePath = Join-Path -Path $projectRoot -ChildPath (Join-Path -Path ".goalkit" -ChildPath (Join-Path -Path "templates" -ChildPath "goal-template.md"))
    if (Test-Path $templatePath) {
        # Read the template
        try {
            $templateContent = Get-Content -Path $templatePath -Raw -ErrorAction Stop
        } catch {
            Handle-Error "Failed to read goal template: $templatePath"
        }

        # Replace placeholders in the template
        $goalContent = $templateContent -replace '\[GOAL DESCRIPTION\]', $GoalDescription
        $goalContent = $goalContent -replace '\[###-goal-name\]', $goalDirName
        $goalContent = $goalContent -replace '\[DATE\]', $timestamp
    } else {
        # Fallback to default content if template not found
        $goalContent = @"
# Goal Statement: $GoalDescription

**Goal Branch**: \`$goalDirName\`
**Created**: $timestamp
**Status**: Draft
**Methodology**: Goal-Driven Development

## Beneficiary Scenarios & Validation *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as beneficiary journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY VALIDATABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Validated independently
  - Demonstrated to users independently
-->

### Beneficiary Story 1 - [Brief Title] (Priority: P1)

[Describe this beneficiary journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Validation**: [Describe how this can be validated independently - e.g., "Can be fully validated by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### Beneficiary Story 2 - [Brief Title] (Priority: P2)

[Describe this beneficiary journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Validation**: [Describe how this can be validated independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### Beneficiary Story 3 - [Brief Title] (Priority: P3)

[Describe this beneficiary journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Validation**: [Describe how this can be validated independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more beneficiary stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System/Process MUST [specific capability, e.g., "allow users to achieve goal"]
- **FR-002**: System/Process MUST [specific capability, e.g., "validate success metrics"]
- **FR-003**: Stakeholders MUST be able to [key interaction, e.g., "measure goal progress"]
- **FR-004**: System/Process MUST [data requirement, e.g., "persist goal progress"]
- **FR-005**: System/Process MUST [behavior, e.g., "log all validation events"]

*Example of marking unclear requirements:*

- **FR-006**: System/Process MUST support [NEEDS CLARIFICATION: specific support method not specified - validation approach, measurement method, etc?]
- **FR-007**: System/Process MUST achieve [NEEDS CLARIFICATION: target level not specified - specific metrics not defined]

### Key Entities *(include if goal involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Stakeholders can measure goal progress in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 measurement requests without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of stakeholders successfully validate primary goal on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
"@
    }

    $goalFile = Join-Path -Path $fullGoalDir -ChildPath "goal.md"
    try {
        Set-Content -Path $goalFile -Value $goalContent -Encoding UTF8 -ErrorAction Stop
    } catch {
        Handle-Error "Failed to create goal.md file"
    }
    
    Write-Success "Created goal.md with description: $GoalDescription"
    
    # Create git branch for this goal
    Write-Info "Setting up git branch for this goal..."
    
    try {
        Set-Location $projectRoot -ErrorAction Stop
    } catch {
        Handle-Error "Failed to change to project root: $projectRoot"
    }
    
    try {
        $branchName = New-GoalBranch $goalDirName
    } catch {
        Handle-Error "Failed to create git branch for goal"
    }
    
    # Add and commit the new goal
    try {
        git add $goalDir 2>$null | Out-Null
        git commit -m "Add goal: $GoalDescription

- Created goal definition in $goalDir/goal.md
- Branch: $branchName" 2>$null -ErrorAction SilentlyContinue | Out-Null
    } catch {
        Write-Warning "Failed to commit goal to git (continuing anyway)"
    }
    
    Write-Success "Goal committed to branch: $branchName"
    
    # Update agent context
    try {
        Update-AgentContext | Out-Null
    } catch {
        Write-Warning "Failed to update agent context (continuing anyway)"
    }
    
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
New-Goal -GoalDescription $GoalDescription -DryRun $DryRun -Force $Force -JsonMode $Json 