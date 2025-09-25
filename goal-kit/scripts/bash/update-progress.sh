#!/bin/bash

# Goal-Kit Progress Update Script
# Updates goal progress and generates reports

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOAL_KIT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Utility functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Help function
show_help() {
    cat << EOF
Goal-Kit Progress Update Script

USAGE:
    $0 [OPTIONS] GOAL_PATH

OPTIONS:
    -p, --progress PERCENT     Overall progress percentage (0-100)
    -s, --status STATUS        Progress status (not_started, in_progress, on_track, behind, ahead, completed)
    -m, --metrics KEY:VALUE    Progress metrics (can be used multiple times)
    -n, --notes NOTES          Progress notes
    -r, --report FORMAT        Generate report in specified format (json, markdown, html)
    -e, --evidence FILE        Add evidence file
    -v, --verbose              Verbose output
    -h, --help                 Show this help message

EXAMPLES:
    $0 ./my-goal -p 75 -s on_track -m "tasks_completed:45,total_tasks:60"
    $0 ./my-goal --progress 90 --status ahead --report markdown
    $0 ./my-goal --metrics "accuracy:94%" --notes "Model performance improved significantly"

EOF
}

# Validate dependencies
check_dependencies() {
    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed"
        exit 1
    fi

    if ! command -v git &> /dev/null; then
        log_warning "git not found - version control features will be limited"
    fi
}

# Validate input
validate_input() {
    local goal_path="$1"
    local progress="$2"
    local status="$3"

    if [ -z "$goal_path" ]; then
        log_error "Goal path is required"
        show_help
        exit 1
    fi

    if [ ! -d "$goal_path" ]; then
        log_error "Goal directory does not exist: $goal_path"
        exit 1
    fi

    local goal_file="$goal_path/goal.json"
    if [ ! -f "$goal_file" ]; then
        log_error "Goal file not found: $goal_file"
        exit 1
    fi

    # Validate progress percentage
    if [ -n "$progress" ]; then
        if ! [[ "$progress" =~ ^[0-9]+$ ]] || [ "$progress" -lt 0 ] || [ "$progress" -gt 100 ]; then
            log_error "Progress must be a number between 0 and 100"
            exit 1
        fi
    fi

    # Validate status
    if [ -n "$status" ]; then
        local valid_statuses=("not_started" "in_progress" "on_track" "behind" "ahead" "completed" "at_risk")
        if [[ ! " ${valid_statuses[*]} " =~ " ${status} " ]]; then
            log_error "Invalid status. Valid options: ${valid_statuses[*]}"
            exit 1
        fi
    fi
}

# Parse command line arguments
parse_arguments() {
    GOAL_PATH=""
    PROGRESS=""
    STATUS=""
    METRICS=()
    NOTES=""
    REPORT_FORMAT=""
    EVIDENCE_FILE=""
    VERBOSE=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            -p|--progress)
                PROGRESS="$2"
                shift 2
                ;;
            -s|--status)
                STATUS="$2"
                shift 2
                ;;
            -m|--metrics)
                METRICS+=("$2")
                shift 2
                ;;
            -n|--notes)
                NOTES="$2"
                shift 2
                ;;
            -r|--report)
                REPORT_FORMAT="$2"
                shift 2
                ;;
            -e|--evidence)
                EVIDENCE_FILE="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            -*)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                if [ -z "$GOAL_PATH" ]; then
                    GOAL_PATH="$1"
                else
                    log_error "Multiple goal paths specified. Please provide only one goal path."
                    show_help
                    exit 1
                fi
                shift
                ;;
        esac
    done
}

# Backup goal file
backup_goal_file() {
    local goal_file="$1"
    local backup_file="${goal_file}.backup.$(date +%Y%m%d_%H%M%S)"

    cp "$goal_file" "$backup_file"
    if [ "$VERBOSE" = true ]; then
        log_info "Created backup: $backup_file"
    fi
}

# Update goal progress
update_goal_progress() {
    local goal_file="$1"
    local progress="$2"
    local status="$3"
    local metrics="$4"
    local notes="$5"

    log_info "Updating goal progress..."

    # Read current goal file
    local goal_content=$(cat "$goal_file")

    # Update progress and status
    if [ -n "$progress" ]; then
        goal_content=$(echo "$goal_content" | jq ".progress = $progress")
    fi

    if [ -n "$status" ]; then
        goal_content=$(echo "$goal_content" | jq ".status = \"$status\"")
    fi

    # Add metrics to metadata if provided
    if [ -n "$metrics" ]; then
        local metrics_obj="{"
        for metric in "${METRICS[@]}"; do
            local key=$(echo "$metric" | cut -d: -f1)
            local value=$(echo "$metric" | cut -d: -f2-)
            metrics_obj="${metrics_obj}\"$key\":\"$value\","
        done
        metrics_obj="${metrics_obj%?}}"  # Remove trailing comma

        goal_content=$(echo "$goal_content" | jq ".metadata.last_metrics = $metrics_obj")
    fi

    # Update last modified timestamp
    local updated_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    goal_content=$(echo "$goal_content" | jq ".updated_at = \"$updated_at\"")

    # Write back to file
    echo "$goal_content" > "$goal_file"

    if [ "$VERBOSE" = true ]; then
        log_success "Updated goal file: $goal_file"
    fi
}

