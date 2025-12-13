# tests/test_compat_claude.py
"""Tests for the nexoia.compat.claude compatibility layer."""

from __future__ import annotations

from typing import Any
import sys
import types

import pytest


def _install_fake_openai_module() -> None:
    """Inyecta un módulo 'openai' falso en sys.modules.

    Esto evita que nexoia.clients.openai_client falle al hacer:
        from openai import OpenAI
    durante los tests, sin requerir el paquete real.
    """
    if "openai" in sys.modules:
        return  # ya está instalado (por otro test)

    fake_openai = types.ModuleType("openai")

    class _DummyOpenAI:
        def __init__(self, *args, **kwargs) -> None:
            # Estructura mínima para que OpenAIClient pueda usar:
            #   self._client.chat.completions.create(...)
            self.chat = types.SimpleNamespace(
                completions=types.SimpleNamespace(
                    create=lambda **kw: types.SimpleNamespace(
                        choices=[
                            types.SimpleNamespace(
                                message=types.SimpleNamespace(content="pong")
                            )
                        ]
                    )
                )
            )


    fake_openai.OpenAI = _DummyOpenAI
    sys.modules["openai"] = fake_openai


def test_compat_claude_chat_completion(monkeypatch):
    """Comprueba que chat.completions.create:
    - valida/normaliza messages
    - concatena solo los mensajes de role 'user'
    - delega en ClaudeClient.generate_text
    - devuelve un objeto con choices[0].message.content
    """

    # 1) Módulo openai falso para que OpenAIClient no reviente
    _install_fake_openai_module()

    # 2) API KEY requerida por ClaudeClient (aunque luego ignoraremos __init__)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

    # 3) Importamos compat.claude y el cliente concreto
    from nexoia.compat import claude  # noqa: WPS433
    from nexoia.clients.claude_client import ClaudeClient

    # 4) Evitar que ClaudeClient.__init__ llame a BaseLLMClient.__init__
    #    (así no tocamos get_api_key ni la caché de config)
    def fake_init(self, *args: Any, **kwargs: Any) -> None:
        # Sólo definimos los atributos que podrían ser usados en tests futuros
        self.api_key = "dummy"
        self.timeout = 10

    monkeypatch.setattr(ClaudeClient, "__init__", fake_init, raising=True)

    called: dict[str, Any] = {}

    def fake_generate_text(
        self,
        prompt: str,
        *,
        model: str,
        max_tokens: int = 512,
        **kw: Any,
    ) -> str:
        called["prompt"] = prompt
        called["model"] = model
        called["max_tokens"] = max_tokens
        called["extra"] = kw
        return "pong-claude"

    monkeypatch.setattr(
        ClaudeClient,
        "generate_text",
        fake_generate_text,
        raising=True,
    )

    resp = claude.chat.completions.create(
        model="claude-sonnet-4-5",
        messages=[
            {"role": "system", "content": "Eres un asistente."},
            {"role": "user", "content": "Hola 1"},
            {"role": "assistant", "content": "Algo previo"},
            {"role": "user", "content": "Hola 2"},
        ],
        max_tokens=128,
        temperature=0.3,
    )

    # El resultado imita la API de OpenAI
    assert resp.choices[0].message.content == "pong-claude"

    # Prompt = concatenación de los mensajes user
    assert called["prompt"] == "Hola 1\nHola 2"
    assert called["model"] == "claude-sonnet-4-5"
    assert called["max_tokens"] == 128
    # temperature debería viajar en **kw
    assert called["extra"].get("temperature") == 0.3


def test_compat_claude_invalid_messages_type():
    """Debe fallar si messages no es una lista."""
    _install_fake_openai_module()
    from nexoia.compat import claude

    with pytest.raises(ValueError):
        claude.chat.completions.create(
            model="claude-sonnet-4-5",
            messages="no es una lista",  # type: ignore[arg-type]
        )


def test_compat_claude_invalid_message_shape():
    """Debe fallar si un mensaje no tiene role/content."""
    _install_fake_openai_module()
    from nexoia.compat import claude

    with pytest.raises(ValueError):
        claude.chat.completions.create(
            model="claude-sonnet-4-5",
            messages=[{"role": "user"}],  # falta 'content'
        )
