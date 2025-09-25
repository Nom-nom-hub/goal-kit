---
title: "Milestone Planning Command"
description: "Create and manage goal milestones with dependencies"
agent: "goal-kit"
version: "1.0"
command_type: "goal_management"
execution_context: "milestone_planning"
required_tools: ["file_system", "json_parser", "dependency_resolver"]
---

# Milestone Planning Command Template

## Command Overview
**Command:** `goal milestone`
**Purpose:** Create, update, and manage goal milestones with dependencies
**Input:** Goal file and milestone specifications
**Output:** Updated goal with milestone structure

## Command Usage

### Basic Syntax
```bash
goal milestone [goal-file] add "Milestone Name" --duration [weeks] --description "Description"
```

### Advanced Syntax
```bash
goal milestone my-goal.json add "Core Development" \
  --duration 4 \
  --description "Implement core features" \
  --depends-on "1,2" \
  --priority high \
  --resources "developer:2,designer:1" \
  --deliverables "feature-complete prototype"
```

## Command Types

### Add Milestone
```bash
goal milestone [goal-file] add [milestone-name] [options]
```

### Update Milestone
```bash
goal milestone [goal-file] update [milestone-id] [options]
```

### Delete Milestone
```bash
goal milestone [goal-file] delete [milestone-id]
```

### List Milestones
```bash
goal milestone [goal-file] list
```

### Milestone Status
```bash
goal milestone [goal-file] status [milestone-id]
```

## Command Parameters

### Required Parameters
- **goal-file** (string): Path to the goal JSON file
- **action** (string): Action to perform [add/update/delete/list/status]

### Milestone Definition Parameters
- **name** (string): Milestone name/title
- **description** (string): Detailed description of the milestone
- **duration** (number): Estimated duration in weeks
- **depends-on** (string): Comma-separated list of milestone IDs this depends on

### Optional Parameters
- **priority** (string): Priority level [low/medium/high/critical]
- **status** (string): Current status [not_started/in_progress/review/completed]
- **start_date** (date): Milestone start date (YYYY-MM-DD)
- **end_date** (date): Milestone end date (YYYY-MM-DD)
- **resources** (string): Resource requirements (format: "role:count,role:count")
- **deliverables** (string): Comma-separated list of expected deliverables
- **success_criteria** (string): Criteria for milestone completion
- **risk_level** (string): Risk level [low/medium/high]

## Command Examples

### Example 1: Add Basic Milestone
```bash
goal milestone "web-app-goal.json" add "Project Setup" \
  --duration 2 \
  --description "Set up development environment and project structure" \
  --priority high
```

### Example 2: Add Milestone with Dependencies
```bash
goal milestone "web-app-goal.json" add "Authentication System" \
  --duration 3 \
  --description "Implement user authentication and authorization" \
  --depends-on "1,2" \
  --resources "backend-developer:2,security-expert:1" \
  --deliverables "login-system,user-roles,security-tests"
```

### Example 3: Complex Milestone Chain
```bash
# Foundation milestone
goal milestone "ai-project.json" add "Data Pipeline Setup" \
  --duration 2 \
  --description "Build data ingestion and processing pipeline" \
  --priority critical \
  --resources "data-engineer:1,ml-engineer:1"

# Dependent milestone
goal milestone "ai-project.json" add "Model Development" \
  --duration 4 \
  --description "Develop and train machine learning models" \
  --depends-on "1" \
  --resources "ml-engineer:2,data-scientist:1" \
  --success_criteria "model-accuracy>95%,validation-complete"

# Parallel milestone
goal milestone "ai-project.json" add "API Development" \
  --duration 3 \
  --description "Build REST API for model inference" \
  --depends-on "1" \
  --resources "backend-developer:1,api-architect:1"
```

### Example 4: Update Milestone Status
```bash
goal milestone "web-app-goal.json" update 2 \
  --status in_progress \
  --progress 25
```

