# Multi-Team and Workflow Support

This document outlines the advanced multi-team and workflow support for Goal-Dev-Spec that exceeds spec-kit functionality.

## Team Organization Structure

### Team Directory Structure

```
teams/
├── engineering/
│   ├── frontend/
│   │   ├── team.yaml
│   │   ├── goals/
│   │   ├── specs/
│   │   └── workflows/
│   ├── backend/
│   │   ├── team.yaml
│   │   ├── goals/
│   │   ├── specs/
│   │   └── workflows/
│   ├── devops/
│   │   ├── team.yaml
│   │   ├── goals/
│   │   ├── specs/
│   │   └── workflows/
│   └── qa/
│       ├── team.yaml
│       ├── goals/
│       ├── specs/
│       └── workflows/
├── product/
│   ├── management/
│   │   ├── team.yaml
│   │   ├── goals/
│   │   ├── specs/
│   │   └── workflows/
│   └── design/
│       ├── team.yaml
│       ├── goals/
│       ├── specs/
│       └── workflows/
├── data/
│   ├── science/
│   │   ├── team.yaml
│   │   ├── goals/
│   │   ├── specs/
│   │   └── workflows/
│   └── analytics/
│       ├── team.yaml
│       ├── goals/
│       ├── specs/
│       └── workflows/
└── operations/
    ├── support/
    │   ├── team.yaml
    │   ├── goals/
    │   ├── specs/
    │   └── workflows/
    └── security/
        ├── team.yaml
        ├── goals/
        ├── specs/
        └── workflows/
```

### Team Configuration

Each team has a configuration file defining its structure:

```yaml
# teams/engineering/frontend/team.yaml
team:
  name: "Frontend Engineering"
  description: "Responsible for user interface development"
  lead: "Frontend Lead"
  members:
    - name: "Alice Johnson"
      role: "Senior Frontend Developer"
      responsibilities:
        - Component development
        - UI implementation
        - Performance optimization
    - name: "Bob Smith"
      role: "Frontend Developer"
      responsibilities:
        - Feature implementation
        - Bug fixes
        - Code reviews
    - name: "Carol Davis"
      role: "Frontend Developer"
      responsibilities:
        - Accessibility implementation
        - Testing
        - Documentation

  goals:
    - "Implement responsive design system"
    - "Optimize application performance"
    - "Ensure cross-browser compatibility"

  workflows:
    - daily-standup
    - sprint-planning
    - code-review
    - testing

  tools:
    - react
    - typescript
    - jest
    - storybook

  metrics:
    - code-review-time
    - bug-fix-time
    - feature-delivery-time
```

## Workflow Management System

### Workflow Directory Structure

```
.workflows/
├── development/
│   ├── agile/
│   │   ├── sprint-planning.yaml
│   │   ├── daily-standup.yaml
│   │   ├── sprint-review.yaml
│   │   └── retrospective.yaml
│   ├── kanban/
│   │   ├── board-management.yaml
│   │   └── continuous-flow.yaml
│   └── waterfall/
│       ├── phase-gates.yaml
│       └── documentation.yaml
├── review/
│   ├── code-review.yaml
│   ├── design-review.yaml
│   └── security-review.yaml
├── testing/
│   ├── unit-testing.yaml
│   ├── integration-testing.yaml
│   └── end-to-end-testing.yaml
├── deployment/
│   ├── continuous-integration.yaml
│   ├── continuous-deployment.yaml
│   └── release-management.yaml
└── incident/
    ├── incident-response.yaml
    └── post-mortem.yaml
```

### Workflow Definition

Workflows are defined in YAML with clear steps and responsibilities:

```yaml
# .workflows/development/agile/sprint-planning.yaml
workflow:
  name: "Sprint Planning"
  description: "Plan work for the upcoming sprint"
  type: "ceremony"
  frequency: "bi-weekly"
  duration: "2 hours"
  participants:
    - product-manager
    - engineering-lead
    - team-members
  
  steps:
    - name: "Review Backlog"
      description: "Review and prioritize product backlog items"
      responsible: "product-manager"
      duration: "30 minutes"
      artifacts:
        - product-backlog
    
    - name: "Estimate Stories"
      description: "Estimate effort for selected stories"
      responsible: "team-members"
      duration: "45 minutes"
      artifacts:
        - story-points
    
    - name: "Commit to Sprint"
      description: "Team commits to sprint goals"
      responsible: "engineering-lead"
      duration: "30 minutes"
      artifacts:
        - sprint-backlog
        - sprint-goal
    
    - name: "Assign Tasks"
      description: "Break down stories into tasks and assign"
      responsible: "team-members"
      duration: "15 minutes"
      artifacts:
        - task-assignments

  success_criteria:
    - Sprint goal is clearly defined
    - All stories are estimated
    - Team has committed to deliverables
    - Tasks are assigned to team members

  metrics:
    - planning-accuracy
    - story-point-velocity
    - team-commitment-rate
```

