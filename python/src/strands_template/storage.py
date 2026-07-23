"""Storage Implementation."""

import builtins
import logging

logger = logging.getLogger(__name__)


class TemplateStorage:
    """Template storage backend implementation.

    Storage backends persist raw bytes under string keys. The SDK uses the
    Storage interface for session snapshots, context offloading, and any
    construct that needs durable key-value persistence.

    Example:
        ```python
        from strands import Agent
        from strands.session import SessionManager
        from strands_template import TemplateStorage

        storage = TemplateStorage()
        agent = Agent(session_manager=SessionManager(storage=storage))
        ```
    """

    def __init__(self) -> None:
        """Initialize the storage backend."""
        # TODO: Add backend-specific constructor arguments.

    async def write(self, key: str, data: bytes) -> None:
        """Store data under key, overwriting any existing value.

        Args:
            key: Opaque, '/'-separated key identifying the value.
            data: Raw bytes to persist.
        """
        # TODO: Persist the data to your backend.
        raise NotImplementedError

    async def read(self, key: str) -> bytes | None:
        """Retrieve the bytes previously stored under key.

        Args:
            key: The key to read.

        Returns:
            The stored bytes, or None if no value exists for key.
        """
        # TODO: Read from your backend, return None if not found.
        raise NotImplementedError

    async def delete(self, key: str) -> None:
        """Delete the value stored under key. A no-op if the key does not exist.

        Args:
            key: The key to delete.
        """
        # TODO: Delete from your backend.
        raise NotImplementedError

    async def list(self, query: str = "") -> builtins.list[str]:
        """List keys matching the given prefix query.

        Args:
            query: A prefix string to filter keys. Empty string matches all.

        Returns:
            Matching keys sorted ascending.
        """
        # TODO: Query your backend for keys matching the prefix.
        raise NotImplementedError
