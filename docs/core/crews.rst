Crews
=====

Crews are groups of agents that work together to accomplish complex tasks.

Creating a Crew
---------------

Crews combine multiple agents and define how they work together.

Programmatic Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from taskforce_one.crews.base import BaseCrew
   from taskforce_one.agents.base import BaseAgent
   
   # Create agents
   researcher = BaseAgent(
       role="Researcher",
       goal="Research topics",
       backstory="You are a researcher..."
   )
   
   writer = BaseAgent(
       role="Writer",
       goal="Write content",
       backstory="You are a writer..."
   )
   
   # Create crew
   crew = BaseCrew(
       name="Content Crew",
       description="A crew for creating content",
       agents=[researcher, writer],
       process="sequential",  # or "hierarchical"
       verbose=True,
       memory=True,
   )

Crew Properties
--------------

``name`` (str, required)
   Display name of the crew.

``description`` (str, required)
   Description of the crew's purpose.

``agents`` (list, required)
   List of BaseAgent instances.

``process`` (str, default: "sequential")
   Execution process:
   - ``sequential``: Agents work one after another
   - ``hierarchical``: One agent manages others

``verbose`` (bool, default: True)
   Enable verbose logging.

``memory`` (bool, default: True)
   Enable crew memory (remembers past interactions).

``max_iterations`` (int, default: 10)
   Maximum iterations for the crew.

Using a Crew
------------

Execute a crew:

.. code-block:: python

   result = crew.execute("Write an article about AI")

Execute asynchronously:

.. code-block:: python

   future = crew.execute_async("Write an article about AI")
   result = future.result()

Adding Tasks
------------

Add tasks to a crew:

.. code-block:: python

   from crewai import Task
   
   task = Task(
       description="Research AI trends",
       agent=researcher.crew_agent,
   )
   
   crew.add_task(task)

Crew Factory
-----------

Use CrewFactory to create crews from configuration:

.. code-block:: python

   from taskforce_one.crews.base import CrewFactory
   from taskforce_one.agents.base import AgentFactory
   
   # Load agents
   agent_configs = [...]
   agents = AgentFactory.create_multiple(agent_configs)
   
   # Create crew
   crew_config = {
       "name": "Content Crew",
       "description": "Creates content",
       "agents": ["researcher", "writer"],
   }
   
   crew = CrewFactory.from_config(crew_config, agents)

Crew ID
-------

Each crew has a unique ID:

.. code-block:: python

   crew = BaseCrew(name="Content Creation Crew", ...)
   print(crew.id)  # "content_creation_crew"

Process Types
------------

Sequential
~~~~~~~~~~

Agents complete tasks in order. The output of one agent becomes input to the next.

.. code-block:: python

   crew = BaseCrew(
       name="Content Crew",
       agents=[researcher, writer, editor],
       process="sequential",
   )

Hierarchical
~~~~~~~~~~~~

A manager agent delegates tasks to other agents and synthesizes results.

.. code-block:: python

   crew = BaseCrew(
       name="Content Crew",
       agents=[manager, researcher, writer],
       process="hierarchical",
   )
