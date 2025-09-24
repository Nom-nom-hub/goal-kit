# /analyze Command
*Validate project alignment and surface inconsistencies*

## Overview
The `/analyze` command examines your project structure to validate that all components align with goals, strategies, and plans. It identifies inconsistencies, gaps, and areas for improvement.

## When to Use
- When you want to check project health and alignment
- After making significant changes to goals, strategies, or plans
- Before major implementation phases
- When preparing for reviews or audits
- To identify technical debt or inconsistencies

## Usage
```
/analyze [PROJECT_PATH] [SCOPE]
```

**Options:**
- `--include-goals`: Analyze goal alignment (default: true)
- `--include-technical`: Analyze technical consistency (default: true)
- `--include-structure`: Analyze project structure (default: true)
- `--output`: Specify output file path

**Examples:**
```
/analyze
```

```
/analyze --include-goals --include-technical
```

```
/analyze /path/to/project --output analysis-report.md
```

## What It Does
1. **Analyzes project structure** for completeness and organization
2. **Validates goal alignment** across all project components
3. **Checks technical consistency** in architecture and implementation
4. **Identifies gaps** between plans and current state
5. **Surfaces inconsistencies** in naming, structure, or approach
6. **Assesses project health** and identifies improvement areas
7. **Generates analysis report** in `analysis/[PROJECT_NAME]_analysis.md`

## Analysis Scope
The analysis covers three main areas:

### 1. Goal Alignment Analysis
- **Goal completeness**: Are goals defined and documented?
- **Strategy alignment**: Do strategies support stated goals?
- **Plan consistency**: Do implementation plans align with strategies?
- **Task relevance**: Are tasks supporting the defined plans?
- **Progress tracking**: Is implementation aligned with goals?

### 2. Technical Consistency Analysis
- **Architecture coherence**: Consistent patterns and approaches
- **Technology stack alignment**: Appropriate tech choices for goals
- **Code organization**: Logical structure and naming conventions
- **Dependency management**: Proper handling of external dependencies
- **Configuration consistency**: Unified approach to configuration

### 3. Project Structure Analysis
- **Documentation completeness**: Required docs present and current
- **Testing coverage**: Adequate test structure and coverage
- **Security considerations**: Security practices implemented
- **Performance optimization**: Performance considerations addressed
- **Deployment readiness**: Production deployment considerations

## Analysis Process
1. **Project Scanning**: Examine project structure and files
2. **Component Analysis**: Review goals, strategies, plans, and tasks
3. **Cross-Reference Validation**: Check alignment between components
4. **Gap Identification**: Find missing or inconsistent elements
5. **Risk Assessment**: Identify potential issues or concerns
6. **Recommendation Generation**: Suggest improvements and fixes
7. **Report Creation**: Compile findings into comprehensive report

## Best Practices
- **Run analysis regularly**: Check alignment at key project milestones
- **Act on findings**: Address identified issues promptly
- **Use as decision aid**: Reference analysis when making changes
- **Share with team**: Discuss findings and implications
- **Track improvements**: Monitor how analysis results change over time
- **Combine with reviews**: Use analysis to inform code and design reviews

## Examples

### Comprehensive Project Analysis
```
/analyze
```

Analyzes:
- Goal-to-implementation alignment
- Technical architecture consistency
- Project structure completeness
- Documentation coverage
- Testing strategy adequacy

### Focused Technical Analysis
```
/analyze --include-technical --include-structure
```

Focuses on:
- Code organization and patterns
- Technology stack consistency
- Configuration management
- Security practices
- Performance considerations

### Goal Alignment Check
```
/analyze --include-goals
```

Examines:
- Goal definition completeness
- Strategy-goal alignment
- Plan-strategy consistency
- Task-plan relevance
- Progress tracking alignment

## Analysis Report Structure
Generated reports include:
- **Executive Summary**: Key findings and recommendations
- **Goal Alignment**: Assessment of goal-to-implementation flow
- **Technical Analysis**: Technical consistency and quality metrics
- **Project Health**: Overall project status and concerns
- **Detailed Findings**: Specific issues and inconsistencies
- **Recommendations**: Actionable improvement suggestions
- **Risk Assessment**: Potential issues and mitigation strategies

## Next Steps
After running analysis with `/analyze`:
1. **Review findings** and prioritize issues
2. **Address critical problems** identified in the report
3. **Update goals, strategies, or plans** as needed
4. **Fix technical inconsistencies** and gaps
5. **Implement recommendations** for improvement
6. **Share results** with team and stakeholders
7. **Schedule follow-up analysis** to track improvements

## Troubleshooting
- **Too many findings**: Focus on critical and high-priority issues first
- **Analysis seems wrong**: Verify that goals and plans are up-to-date
- **Technical issues**: Ensure project follows established patterns
- **Missing context**: Provide more specific project information
- **Unclear recommendations**: Ask for clarification on specific findings
- **Overwhelming report**: Use focused analysis with specific flags

## Integration with Other Commands
Analysis helps:
- **Validate goals** (`/goals`): Ensure goals are realistic and achievable
- **Refine strategies** (`/strategize`): Identify strategy gaps or inconsistencies
- **Improve plans** (`/plan`): Surface planning gaps or misalignments
- **Optimize tasks** (`/tasks`): Identify task redundancies or gaps
- **Guide implementation** (`/implement`): Highlight areas needing attention