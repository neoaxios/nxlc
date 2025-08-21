#!/bin/bash

# run-gates.sh - Run all quality gates for the NXLC project
# This script runs all tests and checks that must pass before committing or pushing code

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the project root directory (parent of scripts directory)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Track overall status
FAILED_GATES=()
PASSED_GATES=()

# Function to print section headers
print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Function to run a gate and track results
run_gate() {
    local gate_name="$1"
    local gate_command="$2"
    
    echo -e "\n${YELLOW}▶ Running: ${gate_name}${NC}"
    
    if eval "$gate_command"; then
        echo -e "${GREEN}✓ ${gate_name} passed${NC}"
        PASSED_GATES+=("$gate_name")
        return 0
    else
        echo -e "${RED}✗ ${gate_name} failed${NC}"
        FAILED_GATES+=("$gate_name")
        return 1
    fi
}

# Parse command-line arguments
QUICK_MODE=false
VERBOSE=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --quick|-q) QUICK_MODE=true ;;
        --verbose|-v) VERBOSE=true ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --quick, -q    Run only essential tests (faster)"
            echo "  --verbose, -v  Show detailed output"
            echo "  --help, -h     Show this help message"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
    shift
done

# Main execution
print_header "NXLC Quality Gates"
if [ "$QUICK_MODE" = true ]; then
    echo "Running in QUICK mode (essential tests only)..."
else
    echo "Running all quality checks and tests..."
fi
echo "Project root: $PROJECT_ROOT"

# Check Python environment
print_header "Environment Check"
echo "Python version: $(python3 --version)"
echo "Working directory: $(pwd)"

if [ "$QUICK_MODE" = false ]; then
    # 1. Unit Tests
    print_header "Unit Tests"
    run_gate "Unit Tests" "python3 -m pytest tests/test_*.py -v --tb=short" || true
fi

# 2. E2E Tests (always run - this is the most important gate)
print_header "E2E Tests"
if [ -f "tests/e2e/test_e2e_line_counting.py" ]; then
    run_gate "E2E Line Counting Tests" "python3 -m pytest tests/e2e/test_e2e_line_counting.py -v --tb=short" || true
else
    echo -e "${YELLOW}⚠ E2E tests not found, skipping...${NC}"
fi

# 3. All Tests Combined (skip in quick mode)
if [ "$QUICK_MODE" = false ]; then
    print_header "All Tests"
    run_gate "All Tests Combined" "python3 -m pytest tests/ -v --tb=short --no-header -q" || true
fi

# 4. Syntax Check
print_header "Syntax Validation"
run_gate "Python Syntax Check" "python3 -m py_compile src/nxlc.py" || true

# 5. Import Check
print_header "Import Validation"
run_gate "Import Check" "python3 -c 'import sys; sys.path.insert(0, \"src\"); import nxlc'" || true

# 6. Basic Functionality Test
print_header "Basic Functionality"
run_gate "NXLC Help Command" "python3 src/nxlc.py --help > /dev/null 2>&1" || true
run_gate "NXLC Version Command" "python3 src/nxlc.py --version > /dev/null 2>&1" || true

# 7. Test on Current Directory
print_header "Self-Test"
echo "Running NXLC on its own codebase..."
if run_gate "NXLC Self-Analysis" "python3 src/nxlc.py . --no-git --no-color | head -20" || true; then
    echo -e "${GREEN}Successfully analyzed own codebase${NC}"
fi

# Final Report
print_header "Gate Results Summary"

echo -e "\n${GREEN}Passed Gates (${#PASSED_GATES[@]}):${NC}"
for gate in "${PASSED_GATES[@]}"; do
    echo -e "  ${GREEN}✓${NC} $gate"
done

if [ ${#FAILED_GATES[@]} -gt 0 ]; then
    echo -e "\n${RED}Failed Gates (${#FAILED_GATES[@]}):${NC}"
    for gate in "${FAILED_GATES[@]}"; do
        echo -e "  ${RED}✗${NC} $gate"
    done
fi

# Summary statistics
TOTAL_GATES=$((${#PASSED_GATES[@]} + ${#FAILED_GATES[@]}))
echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Total Gates: $TOTAL_GATES"
echo -e "${GREEN}Passed: ${#PASSED_GATES[@]}${NC}"
echo -e "${RED}Failed: ${#FAILED_GATES[@]}${NC}"

# Exit status
if [ ${#FAILED_GATES[@]} -eq 0 ]; then
    echo -e "\n${GREEN}━━━ ✓ ALL GATES PASSED ✓ ━━━${NC}"
    echo -e "${GREEN}Code is ready for commit/push!${NC}\n"
    exit 0
else
    echo -e "\n${RED}━━━ ✗ GATES FAILED ✗ ━━━${NC}"
    echo -e "${RED}Please fix the failing gates before committing.${NC}\n"
    exit 1
fi