"""Unit tests for ToolRegistry."""

from unittest.mock import MagicMock

import pytest

from taskforce_one.tools.registry import ToolRegistry, get_registry


class TestToolRegistry:
    """Tests for ToolRegistry class."""

    @pytest.fixture
    def registry(self):
        """Create a fresh tool registry."""
        return ToolRegistry()

    def test_registry_initialization(self, registry):
        """Test registry initialization."""
        assert registry is not None
        assert isinstance(registry._tools, dict)

    def test_register_tool(self, registry):
        """Test registering a tool."""
        mock_tool = MagicMock()
        registry.register("test_tool", mock_tool)

        assert "test_tool" in registry._tools
        assert registry._tools["test_tool"] is mock_tool

    def test_get_tool(self, registry):
        """Test getting a tool by name."""
        mock_tool = MagicMock()
        registry.register("test_tool", mock_tool)

        tool = registry.get("test_tool")

        assert tool is mock_tool

    def test_get_tool_not_found(self, registry):
        """Test getting a non-existent tool."""
        tool = registry.get("nonexistent")

        assert tool is None

    def test_get_multiple_tools(self, registry):
        """Test getting multiple tools."""
        tool1 = MagicMock()
        tool2 = MagicMock()
        registry.register("tool1", tool1)
        registry.register("tool2", tool2)

        tools = registry.get_multiple(["tool1", "tool2"])

        assert len(tools) == 2
        assert tools[0] is tool1
        assert tools[1] is tool2

    def test_get_multiple_tools_with_missing(self, registry):
        """Test getting multiple tools with some missing."""
        tool1 = MagicMock()
        registry.register("tool1", tool1)

        tools = registry.get_multiple(["tool1", "nonexistent"])

        assert len(tools) == 1
        assert tools[0] is tool1

    def test_list_tools(self, registry):
        """Test listing all tools."""
        tool1 = MagicMock()
        tool2 = MagicMock()
        registry.register("tool1", tool1)
        registry.register("tool2", tool2)

        tools = registry.list_tools()

        # Registry may have default tools pre-registered, so check at least 2
        assert len(tools) >= 2
        assert "tool1" in tools
        assert "tool2" in tools

    def test_has_tool(self, registry):
        """Test checking if tool exists."""
        tool = MagicMock()
        registry.register("test_tool", tool)

        assert registry.has_tool("test_tool") is True
        assert registry.has_tool("nonexistent") is False

    def test_unregister_tool(self, registry):
        """Test unregistering a tool."""
        tool = MagicMock()
        registry.register("test_tool", tool)

        result = registry.unregister("test_tool")

        assert result is True
        assert "test_tool" not in registry._tools

    def test_unregister_nonexistent_tool(self, registry):
        """Test unregistering a non-existent tool."""
        result = registry.unregister("nonexistent")

        assert result is False


class TestGetRegistry:
    """Tests for get_registry function."""

    def test_get_registry_singleton(self):
        """Test that get_registry returns a singleton."""
        registry1 = get_registry()
        registry2 = get_registry()

        assert registry1 is registry2

    def test_get_registry_different_instances(self):
        """Test get_registry returns different instances after reset."""
        from taskforce_one.tools import registry as registry_module

        # Get first instance
        registry1 = get_registry()

        # Reset global
        registry_module._registry = None

        # Get new instance
        registry2 = get_registry()

        assert registry1 is not registry2
