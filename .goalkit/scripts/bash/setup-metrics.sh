#!/bin/bash
# Setup metrics planning in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

create_metrics_file() {
    local goal_directory="$1"
    local dry_run=false
    local force=false
    local json_mode=false
    local verbose=false
    
    # Parse remaining arguments
    shift 1
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                dry_run=true
                shift
                ;;
            --force)
                force=true
                shift
                ;;
            --json)
                json_mode=true
                shift
                ;;
            --verbose)
                verbose=true
                shift
                ;;
            *)
                handle_error "Unknown option: $1"
                ;;
        esac
    done
    
    # Check if we're in a git repository
    if ! test_git_repo; then
        handle_error "Not in a git repository. Please run this from the root of a Goal Kit project"
    fi
    
    # Get project root
    local project_root
    project_root=$(get_git_root) || handle_error "Could not determine git root"
    if [ -z "$project_root" ]; then
        handle_error "Could not determine git root. Not in a git repository."
    fi
    
    cd "$project_root" || handle_error "Failed to change to project root: $project_root"
    
    if [ "$json_mode" = true ]; then
        if [ ! -d "$goal_directory" ]; then
            handle_error "Goal directory does not exist: $goal_directory"
        fi
        
        local goal_dir_name=$(basename "$goal_directory")
        local metrics_file="$goal_directory/metrics.md"
        local branch_name="$goal_dir_name"
        
        # Output JSON with required variables
        cat <<EOF
{"GOAL_DIR":"$goal_directory","METRICS_FILE":"$metrics_file","BRANCH_NAME":"$branch_name"}
EOF
        return
    fi
    
    # Verify goal directory exists
    if [ ! -d "$goal_directory" ]; then
        handle_error "Goal directory does not exist: $goal_directory"
    fi
    
    # Check if metrics.md already exists
    local metrics_file="$goal_directory/metrics.md"
    if [ -f "$metrics_file" ] && [ "$dry_run" = false ]; then
        write_warning "Metrics file already exists: $metrics_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing metrics file? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi
    
    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create metrics file: $metrics_file"
        return
    fi
    
    # Create metrics file with basic template
    local goal_dir_name=$(basename "$goal_directory")
    
    cat > "$metrics_file" <<EOF || handle_error "Failed to write metrics file: $metrics_file"
# Metrics Plan for $goal_dir_name

## Overview
Metrics and measurement plan for goal: $goal_dir_name

## Success Criteria Review
Extract success criteria from goal.md and validate metric quality.

| Metric ID | Description | Target | Timeframe | Quality Score |
|-----------|-------------|--------|-----------|---------------|
| SC-001 | [Metric description] | [Target value] | [By when] | [See checklist below] |
| SC-002 | [Metric description] | [Target value] | [By when] | [See checklist below] |
| SC-003 | [Metric description] | [Target value] | [By when] | [See checklist below] |

## Metric Quality Validation

For each success criterion, validate against quality checklist:

### SC-001: [Metric Name]

