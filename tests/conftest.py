"""Shared pytest fixtures for Task Force One tests."""

import os
import sys
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
import yaml

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def temp_config_dir() -> Generator[Path, None, None]:
    """Create a temporary configuration directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir) / "config"
        config_dir.mkdir()
        yield config_dir


@pytest.fixture
def sample_agents_config() -> list:
    """Sample agents configuration."""
    return [
        {
            "id": "test_agent",
            "role": "Test Agent",
            "goal": "Test goal",
            "backstory": "Test backstory",
            "verbose": True,
            "max_iterations": 5,
            "allow_delegation": False,
        },
        {
            "id": "researcher",
            "role": "Senior Researcher",
            "goal": "Research and gather accurate information",
            "backstory": "You are an experienced researcher",
            "verbose": True,
            "max_iterations": 10,
            "allow_delegation": True,
        },
    ]


@pytest.fixture
def sample_crews_config() -> list:
    """Sample crews configuration."""
    return [
        {
            "id": "test_crew",
            "name": "Test Crew",
            "description": "A test crew",
            "agents": ["test_agent"],
            "process": "sequential",
            "verbose": True,
            "memory": True,
            "max_iterations": 10,
        },
    ]


@pytest.fixture
def sample_settings_config() -> dict:
    """Sample settings configuration."""
    return {
        "app": {
            "name": "Task Force One",
            "version": "0.1.0",
        },
        "api": {
            "host": "0.0.0.0",
            "port": 8000,
            "reload": False,
            "workers": 1,
            "log_level": "info",
        },
        "llm": {
            "provider": "openai",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "timeout": 60,
        },
        "storage": {
            "type": "local",
            "path": "./data",
            "redis_host": "localhost",
            "redis_port": 6379,
            "postgres_host": "localhost",
            "postgres_port": 5432,
        },
        "logging": {
            "level": "INFO",
            "file": "./logs/taskforce.log",
            "rotation": "100 MB",
            "retention": "30 days",
        },
    }


@pytest.fixture
def config_files(temp_config_dir, sample_agents_config, sample_crews_config, sample_settings_config) -> Path:
    """Create configuration files in temp directory."""
    # Write agents.yaml
    agents_file = temp_config_dir / "agents.yaml"
    with open(agents_file, "w") as f:
        yaml.dump({"agents": sample_agents_config}, f)
    
    # Write crews.yaml
    crews_file = temp_config_dir / "crews.yaml"
    with open(crews_file, "w") as f:
        yaml.dump({"crews": sample_crews_config}, f)
    
    # Write settings.yaml
    settings_file = temp_config_dir / "settings.yaml"
    with open(settings_file, "w") as f:
        yaml.dump(sample_settings_config, f)
    
    return temp_config_dir


@pytest.fixture
def mock_crew_agent():
    """Mock CrewAI Agent."""
    with patch("taskforce_one.agents.base.CrewAgent") as mock:
        mock_instance = MagicMock()
        mock_instance.execute_task.return_value = "Mock task result"
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_crew():
    """Mock CrewAI Crew."""
    with patch("taskforce_one.crews.base.Crew") as mock:
        mock_instance = MagicMock()
        mock_instance.kickoff.return_value = "Mock crew result"
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_config_dir(monkeypatch, config_files):
    """Set CONFIG_DIR environment variable for tests."""
    monkeypatch.setenv("CONFIG_DIR", str(config_files))
    yield config_files


@pytest.fixture
def api_client():
    """Create a test client for the FastAPI app."""
    from fastapi.testclient import TestClient
    from taskforce_one.api import app
    
    with patch("taskforce_one.config.loader.ConfigLoader") as mock_loader:
        # Setup mock to return test config
        mock_instance = MagicMock()
        mock_instance.load_agents.return_value = {
            "test_agent": {
                "id": "test_agent",
                "role": "Test Agent",
                "goal": "Test goal",
                "backstory": "Test backstory",
            }
        }
        mock_instance.load_crews.return_value = {}
        mock_loader.return_value = mock_instance
        
        with TestClient(app) as client:
            yield client


@pytest.fixture
def isolated_config():
    """Isolate config by resetting global state."""
    import taskforce_one.config.loader as loader_module
    
    # Reset global config
    loader_module._config = None
    
    yield
    
    # Cleanup after test
    loader_module._config = None


@pytest.fixture
def isolated_registry():
    """Isolate tool registry by resetting global state."""
    import taskforce_one.tools.registry as registry_module
    
    # Reset global registry
    registry_module._registry = None
    
    yield
    
    # Cleanup after test
    registry_module._registry = None
