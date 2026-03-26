# tests/test_openai_client.py
"""Tests for OpenAIClient with monkey-patched SDK (no real dependency)."""

from __future__ import annotations

import sys
import types
from types import SimpleNamespace

import pytest


class _FakeChat:
    def __init__(self):
        self.completions = SimpleNamespace(create=self._create)

    def _create(self, **_):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content="pong"),
                )
            ]
        )


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


def test_openai_client_generate():
    from nexoia.clients.openai_client import OpenAIClient
    from nexoia.types import LLMResponse

    client = OpenAIClient(api_key="key")
    out = client.generate("ping")

    assert isinstance(out, LLMResponse)
    assert out.text == "pong"
    assert out.provider == "openai"
    assert out.model == "gpt-3.5-turbo"
    assert out.finish_reason is None