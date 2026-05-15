#!/bin/bash
# Generate portfolio overview in a Goal Kit project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
source "$SCRIPT_DIR/common.sh"

generate_portfolio_file() {
    local dry_run=false
    local force=false
    local json_mode=false
    # shellcheck disable=SC2034
    local verbose=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run) dry_run=true; shift ;;
            --force) force=true; shift ;;
            --json) json_mode=true; shift ;;
            # shellcheck disable=SC2034
            --verbose) verbose=true; shift ;;
            *) handle_error "Unknown option: $1" ;;
        esac
    done

    if ! test_git_repo; then
        handle_error "Not in a git repository. Please run this from the root of a Goal Kit project"
    fi

    local project_root
    project_root=$(get_git_root) || handle_error "Could not determine git root"
    if [ -z "$project_root" ]; then
        handle_error "Could not determine git root. Not in a git repository."
    fi

    cd "$project_root" || handle_error "Failed to change to project root: $project_root"

    if [ "$json_mode" = true ]; then
        local portfolio_file=".goalkit/portfolio.md"
        local goals_dir=".goalkit/goals"

        cat <<EOF
{"PORTFOLIO_FILE":"$portfolio_file","GOALS_DIR":"$goals_dir"}
EOF
        return
    fi

    local portfolio_file=".goalkit/portfolio.md"
    if [ -f "$portfolio_file" ] && [ "$dry_run" = false ]; then
        write_warning "Portfolio file already exists: $portfolio_file"
        if [ "$force" = false ]; then
            read -p "Overwrite existing portfolio file? (y/N): " -r
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                write_info "Operation cancelled"
                return
            fi
        fi
    fi

    if [ "$dry_run" = true ]; then
        write_info "[DRY RUN] Would create portfolio file: $portfolio_file"
        return
    fi

    local timestamp
    timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')

    # Scan for active goals
    local goals_dir=".goalkit/goals"
    local goal_count=0
    local on_track=0
    local at_risk=0
    local completed=0
    local goal_list=""

    if [ -d "$goals_dir" ]; then
        for goal_dir in "$goals_dir"/*/; do
            if [ -d "$goal_dir" ] && [ -f "$goal_dir/goal.md" ]; then
                goal_count=$((goal_count + 1))
                local goal_name
                goal_name=$(basename "$goal_dir")
                goal_list="$goal_list- $goal_name\n"
                on_track=$((on_track + 1))
            fi
        done
    fi

    cat > "$portfolio_file" <<EOF || handle_error "Failed to write portfolio file: $portfolio_file"
# Portfolio Overview

**Generated**: $timestamp
**Total Goals**: $goal_count
**On Track**: $on_track | **At Risk**: $at_risk | **Completed**: $completed

## Executive Summary

Portfolio health overview for the current period.

## Active Goals

${goal_list:-No active goals yet. Use /goalkit.goal to create your first goal.}

## Health Metrics
- **Average Completion**: [Calculated from goal files]
- **Average Health Score**: [Calculated from goal files]
- **Velocity**: [Goals completed per month]

## Risks & Opportunities
- **Top Risks**: [Goals at risk and mitigation plans]
- **Opportunities**: [Acceleration opportunities]

## Resource Allocation
- **Team Distribution**: [Goals by team]
- **Over/Under Allocated**: [Resource balance assessment]

## Leadership Actions
- **Decisions Needed**: [What leadership needs to decide]
- **Escalations**: [Items needing attention]
EOF

    write_success "Created portfolio file: $portfolio_file"
    echo
    write_info "Portfolio Details:"
    echo "  Goals Found: $goal_count"
    echo "  Portfolio File: $portfolio_file"
    echo
    write_info "Next Steps:"
    echo "  1. Review the portfolio overview"
    echo "  2. Check goal health and risks"
    echo "  3. Use /goalkit.goal to review specific goals"
    echo "  4. Use /goalkit.report to generate detailed reports"
    echo
}

main() {
    generate_portfolio_file "$@"
}

main "$@"
