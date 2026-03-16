"""Tests for TemplateModel."""

from strands_template import TemplateModel


def test_template_model_init():
    """Test initialization."""
    model = TemplateModel(api_key="test-key", model_id="test-model")
    config = model.get_config()
    assert config["api_key"] == "test-key"
    assert config["model_id"] == "test-model"
