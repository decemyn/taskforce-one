# Task Force One - Usage Guide

This guide explains how to use Task Force One's administration scripts, deployment options, and testing features.

## Table of Contents

- [Administration Scripts](#administration-scripts)
- [Building Documentation](#building-documentation)
- [Deployment](#deployment)
- [Testing](#testing)

---

## Administration Scripts

All scripts are located in the `scripts/` directory and can be run with `bash scripts/<script>.sh`.

### Available Scripts

| Script | Purpose |
|--------|---------|
| [`deploy.sh`](scripts/deploy.sh) | Deploy the application using Docker |
| [`dev.sh`](scripts/dev.sh) | Set up development environment |
| [`test.sh`](scripts/test.sh) | Run the test suite |
| [`lint.sh`](scripts/lint.sh) | Run code linters (ruff, mypy) |
| [`format.sh`](scripts/format.sh) | Format code (ruff) |
| [`health.sh`](scripts/health.sh) | Check service health |
| [`logs.sh`](scripts/logs.sh) | View application logs |
| [`docs.sh`](scripts/docs.sh) | Build Sphinx documentation |

---

## Building Documentation

### Docker (Recommended)

```bash
bash scripts/docs.sh
```

This builds and serves the documentation at http://localhost:8080

Custom port:
```bash
bash scripts/docs.sh --port 9000
```

---

## Deployment

### Option 1: Docker Compose (Recommended)

The easiest way to deploy:

```bash
bash scripts/deploy.sh
```

### External Configuration

Task Force One allows loading agent and crew configurations from a location outside its own repository. To use an external configuration directory (e.g., `agents_of_ai/custom_workflow`), set the `CONFIG_DIR` environment variable to the absolute path of your configuration folder before deploying or running the services.

When using Docker Compose, you can provide this path via the environment:

```bash
CONFIG_DIR=$(pwd)/../custom_workflow bash scripts/deploy.sh
```

This will mount your external directory into the container's `/app/config` location, ensuring that your private or proprietary configurations are never committed to the core engine repository.

This script:
1. Checks Docker availability
2. Installs Python dependencies if needed
3. Builds the Docker image
4. Starts PostgreSQL, Redis, and the API services
5. Waits for services to be healthy
6. Reports the application URL

### Manual Deployment

```bash
# Start services
docker compose -f docker/docker-compose.yml up -d

# Check status
docker compose -f docker/docker-compose.yml ps

# View logs
docker compose -f docker/docker-compose.yml logs -f
```

### Service URLs

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Documentation | http://localhost:8080 |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

---

## Testing

### Running Tests

```bash
# Run all tests
bash scripts/test.sh

# Run specific test types
bash scripts/test.sh --unit        # Unit tests only
bash scripts/test.sh --integration # Integration tests only
bash scripts/test.sh --e2e         # End-to-end tests only

# Run with verbose output
bash scripts/test.sh --verbose
```

### Test Coverage

The test suite includes:
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test API endpoints and service interactions
- **E2E Tests**: Test complete deployment workflows

View coverage reports in `htmlcov/index.html` after running tests.

### Running Other Quality Checks

```bash
# Lint code
bash scripts/lint.sh

# Format code
bash scripts/format.sh

# Both lint and format
bash scripts/lint.sh && bash scripts/format.sh
```

---

## Development Workflow

1. **Set up environment**:
   ```bash
   bash scripts/dev.sh
   ```

2. **Make code changes**

3. **Run tests**:
   ```bash
   bash scripts/test.sh
   ```

4. **Fix issues**:
   ```bash
   bash scripts/lint.sh   # Find issues
   bash scripts/format.sh  # Auto-fix formatting
   ```

5. **Build docs** (if changed):
   ```bash
   bash scripts/docs.sh
   ```

6. **Deploy**:
   ```bash
   bash scripts/deploy.sh
   ```

---

## Troubleshooting

### Services not starting

Check Docker is running:
```bash
docker info
```

View logs:
```bash
bash scripts/logs.sh
```

### Tests failing

Run with verbose output:
```bash
bash scripts/test.sh --verbose
```

### Health check fails

Check service status:
```bash
bash scripts/health.sh
```

Force restart services:
```bash
docker compose -f docker/docker-compose.yml restart
```
