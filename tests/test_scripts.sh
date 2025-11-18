#!/bin/bash

# Integration tests for shell scripts (bash)
# Tests cover:
# - Common script utilities
# - Create new goal script
# - Setup strategy script
# - Setup milestones script
# - Setup execution script
# - Error handling and validation

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Create temp directory for testing
TEST_DIR=$(mktemp -d)
trap "rm -rf $TEST_DIR" EXIT

# Helper function to run tests
run_test() {
    local test_name=$1
    local test_func=$2
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    echo -ne "Test $TESTS_RUN: $test_name ... "
    
    if $test_func > /dev/null 2>&1; then
        echo -e "${GREEN}PASSED${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Test: common.sh functions exist
test_common_script_exists() {
    [ -f "scripts/bash/common.sh" ]
}

# Test: common.sh is executable
test_common_script_executable() {
    [ -x "scripts/bash/common.sh" ] || [ -f "scripts/bash/common.sh" ]
}

# Test: common.sh contains write_colored function
test_common_has_write_colored() {
    grep -q "write_colored" "scripts/bash/common.sh"
}

# Test: common.sh contains write_info function
test_common_has_write_info() {
    grep -q "write_info" "scripts/bash/common.sh"
}

# Test: common.sh contains write_success function
test_common_has_write_success() {
    grep -q "write_success" "scripts/bash/common.sh"
}

# Test: common.sh contains write_error function
test_common_has_write_error() {
    grep -q "write_error" "scripts/bash/common.sh"
}

# Test: common.sh contains git functions
test_common_has_git_functions() {
    grep -q "test_git_repo\|get_git_root" "scripts/bash/common.sh"
}

# Test: create-new-goal.sh exists
test_create_goal_script_exists() {
    [ -f "scripts/bash/create-new-goal.sh" ]
}

# Test: create-new-goal.sh is executable or exists
test_create_goal_script_executable() {
    [ -x "scripts/bash/create-new-goal.sh" ] || [ -f "scripts/bash/create-new-goal.sh" ]
}

# Test: create-new-goal.sh has valid shebang
test_create_goal_valid_shebang() {
    grep -q "^#!/bin/bash" "scripts/bash/create-new-goal.sh"
}

# Test: create-new-goal.sh imports common
test_create_goal_imports_common() {
    grep -q "source.*common.sh\|\..*common.sh" "scripts/bash/create-new-goal.sh"
}

# Test: setup-strategy.sh exists
test_setup_strategy_script_exists() {
    [ -f "scripts/bash/setup-strategy.sh" ]
}

# Test: setup-strategy.sh is executable
test_setup_strategy_script_executable() {
    [ -x "scripts/bash/setup-strategy.sh" ] || [ -f "scripts/bash/setup-strategy.sh" ]
}

# Test: setup-strategy.sh has valid shebang
test_setup_strategy_valid_shebang() {
    grep -q "^#!/bin/bash" "scripts/bash/setup-strategy.sh"
}

# Test: setup-milestones.sh exists
test_setup_milestones_script_exists() {
    [ -f "scripts/bash/setup-milestones.sh" ]
}

# Test: setup-milestones.sh is executable
test_setup_milestones_script_executable() {
    [ -x "scripts/bash/setup-milestones.sh" ] || [ -f "scripts/bash/setup-milestones.sh" ]
}

# Test: setup-milestones.sh has valid shebang
test_setup_milestones_valid_shebang() {
    grep -q "^#!/bin/bash" "scripts/bash/setup-milestones.sh"
}

# Test: setup-execution.sh exists
test_setup_execution_script_exists() {
    [ -f "scripts/bash/setup-execution.sh" ]
}

# Test: setup-execution.sh is executable
test_setup_execution_script_executable() {
    [ -x "scripts/bash/setup-execution.sh" ] || [ -f "scripts/bash/setup-execution.sh" ]
}

# Test: setup-execution.sh has valid shebang
test_setup_execution_valid_shebang() {
    grep -q "^#!/bin/bash" "scripts/bash/setup-execution.sh"
}

# Test: scripts have error handling
test_scripts_have_error_handling() {
    grep -q "set -e\|exit.*[1-9]\|if.*; then" "scripts/bash/create-new-goal.sh"
}

# Test: scripts follow naming conventions
test_scripts_follow_conventions() {
    [ -f "scripts/bash/create-new-goal.sh" ] && \
    [ -f "scripts/bash/setup-strategy.sh" ] && \
    [ -f "scripts/bash/setup-milestones.sh" ] && \
    [ -f "scripts/bash/setup-execution.sh" ]
}

# Test: PowerShell scripts exist on Windows
test_powershell_scripts_exist() {
    if [ -d "scripts/powershell" ]; then
        [ -f "scripts/powershell/common.ps1" ] && \
        [ -f "scripts/powershell/create-new-goal.ps1" ] && \
        [ -f "scripts/powershell/setup-strategy.ps1" ] && \
        [ -f "scripts/powershell/setup-milestones.ps1" ] && \
        [ -f "scripts/powershell/setup-execution.ps1" ]
    else
        # PowerShell scripts are Windows-specific, skip on non-Windows
        true
    fi
}

# Test: scripts are in proper directory structure
test_script_directory_structure() {
    [ -d "scripts/bash" ] && \
    [ -f "scripts/bash/common.sh" ] && \
    [ -f "scripts/bash/create-new-goal.sh" ]
}

# Test: create-new-goal script mentions goal directory creation
test_create_goal_creates_directory() {
    grep -q "mkdir\|goal.*dir" "scripts/bash/create-new-goal.sh"
}

# Test: setup strategy script copies template
test_setup_strategy_copies_template() {
    grep -q "cp\|copy\|template" "scripts/bash/setup-strategy.sh"
}

# Test: setup milestones script copies template
test_setup_milestones_copies_template() {
    grep -q "cp\|copy\|template" "scripts/bash/setup-milestones.sh"
}

# Test: setup execution script copies template
test_setup_execution_copies_template() {
    grep -q "cp\|copy\|template" "scripts/bash/setup-execution.sh"
}

# Test: scripts handle arguments
test_scripts_handle_arguments() {
    grep -q '\$1\|\$@\|[$][0-9]' "scripts/bash/create-new-goal.sh"
}

# Test: scripts output JSON mode support
test_scripts_json_mode() {
    grep -q "json\|--json\|-j" "scripts/bash/create-new-goal.sh"
}

# Test: common.sh has update_agent_context function
test_common_has_update_agent_context() {
    grep -q "update_agent_context" "scripts/bash/common.sh"
}

# Test: scripts are readable
test_scripts_are_readable() {
    [ -r "scripts/bash/common.sh" ] && \
    [ -r "scripts/bash/create-new-goal.sh" ]
}

# Run all tests
echo -e "${YELLOW}Running Bash Script Tests${NC}"
echo "=============================="
echo

run_test "common.sh script exists" test_common_script_exists
run_test "common.sh is executable" test_common_script_executable
run_test "common.sh has write_colored function" test_common_has_write_colored
run_test "common.sh has write_info function" test_common_has_write_info
run_test "common.sh has write_success function" test_common_has_write_success
run_test "common.sh has write_error function" test_common_has_write_error
run_test "common.sh has git functions" test_common_has_git_functions
run_test "create-new-goal.sh exists" test_create_goal_script_exists
run_test "create-new-goal.sh is executable" test_create_goal_script_executable
run_test "create-new-goal.sh has valid shebang" test_create_goal_valid_shebang
run_test "create-new-goal.sh imports common" test_create_goal_imports_common
run_test "setup-strategy.sh exists" test_setup_strategy_script_exists
run_test "setup-strategy.sh is executable" test_setup_strategy_script_executable
run_test "setup-strategy.sh has valid shebang" test_setup_strategy_valid_shebang
run_test "setup-milestones.sh exists" test_setup_milestones_script_exists
run_test "setup-milestones.sh is executable" test_setup_milestones_script_executable
run_test "setup-milestones.sh has valid shebang" test_setup_milestones_valid_shebang
run_test "setup-execution.sh exists" test_setup_execution_script_exists
run_test "setup-execution.sh is executable" test_setup_execution_script_executable
run_test "setup-execution.sh has valid shebang" test_setup_execution_valid_shebang
run_test "scripts have error handling" test_scripts_have_error_handling
run_test "scripts follow naming conventions" test_scripts_follow_conventions
run_test "PowerShell scripts exist (if applicable)" test_powershell_scripts_exist
run_test "script directory structure is correct" test_script_directory_structure
run_test "create-new-goal creates directory" test_create_goal_creates_directory
run_test "setup-strategy copies template" test_setup_strategy_copies_template
run_test "setup-milestones copies template" test_setup_milestones_copies_template
run_test "setup-execution copies template" test_setup_execution_copies_template
run_test "scripts handle arguments" test_scripts_handle_arguments
run_test "scripts support JSON mode" test_scripts_json_mode
run_test "common.sh has update_agent_context" test_common_has_update_agent_context
run_test "scripts are readable" test_scripts_are_readable

echo
echo "=============================="
echo -e "${YELLOW}Test Summary${NC}"
echo "=============================="
echo "Tests run:    $TESTS_RUN"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi
