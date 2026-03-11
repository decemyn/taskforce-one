"""Unit tests for BaseAgent and AgentFactory."""

from unittest.mock import MagicMock, patch

import pytest

from taskforce_one.agents.base import AgentFactory, BaseAgent


class TestBaseAgent:
    """Tests for BaseAgent class."""

    def test_agent_initialization(self):
        """Test agent initialization with required parameters."""
        agent = BaseAgent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
        )

        assert agent.role == "Test Agent"
        assert agent.goal == "Test goal"
        assert agent.backstory == "Test backstory"
        assert agent.verbose is True
        assert agent.max_iterations == 5
        assert agent.allow_delegation is False

    def test_agent_initialization_with_options(self):
        """Test agent initialization with optional parameters."""
        agent = BaseAgent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
            verbose=False,
            max_iterations=10,
            allow_delegation=True,
        )

        assert agent.verbose is False
        assert agent.max_iterations == 10
        assert agent.allow_delegation is True

    def test_agent_id(self):
        """Test agent ID generation."""
        agent = BaseAgent(
            role="Senior Researcher",
            goal="Test goal",
            backstory="Test backstory",
        )

        assert agent.id == "senior_researcher"

    def test_agent_id_with_spaces(self):
        """Test agent ID with spaces in role."""
        agent = BaseAgent(
            role="Content Writer",
            goal="Test goal",
            backstory="Test backstory",
        )

        assert agent.id == "content_writer"

    def test_agent_tools(self):
        """Test agent tools initialization."""
        mock_tool = MagicMock()
        agent = BaseAgent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
            tools=[mock_tool],
        )

        assert len(agent.tools) == 1
        assert agent.tools[0] is mock_tool

    def test_agent_llm_config(self):
        """Test agent LLM configuration."""
        llm_config = {"model": "gpt-4", "temperature": 0.5}
        agent = BaseAgent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
            llm_config=llm_config,
        )

        assert agent.llm_config == llm_config

    def test_agent_repr(self):
        """Test agent string representation."""
        agent = BaseAgent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
        )

        assert "BaseAgent" in repr(agent)
        assert "test_agent" in repr(agent)
        assert "Test Agent" in repr(agent)

    @patch("taskforce_one.agents.base.CrewAgent")
    def test_crew_agent_creation(self, mock_crew_agent):
        """Test CrewAI agent creation."""
        agent = BaseAgent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
        )

        crew = agent.crew_agent

        assert crew is not None
        mock_crew_agent.assert_called_once()
        call_kwargs = mock_crew_agent.call_args[1]
        assert call_kwargs["role"] == "Test Agent"
        assert call_kwargs["goal"] == "Test goal"
        assert call_kwargs["backstory"] == "Test backstory"

    @patch("taskforce_one.agents.base.CrewAgent")
    def test_crew_agent_cached(self, mock_crew_agent):
        """Test that CrewAI agent is cached."""
        agent = BaseAgent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
        )

        # Call crew_agent twice
        _ = agent.crew_agent
        _ = agent.crew_agent

        # Should only create once
        assert mock_crew_agent.call_count == 1


class TestAgentFactory:
    """Tests for AgentFactory class."""

    def test_from_config_minimal(self):
        """Test creating agent from minimal config."""
        config = {
            "role": "Test Agent",
            "goal": "Test goal",
            "backstory": "Test backstory",
        }

        agent = AgentFactory.from_config(config)

        assert agent.role == "Test Agent"
        assert agent.goal == "Test goal"
        assert agent.backstory == "Test backstory"

    def test_from_config_full(self):
        """Test creating agent from full config."""
        config = {
            "role": "Test Agent",
            "goal": "Test goal",
            "backstory": "Test backstory",
            "verbose": False,
            "max_iterations": 10,
            "allow_delegation": True,
            "tools": [],
            "llm": {"model": "gpt-4"},
        }

        agent = AgentFactory.from_config(config)

        assert agent.verbose is False
        assert agent.max_iterations == 10
        assert agent.allow_delegation is True
        assert agent.llm_config == {"model": "gpt-4"}

    def test_from_config_defaults(self):
        """Test creating agent with default values."""
        config = {
            "role": "Test Agent",
            "goal": "Test goal",
        }

        agent = AgentFactory.from_config(config)

        assert agent.backstory == ""
        assert agent.verbose is True
        assert agent.max_iterations == 5
        assert agent.allow_delegation is False

    def test_create_multiple(self):
        """Test creating multiple agents."""
        configs = [
            {"role": "Agent 1", "goal": "Goal 1", "backstory": "Backstory 1"},
            {"role": "Agent 2", "goal": "Goal 2", "backstory": "Backstory 2"},
        ]

        agents = AgentFactory.create_multiple(configs)

        assert len(agents) == 2
        assert agents[0].role == "Agent 1"
        assert agents[1].role == "Agent 2"

    def test_create_multiple_empty_list(self):
        """Test creating multiple agents from empty list."""
        agents = AgentFactory.create_multiple([])

        assert len(agents) == 0
