param(
    [switch]$Verbose = $false,
    [switch]$Force = $false
)

# Setup script for goal-driven development

# Load common utilities
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. "$scriptDir\common.ps1"

# Function to display usage information
function Show-Usage {
    Write-Host "Usage: $($MyInvocation.MyCommand.Name) [OPTIONS]" -ForegroundColor Cyan
    ""
    "Setup the current goal for development by ensuring all required files and configurations are in place."
    ""
    "OPTIONS:"
    "    -Verbose          Enable verbose output"
    "    -Force           Force recreation of existing files"
    "    -h, -?           Show this help message"
    ""
    "EXAMPLES:"
    "    $($MyInvocation.MyCommand.Name)"
    "    $($MyInvocation.MyCommand.Name) -Verbose"
    "    $($MyInvocation.MyCommand.Name) -Force"
    ""
}

# Show help if requested
if ($args -contains "-h" -or $args -contains "-?") {
    Show-Usage
    exit 0
}

# Validate we're in a goal directory
Test-GoalContext

# Get current goal information
$goalDir = Get-Location
$goalName = Get-CurrentGoalName
$projectRoot = Get-GitRoot

if ($Verbose) {
    Write-Info "Setting up goal: $goalName"
    Write-Info "Goal directory: $goalDir"
    Write-Info "Project root: $projectRoot"
}

# Check if required files exist
$requiredFiles = @("goal.md")
$missingFiles = @()

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Error "Missing required files: $($missingFiles -join ', ')"
    Write-Info "Please create the missing files or use create-new-goal.ps1 to set up a proper goal"
    exit 1
}

