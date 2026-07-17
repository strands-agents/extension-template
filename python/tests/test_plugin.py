"""Tests for TemplatePlugin."""

from strands_template import TemplatePlugin


def test_template_plugin_exposes_name():
    """The plugin exposes its stable name."""
    plugin = TemplatePlugin()
    assert plugin.name == "template-plugin"
