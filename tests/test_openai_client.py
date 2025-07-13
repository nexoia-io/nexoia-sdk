# tests/test_openai_client.py
"""Tests for OpenAIClient with monkey‑patched SDK (no real dependency)."""

from __future__ import annotations

import sys
import types
from types import SimpleNamespace

import pytest


class _FakeChat:
    def __init__(self):
        self.completions = SimpleNamespace(create=self._create)

    def _create(self, **_):
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="pong"))])


class _FakeOpenAI:
    def __init__(self, *_, **__):
        self.chat = _FakeChat()


@pytest.fixture(autouse=True)
def _patch_openai(monkeypatch):
    """Insert a fake 'openai' module before any import happens."""

    fake_module = types.ModuleType("openai")
    fake_module.OpenAI = _FakeOpenAI  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "openai", fake_module)
    yield
    # cleanup handled automatically by monkeypatch fixture


def test_openai_client_generate_text():
    # Import after the patch so it sees the fake SDK
    from nexoia.clients.openai_client import OpenAIClient  # noqa: WPS433

    client = OpenAIClient(api_key="key")
    txt = client.generate_text("ping")
    assert txt == "pong"
    client = OpenAIClient(api_key="key")
    txt = client.generate_text("ping")
    assert txt == "pong"