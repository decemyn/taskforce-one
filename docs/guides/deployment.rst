Deployment Guide
================

Task Force One can be deployed using Docker Compose or directly on a server.

Docker Deployment
-----------------

The recommended way to deploy Task Force One is using Docker Compose.

Prerequisites
~~~~~~~~~~~~

* Docker Engine 20.10+
* Docker Compose 2.0+

Quick Start
~~~~~~~~~~~

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/taskforce-one/taskforce-one.git
   cd taskforce-one

2. Create environment file:

.. code-block:: bash

   cp .env.example .env
   # Edit .env with your settings

3. Start the services:

.. code-block:: bash

   docker compose up -d

4. Check the status:

.. code-block:: bash

   docker compose ps

5. View logs:

.. code-block:: bash

   docker compose logs -f taskforce-one

Services
~~~~~~~~

The Docker Compose configuration starts the following services:

* ``taskforce-one`` - Main API server
* ``taskforce-postgres`` - PostgreSQL database
* ``taskforce-redis`` - Redis cache

Accessing the API
~~~~~~~~~~~~~~~~~

The API is available at http://localhost:8000

Health check:

.. code-block:: bash

   curl http://localhost:8000/health

List agents:

.. code-block:: bash

   curl http://localhost:8000/agents

Stop the services:

.. code-block:: bash

   docker compose down

Development Mode
---------------

For development, you can use the development Docker configuration:

.. code-block:: bash

   docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up -d

This enables auto-reload and additional debugging features.

Environment Variables
--------------------

Configure your deployment using environment variables:

.. code-block:: bash

   # API Configuration
   API_HOST=0.0.0.0
   API_PORT=8000
   
   # LLM Configuration
   OPENAI_API_KEY=your-api-key
   ANTHROPIC_API_KEY=your-anthropic-key
   
   # Storage Configuration
   POSTGRES_HOST=taskforce-postgres
   POSTGRES_PORT=5432
   REDIS_HOST=taskforce-redis
   REDIS_PORT=6379

Production Deployment
--------------------

For production deployments:

1. Use a reverse proxy (nginx, Traefik)
2. Enable HTTPS/TLS
3. Set appropriate resource limits
4. Configure monitoring and logging
5. Use secrets management

Example nginx configuration:

.. code-block:: nginx

   upstream taskforce {
       server localhost:8000;
   }
   
   server {
       listen 443 ssl http2;
       server_name api.example.com;
       
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
       
       location / {
           proxy_pass http://taskforce;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }

Docker Swarm
------------

Deploy to Docker Swarm:

.. code-block:: bash

   docker stack deploy -c docker/docker-compose.yml taskforce

Kubernetes
----------

For Kubernetes deployment, you'll need to create your own manifests. The Docker images are available at:

* ``taskforce-one:latest`` - Main API image

Manual Installation
------------------

For manual installation without Docker:

1. Install Python 3.11+

2. Install dependencies:

.. code-block:: bash

   pip install -e .

3. Configure environment:

.. code-block:: bash

   cp .env.example .env
   # Edit .env

4. Start the server:

.. code-block:: bash

   taskforce serve

Or directly:

.. code-block:: bash

   uvicorn taskforce_one.api:app --host 0.0.0.0 --port 8000
