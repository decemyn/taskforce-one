"""Unit tests for ConfigLoader."""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from taskforce_one.config.loader import (
    AppSettings,
    ConfigLoader,
    LLMSettings,
    get_config,
)


class TestLLMSettings:
    """Tests for LLMSettings."""

    def test_default_values(self):
        """Test default LLM settings."""
        settings = LLMSettings()
        assert settings.provider == "openai"
        assert settings.model == "gpt-4"
        assert settings.temperature == 0.7
        assert settings.max_tokens == 2000
        assert settings.timeout == 60

    def test_custom_values(self):
        """Test custom LLM settings."""
        settings = LLMSettings(
            provider="anthropic",
            model="claude-3",
            temperature=0.5,
            max_tokens=4000,
            timeout=120,
        )
        assert settings.provider == "anthropic"
        assert settings.model == "claude-3"
        assert settings.temperature == 0.5
        assert settings.max_tokens == 4000
        assert settings.timeout == 120


class TestConfigLoader:
    """Tests for ConfigLoader."""

    def test_default_config_dir(self):
        """Test default configuration directory."""
        # Set environment variable to override default
        with pytest.MonkeyPatch.context() as mp:
            mp.delenv("CONFIG_DIR", raising=False)
            loader = ConfigLoader()
            # Should default to /app/config in container or similar
            assert loader.config_dir is not None

    def test_custom_config_dir(self, temp_config_dir):
        """Test custom configuration directory."""
        loader = ConfigLoader(config_dir=temp_config_dir)
        assert loader.config_dir == temp_config_dir

    def test_load_agents_from_file(self, config_files):
        """Test loading agents from YAML file."""
        loader = ConfigLoader(config_dir=config_files)
        agents = loader.load_agents()

        assert "test_agent" in agents
        assert agents["test_agent"]["role"] == "Test Agent"
        assert agents["test_agent"]["goal"] == "Test goal"

    def test_load_crews_from_file(self, config_files):
        """Test loading crews from YAML file."""
        loader = ConfigLoader(config_dir=config_files)
        crews = loader.load_crews()

        assert "test_crew" in crews
        assert crews["test_crew"]["name"] == "Test Crew"
        assert crews["test_crew"]["agents"] == ["test_agent"]

    def test_load_settings_from_file(self, config_files):
        """Test loading settings from YAML file."""
        loader = ConfigLoader(config_dir=config_files)
        settings = loader.settings

        assert settings.app_name == "Task Force One"
        assert settings.api.host == "0.0.0.0"
        assert settings.api.port == 8000

    def test_load_agents_empty_directory(self, temp_config_dir):
        """Test loading agents from directory with no agents file."""
        loader = ConfigLoader(config_dir=temp_config_dir)
        agents = loader.load_agents()

        assert agents == {}

    def test_load_crews_empty_directory(self, temp_config_dir):
        """Test loading crews from directory with no crews file."""
        loader = ConfigLoader(config_dir=temp_config_dir)
        crews = loader.load_crews()

        assert crews == {}

    def test_get_agent_config(self, config_files):
        """Test getting specific agent configuration."""
        loader = ConfigLoader(config_dir=config_files)
        agent = loader.get_agent_config("test_agent")

        assert agent is not None
        assert agent["role"] == "Test Agent"

    def test_get_agent_config_not_found(self, config_files):
        """Test getting non-existent agent configuration."""
        loader = ConfigLoader(config_dir=config_files)
        agent = loader.get_agent_config("nonexistent")

        assert agent is None

    def test_get_crew_config(self, config_files):
        """Test getting specific crew configuration."""
        loader = ConfigLoader(config_dir=config_files)
        crew = loader.get_crew_config("test_crew")

        assert crew is not None
        assert crew["name"] == "Test Crew"

    def test_get_crew_config_not_found(self, config_files):
        """Test getting non-existent crew configuration."""
        loader = ConfigLoader(config_dir=config_files)
        crew = loader.get_crew_config("nonexistent")

        assert crew is None

    def test_reload(self, config_files):
        """Test reloading configuration."""
        loader = ConfigLoader(config_dir=config_files)

        # Load first time
        agents1 = loader.load_agents()
        assert "test_agent" in agents1

        # Modify the file
        agents_file = config_files / "agents.yaml"
        with open(agents_file, "w") as f:
            yaml.dump({"agents": []}, f)

        # Reload should get new data
        loader.reload()
        agents2 = loader.load_agents()
        assert agents2 == {}

    def test_config_dir_from_env_var(self, temp_config_dir, monkeypatch):
        """Test config directory from environment variable."""
        monkeypatch.setenv("CONFIG_DIR", str(temp_config_dir))
        loader = ConfigLoader()
        assert loader.config_dir == temp_config_dir


class TestGetConfig:
    """Tests for get_config function."""

    def test_get_config_singleton(self, temp_config_dir):
        """Test that get_config returns a singleton."""
        config1 = get_config(config_dir=temp_config_dir)
        config2 = get_config(config_dir=temp_config_dir)

        assert config1 is config2

    def test_get_config_different_dirs(self, temp_config_dir):
        """Test get_config with different directories."""
        import taskforce_one.config.loader as loader_module

        # Reset global to test fresh instances
        loader_module._config = None

        config1 = get_config(config_dir=temp_config_dir)

        # Reset again for second instance
        loader_module._config = None

        with tempfile.TemporaryDirectory() as tmpdir:
            config2 = get_config(config_dir=Path(tmpdir))

            # After getting with different dir, should be different instance
            assert config1.config_dir != config2.config_dir


class TestAppSettings:
    """Tests for AppSettings."""

    def test_default_settings(self):
        """Test default application settings."""
        settings = AppSettings()

        assert settings.app_name == "Task Force One"
        assert settings.app_version == "0.1.0"
        assert settings.environment == "development"

    def test_settings_from_env(self, monkeypatch):
        """Test settings from environment variables."""
        monkeypatch.setenv("APP_NAME", "Custom App")
        monkeypatch.setenv("ENVIRONMENT", "production")

        settings = AppSettings()

        assert settings.app_name == "Custom App"
        assert settings.environment == "production"
