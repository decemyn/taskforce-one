#!/bin/bash
# Code formatting script for Task Force One

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
CHECK=""
VERBOSE=""
FILES="."

while [[ $# -gt 0 ]]; do
    case $1 in
        --check)
            CHECK="--check"
            shift
            ;;
        --verbose|-v)
            VERBOSE="-v"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS] [FILES]"
            echo ""
            echo "Options:"
            echo "  --check    Check formatting without applying changes"
            echo "  -v         Verbose output"
            echo "  -h         Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                  Format all code"
            echo "  $0 --check          Check formatting"
            echo "  $0 src/             Format specific directory"
            exit 0
            ;;
        *)
            FILES="$FILES $1"
            shift
            ;;
    esac
done

echo -e "${GREEN}Running Task Force One Code Formatter${NC}"
echo "============================================"

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container"
    cd /app
else
    echo "Running locally"
fi

# Install ruff if not present
if ! command -v ruff &> /dev/null; then
    echo -e "${YELLOW}Installing ruff...${NC}"
    python3 -m pip install ruff
fi

echo ""
echo -e "${BLUE}Running ruff format...${NC}"
echo "-------------------------------"

if [ -n "$CHECK" ]; then
    echo -e "${YELLOW}Checking formatting...${NC}"
    ruff format --check $FILES
else
    echo -e "${YELLOW}Applying formatting...${NC}"
    ruff format $FILES
fi

echo ""
echo "============================================"

if [ $? -eq 0 ]; then
    if [ -n "$CHECK" ]; then
        echo -e "${GREEN}Formatting check passed!${NC}"
    else
        echo -e "${GREEN}Formatting applied!${NC}"
    fi
else
    echo -e "${RED}Formatting issues found!${NC}"
    exit 1
fi
