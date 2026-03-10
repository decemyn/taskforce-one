API Reference
============

Task Force One provides a FastAPI-based REST API for managing and executing agents and crews.

Base URL
-------

::

   http://localhost:8000

Authentication
-------------

Currently, no authentication is required. For production deployments, implement your own authentication.

Endpoints
--------

Root
~~~

**GET /**

Returns API information.

**Response:**

.. code-block:: json

   {
     "name": "Task Force One",
     "version": "0.1.0",
     "description": "CrewAI-based orchestration toolkit"
   }

Health Check
~~~~~~~~~~~~

**GET /health**

Returns the health status of the API.

**Response:**

.. code-block:: json

   {
     "status": "healthy",
     "version": "0.1.0"
   }

List Agents
~~~~~~~~~~~

**GET /agents**

Returns a list of all configured agents.

**Response:**

.. code-block:: json

   {
     "agents": [
       {
         "id": "researcher",
         "role": "Senior Researcher",
         "goal": "Research and gather accurate information"
       }
     ]
   }

List Crews
~~~~~~~~~~

**GET /crews**

Returns a list of all configured crews.

**Response:**

.. code-block:: json

   {
     "crews": [
       {
         "id": "content_crew",
         "name": "Content Creation Crew",
         "description": "A crew for creating content",
         "agents": ["researcher", "writer"]
       }
     ]
   }

Execute Agent
~~~~~~~~~~~~

**POST /agents/{agent_id}/execute**

Executes an agent with a given task.

**Path Parameters:**

* ``agent_id`` (string) - The ID of the agent to execute

**Request Body:**

.. code-block:: json

   {
     "agent_id": "researcher",
     "task": "Research the latest AI trends"
   }

**Response:**

.. code-block:: json

   {
     "agent_id": "researcher",
     "result": "Here are the latest AI trends..."
   }

Execute Crew
~~~~~~~~~~~~

**POST /crews/{crew_id}/execute**

Executes a crew with given input data.

**Path Parameters:**

* ``crew_id`` (string) - The ID of the crew to execute

**Request Body:**

.. code-block:: json

   {
     "crew_id": "content_crew",
     "input_data": "Write an article about AI"
   }

**Response:**

.. code-block:: json

   {
     "crew_id": "content_crew",
     "result": "Here is the article..."
   }

Error Responses
--------------

**404 Not Found**

.. code-block:: json

   {
     "detail": "Agent researcher not found"
   }

**500 Internal Server Error**

.. code-block:: json

   {
     "detail": "Error executing agent"
   }

API Clients
----------

Python
~~~~~~

Using requests:

.. code-block:: python

   import requests
   
   base_url = "http://localhost:8000"
   
   # Get agents
   response = requests.get(f"{base_url}/agents")
   agents = response.json()
   
   # Execute agent
   response = requests.post(
       f"{base_url}/agents/researcher/execute",
       json={"agent_id": "researcher", "task": "Research AI"}
   )
   result = response.json()

Using OpenAPI Client
~~~~~~~~~~~~~~~~~~~~

Generate a client from the OpenAPI spec:

.. code-block:: bash

   curl http://localhost:8000/openapi.json -o openapi.json
   npx @openapi-generator/cli generate -i openapi.json -g python -o client