# Create progress entry
create_progress_entry() {
    local goal_path="$1"
    local progress="$2"
    local status="$3"
    local notes="$4"
    local progress_dir="$goal_path/progress"

    # Ensure progress directory exists
    mkdir -p "$progress_dir"

    # Create progress entry
    local timestamp=$(date -u +"%Y-%m-%dT%H-%M-%SZ")
    local progress_file="$progress_dir/progress-${timestamp}.json"

    local progress_entry=$(cat << EOF
{
  "timestamp": "$timestamp",
  "progress": $progress,
  "status": "$status",
  "notes": "$notes",
  "metrics": {
EOF
)

    # Add metrics
    for metric in "${METRICS[@]}"; do
        local key=$(echo "$metric" | cut -d: -f1)
        local value=$(echo "$metric" | cut -d: -f2-)
        progress_entry="${progress_entry}\n    \"$key\": \"$value\","
    done

    progress_entry="${progress_entry%,}\n  }"
    progress_entry="${progress_entry}\n}"

    echo -e "$progress_entry" > "$progress_file"

    if [ "$VERBOSE" = true ]; then
        log_success "Created progress entry: $progress_file"
    fi
}

# Add evidence file
add_evidence() {
    local goal_path="$1"
    local evidence_file="$2"
    local evidence_dir="$goal_path/achievements"

    if [ ! -f "$evidence_file" ]; then
        log_error "Evidence file not found: $evidence_file"
        return 1
    fi

    # Ensure evidence directory exists
    mkdir -p "$evidence_dir"

    # Copy evidence file
    local filename=$(basename "$evidence_file")
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local new_filename="${timestamp}_${filename}"
    local evidence_path="$evidence_dir/$new_filename"

    cp "$evidence_file" "$evidence_path"

    if [ "$VERBOSE" = true ]; then
        log_success "Added evidence: $evidence_path"
    fi

    return 0
}

# Generate progress report
generate_report() {
    local goal_path="$1"
    local format="$2"
    local goal_file="$goal_path/goal.json"
    local report_dir="$goal_path/progress"

    log_info "Generating progress report ($format format)..."

    # Ensure report directory exists
    mkdir -p "$report_dir"

    # Create report filename
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local report_file="$report_dir/progress-report-${timestamp}.$format"

    # Read goal data
    local goal_content=$(cat "$goal_file")
    local goal_name=$(echo "$goal_content" | jq -r '.name')
    local progress=$(echo "$goal_content" | jq -r '.progress')
    local status=$(echo "$goal_content" | jq -r '.status')
    local category=$(echo "$goal_content" | jq -r '.category')
    local priority=$(echo "$goal_content" | jq -r '.priority')

    case "$format" in
        json)
            # JSON report
            local report_data=$(cat << EOF
{
  "report_type": "progress",
  "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "goal": {
    "name": "$goal_name",
    "progress": $progress,
    "status": "$status",
    "category": "$category",
    "priority": "$priority"
  },
  "metrics": {
EOF
)

            # Add current metrics
            if [ ${#METRICS[@]} -gt 0 ]; then
                for metric in "${METRICS[@]}"; do
                    local key=$(echo "$metric" | cut -d: -f1)
                    local value=$(echo "$metric" | cut -d: -f2-)
                    report_data="${report_data}\n    \"$key\": \"$value\","
                done
                report_data="${report_data%,}"
            fi

            report_data="${report_data}\n  }"
            report_data="${report_data}\n}"

            echo -e "$report_data" > "$report_file"
            ;;

        markdown)
            # Markdown report
            local report_content=$(cat << EOF
# Progress Report: $goal_name

## Overview
- **Goal:** $goal_name
- **Progress:** $progress%
- **Status:** $status
- **Category:** $category
- **Priority:** $priority
- **Report Generated:** $(date +%Y-%m-%d %H:%M:%S UTC)

## Current Metrics
EOF
)

            if [ ${#METRICS[@]} -gt 0 ]; then
                report_content="${report_content}\n| Metric | Value |\n|--------|--------|\n"
                for metric in "${METRICS[@]}"; do
                    local key=$(echo "$metric" | cut -d: -f1)
                    local value=$(echo "$metric" | cut -d: -f2-)
                    report_content="${report_content}| $key | $value |\n"
                done
            fi

            if [ -n "$NOTES" ]; then
                report_content="${report_content}\n## Notes\n$NOTES\n"
            fi

            echo -e "$report_content" > "$report_file"
            ;;

        html)
            # HTML report
            local report_content=$(cat << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Progress Report: $goal_name</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { color: #333; border-bottom: 2px solid #007acc; }
        .metrics { background: #f5f5f5; padding: 20px; border-radius: 5px; }
        .metric { display: inline-block; margin: 10px; padding: 10px; background: white; border-radius: 3px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Progress Report: $goal_name</h1>
        <p><strong>Generated:</strong> $(date +%Y-%m-%d %H:%M:%S UTC)</p>
    </div>

    <h2>Goal Overview</h2>
    <ul>
        <li><strong>Progress:</strong> $progress%</li>
        <li><strong>Status:</strong> $status</li>
        <li><strong>Category:</strong> $category</li>
        <li><strong>Priority:</strong> $priority</li>
    </ul>

    <h2>Current Metrics</h2>
    <div class="metrics">
EOF
)

            if [ ${#METRICS[@]} -gt 0 ]; then
                report_content="${report_content}\n        <table>\n            <tr><th>Metric</th><th>Value</th></tr>\n"
                for metric in "${METRICS[@]}"; do
                    local key=$(echo "$metric" | cut -d: -f1)
                    local value=$(echo "$metric" | cut -d: -f2-)
                    report_content="${report_content}            <tr><td>$key</td><td>$value</td></tr>\n"
                done
                report_content="${report_content}        </table>\n"
            fi

            if [ -n "$NOTES" ]; then
                report_content="${report_content}\n    <h2>Notes</h2>\n    <p>$NOTES</p>\n"
            fi

            report_content="${report_content}</div>\n</body>\n</html>"

            echo -e "$report_content" > "$report_file"
            ;;
    esac

    log_success "Generated report: $report_file"
}

# Commit changes to git
commit_changes() {
    local goal_path="$1"

    if command -v git &> /dev/null && [ -d "$goal_path/.git" ]; then
        cd "$goal_path"

        # Check if there are changes to commit
        if git diff --quiet && git diff --staged --quiet; then
            log_info "No changes to commit"
            return 0
        fi

        # Add all changes
        git add .

        # Create commit message
        local commit_msg="Update progress: "
        if [ -n "$PROGRESS" ]; then
            commit_msg="${commit_msg}Progress $PROGRESS%. "
        fi
        if [ -n "$STATUS" ]; then
            commit_msg="${commit_msg}Status: $STATUS. "
        fi
        commit_msg="${commit_msg}($(date +%Y-%m-%d %H:%M))"

        # Commit changes
        git commit -m "$commit_msg" --quiet

        if [ "$VERBOSE" = true ]; then
            log_success "Committed changes to git"
        fi
    fi
}

# Main execution
main() {
    log_info "Goal-Kit Progress Update Script v1.0"
    log_info "==================================="

    # Parse arguments
    parse_arguments "$@"

    # Check dependencies
    check_dependencies

    # Validate input
    validate_input "$GOAL_PATH" "$PROGRESS" "$STATUS"

    # Backup goal file
    local goal_file="$GOAL_PATH/goal.json"
    backup_goal_file "$goal_file"

    # Update goal progress
    if [ -n "$PROGRESS" ] || [ -n "$STATUS" ] || [ ${#METRICS[@]} -gt 0 ]; then
        update_goal_progress "$goal_file" "$PROGRESS" "$STATUS" "$METRICS" "$NOTES"
    fi

    # Create progress entry
    if [ -n "$PROGRESS" ] || [ -n "$STATUS" ] || [ ${#METRICS[@]} -gt 0 ] || [ -n "$NOTES" ]; then
        create_progress_entry "$GOAL_PATH" "$PROGRESS" "$STATUS" "$NOTES"
    fi

    # Add evidence if provided
    if [ -n "$EVIDENCE_FILE" ]; then
        add_evidence "$GOAL_PATH" "$EVIDENCE_FILE"
    fi

    # Generate report if requested
    if [ -n "$REPORT_FORMAT" ]; then
        generate_report "$GOAL_PATH" "$REPORT_FORMAT"
    fi

    # Commit changes
    commit_changes "$GOAL_PATH"

    # Success message
    log_success "Progress update completed successfully!"

    if [ -n "$REPORT_FORMAT" ]; then
        log_info "Report generated in $REPORT_FORMAT format"
    fi

    log_info "Keep up the great work! 🎯"
}

# Run main function with all arguments
main "$@"