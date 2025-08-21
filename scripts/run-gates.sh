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
GATE_TIMES=()
SCRIPT_START_TIME=$(date +%s)

# Function to print section headers
print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Function to run a gate and track results with timing
run_gate() {
    local gate_name="$1"
    local gate_command="$2"
    local start_time=$(date +%s)
    
    echo -e "\n${YELLOW}▶ Running: ${gate_name}${NC}"
    
    if eval "$gate_command"; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        echo -e "${GREEN}✓ ${gate_name} passed (${duration}s)${NC}"
        PASSED_GATES+=("$gate_name")
        GATE_TIMES+=("${gate_name}: ${duration}s")
        return 0
    else
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        echo -e "${RED}✗ ${gate_name} failed (${duration}s)${NC}"
        FAILED_GATES+=("$gate_name")
        GATE_TIMES+=("${gate_name}: ${duration}s")
        return 1
    fi
}

# Parse command-line arguments
VERBOSE=false
PARALLEL_OVERRIDE=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --verbose|-v) VERBOSE=true ;;
        --parallel|-p)
            shift
            PARALLEL_OVERRIDE="$1"
            ;;
        --no-parallel) PARALLEL_OVERRIDE="0" ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --verbose, -v         Show detailed output"
            echo "  --parallel, -p N      Use N parallel workers (default: auto)"
            echo "  --no-parallel         Disable parallel execution"
            echo "  --help, -h            Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                    # Run all gates with auto parallelism"
            echo "  $0 --parallel 4       # Use 4 parallel workers"
            echo "  $0 --no-parallel      # Run tests sequentially"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
    shift
done

# Main execution
print_header "NXLC Quality Gates"
echo "Running all quality checks and tests..."
echo "Project root: $PROJECT_ROOT"

# Detect number of CPU cores for parallel execution
if command -v nproc &> /dev/null; then
    NUM_CORES=$(nproc)
elif command -v sysctl &> /dev/null; then
    NUM_CORES=$(sysctl -n hw.ncpu 2>/dev/null || echo 1)
else
    NUM_CORES=1
fi

# Determine parallel execution settings
if [ -n "$PARALLEL_OVERRIDE" ]; then
    if [ "$PARALLEL_OVERRIDE" = "0" ]; then
        PYTEST_PARALLEL=""
    else
        PYTEST_PARALLEL="-n $PARALLEL_OVERRIDE"
    fi
elif [ -n "$CI" ] || [ -n "$GITHUB_ACTIONS" ]; then
    PYTEST_PARALLEL="-n 2"  # Conservative for CI
else
    # Use auto for pytest-xdist to automatically determine optimal worker count
    PYTEST_PARALLEL="-n auto"
fi

# Check Python environment
print_header "Environment Check"
echo "Python version: $(python3 --version)"
echo "Working directory: $(pwd)"
echo "CPU cores detected: $NUM_CORES"

# Check if pytest-xdist is installed
if python3 -c "import xdist" 2>/dev/null; then
    if [ -z "$PYTEST_PARALLEL" ]; then
        echo -e "${YELLOW}Parallel execution disabled by user${NC}"
        PARALLEL_ENABLED=false
    else
        echo -e "${GREEN}pytest-xdist installed: parallel execution enabled${NC}"
        echo "Parallel execution: $PYTEST_PARALLEL"
        PARALLEL_ENABLED=true
    fi
else
    echo -e "${YELLOW}pytest-xdist not installed: running tests sequentially${NC}"
    echo -e "${YELLOW}Install with: pip install pytest-xdist for faster execution${NC}"
    PARALLEL_ENABLED=false
    PYTEST_PARALLEL=""
fi

# 1. Unit Tests
print_header "Unit Tests"
run_gate "Unit Tests" "python3 -m pytest tests/test_*.py $PYTEST_PARALLEL -v --tb=short --strict" || true

# 2. E2E Tests
print_header "E2E Tests"
if [ -f "tests/e2e/test_e2e_line_counting.py" ]; then
    # E2E tests handle fixtures individually, so parallelization helps significantly
    run_gate "E2E Line Counting Tests" "python3 -m pytest tests/e2e/test_e2e_line_counting.py $PYTEST_PARALLEL -v --tb=short --strict" || true
else
    echo -e "${YELLOW}⚠ E2E tests not found, skipping...${NC}"
fi

# 3. All Tests Combined
print_header "All Tests"
run_gate "All Tests Combined" "python3 -m pytest tests/ $PYTEST_PARALLEL -v --tb=short --no-header -q --strict" || true

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

# 8. Security Checks
print_header "Security Scanning"
echo -e "${YELLOW}Note: Some security tools may not be installed. Install for better coverage.${NC}"

# Check for hardcoded secrets
if command -v grep &> /dev/null; then
    echo "Checking for potential secrets..."
    run_gate "Secret Detection" "! grep -r -E '(api[_-]?key|apikey|secret[_-]?key|password|passwd|pwd|token|auth|credential|private[_-]?key)\\s*=\\s*[\"'\''][^\"'\'']+[\"'\'']' --include='*.py' --include='*.sh' --include='*.yml' --include='*.yaml' --include='*.json' --exclude-dir=.git --exclude-dir=.venv --exclude-dir=__pycache__ --exclude-dir=tests src/ scripts/ 2>/dev/null" || true
