Development Guide
==================

This guide covers setting up a development environment and contributing to Task Force One.

Development Environment Setup
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Quick Start
~~~~~~~~~~~~

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/taskforce-one/taskforce-one.git
   cd taskforce-one

2. Run the development setup script:

.. code-block:: bash

   ./scripts/dev.sh

3. Activate the virtual environment:

.. code-block:: bash

   source .venv/bin/activate

Manual Setup
~~~~~~~~~~~~~

1. Create a virtual environment:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate  # Windows

2. Install dependencies:

.. code-block:: bash

   pip install -e ".[dev]"

3. Copy environment file:

.. code-block:: bash

   cp .env.example .env
   # Edit .env with your settings

Running the Application
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Start the API server:

.. code-block:: bash

   taskforce serve

Or use the run script:

.. code-block:: bash

   ./scripts/run.sh

Running Tests
--------------------------------------------------------------------------------------

Run all tests:

.. code-block:: bash

   ./scripts/test.sh

Run specific test types:

.. code-block:: bash

   # Unit tests only
   ./scripts/test.sh --unit
   
   # Integration tests only
   ./scripts/test.sh --integration
   
   # E2E tests only
   ./scripts/test.sh --e2e

Run with coverage:

.. code-block:: bash

   ./scripts/test.sh --coverage

Code Quality
--------------------------------------------------------------

Run linters:

.. code-block:: bash

   ./scripts/lint.sh

Run formatter:

.. code-block:: bash

   ./scripts/format.sh
   ./scripts/format.sh --check  # Check without applying

Project Structure
------------------------------------------------------------------------------------------------------------------------------------------

::

   taskforce-one/
   ├── src/taskforce_one/     # Source code
   │   ├── api.py            # FastAPI application
   │   ├── cli.py            # CLI commands
   │   ├── agents/           # Agent implementations
   │   ├── crews/            # Crew implementations
   │   ├── config/           # Configuration loading
   │   └── tools/            # Tool registry
   ├── config/               # Configuration files
   ├── tests/                # Test suite
   │   ├── unit/            # Unit tests
   │   ├── integration/      # Integration tests
   │   └── e2e/             # End-to-end tests
   ├── scripts/              # Utility scripts
   └── docs/                 # Documentation

Code Style
----------------------------------------------------------

* Follow PEP 8
* Use type hints
* Write docstrings (Google style)
* Run formatter before committing

Git Workflow
--------------------------------------------------------------

1. Create a feature branch:

.. code-block:: bash

   git checkout -b feature/my-feature

2. Make your changes

3. Run tests and linters:

.. code-block:: bash

   ./scripts/test.sh
   ./scripts/lint.sh
   ./scripts/format.sh

4. Commit your changes:

.. code-block:: bash

   git add .
   git commit -m "Add my feature"

5. Push to GitHub:

.. code-block:: bash

   git push origin feature/my-feature

6. Create a Pull Request

Debugging
--------------------------------------------

View application logs:

.. code-block:: bash

   docker compose logs -f taskforce-one

Or use the logs script:

.. code-block:: bash

   ./scripts/logs.sh --follow

Health check:

.. code-block:: bash

   ./scripts/health.sh

IDE Setup
--------------------------------------------

VS Code
~~~~~~~

The project includes VS Code settings for Python development:

1. Install Python extension
2. Install Ruff extension
3. The workspace should automatically configure linting and formatting

PyCharm
~~~~~~~

1. Open the project
2. Set Python interpreter to the virtual environment
3. Configure test runner in settings

Contributing
--------------------------------------------------------------------------------------

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Ensure all tests pass
6. Submit a Pull Request

Questions?
----------------------------------------------------------

If you have questions, please open an issue on GitHub.
