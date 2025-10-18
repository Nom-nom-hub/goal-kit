# Create a new collaboration plan in a Goal Kit project
# Supports both single-agent coordination and multi-agent coordination

param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$CollaborationDescription,
    [switch]$DryRun,
    [switch]$Verbose,
    [switch]$JsonMode
)

# Get script directory
$ScriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
$CommonScript = Join-Path $ScriptDir "common.ps1"

# Dot source common utilities
if (Test-Path $CommonScript) {
    . $CommonScript
}
else {
    Write-Error "Common utilities script not found: $CommonScript"
    exit 1
}

if ($Verbose) {
    Write-Host "Collaboration script started" -ForegroundColor Cyan
}

# Validate arguments
$CollabDescription = $CollaborationDescription -join " "
if ([string]::IsNullOrWhiteSpace($CollabDescription)) {
    Write-Host "Error: Collaboration description is required" -ForegroundColor Red
    Write-Host "Usage: setup-collaboration.ps1 [-DryRun] [-Verbose] <CollaborationDescription>" -ForegroundColor Yellow
    exit 1
}

# Check if we're in a git repository
if (-not (Test-GitRepo)) {
    Write-Host "Error: Not in a git repository" -ForegroundColor Red
    Write-Host "Please run this from the root of a Goal Kit project" -ForegroundColor Yellow
    exit 1
}

# Get project root
$ProjectRoot = Get-GitRoot
Set-Location $ProjectRoot

# Check if this is a Goal Kit project
$VisionFilePath = Join-Path $ProjectRoot ".goalkit" "vision.md"
if (-not (Test-Path $VisionFilePath)) {
    Write-Host "Error: Not a Goal Kit project" -ForegroundColor Red
    Write-Host "Please run 'goalkeeper init' first to set up the project" -ForegroundColor Yellow
    exit 1
}

# If JSON mode, output JSON and exit early
if ($JsonMode -or $env:JSON_MODE -eq "true") {
    # Find the next collaboration number (use same numbering as goals)
    $NextNumber = 1
    $CollabsDir = "collaborations"
    $CollabsPath = Join-Path $ProjectRoot $CollabsDir
    
    if (Test-Path $CollabsPath) {
        $CollabDirs = Get-ChildItem -Path $CollabsPath -Directory | Where-Object { $_.Name -match "^\d+-" }
        foreach ($dir in $CollabDirs) {
            $dirName = $dir.Name
            $num = [int]($dirName -replace "^(\d+)-.*", '$1')
            if ($num -ge $NextNumber) {
                $NextNumber = $num + 1
            }
        }
    }

    # Create collaboration directory name
    $CollabNumber = $NextNumber.ToString("D3")
    $CleanDescription = $CollabDescription -replace '[^a-zA-Z0-9\s-]', '' -replace '\s+', '-' -replace '--+', '-'
    $CleanDescription = $CleanDescription.ToLower()
    $CollabDirName = "${CollabNumber}-${CleanDescription}"
    $CollabDir = Join-Path $CollabsDir $CollabDirName
    $CollabFile = Join-Path $CollabDir "collaboration.md"
    
    # Output JSON with required variables
    $JsonData = @{
        COLLAB_DIR = $CollabDir
        COLLAB_FILE = $CollabFile
        COLLAB_DESCRIPTION = $CollabDescription
        BRANCH_NAME = $CollabDirName
    } | ConvertTo-Json -Compress
    
    Write-Output $JsonData
    exit 0
}

# Check if collaborations directory exists
$CollabsDir = "collaborations"
$CollabsPath = Join-Path $ProjectRoot $CollabsDir

if (-not (Test-Path $CollabsPath)) {
    if ($DryRun) {
        Write-Host "[DRY RUN] Would create collaborations directory: $CollabsDir" -ForegroundColor Yellow
    }
    else {
        New-Item -ItemType Directory -Path $CollabsPath -Force | Out-Null
        Write-Host "Created collaborations directory: $CollabsDir" -ForegroundColor Green
    }
}