**Metric Description**: [Full description of what's being measured]

#### Quality Checklist
- [ ] **Measurable**: Can we collect this data reliably and objectively?
  - *How measured*: [Specific measurement method]
  - *Data source*: [Where data comes from]
  - *Frequency*: [How often measured]

- [ ] **Actionable**: Will this metric drive specific decisions?
  - *Green zone (≥ target)*: [What action to take]
  - *Yellow zone (near target)*: [What action to take]
  - *Red zone (< threshold)*: [What action to take]

- [ ] **Leading**: Does it predict future success (not just lag)?
  - *Leading indicator*: [Yes/No - explain]
  - *Lag time*: [How long until impact visible]

- [ ] **Bounded**: Is there a clear target and timeframe?
  - *Target*: [Specific number/percentage]
  - *Baseline*: [Current state]
  - *Deadline*: [When to achieve by]

- [ ] **Valuable**: Does it connect to user/business outcomes?
  - *User value*: [How this helps users]
  - *Business value*: [How this helps business]
  - *Alignment*: [Links to vision scenario]

**Quality Score**: [Pass/Needs Improvement/Fail]

**Issues to address**: [Any quality gaps to fix]

## Baseline Measurements

Establish current state before starting work.

| Metric | Current Baseline | Measurement Date | Measurement Method | Notes |
|--------|------------------|------------------|-------------------|-------|
| SC-001 | [Current value] | [Date measured] | [How measured] | [Context] |
| SC-002 | [Current value] | [Date measured] | [How measured] | [Context] |
| SC-003 | [Current value] | [Date measured] | [How measured] | [Context] |

**Baseline validation**:
- [ ] Baselines measured using same method as target measurement
- [ ] Baselines represent typical state (not outliers)
- [ ] Baselines documented with context (time period, conditions)

## Instrumentation Plan

Define how to collect data for each metric.

### SC-001: [Metric Name]

**What to instrument**:
- [Specific events to track]
- [User behaviors to log]
- [System metrics to capture]

**How to collect**:
- **Tool/Platform**: [Analytics tool, logging system, database query]
- **Implementation**: [Code changes needed, tracking setup]
- **Storage**: [Where data is stored]

**When to measure**:
- **Frequency**: [Real-time, daily, weekly]
- **Triggers**: [Events that trigger measurement]
- **Duration**: [How long to collect data]

**Who analyzes**:
- **Responsible person**: [Name/role]
- **Review frequency**: [How often to review]
- **Reporting format**: [Dashboard, report, alert]

**Validation**:
- [ ] Instrumentation tested and working
- [ ] Data collection verified accurate
- [ ] Dashboard/reporting set up

## Decision Thresholds

Define what actions to take based on metric values.

### SC-001: [Metric Name]

| Zone | Threshold | Status | Action |
|------|-----------|--------|--------|
| 🟢 **Green (Success)** | ≥ [target] | Goal met | Scale feature, celebrate, document success |
| 🟡 **Yellow (Warning)** | [X] to [Y] | Needs attention | Investigate root cause, adjust tactics |
| 🔴 **Red (Failure)** | < [threshold] | Goal at risk | Pivot strategy, escalate, consider alternatives |

**Pivot triggers**:
- If metric stays in red zone for [duration] → [specific action]
- If metric trends downward for [duration] → [specific action]

## Measurement Dashboard

Define how metrics will be visualized and monitored.

### Dashboard Design

**Tool/Platform**: [Grafana, Metabase, Tableau, Google Analytics, Custom]

**Dashboard sections**:
1. **Overview**: All metrics at-a-glance with status indicators
2. **Trends**: Time-series charts showing metric evolution
3. **Breakdowns**: Segmentation by user type, platform, etc.
4. **Alerts**: Notifications when metrics cross thresholds

**Access**:
- **Who can view**: [Team members, stakeholders]
- **Update frequency**: [Real-time, hourly, daily]
- **Link**: [URL to dashboard when created]

## Metric Types Classification

Categorize metrics to ensure balanced measurement.

### User Behavior Metrics
Metrics that measure how users actually use the feature:
- **[Metric ID]**: [Description]

### Business Impact Metrics
Metrics that measure business value delivered:
- **[Metric ID]**: [Description]

### Technical Quality Metrics
Metrics that measure system performance/reliability:
- **[Metric ID]**: [Description]

### Learning Metrics
Metrics that measure what we discovered/capabilities built:
- **[Metric ID]**: [Description]

**Balance check**:
- [ ] At least one user behavior metric
- [ ] At least one business impact metric
- [ ] Technical metrics support user/business metrics
- [ ] Learning objectives defined

## Success Criteria

This measurement plan is ready when:

- [ ] All metrics pass quality validation checklist
- [ ] Baselines measured and documented
- [ ] Instrumentation implemented and tested
- [ ] Dashboard created and accessible
- [ ] Decision thresholds defined and agreed
- [ ] Review schedule established
- [ ] Team trained on metric interpretation
EOF
    
    write_success "Created metrics file: $metrics_file"
    
    # Print summary
    write_success "Metrics planning setup completed!"
    echo
    write_info "Metrics Details:"
    echo "  Goal Directory: $goal_directory"
    echo "  Metrics File: $metrics_file"
    echo
    
    write_info "Next Steps:"
    echo "  1. Extract success criteria from goal.md"
    echo "  2. Validate each metric against quality checklist"
    echo "  3. Define instrumentation and measurement methods"
    echo "  4. Set up baseline measurements before implementation"
    echo "  5. Use /goalkit.strategies to explore implementation approaches"
    
    # Setup goal environment for immediate development
    if ! set_goal_environment "$goal_directory"; then
        handle_error "Failed to setup goal environment for $goal_directory"
    fi
}

# Main entry point
main() {
    if [ $# -lt 1 ]; then
        handle_error "Goal directory is required. Usage: $0 <goal_directory> [--dry-run] [--force] [--json] [--verbose]"
    fi
    
    create_metrics_file "$@"
}

main "$@"