### Example 5: Milestone Planning Session
```bash
# Create comprehensive milestone structure
goal milestone "startup-goal.json" add "Market Research" \
  --duration 3 \
  --description "Conduct market analysis and competitive research"

goal milestone "startup-goal.json" add "MVP Development" \
  --duration 8 \
  --depends-on "1" \
  --resources "fullstack-developer:2,ui-designer:1"

goal milestone "startup-goal.json" add "Beta Testing" \
  --duration 4 \
  --depends-on "2" \
  --resources "qa-tester:1,product-manager:1"

goal milestone "startup-goal.json" add "Launch Preparation" \
  --duration 2 \
  --depends-on "3" \
  --resources "marketing-specialist:1,operations-manager:1"
```

## Milestone Planning Strategies

### Sequential Milestones
```javascript
// Example: Waterfall approach
const sequentialMilestones = [
  { name: "Planning", duration: 2, dependsOn: [] },
  { name: "Design", duration: 4, dependsOn: ["1"] },
  { name: "Development", duration: 8, dependsOn: ["2"] },
  { name: "Testing", duration: 3, dependsOn: ["3"] },
  { name: "Deployment", duration: 1, dependsOn: ["4"] }
];
```

### Parallel Milestones
```javascript
// Example: Agile approach with parallel streams
const parallelMilestones = [
  { name: "Backend Development", duration: 6, dependsOn: [] },
  { name: "Frontend Development", duration: 6, dependsOn: [] },
  { name: "Database Design", duration: 4, dependsOn: [] },
  { name: "API Integration", duration: 3, dependsOn: ["1", "2", "3"] }
];
```

### Hybrid Approach
```javascript
// Example: Combination of sequential and parallel
const hybridMilestones = [
  { name: "Foundation", duration: 2, dependsOn: [] },
  {
    name: "Core Development",
    duration: 6,
    dependsOn: ["1"],
    parallelTasks: ["backend", "frontend", "database"]
  },
  { name: "Integration", duration: 3, dependsOn: ["2"] },
  { name: "Launch", duration: 2, dependsOn: ["3"] }
];
```

## Dependency Management

### Dependency Types
- **Hard Dependencies:** Must be completed before starting
- **Soft Dependencies:** Can start with partial completion
- **Resource Dependencies:** Requires specific resources
- **External Dependencies:** Outside the current goal scope

### Dependency Resolution
```javascript
function resolveDependencies(milestones) {
  const dependencyGraph = buildDependencyGraph(milestones);
  const executionOrder = topologicalSort(dependencyGraph);
  const criticalPath = calculateCriticalPath(executionOrder);
  return { executionOrder, criticalPath };
}
```

### Circular Dependency Detection
```javascript
function detectCircularDependencies(milestones) {
  const graph = buildDependencyGraph(milestones);
  const visited = new Set();
  const recursionStack = new Set();

  for (const milestone of milestones) {
    if (hasCircularDependency(milestone, graph, visited, recursionStack)) {
      throw new Error(`Circular dependency detected involving ${milestone.name}`);
    }
  }
}
```

## Resource Planning

### Resource Allocation
```javascript
const resourcePlan = {
  milestones: [
    {
      name: "Development Phase",
      resources: {
        "Software Engineer": { quantity: 3, allocation: "100%" },
        "UI/UX Designer": { quantity: 1, allocation: "50%" },
        "DevOps Engineer": { quantity: 1, allocation: "25%" }
      }
    }
  ],
  totalFTE: 4.75,
  budgetAllocation: 150000
};
```

### Resource Conflict Resolution
```javascript
function resolveResourceConflicts(milestones) {
  const resourceUsage = calculateResourceUsage(milestones);
  const conflicts = identifyConflicts(resourceUsage);
  const resolutionStrategies = [
    "Adjust timelines",
    "Add resources",
    "Reduce scope",
    "Outsource tasks"
  ];
  return { conflicts, resolutionStrategies };
}
```

## Risk Assessment

