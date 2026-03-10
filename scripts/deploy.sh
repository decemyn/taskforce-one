#!/bin/bash
# Task Force One - Deploy Script
# Deploys the application using Docker
# Includes automatic installation of required tools if missing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Default values
ENVIRONMENT="production"
COMPOSE_FILE="docker/docker-compose.yml"
IMAGE_NAME="taskforce-one"
REGISTRY=""
TAG="latest"
INSTALL_DOCKER=false
SKIP_INSTALL=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --tag)
            TAG="$2"
            shift 2
            ;;
        --registry)
            REGISTRY="$2"
            shift 2
            ;;
        --install-docker)
            INSTALL_DOCKER=true
            shift
            ;;
        --skip-install)
            SKIP_INSTALL=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --env ENV         Set environment (development|staging|production) [default: production]"
            echo "  --tag TAG         Set image tag [default: latest]"
            echo "  --registry URL    Set container registry URL"
            echo "  --install-docker  Install Docker if not found (requires root)"
            echo "  --skip-install    Skip dependency installation checks"
            echo "  --help            Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Task Force One - Deploy${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Environment: ${CYAN}$ENVIRONMENT${NC}"
echo -e "Image Tag:   ${CYAN}$TAG${NC}"
echo ""

# Function to install Docker on Ubuntu/Debian
install_docker_ubuntu() {
    echo -e "${YELLOW}Installing Docker...${NC}"
    
    # Update package index
    sudo apt-get update -qq
    
    # Install dependencies
    sudo apt-get install -y -qq ca-certificates curl gnupg lsb-release
    
    # Add Docker GPG key
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Add Docker repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker
    sudo apt-get update -qq
    sudo apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    echo -e "${GREEN}✓ Docker installed successfully${NC}"
}

# Function to install Docker on CentOS/RHEL
install_docker_rhel() {
    echo -e "${YELLOW}Installing Docker...${NC}"
    
    sudo yum install -y -q yum-utils
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo yum install -y -q docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    echo -e "${GREEN}✓ Docker installed successfully${NC}"
}

# Function to install pip
install_pip() {
    echo -e "${YELLOW}Installing pip...${NC}"
    
    if command -v python3 &> /dev/null; then
        python3 -m ensurepip --default-pip 2>/dev/null || true
        python3 -m pip install --upgrade pip 2>/dev/null || true
    fi
    
    if command -v python &> /dev/null; then
        python -m ensurepip --default-pip 2>/dev/null || true
        python -m pip install --upgrade pip 2>/dev/null || true
    fi
    
    if command -v pip3 &> /dev/null || command -v pip &> /dev/null; then
        echo -e "${GREEN}✓ pip installed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to install pip${NC}"
        return 1
    fi
}

# Function to install Python dependencies
install_dependencies() {
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    
    # Try pip3 first, then pip, then python -m pip
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
    elif command -v pip &> /dev/null; then
        pip install -r requirements.txt
    elif command -v python3 -m pip &> /dev/null; then
        python3 -m pip install -r requirements.txt
    elif command -v python -m pip &> /dev/null; then
        python -m pip install -r requirements.txt
    else
        echo -e "${RED}✗ pip not found, cannot install dependencies${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
}

# Check and install Docker if needed
if ! command -v docker &> /dev/null; then
    if [ "$SKIP_INSTALL" = true ]; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Docker not found. Attempting to install...${NC}"
    
    # Detect OS and install accordingly
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        case "$ID" in
            ubuntu|debian|linuxmint)
                install_docker_ubuntu
                ;;
            centos|rhel|fedora)
                install_docker_rhel
                ;;
            *)
                echo -e "${RED}Error: Unsupported OS for automatic Docker installation: $ID${NC}"
                echo -e "${YELLOW}Please install Docker manually and run this script again.${NC}"
                exit 1
                ;;
        esac
    else
        echo -e "${RED}Error: Cannot detect OS for automatic Docker installation${NC}"
        echo -e "${YELLOW}Please install Docker manually and run this script again.${NC}"
        exit 1
    fi
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${YELLOW}Docker daemon is not running. Attempting to start...${NC}"
    sudo systemctl start docker 2>/dev/null || sudo service docker start 2>/dev/null || true
    
    # Wait for Docker to start
    sleep 3
    
    if ! docker info &> /dev/null; then
        echo -e "${RED}✗ Could not start Docker daemon. Please start Docker manually.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker daemon started${NC}"
fi

echo -e "${GREEN}✓ Docker is available${NC}"

# Check if Docker Compose is available
if ! command -v docker compose &> /dev/null && ! command -v docker-compose &> /dev/null; then
    if [ "$SKIP_INSTALL" = true ]; then
        echo -e "${RED}Error: Docker Compose is not installed${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Docker Compose not found. Installing...${NC}"
    
    # Install Docker Compose standalone
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    echo -e "${GREEN}✓ Docker Compose installed successfully${NC}"
fi

# Set Docker Compose command
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo -e "${GREEN}✓ Docker Compose is available${NC}"

# Install pip if needed (for local development)
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    if [ "$SKIP_INSTALL" = false ]; then
        install_pip || true
    fi
fi

# Install Python dependencies if not using Docker build
if [ "$SKIP_INSTALL" = false ]; then
    if [ -f "requirements.txt" ]; then
        install_dependencies || true
    fi
fi

# Set environment file
ENV_FILE=".env.$ENVIRONMENT"
if [ -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}Using environment file: $ENV_FILE${NC}"
    export ENV_FILE
else
    if [ -f ".env" ]; then
        echo -e "${YELLOW}Using default .env file${NC}"
    else
        echo -e "${RED}Error: No environment file found (.env or $ENV_FILE)${NC}"
        exit 1
    fi
fi

# Build the image
echo -e "${YELLOW}Building Docker image...${NC}"
IMAGE_TAG="${REGISTRY}${IMAGE_NAME}:${TAG}"
docker build -t "$IMAGE_TAG" -f docker/Dockerfile .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Image built successfully${NC}"
else
    echo -e "${RED}✗ Image build failed${NC}"
    exit 1
fi

# Pull optional services (redis, postgres) if needed
echo -e "${YELLOW}Pulling supporting services...${NC}"
$DOCKER_COMPOSE -f "$COMPOSE_FILE" pull redis postgres 2>/dev/null || true

# Start the services
echo -e "${YELLOW}Starting services...${NC}"
ENVIRONMENT="$ENVIRONMENT" $DOCKER_COMPOSE -f "$COMPOSE_FILE" up -d

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Services started successfully${NC}"
else
    echo -e "${RED}✗ Failed to start services${NC}"
    exit 1
fi

# Wait for services to be healthy
echo -e "${YELLOW}Waiting for services to be healthy...${NC}"
sleep 5

# Check service status
echo ""
echo -e "${BLUE}Service Status:${NC}"
$DOCKER_COMPOSE -f "$COMPOSE_FILE" ps

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Application: ${CYAN}http://localhost:8000${NC}"
echo -e "API Docs:    ${CYAN}http://localhost:8000/docs${NC}"
echo ""
