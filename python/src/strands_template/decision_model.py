"""Decision Model Implementation."""

import logging
from typing import Any

from strands.decisions import DecisionInput, DecisionModel, DecisionResult, Question

logger = logging.getLogger(__name__)


class TemplateDecisionModel(DecisionModel):
    """Template decision model implementation.

    Decision models answer closed questions (yes/no or one of a fixed set of
    choices) over agent state. The inherited ask method validates the questions
    and records tracing and usage, then delegates to _ask.

    Example:
        ```python
        from strands_template import TemplateDecisionModel

        decisions = TemplateDecisionModel(api_key="...")
        result = await decisions.ask(
            "A customer needs a refund today.",
            {"urgent": {"question": "Is this urgent?", "choices": "boolean"}},
        )
        ```
    """

    def __init__(self, api_key: str) -> None:
        """Initialize the decision model.

        Args:
            api_key: API key for the upstream provider.
        """
        self.api_key = api_key

    async def _ask(self, state: DecisionInput, questions: dict[str, Question], **kwargs: Any) -> DecisionResult:
        """Answer the questions over the given state.

        Args:
            state: A plain string, a content list, or a message history.
            questions: Map of identifier to question.
            **kwargs: Additional keyword arguments for future extensibility.

        Returns:
            A DecisionResult with one answer per question identifier: a bool for
            "boolean" choices, one of the listed choices otherwise, or Uncertain
            when the question allows it.
        """
        # TODO: Send the state and questions to your provider and map its response.
        # Set metadata.latency_ms from the provider call, and usage when the
        # provider reports token counts.
        raise NotImplementedError
