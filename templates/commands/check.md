---
description: Validate methodology compliance and check project adherence to goal-driven development principles
scripts:
  sh: .goalkit/scripts/python/validate_methodology.py --format text
  ps: .goalkit/scripts/python/validate_methodology.py --format text
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

# Methodology Check Command

**Purpose**: Validate project adherence to goal-driven development principles, check methodology compliance, and identify areas requiring improvement

**When to Use**:

- To verify methodology compliance after creating components
- Before proceeding to next workflow steps
- When methodology deviations are suspected
- For regular compliance and quality checks

## Quick Prerequisites Check

**BEFORE RUNNING METHODOLOGY CHECK**:

1. **Goal Kit project exists**: Verify `.goalkit/` directory structure
2. **Project components created**: Have vision, goals, or other methodology files
3. **Methodology steps followed**: Ensure proper sequence was maintained
4. **Quality concerns exist**: Have specific concerns about methodology adherence

**If missing**: Can still run basic validation but results may be limited.

## Quick Check Steps

**STEP 1**: Analyze project structure for methodology compliance

**STEP 2**: Validate components against goal-driven development standards

**STEP 3**: Identify methodology violations or deviations

**STEP 4**: Generate compliance report with violations and recommendations

**STEP 5**: Assess overall methodology health and adherence

**STEP 6**: Provide actionable recommendations for improvement

## Check Features

**Validation Capabilities**:

- **Compliance Verification**: Check adherence to goal-driven methodology
- **Quality Assessment**: Evaluate component quality against standards
- **Sequence Validation**: Verify proper workflow sequence
- **Content Analysis**: Validate focus on outcomes vs implementation

**Compliance Management**:

- **Violation Detection**: Identify specific methodology deviations
- **Severity Assessment**: Rate violations by impact and importance
- **Recommendation Generation**: Provide specific improvement suggestions
- **Compliance Reporting**: Document overall methodology health

## Input Format

```bash
/goalkit.check [options]
```

### Command Options

```bash
/goalkit.check                    # Run comprehensive methodology compliance check
/goalkit.check --quick            # Fast compliance verification
/goalkit.check --detailed         # Detailed analysis with deep validation
/goalkit.check --focus "area"     # Focus validation on specific methodology area
/goalkit.check --json             # Output in JSON format for integration
```

## Agent Script Execution Guide

**CRITICAL**: When processing `/goalkit.check` commands, agents MUST:

### **STEP 1**: Run the methodology validation script

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/validate_methodology.py --format text
```

### **STEP 2**: If detailed analysis requested

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/validate_methodology.py --detailed --format text
```

### **STEP 3**: Parse validation results

- **Extract compliance status** and adherence metrics
- **Identify specific violations** that need to be addressed
- **Note recommendations** for methodology improvement
- **Check compliance thresholds** before allowing workflow progression

### **STEP 4**: Assess validation quality

- **Severity Classification**: Rate violations by impact and importance
- **Compliance Thresholds**: Determine if project meets methodology standards
- **Action Prioritization**: Identify most critical issues to address
- **Quality Standards**: Verify components meet required quality levels

