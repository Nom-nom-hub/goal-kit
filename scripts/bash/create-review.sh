#!/bin/bash

# Conduct project reviews and retrospectives

# Get the script directory and source common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

REVIEW_TYPE="${1:-}"
FORCE=false
JSON=false
VERBOSE=false

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
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
            handle_error "Unknown option: $1"
            ;;
        *)
            REVIEW_TYPE="$1"
            shift
            ;;
    esac
done

# Check if we're in a git repository
if ! test_git_repo; then
    handle_error "Not in a git repository. Please run this from the root of a Goal Kit project"
fi

PROJECT_ROOT=$(get_git_root) || handle_error "Could not determine git root"
cd "$PROJECT_ROOT" || handle_error "Failed to change to project root: $PROJECT_ROOT"

# Check if this is a Goal Kit project
if [ ! -f ".goalkit/vision.md" ]; then
    handle_error "Not a Goal Kit project. Please run 'goalkeeper init' first to set up the project"
fi

# Define review directory
REVIEW_DIR=".goalkit/reviews"
mkdir -p "$REVIEW_DIR" || handle_error "Failed to create reviews directory"

# Get timestamp for review
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +'%Y-%m-%d %H:%M:%S')
REVIEW_DATE=$(date +"%Y-%m-%d")

# Determine review type and file name
if [ -z "$REVIEW_TYPE" ]; then
    REVIEW_TYPE="general"
fi

REVIEW_FILE_NAME="review-$REVIEW_TYPE-$REVIEW_DATE.md"
REVIEW_FILE="$REVIEW_DIR/$REVIEW_FILE_NAME"

# If JSON mode, output JSON
if [ "$JSON" = true ]; then
    echo "{\"REVIEW_FILE\":\"$REVIEW_FILE\",\"REVIEW_DIR\":\"$REVIEW_DIR\",\"REVIEW_DATE\":\"$REVIEW_DATE\",\"REVIEW_TYPE\":\"$REVIEW_TYPE\"}"
    exit 0
fi

# Check if review file already exists
if [ -f "$REVIEW_FILE" ] && [ "$FORCE" = false ]; then
    write_warning "Review file already exists for this date: $REVIEW_FILE"
    write_info "Use --force to create a new review"
    exit 0
fi

# Check if template exists
TEMPLATE_PATH="$project_root/.goalkit/templates/review-template.md"
if [ -f "$TEMPLATE_PATH" ]; then
    REVIEW_CONTENT=$(cat "$TEMPLATE_PATH") || handle_error "Failed to read review template"
    REVIEW_CONTENT="${REVIEW_CONTENT//\[DATE\]/$TIMESTAMP}"
    REVIEW_CONTENT="${REVIEW_CONTENT//\[REVIEW_DATE\]/$REVIEW_DATE}"
    REVIEW_CONTENT="${REVIEW_CONTENT//\[REVIEW_TYPE\]/$REVIEW_TYPE}"
else
    # Fallback to default content based on review type
    if [ "$REVIEW_TYPE" = "retrospective" ]; then
        REVIEW_CONTENT="# Retrospective Review - $REVIEW_DATE

**Review Date**: $TIMESTAMP
**Review Type**: Retrospective

## What Went Well

- [Positive aspect 1]
- [Positive aspect 2]
- [Positive aspect 3]
- [Positive aspect 4]

## What Could Be Improved

- [Area for improvement 1]
  - **Action**: [Specific action to improve]
- [Area for improvement 2]
  - **Action**: [Specific action to improve]
- [Area for improvement 3]
  - **Action**: [Specific action to improve]

## What Surprised Us

- [Unexpected discovery or learning]
- [Unexpected discovery or learning]

## Action Items

| Action | Owner | Target Date | Status |
|--------|-------|-------------|--------|
| [Action 1] | [Owner] | [Date] | [ ] |
| [Action 2] | [Owner] | [Date] | [ ] |
| [Action 3] | [Owner] | [Date] | [ ] |

