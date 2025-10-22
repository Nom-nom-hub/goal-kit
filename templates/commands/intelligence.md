---
description: Analyze workflow intelligence and generate insights for project optimization
scripts:
  sh: .goalkit/scripts/python/workflow_intelligence.py --format text
  ps: .goalkit/scripts/python/workflow_intelligence.py --format text
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

## Workflow Intelligence Command

**Purpose**: Generate intelligent analysis and insights for project optimization based on workflow patterns and project data

**When to Use**:
- To analyze project patterns and identify optimization opportunities
- After significant project milestones for insight extraction
- To predict potential challenges and opportunities
- For data-driven project optimization recommendations

## Quick Prerequisites Check

**BEFORE ANALYZING INTELLIGENCE**:
1. **Goal Kit project exists**: Verify `.goalkit/` directory structure
2. **Project has meaningful data**: Have goals, strategies, or execution activities to analyze
3. **Sufficient activity history**: Have enough project history for pattern recognition
4. **Active components**: Have goals or work in progress to analyze

**If missing**: Allow for basic analysis but note limitations.

## Quick Intelligence Analysis Steps

**STEP 1**: Scan all project components for pattern recognition

**STEP 2**: Analyze workflow patterns across:
- Goal completion velocity
- Strategy effectiveness
- Milestone achievement patterns
- Timeline adherence
- Quality metrics over time

**STEP 3**: Generate intelligence report with insights and recommendations

**STEP 4**: Identify optimization opportunities

**STEP 5**: Provide actionable intelligence for decision-making

## Intelligence Analysis Dimensions

**Performance Indicators**:
- **Velocity Trends**: Goal/milestone completion patterns over time
- **Quality Patterns**: How quality scores change with time or approach
- **Efficiency Metrics**: Time and effort required for different activities
- **Success Correlations**: Factors that correlate with successful outcomes

**Pattern Recognition**:
- **Successful Approaches**: Strategies that tend to work well
- **Risk Indicators**: Patterns that precede problems or delays
- **Optimization Opportunities**: Areas where efficiency can be improved
- **Resource Patterns**: How different resources affect outcomes

## Input Format

```
/goalkit.intelligence [options]
```

### Command Options

```
/goalkit.intelligence               # Generate comprehensive intelligence report
/goalkit.intelligence --quick       # Quick intelligence summary
/goalkit.intelligence --detailed    # Detailed analysis with deep insights
/goalkit.intelligence --json        # Output in JSON format for integration
```

## Agent Script Execution Guide

**CRITICAL**: When processing `/goalkit.intelligence` commands, agents MUST:

### **STEP 1**: Run the intelligence analysis script
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/workflow_intelligence.py --format text
```

### **STEP 2**: If detailed analysis needed
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/workflow_intelligence.py --detailed --format text
```

### **STEP 3**: Parse intelligence results
- **Extract insights** and pattern recognitions
- **Identify optimization opportunities** for project improvement
- **Note predictive indicators** for future success
- **Highlight actionable recommendations** for decision-making

### **STEP 4**: Interpret intelligence findings
- **High Confidence**: Strong patterns with statistical significance
- **Medium Confidence**: Emerging patterns requiring validation
- **Low Confidence**: Tentative patterns needing more data