## Cross-Team Collaboration

### Inter-Team Dependencies

Managing dependencies between teams:

```yaml
# .goal/goals/abc123/goal.yaml
goal:
  id: "abc123"
  title: "Implement User Authentication"
  description: "Develop secure user authentication system"
  
  dependencies:
    - team: "design"
      goal_id: "def456"
      description: "UI design for login screens"
      status: "pending"
    
    - team: "backend"
      goal_id: "ghi789"
      description: "API endpoints for authentication"
      status: "in-progress"
    
    - team: "security"
      goal_id: "jkl012"
      description: "Security review of authentication implementation"
      status: "planned"

  stakeholders:
    - team: "engineering"
      role: "implementer"
    - team: "product"
      role: "owner"
    - team: "qa"
      role: "validator"
    - team: "security"
      role: "advisor"
```

### Collaboration Workflows

Workflows that span multiple teams:

```yaml
# .workflows/collaboration/cross-team-review.yaml
workflow:
  name: "Cross-Team Design Review"
  description: "Review design decisions that impact multiple teams"
  type: "ceremony"
  frequency: "as-needed"
  duration: "1-2 hours"
  participants:
    - design-team
    - engineering-team
    - product-team
    - security-team
  
  steps:
    - name: "Design Presentation"
      description: "Present design to all stakeholders"
      responsible: "design-team"
      duration: "30 minutes"
    
    - name: "Engineering Feedback"
      description: "Engineering team provides technical feedback"
      responsible: "engineering-team"
      duration: "30 minutes"
    
    - name: "Product Feedback"
      description: "Product team provides business feedback"
      responsible: "product-team"
      duration: "20 minutes"
    
    - name: "Security Feedback"
      description: "Security team provides security feedback"
      responsible: "security-team"
      duration: "20 minutes"
    
    - name: "Decision Making"
      description: "Make decisions based on all feedback"
      responsible: "product-manager"
      duration: "20 minutes"

  artifacts:
    - design-documents
    - feedback-notes
    - decision-log

  success_criteria:
    - All stakeholder concerns are addressed
    - Design decisions are documented
    - Next steps are clearly defined
```

## Team Communication System

### Communication Channels

Structured communication channels for teams:

```yaml
# teams/engineering/frontend/communication.yaml
communication:
  channels:
    - name: "Frontend Team Standup"
      type: "video-call"
      frequency: "daily"
      time: "09:00 AM"
      participants: "all-team-members"
      agenda:
        - Yesterday's progress
        - Today's plans
        - Blockers
    
    - name: "Frontend Tech Sync"
      type: "slack-channel"
      frequency: "ongoing"
      participants: "all-team-members"
      purpose: "Technical discussions and code reviews"
    
    - name: "Frontend Planning"
      type: "video-call"
      frequency: "bi-weekly"
      time: "Monday 10:00 AM"
      participants: "all-team-members"
      agenda:
        - Sprint planning
        - Retrospective
        - Technical planning
    
    - name: "Frontend Leadership"
      type: "email-group"
      frequency: "weekly"
      participants: "team-lead"
      purpose: "Leadership updates and cross-team coordination"
```

### Meeting Templates

Standardized meeting templates:

```markdown
# [TEAM] Daily Standup - [DATE]

## Attendees
- [Attendee 1]
- [Attendee 2]
- [Attendee 3]

## Yesterday
- [Team member 1]: [What they worked on]
- [Team member 2]: [What they worked on]
- [Team member 3]: [What they worked on]

## Today
- [Team member 1]: [What they plan to work on]
- [Team member 2]: [What they plan to work on]
- [Team member 3]: [What they plan to work on]

## Blockers
- [Blocker 1]: [Description and owner]
- [Blocker 2]: [Description and owner]

## Notes
[Any additional notes or discussions]
```

## Resource Management

### Team Resource Allocation

