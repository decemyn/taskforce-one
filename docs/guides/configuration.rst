Configuration Guide
==================

Task Force One uses YAML configuration files to define agents, crews, and application settings. By default, these files are located in the ``config/`` directory.

Configuration Directory
-----------------------

You can specify a custom configuration directory using:

1. Environment variable: ``CONFIG_DIR``
2. Docker volume mount: ``/app/config``

Agents Configuration
-------------------

The ``agents.yaml`` file defines your AI agents. Each agent has the following properties:

.. code-block:: yaml

   agents:
     - id: researcher
       role: Senior Researcher
       goal: Research and gather accurate information on any topic
       backstory: |
         You are an experienced researcher with a keen eye for detail.
         You have access to various research tools and databases.
       verbose: true
       max_iterations: 10
       allow_delegation: true
       tools:
         - search
         - scrape
     
     - id: writer
       role: Content Writer
       goal: Create high-quality written content based on research
       backstory: |
         You are a skilled writer known for engaging content.
       verbose: true
       max_iterations: 5

Agent Properties
~~~~~~~~~~~~~~~

``id`` (required)
   Unique identifier for the agent

``role`` (required)
   The role/title of the agent

``goal`` (required)
   The objective the agent aims to achieve

``backstory`` (required)
   The personality and background of the agent

``verbose`` (optional, default: true)
   Enable verbose logging

``max_iterations`` (optional, default: 5)
   Maximum iterations for task execution

``allow_delegation`` (optional, default: false)
   Allow the agent to delegate tasks to other agents

``tools`` (optional)
   List of tool names available to the agent

Crews Configuration
------------------

The ``crews.yaml`` file defines crews - groups of agents that work together:

.. code-block:: yaml

   crews:
     - id: content_crew
       name: Content Creation Crew
       description: A crew for creating high-quality content
       agents:
         - researcher
         - writer
         - editor
       process: sequential
       verbose: true
       memory: true
       max_iterations: 10

Crew Properties
~~~~~~~~~~~~~~

``id`` (required)
   Unique identifier for the crew

``name`` (required)
   Display name of the crew

``description`` (required)
   Description of the crew's purpose

``agents`` (required)
   List of agent IDs that belong to this crew

``process`` (optional, default: sequential)
   Execution process: ``sequential`` or ``hierarchical``

``verbose`` (optional, default: true)
   Enable verbose logging

``memory`` (optional, default: true)
   Enable crew memory

``max_iterations`` (optional, default: 10)
   Maximum iterations for execution

Settings Configuration
---------------------

The ``settings.yaml`` file controls application settings:

.. code-block:: yaml

   app:
     name: Task Force One
     version: 0.1.0
   
   api:
     host: 0.0.0.0
     port: 8000
     reload: false
     workers: 1
     log_level: info
   
   llm:
     provider: openai
     model: gpt-4
     temperature: 0.7
     max_tokens: 2000
     timeout: 60
   
   storage:
     type: local
     path: ./data
     redis_host: localhost
     redis_port: 6379
     postgres_host: localhost
     postgres_port: 5432
   
   logging:
     level: INFO
     file: ./logs/taskforce.log
     rotation: 100 MB
     retention: 30 days

Settings Properties
~~~~~~~~~~~~~~~~~~

``app``
   Application metadata

``api``
   API server configuration

``llm``
   Language model settings

``storage``
   Storage backend configuration

``logging``
   Logging configuration

Environment Variables
---------------------

You can override settings using environment variables:

.. code-block:: bash

   export OPENAI_API_KEY=your-api-key
   export CONFIG_DIR=/path/to/config
   export ENVIRONMENT=production
