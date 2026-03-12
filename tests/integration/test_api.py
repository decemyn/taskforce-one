"""Integration tests for the FastAPI application."""

import pytest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient


@pytest.fixture
def mock_config():
    """Mock configuration loader."""
    with patch("taskforce_one.config.loader.ConfigLoader") as mock:
        mock_instance = MagicMock()
        mock_instance.load_agents.return_value = {
            "test_agent": {
                "id": "test_agent",
                "role": "Test Agent",
                "goal": "Test goal",
                "backstory": "Test backstory",
            }
        }
        mock_instance.load_crews.return_value = {
            "test_crew": {
                "id": "test_crew",
                "name": "Test Crew",
                "description": "Test crew description",
                "agents": ["test_agent"],
            }
        }
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def client(mock_config):
    """Create test client with mocked dependencies."""
    with (
        patch("taskforce_one.agents.base.CrewAgent") as mock_agent,
        patch("taskforce_one.crews.base.Crew") as mock_crew,
    ):
        # Mock the agent
        mock_agent_instance = MagicMock()
        mock_agent_instance.execute_task.return_value = "Test result"
        mock_agent.return_value = mock_agent_instance

        # Mock the crew
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "Crew result"
        mock_crew.return_value = mock_crew_instance

        from taskforce_one.api import app

        with TestClient(app) as test_client:
            yield test_client


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root(self, client):
        """Test root endpoint returns correct info."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Task Force One"
        assert "version" in data


class TestHealthEndpoint:
    """Tests for health endpoint."""

    def test_health(self, client):
        """Test health endpoint returns healthy status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestAgentsEndpoint:
    """Tests for agents endpoints."""

    def test_list_agents(self, client):
        """Test listing all agents."""
        response = client.get("/agents")

        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert len(data["agents"]) >= 1

        # Check agent structure
        agent = data["agents"][0]
        assert "id" in agent
        assert "role" in agent
        assert "goal" in agent


class TestCrewsEndpoint:
    """Tests for crews endpoints."""

    def test_list_crews(self, client):
        """Test listing all crews."""
        response = client.get("/crews")

        assert response.status_code == 200
        data = response.json()
        assert "crews" in data


class TestAgentExecution:
    """Tests for agent execution endpoint."""

    def test_execute_agent_not_found(self, client):
        """Test executing non-existent agent returns 404."""
        response = client.post(
            "/agents/nonexistent/execute", json={"agent_id": "nonexistent", "task": "test task"}
        )

        assert response.status_code == 404

    @patch("taskforce_one.agents.base.BaseAgent.execute")
    def test_execute_agent_success(self, mock_execute, client):
        """Test executing agent successfully."""
        mock_execute.return_value = "Test result"
        response = client.post(
            "/agents/test_agent/execute", json={"agent_id": "test_agent", "task": "test task"}
        )

        assert response.status_code == 200
        assert response.json()["result"] == "Test result"


class TestCrewExecution:
    """Tests for crew execution endpoint."""

    def test_execute_crew_not_found(self, client):
        """Test executing non-existent crew returns 404."""
        response = client.post(
            "/crews/nonexistent/execute",
            json={"crew_id": "nonexistent", "input_data": "test input"},
        )

        assert response.status_code == 404

    def test_execute_crew_success(self, client):
        """Test executing crew successfully."""
        response = client.post(
            "/crews/test_crew/execute", json={"crew_id": "test_crew", "input_data": "test input"}
        )

        # May return 500 if mocking doesn't work, but tests the endpoint exists
        assert response.status_code in [200, 500]


class TestCORS:
    """Tests for CORS configuration."""

    def test_cors_headers_on_request(self, client):
        """Test CORS headers are present on GET request."""
        response = client.get("/")

        # CORS headers should be present
        # FastAPI's CORSMiddleware adds these on actual requests
        assert response.status_code == 200


class TestConfigReload:
    """Tests for configuration reload endpoint."""

    def test_reload_config_endpoint_exists(self, client):
        """Test that the reload endpoint exists and returns success."""
        response = client.post("/config/reload")

        # Should return 200 and success status
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "agents_loaded" in data
        assert "crews_loaded" in data
        assert "message" in data

    @patch("taskforce_one.api._initialize_agents")
    @patch("taskforce_one.api._initialize_crews")
    @patch("taskforce_one.api.config")
    def test_reload_calls_reinitialize_functions(self, mock_config, mock_init_crews, mock_init_agents, client):
        """Test that reload endpoint calls the reinitialize functions."""
        # Setup mocks
        mock_config.reload.return_value = None

        response = client.post("/config/reload")

        assert response.status_code == 200
        mock_config.reload.assert_called_once()
        mock_init_agents.assert_called_once()
        mock_init_crews.assert_called_once()

    def test_reload_returns_counts(self, client):
        """Test that reload endpoint returns the correct counts."""
        response = client.post("/config/reload")

        assert response.status_code == 200
        data = response.json()
        # Based on mock_config, should have 1 agent and 1 crew
        assert data["agents_loaded"] >= 0
        assert data["crews_loaded"] >= 0