Managing resources across teams:

```yaml
# teams/engineering/resources.yaml
resources:
  personnel:
    - name: "Alice Johnson"
      role: "Senior Frontend Developer"
      allocation:
        - team: "frontend"
          percentage: 80
          goals:
            - "implement-dashboard"
            - "optimize-performance"
        - team: "cross-functional"
          percentage: 20
          goals:
            - "accessibility-improvements"
    
    - name: "Bob Smith"
      role: "Frontend Developer"
      allocation:
        - team: "frontend"
          percentage: 100
          goals:
            - "feature-implementation"
            - "bug-fixing"

  tools:
    - name: "Figma"
      teams:
        - design
        - frontend
        - product
      licenses: 10
    
    - name: "Jira"
      teams:
        - all
      licenses: 25

  infrastructure:
    - name: "Development Environment"
      teams:
        - engineering
      access: "shared"
    
    - name: "Staging Environment"
      teams:
        - engineering
        - qa
      access: "shared"
```

### Capacity Planning

Capacity planning across teams:

```yaml
# teams/capacity-planning.yaml
capacity:
  q4-2025:
    engineering:
      frontend:
        available_hours: 320
        committed_hours: 280
        utilization: 87.5%
      backend:
        available_hours: 360
        committed_hours: 340
        utilization: 94.4%
      devops:
        available_hours: 320
        committed_hours: 200
        utilization: 62.5%
    
    product:
      management:
        available_hours: 320
        committed_hours: 250
        utilization: 78.1%
    
    qa:
      testing:
        available_hours: 320
        committed_hours: 220
        utilization: 68.8%

  risks:
    - team: "backend"
      risk: "High utilization may lead to burnout"
      mitigation: "Hire additional backend developer"
    
    - team: "devops"
      risk: "Underutilization may indicate misalignment"
      mitigation: "Reassess team responsibilities"
```

## Workflow Automation

### Automated Workflow Triggers

Automating workflow execution:

```yaml
# .workflows/automation/code-review-trigger.yaml
automation:
  name: "Code Review Trigger"
  description: "Automatically trigger code review workflow"
  trigger:
    event: "pull-request-created"
    repository: "frontend"
  
  actions:
    - name: "Assign Reviewers"
      type: "notification"
      target: "team-members"
      message: "New pull request requires review: {{pr_url}}"
    
    - name: "Update Task Status"
      type: "task-update"
      task_id: "{{task_id}}"
      status: "in-review"
    
    - name: "Log Workflow Start"
      type: "audit-log"
      message: "Code review workflow started for PR {{pr_id}}"
```

### Workflow Metrics and Analytics

Tracking workflow performance:

```yaml
# .workflows/metrics/code-review.yaml
metrics:
  name: "Code Review Metrics"
  description: "Track code review process performance"
  
  kpis:
    - name: "Average Review Time"
      description: "Average time from PR creation to review completion"
      target: "< 24 hours"
      calculation: "avg(time_to_review_completion)"
    
    - name: "Review Coverage"
      description: "Percentage of code changes that receive review"
      target: "100%"
      calculation: "count(reviewed_prs) / count(total_prs)"
    
    - name: "Reviewer Participation"
      description: "Percentage of team members participating in reviews"
      target: "> 80%"
      calculation: "count(active_reviewers) / count(team_members)"
    
    - name: "Defect Detection Rate"
      description: "Number of defects caught in code review"
      target: "> 50% of total defects"
      calculation: "count(review_defects) / count(total_defects)"

  reporting:
    frequency: "weekly"
    recipients:
      - engineering-lead
      - team-members
    format: "dashboard"
```

## Multi-Team Goal Management

### Cross-Team Goal Dependencies

Managing goals that span multiple teams:

