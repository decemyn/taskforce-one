"""Tool Registry for Task Force One

Manages and provides access to tools for agents.
"""


from crewai.tools import BaseTool
from loguru import logger


class ToolRegistry:
    """Registry for managing available tools."""

    def __init__(self):
        """Initialize the tool registry."""
        self._tools: dict[str, BaseTool] = {}
        self._initialize_default_tools()

    def _initialize_default_tools(self) -> None:
        """Initialize default tools available to agents."""
        # Import default crewai tools
        try:
            from crewai.tools import (
                FileReadTool,
                FileWriteTool,
                ScrapeWebsiteTool,
                SerperDevTool,
            )

            # Register default tools
            self.register("read_file", FileReadTool())
            self.register("write_file", FileWriteTool())
            self.register("search", SerperDevTool())
            self.register("scrape", ScrapeWebsiteTool())

            logger.info("Default tools initialized")
        except ImportError as e:
            logger.warning(f"Could not import default tools: {e}")

    def register(self, name: str, tool: BaseTool) -> None:
        """Register a tool.

        Args:
            name: The name to register the tool under
            tool: The tool instance
        """
        self._tools[name] = tool
        logger.debug(f"Registered tool: {name}")

    def get(self, name: str) -> BaseTool | None:
        """Get a tool by name.

        Args:
            name: The name of the tool

        Returns:
            The tool instance or None if not found
        """
        return self._tools.get(name)

    def get_multiple(self, names: list[str]) -> list[BaseTool]:
        """Get multiple tools by name.

        Args:
            names: List of tool names

        Returns:
            List of tool instances
        """
        tools = []
        for name in names:
            tool = self.get(name)
            if tool:
                tools.append(tool)
        return tools

    def list_tools(self) -> list[str]:
        """List all registered tool names.

        Returns:
            List of tool names
        """
        return list(self._tools.keys())

    def has_tool(self, name: str) -> bool:
        """Check if a tool is registered.

        Args:
            name: The name of the tool

        Returns:
            True if the tool is registered
        """
        return name in self._tools

    def unregister(self, name: str) -> bool:
        """Unregister a tool.

        Args:
            name: The name of the tool

        Returns:
            True if the tool was unregistered
        """
        if name in self._tools:
            del self._tools[name]
            logger.debug(f"Unregistered tool: {name}")
            return True
        return False


# Global tool registry instance
_registry: ToolRegistry | None = None


def get_registry() -> ToolRegistry:
    """Get the global tool registry instance.

    Returns:
        ToolRegistry instance
    """
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry
