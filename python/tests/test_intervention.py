"""Tests for TemplateIntervention."""

from strands_template import TemplateIntervention


def test_template_intervention_init():
    """Test initialization."""
    handler = TemplateIntervention()
    assert handler.name is not None
