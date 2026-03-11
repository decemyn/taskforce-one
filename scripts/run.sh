#!/bin/bash
# Task Force One - Run Script
# Starts the application in development mode

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Task Force One - Run${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found. Using default configuration.${NC}"
    echo -e "${YELLOW}Run './scripts/setup.sh' first to create a proper environment.${NC}"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Running setup...${NC}"
    ./scripts/setup.sh
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Set environment variables
export ENVIRONMENT=development
export LOG_LEVEL=INFO

# Run the application
echo -e "${GREEN}Starting Task Force One...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

python -m uvicorn taskforce_one.api:app --host 0.0.0.0 --port 8000 --reload
