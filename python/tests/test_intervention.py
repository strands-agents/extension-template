"""Tests for TemplateIntervention."""

from strands_template import TemplateIntervention


def test_template_intervention_exposes_name():
    """The handler exposes its stable name."""
    handler = TemplateIntervention()
    assert handler.name == "template-intervention"
