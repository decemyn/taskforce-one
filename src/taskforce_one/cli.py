"""Task Force One - CLI Module

Command-line interface for Task Force One.
"""

import sys
from typing import Optional

import click
from loguru import logger

from taskforce_one import __version__
from taskforce_one.agents.base import AgentFactory
from taskforce_one.config.loader import ConfigLoader
from taskforce_one.crews.base import CrewFactory


@click.group()
@click.version_option(version=__version__)
def cli():
    """Task Force One - CrewAI Orchestration Toolkit"""
    pass


@cli.command()
def info():
    """Show information about Task Force One."""
    click.echo(f"Task Force One v{__version__}")
    click.echo("CrewAI-based orchestration toolkit for Micro SaaS applications")


@cli.command()
@click.option("--config-dir", type=click.Path(exists=True), help="Configuration directory")
def list_agents(config_dir: Optional[str] = None):
    """List all available agents."""
    config = ConfigLoader(config_dir) if config_dir else ConfigLoader()
    agents_config = config.load_agents()
    
    if not agents_config:
        click.echo("No agents configured")
        return
    
    click.echo("Available Agents:")
    click.echo("-" * 50)
    for agent_id, agent_config in agents_config.items():
        click.echo(f"  {agent_id}")
        click.echo(f"    Role: {agent_config.get('role', 'N/A')}")
        click.echo(f"    Goal: {agent_config.get('goal', 'N/A')[:50]}...")
        click.echo()


@cli.command()
@click.option("--config-dir", type=click.Path(exists=True), help="Configuration directory")
def list_crews(config_dir: Optional[str] = None):
    """List all available crews."""
    config = ConfigLoader(config_dir) if config_dir else ConfigLoader()
    crews_config = config.load_crews()
    
    if not crews_config:
        click.echo("No crews configured")
        return
    
    click.echo("Available Crews:")
    click.echo("-" * 50)
    for crew_id, crew_config in crews_config.items():
        click.echo(f"  {crew_id}")
        click.echo(f"    Name: {crew_config.get('name', 'N/A')}")
        click.echo(f"    Description: {crew_config.get('description', 'N/A')[:50]}...")
        click.echo(f"    Process: {crew_config.get('process', 'sequential')}")
        click.echo()


@cli.command()
@click.argument("agent_id")
@click.argument("task")
@click.option("--config-dir", type=click.Path(exists=True), help="Configuration directory")
def run_agent(agent_id: str, task: str, config_dir: Optional[str] = None):
    """Run an agent with a specific task."""
    config = ConfigLoader(config_dir) if config_dir else ConfigLoader()
    agents_config = config.load_agents()
    
    if agent_id not in agents_config:
        click.echo(f"Error: Agent '{agent_id}' not found", err=True)
        sys.exit(1)
    
    agent_config = agents_config[agent_id]
    agent = AgentFactory.from_config(agent_config)
    
    click.echo(f"Running agent '{agent_id}'...")
    result = agent.execute(task)
    click.echo(f"\nResult:\n{result}")


@cli.command()
@click.argument("crew_id")
@click.argument("input_data")
@click.option("--config-dir", type=click.Path(exists=True), help="Configuration directory")
def run_crew(crew_id: str, input_data: str, config_dir: Optional[str] = None):
    """Run a crew with input data."""
    config = ConfigLoader(config_dir) if config_dir else ConfigLoader()
    crews_config = config.load_crews()
    agents_config = config.load_agents()
    
    if crew_id not in crews_config:
        click.echo(f"Error: Crew '{crew_id}' not found", err=True)
        sys.exit(1)
    
    # Create agents
    agents = []
    for agent_id in agents_config:
        agents.append(AgentFactory.from_config(agents_config[agent_id]))
    
    # Create crew
    crew_config = crews_config[crew_id]
    crew = CrewFactory.from_config(crew_config, agents)
    
    click.echo(f"Running crew '{crew_id}'...")
    result = crew.execute(input_data)
    click.echo(f"\nResult:\n{result}")


@cli.command()
def serve():
    """Start the API server."""
    from taskforce_one.api import app
    import uvicorn
    
    click.echo("Starting Task Force One API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
