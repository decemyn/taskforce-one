Tools
=====

Tools give agents capabilities to interact with external systems and perform specific actions.

Default Tools
--------------------------------------------------------------------------------------

Task Force One includes several default tools:

* ``read_file`` - Read content from files
* ``write_file`` - Write content to files
* ``search`` - Search the web using Serper
* ``scrape`` - Scrape content from websites

Using Tools
--------------------------------------------------------------

Assign tools to agents:

.. code-block:: python

   from taskforce_one.tools.registry import get_registry
   from taskforce_one.agents.base import BaseAgent
   
   # Get the registry
   registry = get_registry()
   
   # Get tools
   search_tool = registry.get("search")
   scrape_tool = registry.get("scrape")
   
   # Create agent with tools
   agent = BaseAgent(
       role="Researcher",
       goal="Research topics",
       backstory="You are a researcher...",
       tools=[search_tool, scrape_tool],
   )

Tool Registry
--------------------------------------------------------------------------------------

The ToolRegistry manages available tools:

.. code-block:: python

   from taskforce_one.tools.registry import ToolRegistry
   
   registry = ToolRegistry()
   
   # List available tools
   tools = registry.list_tools()
   print(tools)  # ['read_file', 'write_file', 'search', 'scrape']
   
   # Check if tool exists
   if registry.has_tool("search"):
       tool = registry.get("search")
   
   # Register custom tool
   registry.register("my_tool", custom_tool)
   
   # Unregister tool
   registry.unregister("my_tool")

Custom Tools
--------------------------------------------------------------------------------------

Create custom tools using CrewAI's BaseTool:

.. code-block:: python

   from crewai.tools import BaseTool
   from pydantic import Field
   
   class MyCustomTool(BaseTool):
       name: str = Field(description="The name of the tool")
       description: str = Field(description="What the tool does")
       
       def _run(self, input_data: str) -> str:
           # Tool logic here
           return f"Processed: {input_data}"
   
   # Register the tool
   custom_tool = MyCustomTool()
   registry.register("custom", custom_tool)

Tool Configuration
----------------------------------------------------------------------------------------------------------------------------------------------

Tools can be configured in agent definitions:

.. code-block:: yaml

   agents:
     - id: researcher
       role: Researcher
       goal: Research topics
       backstory: You are a researcher...
       tools:
         - search
         - scrape

Best Practices
-----------------------------------------------------------------------------------------

1. **Use appropriate tools**: Assign only relevant tools to each agent
2. **Document tools**: Provide clear descriptions for custom tools
3. **Handle errors**: Implement error handling in custom tools
4. **Test tools**: Test tools independently before using in agents
