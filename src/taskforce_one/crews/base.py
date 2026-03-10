"""Base Crew Implementation for Task Force One

Provides a foundation for creating crew workflows with CrewAI.
"""

from collections.abc import Sequence
from typing import Any

from crewai import Crew, Task
from loguru import logger

from taskforce_one.agents.base import BaseAgent


class BaseCrew:
    """Base class for Task Force One crews.

    This class provides a wrapper around CrewAI's Crew with
    additional functionality specific to Task Force One.
    """

    def __init__(
        self,
        name: str,
        description: str,
        agents: Sequence[BaseAgent],
        process: str = "sequential",
        verbose: bool = True,
        memory: bool = True,
        max_iterations: int = 10,
    ):
        """Initialize a base crew.

        Args:
            name: The name of the crew
            description: Description of the crew's purpose
            agents: List of agents in the crew
            process: Process type (sequential or hierarchical)
            verbose: Enable verbose output
            memory: Enable crew memory
            max_iterations: Maximum iterations for the crew
        """
        self.name = name
        self.description = description
        self.agents = agents
        self.process = process
        self.verbose = verbose
        self.memory = memory
        self.max_iterations = max_iterations

        self._crew: Crew | None = None
        self._tasks: list[Task] = []
        self._id = name.lower().replace(" ", "_")

    @property
    def id(self) -> str:
        """Get the crew's unique identifier."""
        return self._id

    @property
    def crew(self) -> Crew:
        """Get the underlying CrewAI crew."""
        if self._crew is None:
            self._crew = self._create_crew()
        return self._crew

    def _create_crew(self) -> Crew:
        """Create the underlying CrewAI crew."""
        crew_agents = [agent.crew_agent for agent in self.agents]

        return Crew(
            agents=crew_agents,  # type: ignore[arg-type]
            tasks=self._tasks,
            process=self.process,  # type: ignore[arg-type]
            verbose=self.verbose,
            memory=self.memory,
        )

    def add_task(self, task: Task) -> "BaseCrew":
        """Add a task to the crew.

        Args:
            task: The task to add

        Returns:
            Self for method chaining
        """
        self._tasks.append(task)
        # Reset crew to rebuild with new tasks
        self._crew = None
        return self

    def add_tasks(self, tasks: list[Task]) -> "BaseCrew":
        """Add multiple tasks to the crew.

        Args:
            tasks: List of tasks to add

        Returns:
            Self for method chaining
        """
        for task in tasks:
            self.add_task(task)
        return self

    def execute(self, input_data: str) -> str:
        """Execute the crew with input data.

        Args:
            input_data: Input data for the crew

        Returns:
            The result of the crew execution
        """
        logger.info(f"Crew {self.id} starting execution...")
        result = self.crew.kickoff(inputs={"input": input_data})
        logger.info(f"Crew {self.id} execution complete")
        return str(result)

    def execute_async(self, input_data: str) -> Any:
        """Execute the crew asynchronously.

        Args:
            input_data: Input data for the crew

        Returns:
            Future result of the crew execution
        """
        logger.info(f"Crew {self.id} starting async execution...")
        return self.crew.kickoff_async(inputs={"input": input_data})

    def __repr__(self) -> str:
        return f"<BaseCrew(id={self.id}, name={self.name}, agents={len(self.agents)})>"


class CrewFactory:
    """Factory for creating crews from configuration."""

    @staticmethod
    def from_config(
        config: dict[str, Any],
        agents: list[BaseAgent],
    ) -> BaseCrew:
        """Create a crew from configuration.

        Args:
            config: Crew configuration dictionary
            agents: List of available agents

        Returns:
            BaseCrew instance
        """
        agent_map = {agent.id: agent for agent in agents}

        # Get agents for this crew
        crew_agents = []
        for agent_id in config.get("agents", []):
            if agent_id in agent_map:
                crew_agents.append(agent_map[agent_id])

        return BaseCrew(
            name=config.get("name", ""),
            description=config.get("description", ""),
            agents=crew_agents,
            process=config.get("process", "sequential"),
            verbose=config.get("verbose", True),
            memory=config.get("memory", True),
            max_iterations=config.get("max_iterations", 10),
        )

    @staticmethod
    def create_multiple(
        configs: list[dict[str, Any]],
        agents: list[BaseAgent],
    ) -> list[BaseCrew]:
        """Create multiple crews from configurations.

        Args:
            configs: List of crew configurations
            agents: List of available agents

        Returns:
            List of BaseCrew instances
        """
        return [
            CrewFactory.from_config(config, agents)
            for config in configs
        ]
