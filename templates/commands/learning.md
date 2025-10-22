---
description: Enable and manage learning systems for continuous improvement and knowledge capture
scripts:
  sh: .goalkit/scripts/python/learning_system.py --format text
  ps: .goalkit/scripts/python/learning_system.py --format text
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

## Learning System Command

**Purpose**: Capture, organize, and apply learning insights to continuously improve project methodology and outcomes

**When to Use**:
- To capture insights and learnings during project execution
- After completing milestones to extract lessons learned
- Before making methodology improvements based on evidence
- To establish learning loops for adaptive development

## Quick Prerequisites Check

**BEFORE INITIALIZING LEARNING SYSTEM**:
1. **Goal Kit project exists**: Verify `.goalkit/` directory structure
2. **Active project work**: Have ongoing work from which to extract learning
3. **Learning opportunities**: Have completed activities or milestones to analyze
4. **Improvement goals**: Have areas where learning could drive improvements

**If missing**: Learning system can still establish capture mechanisms for future insights.

## Quick Learning Setup Steps

**STEP 1**: Analyze project activities for learning opportunities

**STEP 2**: Set up learning capture mechanisms for ongoing work

**STEP 3**: Identify patterns and insights from completed activities

**STEP 4**: Organize learnings into actionable improvements

**STEP 5**: Apply insights to optimize current and future work

**STEP 6**: Monitor effectiveness of learning-based changes

## Learning System Features

**Knowledge Capture**:
- **Insight Extraction**: Systematic capture of lessons learned
- **Pattern Recognition**: Identification of success/failure patterns
- **Knowledge Organization**: Structured storage of insights
- **Learning Documentation**: Formal documentation of key learnings

**Continuous Improvement**:
- **Hypothesis Testing**: Apply learnings as improvements to test
- **Methodology Refinement**: Adjust methodology based on evidence
- **Performance Optimization**: Use insights for better outcomes
- **Adaptive Adjustments**: Continuous refinement based on results

## Input Format

```
/goalkit.learning [options]
```

### Command Options

```
/goalkit.learning                 # Initialize learning system and capture insights
/goalkit.learning --capture       # Capture specific learning from recent activities
/goalkit.learning --analyze       # Analyze accumulated learning for insights
/goalkit.learning --apply         # Apply learning insights to current methodology
/goalkit.learning --report        # Generate learning summary and insights report
/goalkit.learning --json          # Output in JSON format for integration
```

## Agent Script Execution Guide

**CRITICAL**: When processing `/goalkit.learning` commands, agents MUST:

### **STEP 1**: Run the learning system script
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/learning_system.py --format text
```

### **STEP 2**: If capturing specific learning
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/learning_system.py --capture --format text
```

### **STEP 3**: Parse learning results
- **Extract insights** and patterns from project activities
- **Identify improvement opportunities** based on evidence
- **Note successful patterns** to replicate in future work
- **Document lessons learned** and recommendations

### **STEP 4**: Assess learning quality
- **Evidence Strength**: Evaluate strength of learning evidence
- **Applicability**: Determine relevance to current/future work
- **Impact Potential**: Assess improvement potential of insights
- **Implementation Feasibility**: Consider practicality of applying insights

