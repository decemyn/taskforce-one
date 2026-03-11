"""Unit tests for BaseCrew and CrewFactory."""

from unittest.mock import MagicMock, patch

import pytest

from taskforce_one.agents.base import BaseAgent
from taskforce_one.crews.base import CrewFactory, BaseCrew


class TestBaseCrew:
    """Tests for BaseCrew class."""

    @pytest.fixture
    def mock_agents(self):
        """Create mock agents for testing."""
        agent1 = BaseAgent(
            role="Agent 1",
            goal="Goal 1",
            backstory="Backstory 1",
        )
        agent1._id = "agent_1"
        
        agent2 = BaseAgent(
            role="Agent 2",
            goal="Goal 2",
            backstory="Backstory 2",
        )
        agent2._id = "agent_2"
        
        return [agent1, agent2]

    def test_crew_initialization(self, mock_agents):
        """Test crew initialization with required parameters."""
        crew = BaseCrew(
            name="Test Crew",
            description="Test description",
            agents=mock_agents,
        )
        
        assert crew.name == "Test Crew"
        assert crew.description == "Test description"
        assert len(crew.agents) == 2
        assert crew.process == "sequential"
        assert crew.verbose is True
        assert crew.memory is True
        assert crew.max_iterations == 10

    def test_crew_initialization_with_options(self, mock_agents):
        """Test crew initialization with optional parameters."""
        crew = BaseCrew(
            name="Test Crew",
            description="Test description",
            agents=mock_agents,
            process="hierarchical",
            verbose=False,
            memory=False,
            max_iterations=20,
        )
        
        assert crew.process == "hierarchical"
        assert crew.verbose is False
        assert crew.memory is False
        assert crew.max_iterations == 20

    def test_crew_id(self, mock_agents):
        """Test crew ID generation."""
        crew = BaseCrew(
            name="Test Crew",
            description="Test description",
            agents=mock_agents,
        )
        
        assert crew.id == "test_crew"

    def test_crew_id_with_spaces(self, mock_agents):
        """Test crew ID with spaces in name."""
        crew = BaseCrew(
            name="Content Creation Crew",
            description="Test description",
            agents=mock_agents,
        )
        
        assert crew.id == "content_creation_crew"

    def test_crew_repr(self, mock_agents):
        """Test crew string representation."""
        crew = BaseCrew(
            name="Test Crew",
            description="Test description",
            agents=mock_agents,
        )
        
        assert "BaseCrew" in repr(crew)
        assert "test_crew" in repr(crew)
        assert "Test Crew" in repr(crew)
        assert "2" in repr(crew)  # 2 agents

    @patch("taskforce_one.crews.base.Crew")
    @patch("taskforce_one.agents.base.CrewAgent")
    def test_crew_creation(self, mock_agent, mock_crew, mock_agents):
        """Test CrewAI crew creation."""
        mock_agent.return_value = MagicMock()
        crew = BaseCrew(
            name="Test Crew",
            description="Test description",
            agents=mock_agents,
        )
        
        result = crew.crew
        
        assert result is not None
        mock_crew.assert_called_once()
        call_kwargs = mock_crew.call_args[1]
        assert call_kwargs["process"] == "sequential"
        assert call_kwargs["verbose"] is True
        assert call_kwargs["memory"] is True

    @patch("taskforce_one.crews.base.Crew")
    @patch("taskforce_one.agents.base.CrewAgent")
    def test_crew_cached(self, mock_agent, mock_crew, mock_agents):
        """Test that CrewAI crew is cached."""
        mock_agent.return_value = MagicMock()
        crew = BaseCrew(
            name="Test Crew",
            description="Test description",
            agents=mock_agents,
        )
        
        # Call crew twice
        _ = crew.crew
        _ = crew.crew
        
        # Should only create once
        assert mock_crew.call_count == 1

    def test_add_task(self, mock_agents):
        """Test adding a task to crew."""
        crew = BaseCrew(
            name="Test Crew",
            description="Test description",
            agents=mock_agents,
        )
        
        mock_task = MagicMock()
        result = crew.add_task(mock_task)
        
        assert len(crew._tasks) == 1
        assert result is crew  # Method chaining

    def test_add_tasks(self, mock_agents):
        """Test adding multiple tasks to crew."""
        crew = BaseCrew(
            name="Test Crew",
            description="Test description",
            agents=mock_agents,
        )
        
        mock_tasks = [MagicMock(), MagicMock()]
        result = crew.add_tasks(mock_tasks)
        
        assert len(crew._tasks) == 2
        assert result is crew  # Method chaining


