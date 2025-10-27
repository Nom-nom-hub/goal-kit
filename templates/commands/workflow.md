---
description: Enforce workflow compliance and methodology adherence across all project components
scripts:
  sh: .goalkit/scripts/python/workflow_enforcer.py --format text
  ps: .goalkit/scripts/python/workflow_enforcer.py --format text
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

# Workflow Enforcement Command

**Purpose**: Validate and enforce compliance with Goal-Driven Development methodology across all project components

**When to Use**:

- To verify methodology compliance after creating components
- Before proceeding to next workflow steps
- To identify and fix workflow violations
- When methodology deviations are suspected

## Quick Prerequisites Check

**BEFORE ENFORCING WORKFLOW**:

1. **Goal Kit project exists**: Verify `.goalkit/` directory structure
2. **Project components created**: Have vision, goals, or other methodology files
3. **Methodology steps followed**: Ensure proper sequence was maintained

**If missing**: Follow methodology sequence before running workflow enforcement.

## Quick Workflow Enforcement Steps

**STEP 1**: Analyze all project components for methodology compliance

**STEP 2**: Check workflow sequence adherence:

- Vision → Goals → Strategies → Milestones → Execute
- Proper file creation and completion
- Validation requirements met

**STEP 3**: Generate compliance report with violations and recommendations

**STEP 4**: Address any identified workflow violations

**STEP 5**: Re-validate after fixes until compliance is achieved

## Compliance Standards

**Mandatory Requirements**:

- **Sequential Flow**: Each methodology step completed before next
- **File Validation**: All required files present and properly structured
- **Quality Thresholds**: Minimum quality scores met (goal: 7.0+, others: 6.0+)
- **Content Requirements**: Proper focus on outcomes vs implementation

**Validation Checks**:

- **File Existence**: Required methodology components present
- **Content Quality**: Proper focus and structure
- **Sequence Compliance**: Proper workflow order followed
- **Quality Assurance**: Minimum quality standards met

## Input Format

```bash
/goalkit.workflow [options]
```

### Command Options

```bash
/goalkit.workflow                    # Run full workflow compliance check
/goalkit.workflow --check            # Quick compliance verification
/goalkit.workflow --json             # Output results in JSON format
```

## Agent Script Execution Guide

**CRITICAL**: When processing `/goalkit.workflow` commands, agents MUST:

### **STEP 1**: Run the workflow enforcement script

```python
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/workflow_enforcer.py --format text
```

### **STEP 2**: If detailed analysis requested

```python
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/workflow_enforcer.py --detailed --format text
```

### **STEP 3**: Parse compliance results

- **Extract violation reports** and compliance status
- **Identify specific issues** that need to be addressed
- **Note recommendations** for compliance improvement
- **Check compliance thresholds** before allowing workflow progression

### **STEP 4**: Make compliance-based decisions

- **Compliant**: "Excellent adherence to methodology - ready to proceed"
- **Minor Violations**: "Address issues before proceeding to next step"
- **Major Violations**: "Significant methodology violations - fix before continuing"

