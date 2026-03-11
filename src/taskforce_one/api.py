"""Task Force One - API Module

FastAPI application for serving the orchestration toolkit.
"""


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel

from taskforce_one import __version__
from taskforce_one.agents.base import AgentFactory, BaseAgent
from taskforce_one.config.loader import ConfigLoader
from taskforce_one.crews.base import BaseCrew, CrewFactory

# Initialize FastAPI app
app = FastAPI(
    title="Task Force One",
    description="CrewAI-based orchestration toolkit for Micro SaaS applications",
    version=__version__,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize configuration
config = ConfigLoader()


# Request/Response models
class AgentRequest(BaseModel):
    """Request model for agent execution."""
    agent_id: str
    task: str


class CrewRequest(BaseModel):
    """Request model for crew execution."""
    crew_id: str
    input_data: str


class AgentResponse(BaseModel):
    """Response model for agent execution."""
    agent_id: str
    result: str


class CrewResponse(BaseModel):
    """Response model for crew execution."""
    crew_id: str
    result: str


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str


# Store for agents and crews
_agents: dict[str, BaseAgent] = {}
_crews: dict[str, BaseCrew] = {}


def _initialize_agents():
    """Initialize agents from configuration."""
    global _agents

    agents_config = config.load_agents()
    for agent_id, agent_config in agents_config.items():
        try:
            agent = AgentFactory.from_config(agent_config)
            _agents[agent_id] = agent
            logger.info(f"Loaded agent: {agent_id}")
        except Exception as e:
            logger.error(f"Failed to load agent {agent_id}: {e}")


def _initialize_crews():
    """Initialize crews from configuration."""
    global _crews

    crews_config = config.load_crews()
    for crew_id, crew_config in crews_config.items():
        try:
            # Get agents for this crew
            crew_agents = []
            for agent_id in crew_config.get("agents", []):
                if agent_id in _agents:
                    crew_agents.append(_agents[agent_id])

            if crew_agents:
                crew = CrewFactory.from_config(crew_config, crew_agents)
                _crews[crew_id] = crew
                logger.info(f"Loaded crew: {crew_id}")
        except Exception as e:
            logger.error(f"Failed to load crew {crew_id}: {e}")


@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info("Starting Task Force One API...")
    _initialize_agents()
    _initialize_crews()
    logger.info(f"Loaded {len(_agents)} agents and {len(_crews)} crews")


@app.get("/", response_model=dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "name": "Task Force One",
        "version": __version__,
        "description": "CrewAI-based orchestration toolkit",
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=__version__,
    )


@app.get("/agents")
async def list_agents():
    """List all available agents."""
    return {
        "agents": [
            {
                "id": agent_id,
                "role": agent.role,
                "goal": agent.goal,
            }
            for agent_id, agent in _agents.items()
        ]
    }


@app.get("/crews")
async def list_crews():
    """List all available crews."""
    return {
        "crews": [
            {
                "id": crew_id,
                "name": crew.name,
                "description": crew.description,
                "agents": [a.id for a in crew.agents],
            }
            for crew_id, crew in _crews.items()
        ]
    }


@app.post("/agents/{agent_id}/execute", response_model=AgentResponse)
async def execute_agent(agent_id: str, request: AgentRequest):
    """Execute an agent with a task."""
    if agent_id not in _agents:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

    agent = _agents[agent_id]
    result = agent.execute(request.task)

    return AgentResponse(
        agent_id=agent_id,
        result=result,
    )


@app.post("/crews/{crew_id}/execute", response_model=CrewResponse)
async def execute_crew(crew_id: str, request: CrewRequest):
    """Execute a crew with input data."""
    if crew_id not in _crews:
        raise HTTPException(status_code=404, detail=f"Crew {crew_id} not found")

    crew = _crews[crew_id]
    result = crew.execute(request.input_data)

    return CrewResponse(
        crew_id=crew_id,
        result=str(result),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
