#!/bin/bash

# Goal-Kit Report Generation Script
# Generates comprehensive progress reports for goals

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
Goal-Kit Report Generation Script

USAGE:
    $0 [OPTIONS] GOAL_PATH

OPTIONS:
    -f, --format FORMAT        Report format (json, markdown, html, pdf)
    -t, --type TYPE            Report type (summary, detailed, milestone, achievement)
    -p, --period PERIOD        Reporting period (daily, weekly, monthly, quarterly, all)
    -o, --output FILE          Output file path (default: auto-generated)
    -i, --include-evidence     Include evidence files in report
    -m, --include-metrics      Include detailed metrics
    -c, --charts               Generate charts and visualizations
    -v, --verbose              Verbose output
    -h, --help                 Show this help message

REPORT TYPES:
    summary       - High-level overview with key metrics
    detailed      - Comprehensive report with full details
    milestone     - Focus on milestone progress
    achievement   - Focus on achievement tracking

EXAMPLES:
    $0 ./my-goal -f markdown -t detailed
    $0 ./my-goal --format html --type summary --include-metrics
    $0 ./my-goal -f json -p monthly -o ./reports/monthly-report.json

EOF
}

# Validate dependencies
check_dependencies() {
    local missing_deps=()

    if ! command -v jq &> /dev/null; then
        missing_deps+=("jq")
    fi

    if ! command -v git &> /dev/null; then
        log_warning "git not found - version control info will be limited"
    fi

    # Optional dependencies for PDF generation
    if [ "$FORMAT" = "pdf" ]; then
        if ! command -v pandoc &> /dev/null; then
            log_warning "pandoc not found - PDF generation will be limited"
        fi
        if ! command -v wkhtmltopdf &> /dev/null; then
            log_warning "wkhtmltopdf not found - PDF generation will be limited"
        fi
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Please install the missing dependencies and try again."
        exit 1
    fi
}

# Parse command line arguments
parse_arguments() {
    GOAL_PATH=""
    FORMAT="markdown"
    REPORT_TYPE="detailed"
    PERIOD="all"
    OUTPUT_FILE=""
    INCLUDE_EVIDENCE=false
    INCLUDE_METRICS=false
    GENERATE_CHARTS=false
    VERBOSE=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            -f|--format)
                FORMAT="$2"
                shift 2
                ;;
            -t|--type)
                REPORT_TYPE="$2"
                shift 2
                ;;
            -p|--period)
                PERIOD="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_FILE="$2"
                shift 2
                ;;
            -i|--include-evidence)
                INCLUDE_EVIDENCE=true
                shift
                ;;
            -m|--include-metrics)
                INCLUDE_METRICS=true
                shift
                ;;
            -c|--charts)
                GENERATE_CHARTS=true
                shift
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

    # Validate format
    local valid_formats=("json" "markdown" "html" "pdf")
    if [[ ! " ${valid_formats[*]} " =~ " ${FORMAT} " ]]; then
        log_error "Invalid format. Valid options: ${valid_formats[*]}"
        exit 1
    fi

    # Validate report type
    local valid_types=("summary" "detailed" "milestone" "achievement")
    if [[ ! " ${valid_types[*]} " =~ " ${REPORT_TYPE} " ]]; then
        log_error "Invalid report type. Valid options: ${valid_types[*]}"
        exit 1
    fi

    # Validate period
    local valid_periods=("daily" "weekly" "monthly" "quarterly" "all")
    if [[ ! " ${valid_periods[*]} " =~ " ${PERIOD} " ]]; then
        log_error "Invalid period. Valid options: ${valid_periods[*]}"
        exit 1
    fi
}

# Generate output filename if not provided
generate_output_filename() {
    local goal_path="$1"
    local format="$2"
    local report_type="$3"
    local period="$4"

    local goal_name=$(basename "$goal_path")
    local timestamp=$(date +%Y%m%d_%H%M%S)

    if [ -z "$OUTPUT_FILE" ]; then
        OUTPUT_FILE="$goal_path/reports/${report_type}-report-${timestamp}.$format"
    fi

    # Ensure output directory exists
    local output_dir=$(dirname "$OUTPUT_FILE")
    mkdir -p "$output_dir"

    if [ "$VERBOSE" = true ]; then
        log_info "Output file: $OUTPUT_FILE"
    fi
}

