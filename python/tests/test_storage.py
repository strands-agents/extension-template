"""Tests for TemplateStorage."""

from strands.storage import Storage

from strands_template import TemplateStorage


def test_template_storage_init():
    """Test initialization."""
    storage = TemplateStorage()
    assert isinstance(storage, TemplateStorage)


def test_satisfies_storage_protocol():
    """TemplateStorage satisfies the Storage protocol."""
    storage = TemplateStorage()
    assert isinstance(storage, Storage)
