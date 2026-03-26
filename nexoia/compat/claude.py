# -----------------------------------------------------------------------------
# nexoia/compat/claude.py
# -----------------------------------------------------------------------------
"""Superficie tipo OpenAI, respaldada por ClaudeClient (Anthropic)."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from ..clients.claude_client import ClaudeClient
from ..registry import register_client

# Registrar el provider en el runtime registry
register_client("claude", ClaudeClient)


def _ensure_messages(messages: Any) -> list[dict[str, str]]:
    if not isinstance(messages, list):
        raise ValueError("`messages` debe ser lista de {'role','content'}.")

    for m in messages:
        if not isinstance(m, dict) or "role" not in m or "content" not in m:
            raise ValueError("Cada mensaje debe ser dict {'role': str, 'content': str}.")

    return messages  # type: ignore[return-value]


def _extract_prompt(messages: list[dict[str, str]]) -> str:
    # Igual que en compat.deepseek: concatenamos el contenido de los roles 'user'
    return "\n".join(m["content"] for m in messages if m.get("role") == "user").strip()


class _ChatCompletions:
    @staticmethod
    def create(*, model: str, messages: Any, **kwargs: Any):
        msgs = _ensure_messages(messages)
        prompt = _extract_prompt(msgs)

        client = ClaudeClient()
        resp = client.generate(prompt, model=model, **kwargs)

        return SimpleNamespace(
            id=resp.response_id,
            model=resp.model,
            created=resp.created,
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content=resp.text),
                    finish_reason=resp.finish_reason,
                )
            ],
        )

class _Chat:
    completions = _ChatCompletions()


# API público al estilo openai
chat = _Chat()