### **STEP 5**: Update agent context with learning insights
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/update_agent_context.py
```

## Output

The command generates:
- **Learning Report**: Comprehensive summary of captured insights
- **Pattern Recognition**: Identified success and failure patterns
- **Improvement Recommendations**: Specific suggestions for methodology optimization
- **Knowledge Database**: Structured knowledge of project learnings
- **Action Items**: Concrete steps to apply learning insights

### Learning Process

**Systematic Learning**:
1. **Experience Capture**: Collect data from completed activities
2. **Pattern Analysis**: Identify patterns in successes and failures
3. **Insight Extraction**: Extract actionable insights from patterns
4. **Knowledge Organization**: Structure learnings for future application
5. **Improvement Application**: Apply insights to optimize methodology

## Learning Components

### 1. Experience Capture
- **Activity Documentation**: Record completed activities and outcomes
- **Result Tracking**: Monitor success/failure of different approaches
- **Context Recording**: Capture conditions and circumstances of outcomes
- **Stakeholder Feedback**: Collect feedback from involved parties

### 2. Pattern Recognition
- **Success Factors**: Identify elements that correlate with success
- **Failure Indicators**: Recognize patterns that precede problems
- **Efficiency Patterns**: Identify approaches that yield best results
- **Quality Correlations**: Understand factors that affect quality

### 3. Insight Extraction
- **Root Cause Analysis**: Understand why approaches succeeded or failed
- **Causal Relationships**: Identify cause-effect relationships in outcomes
- **Context Sensitivity**: Understand when insights apply specifically
- **Generalization Potential**: Determine broader applicability of insights

### 4. Knowledge Application
- **Methodology Improvement**: Adjust methodology based on insights
- **Approach Optimization**: Refine approaches based on evidence
- **Risk Management**: Apply learning to prevent similar issues
- **Success Replication**: Replicate successful approaches in similar contexts

## Learning Quality Standards

### Insight Validity
- **Evidence-Based**: Insights grounded in concrete project evidence
- **Context Awareness**: Recognition of when insights apply
- **Statistical Significance**: Adequate data to support conclusions
- **Practical Relevance**: Focus on actionable, relevant insights

### Knowledge Management
- **Organization**: Learnings structured for easy retrieval and application
- **Accessibility**: Easy access to relevant insights for decision-making
- **Currency**: Up-to-date information reflecting current understanding
- **Completeness**: Comprehensive coverage of relevant learning areas

## Integration with Other Commands

### Learning in Workflow
- **During `/goalkit.execute`**: Capture learning from implementation
- **After milestone completion**: Extract lessons from completed work
- **Before strategy selection**: Apply learning to approach decisions
- **During methodology optimization**: Use learning to refine processes

### Learning-Driven Improvements
```
/goalkit.goal → Define goal
/goalkit.learning --capture → Capture insights from goal definition
[Apply learning to improve goal-setting process] → /goalkit.strategies
/goalkit.learning --analyze → Analyze strategy effectiveness
[Refine approach based on learning] → Continue with optimized strategy
```

## Best Practices

### Learning Capture
- **Timely Documentation**: Capture insights while they're fresh
- **Specific Details**: Include specific context and conditions
- **Objective Analysis**: Separate objective evidence from subjective opinion
- **Actionable Focus**: Prioritize insights that can drive improvements

### Learning Application
- **Systematic Application**: Apply relevant learnings to current work
- **Gradual Implementation**: Introduce changes gradually to monitor effectiveness
- **Continuous Monitoring**: Track impact of learning-based changes
- **Feedback Integration**: Gather feedback on applied learning

### Knowledge Management
- **Structured Organization**: Organize learnings for easy retrieval
- **Clear Documentation**: Document insights clearly and comprehensively
- **Regular Review**: Periodically review and update learning database
- **Context Tagging**: Tag learnings with relevant context for retrieval

## Common Learning Scenarios

### Project Execution Learning
- **Implementation Insights**: What worked and didn't work during execution
- **Approach Effectiveness**: Which strategies proved most effective
- **Problem Resolution**: Effective approaches to challenge resolution
- **Quality Improvement**: Learning that improves quality outcomes

### Methodology Learning
- **Process Optimization**: How to improve workflow and methodology
- **Quality Assurance**: Better approaches to quality validation
- **Communication**: Improved communication and coordination methods
- **Risk Management**: Enhanced risk identification and mitigation

### Success Pattern Learning
- **Efficiency Patterns**: Approaches that yielded best efficiency
- **Quality Patterns**: Methods that produced highest quality results
- **Collaboration Patterns**: Best approaches to multi-agent work
- **Stakeholder Patterns**: Effective ways to engage stakeholders

## Examples

### Example 1: Initialize Learning System
```
/goalkit.learning
```
**Output**: Sets up learning capture mechanisms and analyzes available insights

### Example 2: Capture Specific Learning
```
/goalkit.learning --capture
```
**Output**: Captures insights from recent project activities

### Example 3: Analyze Accumulated Learning
```
/goalkit.learning --analyze
```
**Output**: Deep analysis of collected learning for pattern identification

### Example 4: Apply Learning to Improve Process
```
/goalkit.goal Create user interface for productivity app
/goalkit.learning --capture → Capture insights from UI design
[Learning shows iterative design approach worked best] → /goalkit.strategies
/goalkit.strategies → Focus on iterative UI design based on learning
/goalkit.learning --apply → Apply learning insights to current strategy
```

## Agent Integration

### Learning-Aware Decision Making
**CRITICAL**: Agents should leverage learning insights for evidence-based decisions:

1. **Pattern Application**: Apply successful patterns from past experience
2. **Risk Avoidance**: Avoid approaches that proved problematic before
3. **Efficiency Optimization**: Use learning to optimize approaches
4. **Quality Enhancement**: Apply learning to improve quality outcomes

### Automated Learning Integration
- **Continuous Capture**: Automatically capture insights during work
- **Pattern Recognition**: Identify patterns across project activities
- **Knowledge Organization**: Structure learning for easy retrieval
- **Application Suggestion**: Recommend learning-based improvements

## Learning Applications

### Process Improvement
- **Workflow Optimization**: Apply learning to streamline processes
- **Quality Enhancement**: Use learning to improve quality methods
- **Risk Mitigation**: Apply learning to prevent similar issues
- **Efficiency Gains**: Use learning to identify optimization opportunities

### Approach Refinement
- **Strategy Selection**: Apply learning to choose better approaches
- **Methodology Adjustment**: Refine methodology based on evidence
- **Technology Choice**: Use learning to inform technical decisions
- **Communication**: Apply learning to improve collaboration

## Key Benefits

- **Continuous Improvement**: Ongoing optimization based on evidence
- **Mistake Prevention**: Avoid repeating past mistakes
- **Success Replication**: Repeat successful approaches
- **Adaptive Methodology**: Adjust methodology based on learning
- **Knowledge Accumulation**: Build organizational learning over time

## Critical Rules

✅ **DO**: Capture insights systematically during project execution
✅ **DO**: Apply learning insights to improve current and future work
✅ **DO**: Document learning clearly for future reference
✅ **DO**: Monitor effectiveness of learning-based changes
❌ **DON'T**: Ignore opportunities to capture valuable learning
❌ **DON'T**: Apply learning beyond its relevant context
❌ **DON'T**: Forget to document important lessons learned

## Next Steps Integration

**After `/goalkit.learning`**:
- **Review Insights**: Examine captured insights and patterns
- **Identify Applications**: Determine where to apply learning
- **Plan Implementation**: Decide which learning-based changes to apply first
- **Monitor Impact**: Track effectiveness of learning-based improvements
- **Continuous Learning**: Maintain learning capture for ongoing improvement