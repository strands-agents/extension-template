"""Memory Store Implementation."""

import logging
from typing import Any

from strands.memory import AddMessagesContext, MemoryEntry, MemoryStore, MemoryStoreConfig, SearchOptions
from strands.types.content import Message
from typing_extensions import Unpack

logger = logging.getLogger(__name__)


class TemplateMemoryStoreConfig(MemoryStoreConfig, total=False):
    """Configuration for a TemplateMemoryStore, passed as its constructor kwargs.

    Extends MemoryStoreConfig (name, description, max_search_results, writable,
    extraction) with any backend-specific fields your store needs.
    """

    # TODO: replace with a backend-specific field your store needs (e.g. namespace, index name).
    connection_string: str


class TemplateMemoryStore(MemoryStore):
    """Template memory store implementation.

    Memory stores give an agent cross-session knowledge: a MemoryManager
    searches them to recall facts and, when writable, writes new ones.

    Example:
        ```python
        from strands import Agent
        from strands.memory import MemoryManager
        from strands_template import TemplateMemoryStore

        store = TemplateMemoryStore(name="notes")
        agent = Agent(memory_manager=MemoryManager(stores=[store]))
        ```
    """

    def __init__(self, **store_config: Unpack[TemplateMemoryStoreConfig]) -> None:
        """Initialize the memory store."""
        self.name = store_config["name"]
        self.description = store_config.get("description")
        self.max_search_results = store_config.get("max_search_results")
        self.writable = store_config.get("writable", False)
        self.extraction = store_config.get("extraction")

    async def search(self, query: str, options: SearchOptions | None = None) -> list[MemoryEntry]:
        """Search the store for entries matching the query, ordered by relevance."""
        # TODO: Query your backend and map each hit to a MemoryEntry.
        raise NotImplementedError

    async def add(self, content: str, metadata: dict[str, Any] | None = None) -> Any:
        """Write one discrete entry. Can be implemented alongside add_messages."""
        # TODO: Persist the memory to your backend.
        raise NotImplementedError

    async def add_messages(self, messages: list[Message], context: AddMessagesContext | None = None) -> Any:
        """Ingest raw conversation turns for server-side extraction. Not implemented for vector-DB-style backends."""
        # TODO: Hand the raw messages to your backend to extract and store.
        raise NotImplementedError
