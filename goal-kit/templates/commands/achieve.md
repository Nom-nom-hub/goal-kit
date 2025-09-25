---
title: "Achievement Execution Command"
description: "Execute and track goal achievements with TDD-style breakdown"
agent: "goal-kit"
version: "1.0"
command_type: "goal_execution"
execution_context: "achievement_tracking"
required_tools: ["file_system", "task_manager", "progress_tracker"]
---

# Achievement Execution Command Template

## Command Overview

**Command:** `goal achieve`
**Purpose:** Execute goal achievements with TDD-style task breakdown and tracking
**Input:** Goal file and achievement specifications
**Output:** Updated progress and achievement status

## Command Usage

### Basic Syntax

```bash
goal achieve [goal-file] [achievement-id] --status [status] --progress [percentage]
```

### Advanced Syntax

```bash
goal achieve "web-app-goal.json" A1 \
  --status completed \
  --progress 100 \
  --deliverables "user-auth-system,admin-panel" \
  --quality-metrics "test-coverage:95%,performance:good" \
  --lessons-learned "early-prototyping-valuable"
```

## Command Types

### Mark Achievement Complete

```bash
goal achieve [goal-file] [achievement-id] --status completed --progress 100
```

### Update Achievement Progress

```bash
goal achieve [goal-file] [achievement-id] --progress 75 --status in_progress
```

### Add Achievement Evidence

```bash
goal achieve [goal-file] [achievement-id] --evidence-add [file-path]
```

### Review Achievement Quality

```bash
goal achieve [goal-file] [achievement-id] --quality-review --criteria [criteria]
```

### Achievement Breakdown

```bash
goal achieve [goal-file] breakdown [achievement-id] --method tdd
```

## Command Parameters

### Required Parameters

- **goal-file** (string): Path to the goal JSON file
- **achievement-id** (string): Achievement identifier (e.g., A1, A2, 1.1)

### Status Parameters

- **status** (string): Achievement status [not_started/in_progress/review/completed/blocked]
- **progress** (number): Progress percentage (0-100)

### Optional Parameters

- **deliverables** (string): Comma-separated list of completed deliverables
- **quality-metrics** (string): Key-value pairs of quality measurements
- **lessons-learned** (string): Insights and lessons from this achievement
- **evidence** (string): Path to supporting evidence or documentation
- **notes** (string): Additional notes or observations
- **reviewer** (string): Person who reviewed this achievement

### Advanced Parameters

- **validation-method** (string): How to validate this achievement [automated/manual/peer-review]
- **quality-gates** (array): Quality criteria that must be met
- **dependencies-met** (array): Dependencies that were satisfied
- **next-actions** (array): Recommended next steps

## Command Examples

### Example 1: Mark Achievement Complete

```bash
goal achieve "web-app-goal.json" A1 \
  --status completed \
  --progress 100 \
  --deliverables "user-registration,login-system,email-verification" \
  --quality-metrics "test-coverage:92%,security-scan:passed,performance:excellent"
```

### Example 2: Update Progress with Evidence

```bash
goal achieve "ai-model-goal.json" M2 \
  --status in_progress \
  --progress 65 \
  --evidence-add "./models/trained_model_v1.pkl" \
  --notes "Model accuracy improved from 87% to 94%" \
  --lessons-learned "feature-engineering-critical-for-accuracy"
```

### Example 3: Achievement with Quality Review

```bash
goal achieve "mobile-app-goal.json" UI1 \
  --status review \
  --progress 90 \
  --quality-review \
  --criteria "usability,accessibility,performance,design-consistency" \
  --reviewer "ux-lead" \
  --notes "Minor accessibility issues found, ready for final review"
```

### Example 4: TDD-Style Achievement Breakdown

```bash
goal achieve "api-development-goal.json" breakdown A2 \
  --method tdd \
  --tasks "write-failing-tests,implement-minimal-api,add-error-handling,optimize-performance"
```

### Example 5: Achievement with Dependencies

```bash
goal achieve "data-pipeline-goal.json" DP3 \
  --status completed \
  --progress 100 \
  --dependencies-met "DP1,DP2" \
  --next-actions "monitor-pipeline-health,setup-alerting,document-troubleshooting"
```

## Achievement Execution Strategies

### TDD-Style Development

```javascript
// Test-Driven Development approach for achievements
const tddProcess = {
  1: { step: "Write Failing Test", description: "Define success criteria" },
  2: {
    step: "Implement Minimal Solution",
    description: "Basic implementation that passes test",
  },
  3: {
    step: "Refactor and Improve",
    description: "Enhance code while maintaining test coverage",
  },
  4: {
    step: "Validate and Document",
    description: "Ensure quality and document the solution",
  },
};
```

### Parallel Task Execution

```javascript
const parallelExecution = {
  achievement: "User Interface Development",
  parallelTasks: [
    { task: "Design System", assignee: "UI Designer", duration: "2 weeks" },
    {
      task: "Component Library",
      assignee: "Frontend Dev",
      duration: "3 weeks",
    },
    {
      task: "Responsive Layout",
      assignee: "Frontend Dev",
      duration: "2 weeks",
    },
    {
      task: "Accessibility Audit",
      assignee: "QA Engineer",
      duration: "1 week",
    },
  ],
  synchronizationPoints: ["Week 2: Design Review", "Week 3: Integration Test"],
};
```

### Quality Gates and Validation

