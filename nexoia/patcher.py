# -----------------------------------------------------------------------------
# nexoia/patcher.py
# -----------------------------------------------------------------------------
"""Monkey-patch helper to alias ``openai`` to ``nexoia.compat``."""

from __future__ import annotations

import importlib
import sys
from types import ModuleType
from typing import Any


def patch_openai() -> ModuleType:  # pragma: no cover
    """Replace the ``openai`` module with :pymod:`nexoia.compat.openai`.

    After calling this function, ``import openai`` anywhere in the same Python
    process will actually import NexoIA's compatibility shim.
    """

    compat = importlib.import_module("nexoia.compat.openai")
    sys.modules["openai"] = compat  # alias
    return compat