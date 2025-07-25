import pytest
from nexoia.clients.deepseek_client import DeepSeekClient
from nexoia.exceptions import APIError


def test_apierror_raised(monkeypatch):
    # Fake httpx response con 404
    class _FakeResp:
        status_code = 404
        text = "oops"

    class _FakeClient:
        def __init__(self, *_, **__):
            pass                       # acepta cualquier argumento

        def post(self, *_, **__):
            return _FakeResp()

    monkeypatch.setattr("httpx.Client", _FakeClient)

    client = DeepSeekClient(api_key="x")
    with pytest.raises(APIError):
        client.generate_text("hola")