```yaml
# .goal/goals/xyz789/goal.yaml
goal:
  id: "xyz789"
  title: "Launch E-commerce Platform"
  description: "Complete launch of full e-commerce platform"
  
  cross_team_dependencies:
    - team: "frontend"
      deliverables:
        - "responsive-ui"
        - "checkout-flow"
      timeline: "Q1 2026"
      status: "in-progress"
    
    - team: "backend"
      deliverables:
        - "product-catalog-api"
        - "payment-processing-api"
      timeline: "Q1 2026"
      status: "planned"
    
    - team: "design"
      deliverables:
        - "ui-design-system"
        - "user-experience-flows"
      timeline: "Q4 2025"
      status: "completed"
    
    - team: "qa"
      deliverables:
        - "test-cases"
        - "automated-tests"
      timeline: "Q1 2026"
      status: "planned"
    
    - team: "devops"
      deliverables:
        - "deployment-pipeline"
        - "monitoring-setup"
      timeline: "Q1 2026"
      status: "planned"

  integration_points:
    - name: "Frontend-Backend API"
      teams: ["frontend", "backend"]
      status: "in-development"
    
    - name: "Payment Integration"
      teams: ["backend", "external"]
      status: "planned"
    
    - name: "Analytics Integration"
      teams: ["backend", "data"]
      status: "planned"

  success_criteria:
    - "Platform is live and accessible"
    - "All core features are functional"
    - "Performance meets SLA requirements"
    - "Security audit is passed"
```

### Multi-Team Reporting

Reporting across teams:

```yaml
# teams/reporting/cross-team-status.yaml
reporting:
  name: "Cross-Team Status Report"
  description: "Weekly status report across all teams"
  frequency: "weekly"
  
  sections:
    - name: "Executive Summary"
      audience: "executives"
      content:
        - overall_progress
        - key_milestones
        - major_risks
    
    - name: "Team Status"
      audience: "all-teams"
      content:
        - team_progress
        - completed_goals
        - upcoming_deliverables
    
    - name: "Cross-Team Dependencies"
      audience: "team-leads"
      content:
        - dependency_status
        - blocker_resolution
        - resource_allocation
    
    - name: "Metrics Dashboard"
      audience: "managers"
      content:
        - kpi_summary
        - trend_analysis
        - benchmark_comparison

  distribution:
    - channel: "email"
      recipients: "all-stakeholders"
      format: "pdf"
    
    - channel: "dashboard"
      recipients: "team-leads"
      format: "interactive"
    
    - channel: "slack"
      recipients: "all-teams"
      format: "summary"
```

## Team Customization and Flexibility

### Team-Specific Workflows

Allowing teams to customize their workflows:

```yaml
# teams/engineering/frontend/custom-workflows.yaml
custom_workflows:
  - name: "Frontend Component Review"
    description: "Specialized review process for UI components"
    base_workflow: "code-review"
    modifications:
      - add_step:
          name: "Accessibility Check"
          description: "Verify component meets accessibility standards"
          responsible: "accessibility-specialist"
          duration: "15 minutes"
      
      - modify_step:
          name: "Performance Testing"
          description: "Test component performance in different browsers"
          responsible: "frontend-developer"
          duration: "30 minutes"
      
      - add_artifact:
          name: "Accessibility Report"
          description: "Document accessibility test results"
      
      - add_success_criteria:
          - "Component passes accessibility standards"
          - "Component performs well across browsers"
```

### Flexible Team Structures

Supporting different team structures:

```yaml
# teams/organization.yaml
organization:
  structure: "matrix"
  
  functional_teams:
    - name: "Engineering"
      subteams:
        - frontend
        - backend
        - devops
        - qa
    
    - name: "Product"
      subteams:
        - management
        - design
    
    - name: "Data"
      subteams:
        - science
        - analytics
  
  project_teams:
    - name: "E-commerce Launch"
      members:
        - team: "frontend"
          representatives: ["Alice Johnson"]
        - team: "backend"
          representatives: ["David Wilson"]
        - team: "design"
          representatives: ["Eva Martinez"]
        - team: "qa"
          representatives: ["Frank Thompson"]
  
  virtual_teams:
    - name: "Security Working Group"
      members:
        - "Carol Davis"  # from frontend
        - "Grace Lee"    # from backend
        - "Henry Brown"  # from operations/security
      purpose: "Cross-functional security initiatives"
```

## Integration with External Tools

### Tool Integration Framework

Integrating with external collaboration tools:

```yaml
# teams/integrations/slack.yaml
integrations:
  tool: "Slack"
  teams:
    - engineering
    - product
    - data
  
  channels:
    - name: "#engineering"
      purpose: "Engineering team communication"
      workflows:
        - daily-standup-notifications
        - build-status-updates
        - deployment-notifications
    
    - name: "#product"
      purpose: "Product team communication"
      workflows:
        - sprint-planning-reminders
        - release-announcements
        - customer-feedback
    
    - name: "#general"
      purpose: "Company-wide communication"
      workflows:
        - company-announcements
        - all-hands-meeting-reminders
        - social-events

  bots:
    - name: "GoalBot"
      purpose: "Goal tracking and updates"
      commands:
        - "/goal status [goal-id]"
        - "/goal create [description]"
        - "/goal assign [goal-id] [assignee]"
```

