"""Tests for TemplateConversationManager."""

from strands_template import TemplateConversationManager


def test_template_conversation_manager_init():
    """Test initialization."""
    cm = TemplateConversationManager()
    assert cm is not None
