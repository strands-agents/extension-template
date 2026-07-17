"""Tests for template_tool."""

from strands_template import template_tool


def test_template_tool_is_registered():
    """The @tool decorator exposes the function under its tool name."""
    assert template_tool.tool_name == "template_tool"

    # TODO: Add behavior tests once you implement the tool body.
