# -----------------------------------------------------------------------------
# nexoia/registry.py
# -----------------------------------------------------------------------------
"""Runtime registry for provider clients used by the compatibility layer."""

from __future__ import annotations

from typing import Type

from .clients.base import BaseLLMClient

_CLIENTS: dict[str, Type[BaseLLMClient]] = {}


def register_client(name: str, cls: Type[BaseLLMClient]) -> None:
    _CLIENTS[name.lower()] = cls


def get_client(name: str) -> Type[BaseLLMClient]:
    return _CLIENTS[name.lower()]
