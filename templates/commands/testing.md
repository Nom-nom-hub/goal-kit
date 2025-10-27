---
description: Run optimization tests and validation to improve project methodology
scripts:
  sh: .goalkit/scripts/python/optimization_tester.py --format text
  ps: .goalkit/scripts/python/optimization_tester.py --format text
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

# Optimization Testing Command

**Purpose**: Run systematic tests to validate and optimize project methodology, approaches, and implementation strategies

**When to Use**:

- To validate the effectiveness of different implementation approaches
- Before committing to a specific strategy to test its viability
- To optimize methodology components for better outcomes
- When comparing multiple approaches for the same goal

## Quick Prerequisites Check

**BEFORE RUNNING OPTIMIZATION TESTS**:

1. **Goal Kit project exists**: Verify `.goalkit/` directory structure
2. **Clear objective**: Have specific optimization goal or hypothesis to test
3. **Testable components**: Have defined strategies or approaches to compare
4. **Success metrics**: Have measurable criteria for test success

**If missing**: Define clear objectives before testing.

## Quick Testing Steps

**STEP 1**: Define optimization hypotheses to test

**STEP 2**: Set up test conditions with measurable success criteria

**STEP 3**: Execute tests using different approaches or parameters

**STEP 4**: Measure and compare results against success criteria

**STEP 5**: Analyze results and identify optimization opportunities

**STEP 6**: Document findings and recommendations for implementation

## Testing Methodology

**Test Design Principles**:

- **Controlled Variables**: Isolate factors being tested
- **Measurable Outcomes**: Use specific, quantifiable metrics
- **Reproducible Conditions**: Ensure tests can be repeated
- **Statistical Significance**: Plan for adequate sample sizes

**Optimization Dimensions**:

- **Efficiency**: Time and resource utilization comparison
- **Effectiveness**: Quality and success rate comparison
- **Reliability**: Consistency across different conditions
- **Scalability**: Performance with increasing demands

## Input Format

```text
/goalkit.testing [options]
```

### Command Options

```text
/goalkit.testing                    # Run default optimization tests
/goalkit.testing --quick            # Run fast validation tests
/goalkit.testing --comprehensive    # Run full optimization battery
/goalkit.testing --compare "strategy1" "strategy2"  # Compare specific approaches
```

## Agent Script Execution Guide

**CRITICAL**: When processing `/goalkit.testing` commands, agents MUST:

### **STEP 1**: Run the optimization testing script

```python
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/optimization_tester.py --format text
```

### **STEP 2**: If strategy comparison requested

```python
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/optimization_tester.py --compare "STRATEGY1" "STRATEGY2" --format text
```

### **STEP 3**: Parse optimization results

- **Extract test outcomes** and success metrics
- **Identify winning approaches** across different dimensions
- **Note performance differences** between tested approaches
- **Document optimization recommendations** for implementation

### **STEP 4**: Assess test validity

- **Sample Adequacy**: Ensure sufficient test samples for confidence
- **Bias Checking**: Identify potential sources of test bias
- **External Factors**: Account for variables beyond test control
- **Reproducibility**: Verify test results can be reproduced

