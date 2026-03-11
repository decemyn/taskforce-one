"""Base Agent Implementation for Task Force One

Provides a foundation for creating custom agents with CrewAI.
"""

from typing import Any

from crewai import Agent as CrewAgent
from crewai import Task
from loguru import logger

from taskforce_one.llm import DynamicLLMLoader


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
        agent_id: str | None = None,
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
        self.llm: Any = None

        self._agent: CrewAgent | None = None
        self._id = agent_id or role.lower().replace(" ", "_")

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
        kwargs: dict[str, Any] = {
            "role": self.role,
            "goal": self.goal,
            "backstory": self.backstory,
            "verbose": self.verbose,
            "max_iterations": self.max_iterations,
            "allow_delegation": self.allow_delegation,
            "tools": self.tools,
        }

        # If an LLM was successfully loaded dynamically, inject it
        if self.llm is not None:
            kwargs["llm"] = self.llm

        return CrewAgent(**kwargs)

    def execute(self, task: str) -> str:
        """Execute a task with this agent.

        Args:
            task: The task description

        Returns:
            The result of the task execution
        """
        logger.info(f"Agent {self.id} executing task: {task[:50]}...")
        # Create a Task from the string description
        crew_task = Task(
            description=task, expected_output="Task completion result", agent=self.crew_agent
        )
        result = self.crew_agent.execute_task(crew_task)
        return str(result)

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
        agent = BaseAgent(
            role=config.get("role", ""),
            goal=config.get("goal", ""),
            backstory=config.get("backstory", ""),
            verbose=config.get("verbose", True),
            max_iterations=config.get("max_iterations", 5),
            allow_delegation=config.get("allow_delegation", False),
            tools=config.get("tools", []),
            llm_config=config.get("llm", {}),
            agent_id=config.get("id"),
        )

        # Process dynamic LLM loading if defined in configuration
        llm_config = agent.llm_config
        provider_module = llm_config.get("provider_module")
        provider_class = llm_config.get("provider_class")
        provider_config = llm_config.get("config", {})

        if provider_module and provider_class:
            try:
                langchain_llm = DynamicLLMLoader.load(
                    provider_module=provider_module,
                    provider_class=provider_class,
                    config=provider_config,
                )
                # Wrap the LangChain model in a CrewAI-compatible adapter
                from taskforce_one.llm.crewai_adapter import LangChainLLMAdapter
                agent.llm = LangChainLLMAdapter(langchain_llm)
                logger.info(
                    f"Wrapped {provider_class} in LangChainLLMAdapter for agent '{agent.id}'"
                )
            except Exception as e:
                logger.warning(
                    f"Failed to load dynamic LLM {provider_module}.{provider_class} "
                    f"for agent '{agent.id}': {e}. Falling back to default."
                )

        return agent

    @staticmethod
    def create_multiple(configs: list[dict[str, Any]]) -> list[BaseAgent]:
        """Create multiple agents from configurations.

        Args:
            configs: List of agent configurations

        Returns:
            List of BaseAgent instances
        """
        return [AgentFactory.from_config(config) for config in configs]
