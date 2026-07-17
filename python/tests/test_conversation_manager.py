"""Tests for TemplateConversationManager."""

from strands.agent.conversation_manager.conversation_manager import ConversationManager

from strands_template import TemplateConversationManager


def test_template_conversation_manager_implements_interface():
    """Constructing proves the skeleton implements every abstract method."""
    cm = TemplateConversationManager()
    assert isinstance(cm, ConversationManager)