### **STEP 5**: Update agent context with optimization insights

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/update_agent_context.py
```

## Output

The command generates:

- **Test Results**: Detailed comparison of tested approaches
- **Optimization Rankings**: Performance ranking of different methods
- **Confidence Intervals**: Statistical confidence in test outcomes
- **Recommendations**: Specific optimization suggestions for implementation
- **Efficiency Metrics**: Quantified improvement opportunities

### Testing Process

**Systematic Optimization**:

1. **Hypothesis Formulation**: Define what to test and expected outcomes
2. **Test Design**: Create controlled conditions for fair comparison
3. **Execution**: Run tests systematically across approaches
4. **Measurement**: Collect quantified performance data
5. **Analysis**: Compare results and identify optimizations

## Testing Components

### 1. Strategy Testing

- **Approach Comparison**: Test multiple strategies for same goal
- **Performance Metrics**: Compare efficiency, effectiveness, and reliability
- **Risk Assessment**: Evaluate risk profiles of different approaches
- **Scalability Testing**: Test how approaches perform under load

### 2. Methodology Optimization

- **Process Testing**: Validate different workflow approaches
- **Quality Validation**: Test different quality assurance methods
- **Efficiency Testing**: Measure different optimization strategies
- **Integration Testing**: Validate methodology component interactions

### 3. Implementation Testing

- **Technology Comparison**: Test different implementation technologies
- **Architecture Testing**: Validate different system architectures
- **Performance Validation**: Test different performance optimization approaches
- **Quality Assurance**: Validate different testing strategies

### 4. Resource Optimization

- **Time Allocation**: Test different time management approaches
- **Effort Distribution**: Compare different effort allocation strategies
- **Resource Utilization**: Test different resource optimization methods
- **Cost Optimization**: Validate cost-effective approaches

## Test Quality Standards

### Statistical Significance

- **Sample Size**: Ensure adequate samples for confidence
- **P-Value**: Statistical significance threshold (typically p<0.05)
- **Effect Size**: Practical significance of differences
- **Confidence Intervals**: Range of likely true values

### Test Validity

- **Internal Validity**: Confidence in causal relationships
- **External Validity**: Generalizability of results
- **Construct Validity**: Accuracy of measured concepts
- **Statistical Conclusion Validity**: Appropriateness of statistical tests

## Integration with Other Commands

### Testing in Workflow

- **Before `/goalkit.strategies`**: Test initial approach viability
- **During strategy selection**: Compare different strategy options
- **After milestone planning**: Test milestone achievement approaches
- **Before execution**: Validate implementation approaches

### Optimization-Driven Decisions

```text
/goalkit.goal → Define goal with success criteria
/goalkit.testing → Test different approach options
[Select optimal approach based on test results] → /goalkit.strategies
```

## Best Practices

### Test Design

- **Clear Hypotheses**: Define specific, testable predictions
- **Control Groups**: Maintain baseline for comparison
- **Randomization**: Minimize bias in test execution
- **Blinding**: Prevent expectation bias when possible

### Test Execution

- **Systematic Approach**: Follow consistent procedures across tests
- **Detailed Documentation**: Record all test conditions and parameters
- **Reproducible Results**: Ensure others can reproduce tests
- **Statistical Rigor**: Apply appropriate statistical methods

### Result Interpretation

- **Effect Over Significance**: Prioritize practical over statistical significance
- **Confidence Assessment**: Consider confidence intervals and sample sizes
- **External Factors**: Account for variables beyond test control
- **Replication**: Verify important findings with additional tests

## Common Testing Scenarios

### Approach Comparison

- **Technology Stack**: Compare different technology combinations
- **Implementation Method**: Test iterative vs waterfall methods
- **Resource Allocation**: Test different team organization approaches
- **Quality Methods**: Compare different testing and validation approaches

### Performance Optimization

- **Speed vs Quality**: Test trade-offs between speed and quality
- **Resource Efficiency**: Compare different resource utilization strategies
- **Scalability Testing**: Validate performance under different loads
- **Cost Optimization**: Compare different budget allocation strategies

### Process Validation

- **Workflow Comparison**: Test different workflow methodologies
- **Collaboration Models**: Compare different team collaboration approaches
- **Review Processes**: Test different quality review approaches
- **Communication Protocols**: Validate different communication strategies

## Examples

### Example 1: Default Optimization Testing

```text
/goalkit.testing
```

**Output**: Standard optimization tests for common project dimensions

### Example 2: Strategy Comparison

```text
/goalkit.testing --compare "agile-iterative" "structured-waterfall"
```

**Output**: Detailed comparison of two different project approaches

### Example 3: Comprehensive Testing

```text
/goalkit.testing --comprehensive
```

**Output**: Full battery of optimization tests across all dimensions

### Example 4: Goal-Specific Testing

```text
/goalkit.goal Create recommendation system for user engagement
/goalkit.testing --compare "machine-learning" "rule-based" "hybrid-approach"
[Review test results showing ML approach most efficient]
/goalkit.strategies → Focus on machine learning strategy based on test results
```

## Agent Integration

### Testing-Aware Decision Making

**CRITICAL**: Agents should use test results for evidence-based decisions:

1. **Evidence-Based Selection**: Choose approaches based on test results
2. **Statistical Awareness**: Consider confidence levels and sample sizes
3. **Practical Application**: Factor test results into implementation decisions
4. **Continuous Validation**: Test assumptions and approach effectiveness

### Automated Testing Integration

- **Pre-Strategy Testing**: Run tests before strategy selection
- **A/B Testing**: Compare multiple approaches systematically
- **Performance Monitoring**: Track optimization results over time
- **Learning Integration**: Use test results to improve future decisions

## Testing Applications

### Strategic Testing

- **Methodology Validation**: Test different goal-driven approaches
- **Technology Assessment**: Compare technical approaches for goals
- **Process Optimization**: Validate workflow improvements
- **Quality Assurance**: Test different validation methods

### Implementation Testing

- **Architecture Comparison**: Test different system designs
- **Performance Validation**: Compare different implementation strategies
- **User Experience**: Test different UX approaches
- **Resource Allocation**: Validate different effort distribution methods

## Key Benefits

- **Evidence-Based Decisions**: Make choices based on systematic testing
- **Risk Reduction**: Identify problems before full implementation
- **Optimization**: Identify highest-impact improvement opportunities
- **Validation**: Confirm approach effectiveness before commitment
- **Learning Acceleration**: Learn from systematic comparison

## Critical Rules

✅ **DO**: Run tests before committing to major approach decisions
✅ **DO**: Consider statistical significance and confidence levels
✅ **DO**: Document test procedures for reproducibility
✅ **DO**: Use test results to inform strategy decisions
❌ **DON'T**: Make major approach decisions without testing
❌ **DON'T**: Ignore statistical limitations of tests
❌ **DON'T**: Apply test results beyond their tested context

## Next Steps Integration

**After `/goalkit.testing`**:

- **Analyze Results**: Review test outcomes and confidence levels
- **Select Optimal Approach**: Choose best-performing approach based on tests
- **Plan Implementation**: Apply winning approach to project work
- **Monitor Performance**: Track real-world performance against test predictions
- **Continuous Testing**: Schedule additional tests as needed for ongoing optimization
