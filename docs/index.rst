Task Force One Documentation
============================

.. image:: https://img.shields.io/badge/version-0.1.0-blue.svg
   :target: https://github.com/taskforce-one/taskforce-one
   :alt: Version

.. image:: https://img.shields.io/badge/python-3.11+-green.svg
   :target: https://www.python.org/
   :alt: Python Version

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: LICENSE
   :alt: License

Task Force One is a CrewAI-based orchestration toolkit for Micro SaaS applications. It provides a flexible framework for creating and managing AI agent crews that can collaborate to accomplish complex tasks.

Building the Documentation
--------------------------

To build the HTML documentation:

.. code-block:: bash

   ./scripts/docs.sh

Or using make:

.. code-block:: bash

   cd docs && make html

The built documentation will be in ``docs/_build/html/``. Open ``index.html`` in your browser to view.

For live-reload development:

.. code-block:: bash

   cd docs && make livehtml

Features
--------

* **Agent Management**: Create and configure AI agents with custom roles, goals, and backstories
* **Crew Orchestration**: Organize agents into crews with sequential or hierarchical processing
* **REST API**: FastAPI-based API for remote agent and crew execution
* **Tool Registry**: Built-in tools for file operations, web search, and web scraping
* **Docker Support**: Containerized deployment with Docker Compose
* **Configuration**: YAML-based configuration for agents, crews, and settings

Quick Start
-----------

Install the package:

.. code-block:: bash

   pip install taskforce-one

Or install from source:

.. code-block:: bash

   git clone https://github.com/taskforce-one/taskforce-one.git
   cd taskforce-one
   pip install -e .

Start the API server:

.. code-block:: bash

   taskforce serve

Or use Docker:

.. code-block:: bash

   docker compose up -d

Now visit http://localhost:8000 to access the API.

Configuration
-------------

Task Force One uses YAML configuration files located in the ``config/`` directory:

* ``agents.yaml`` - Define your AI agents
* ``crews.yaml`` - Configure agent crews
* ``settings.yaml`` - Application settings

See the :doc:`guides/configuration` guide for detailed configuration options.

API Endpoints
-------------

The API provides the following endpoints:

* ``GET /`` - API information
* ``GET /health`` - Health check
* ``GET /agents`` - List all agents
* ``GET /crews`` - List all crews
* ``POST /agents/{id}/execute`` - Execute an agent
* ``POST /crews/{id}/execute`` - Execute a crew

See the :doc:`api_reference` for detailed API documentation.

Development
-----------

Clone the repository and set up the development environment:

.. code-block:: bash

   git clone https://github.com/taskforce-one/taskforce-one.git
   cd taskforce-one
   ./scripts/dev.sh

Run tests:

.. code-block:: bash

   ./scripts/test.sh

Run linters:

.. code-block:: bash

   ./scripts/lint.sh

See the :doc:`guides/development` guide for more development information.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guides/configuration
   guides/deployment
   guides/development

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api_reference

.. toctree::
   :maxdepth: 2
   :caption: Core Concepts

   core/agents
   core/crews
   core/tools

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
