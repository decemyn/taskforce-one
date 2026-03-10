# Task Force One

A powerful orchestration toolkit built on [CrewAI](https://crewai.com) for creating multi-agent systems for Micro SaaS applications.

## Overview

Task Force One provides a comprehensive framework for building, deploying, and managing AI agent workflows. It leverages CrewAI's powerful multi-agent orchestration capabilities while adding:

- **Configuration-driven** agent and crew definitions
- **Docker-first** deployment pipeline
- **REST API** for integration
- **CLI tools** for quick operations
- **Extensible architecture** for custom agents and tools

## Features

- 🔧 **Agent Management** - Define agents via YAML configuration
- ⚙️ **Crew Workflows** - Orchestrate multi-agent workflows
- 🐳 **Docker Deployment** - Production-ready containers
- 🌐 **REST API** - FastAPI-based API server
- 📦 **CLI Tools** - Command-line interface for quick tasks
- 🔄 **Hot Reload** - Development with live reloading
- 📊 **Monitoring** - Prometheus metrics support (optional)

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- API keys for your chosen LLM provider

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/taskforce-one.git
cd taskforce-one
```

2. Run the setup script:
```bash
./scripts/setup.sh
```

3. Configure your environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Start the API server:
```bash
./scripts/run.sh
```

The API will be available at `http://localhost:8000`

### Docker Deployment

```bash
# Build and run with Docker
./scripts/deploy.sh

# Or use Docker Compose directly
cd docker
docker-compose up -d
```

## Configuration

### Agent Configuration (`config/agents.yaml`)

Define your agents with custom roles, goals, and backstories:

```yaml
agents:
  - id: "researcher"
    role: "Senior Researcher"
    goal: "Research and gather accurate information"
    backstory: "You are an experienced researcher..."
```

### Crew Configuration (`config/crews.yaml`)

Define crew workflows:

```yaml
crews:
  - id: "content_creation"
    name: "Content Creation Crew"
    process: "sequential"
    agents:
      - "researcher"
      - "writer"
      - "editor"
```

### Settings (`config/settings.yaml`)

Configure application settings, LLM providers, storage, and more.

## API Usage

### List Agents
```bash
curl http://localhost:8000/agents
```

### List Crews
```bash
curl http://localhost:8000/crews
```

### Execute Agent
```bash
curl -X POST http://localhost:8000/agents/researcher/execute \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "researcher", "task": "Research AI trends in 2024"}'
```

### Execute Crew
```bash
curl -X POST http://localhost:8000/crews/content_creation/execute \
  -H "Content-Type: application/json" \
  -d '{"crew_id": "content_creation", "input_data": "Write about AI trends"}'
```

## CLI Usage

```bash
# Show version
taskforce info

# List agents
taskforce list-agents

# List crews
taskforce list-crews

# Run an agent
taskforce run-agent researcher "Research AI trends"

# Run a crew
taskforce run-crew content_creation "Write about AI"

# Start API server
taskforce serve
```

## Project Structure

```
taskforce-one/
├── config/              # Configuration files
│   ├── agents.yaml     # Agent definitions
│   ├── crews.yaml     # Crew definitions
│   └── settings.yaml  # Application settings
├── docker/            # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/           # Deployment scripts
│   ├── setup.sh
│   ├── run.sh
│   └── deploy.sh
├── src/taskforce_one/ # Source code
│   ├── agents/       # Agent implementations
│   ├── crews/       # Crew implementations
│   ├── tools/       # Tool registry
│   ├── config/      # Configuration loader
│   ├── api.py       # FastAPI application
│   └── cli.py       # CLI tools
└── tests/           # Test files
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Lint
ruff check src/

# Type check
mypy src/
```

## Deployment Options

### Local Development
```bash
./scripts/run.sh
```

### Docker (Recommended)
```bash
./scripts/deploy.sh --env production
```

### Cloud Platforms
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- Kubernetes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- Documentation: [docs.taskforce.one](https://docs.taskforce.one)
- Issues: [GitHub Issues](https://github.com/yourusername/taskforce-one/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/taskforce-one/discussions)
