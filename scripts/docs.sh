#!/bin/bash
# Documentation build script for Task Force One
# Only runs in Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PORT=8080

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            PORT="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --port PORT    Port for HTTP server (default: 8080)"
            echo "  -h             Show this help message"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

echo -e "${GREEN}Building Task Force One Documentation${NC}"
echo "=========================================="

# Build and serve docs in Docker
# Note: we run from /app to allow sphinx to find the conf.py in /app/docs
docker run --rm -v "$(pwd):/app" -p "${PORT}:8080" -w /app python:3.11-slim bash -c "
    pip install sphinx sphinx-rtd-theme myst-parser sphinx-autodoc-typehints --break-system-packages &&
    sphinx-build -b html docs docs/_build/html &&
    cd docs/_build/html &&
    python3 -m http.server 8080
"

echo -e "${GREEN}Documentation available at http://localhost:${PORT}${NC}"
