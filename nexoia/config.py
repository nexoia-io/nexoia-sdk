# -----------------------------------------------------------------------------
# nexoia/config.py
# -----------------------------------------------------------------------------
"""Centralised configuration loader.

Supports:
* YAML file indicated by ``$NEXOIA_CONFIG`` (default: ``~/.config/nexoia.yaml``)
* Environment variables ``<PROVIDER>_API_KEY`` (e.g. ``OPENAI_API_KEY``)
"""

from __future__ import annotations

import os
import pathlib
from typing import Any, Mapping

import yaml

_DEFAULT_CONFIG_PATH = pathlib.Path.home() / ".config" / "nexoia.yaml"


def _load_yaml(path: pathlib.Path) -> Mapping[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf‑8") as fp:
        return yaml.safe_load(fp) or {}


def load_config() -> Mapping[str, Any]:
    """Return merged configuration from YAML (if any)."""
    path = pathlib.Path(os.getenv("NEXOIA_CONFIG", _DEFAULT_CONFIG_PATH))
    return _load_yaml(path)


_CONFIG_CACHE: Mapping[str, Any] | None = None


def get_api_key(provider: str) -> str | None:
    """Lookup API key for *provider* (case‑insensitive) in YAML config."""
    global _CONFIG_CACHE
    if _CONFIG_CACHE is None:
        _CONFIG_CACHE = load_config()

    key = _CONFIG_CACHE.get("api_keys", {}).get(provider.lower())  # type: ignore[index]
    return key