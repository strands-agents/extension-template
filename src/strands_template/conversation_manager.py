"""Conversation Manager Implementation."""

import logging
from typing import TYPE_CHECKING, Any

from strands.agent.conversation_manager.conversation_manager import ConversationManager

if TYPE_CHECKING:
    from strands.agent.agent import Agent

logger = logging.getLogger(__name__)


class TemplateConversationManager(ConversationManager):
    """Template conversation manager implementation."""

    def __init__(self) -> None:
        """Initialize the conversation manager."""
        super().__init__()

    def apply_management(self, agent: "Agent", **kwargs: Any) -> None:
        """Apply conversation management strategy."""
        pass

    def reduce_context(self, agent: "Agent", e: Exception | None = None, **kwargs: Any) -> None:
        """Reduce conversation context when overflow occurs."""
        pass
