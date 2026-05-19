"""Tests for TemplateSessionManager."""

from strands_template import TemplateSessionManager


def test_template_session_manager_init():
    """Test initialization."""
    session = TemplateSessionManager(session_id="test-session")
    assert session.session_id == "test-session"
