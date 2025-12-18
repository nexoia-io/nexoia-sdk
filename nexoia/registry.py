# -----------------------------------------------------------------------------
# nexoia/registry.py
# -----------------------------------------------------------------------------
"""Runtime registry for provider clients used by the compatibility layer."""

from __future__ import annotations

from .clients.base import BaseLLMClient

_CLIENTS: dict[str, type[BaseLLMClient]] = {}


def register_client(name: str, cls: type[BaseLLMClient]) -> None:
    _CLIENTS[name.lower()] = cls


def get_client(name: str) -> type[BaseLLMClient]:
    return _CLIENTS[name.lower()]
