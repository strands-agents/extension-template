"""Tests for TemplatePlugin."""

from strands_template import TemplatePlugin


def test_template_plugin_init():
    """Test initialization."""
    plugin = TemplatePlugin()
    assert plugin.name is not None
