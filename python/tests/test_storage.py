"""Tests for TemplateStorage."""

from unittest.mock import AsyncMock

import pytest
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


@pytest.mark.parametrize(
    ("query", "expected_keys"),
    [
        ("session snapshot", ["matching", "partial"]),
        ("unmatched", []),
    ],
)
async def test_search_uses_persistence_methods(monkeypatch, query, expected_keys):
    """A backend implementing list and read gets ranked keyword search."""
    data = {
        "partial": b"session",
        "unrelated": b"agent tools",
        "matching": b"session snapshot",
    }
    storage = TemplateStorage()
    monkeypatch.setattr(storage, "list", AsyncMock(return_value=list(data)))
    monkeypatch.setattr(storage, "read", AsyncMock(side_effect=data.get))

    results = await storage.search(query)

    assert [result.key for result in results] == expected_keys
    assert all(result.data == data[result.key] for result in results)
