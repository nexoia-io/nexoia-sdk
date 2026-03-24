# nexoia/patcher.py

from __future__ import annotations

import importlib
import sys
from types import ModuleType


def patch_openai() -> ModuleType:  # pragma: no cover
    """Replace the ``openai`` module with :pymod:`nexoia.compat.openai`.

    After calling this function, ``import openai`` anywhere in the same Python
    process will actually import NexoIA's compatibility shim.
    """

    # Aseguramos que los proveedores built-in queden registrados
    try:
        importlib.import_module("nexoia.compat.deepseek")
    except ModuleNotFoundError:
        pass

    try:
        importlib.import_module("nexoia.compat.claude")
    except ModuleNotFoundError:
        pass
    try:
        importlib.import_module("nexoia.compat.gemini")
    except ModuleNotFoundError:
        pass

    compat = importlib.import_module("nexoia.compat.openai")
    sys.modules["openai"] = compat  # alias
    return compat
