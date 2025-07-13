# tests/test_patcher.py
"""Ensure patch_openai aliases correctly with fake SDK present."""

import importlib
import sys
import types

from nexoia.patcher import patch_openai


def test_patcher_alias(monkeypatch):
    fake_module = types.ModuleType("openai")
    fake_module.OpenAI = lambda *_, **__: None  # type: ignore[arg-type]
    monkeypatch.setitem(sys.modules, "openai", fake_module)

    compat = patch_openai()
    mod = importlib.import_module("openai")
    assert mod is compat