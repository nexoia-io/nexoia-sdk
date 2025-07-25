"""Tests for DeepSeekClient (simulated)."""

import httpx
import pytest


@pytest.fixture(autouse=True)
def _patch_httpx(monkeypatch):
    """Sustituye httpx.Client para evitar red real."""

    class _FakeResp:
        status_code = 200

        def json(self):
            # <-- aquí estaba el problema: faltaba la llave de cierre
            return {
                "choices": [
                    {"message": {"content": "Respuesta generada por DeepSeek para: hola"}}
                ]
            }

    class _FakeClient:
        def __init__(self, *_, **__):
            pass

        def post(self, *_, **__):
            return _FakeResp()

    monkeypatch.setattr(httpx, "Client", _FakeClient)
    yield


def test_deepseek_simulated():
    # Importa después del patch
    from nexoia.clients.deepseek_client import DeepSeekClient

    client = DeepSeekClient(api_key="token")
    out = client.generate_text("hola")
    assert "hola" in out.lower()
