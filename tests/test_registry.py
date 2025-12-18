# tests/test_registry.py
"""Unit tests for nexoia.registry."""

from nexoia.clients.base import BaseLLMClient
from nexoia.registry import get_client, register_client


class _Dummy(BaseLLMClient):
    ENV_API_KEY = "DUMMY_KEY"

    def _init_http(self) -> None:
        pass

    def generate_text(self, prompt: str, **kw):  # type: ignore[override]
        return prompt.upper()

    def get_model_info(self):  # type: ignore[override]
        from nexoia.clients.base import ModelInfo

        return ModelInfo("dummy", "0.1", "Dummy client", "dummy")


def test_registry_roundtrip():
    register_client("dummy", _Dummy)
    cls = get_client("DUMMY")
    assert issubclass(cls, BaseLLMClient)
    assert cls is _Dummy
