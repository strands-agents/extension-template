"""Plugin Implementation."""

import logging
from typing import TYPE_CHECKING

from strands import tool
from strands.hooks import BeforeToolCallEvent
from strands.plugins import Plugin, hook

if TYPE_CHECKING:
    from strands.agent.agent import Agent

logger = logging.getLogger(__name__)


class TemplatePlugin(Plugin):
    """Template plugin implementation.

    Plugins provide a composable way to extend agent behavior through
    automatic hook and tool registration. Methods decorated with @hook
    and @tool are discovered and registered automatically.

    Example:
        ```python
        from strands import Agent
        from strands_template import TemplatePlugin

        plugin = TemplatePlugin()
        agent = Agent(plugins=[plugin])
        ```
    """

    name = "template-plugin"

    def __init__(self) -> None:
        """Initialize the plugin."""
        super().__init__()

    def init_agent(self, agent: "Agent") -> None:
        """Initialize the plugin with an agent instance.

        Decorated hooks and tools are auto-registered by the plugin registry.
        Override this method to add custom initialization logic.

        Args:
            agent: The agent instance to extend.
        """
        pass

    @hook  # type: ignore[call-overload]
    def on_before_tool_call(self, event: BeforeToolCallEvent) -> None:
        """Hook that runs before each tool call.

        Args:
            event: The before-tool-call event with tool_use and agent reference.
        """
        # TODO: Implement your hook logic
        pass

    @tool
    def template_plugin_tool(self, param1: str) -> str:
        """Brief description of what your plugin tool does.

        Args:
            param1: Description of parameter 1.
        """
        # TODO: Implement your tool logic
        raise NotImplementedError
