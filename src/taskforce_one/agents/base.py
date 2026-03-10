"""Base Agent Implementation for Task Force One

Provides a foundation for creating custom agents with CrewAI.
"""

from typing import Any

from crewai import Agent as CrewAgent
from loguru import logger


class BaseAgent:
    """Base class for Task Force One agents.

    This class provides a wrapper around CrewAI's Agent with
    additional functionality specific to Task Force One.
    """

    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        verbose: bool = True,
        max_iterations: int = 5,
        allow_delegation: bool = False,
        tools: list[Any] | None = None,
        llm_config: dict[str, Any] | None = None,
    ):
        """Initialize a base agent.

        Args:
            role: The role/role of the agent
            goal: The goal the agent aims to achieve
            backstory: The backstory/personality of the agent
            verbose: Enable verbose output
            max_iterations: Maximum iterations for the agent
            allow_delegation: Allow the agent to delegate tasks
            tools: List of tools available to the agent
            llm_config: LLM configuration overrides
        """
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        self.max_iterations = max_iterations
        self.allow_delegation = allow_delegation
        self.tools = tools or []
        self.llm_config = llm_config or {}

        self._agent: CrewAgent | None = None
        self._id = role.lower().replace(" ", "_")

    @property
    def id(self) -> str:
        """Get the agent's unique identifier."""
        return self._id

    @property
    def crew_agent(self) -> CrewAgent:
        """Get the underlying CrewAI agent."""
        if self._agent is None:
            self._agent = self._create_agent()
        return self._agent

    def _create_agent(self) -> CrewAgent:
        """Create the underlying CrewAI agent."""
        return CrewAgent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=self.verbose,
            max_iterations=self.max_iterations,
            allow_delegation=self.allow_delegation,
            tools=self.tools,
        )

    def execute(self, task: str) -> str:
        """Execute a task with this agent.

        Args:
            task: The task description

        Returns:
            The result of the task execution
        """
        logger.info(f"Agent {self.id} executing task: {task[:50]}...")
        result = self.crew_agent.execute_task(task)
        return result

    def __repr__(self) -> str:
        return f"<BaseAgent(id={self.id}, role={self.role})>"


class AgentFactory:
    """Factory for creating agents from configuration."""

    @staticmethod
    def from_config(config: dict[str, Any]) -> BaseAgent:
        """Create an agent from configuration.

        Args:
            config: Agent configuration dictionary

        Returns:
            BaseAgent instance
        """
        return BaseAgent(
            role=config.get("role", ""),
            goal=config.get("goal", ""),
            backstory=config.get("backstory", ""),
            verbose=config.get("verbose", True),
            max_iterations=config.get("max_iterations", 5),
            allow_delegation=config.get("allow_delegation", False),
            tools=config.get("tools", []),
            llm_config=config.get("llm", {}),
        )

    @staticmethod
    def create_multiple(configs: list[dict[str, Any]]) -> list[BaseAgent]:
        """Create multiple agents from configurations.

        Args:
            configs: List of agent configurations

        Returns:
            List of BaseAgent instances
        """
        return [AgentFactory.from_config(config) for config in configs]