```javascript
const qualityGates = {
  achievement: "Security Implementation",
  gates: [
    {
      name: "Code Security Review",
      type: "manual",
      criteria: "No high-severity vulnerabilities",
      responsible: "Security Lead",
    },
    {
      name: "Automated Security Tests",
      type: "automated",
      criteria: "All security tests passing",
      threshold: "100% pass rate",
    },
    {
      name: "Performance Benchmark",
      type: "automated",
      criteria: "Response time < 200ms",
      threshold: "95th percentile",
    },
    {
      name: "Documentation Review",
      type: "manual",
      criteria: "Complete API documentation",
      responsible: "Technical Writer",
    },
  ],
};
```

## Progress Tracking Methods

### Quantitative Progress Tracking

```javascript
const progressMetrics = {
  achievement: "Database Migration",
  metrics: {
    totalTasks: 15,
    completedTasks: 12,
    inProgressTasks: 2,
    blockedTasks: 1,
    completionPercentage: 80,
    estimatedCompletion: "2024-02-20",
    velocity: 3.5, // tasks per day
  },
  qualityIndicators: {
    testCoverage: 88,
    codeQualityScore: "A-",
    securityScanResults: "Clean",
    performanceBenchmark: "Excellent",
  },
};
```

### Qualitative Progress Assessment

```javascript
const qualitativeAssessment = {
  achievement: "Team Training Program",
  assessment: {
    knowledgeTransfer: "Good",
    skillApplication: "Excellent",
    confidenceLevel: "High",
    engagementLevel: "Very High",
    feedback: "Team members report high satisfaction and clear understanding",
  },
  evidence: [
    "Training session recordings",
    "Quiz results (average 92%)",
    "Hands-on project completions",
    "Peer feedback surveys",
  ],
};
```

### Evidence Collection Framework

```javascript
const evidenceCollection = {
  types: [
    "Code commits and pull requests",
    "Test results and coverage reports",
    "Documentation updates",
    "Performance benchmarks",
    "Security scan reports",
    "User feedback and surveys",
    "Demo videos and screenshots",
    "Meeting notes and decisions",
  ],
  organization: {
    byMilestone: true,
    byAchievement: true,
    byDate: true,
    taggedByCategory: true,
  },
};
```

## Achievement Validation

### Automated Validation

```javascript
const automatedValidation = {
  achievement: "API Development",
  validators: [
    {
      name: "Unit Test Validator",
      type: "automated",
      command: "npm test",
      expectedResult: "All tests passing",
      timeout: "5 minutes",
    },
    {
      name: "Code Coverage Validator",
      type: "automated",
      command: "npm run coverage",
      expectedResult: "Coverage > 85%",
      timeout: "2 minutes",
    },
    {
      name: "Performance Validator",
      type: "automated",
      command: "npm run performance-test",
      expectedResult: "All benchmarks passing",
      timeout: "10 minutes",
    },
  ],
};
```

### Manual Validation

```javascript
const manualValidation = {
  achievement: "User Experience Design",
  validators: [
    {
      name: "Usability Review",
      type: "manual",
      responsible: "UX Designer",
      criteria: [
        "Intuitive navigation",
        "Consistent design language",
        "Accessible to all users",
        "Fast loading times",
      ],
    },
    {
      name: "Stakeholder Approval",
      type: "manual",
      responsible: "Product Owner",
      criteria: [
        "Meets business requirements",
        "Aligns with brand guidelines",
        "Ready for development",
      ],
    },
  ],
};
```

## Integration Points

### Version Control Integration

- Track achievement evidence in Git
- Link achievements to specific commits
- Create achievement branches for complex work
- Automatic achievement updates on merge

### Continuous Integration

- Automated testing on achievement progress
- Quality gate validation in CI/CD pipeline
- Achievement status updates on build completion
- Evidence collection from CI/CD artifacts

### Project Management Integration

- Sync achievements with project boards
- Update task status based on achievements
- Generate progress reports for stakeholders
- Resource allocation based on achievement status

## Best Practices

### Achievement Definition

- **Clear Criteria:** Specific, measurable completion criteria
- **Evidence-Based:** Require concrete evidence of completion
- **Quality-Focused:** Include quality validation requirements
- **Reviewable:** Allow for stakeholder review and feedback

### Progress Tracking

- **Regular Updates:** Frequent progress updates (daily/weekly)
- **Evidence Collection:** Collect evidence throughout the process
- **Quality Monitoring:** Track quality metrics continuously
- **Risk Management:** Identify and address blockers early

### Completion Validation

- **Comprehensive Review:** Multiple validation methods
- **Stakeholder Involvement:** Get feedback from relevant parties
- **Documentation:** Complete documentation of the achievement
- **Knowledge Transfer:** Share learnings with the team

## Troubleshooting

### Common Issues

1. **Unclear Achievement Criteria:** Use the clarify command to define better criteria
2. **Missing Evidence:** Set up evidence collection early in the process
3. **Quality Gate Failures:** Address quality issues before marking complete
4. **Dependency Issues:** Use dependency tracking to manage prerequisites

### Performance Optimization

- **Early Validation:** Validate assumptions early in the process
- **Parallel Execution:** Identify parallelizable tasks within achievements
- **Resource Allocation:** Ensure adequate resources for critical achievements
- **Risk Mitigation:** Proactive identification and management of risks

### Evidence Management

- **Organized Collection:** Systematic evidence organization
- **Version Control:** Evidence tracking in version control
- **Accessibility:** Easy access for stakeholders and reviewers
- **Completeness:** Comprehensive evidence for all criteria

## Related Commands

- `goal define` - Create goals with achievement structures
- `goal milestone` - Manage milestones and dependencies
- `goal progress` - Track overall goal progress
- `goal report` - Generate achievement reports
- `goal validate` - Validate achievement completion

## Command Reference

- `goal achieve --help` - Show detailed help
- `goal achieve examples` - Show usage examples
- `goal achieve templates` - List achievement templates
- `goal achieve validate [goal-file] [achievement-id]` - Validate achievement
