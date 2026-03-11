#!/bin/bash
# Test runner script for Task Force One
# Only runs in Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
TEST_TYPE="all"
VERBOSE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --unit)
            TEST_TYPE="unit"
            shift
            ;;
        --integration)
            TEST_TYPE="integration"
            shift
            ;;
        --e2e)
            TEST_TYPE="e2e"
            shift
            ;;
        --all)
            TEST_TYPE="all"
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
            echo "  --unit         Run unit tests only"
            echo "  --integration  Run integration tests only"
            echo "  --e2e         Run end-to-end tests only"
            echo "  --all         Run all tests (default)"
            echo "  --verbose      Verbose output"
            echo "  -h             Show this help message"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

echo -e "${GREEN}Running Task Force One Tests${NC}"
echo "=========================================="

# Run tests in Docker
docker run --rm \
    -v "$(pwd):/app" \
    -w /app \
    -e PYTHONPATH=/app/src \
    python:3.11-slim bash -c "
        pip install -e . pytest pytest-cov --break-system-packages >/dev/null 2>&1 &&
        pytest tests/ $VERBOSE --cov=src/taskforce_one --cov-report=html
    "

echo ""
echo -e "${GREEN}Tests completed${NC}"
echo "Coverage report available in htmlcov/index.html"
