#!/bin/bash
# Health check script for Task Force One deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
HOST="localhost"
PORT="8000"
TIMEOUT=5
VERBOSE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --host HOST      API host (default: localhost)"
            echo "  --port PORT      API port (default: 8000)"
            echo "  --timeout SECS   Timeout in seconds (default: 5)"
            echo "  -v               Verbose output"
            echo "  -h               Show this help message"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

BASE_URL="http://${HOST}:${PORT}"

echo -e "${GREEN}Task Force One Health Check${NC}"
echo "================================"
echo "URL: $BASE_URL"
echo ""

# Function to check endpoint
check_endpoint() {
    local endpoint=$1
    local description=$2
    
    if [ -n "$VERBOSE" ]; then
        echo -e "${BLUE}Checking $endpoint...${NC}"
    fi
    
    response=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "${BASE_URL}${endpoint}" 2>/dev/null || echo "000")
    
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✓${NC} $description"
        return 0
    else
        echo -e "${RED}✗${NC} $description (HTTP $response)"
        return 1
    fi
}

# Check root endpoint
echo -e "${BLUE}API Endpoints:${NC}"
check_endpoint "/" "Root endpoint"

# Check health endpoint
check_endpoint "/health" "Health check"

# Check agents endpoint
check_endpoint "/agents" "List agents"

# Check crews endpoint
check_endpoint "/crews" "List crews"

echo ""
echo "================================"

# Overall status
if check_endpoint "/health" > /dev/null 2>&1; then
    echo -e "${GREEN}All health checks passed!${NC}"
    exit 0
else
    echo -e "${RED}Some health checks failed!${NC}"
    exit 1
fi
