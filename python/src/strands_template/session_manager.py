"""Session Manager Implementation."""

import logging
from typing import TYPE_CHECKING, Any

from strands.session.session_manager import SessionManager
from strands.types.content import Message

if TYPE_CHECKING:
    from strands.agent.agent import Agent

logger = logging.getLogger(__name__)


class TemplateSessionManager(SessionManager):
    """Template session manager implementation."""

    def __init__(self, session_id: str) -> None:
        """Initialize the session manager."""
        self.session_id = session_id

    def initialize(self, agent: "Agent", **kwargs: Any) -> None:
        """Initialize an agent with session data."""
        pass

    def append_message(self, message: Message, agent: "Agent", **kwargs: Any) -> None:
        """Append a message to the session storage."""
        pass

    def redact_latest_message(self, redact_message: Message, agent: "Agent", **kwargs: Any) -> None:
        """Redact (replace) the most recently appended message."""
        pass

    def sync_agent(self, agent: "Agent", **kwargs: Any) -> None:
        """Synchronize agent state with session storage."""
        pass