# Read goal data
read_goal_data() {
    local goal_file="$1"
    local goal_content=$(cat "$goal_file")

    # Extract basic goal information
    GOAL_NAME=$(echo "$goal_content" | jq -r '.name')
    GOAL_ID=$(echo "$goal_content" | jq -r '.metadata.template // "unknown"')
    PROGRESS=$(echo "$goal_content" | jq -r '.progress')
    STATUS=$(echo "$goal_content" | jq -r '.status')
    CATEGORY=$(echo "$goal_content" | jq -r '.category')
    PRIORITY=$(echo "$goal_content" | jq -r '.priority')
    CREATED_AT=$(echo "$goal_content" | jq -r '.created_at')
    UPDATED_AT=$(echo "$goal_content" | jq -r '.updated_at // .created_at')

    # Calculate duration
    local created_timestamp=$(date -d "$CREATED_AT" +%s)
    local current_timestamp=$(date +%s)
    local duration_days=$(( (current_timestamp - created_timestamp) / 86400 ))

    if [ "$VERBOSE" = true ]; then
        log_info "Read goal data: $GOAL_NAME ($PROGRESS% complete)"
    fi
}

# Collect progress data
collect_progress_data() {
    local goal_path="$1"
    local period="$2"
    local progress_dir="$goal_path/progress"

    PROGRESS_ENTRIES=()
    MILESTONE_COUNT=0
    ACHIEVEMENT_COUNT=0

    if [ -d "$progress_dir" ]; then
        # Find progress files based on period
        local date_filter=""
        case "$period" in
            daily)
                date_filter=$(date +%Y-%m-%d)
                ;;
            weekly)
                local week_start=$(date -d "last monday" +%Y-%m-%d)
                date_filter="$week_start"
                ;;
            monthly)
                date_filter=$(date +%Y-%m-01)
                ;;
            quarterly)
                local quarter_start_month=$(( (($(date +%-m) - 1) / 3) * 3 + 1 ))
                date_filter=$(date +%Y-${quarter_start_month}-01)
                ;;
            all)
                date_filter=""
                ;;
        esac

        if [ -n "$date_filter" ]; then
            PROGRESS_ENTRIES=($(find "$progress_dir" -name "*.json" -exec grep -l "\"$date_filter" {} \; 2>/dev/null || true))
        else
            PROGRESS_ENTRIES=($(find "$progress_dir" -name "*.json" | sort))
        fi
    fi

    # Count milestones and achievements
    if [ -d "$goal_path/milestones" ]; then
        MILESTONE_COUNT=$(find "$goal_path/milestones" -name "*.json" | wc -l)
    fi

    if [ -d "$goal_path/achievements" ]; then
        ACHIEVEMENT_COUNT=$(find "$goal_path/achievements" -name "*.json" | wc -l)
    fi

    if [ "$VERBOSE" = true ]; then
        log_info "Found ${#PROGRESS_ENTRIES[@]} progress entries, $MILESTONE_COUNT milestones, $ACHIEVEMENT_COUNT achievements"
    fi
}

# Generate JSON report
generate_json_report() {
    local goal_path="$1"
    local output_file="$2"

    log_info "Generating JSON report..."

    # Build JSON structure
    local report_data="{
  \"report_metadata\": {
    \"type\": \"$REPORT_TYPE\",
    \"format\": \"json\",
    \"generated_at\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",
    \"period\": \"$PERIOD\",
    \"generator\": \"goal-kit-report-generator\"
  },
  \"goal\": {
    \"name\": \"$GOAL_NAME\",
    \"id\": \"$GOAL_ID\",
    \"progress\": $PROGRESS,
    \"status\": \"$STATUS\",
    \"category\": \"$CATEGORY\",
    \"priority\": \"$PRIORITY\",
    \"created_at\": \"$CREATED_AT\",
    \"updated_at\": \"$UPDATED_AT\",
    \"duration_days\": $duration_days
  },
  \"metrics\": {
    \"milestones_count\": $MILESTONE_COUNT,
    \"achievements_count\": $ACHIEVEMENT_COUNT,
    \"progress_entries_count\": ${#PROGRESS_ENTRIES[@]}
  }"

    # Add progress entries if requested
    if [ "$INCLUDE_METRICS" = true ]; then
        report_data="$report_data,
  \"progress_history\": ["
        for entry_file in "${PROGRESS_ENTRIES[@]}"; do
            local entry_content=$(cat "$entry_file")
            report_data="$report_data
    $entry_content,"
        done
        report_data="${report_data%,}
  ]"
    fi

    # Close JSON structure
    report_data="$report_data
}"

    echo "$report_data" > "$output_file"
    log_success "Generated JSON report: $output_file"
}