### **STEP 5**: Update agent context with intelligence insights
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/update_agent_context.py
```

## Output

The command generates:
- **Intelligence Report**: Comprehensive analysis with key insights
- **Pattern Recognition**: Identification of successful and problematic patterns
- **Predictive Indicators**: Early warning signs and success factors
- **Optimization Recommendations**: Specific areas for improvement
- **Confidence Levels**: Statistical confidence in each insight

### Intelligence Analysis Process

**Multi-Dimensional Analysis**:
1. **Historical Patterns**: Analysis of completed work and outcomes
2. **Current Trends**: Ongoing patterns and emerging trends
3. **Comparative Analysis**: Different approaches and their outcomes
4. **Predictive Modeling**: Future projections based on current patterns
5. **Optimization Potential**: Areas with highest improvement potential

## Intelligence Components

### 1. Performance Intelligence
- **Velocity Analysis**: How goal completion speed changes over time
- **Quality Trends**: How work quality changes with experience or approach
- **Efficiency Patterns**: Which approaches yield best results
- **Timeline Predictions**: Expected completion times based on patterns

### 2. Pattern Recognition
- **Success Factors**: Elements that correlate with successful outcomes
- **Risk Indicators**: Early warning signs of potential problems
- **Optimization Opportunities**: Areas where efficiency can be improved
- **Approach Effectiveness**: Which strategies work best in which contexts

### 3. Predictive Intelligence
- **Completion Forecasts**: Predicted completion dates based on patterns
- **Risk Predictions**: Likelihood of future challenges based on trends
- **Success Probabilities**: Likelihood of goal achievement based on patterns
- **Optimization Impact**: Predicted benefits of different improvements

### 4. Optimization Intelligence
- **High-Impact Changes**: Smallest changes with largest improvements
- **Resource Optimization**: Best allocation of time and effort
- **Process Improvements**: Workflow modifications for better outcomes
- **Strategy Optimization**: Approach refinements based on data

## Intelligence Confidence Levels

### Confidence Assessment
- **High Confidence (80%+)**: Strong statistical evidence, reliable patterns
- **Medium Confidence (60-79%)**: Emerging patterns requiring validation
- **Low Confidence (40-59%)**: Tentative observations needing more data
- **Speculative (<40%)**: Hypotheses requiring extensive validation

### Intelligence Quality Factors
- **Data Volume**: Amount of historical data available
- **Pattern Consistency**: How consistent patterns are across time
- **Statistical Significance**: Mathematical certainty of findings
- **External Factors**: Influence of uncontrolled variables

## Integration with Other Commands

### Intelligence in Workflow
- **After Milestone Completion**: Analyze patterns in completed work
- **Before Strategy Selection**: Use insights to inform approach decisions
- **During Execution**: Apply intelligence to optimize ongoing work
- **For Quality Assessment**: Use patterns to predict quality outcomes

### Intelligence-Guided Decisions
```
/goalkit.goal → Define goal
/goalkit.intelligence → Analyze project patterns
[Apply insights to goal approach] → Continue with pattern-aware strategy
```

## Best Practices

### Intelligence Analysis
- **Sufficient Data**: Wait for adequate project history before analysis
- **Context Awareness**: Consider project-specific factors in analysis
- **Pattern Validation**: Verify patterns before making decisions
- **Confidence Awareness**: Factor confidence levels into decision-making

### Intelligence Application
- **Incremental Implementation**: Apply insights gradually, not all at once
- **Validation Testing**: Test intelligence-based changes on small scales first
- **Continuous Monitoring**: Track effectiveness of intelligence-based changes
- **Feedback Incorporation**: Update intelligence based on results

### Pattern Recognition
- **Correlation vs Causation**: Distinguish between related and causal patterns
- **External Factors**: Account for variables beyond the project
- **Situational Relevance**: Consider when patterns may not apply
- **Trend Validation**: Verify patterns are ongoing, not historical anomalies

## Common Intelligence Patterns

### Performance Patterns
- **Learning Curves**: Performance improvement over time and experience
- **Seasonal Variations**: Time-based patterns in productivity or quality
- **Team Dynamics**: How collaboration affects performance patterns
- **Resource Impact**: How different resources affect outcomes

### Risk Patterns
- **Risk Precursors**: Early indicators that predict future problems
- **Quality Degradation**: Patterns that precede quality issues
- **Timeline Slippage**: Factors that correlate with delays
- **Scope Creep Indicators**: Patterns that precede requirement changes

### Success Patterns
- **High-Impact Activities**: Work that has disproportionate positive effects
- **Efficiency Leverage**: Small changes with large improvements
- **Quality Indicators**: Early signs that predict final quality
- **Engagement Factors**: Elements that increase motivation/success

## Examples

### Example 1: Comprehensive Intelligence Analysis
```
/goalkit.intelligence
```
**Output**: Full analysis including historical patterns, predictive indicators, and optimization recommendations

### Example 2: Quick Intelligence Summary
```
/goalkit.intelligence --quick
```
**Output**: High-level insights and key optimization opportunities

### Example 3: Strategy Guidance Using Intelligence
```
/goalkit.intelligence
[Review patterns showing faster completion with iterative approaches]
/goalkit.strategies → Focus on iterative strategy approach based on intelligence
```

## Agent Integration

### Intelligence-Aware Assistance
**CRITICAL**: Agents should leverage intelligence insights for enhanced decision-making:

1. **Pattern-Based Guidance**: Use historical patterns to inform recommendations
2. **Predictive Assistance**: Apply predictive insights to future decisions
3. **Optimization Awareness**: Factor efficiency insights into approach suggestions
4. **Contextual Intelligence**: Apply project-specific patterns and insights

### Automated Intelligence Integration
- **Regular Analysis**: Periodic intelligence reports during active projects
- **Event-Triggered Analysis**: Analysis after significant milestones
- **Trend Monitoring**: Continuous tracking of pattern changes
- **Alert Generation**: Notifications when patterns suggest changes needed

## Intelligence Applications

### Process Optimization
- **Workflow Adjustment**: Modify processes based on pattern insights
- **Resource Allocation**: Distribute effort based on effectiveness patterns
- **Timeline Adjustment**: Modify expectations based on historical velocity
- **Quality Focus**: Prioritize areas that most impact success

### Strategy Development
- **Approach Selection**: Choose strategies based on success patterns
- **Risk Mitigation**: Address predictable risk patterns
- **Efficiency Enhancement**: Apply optimization insights
- **Learning Acceleration**: Use patterns to accelerate learning

## Key Benefits

- **Data-Driven Decisions**: Make choices based on actual project patterns
- **Predictive Insights**: Anticipate challenges and opportunities
- **Optimization Guidance**: Identify highest-impact improvement opportunities
- **Pattern Recognition**: Learn from past successes and failures
- **Intelligent Adaptation**: Adjust approaches based on evidence

## Critical Rules

✅ **DO**: Use intelligence insights to inform decision-making
✅ **DO**: Consider confidence levels when applying insights
✅ **DO**: Validate intelligence-based changes before full implementation
✅ **DO**: Update approaches based on pattern recognition
❌ **DON'T**: Apply intelligence insights without considering context
❌ **DON'T**: Ignore confidence levels in intelligence findings
❌ **DON'T**: Make major changes based on low-confidence patterns

## Next Steps Integration

**After `/goalkit.intelligence`**:
- **Review Key Insights**: Identify the most impactful findings
- **Validate Recommendations**: Ensure suggestions fit current context
- **Plan Implementation**: Decide which insights to apply first
- **Monitor Results**: Track effectiveness of intelligence-based changes
- **Continual Analysis**: Schedule regular intelligence updates for ongoing insights