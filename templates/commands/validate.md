---
description: Enhanced validation with quality scoring and detailed feedback for methodology components
scripts:
  sh: .goalkit/scripts/python/enhanced_validator.py --format text
  ps: .goalkit/scripts/python/enhanced_validator.py --format text
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

# Enhanced Validation Command

**Purpose**: Run comprehensive validation with quality scoring (1-10 scale) and detailed feedback

**When to Use**:

- After creating vision, goals, strategies, milestones
- Before proceeding to next methodology step
- When quality concerns arise
- To get specific improvement recommendations

## Quick Prerequisites Check

**BEFORE VALIDATING**:

1. **Goal Kit project exists**: Verify `.goalkit/` directory structure
2. **Components created**: Have vision, goals, or other methodology files to validate

**If missing**: Create components first using appropriate commands.

## Quick Validation Steps

**STEP 1**: Identify what to validate (entire project or specific component)

**STEP 2**: Run enhanced validation engine with multi-layered analysis:

- Content quality analysis
- Methodology compliance checking
- Specific feedback and recommendations

**STEP 3**: Review quality scores (1-10 scale) and detailed feedback

**STEP 4**: Address any issues found before proceeding

**STEP 5**: Report validation results and next steps

## Quality Standards

**Validation Thresholds**:

- **Vision**: 6.0+ score required for quality foundation
- **Goals**: 7.0+ score required (higher standard for goals)
- **Strategies/Milestones**: 6.0+ score required

**Quality Dimensions**:

- **Completeness**: How thorough is the content?
- **Specificity**: How specific and actionable?
- **Measurability**: How measurable are the outcomes?
- **Clarity**: How clear and well-written?
- **Structure**: How well-organized and logical?

## Input Format

```text
/goalkit.validate [optional: specific-goal-name]
```

### Example Inputs

```text
/goalkit.validate
/goalkit.validate user-authentication
/goalkit.validate 001-user-authentication
```

## Agent Script Execution Guide

**CRITICAL**: When processing `/goalkit.validate` commands, agents MUST follow this exact sequence:

### **STEP 1**: Run the validation script FIRST

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/enhanced_validator.py --format text
```

### **STEP 2**: If user specifies a goal, run targeted validation

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/enhanced_validator.py --goal "{SPECIFIC_GOAL}" --format text
```

### **STEP 3**: Parse and interpret results

- **Extract quality scores** (1-10 scale) for decision-making
- **Identify specific issues** that need to be addressed
- **Note recommendations** for quality improvement
- **Check quality thresholds** before allowing workflow progression

### **STEP 4**: Make quality-gated decisions

- **Score ≥ 7.0**: "Excellent quality - ready to proceed to next step"
- **Score 5.0-6.9**: "Good foundation - address specific issues before proceeding"
- **Score < 5.0**: "Major revision needed - work on recommendations first"

