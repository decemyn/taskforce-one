#!/bin/bash
# Linting script for Task Force One

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
LINTERS="ruff,mypy"
FIX=""
VERBOSE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --ruff)
            LINTERS="ruff"
            shift
            ;;
        --mypy)
            LINTERS="mypy"
            shift
            ;;
        --all)
            LINTERS="ruff,mypy"
            shift
            ;;
        --fix)
            FIX="--fix"
            shift
            ;;
        --verbose|-v)
            VERBOSE="-v"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --ruff    Run only ruff linter"
            echo "  --mypy   Run only mypy type checker"
            echo "  --all     Run all linters (default)"
            echo "  --fix     Attempt to fix issues (ruff only)"
            echo "  -v        Verbose output"
            echo "  -h        Show this help message"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

echo -e "${GREEN}Running Task Force One Linters${NC}"
echo "========================================"

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container"
    cd /app
else
    echo "Running locally"
fi

# Install linting tools if not present
if ! command -v ruff &> /dev/null; then
    echo -e "${YELLOW}Installing ruff...${NC}"
    python3 -m pip install ruff
fi

if ! command -v mypy &> /dev/null; then
    echo -e "${YELLOW}Installing mypy...${NC}"
    python3 -m pip install mypy
fi

# Run linters
IFS=',' read -ra LINTER_ARRAY <<< "$LINTERS"
FAILED=0

for LINTER in "${LINTER_ARRAY[@]}"; do
    echo ""
    echo -e "${BLUE}Running $LINTER...${NC}"
    echo "-----------------------------------"
    
    case $LINTER in
        ruff)
            if [ -n "$FIX" ]; then
                ruff check --fix src/ || FAILED=1
            else
                ruff check src/ || FAILED=1
            fi
            ;;
        mypy)
            mypy src/ || FAILED=1
            ;;
    esac
done

echo ""
echo "========================================"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All linting passed!${NC}"
else
    echo -e "${RED}Linting found issues!${NC}"
    exit 1
fi
