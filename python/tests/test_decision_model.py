"""Tests for TemplateDecisionModel."""

import pytest
from strands.decisions import DecisionModel

from strands_template import TemplateDecisionModel


def test_template_decision_model_init():
    """Test initialization."""
    decisions = TemplateDecisionModel(api_key="test-key")
    assert isinstance(decisions, DecisionModel)
    assert decisions.api_key == "test-key"


async def test_ask_raises_until_implemented():
    """ask delegates to _ask, which the skeleton leaves unimplemented."""
    decisions = TemplateDecisionModel(api_key="test-key")
    with pytest.raises(NotImplementedError):
        await decisions.ask(
            "A customer needs a refund today.",
            {"urgent": {"question": "Is this urgent?", "choices": "boolean"}},
        )