### **STEP 5**: Update progress tracking

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/progress_tracker.py --save
```

### **STEP 6**: Provide intelligent user feedback

- **Show quality scores** with clear interpretation
- **Highlight specific issues** that need attention
- **Provide actionable recommendations** for improvement
- **Set clear next steps** based on quality assessment

## Output

The command generates:

- **Quality Report**: Detailed analysis with scores and feedback
- **Specific Issues**: Clear identification of problems
- **Actionable Recommendations**: Specific steps to improve quality
- **Strengths Identification**: What components are working well

### File Analysis Process

**Multi-Layered Validation**:

1. **Structure Check**: Verify required sections exist
2. **Content Analysis**: Analyze quality and specificity
3. **Methodology Compliance**: Ensure Goal-Driven Development principles
4. **Quality Scoring**: Calculate 1-10 quality scores
5. **Feedback Generation**: Provide specific recommendations

## Validation Components

### 1. Vision Validation

- **Project Purpose**: Clear mission and outcomes
- **Success Metrics**: Specific, measurable criteria
- **Guiding Principles**: Actionable AI guidance
- **Project Goals**: High-level outcome focus
- **Project Scope**: Clear boundaries and flexibility

### 2. Goal Validation

- **Goal Statement**: Clear outcome description
- **Success Metrics**: Specific targets (%, $, timeframes)
- **Validation Strategy**: Measurement approaches
- **Risk Assessment**: Potential issues and mitigation
- **Completion Criteria**: Clear success indicators

### 3. Strategy Validation

- **Multiple Approaches**: 3+ different strategies explored
- **Comparative Analysis**: Feasibility, effort, risk assessment
- **Validation Experiments**: Testing approaches
- **Recommendation Rationale**: Evidence-based choice

### 4. Milestone Validation

- **Measurable Outcomes**: Clear success indicators
- **Progress Tracking**: Measurement approaches
- **Validation Methods**: Success confirmation
- **Learning Objectives**: Insights to be gained

## Quality Scoring System

### Score Interpretation

- **9-10**: Excellent - Exceeds quality standards
- **7-8**: Good - Meets quality standards
- **5-6**: Needs Improvement - Address key issues
- **3-4**: Major Issues - Significant rework needed
- **1-2**: Critical Issues - Complete revision required

### Scoring Weights by Component

- **Vision**: Completeness (25%), Specificity (20%), Measurability (20%), Clarity (20%), Structure (15%)
- **Goals**: Specificity (25%), Measurability (30%), Completeness (20%), Clarity (15%), Structure (10%)
- **Strategies**: Completeness (25%), Specificity (25%), Clarity (20%), Structure (15%), Measurability (15%)
- **Milestones**: Measurability (30%), Completeness (20%), Specificity (20%), Clarity (15%), Structure (15%)

## Integration with Other Commands

### Quality Gates for Workflow

- **Before `/goalkit.strategies`**: Validate goal quality (7.0+ required)
- **Before `/goalkit.milestones`**: Validate strategies (6.0+ required)
- **Before `/goalkit.execute`**: Validate milestones (6.0+ required)

### Validation in Workflow

```text
/goalkit.vision → Create vision
/goalkit.validate → Check vision quality (6.0+)
/goalkit.goal → Create goal
/goalkit.validate → Check goal quality (7.0+)
/goalkit.strategies → Explore strategies
/goalkit.validate → Check strategies quality (6.0+)
```

## Best Practices

### Regular Validation

- **After Each Component**: Validate quality before proceeding
- **Before Major Changes**: Validate current state
- **Quality Monitoring**: Track quality trends over time

### Addressing Validation Issues

- **Low Completeness**: Add missing sections and details
- **Low Specificity**: Add concrete examples and measurable targets
- **Low Measurability**: Define specific success criteria and measurement approaches
- **Low Clarity**: Improve structure and eliminate ambiguity

### Quality Improvement Process

1. **Run Validation**: Identify specific issues
2. **Review Feedback**: Understand quality problems
3. **Implement Fixes**: Address identified issues
4. **Re-validate**: Confirm quality improvement
5. **Document Learnings**: Capture improvement insights

## Common Validation Patterns

### Vision Quality Issues

- **Missing Metrics**: Add specific success criteria
- **Vague Principles**: Make principles more actionable
- **Unclear Purpose**: Better define project mission
- **Scope Issues**: Clarify boundaries and flexibility

### Goal Quality Issues

- **Implementation Details**: Remove technology references
- **Vague Metrics**: Add specific targets and timeframes
- **Missing Validation**: Define measurement approaches
- **Risk Assessment**: Add potential issues and mitigation

### Strategy Quality Issues

- **Single Approach**: Explore additional strategies
- **Missing Analysis**: Add feasibility and risk assessment
- **No Validation**: Define testing approaches
- **Weak Rationale**: Strengthen recommendation reasoning

## Examples

### Example 1: Project-Level Validation

```text
/goalkit.validate
```

**Output**: Validates entire project, shows overall quality scores and recommendations

### Example 2: Goal-Specific Validation

```text
/goalkit.validate user-engagement
```

**Output**: Detailed analysis of specific goal with quality scoring and improvement suggestions

### Example 3: Quality Gate Usage

```text
/goalkit.goal Create user engagement goal with 40% improvement target
/goalkit.validate
[If score >= 7.0] → /goalkit.strategies
[If score < 7.0] → Address issues first
```

## Agent Integration

### Quality-First Workflow

**CRITICAL**: Agents should enforce quality standards:

1. **Pre-validation**: Run validation before allowing workflow progression
2. **Quality Gates**: Block progression if quality thresholds not met
3. **Improvement Guidance**: Provide specific steps to address issues
4. **Success Confirmation**: Verify quality improvements after fixes

### Validation Automation

- **Auto-validation**: Run after each methodology component creation
- **Quality Reporting**: Include validation results in progress updates
- **Trend Tracking**: Monitor quality improvements over time

## Key Benefits

- **Quality Assurance**: Ensures methodology components meet standards
- **Early Issue Detection**: Identifies problems before they impact execution
- **Continuous Improvement**: Provides specific guidance for enhancement
- **Consistency**: Maintains quality across all project components
- **Risk Reduction**: Prevents poor-quality components from proceeding

## Critical Rules

✅ **DO**: Run validation after creating major components
✅ **DO**: Address quality issues before proceeding to next steps
✅ **DO**: Use validation feedback for continuous improvement
✅ **DO**: Maintain quality standards throughout project lifecycle
❌ **DON'T**: Skip validation when quality concerns exist
❌ **DON'T**: Proceed with low-quality components
❌ **DON'T**: Ignore specific recommendations for improvement

## Next Steps Integration

**After `/goalkit.validate`**:

- **High Scores (7.0+)**: Proceed to next methodology step
- **Medium Scores (5.0-6.9)**: Address specific issues, then re-validate
- **Low Scores (< 5.0)**: Major revision required before proceeding

**Quality Improvement Workflow**:

1. Run validation → 2. Review feedback → 3. Address issues → 4. Re-validate → 5. Proceed when quality met
