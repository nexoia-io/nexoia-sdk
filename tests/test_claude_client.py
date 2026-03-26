# tests/test_claude_client.py
"""Tests for ClaudeClient (simulated)."""

from __future__ import annotations

import httpx
import pytest
from nexoia.exceptions import APIError


@pytest.fixture(autouse=True)
def _patch_httpx(monkeypatch):
    """Sustituye httpx.Client para evitar red real (caso OK por defecto)."""

    class _FakeResp:
        status_code = 200

        def __init__(self, payload: dict | None = None, text: str = "ok"):
            self._payload = payload or {
                "content": [{"type": "text", "text": "Respuesta Claude para: hola"}]
            }
            self.text = text

        def raise_for_status(self):
            if self.status_code >= 400:
                raise httpx.HTTPStatusError(
                    "HTTP error",
                    request=httpx.Request("POST", "https://api.anthropic.com/v1/messages"),
                    response=self,
                )

        def json(self):
            return self._payload

    class _FakeClient:
        def __init__(self, *_, **__):
            self.last_url = None
            self.last_json = None

        def post(self, url, json=None, **kwargs):
            self.last_url = url
            self.last_json = json
            return _FakeResp()

    monkeypatch.setattr(httpx, "Client", _FakeClient)
    yield


def test_claude_generate_basic():
    from nexoia.clients.claude_client import ClaudeClient
    from nexoia.types import LLMResponse

    client = ClaudeClient(api_key="token")
    out = client.generate("hola", model="claude-sonnet-4-5", max_tokens=123)

    assert isinstance(out, LLMResponse)
    assert isinstance(out.text, str)
    assert "claude" in out.text.lower() or "respuesta" in out.text.lower()
    assert out.provider == "anthropic"
    assert out.model is not None
    assert isinstance(out.content_blocks, tuple)
    assert len(out.content_blocks) == 1
    assert out.content_blocks[0]["type"] == "text"


def test_claude_uses_messages_payload(monkeypatch):
    """Verifica que el payload enviado sigue el formato esperado por Claude."""
    captured = {}

    class _FakeResp:
        status_code = 200

        def __init__(self):
            self.text = "ok"

        def raise_for_status(self):
            if self.status_code >= 400:
                raise httpx.HTTPStatusError(
                    "HTTP error",
                    request=httpx.Request("POST", "https://api.anthropic.com/v1/messages"),
                    response=self,
                )

        def json(self):
            return {"content": [{"type": "text", "text": "algo"}]}

    class _FakeClient:
        def __init__(self, *_, **__):
            self.last_url = None
            self.last_json = None

        def post(self, url, json=None, **kwargs):
            captured["url"] = url
            captured["json"] = json
            return _FakeResp()

    monkeypatch.setattr(httpx, "Client", _FakeClient)

    from nexoia.clients.claude_client import ClaudeClient
    from nexoia.types import LLMResponse

    client = ClaudeClient(api_key="token", endpoint="https://api.anthropic.com")
    prompt = "Hola Claude"
    out = client.generate(prompt, model="claude-sonnet-4-5", max_tokens=42)

    assert isinstance(out, LLMResponse)
    assert out.text == "algo"
    assert out.provider == "anthropic"

    assert captured["url"].endswith("/v1/messages")
    body = captured["json"]
    assert body["model"] == "claude-sonnet-4-5"
    assert body["max_tokens"] == 42
    assert body["messages"][0]["role"] == "user"
    assert body["messages"][0]["content"] == prompt


def test_claude_raises_on_http_error(monkeypatch):
    """Si el status_code != 200 debe lanzar APIError."""

    class _FakeResp:
        status_code = 500
        text = "boom"

        def raise_for_status(self):
            raise httpx.HTTPStatusError(
                "boom",
                request=httpx.Request("POST", "https://api.anthropic.com/v1/messages"),
                response=self,
            )

        def json(self):
            return {}

    class _FakeClient:
        def __init__(self, *_, **__):
            pass

        def post(self, *_, **__):
            return _FakeResp()

    monkeypatch.setattr(httpx, "Client", _FakeClient)

    from nexoia.clients.claude_client import ClaudeClient

    client = ClaudeClient(api_key="token")

    with pytest.raises(APIError):
        client.generate("hola")