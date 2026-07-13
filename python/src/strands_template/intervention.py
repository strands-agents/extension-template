"""Intervention Handler Implementation."""

import logging
from typing import Any

from strands.hooks.events import BeforeToolCallEvent
from strands.interventions import InterventionHandler, Proceed, Deny

logger = logging.getLogger(__name__)


class TemplateIntervention(InterventionHandler):
    """Template intervention handler implementation.

    Intervention handlers provide composable control layers for agents.
    Override lifecycle methods to intercept events and return typed
    decisions (Proceed, Deny, Guide, Confirm, Transform).

    Example:
        ```python
        from strands import Agent
        from strands_template import TemplateIntervention

        handler = TemplateIntervention()
        agent = Agent(interventions=[handler])
        ```
    """

    name = "template-intervention"

    # Override any lifecycle methods you need — not just before_tool_call.

    def before_tool_call(self, event: BeforeToolCallEvent, **kwargs: Any) -> Proceed | Deny:
        """Called before a tool is executed.

        Args:
            event: The before-tool-call event with tool_use and agent reference.
        """
        # TODO: Implement your intervention logic
        return Proceed()
