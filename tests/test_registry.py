# tests/test_registry.py
"""Unit tests for nexoia.registry."""

from __future__ import annotations

from nexoia.clients.base import BaseLLMClient
from nexoia.registry import get_client, register_client
from nexoia.types import LLMResponse


class _Dummy(BaseLLMClient):
    ENV_API_KEY = "DUMMY_KEY"

    def _init_http(self) -> None:
        pass

    def generate(self, prompt: str, **kw) -> LLMResponse:  # type: ignore[override]
        return LLMResponse(
            text=prompt.upper(),
            provider="dummy",
            model="dummy-model",
        )

    def get_model_info(self):  # type: ignore[override]
        from nexoia.clients.base import ModelInfo

        return ModelInfo("dummy", "0.1", "Dummy client", "dummy")


def test_registry_roundtrip():
    register_client("dummy", _Dummy)
    cls = get_client("DUMMY")
    assert issubclass(cls, BaseLLMClient)
    assert cls is _Dummy