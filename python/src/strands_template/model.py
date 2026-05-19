"""Model Provider Implementation."""

import logging
from collections.abc import AsyncGenerator, AsyncIterable
from typing import Any, TypeVar

from pydantic import BaseModel
from strands.models.model import Model
from strands.types.content import Messages
from strands.types.streaming import StreamEvent
from strands.types.tools import ToolSpec
from typing_extensions import override

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class TemplateModel(Model):
    """Template model provider implementation."""

    def __init__(self, api_key: str, model_id: str) -> None:
        """Initialize the model provider."""
        self.api_key = api_key
        self.model_id = model_id

    @override
    def update_config(self, **model_config: Any) -> None:
        """Update the model configuration."""
        pass

    @override
    def get_config(self) -> dict[str, Any]:
        """Get the current model configuration."""
        return {"api_key": self.api_key, "model_id": self.model_id}

    @override
    async def stream(
        self,
        messages: Messages,
        tool_specs: list[ToolSpec] | None = None,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> AsyncIterable[StreamEvent]:
        """Stream conversation with the model."""
        # TODO: Implement streaming logic
        raise NotImplementedError
        yield  # type: ignore

    @override
    async def structured_output(
        self,
        output_model: type[T],
        prompt: Messages,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> AsyncGenerator[dict[str, T | Any], None]:
        """Generate structured output from the model."""
        # TODO: Implement structured output logic
        raise NotImplementedError
        yield  # type: ignore