### **STEP 5**: Update agent context with compliance status

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/update_agent_context.py
```

## Output

The command generates:

- **Compliance Report**: Detailed analysis of methodology adherence
- **Violation Identification**: Clear identification of workflow issues
- **Actionable Recommendations**: Specific steps to achieve compliance
- **Compliance Score**: Overall adherence measurement (1-10 scale)

### Workflow Analysis Process

**Multi-Layered Compliance Check**:

1. **Sequence Verification**: Ensure proper methodology flow
2. **Component Validation**: Check each component for completeness
3. **Content Analysis**: Verify content aligns with methodology
4. **Quality Assessment**: Ensure minimum quality standards
5. **Dependency Validation**: Check component interdependencies

## Workflow Components

### 1. Vision Compliance

- **Foundation Required**: Vision file exists and properly structured
- **Quality Threshold**: Vision score meets minimum requirements (6.0+)
- **Content Alignment**: Proper focus on mission and outcomes

### 2. Goal Compliance

- **Goal Definition**: Goals created with clear success metrics
- **Quality Threshold**: Goal score meets minimum requirements (7.0+)
- **Content Focus**: Proper outcome focus, no implementation details

### 3. Strategy Compliance

- **Multiple Approaches**: 3+ strategies explored for each goal
- **Comparative Analysis**: Feasibility and risk assessment completed
- **Validation Planning**: Strategy testing approaches defined

### 4. Milestone Compliance

- **Measurable Progress**: Milestones defined with clear metrics
- **Progress Tracking**: Measurement approaches established
- **Validation Methods**: Success confirmation methods defined

### 5. Execution Compliance

- **Milestone Prerequisites**: Milestones completed before execution
- **Learning Framework**: Implementation includes measurement and adaptation
- **Progress Monitoring**: Execution includes progress tracking

## Compliance Scoring System

### Score Interpretation

- **9-10**: Excellent Compliance - Full methodology adherence
- **7-8**: Good Compliance - Minor areas for improvement
- **5-6**: Partial Compliance - Address key issues before proceeding
- **3-4**: Incomplete Compliance - Significant methodology gaps
- **1-2**: Non-Compliant - Major methodology violations to fix

## Integration with Other Commands

### Workflow Enforcement in Sequence

- **After `/goalkit.vision`**: Verify vision compliance
- **After `/goalkit.goal`**: Verify goal compliance (7.0+ required)
- **After `/goalkit.strategies`**: Verify strategy compliance (6.0+ required)
- **After `/goalkit.milestones`**: Verify milestone compliance (6.0+ required)
- **Before `/goalkit.execute`**: Final compliance check required

### Compliance-Gated Workflow

```bash
/goalkit.vision → Create vision
/goalkit.workflow → Check compliance (6.0+)
/goalkit.goal → Create goal  
/goalkit.workflow → Check compliance (7.0+)
/goalkit.strategies → Explore strategies
/goalkit.workflow → Check compliance (6.0+)
```

## Best Practices

### Regular Compliance Checks

- **After Each Component**: Validate compliance before proceeding
- **Before Major Changes**: Verify current state compliance
- **Weekly Reviews**: Check overall methodology adherence
- **Before Execution**: Final compliance verification

### Addressing Violations

- **Sequence Violations**: Return to proper workflow order
- **Quality Deficiencies**: Improve component quality to standards
- **Missing Components**: Create required components
- **Content Issues**: Correct focus from implementation to outcomes

### Compliance Improvement Process

1. **Run Enforcement**: Identify specific violations
2. **Review Issues**: Understand compliance problems
3. **Implement Fixes**: Address identified violations
4. **Re-validate**: Confirm compliance after fixes
5. **Document Learnings**: Capture improvement insights

## Common Workflow Issues

### Sequence Problems

- **Goals before vision**: Create vision first before goals
- **Execution before milestones**: Complete milestones before executing
- **Strategies before goals**: Define goals before exploring strategies

### Quality Issues

- **Implementation focus**: Replace with outcome focus
- **Vague metrics**: Add specific, measurable targets
- **Missing validation**: Define measurement approaches

### Structure Issues

- **Missing files**: Create required methodology components
- **Incomplete sections**: Fill missing content areas
- **Incorrect format**: Fix structural problems

## Examples

### Example 1: Full Compliance Check

```bash
/goalkit.workflow
```

**Output**: Comprehensive analysis of entire project methodology compliance

### Example 2: Quick Validation

```bash
/goalkit.workflow --check
```

**Output**: Fast compliance verification with pass/fail status

### Example 3: Integration with Validation

```bash
/goalkit.goal Create user engagement goal
/goalkit.validate
/goalkit.workflow
[If compliant] → /goalkit.strategies
[If violations] → Address issues first
```

## Agent Integration

### Compliance-Aware Workflow

**CRITICAL**: Agents should enforce methodology compliance:

1. **Pre-validation**: Run workflow enforcement before allowing progression
2. **Compliance Gates**: Block advancement if compliance thresholds not met
3. **Guidance Provision**: Provide specific steps to address violations
4. **Success Confirmation**: Verify compliance improvements after fixes

### Enforcement Automation

- **Auto-checks**: Run enforcement after each methodology component creation
- **Compliance Reporting**: Include enforcement results in progress updates
- **Trend Tracking**: Monitor compliance improvements over time

## Key Benefits

- **Methodology Assurance**: Ensures Goal-Driven Development principles are followed
- **Early Issue Detection**: Identifies methodology violations before they impact execution
- **Consistency Maintenance**: Keeps project aligned with goal-driven approach
- **Risk Reduction**: Prevents methodology problems from impacting success
- **Quality Maintenance**: Ensures proper focus on outcomes over implementation

## Critical Rules

✅ **DO**: Run compliance checks after creating major components  
✅ **DO**: Address violations before proceeding to next steps
✅ **DO**: Use enforcement feedback for methodology improvement
✅ **DO**: Maintain compliance standards throughout project lifecycle
❌ **DON'T**: Skip workflow enforcement when compliance concerns exist
❌ **DON'T**: Proceed with non-compliant components
❌ **DON'T**: Ignore specific recommendations for compliance improvement

## Next Steps Integration

**After `/goalkit.workflow`**:

- **High Compliance (7.0+)**: Proceed to next methodology step
- **Medium Compliance (5.0-6.9)**: Address violations, then re-validate
- **Low Compliance (< 5.0)**: Major methodology revision required before proceeding
- **Compliance Improvement**: Fix violations and re-check before proceeding
