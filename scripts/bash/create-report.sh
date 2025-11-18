#!/bin/bash

# Generate progress reports for a project or goal

set -e

GOAL_DIR="${1:-}"
EDIT=false
FORCE=false
JSON=false
VERBOSE=false

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --edit)
            EDIT=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --json)
            JSON=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            GOAL_DIR="$1"
            shift
            ;;
    esac
done

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    write_error "Not in a git repository"
    write_info "Please run this from the root of a Goal Kit project"
    exit 1
fi

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

# Check if this is a Goal Kit project
if [ ! -f ".goalkit/vision.md" ]; then
    write_error "Not a Goal Kit project"
    write_info "Please run 'goalkeeper init' first to set up the project"
    exit 1
fi

# Define report directory
REPORT_DIR=".goalkit/reports"
mkdir -p "$REPORT_DIR"

# Get timestamp for report
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
REPORT_DATE=$(date +"%Y-%m-%d")

# Determine report file name
if [ -z "$GOAL_DIR" ]; then
    REPORT_FILE_NAME="progress-report-$REPORT_DATE.md"
else
    REPORT_FILE_NAME="report-$GOAL_DIR-$REPORT_DATE.md"
fi

REPORT_FILE="$REPORT_DIR/$REPORT_FILE_NAME"

# If JSON mode, output JSON
if [ "$JSON" = true ]; then
    echo "{\"REPORT_FILE\":\"$REPORT_FILE\",\"REPORT_DIR\":\"$REPORT_DIR\",\"REPORT_DATE\":\"$REPORT_DATE\"}"
    exit 0
fi

# Check if report file already exists
if [ -f "$REPORT_FILE" ] && [ "$EDIT" = false ] && [ "$FORCE" = false ]; then
    write_warning "Report file already exists for this date: $REPORT_FILE"
    write_info "Use --edit to open in editor or --force to create a new report"
    exit 0
fi

if [ -f "$REPORT_FILE" ] && [ "$EDIT" = true ]; then
    if [ "$VERBOSE" = true ]; then
        write_info "Opening report file for editing..."
    fi
    # Open in default editor
    if command -v code &> /dev/null; then
        code "$REPORT_FILE"
    elif command -v nano &> /dev/null; then
        nano "$REPORT_FILE"
    else
        vi "$REPORT_FILE"
    fi
    exit 0
fi

# Check if template exists
TEMPLATE_PATH=".goalkit/templates/report-template.md"
if [ -f "$TEMPLATE_PATH" ]; then
    REPORT_CONTENT=$(cat "$TEMPLATE_PATH")
    REPORT_CONTENT="${REPORT_CONTENT//\[DATE\]/$TIMESTAMP}"
    REPORT_CONTENT="${REPORT_CONTENT//\[REPORT_DATE\]/$REPORT_DATE}"
    if [ -n "$GOAL_DIR" ]; then
        REPORT_CONTENT="${REPORT_CONTENT//\[GOAL\]/$GOAL_DIR}"
    fi
else
    # Fallback to default content
    GOAL_DISPLAY="${GOAL_DIR:-Overall Project}"
    REPORT_CONTENT="# Progress Report - $REPORT_DATE

**Report Date**: $TIMESTAMP
**Goal**: $GOAL_DISPLAY

## Executive Summary

[Provide a high-level overview of progress made in this period]

## Goals & Objectives Status

### Overall Goal Status
- **Status**: [On Track / At Risk / Off Track / Completed]
- **Progress**: [X% complete]
- **Key Achievements**: [List major achievements this period]

---

## Detailed Progress

### Completed Items

- [ ] [Completed item 1]
- [ ] [Completed item 2]
- [ ] [Completed item 3]

### In Progress

- **[Item Name]**: [Progress percentage] - [Brief description]
- **[Item Name]**: [Progress percentage] - [Brief description]

### Upcoming

- [ ] [Planned item 1]
- [ ] [Planned item 2]

---

## Blockers & Challenges

### Current Blockers

1. **[Blocker Title]**: [Description and impact]
   - **Impact**: [How this affects progress]
   - **Mitigation**: [Plan to resolve]

2. **[Blocker Title]**: [Description and impact]

### Lessons Learned

- [What we learned from this period]
- [What went well]
- [What could improve]

---

## Metrics & KPIs

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| [Metric 1] | [Target] | [Actual] | [✓/✗] |
| [Metric 2] | [Target] | [Actual] | [✓/✗] |
| [Metric 3] | [Target] | [Actual] | [✓/✗] |

---

## Resource & Team Status

- **Team Capacity**: [X% utilized / Available]
- **Major Resource Changes**: [Any staffing or resource changes]
- **Skills Gaps**: [Any identified training needs]

---

## Next Period Plan

### Priority Items for Next Period

1. **[High Priority Item]**: [Description and rationale]
2. **[High Priority Item]**: [Description and rationale]
3. **[Medium Priority Item]**: [Description and rationale]

### Success Criteria for Next Period

- [ ] [Specific criterion]
- [ ] [Specific criterion]
- [ ] [Specific criterion]

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| [Risk 1] | [High/Medium/Low] | [High/Medium/Low] | [Plan] |
| [Risk 2] | [High/Medium/Low] | [High/Medium/Low] | [Plan] |

---

## Appendices

### A. Detailed Metrics
[Include any detailed data or charts]

### B. Code Changes Summary
[Brief summary of code commits and changes]

### C. Communication
[Notes on stakeholder communications or decisions made]
"
fi

# Write report file
echo "$REPORT_CONTENT" > "$REPORT_FILE"
write_success "Created progress report: $REPORT_FILE"

# Git operations
git add "$REPORT_FILE" 2>/dev/null || true
if [ -z "$GOAL_DIR" ]; then
    git commit -m "Add progress report for $REPORT_DATE" 2>/dev/null || true
else
    git commit -m "Add progress report for goal $GOAL_DIR on $REPORT_DATE" 2>/dev/null || true
fi

write_success "Report committed to repository"

# Print summary
echo ""
write_info "Progress report created successfully!"
echo "  Report File: $REPORT_FILE"
echo "  Report Date: $REPORT_DATE"
echo ""
write_info "Next Steps:"
echo "  1. Fill in progress details and metrics"
echo "  2. Document blockers and lessons learned"
echo "  3. Review with team and stakeholders"
echo "  4. Use this to plan next period's work"
echo ""
