# tests/test_compat_gemini.py
from __future__ import annotations

from typing import Any

import pytest


def test_compat_gemini_chat_completion(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    from nexoia.clients.gemini_client import GeminiClient
    from nexoia.compat import gemini

    def fake_init(self, *args: Any, **kwargs: Any) -> None:
        self.api_key = "dummy"
        self.timeout = 10

    monkeypatch.setattr(GeminiClient, "__init__", fake_init, raising=True)

    called: dict[str, Any] = {}

    def fake_generate_text(
        self,
        prompt: str,
        *,
        model: str,
        **kw: Any,
    ) -> str:
        called["prompt"] = prompt
        called["model"] = model
        called["extra"] = kw
        return "pong-gemini"

    monkeypatch.setattr(
        GeminiClient,
        "generate_text",
        fake_generate_text,
        raising=True,
    )

    resp = gemini.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {"role": "system", "content": "Eres un asistente."},
            {"role": "user", "content": "Hola 1"},
            {"role": "assistant", "content": "Algo previo"},
            {"role": "user", "content": "Hola 2"},
        ],
        temperature=0.3,
    )

    assert resp.choices[0].message.content == "pong-gemini"
    assert called["prompt"] == "Hola 1\nHola 2"
    assert called["model"] == "gemini-1.5-flash"
    assert called["extra"].get("temperature") == 0.3


def test_compat_gemini_invalid_messages_type():
    from nexoia.compat import gemini

    with pytest.raises(ValueError):
        gemini.chat.completions.create(
            model="gemini-1.5-flash",
            messages="no es una lista",  # type: ignore[arg-type]
        )


def test_compat_gemini_invalid_message_shape():
    from nexoia.compat import gemini

    with pytest.raises(ValueError):
        gemini.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": "user"}],  # falta content
        )