# Find the next collaboration number (use same numbering as goals)
$NextNumber = 1
if (Test-Path $CollabsPath) {
    $CollabDirs = Get-ChildItem -Path $CollabsPath -Directory | Where-Object { $_.Name -match "^\d+-" }
    foreach ($dir in $CollabDirs) {
        $dirName = $dir.Name
        $num = [int]($dirName -replace "^(\d+)-.*", '$1')
        if ($num -ge $NextNumber) {
            $NextNumber = $num + 1
        }
    }
}

# Create collaboration directory name
$CollabNumber = $NextNumber.ToString("D3")
$CleanDescription = $CollabDescription -replace '[^a-zA-Z0-9\s-]', '' -replace '\s+', '-' -replace '--+', '-'
$CleanDescription = $CleanDescription.ToLower()
$CollabDirName = "${CollabNumber}-${CleanDescription}"
$CollabDir = Join-Path $CollabsDir $CollabDirName

# Check if collaboration directory already exists
if (Test-Path (Join-Path $ProjectRoot $CollabDir)) {
    Write-Host "Error: Collaboration directory already exists: $CollabDir" -ForegroundColor Red
    Write-Host "Use a different collaboration description or remove the existing directory" -ForegroundColor Yellow
    exit 1
}

if ($DryRun) {
    Write-Host "[DRY RUN] Would create collaboration directory: $CollabDir" -ForegroundColor Yellow
    Write-Host "[DRY RUN] Would create collaboration.md with description: $CollabDescription" -ForegroundColor Yellow
    Write-Host "[DRY RUN] Would create branch: $CollabDirName" -ForegroundColor Yellow
    exit 0
}

# Create collaboration directory
New-Item -ItemType Directory -Path (Join-Path $ProjectRoot $CollabDir) -Force | Out-Null
Write-Host "Created collaboration directory: $CollabDir" -ForegroundColor Green

# Create collaboration.md file with coordination structure
$CollaborationContent = @"
# Collaboration Plan: $CollabDescription