class TestCrewFactory:
    """Tests for CrewFactory class."""

    @pytest.fixture
    def mock_agents(self):
        """Create mock agents for testing."""
        agent1 = BaseAgent(
            role="Agent 1",
            goal="Goal 1",
            backstory="Backstory 1",
        )
        agent1._id = "agent_1"
        
        agent2 = BaseAgent(
            role="Agent 2",
            goal="Goal 2",
            backstory="Backstory 2",
        )
        agent2._id = "agent_2"
        
        return [agent1, agent2]

    def test_from_config_minimal(self, mock_agents):
        """Test creating crew from minimal config."""
        config = {
            "name": "Test Crew",
            "description": "Test description",
            "agents": ["agent_1"],
        }
        
        crew = CrewFactory.from_config(config, mock_agents)
        
        assert crew.name == "Test Crew"
        assert crew.description == "Test description"
        assert len(crew.agents) == 1

    def test_from_config_full(self, mock_agents):
        """Test creating crew from full config."""
        config = {
            "name": "Test Crew",
            "description": "Test description",
            "agents": ["agent_1", "agent_2"],
            "process": "hierarchical",
            "verbose": False,
            "memory": False,
            "max_iterations": 20,
        }
        
        crew = CrewFactory.from_config(config, mock_agents)
        
        assert crew.process == "hierarchical"
        assert crew.verbose is False
        assert crew.memory is False
        assert crew.max_iterations == 20

    def test_from_config_defaults(self, mock_agents):
        """Test creating crew with default values."""
        config = {
            "name": "Test Crew",
            "description": "Test description",
            "agents": ["agent_1"],
        }
        
        crew = CrewFactory.from_config(config, mock_agents)
        
        assert crew.process == "sequential"
        assert crew.verbose is True
        assert crew.memory is True
        assert crew.max_iterations == 10

    def test_from_config_agent_not_found(self, mock_agents):
        """Test creating crew with non-existent agent."""
        config = {
            "name": "Test Crew",
            "description": "Test description",
            "agents": ["nonexistent"],
        }
        
        crew = CrewFactory.from_config(config, mock_agents)
        
        assert len(crew.agents) == 0

    def test_from_config_multiple_agents(self, mock_agents):
        """Test creating crew with multiple agents."""
        config = {
            "name": "Test Crew",
            "description": "Test description",
            "agents": ["agent_1", "agent_2"],
        }
        
        crew = CrewFactory.from_config(config, mock_agents)
        
        assert len(crew.agents) == 2

    def test_create_multiple(self, mock_agents):
        """Test creating multiple crews."""
        configs = [
            {"name": "Crew 1", "description": "Desc 1", "agents": ["agent_1"]},
            {"name": "Crew 2", "description": "Desc 2", "agents": ["agent_2"]},
        ]
        
        crews = CrewFactory.create_multiple(configs, mock_agents)
        
        assert len(crews) == 2
        assert crews[0].name == "Crew 1"
        assert crews[1].name == "Crew 2"

    def test_create_multiple_empty_list(self, mock_agents):
        """Test creating multiple crews from empty list."""
        crews = CrewFactory.create_multiple([], mock_agents)
        
        assert len(crews) == 0
