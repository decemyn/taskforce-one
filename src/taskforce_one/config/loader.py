"""Configuration Loader for Task Force One

Loads and manages configuration from YAML files and environment variables.
"""

import os
from pathlib import Path
from typing import Any

import yaml
from loguru import logger
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class LLMSettings(BaseModel):
    """LLM provider settings."""
    provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 60


class APISettings(BaseModel):
    """API server settings."""
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    workers: int = 1
    log_level: str = "info"


class StorageSettings(BaseModel):
    """Storage configuration."""
    type: str = "local"
    path: str = "./data"
    redis_host: str = "localhost"
    redis_port: int = 6379
    postgres_host: str = "localhost"
    postgres_port: int = 5432


class LoggingSettings(BaseModel):
    """Logging configuration."""
    level: str = "INFO"
    file: str = "./logs/taskforce.log"
    rotation: str = "100 MB"
    retention: str = "30 days"


class AppSettings(BaseSettings):
    """Application settings loaded from environment and config files."""

    # App config
    app_name: str = "Task Force One"
    app_version: str = "0.1.0"
    environment: str = "development"

    # API settings
    api: APISettings = APISettings()

    # LLM settings
    llm: LLMSettings = LLMSettings()

    # Storage
    storage: StorageSettings = StorageSettings()

    # Logging
    logging: LoggingSettings = LoggingSettings()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class ConfigLoader:
    """Loads and manages configuration from YAML files and environment."""

    def __init__(self, config_dir: Path | None = None):
        """Initialize the configuration loader.

        Args:
            config_dir: Path to configuration directory. Defaults to /app/config
        """
        if config_dir is None:
            # Check environment variable first
            config_dir_str = os.getenv("CONFIG_DIR")
            if config_dir_str:
                config_dir = Path(config_dir_str)
            else:
                # Default to /app/config (Docker container path)
                config_dir = Path("/app/config")

        self.config_dir = Path(config_dir)
        self._settings: AppSettings | None = None
        self._agents_config: dict[str, Any] | None = None
        self._crews_config: dict[str, Any] | None = None

    @property
    def settings(self) -> AppSettings:
        """Get application settings."""
        if self._settings is None:
            self._settings = self._load_settings()
        return self._settings

    def _load_settings(self) -> AppSettings:
        """Load settings from YAML and environment."""
        settings_file = self.config_dir / "settings.yaml"

        if settings_file.exists():
            with open(settings_file) as f:
                config_data = yaml.safe_load(f)

            # Merge with environment
            return AppSettings(
                app_name=config_data.get("app", {}).get("name", "Task Force One"),
                app_version=config_data.get("app", {}).get("version", "0.1.0"),
                environment=os.getenv("ENVIRONMENT", "development"),
                api=APISettings(**config_data.get("api", {})),
                llm=LLMSettings(**config_data.get("llm", {})),
                storage=StorageSettings(**config_data.get("storage", {})),
                logging=LoggingSettings(**config_data.get("logging", {})),
            )

        return AppSettings()

    def load_agents(self) -> dict[str, Any]:
        """Load agent configurations from YAML."""
        if self._agents_config is None:
            agents_file = self.config_dir / "agents.yaml"

            if agents_file.exists():
                with open(agents_file) as f:
                    data = yaml.safe_load(f)
                    self._agents_config = {agent["id"]: agent for agent in data.get("agents", [])}
            else:
                self._agents_config = {}

        return self._agents_config

    def load_crews(self) -> dict[str, Any]:
        """Load crew configurations from YAML."""
        if self._crews_config is None:
            crews_file = self.config_dir / "crews.yaml"

            if crews_file.exists():
                with open(crews_file) as f:
                    data = yaml.safe_load(f)
                    self._crews_config = {crew["id"]: crew for crew in data.get("crews", [])}
            else:
                self._crews_config = {}

        return self._crews_config

    def get_agent_config(self, agent_id: str) -> dict[str, Any] | None:
        """Get configuration for a specific agent."""
        agents = self.load_agents()
        return agents.get(agent_id)

    def get_crew_config(self, crew_id: str) -> dict[str, Any] | None:
        """Get configuration for a specific crew."""
        crews = self.load_crews()
        return crews.get(crew_id)

    def reload(self) -> None:
        """Reload all configurations."""
        self._settings = None
        self._agents_config = None
        self._crews_config = None
        logger.info("Configuration reloaded")


# Global configuration instance
_config: ConfigLoader | None = None


def get_config(config_dir: Path | None = None) -> ConfigLoader:
    """Get the global configuration instance.

    Args:
        config_dir: Optional path to config directory

    Returns:
        ConfigLoader instance
    """
    global _config
    if _config is None:
        _config = ConfigLoader(config_dir)
    return _config