### Milestone Risk Analysis
| Risk Category | Probability | Impact | Mitigation |
|---------------|------------|--------|------------|
| Technical Complexity | High | High | Prototype early |
| Resource Availability | Medium | High | Backup resources |
| Dependency Delays | Medium | Medium | Buffer time |
| Scope Creep | High | Medium | Strict change control |

### Risk Mitigation Strategies
- **Buffer Time:** Add 10-20% buffer to milestone durations
- **Parallel Paths:** Create alternative approaches
- **Early Validation:** Test assumptions early
- **Stakeholder Buy-in:** Regular milestone reviews

## Quality Gates

### Milestone Exit Criteria
```javascript
const exitCriteria = {
  milestone: "Core Development",
  criteria: [
    "All features implemented",
    "Unit tests passing (80% coverage)",
    "Code review completed",
    "Performance benchmarks met",
    "Documentation updated"
  ],
  validationMethods: [
    "Automated testing",
    "Code review",
    "Stakeholder demo",
    "Performance testing"
  ]
};
```

### Quality Metrics
- **Completion Quality:** Meets all acceptance criteria
- **Timeliness:** Delivered within planned timeframe
- **Budget Adherence:** Within allocated budget
- **Stakeholder Satisfaction:** Meets or exceeds expectations

## Progress Tracking

### Milestone Progress Indicators
```javascript
const progressIndicators = {
  milestone: "Development Phase",
  totalTasks: 25,
  completedTasks: 18,
  inProgressTasks: 5,
  blockedTasks: 2,
  progressPercentage: 72,
  estimatedCompletion: "2024-02-15",
  velocity: 4.5 // tasks per week
};
```

### Progress Calculation
```javascript
function calculateProgress(milestone) {
  const totalWeight = milestone.tasks.reduce((sum, task) => sum + task.weight, 0);
  const completedWeight = milestone.tasks
    .filter(task => task.status === 'completed')
    .reduce((sum, task) => sum + task.weight, 0);

  return (completedWeight / totalWeight) * 100;
}
```

## Integration Points

### Version Control Integration
- Track milestone changes in Git
- Milestone branches for parallel work
- Automatic milestone updates on commits

### Project Management Integration
- Sync milestones with project management tools
- Automated progress updates
- Resource allocation tracking

### Calendar Integration
- Milestone deadline reminders
- Review meeting scheduling
- Resource booking notifications

## Best Practices

### Milestone Design
- **Clear Scope:** Each milestone should have well-defined boundaries
- **Measurable Outcomes:** Specific deliverables and success criteria
- **Realistic Duration:** Based on team capacity and complexity
- **Balanced Workload:** Distribute work evenly across milestones

### Dependency Management
- **Minimal Dependencies:** Reduce unnecessary dependencies
- **Clear Relationships:** Explicit predecessor/successor relationships
- **Critical Path Focus:** Monitor milestones on critical path
- **Buffer Management:** Include buffers for high-risk dependencies

### Resource Planning
- **Capacity Planning:** Match resources to milestone requirements
- **Skill Alignment:** Ensure team skills match milestone needs
- **Contingency Planning:** Backup resources for critical milestones
- **Work-Life Balance:** Avoid resource overload

## Troubleshooting

### Common Issues
1. **Milestone too large:** Break into smaller, manageable pieces
2. **Unclear dependencies:** Map and validate all dependencies
3. **Resource conflicts:** Rebalance resource allocation
4. **Scope creep:** Implement strict change control

### Performance Optimization
- **Critical Path Analysis:** Focus on bottleneck milestones
- **Parallel Processing:** Identify parallelizable work
- **Resource Leveling:** Optimize resource utilization
- **Risk Mitigation:** Proactive risk management

## Related Commands
- `goal define` - Create new goals with milestones
- `goal progress` - Track milestone progress
- `goal achieve` - Mark milestone completion
- `goal report` - Generate milestone reports
- `goal resource` - Manage resource allocation

## Command Reference
- `goal milestone --help` - Show detailed help
- `goal milestone examples` - Show usage examples
- `goal milestone templates` - List milestone templates
- `goal milestone validate [goal-file]` - Validate milestone structure