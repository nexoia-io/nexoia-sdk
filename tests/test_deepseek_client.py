"""Tests for DeepSeekClient (simulated)."""

from __future__ import annotations

import httpx
import pytest


@pytest.fixture(autouse=True)
def _patch_httpx(monkeypatch):
    """Sustituye httpx.Client para evitar red real."""

    class _FakeResp:
        status_code = 200
        text = "ok"

        def raise_for_status(self):
            if self.status_code >= 400:
                raise httpx.HTTPStatusError(
                    "HTTP error",
                    request=httpx.Request("POST", "https://api.deepseek.com/chat/completions"),
                    response=self,
                )

        def json(self):
            return {
                "id": "ds_123",
                "model": "deepseek-chat",
                "choices": [
                    {
                        "message": {"content": "Respuesta generada por DeepSeek para: hola"},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 5,
                    "completion_tokens": 7,
                    "total_tokens": 12,
                },
            }

    class _FakeClient:
        def __init__(self, *_, **__):
            pass

        def post(self, *_, **__):
            return _FakeResp()

    monkeypatch.setattr(httpx, "Client", _FakeClient)
    yield


def test_deepseek_simulated():
    from nexoia.clients.deepseek_client import DeepSeekClient
    from nexoia.types import LLMResponse

    client = DeepSeekClient(api_key="token")
    out = client.generate("hola")

    assert isinstance(out, LLMResponse)
    assert "hola" in out.text.lower()
    assert out.provider == "deepseek"
    assert out.model == "deepseek-chat"
    assert out.finish_reason == "stop"
    assert out.usage is not None
    assert out.usage.input_tokens == 5
    assert out.usage.output_tokens == 7
    assert out.usage.total_tokens == 12