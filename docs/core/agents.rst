Agents
======

Agents are the fundamental units of Task Force One. Each agent is an AI with a specific role, goal, and backstory.

Creating an Agent
-----------------

Agents can be created programmatically or loaded from configuration.

Programmatic Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from taskforce_one.agents.base import BaseAgent
   
   agent = BaseAgent(
       role="Researcher",
       goal="Research and gather information",
       backstory="You are an experienced researcher...",
       verbose=True,
       max_iterations=10,
       allow_delegation=True,
   )

Agent Properties
---------------

``role`` (str, required)
   The role or title of the agent.

``goal`` (str, required)
   The objective the agent aims to achieve.

``backstory`` (str, required)
   The personality, background, and context for the agent.

``verbose`` (bool, default: True)
   Enable verbose logging during execution.

``max_iterations`` (int, default: 5)
   Maximum number of iterations the agent can run.

``allow_delegation`` (bool, default: False)
   Whether the agent can delegate tasks to other agents.

``tools`` (list, optional)
   List of tools the agent can use.

``llm_config`` (dict, optional)
   Custom LLM configuration overrides.

Using an Agent
-------------

Execute a task with an agent:

.. code-block:: python

   result = agent.execute("Research the latest AI trends")

Agent Factory
------------

Use the AgentFactory to create agents from configuration:

.. code-block:: python

   from taskforce_one.agents.base import AgentFactory
   
   config = {
       "role": "Researcher",
       "goal": "Research topics",
       "backstory": "You are a researcher...",
   }
   
   agent = AgentFactory.from_config(config)

Creating Multiple Agents
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   configs = [
       {"role": "Researcher", "goal": "Research", "backstory": "..."},
       {"role": "Writer", "goal": "Write", "backstory": "..."},
   ]
   
   agents = AgentFactory.create_multiple(configs)

Agent ID
-------

Each agent has a unique ID generated from its role:

.. code-block:: python

   agent = BaseAgent(role="Senior Researcher", ...)
   print(agent.id)  # "senior_researcher"

The ID is used to reference agents in crews and the API.
