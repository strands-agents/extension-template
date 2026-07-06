"""Tests for TemplateMemoryStore."""

from strands_template import TemplateMemoryStore


def test_template_memory_store_init():
    """Test initialization from config."""
    store = TemplateMemoryStore(name="notes", description="scratch notes")
    assert store.name == "notes"
    assert store.description == "scratch notes"


def test_writable_from_config():
    """writable is read from config, defaulting to False."""
    assert TemplateMemoryStore(name="notes", writable=True).writable is True
