# -----------------------------------------------------------------------------
# nexoia/compat/deepseek.py
# -----------------------------------------------------------------------------
"""Surface tipo OpenAI, respaldada por el cliente DeepSeek."""

from __future__ import annotations
from types import SimpleNamespace
from typing import Any, List, Dict

from ..clients.deepseek_client import DeepSeekClient

from ..registry import register_client

register_client("deepseek", DeepSeekClient )

def _ensure_messages(messages: Any) -> List[Dict[str, str]]:
    if not isinstance(messages, list):
        raise ValueError("`messages` debe ser lista de {'role','content'}.")
    for m in messages:
        if not isinstance(m, dict) or "role" not in m or "content" not in m:
            raise ValueError("Cada mensaje debe ser dict {'role': str, 'content': str}.")
    return messages  # type: ignore[return-value]

def _extract_prompt(messages: List[Dict[str, str]]) -> str:
    return "\n".join(m["content"] for m in messages if m.get("role") == "user").strip()

class _ChatCompletions:
    @staticmethod
    def create(*, model: str, messages: Any, **kwargs: Any):
        msgs = _ensure_messages(messages)
        prompt = _extract_prompt(msgs)
        client = DeepSeekClient()
        text = client.generate_text(prompt, model=model, **kwargs)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=text))]
        )

class _Chat:
    completions = _ChatCompletions()

chat = _Chat()