**Branch**: `$CollabDirName`$
**Created**: $(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
**Mode**: [Single-Agent/Multi-Agent/Self-Coordination]
**Status**: Draft

## 🤝 Collaboration Overview

**Coordination Statement**: $CollabDescription

**Context**: [Why is this coordination important? What coordination challenge does it solve?]

**Participants**: [List of agents, systems, or processes involved in coordination - use "Self" for single-agent coordination]

**Success Level**: [What "successful coordination" looks like for this collaboration]

## 🎯 Coordination Mode

### Selected Mode: [Single-Agent Mode | Multi-Agent Mode | Self-Coordination Mode]

**Mode Justification**: [Why this coordination mode was selected - detected agents, user input, or default behavior]

### Single-Agent Mode Features
- **Self-Consistency**: Maintaining consistency across different interactions with the same agent
- **State Tracking**: Tracking decision state across different sessions
- **Progress Validation**: Validating previous decisions remain valid

### Multi-Agent Mode Features (If Applicable)
- **Agent Awareness**: Agents aware of work done by other agents
- **Conflict Detection**: Identifying potential conflicts between agent work
- **Task Synchronization**: Coordinating work between agents to avoid conflicts
- **Knowledge Sharing**: Agents can access information created by other agents

### Self-Coordination Mode Features
- **State Consistency**: Ensuring the agent maintains consistency with its own previous work
- **Self-Verification**: Checking if previous decisions are still valid
- **Progress Tracking**: Maintaining awareness of own progress over time

## 📊 Coordination Success Metrics

### Primary Metrics (Must achieve for successful coordination)

- **Metric 1**: [Measurable coordination outcome] - Target: [specific, quantifiable target]
- **Metric 2**: [Measurable coordination outcome] - Target: [specific, quantifiable target]
- **Metric 3**: [Measurable coordination outcome] - Target: [specific, quantifiable target]

### Secondary Metrics (Valuable but not required)

- **Metric 1**: [Nice-to-have coordination outcome] - Target: [aspirational target]
- **Metric 2**: [Nice-to-have coordination outcome] - Target: [aspirational target]

## 👥 Coordination Participants & Roles

### Coordination Participants
- **[Participant 1]**: [Role in coordination - what they do]
- **[Participant 2]**: [Role in coordination - what they do]

### Coordination Responsibilities
- **[Responsibility 1]**: [Who handles this coordination task]
- **[Responsibility 2]**: [Who handles this coordination task]

## 🎯 Coordination Activities

### Activity 1: [Activity Title] (Priority: P1)
**Description**: [What this coordination activity achieves]

**Success Indicators**:
- [Measurable coordination outcome 1]
- [Measurable coordination outcome 2]

**Validation Method**: [How to confirm this coordination activity is achieved]

**Expected Timeline**: [Rough time estimate]

**Owner**: [Who is responsible for this activity]

---

### Activity 2: [Activity Title] (Priority: P2)
**Description**: [What this coordination activity achieves]

**Success Indicators**:
- [Measurable coordination outcome 1]
- [Measurable coordination outcome 2]

**Validation Method**: [How to confirm this coordination activity is achieved]

**Expected Timeline**: [Rough time estimate]

**Owner**: [Who is responsible for this activity]

---

### Activity 3: [Activity Title] (Priority: P3)
**Description**: [What this coordination activity achieves]

**Success Indicators**:
- [Measurable coordination outcome 1]
- [Measurable coordination outcome 2]

**Validation Method**: [How to confirm this coordination activity is achieved]

**Expected Timeline**: [Rough time estimate]

**Owner**: [Who is responsible for this activity]

---

## 🔗 Coordination Dependencies

### Coordination Dependencies
- **[Dependency 1]**: [What this coordination depends on]
- **[Dependency 2]**: [What this coordination depends on]

### Coordination Impacts
- **[Impact 1]**: [What this coordination affects]
- **[Impact 2]**: [What this coordination affects]

## 🗣️ Communication Plan

### Communication Channels
- **[Channel 1]**: [How coordination information is shared]
- **[Channel 2]**: [How coordination information is shared]

### Communication Frequency
- **Status Updates**: [How often coordination status is checked/shared]
- **Conflict Resolution**: [How conflicts are communicated and resolved]

### Communication Protocol
- **[Protocol 1]**: [How coordination information is formatted/shared]
- **[Protocol 2]**: [How coordination information is formatted/shared]

## 🔄 Synchronization Points

### Synchronization Events
- **[Event 1]**: [When coordination alignment happens]
- **[Event 2]**: [When coordination alignment happens]

### Synchronization Process
- **[Process 1]**: [How coordination alignment is achieved]
- **[Process 2]**: [How coordination alignment is achieved]

## ⚠️ Conflict Resolution

### Potential Conflicts
- **[Conflict 1]**: [What could go wrong in coordination]
- **[Conflict 2]**: [What could go wrong in coordination]

### Resolution Approaches
- **[Approach 1]**: [How to resolve this type of conflict]
- **[Approach 2]**: [How to resolve this type of conflict]

## 📈 Coordination Validation Strategy

### Measurement Approach
- **Data Sources**: [Where to collect coordination metrics from]
- **Measurement Frequency**: [How often to measure coordination effectiveness]
- **Success Thresholds**: [When to consider the coordination successful]

### Learning Objectives
- **What to Learn**: [Key insights to gain from coordination]
- **Adaptation Points**: [When to reconsider the coordination approach]
- **Documentation**: [What coordination information to document for future reference]

## 📋 Coordination Checkpoints

### Coordination Milestones
- **[Milestone 1]**: [Coordination achievement to reach]
- **[Milestone 2]**: [Coordination achievement to reach]

### Coordination Verification Points
- **[Verification 1]**: [When to verify coordination is working properly]
- **[Verification 2]**: [When to verify coordination is working properly]

## 🚀 Coordination Implementation

### Setup Requirements
- **[Requirement 1]**: [What needs to be set up for coordination]
- **[Requirement 2]**: [What needs to be set up for coordination]

### Implementation Steps
1. **Step 1**: [First step in coordination implementation]
2. **Step 2**: [Second step in coordination implementation]
3. **Step 3**: [Third step in coordination implementation]

## 🏁 Coordination Completion Criteria

### Success Indicators
- [ ] Primary coordination metrics achieved at target levels
- [ ] Coordination objectives validated through measurement
- [ ] All coordination participants aligned and informed
- [ ] No significant coordination conflicts discovered
- [ ] Coordination learning objectives accomplished

### Success Validation
- **[Validation 1]**: [How to confirm coordination was successful]
- **[Validation 2]**: [How to confirm coordination was successful]

## 🔁 Coordination Review & Adaptation

### Regular Review Schedule
- **After Each Activity**: [What to review and how]
- **Weekly**: [Coordination effectiveness assessment]
- **When Conflicts Arise**: [How to reassess coordination approach]

### Adaptation Triggers
- **Pivot Trigger 1**: [When to change coordination approach]
- **Pause Trigger**: [When to temporarily adjust coordination]
- **Realign Trigger**: [When to reconsider coordination strategy entirely]

## 🔄 Coordination State Management

### State Tracking
- **[State Element 1]**: [What coordination state is tracked]
- **[State Element 2]**: [What coordination state is tracked]

### State Validation
- **[Validation 1]**: [How to ensure coordination state is valid]
- **[Validation 2]**: [How to ensure coordination state is valid]

---

*This collaboration plan serves as the foundation for coordinated work between agents or for maintaining consistency in single-agent environments. It should be reviewed and updated as coordination needs evolve during implementation.*

"@

$CollabFilePath = Join-Path $ProjectRoot $CollabDir "collaboration.md"
Set-Content -Path $CollabFilePath -Value $CollaborationContent -Encoding UTF8
Write-Host "Created collaboration.md with description: $CollabDescription" -ForegroundColor Green

# Get current persona for the collaboration
$CurrentPersona = "general"
$PersonaConfigDir = Join-Path $ProjectRoot ".goalkit" "personas"
$CurrentPersonaFile = Join-Path $PersonaConfigDir "current_persona.txt"
if (Test-Path $CurrentPersonaFile) {
    $CurrentPersona = Get-Content $CurrentPersonaFile -Raw | ForEach-Object { $_.Trim() }
}

# Create git branch for this collaboration
Write-Host "Setting up git branch for this collaboration..." -ForegroundColor Cyan
Set-Location $ProjectRoot
$BranchName = Create-GoalBranch -GoalName $CollabDirName  # Reuse goal branch function

# Add and commit the new collaboration
Set-Location $ProjectRoot
git add $CollabDir
git commit -m "Add collaboration: $CollabDescription

- Created collaboration definition in $CollabDir/collaboration.md
- Branch: $BranchName
- Active persona: $CurrentPersona"

Write-Host "Collaboration committed to branch: $BranchName" -ForegroundColor Green

# Update agent context
Update-AgentContext

# Print summary
Write-Host "Collaboration created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Collaboration Details:" -ForegroundColor Cyan
Write-Host "  Directory: $CollabDir"
Write-Host "  Branch: $BranchName"
Write-Host "  Description: $CollabDescription"
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Navigate to collaboration directory: cd $CollabDir"
Write-Host "  2. Complete the collaboration plan with specific details"
Write-Host "  3. Use coordination features as needed during development"
Write-Host ""
Write-Host "Current branch is: $(git branch --show-current)" -ForegroundColor Cyan

# Setup collaboration environment for immediate development
Setup-GoalEnvironment -GoalDir $CollabDir