## Metrics from This Period

| Metric | Value | Trend |
|--------|-------|-------|
| [Metric 1] | [Value] | [↑/↓/-] |
| [Metric 2] | [Value] | [↑/↓/-] |
| [Metric 3] | [Value] | [↑/↓/-] |

## Commitments for Next Period

- [ ] [Specific commitment 1]
- [ ] [Specific commitment 2]
- [ ] [Specific commitment 3]
"
    else
        REVIEW_CONTENT="# Project Review - $REVIEW_DATE

**Review Date**: $TIMESTAMP
**Review Type**: $REVIEW_TYPE

## Overall Assessment

### Project Health
- **Status**: [On Track / At Risk / Off Track / Completed]
- **Overall Progress**: [X% complete]

### Key Achievements
1. [Major achievement 1]
2. [Major achievement 2]
3. [Major achievement 3]

---

## Goal Progress Review

### Vision Alignment
- Are we staying true to the original vision? [Yes / Partially / No]
- Are we still aligned with project principles? [Yes / Partially / No]

### Goal Status
- **Goal 1**: [Status] - [Progress %]
- **Goal 2**: [Status] - [Progress %]
- **Goal 3**: [Status] - [Progress %]

---

## Technical & Quality Review

### Code Quality
- **Test Coverage**: [X%]
- **Build Status**: [Passing / Failing]
- **Code Review Process**: [Assessment]

### Architecture & Design
- **Design Quality**: [Good / Acceptable / Needs Work]
- **Scalability Concerns**: [List any concerns]
- **Technical Debt**: [Assessment]

---

## Team & Resource Review

### Team Performance
- **Team Morale**: [High / Good / Fair / Low]
- **Productivity**: [Assessment]
- **Collaboration**: [Assessment]

### Learning & Development
- **Skills Growth**: [Areas of growth]
- **Training Needs**: [Identified needs]

---

## Risk & Issue Review

### Outstanding Risks
| Risk | Probability | Impact | Status |
|------|-------------|--------|--------|
| [Risk 1] | [High/Medium/Low] | [High/Medium/Low] | [Mitigating] |
| [Risk 2] | [High/Medium/Low] | [High/Medium/Low] | [Monitoring] |

### Resolved Issues
- [Issue 1 - Resolution]
- [Issue 2 - Resolution]

---

## Recommendations & Next Steps

### Immediate Actions (Next 1-2 weeks)
1. [Action with owner and due date]
2. [Action with owner and due date]

### Medium-term Focus (Next Month)
1. [Focus area]
2. [Focus area]

### Strategic Considerations
- [Long-term consideration]
- [Long-term consideration]

---

## Sign-off

- **Reviewed By**: [Name]
- **Review Date**: $REVIEW_DATE
- **Next Review**: [Scheduled date]
"
    fi
fi

# Write review file
echo "$REVIEW_CONTENT" > "$REVIEW_FILE" || handle_error "Failed to write review file: $REVIEW_FILE"
write_success "Created review document: $REVIEW_FILE"

# Git operations
git add "$REVIEW_FILE" 2>/dev/null || write_warning "Failed to stage review file in git"
git commit -m "Add $REVIEW_TYPE review for $REVIEW_DATE" 2>/dev/null || write_warning "Failed to commit review file to git"

write_success "Review committed to repository"

# Print summary
echo ""
write_info "Review document created successfully!"
echo "  Review File: $REVIEW_FILE"
echo "  Review Type: $REVIEW_TYPE"
echo "  Review Date: $REVIEW_DATE"
echo ""
write_info "Review Types:"
echo "  - retrospective: Team retrospective and lessons learned"
echo "  - general: Overall project health and progress review"
echo "  - goal: Individual goal milestone review"
echo ""
write_info "Next Steps:"
echo "  1. Complete the review document with detailed assessments"
echo "  2. Identify action items and assign owners"
echo "  3. Share with team and stakeholders"
echo "  4. Use insights to inform next period's planning"
echo ""