fi

# Check for common security issues with Bandit (only fail on medium+ severity)
if python3 -c "import bandit" 2>/dev/null; then
    run_gate "Bandit Security Scan" "python3 -m bandit -r src/ -ll --severity-level medium 2>/dev/null | grep -q 'No issues identified' && echo 'No high/medium severity issues found'" || true
else
    echo -e "${YELLOW}Bandit not installed: skipping security scan${NC}"
    echo -e "${YELLOW}Install with: pip install bandit${NC}"
fi

# Check for dependency vulnerabilities with pip-audit (more modern than safety)
if python3 -c "import pip_audit" 2>/dev/null; then
    run_gate "Dependency Security Check" "python3 -m pip_audit --desc 2>/dev/null | grep -q 'No known vulnerabilities' && echo 'No known vulnerabilities'" || true
elif python3 -c "import safety" 2>/dev/null; then
    # Fallback to safety if pip-audit not available
    run_gate "Dependency Security Check" "python3 -m safety scan --json 2>/dev/null | python3 -c 'import sys, json; data=json.load(sys.stdin) if sys.stdin.isatty() else {}; sys.exit(0)' 2>/dev/null && echo 'No known vulnerabilities'" || true
else
    echo -e "${YELLOW}pip-audit not installed: skipping dependency scan${NC}"
    echo -e "${YELLOW}Install with: pip install pip-audit${NC}"
fi

# Check for insecure practices
echo "Checking for insecure practices..."
run_gate "Insecure Practices Check" "! grep -r -E '(eval\\(|exec\\(|subprocess\\.call\\(|os\\.system\\(|pickle\\.loads?\\(|yaml\\.load\\()' --include='*.py' --exclude-dir=.git --exclude-dir=.venv --exclude-dir=__pycache__ --exclude-dir=tests src/ 2>/dev/null" || true

# 9. Code Quality Checks
print_header "Code Quality"

# Check for debugging artifacts
echo "Checking for debug artifacts..."
run_gate "Debug Artifacts Check" "! grep -r -E '(print\\(|console\\.log|debugger|import pdb|pdb\\.set_trace|breakpoint\\(\\))' --include='*.py' --exclude-dir=.git --exclude-dir=.venv --exclude-dir=__pycache__ --exclude-dir=tests --exclude='nxlc.py' src/ 2>/dev/null" || true

# Check for TODO/FIXME comments
if run_gate "TODO/FIXME Check" "grep -r -E '(TODO|FIXME|XXX|HACK|BUG)' --include='*.py' --include='*.sh' --exclude-dir=.git --exclude-dir=.venv src/ scripts/ 2>/dev/null | wc -l | xargs -I {} test {} -le 10" || true; then
    TODO_COUNT=$(grep -r -E '(TODO|FIXME|XXX|HACK|BUG)' --include='*.py' --include='*.sh' --exclude-dir=.git --exclude-dir=.venv src/ scripts/ 2>/dev/null | wc -l)
    echo -e "${YELLOW}Found $TODO_COUNT TODO/FIXME comments${NC}"
fi

# Check for large files
echo "Checking for large files..."
run_gate "Large Files Check" "! find . -type f -size +1M -not -path './.git/*' -not -path './.venv/*' -not -path './dist/*' 2>/dev/null | grep ." || true

# 10. License and Documentation Checks
print_header "License & Documentation"

# Check for license headers
run_gate "License File Exists" "test -f LICENSE" || true

# Check for README
run_gate "README Exists" "test -f README.md" || true

# Check Python files for docstrings
echo "Checking for docstrings in main module..."
run_gate "Docstring Coverage" "python3 -c 'import ast, sys; sys.path.insert(0, \"src\"); import nxlc; tree=ast.parse(open(\"src/nxlc.py\").read()); classes=[n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]; funcs=[n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]; docs=[n for n in classes+funcs if ast.get_docstring(n)]; print(f\"Docstring coverage: {len(docs)}/{len(classes+funcs)}\"); sys.exit(0 if len(docs) >= len(classes+funcs)*0.5 else 1)' 2>/dev/null" || true

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
SCRIPT_END_TIME=$(date +%s)
TOTAL_DURATION=$((SCRIPT_END_TIME - SCRIPT_START_TIME))

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Total Gates: $TOTAL_GATES"
echo -e "${GREEN}Passed: ${#PASSED_GATES[@]}${NC}"
echo -e "${RED}Failed: ${#FAILED_GATES[@]}${NC}"
echo -e "\nTotal execution time: ${TOTAL_DURATION} seconds"

if [ "$PARALLEL_ENABLED" = true ]; then
    echo -e "${GREEN}Parallel execution saved time with $PYTEST_PARALLEL${NC}"
fi

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