### Calendar Integration

Integrating with calendar systems:

```yaml
# teams/integrations/calendar.yaml
calendar:
  provider: "Google Calendar"
  integration_type: "two-way"
  
  event_sync:
    - workflow: "sprint-planning"
      calendar: "Team Calendars"
      event_template: "Sprint Planning - {{team_name}}"
    
    - workflow: "daily-standup"
      calendar: "Team Calendars"
      recurrence: "daily"
      event_template: "Daily Standup - {{team_name}}"
    
    - workflow: "retrospective"
      calendar: "Team Calendars"
      recurrence: "bi-weekly"
      event_template: "Retrospective - {{team_name}}"

  notifications:
    - event: "15-minutes-before"
      channel: "slack"
      message: "Reminder: {{event_name}} starts in 15 minutes"
    
    - event: "day-before"
      channel: "email"
      message: "Tomorrow: {{event_name}} at {{event_time}}"
```

## Team Performance Management

### Performance Metrics

Tracking team performance:

```yaml
# teams/performance/metrics.yaml
performance:
  name: "Team Performance Metrics"
  description: "Track and improve team performance"
  
  engineering_metrics:
    - name: "Velocity"
      description: "Story points completed per sprint"
      teams: ["engineering"]
      target: "> 30 points/sprint"
    
    - name: "Code Quality"
      description: "Code review approval rate and defect density"
      teams: ["engineering"]
      target: "> 90% approval rate, < 1 defect/story"
    
    - name: "Deployment Frequency"
      description: "Number of deployments per week"
      teams: ["devops"]
      target: "> 5 deployments/week"
  
  product_metrics:
    - name: "Goal Completion Rate"
      description: "Percentage of goals completed on time"
      teams: ["product"]
      target: "> 85%"
    
    - name: "Customer Satisfaction"
      description: "Customer feedback scores"
      teams: ["product"]
      target: "> 4.5/5.0"
  
  reporting:
    frequency: "monthly"
    format: "dashboard"
    recipients:
      - team-leads
      - executives
```

### Performance Improvement Plans

Creating improvement plans for teams:

```yaml
# teams/performance/improvement-plan.yaml
improvement_plan:
  team: "Backend Engineering"
  period: "Q1 2026"
  identified_issues:
    - "Low deployment frequency (2 deployments/week vs target of 5)"
    - "High defect rate in production (3 defects/story vs target of <1)"
    - "Long code review times (avg 2 days vs target of <1 day)"
  
  root_causes:
    - "Insufficient automated testing coverage"
    - "Complex code review process"
    - "Lack of deployment automation"
  
  improvement_actions:
    - action: "Implement comprehensive test automation"
      owner: "QA Lead"
      timeline: "6 weeks"
      success_criteria: "Test coverage > 80%"
    
    - action: "Simplify code review process"
      owner: "Engineering Lead"
      timeline: "4 weeks"
      success_criteria: "Avg review time < 1 day"
    
    - action: "Enhance deployment automation"
      owner: "DevOps Lead"
      timeline: "8 weeks"
      success_criteria: "Deployment frequency > 5/week"
  
  tracking:
    frequency: "weekly"
    metrics:
      - deployment_frequency
      - defect_rate
      - code_review_time
```

## Team Knowledge Management

### Knowledge Sharing Workflows

Facilitating knowledge sharing across teams:

```yaml
# .workflows/knowledge-sharing/tech-talks.yaml
workflow:
  name: "Technical Talks"
  description: "Regular technical knowledge sharing sessions"
  type: "recurring-event"
  frequency: "bi-weekly"
  duration: "1 hour"
  
  participants:
    - all-engineering-teams
    - interested-product-members
    - interested-data-members
  
  steps:
    - name: "Topic Selection"
      description: "Select topic for upcoming talk"
      responsible: "knowledge-coordinator"
      timeline: "1 week before"
    
    - name: "Speaker Preparation"
      description: "Prepare presentation materials"
      responsible: "speaker"
      timeline: "ongoing"
    
    - name: "Session Delivery"
      description: "Deliver technical talk"
      responsible: "speaker"
      duration: "45 minutes"
    
    - name: "Q&A and Discussion"
      description: "Interactive discussion and questions"
      responsible: "all-participants"
      duration: "15 minutes"
    
    - name: "Recording and Documentation"
      description: "Record session and create documentation"
      responsible: "knowledge-coordinator"
      timeline: "1 day after"

  artifacts:
    - presentation-slides
    - session-recording
    - key-takeaways-document
    - follow-up-action-items

  success_criteria:
    - Session is well-attended
    - Valuable knowledge is shared
    - Follow-up actions are tracked
```

