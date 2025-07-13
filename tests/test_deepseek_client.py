"""Tests for DeepSeekClient (simulated)."""

import sys
from types import SimpleNamespace

import pytest

from nexoia.clients.deepseek_client import DeepSeekClient


@pytest.fixture(autouse=True)
def _patch_httpx(monkeypatch):
    """Fake httpx.Client.post to avoid real network access."""

    class _FakeResp:
        status_code = 200

        def json(self):  # noqa: D401
            return {"generated_text": "Respuesta generada por DeepSeek para: hola"}

    class _FakeClient:
        def __init__(self, *_, **__):
            pass

        def post(self, *_, **__):  # noqa: D401
            return _FakeResp()

    monkeypatch.setattr("httpx.Client", _FakeClient)
    yield


def test_deepseek_simulated():
    client = DeepSeekClient(api_key="token")
    out = client.generate_text("hola")
    assert "hola" in out.lower()