### **STEP 5**: Update agent context with validation results

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/update_agent_context.py
```

## Output

The command generates:

- **Compliance Report**: Detailed analysis of methodology adherence
- **Violation Identification**: Clear identification of methodology issues
- **Quality Assessment**: Evaluation of component quality against standards
- **Actionable Recommendations**: Specific steps to address compliance issues
- **Compliance Score**: Overall adherence measurement (1-10 scale)

### Validation Process

**Systematic Methodology Assessment**:

1. **Structure Verification**: Ensure proper directory and file structure
2. **Content Analysis**: Validate content aligns with goal-driven principles
3. **Sequence Compliance**: Verify proper workflow order was followed
4. **Quality Validation**: Assess components against required standards
5. **Integration Check**: Confirm components connect properly

## Check Components

### 1. Structure Validation

- **Directory Organization**: Verify proper folder structure
- **File Presence**: Confirm required files exist and are properly named
- **Template Compliance**: Check files follow proper template structure
- **Integration Points**: Validate proper connections between components

### 2. Content Quality

- **Outcome Focus**: Verify content focuses on outcomes, not implementation
- **Measurability**: Confirm success criteria are specific and measurable
- **Completeness**: Ensure all required sections are properly filled
- **Clarity**: Validate content is clear and unambiguous

### 3. Methodology Compliance

- **Workflow Sequence**: Verify proper vision → goal → strategies → milestones → execute flow
- **Quality Thresholds**: Confirm components meet required quality standards
- **Methodology Principles**: Ensure adherence to goal-driven development principles
- **Validation Requirements**: Verify proper validation was performed

### 4. Integration Validation

- **Component Connections**: Ensure components properly integrate
- **Reference Accuracy**: Verify cross-references between components are correct
- **Consistency**: Confirm consistent information across components
- **Dependency Validation**: Check proper inter-component dependencies

## Validation Quality Standards

### Compliance Scoring

- **Excellent (9-10)**: Full adherence to methodology with minor imperfections
- **Good (7-8)**: Strong adherence with few areas for improvement
- **Acceptable (5-6)**: Adequate compliance with some issues to address
- **Concerning (3-4)**: Significant methodology violations requiring attention
- **Poor (1-2)**: Major non-compliance requiring immediate action

### Quality Thresholds

- **Vision**: Meets foundational requirements (6.0+ for compliance)
- **Goals**: High quality required (7.0+ for compliance)
- **Strategies**: Adequate quality (6.0+ for compliance)
- **Milestones**: Adequate quality (6.0+ for compliance)

## Integration with Other Commands

### Check in Workflow

- **After `/goalkit.vision`**: Verify vision compliance (6.0+ required)
- **After `/goalkit.goal`**: Verify goal compliance (7.0+ required)  
- **After `/goalkit.strategies`**: Verify strategy compliance (6.0+ required)
- **After `/goalkit.milestones`**: Verify milestone compliance (6.0+ required)
- **Before `/goalkit.execute`**: Final compliance check required

### Compliance-Gated Workflow

```bash
/goalkit.vision → Create vision
/goalkit.check → Verify compliance (6.0+)
/goalkit.goal → Create goal
/goalkit.check → Verify compliance (7.0+)
/goalkit.strategies → Explore strategies
/goalkit.check → Verify compliance (6.0+)
```

## Best Practices

### Regular Validation

- **After Each Component**: Validate compliance before proceeding
- **Before Major Changes**: Verify current state before modifications
- **Weekly Reviews**: Check overall methodology adherence
- **Before Execution**: Final compliance verification required

### Issue Resolution

- **Severity-Based**: Address critical violations before lesser issues
- **Systematic Fix**: Address root causes rather than symptoms
- **Quality Focus**: Prioritize issues that affect overall quality
- **Methodology Priority**: Focus on violations that compromise approach

### Validation Quality

- **Comprehensive Assessment**: Check all aspects of methodology compliance
- **Context Awareness**: Consider project-specific factors
- **Constructive Feedback**: Provide helpful, actionable recommendations
- **Continuous Improvement**: Use validation to drive ongoing improvements

## Common Compliance Issues

### Structure Problems

- **Missing Directories**: Required folder structure not properly created
- **File Organization**: Files not in expected locations
- **Template Deviations**: Files don't follow required structure
- **Integration Gaps**: Components not properly connected

### Content Issues

- **Implementation Focus**: Content focuses on how instead of what/outcomes
- **Vague Metrics**: Success criteria not specific or measurable
- **Incomplete Sections**: Required information missing
- **Clarity Problems**: Content unclear or ambiguous

### Methodology Violations

- **Sequence Deviations**: Workflow not followed in proper order
- **Quality Deficiencies**: Components don't meet required standards
- **Principle Violations**: Approaches contradict goal-driven principles
- **Validation Gaps**: Proper validation not performed

## Examples

### Example 1: Comprehensive Methodology Check

```text
/goalkit.check
```

**Output**: Complete analysis of methodology compliance across all components

### Example 2: Quick Compliance Verification

```text
/goalkit.check --quick
```

**Output**: Fast validation with pass/fail compliance status

### Example 3: Detailed Analysis

```text
/goalkit.check --detailed
```

**Output**: In-depth analysis with specific recommendations

### Example 4: Integration with Validation Workflow

```text
/goalkit.goal Create user engagement feature
/goalkit.check
[If compliant: 7.0+] → /goalkit.strategies
[If violations exist] → Address issues before proceeding
/goalkit.check --detailed → Deep analysis of strategy components
[Validate detailed strategies before milestones] → /goalkit.milestones
```

## Agent Integration

### Compliance-Aware Workflow

**CRITICAL**: Agents should enforce methodology compliance:

1. **Pre-validation**: Run checks before allowing workflow progression
2. **Compliance Gates**: Block advancement if standards not met
3. **Guidance Provision**: Provide specific steps to address violations
4. **Success Confirmation**: Verify improvements after fixes

### Automated Validation Integration

- **Auto-validation**: Run checks after methodology component creation
- **Compliance Reporting**: Include results in progress updates
- **Trend Tracking**: Monitor improvements in compliance over time
- **Alert Generation**: Notify when compliance drops below thresholds

## Validation Applications

### Quality Assurance

- **Methodology Adherence**: Ensure goal-driven development principles
- **Component Quality**: Maintain required quality standards
- **Process Compliance**: Verify proper workflow sequence
- **Outcome Focus**: Maintain focus on results vs implementation

### Risk Management

- **Deviation Detection**: Identify when methodology is not followed
- **Quality Control**: Prevent low-quality components from progressing
- **Integration Validation**: Ensure components work together properly
- **Standards Maintenance**: Maintain consistent quality across project

## Key Benefits

- **Methodology Assurance**: Ensures goal-driven development principles are followed
- **Quality Maintenance**: Maintains required component quality standards
- **Early Issue Detection**: Identifies problems before they impact execution
- **Consistency**: Keeps project aligned with goal-driven approach
- **Risk Reduction**: Prevents methodology issues from impacting success

## Critical Rules

✅ **DO**: Run compliance checks after creating major components
✅ **DO**: Address violations before proceeding to next steps
✅ **DO**: Use validation feedback for methodology improvement
✅ **DO**: Maintain standards throughout project lifecycle
❌ **DON'T**: Skip validation when compliance concerns exist
❌ **DON'T**: Proceed with non-compliant components
❌ **DON'T**: Ignore specific recommendations for improvement

## Next Steps Integration

**After `/goalkit.check`**:

- **High Compliance (7.0+)**: Proceed to next methodology step
- **Medium Compliance (5.0-6.9)**: Address violations, then re-validate
- **Low Compliance (< 5.0)**: Major revision required before proceeding
- **Compliance Improvement**: Fix issues and re-check before proceeding