### Documentation Standards

Ensuring consistent documentation across teams:

```yaml
# teams/documentation/standards.yaml
documentation:
  standards:
    - name: "Document Structure"
      description: "Standard structure for all documents"
      template:
        - title
        - overview
        - table-of-contents
        - main-content
        - references
        - revision-history
    
    - name: "Version Control"
      description: "All documents must be in version control"
      requirements:
        - stored-in-git
        - clear-commit-messages
        - regular-updates
    
    - name: "Review Process"
      description: "Documents must undergo review process"
      requirements:
        - peer-review
        - subject-matter-expert-review
        - approval-before-publishing
    
    - name: "Accessibility"
      description: "Documents must be accessible"
      requirements:
        - alt-text-for-images
        - clear-structure
        - readable-fonts

  team_responsibilities:
    - engineering: "Technical documentation"
    - product: "Product requirements and user guides"
    - design: "Design specifications and guidelines"
    - data: "Data documentation and analysis reports"
```

## Team Onboarding and Offboarding

### Onboarding Process

Standardized onboarding for new team members:

```yaml
# teams/onboarding/engineering.yaml
onboarding:
  team: "Engineering"
  duration: "4 weeks"
  
  week_1:
    - task: "Environment Setup"
      description: "Set up development environment"
      owner: "DevOps Team"
      duration: "3 days"
    
    - task: "Codebase Introduction"
      description: "Walkthrough of codebase structure"
      owner: "Team Lead"
      duration: "1 day"
    
    - task: "Tool Training"
      description: "Training on team tools and processes"
      owner: "Team Members"
      duration: "1 day"
  
  week_2:
    - task: "First Feature Assignment"
      description: "Small feature to get familiar with workflow"
      owner: "Team Lead"
      duration: "5 days"
    
    - task: "Code Review Participation"
      description: "Participate in code reviews"
      owner: "Senior Developers"
      duration: "ongoing"
  
  week_3:
    - task: "Cross-Team Introduction"
      description: "Meet with other teams and understand dependencies"
      owner: "Team Lead"
      duration: "2 days"
    
    - task: "Advanced Feature Work"
      description: "Work on more complex features"
      owner: "Team Members"
      duration: "3 days"
  
  week_4:
    - task: "Independent Work"
      description: "Work independently with check-ins"
      owner: "New Hire"
      duration: "5 days"
    
    - task: "Onboarding Review"
      description: "Review onboarding experience and gather feedback"
      owner: "HR and Team Lead"
      duration: "1 day"

  success_criteria:
    - Development environment is fully functional
    - New hire can contribute to team goals
    - New hire understands team processes and workflows
    - New hire has established relationships with team members
```

### Offboarding Process

Structured offboarding when team members leave:

```yaml
# teams/offboarding/engineering.yaml
offboarding:
  team: "Engineering"
  duration: "1 week"
  
  tasks:
    - task: "Knowledge Transfer"
      description: "Transfer knowledge to remaining team members"
      owner: "Departing Employee"
      timeline: "first 3 days"
    
    - task: "Code Review and Documentation"
      description: "Ensure code is well-documented and reviewed"
      owner: "Team Members"
      timeline: "first 3 days"
    
    - task: "Access Revocation"
      description: "Revoke all system and tool access"
      owner: "IT Department"
      timeline: "last day"
    
    - task: "Project Update"
      description: "Update project documentation with departure"
      owner: "Team Lead"
      timeline: "last day"
    
    - task: "Exit Interview"
      description: "Conduct exit interview to gather feedback"
      owner: "HR"
      timeline: "last day"

  artifacts:
    - knowledge-transfer-document
    - updated-project-documentation
    - access-revocation-confirmation
    - exit-interview-notes
```

This comprehensive multi-team and workflow support system provides the structure and tools needed for complex projects with multiple teams, ensuring effective collaboration, clear communication, and efficient workflow management.