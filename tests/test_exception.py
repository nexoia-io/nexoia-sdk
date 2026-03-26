import httpx
import pytest

from nexoia.clients.deepseek_client import DeepSeekClient
from nexoia.exceptions import APIError


def test_apierror_raised(monkeypatch):
    # Fake httpx response con 404
    class _FakeResp:
        status_code = 404
        text = "oops"

        def raise_for_status(self):
            raise httpx.HTTPStatusError(
                "HTTP error",
                request=httpx.Request("POST", "https://api.deepseek.com/chat/completions"),
                response=self,
            )

        def json(self):
            return {}

    class _FakeClient:
        def __init__(self, *_, **__):
            pass

        def post(self, *_, **__):
            return _FakeResp()

    monkeypatch.setattr("httpx.Client", _FakeClient)

    client = DeepSeekClient(api_key="x")

    with pytest.raises(APIError):
        client.generate("hola")