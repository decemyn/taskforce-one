#!/bin/bash
# Logs viewer script for Task Force One

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
SERVICE="taskforce"
LINES=100
FOLLOW=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --service|-s)
            SERVICE="$2"
            shift 2
            ;;
        --lines|-n)
            LINES="$2"
            shift 2
            ;;
        --follow|-f)
            FOLLOW=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -s, --service NAME  Service to view logs for (default: taskforce)"
            echo "                       Options: taskforce, postgres, redis, all"
            echo "  -n, --lines NUM     Number of lines to show (default: 100)"
            echo "  -f, --follow       Follow log output (like tail -f)"
            echo "  -h                 Show this help message"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

echo -e "${GREEN}Task Force One Logs${NC}"
echo "====================="
echo "Service: $SERVICE"
echo "Lines: $LINES"
echo ""

# Determine docker compose file
COMPOSE_FILE="docker/docker-compose.yml"

# Check if service exists
if [ "$SERVICE" != "all" ]; then
    if ! docker compose -f $COMPOSE_FILE ps --services | grep -q "^${SERVICE}$"; then
        echo -e "${RED}Service '$SERVICE' not found!${NC}"
        echo "Available services:"
        docker compose -f $COMPOSE_FILE ps --services
        exit 1
    fi
fi

# Build docker logs command
DOCKER_CMD="docker compose -f $COMPOSE_FILE logs"

if [ "$SERVICE" = "all" ]; then
    DOCKER_CMD="$DOCKER_CMD"
else
    DOCKER_CMD="$DOCKER_CMD $SERVICE"
fi

if [ "$FOLLOW" = true ]; then
    DOCKER_CMD="$DOCKER_CMD --follow"
else
    DOCKER_CMD="$DOCKER_CMD --tail $LINES"
fi

# Run the command
eval $DOCKER_CMD