# Generate Markdown report
generate_markdown_report() {
    local goal_path="$1"
    local output_file="$2"

    log_info "Generating Markdown report..."

    local report_content="# Goal Progress Report: $GOAL_NAME

## Executive Summary
- **Goal:** $GOAL_NAME
- **Progress:** $PROGRESS%
- **Status:** $STATUS
- **Category:** $CATEGORY
- **Priority:** $PRIORITY
- **Report Generated:** $(date +%Y-%m-%d %H:%M:%S UTC)
- **Report Period:** $PERIOD
- **Duration:** $duration_days days

## Progress Overview

### Key Metrics
| Metric | Value |
|--------|-------|
| Progress | $PROGRESS% |
| Milestones | $MILESTONE_COUNT |
| Achievements | $ACHIEVEMENT_COUNT |
| Progress Entries | ${#PROGRESS_ENTRIES[@]} |

### Status Timeline
- **Created:** $(date -d "$CREATED_AT" +"%Y-%m-%d %H:%M UTC")
- **Last Updated:** $(date -d "$UPDATED_AT" +"%H:%M UTC")"

    if [ "$INCLUDE_METRICS" = true ]; then
        report_content="$report_content

## Detailed Progress History

### Recent Progress Entries
"

        # Add recent progress entries
        local recent_count=0
        for entry_file in "${PROGRESS_ENTRIES[@]:0:10}"; do  # Show last 10 entries
            local entry_content=$(cat "$entry_file")
            local timestamp=$(echo "$entry_content" | jq -r '.timestamp')
            local progress=$(echo "$entry_content" | jq -r '.progress')
            local status=$(echo "$entry_content" | jq -r '.status')
            local notes=$(echo "$entry_content" | jq -r '.notes // ""')

            report_content="$report_content
#### $(date -d "$timestamp" +"%Y-%m-%d %H:%M UTC")
- **Progress:** $progress%
- **Status:** $status
$(if [ -n "$notes" ]; then echo "- **Notes:** $notes"; fi)
"
            recent_count=$((recent_count + 1))
        done

        if [ $recent_count -eq 0 ]; then
            report_content="$report_content
*No progress entries found for the selected period.*
"
        fi
    fi

    # Add achievements section if requested
    if [ "$INCLUDE_EVIDENCE" = true ]; then
        report_content="$report_content

## Achievements and Evidence

### Recent Achievements
"

        local achievement_dir="$goal_path/achievements"
        if [ -d "$achievement_dir" ]; then
            local achievement_files=($(find "$achievement_dir" -name "*.json" -o -name "*.md" | head -10))
            if [ ${#achievement_files[@]} -gt 0 ]; then
                for achievement_file in "${achievement_files[@]}"; do
                    local filename=$(basename "$achievement_file")
                    report_content="$report_content
- [$filename]($achievement_file)"
                done
            else
                report_content="$report_content
*No achievements recorded yet.*
"
            fi
        fi
    fi

    # Add milestones section
    if [ "$REPORT_TYPE" = "milestone" ]; then
        report_content="$report_content

## Milestone Progress

### Milestone Status
"

        local milestone_dir="$goal_path/milestones"
        if [ -d "$milestone_dir" ]; then
            local milestone_files=($(find "$milestone_dir" -name "*.json"))
            if [ ${#milestone_files[@]} -gt 0 ]; then
                report_content="$report_content
| Milestone | Status | Progress |
|-----------|--------|----------|
"

                for milestone_file in "${milestone_files[@]}"; do
                    local milestone_content=$(cat "$milestone_file")
                    local name=$(echo "$milestone_content" | jq -r '.name')
                    local status=$(echo "$milestone_content" | jq -r '.status')
                    local progress=$(echo "$milestone_content" | jq -r '.progress // 0')

                    report_content="$report_content| $name | $status | $progress% |
"
                done
            else
                report_content="$report_content
*No milestones defined yet.*
"
            fi
        fi
    fi

    # Add final sections
    report_content="$report_content
## Recommendations

### Next Steps
- Continue regular progress updates
- Review milestone progress regularly
- Celebrate achievements as they are completed
- Adjust goals as needed based on progress

### Success Factors
- Maintain consistent progress tracking
- Regular milestone reviews
- Stakeholder communication
- Adaptability to changing circumstances

## Report Metadata

- **Report Type:** $REPORT_TYPE
- **Generated By:** Goal-Kit Report Generator
- **Version:** 1.0
- **Data Period:** $PERIOD

---
*This report was generated automatically by Goal-Kit. Keep up the great work!*
"

    echo "$report_content" > "$output_file"
    log_success "Generated Markdown report: $output_file"
}

# Generate HTML report
generate_html_report() {
    local goal_path="$1"
    local output_file="$2"

    log_info "Generating HTML report..."

    local report_content="<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Goal Progress Report: $GOAL_NAME</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .header {
            background: linear-gradient(135deg, #007acc, #0056b3);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .metric-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .metric-item {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4caf50, #81c784);
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #007acc;
            color: white;
        }
        .status-$STATUS {
            padding: 4px 8px;
            border-radius: 12px;
            color: white;
            font-size: 0.8em;
            text-transform: uppercase;
        }
        .status-completed { background-color: #4caf50; }
        .status-on_track { background-color: #2196f3; }
        .status-behind { background-color: #ff9800; }
        .status-ahead { background-color: #9c27b0; }
        .status-not_started { background-color: #757575; }
        .status-at_risk { background-color: #f44336; }
        .section {
            margin: 30px 0;
        }
        .section h2 {
            color: #007acc;
            border-bottom: 2px solid #007acc;
            padding-bottom: 10px;
        }
        .evidence-item {
            background: #f5f5f5;
            padding: 10px;
            margin: 5px 0;
            border-left: 4px solid #007acc;
        }
    </style>
</head>
<body>
    <div class=\"header\">
        <h1>Goal Progress Report</h1>
        <h2>$GOAL_NAME</h2>
        <p>Generated on $(date +%Y-%m-%d %H:%M:%S UTC)</p>
    </div>

    <div class=\"metric-grid\">
        <div class=\"metric-item\">
            <h3>Progress</h3>
            <div class=\"progress-bar\">
                <div class=\"progress-fill\" style=\"width: $PROGRESS%\"></div>
            </div>
            <strong>$PROGRESS%</strong>
        </div>
        <div class=\"metric-item\">
            <h3>Status</h3>
            <div class=\"status-$STATUS\">$STATUS</div>
        </div>
        <div class=\"metric-item\">
            <h3>Category</h3>
            <strong>$CATEGORY</strong>
        </div>
        <div class=\"metric-item\">
            <h3>Priority</h3>
            <strong>$PRIORITY</strong>
        </div>
    </div>

    <div class=\"section\">
        <h2>Goal Information</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Goal Name</td><td>$GOAL_NAME</td></tr>
            <tr><td>Progress</td><td>$PROGRESS%</td></tr>
            <tr><td>Status</td><td><span class=\"status-$STATUS\">$STATUS</span></td></tr>
            <tr><td>Category</td><td>$CATEGORY</td></tr>
            <tr><td>Priority</td><td>$PRIORITY</td></tr>
            <tr><td>Created</td><td>$(date -d "$CREATED_AT" +"%Y-%m-%d %H:%M UTC")</td></tr>
            <tr><td>Last Updated</td><td>$(date -d "$UPDATED_AT" +"%H:%M UTC")</td></tr>
            <tr><td>Duration</td><td>$duration_days days</td></tr>
        </table>
    </div>"

    # Add progress history section
    if [ "$INCLUDE_METRICS" = true ] && [ ${#PROGRESS_ENTRIES[@]} -gt 0 ]; then
        report_content="$report_content

    <div class=\"section\">
        <h2>Recent Progress</h2>
        <table>
            <tr><th>Date</th><th>Progress</th><th>Status</th><th>Notes</th></tr>"

        for entry_file in "${PROGRESS_ENTRIES[@]:0:10}"; do
            local entry_content=$(cat "$entry_file")
            local timestamp=$(echo "$entry_content" | jq -r '.timestamp')
            local progress=$(echo "$entry_content" | jq -r '.progress')
            local status=$(echo "$entry_content" | jq -r '.status')
            local notes=$(echo "$entry_content" | jq -r '.notes // ""')

            report_content="$report_content
            <tr>
                <td>$(date -d "$timestamp" +"%Y-%m-%d %H:%M")</td>
                <td>$progress%</td>
                <td><span class=\"status-$status\">$status</span></td>
                <td>${notes:0:50}...</td>
            </tr>"
        done

        report_content="$report_content
        </table>
    </div>"
    fi

    # Add achievements section
    if [ "$INCLUDE_EVIDENCE" = true ]; then
        report_content="$report_content

    <div class=\"section\">
        <h2>Achievements & Evidence</h2>"

        local achievement_dir="$goal_path/achievements"
        if [ -d "$achievement_dir" ]; then
            local achievement_files=($(find "$achievement_dir" -type f | head -10))
            if [ ${#achievement_files[@]} -gt 0 ]; then
                for achievement_file in "${achievement_files[@]}"; do
                    local filename=$(basename "$achievement_file")
                    report_content="$report_content
        <div class=\"evidence-item\">
            <strong>$filename</strong><br>
            <small>$(date -r "$achievement_file" +"%Y-%m-%d %H:%M")</small>
        </div>"
                done
            else
                report_content="$report_content
        <p>No achievements recorded yet.</p>"
            fi
        fi

        report_content="$report_content
    </div>"
    fi

    # Close HTML
    report_content="$report_content

    <div class=\"section\">
        <h2>Report Information</h2>
        <p><strong>Report Type:</strong> $REPORT_TYPE</p>
        <p><strong>Period:</strong> $PERIOD</p>
        <p><strong>Generated by:</strong> Goal-Kit v1.0</p>
    </div>

</body>
</html>"

    echo "$report_content" > "$output_file"
    log_success "Generated HTML report: $output_file"
}

# Main execution
main() {
    log_info "Goal-Kit Report Generation Script v1.0"
    log_info "====================================="

    # Parse arguments
    parse_arguments "$@"

    # Check dependencies
    check_dependencies

    # Generate output filename
    generate_output_filename "$GOAL_PATH" "$FORMAT" "$REPORT_TYPE" "$PERIOD"

    # Read goal data
    local goal_file="$GOAL_PATH/goal.json"
    read_goal_data "$goal_file"

    # Collect progress data
    collect_progress_data "$GOAL_PATH" "$PERIOD"

    # Generate report based on format
    case "$FORMAT" in
        json)
            generate_json_report "$GOAL_PATH" "$OUTPUT_FILE"
            ;;
        markdown)
            generate_markdown_report "$GOAL_PATH" "$OUTPUT_FILE"
            ;;
        html)
            generate_html_report "$GOAL_PATH" "$OUTPUT_FILE"
            ;;
        pdf)
            log_info "Generating PDF report..."
            generate_markdown_report "$GOAL_PATH" "${OUTPUT_FILE}.md"
            if command -v pandoc &> /dev/null && command -v wkhtmltopdf &> /dev/null; then
                pandoc "${OUTPUT_FILE}.md" -o "$OUTPUT_FILE" --pdf-engine=wkhtmltopdf
                rm "${OUTPUT_FILE}.md"
                log_success "Generated PDF report: $OUTPUT_FILE"
            else
                log_warning "PDF generation tools not available. PDF report not generated."
                log_info "You can convert the Markdown report to PDF manually."
            fi
            ;;
    esac

    log_success "Report generation completed successfully!"
    log_info "Report saved to: $OUTPUT_FILE"
    log_info "Keep up the great work! 📊"
}

# Run main function with all arguments
main "$@"