# Create strategies.md if it doesn't exist or force is specified
$strategiesFile = "strategies.md"
if (-not (Test-Path $strategiesFile) -or $Force) {
    if ($Verbose) {
        Write-Info "Creating strategies.md"
    }

    $goalStatement = Get-Content "goal.md" | Where-Object { $_ -like "*Goal Statement*" } | Select-Object -First 1
    $goalStatement = $goalStatement -replace ".*Goal Statement:\s*", "" -replace "\*\*", ""

    $strategiesContent = @"
// Strategy Exploration: $goalStatement

**Branch**: \`$goalDirName\` | **Date**: $(Get-Date -Format "yyyy-MM-dd") | **Goal**: [link]
**Input**: Goal definition from \`goal.md\`

## 🎯 Strategy Overview

**Goal Focus**: $goalStatement

**Strategy Mindset**: Multiple valid approaches exist and should be explored

## 🔍 Strategy Exploration Framework

### Technical Strategy Options

#### Option 1: [Technical Approach Name]
**Description**: [How this technical approach would work]

**Pros**:
- [Advantage 1]
- [Advantage 2]
- [Advantage 3]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]
- [Disadvantage 3]

**Risks & Mitigations**:
- **Risk**: [Potential issue] → **Mitigation**: [How to address]
- **Risk**: [Potential issue] → **Mitigation**: [How to address]

**Measurement Approach**:
- **Success Indicators**: [How to measure if this strategy works]
- **Learning Goals**: [What to learn from trying this approach]

#### Option 2: [Technical Approach Name]
**Description**: [How this technical approach would work]

**Pros**:
- [Advantage 1]
- [Advantage 2]
- [Advantage 3]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]
- [Disadvantage 3]

**Risks & Mitigations**:
- **Risk**: [Potential issue] → **Mitigation**: [How to address]
- **Risk**: [Potential issue] → **Mitigation**: [How to address]

**Measurement Approach**:
- **Success Indicators**: [How to measure if this strategy works]
- **Learning Goals**: [What to learn from trying this approach]

### User Experience Strategy Options

#### UX Approach 1: [User Journey Pattern]
**Description**: [How users would interact with this solution]

**User Flow**:
1. [Step 1 in user journey]
2. [Step 2 in user journey]
3. [Step 3 in user journey]

**Cognitive Load**: [How demanding is this approach for users?]

**Accessibility Considerations**: [How well does this work for different user abilities?]

**Measurement Approach**:
- **User Behavior Metrics**: [What user actions to track]
- **Satisfaction Indicators**: [How to measure user experience]

#### UX Approach 2: [Alternative User Journey Pattern]
**Description**: [How users would interact with this alternative solution]

**User Flow**:
1. [Step 1 in user journey]
2. [Step 2 in user journey]
3. [Step 3 in user journey]

**Cognitive Load**: [How demanding is this approach for users?]

**Accessibility Considerations**: [How well does this work for different user abilities?]

**Measurement Approach**:
- **User Behavior Metrics**: [What user actions to track]
- **Satisfaction Indicators**: [How to measure user experience]

### Implementation Strategy Options

#### Implementation Approach 1: [Development Strategy]
**Description**: [How to build and deploy this solution]

**Development Phases**:
1. **Phase 1**: [Initial development focus]
2. **Phase 2**: [Expansion and optimization]
3. **Phase 3**: [Scaling and maintenance]

**Resource Requirements**:
- **Team Skills**: [What expertise is needed]
- **Technology**: [What tools and platforms required]
- **Timeline**: [Rough development schedule]

**Risks & Mitigations**:
- **Risk**: [Development challenge] → **Mitigation**: [How to address]
- **Risk**: [Timeline issue] → **Mitigation**: [How to address]

#### Implementation Approach 2: [Alternative Development Strategy]
**Description**: [Alternative way to build and deploy this solution]

**Development Phases**:
1. **Phase 1**: [Initial development focus]
2. **Phase 2**: [Expansion and optimization]
3. **Phase 3**: [Scaling and maintenance]

**Resource Requirements**:
- **Team Skills**: [What expertise is needed]
- **Technology**: [What tools and platforms required]
- **Timeline**: [Rough development schedule]

**Risks & Mitigations**:
- **Risk**: [Development challenge] → **Mitigation**: [How to address]
- **Risk**: [Timeline issue] → **Mitigation**: [How to address]

## 📊 Strategy Comparison Matrix

| Strategy | Technical Feasibility | User Experience | Development Effort | Risk Level | Learning Potential |
|----------|----------------------|-----------------|-------------------|------------|-------------------|
| [Strategy 1] | [High/Medium/Low] | [High/Medium/Low] | [High/Medium/Low] | [High/Medium/Low] | [High/Medium/Low] |
| [Strategy 2] | [High/Medium/Low] | [High/Medium/Low] | [High/Medium/Low] | [High/Medium/Low] | [High/Medium/Low] |

## 🎯 Recommended Starting Strategy

### Primary Recommendation: [Strategy Name]

**Why This Strategy First**:
- [Reason 1 - e.g., highest learning potential]
- [Reason 2 - e.g., lowest risk]
- [Reason 3 - e.g., fastest validation]

**Success Criteria for This Strategy**:
- [What would make this strategy successful]
- [When to consider it validated]
- [When to pivot to alternative strategies]

### Fallback Strategies
**If Primary Strategy Shows Issues**:
1. **Pivot Trigger**: [When to switch approaches]
2. **Alternative 1**: [Backup strategy]
3. **Alternative 2**: [Backup strategy]

## 🔬 Validation Experiments

### Critical Assumption Tests
- **Assumption 1**: [What to test] → **Experiment**: [How to test it]
- **Assumption 2**: [What to test] → **Experiment**: [How to test it]
- **Assumption 3**: [What to test] → **Experiment**: [How to test it]

### Measurement Plan
- **What to Measure**: [Key metrics for strategy validation]
- **How to Measure**: [Data collection approach]
- **Success Thresholds**: [When strategy is considered working]

## 🚀 Implementation Milestones by Strategy

### If Strategy 1 is Chosen
- **Milestone 1.1**: [Strategy-specific milestone]
- **Milestone 1.2**: [Strategy-specific milestone]
- **Milestone 1.3**: [Strategy-specific milestone]

### If Strategy 2 is Chosen
- **Milestone 2.1**: [Strategy-specific milestone]
- **Milestone 2.2**: [Strategy-specific milestone]
- **Milestone 2.3**: [Strategy-specific milestone]

## 💡 Learning Agenda

### Technical Learning Goals
- [What technical approaches to evaluate]
- [What works well in this domain]
- [What to avoid in future projects]

### User Experience Learning Goals
- [What user patterns are most effective]
- [What causes user confusion or frustration]
- [What delights users and drives engagement]

### Process Learning Goals
- [What development approaches work best]
- [How to measure progress effectively]
- [When to pivot vs persevere]

## 🔄 Strategy Adaptation Framework

### Regular Strategy Reviews
- **Weekly**: [What to review about current strategy]
- **Bi-weekly**: [Strategic alignment check]
- **Monthly**: [Overall approach assessment]

### Pivot Decision Framework
**Continue Current Strategy When**:
- [Indicators that current approach is working]
- [Metrics showing progress toward goals]
- [User feedback is positive]

**Consider Pivot When**:
- [Warning signs that strategy needs change]
- [Metrics not improving despite effort]
- [User feedback indicates problems]

**Strategy Switch Process**:
1. [Step 1 in switching strategies]
2. [Step 2 in switching strategies]
3. [Step 3 in switching strategies]

---

*This strategy document explores multiple approaches for achieving the defined goal. It should be updated as learning occurs and strategies are validated or discarded.*
"@

    $strategiesContent | Out-File $strategiesFile -Encoding UTF8

    if ($Force) {
        Write-Success "Recreated strategies.md"
    }
    else {
        Write-Success "Created strategies.md"
    }
}

# Create milestones.md if it doesn't exist or force is specified
$milestonesFile = "milestones.md"
if (-not (Test-Path $milestonesFile) -or $Force) {
    if ($Verbose) {
        Write-Info "Creating milestones.md"
    }

    $milestonesContent = @"
// Milestones: $(Get-Content "goal.md" | Where-Object { $_ -like "*Goal Definition*" } | Select-Object -First 1 | ForEach-Object { $_ -replace ".*Goal Definition:\s*", "" } -replace "#", "")

**Branch**: \`$goalDirName\` | **Date**: $(Get-Date -Format "yyyy-MM-dd") | **Strategy**: [link]
**Input**: Goal definition and selected strategies

## 🎯 Milestones Overview

**Goal Focus**: $(Get-Content "goal.md" | Where-Object { $_ -like "*Goal Statement*" } | Select-Object -First 1 | ForEach-Object { $_ -replace ".*Goal Statement:\s*", "" } -replace "\*\*", "")

**Strategy Context**: [Which strategies these milestones support]

**Learning Focus**: [What we want to learn from these milestones]

## 📊 Milestone Definition Framework

### Milestone 1: [Milestone Title] (Priority: P1)

**Description**: [What this milestone achieves and why it matters]

**Success Indicators**:
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]

**Learning Objectives**:
- **Hypothesis**: [What assumption this milestone tests]
- **Validation Method**: [How to confirm the hypothesis]
- **Success Criteria**: [When hypothesis is considered validated]

**Value Delivered**:
- **User Value**: [What users gain from this milestone]
- **Business Value**: [What business benefits from this milestone]
- **Learning Value**: [What insights this milestone should generate]

**Implementation Approaches**:
- **Approach 1**: [How this milestone could be implemented]
- **Approach 2**: [Alternative implementation approach]
- **Approach 3**: [Another alternative if needed]

**Measurement Plan**:
- **Metrics to Track**: [What data to collect]
- **Measurement Method**: [How to collect the data]
- **Success Thresholds**: [When milestone is considered achieved]

**Dependencies**:
- **Requires**: [What must be completed first]
- **Enables**: [What this milestone unlocks]

**Risk Assessment**:
- **Risk Level**: [High/Medium/Low]
- **Potential Issues**: [What could go wrong]
- **Mitigation Strategies**: [How to address issues]

---

### Milestone 2: [Milestone Title] (Priority: P2)

**Description**: [What this milestone achieves and why it matters]

**Success Indicators**:
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]

**Learning Objectives**:
- **Hypothesis**: [What assumption this milestone tests]
- **Validation Method**: [How to confirm the hypothesis]
- **Success Criteria**: [When hypothesis is considered validated]

**Value Delivered**:
- **User Value**: [What users gain from this milestone]
- **Business Value**: [What business benefits from this milestone]
- **Learning Value**: [What insights this milestone should generate]

**Implementation Approaches**:
- **Approach 1**: [How this milestone could be implemented]
- **Approach 2**: [Alternative implementation approach]
- **Approach 3**: [Another alternative if needed]

**Measurement Plan**:
- **Metrics to Track**: [What data to collect]
- **Measurement Method**: [How to collect the data]
- **Success Thresholds**: [When milestone is considered achieved]

**Dependencies**:
- **Requires**: [What must be completed first]
- **Enables**: [What this milestone unlocks]

**Risk Assessment**:
- **Risk Level**: [High/Medium/Low]
- **Potential Issues**: [What could go wrong]
- **Mitigation Strategies**: [How to address issues]

---

### Milestone 3: [Milestone Title] (Priority: P3)

**Description**: [What this milestone achieves and why it matters]

**Success Indicators**:
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]

**Learning Objectives**:
- **Hypothesis**: [What assumption this milestone tests]
- **Validation Method**: [How to confirm the hypothesis]
- **Success Criteria**: [When hypothesis is considered validated]

**Value Delivered**:
- **User Value**: [What users gain from this milestone]
- **Business Value**: [What business benefits from this milestone]
- **Learning Value**: [What insights this milestone should generate]

**Implementation Approaches**:
- **Approach 1**: [How this milestone could be implemented]
- **Approach 2**: [Alternative implementation approach]
- **Approach 3**: [Another alternative if needed]

**Measurement Plan**:
- **Metrics to Track**: [What data to collect]
- **Measurement Method**: [How to collect the data]
- **Success Thresholds**: [When milestone is considered achieved]

**Dependencies**:
- **Requires**: [What must be completed first]
- **Enables**: [What this milestone unlocks]

**Risk Assessment**:
- **Risk Level**: [High/Medium/Low]
- **Potential Issues**: [What could go wrong]
- **Mitigation Strategies**: [How to address issues]

---

## 📈 Progress Tracking Framework

### Overall Progress Metrics
- **Goal Progress**: [How to measure overall progress toward the goal]
- **Milestone Velocity**: [How to track speed of milestone completion]
- **Learning Progress**: [How to measure insights and discoveries]

### Milestone Health Indicators
- **On Track**: [Indicators that milestone is progressing well]
- **At Risk**: [Warning signs that milestone needs attention]
- **Blocked**: [Indicators that milestone cannot proceed]

### Adaptation Triggers
- **Accelerate**: [When to speed up milestone execution]
- **Slow Down**: [When to take more time for learning]
- **Pivot**: [When to change milestone approach or sequence]

## 🔄 Milestone Review Process

### Review Cadence
- **After Each Milestone**: [What to review and how]
- **Bi-weekly**: [Regular progress check]
- **Monthly**: [Strategic milestone alignment review]

### Review Framework
**For Each Completed Milestone**:
1. **Measure Results**: [Compare actual vs expected outcomes]
2. **Capture Learning**: [Document what was discovered]
3. **Assess Strategy**: [Evaluate if current approach is working]
4. **Plan Next Steps**: [Adjust subsequent milestones if needed]

**For In-Progress Milestones**:
1. **Progress Assessment**: [Current status vs plan]
2. **Risk Review**: [Identify new risks or issues]
3. **Resource Check**: [Ensure adequate support]
4. **Adjustment Planning**: [Plan any needed changes]

### Decision Framework
**Continue Current Path When**:
- [Indicators that current milestone approach is working]
- [Metrics showing expected progress]
- [Learning supporting current strategy]

**Modify Approach When**:
- [Indicators that current approach needs adjustment]
- [New information suggesting better alternatives]
- [External factors requiring adaptation]

**Reprioritize Milestones When**:
- [Learning suggests different milestone sequence]
- [Business priorities change]
- [Technical constraints require reordering]

## 📊 Success Validation

### Milestone Success Criteria
**For Each Milestone**:
- [ ] Defined success indicators achieved
- [ ] Learning objectives met
- [ ] Value delivered to users or business
- [ ] No significant negative consequences
- [ ] Insights documented for future use

### Goal Progress Indicators
- [ ] Milestone 1 contributes to overall goal
- [ ] Milestone 2 builds on milestone 1 learning
- [ ] Milestone 3 delivers cumulative goal progress
- [ ] Overall trajectory toward goal achievement

### Learning Quality Assessment
- [ ] Technical insights captured and documented
- [ ] User behavior patterns identified
- [ ] Process improvements identified
- [ ] Strategic direction validated or adjusted

## 🚀 Implementation Flexibility

### Technical Flexibility
- **Multiple Implementation Options**: Each milestone can be achieved through different technical approaches
- **Progressive Enhancement**: Start simple and add complexity based on learning
- **Fallback Options**: Alternative implementation paths if primary approach fails

### Scope Flexibility
- **Milestone Splitting**: Large milestones can be broken into smaller, faster-validated pieces
- **Milestone Merging**: Related milestones can be combined for efficiency
- **Milestone Scope Adjustment**: Individual milestone scope can be adjusted based on learning

### Timing Flexibility
- **Parallel Execution**: Independent milestones can be pursued simultaneously
- **Sequential Dependencies**: Some milestones must follow others
- **Adaptive Scheduling**: Timeline adjusted based on milestone progress and learning

## 💡 Learning Integration

### Knowledge Capture
- **Technical Learnings**: What works, what doesn't, why
- **User Insights**: Behavior patterns, preferences, pain points
- **Process Improvements**: Better ways to approach similar milestones
- **Risk Patterns**: Common pitfalls and how to avoid them

### Cross-Milestone Learning
- **Pattern Recognition**: Similar challenges across milestones
- **Solution Reuse**: Successful approaches applied to multiple milestones
- **Dependency Discovery**: Unanticipated relationships between milestones
- **Synergy Identification**: Combined value greater than individual milestones

---

*This milestones document defines measurable progress steps toward the goal. It should be updated as learning occurs and strategies evolve.*
"@

    $milestonesContent | Out-File $milestonesFile -Encoding UTF8

    if ($Force) {
        Write-Success "Recreated milestones.md"
    }
    else {
        Write-Success "Created milestones.md"
    }
}

# Create execution.md if it doesn't exist or force is specified
$executionFile = "execution.md"
if (-not (Test-Path $executionFile) -or $Force) {
    if ($Verbose) {
        Write-Info "Creating execution.md"
    }

    $executionContent = @"
// Adaptive Execution: $(Get-Content "goal.md" | Where-Object { $_ -like "*Goal Definition*" } | Select-Object -First 1 | ForEach-Object { $_ -replace ".*Goal Definition:\s*", "" } -replace "#", "")

**Branch**: \`$goalDirName\` | **Date**: $(Get-Date -Format "yyyy-MM-dd") | **Milestones**: [link]
**Input**: Goal definition, selected strategies, and milestone plan

## 🚀 Execution Overview

**Goal Focus**: $(Get-Content "goal.md" | Where-Object { $_ -like "*Goal Statement*" } | Select-Object -First 1 | ForEach-Object { $_ -replace ".*Goal Statement:\s*", "" } -replace "\*\*", "")

**Starting Milestone**: [Which milestone to implement first]

**Learning Mindset**: Implementation as a learning journey with flexibility to adapt

## 🎯 Execution Strategy

### Current Milestone Focus
**Milestone**: [Name of milestone being executed]

**Hypothesis**: [What assumption this milestone tests]

**Success Criteria**: [How to know this milestone is successful]

### Implementation Approach
**Selected Strategy**: [Which strategy to use for this milestone]

**Why This Approach**:
- [Reason 1 for choosing this strategy]
- [Reason 2 for choosing this strategy]
- [Reason 3 for choosing this strategy]

**Alternative Approaches Available**:
- [Alternative 1]: [Brief description and when to switch]
- [Alternative 2]: [Brief description and when to switch]

## 📊 Measurement Framework

### Key Metrics to Track
- **Progress Metrics**: [Indicators of implementation progress]
- **Outcome Metrics**: [Indicators of milestone success]
- **Learning Metrics**: [Indicators of insights gained]

### Measurement Methods
- **Automated Tracking**: [What can be measured automatically]
- **Manual Observation**: [What requires human observation]
- **User Feedback**: [How to collect user input]

### Success Thresholds
- **Minimum Success**: [Lowest acceptable outcome]
- **Target Success**: [Desired outcome level]
- **Exceptional Success**: [Outstanding outcome level]

## 🔄 Learning Loop Process

### Daily Learning Loop
**Build Phase**:
- [What to implement each day]
- [What experiments to run]
- [What feedback to collect]

**Measure Phase**:
- [What data to review daily]
- [What patterns to look for]
- [What concerns to monitor]

**Learn Phase**:
- [What insights to document]
- [What adjustments to consider]
- [What to communicate to stakeholders]

### Weekly Learning Loop
**Build Phase**:
- [Weekly implementation goals]
- [Weekly experiments planned]
- [Weekly stakeholder updates]

**Measure Phase**:
- [Weekly metric review]
- [Weekly progress assessment]
- [Weekly risk evaluation]

**Learn Phase**:
- [Weekly insight summary]
- [Weekly strategy adjustments]
- [Weekly planning for next week]

## 🎛️ Adaptation Framework

### Progress Indicators
**On Track Indicators**:
- [Signs that milestone is progressing well]
- [Metrics showing expected improvement]
- [Feedback indicating positive direction]

**Warning Indicators**:
- [Early warning signs of problems]
- [Metrics not improving as expected]
- [Feedback suggesting issues]

**Critical Indicators**:
- [Signs that current approach is failing]
- [Metrics showing negative trends]
- [Feedback indicating major problems]

### Adaptation Decision Matrix

| Situation | Metrics | User Feedback | Action |
|-----------|---------|---------------|--------|
| **All Good** | ✅ On target | 😊 Positive | Continue current approach |
| **Minor Issues** | ⚠️ Slightly off | 😐 Mixed | Small adjustments to current approach |
| **Major Issues** | ❌ Well off target | 😞 Negative | Consider alternative approach |
| **Critical Failure** | 💥 Completely failing | 😤 Very negative | Switch to different strategy |

### Pivot Decision Process
**When to Consider Pivot**:
1. **Trigger**: [Specific condition that triggers pivot consideration]
2. **Assessment**: [How to evaluate whether to pivot]
3. **Decision**: [How to decide whether to pivot]
4. **Execution**: [How to execute the pivot]

**Pivot Options**:
- **Strategy Pivot**: Switch to different technical/user approach
- **Scope Pivot**: Change what the milestone delivers
- **Sequence Pivot**: Reorder milestone execution
- **Goal Pivot**: Question if milestone is still relevant

## 📝 Daily Execution Guide

### Daily Standup Questions
- **What did I accomplish yesterday?** [Focus on measurable progress]
- **What will I accomplish today?** [Specific, measurable goals]
- **What obstacles are in my way?** [Clear blockers or concerns]
- **What did I learn yesterday?** [Key insights or discoveries]

### Daily Work Structure
**Morning (Planning)**:
- [Review previous day's results]
- [Set specific daily goals]
- [Identify potential obstacles]

**Midday (Execution)**:
- [Focus on implementation work]
- [Monitor key metrics]
- [Collect feedback and insights]

**Afternoon (Reflection)**:
- [Review progress against goals]
- [Document learning and insights]
- [Plan adjustments for next day]

## 🚨 Risk Management

### Identified Risks
**Risk 1**: [Potential problem]
- **Probability**: [High/Medium/Low]
- **Impact**: [High/Medium/Low]
- **Mitigation**: [How to reduce probability or impact]

**Risk 2**: [Potential problem]
- **Probability**: [High/Medium/Low]
- **Impact**: [High/Medium/Low]
- **Mitigation**: [How to reduce probability or impact]

**Risk 3**: [Potential problem]
- **Probability**: [High/Medium/Low]
- **Impact**: [High/Medium/Low]
- **Mitigation**: [How to reduce probability or impact]

### Risk Monitoring
- **Daily Risk Check**: [What risks to monitor each day]
- **Escalation Triggers**: [When to escalate risks to stakeholders]
- **Risk Documentation**: [How to document new risks discovered]

## 📚 Knowledge Capture

### What to Document
**Technical Learning**:
- [What technical approaches work well]
- [What technical approaches to avoid]
- [Technical patterns discovered]

**User Learning**:
- [User behavior patterns observed]
- [User preferences discovered]
- [User pain points identified]

**Process Learning**:
- [What development processes work]
- [What measurement approaches are effective]
- [What communication patterns help]

### Documentation Format
**Daily Summary**:
- **Accomplishments**: [What was achieved]
- **Metrics**: [Key numbers from the day]
- **Learning**: [Key insights discovered]
- **Tomorrow**: [Plan for next day]

**Weekly Summary**:
- **Progress**: [Overall milestone progress]
- **Insights**: [Major discoveries of the week]
- **Adjustments**: [Changes made based on learning]
- **Next Week**: [Priorities for coming week]

## 🎯 Milestone Completion Criteria

### Success Indicators
- [ ] Primary success metrics achieved
- [ ] User feedback validates the outcome
- [ ] Learning objectives accomplished
- [ ] No critical issues discovered
- [ ] Value delivered to users/business

### Quality Gates
**Before Milestone Completion**:
- [ ] All success indicators met or exceeded
- [ ] Learning objectives documented
- [ ] User feedback collected and analyzed
- [ ] Risks assessed and mitigated
- [ ] Next steps identified

### Handoff Checklist
**Before Moving to Next Milestone**:
- [ ] Current milestone fully documented
- [ ] Learning transferred to next milestone planning
- [ ] Metrics baseline established for next phase
- [ ] Stakeholder communication completed

## 🔄 Next Steps Planning

### Immediate Next Actions
- [ ] Action 1: [What to do right after milestone completion]
- [ ] Action 2: [What to do right after milestone completion]
- [ ] Action 3: [What to do right after milestone completion]

### Next Milestone Preparation
- [ ] Review next milestone requirements
- [ ] Apply learning from current milestone
- [ ] Adjust next milestone plan if needed
- [ ] Communicate changes to stakeholders

### Long-term Learning Integration
- [ ] Update goal definition based on learning
- [ ] Revise strategy options for future milestones
- [ ] Document patterns for similar future goals
- [ ] Share insights with broader team

---

*This execution guide provides a framework for adaptive implementation with continuous learning. It should be updated as new insights are gained and circumstances change.*
"@

    $executionContent | Out-File $executionFile -Encoding UTF8

    if ($Force) {
        Write-Success "Recreated execution.md"
    }
    else {
        Write-Success "Created execution.md"
    }
}

# Update agent context
Update-AgentContext

# Print summary
Write-Success "Goal setup completed!"
""
Write-Info "Created files:"
"  - goal.md (already existed)"
"  - strategies.md"
"  - milestones.md"
"  - execution.md"
""
Write-Info "Next Steps:"
"  1. Review and customize the generated files"
"  2. Use /goalkit.strategies to explore implementation approaches"
"  3. Use /goalkit.milestones to refine milestone definitions"
"  4. Use /goalkit.execute to implement with learning and adaptation"
""
Write-Info "Current branch: $(git branch --show-current)"
Write-Info "Goal directory: $goalDir"

# Setup goal environment
Set-GoalEnvironment -GoalDir $goalDir