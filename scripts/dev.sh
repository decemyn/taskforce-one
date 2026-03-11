#!/bin/bash
# Development environment setup script for Task Force One

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
PYTHON_VERSION="3.11"
VENV_NAME=".venv"
INSTALL_DEPS=true
INSTALL_DEV=true

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --python-version)
            PYTHON_VERSION="$2"
            shift 2
            ;;
        --venv-name)
            VENV_NAME="$2"
            shift 2
            ;;
        --no-deps)
            INSTALL_DEPS=false
            shift
            ;;
        --no-dev)
            INSTALL_DEV=false
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --python-version VERSION  Python version to use (default: 3.11)"
            echo "  --venv-name NAME         Virtual environment name (default: .venv)"
            echo "  --no-deps               Skip dependency installation"
            echo "  --no-dev                Skip dev dependency installation"
            echo "  -h                      Show this help message"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

echo -e "${GREEN}Setting up Task Force One Development Environment${NC}"
echo "====================================================="

# Check Python version
echo ""
echo -e "${BLUE}Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo -e "${RED}Python not found! Please install Python $PYTHON_VERSION${NC}"
    exit 1
fi

PYTHON_VER=$($PYTHON_CMD --version 2>&1)
echo "Found: $PYTHON_VER"

# Check for uv (preferred) or pip
echo ""
echo -e "${BLUE}Checking package manager...${NC}"
if command -v uv &> /dev/null; then
    echo "Using uv for package management"
    PKG_MANAGER="uv"
elif command -v pip &> /dev/null; then
    echo "Using pip for package management"
    PKG_MANAGER="pip"
else
    echo -e "${RED}No package manager found!${NC}"
    exit 1
fi

# Create virtual environment
echo ""
echo -e "${BLUE}Creating virtual environment...${NC}"
if [ -d "$VENV_NAME" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Using it...${NC}"
else
    $PYTHON_CMD -m venv $VENV_NAME
    echo "Created virtual environment: $VENV_NAME"
fi

# Activate virtual environment
echo ""
echo -e "${BLUE}Activating virtual environment...${NC}"
if [ -f "$VENV_NAME/bin/activate" ]; then
    source "$VENV_NAME/bin/activate"
elif [ -f "$VENV_NAME/Scripts/activate" ]; then
    source "$VENV_NAME/Scripts/activate"
fi
echo "Activated: $(which python)"

# Upgrade pip
echo ""
echo -e "${BLUE}Upgrading pip...${NC}"
python3 -m pip install --upgrade pip

# Install dependencies
if [ "$INSTALL_DEPS" = true ]; then
    echo ""
    echo -e "${BLUE}Installing dependencies...${NC}"
    if [ "$PKG_MANAGER" = "uv" ]; then
        uv pip install -e .
    else
        python3 -m pip install -e .
    fi
fi

# Install dev dependencies
if [ "$INSTALL_DEV" = true ]; then
    echo ""
    echo -e "${BLUE}Installing dev dependencies...${NC}"
    if [ "$PKG_MANAGER" = "uv" ]; then
        uv pip install -e ".[dev]"
    else
        python3 -m pip install -e ".[dev]"
    fi
fi

# Verify installation
echo ""
echo -e "${BLUE}Verifying installation...${NC}"
python -c "import taskforce_one; print(f'Task Force One version: {taskforce_one.__version__}')"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo -e "${BLUE}Creating .env file from template...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Created .env file. Please edit it with your settings."
    fi
fi

echo ""
echo "====================================================="
echo -e "${GREEN}Development environment setup complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. Run 'source $VENV_NAME/bin/activate' to activate the venv"
echo "  3. Run './scripts/test.sh' to run tests"
echo "  4. Run './scripts/dev.sh' to start development server"
