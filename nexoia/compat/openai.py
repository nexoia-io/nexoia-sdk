# -----------------------------------------------------------------------------
# nexoia/compat/openai.py  (simplified stub for v0.1)
# -----------------------------------------------------------------------------
"""Minimal subset of the official openai API surface implemented via registry.

Only implements ``chat.completions.create`` for now.  Delegates to a registered
client based on the *model* parameter.  Example::

    import nexoia.patcher; nexoia.patcher.patch_openai()
    import openai  # this module
    resp = openai.chat.completions.create(model="deepseek/chat", messages=[...])
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from ..registry import get_client
from ..clients.openai_client import OpenAIClient  # ensure OpenAI is registered
from ..clients.deepseek_client import DeepSeekClient

# Register built‑in providers (users can register more before calling patch)
from ..registry import register_client

register_client("openai", OpenAIClient)
register_client("deepseek", DeepSeekClient)


class _ChatCompletions:
    @staticmethod
    def create(*, model: str, messages: list[dict[str, str]], **kwargs: Any):
        provider, _, mname = model.partition("/") if "/" in model else ("openai", "", model)
        ClientCls = get_client(provider)
        client = ClientCls()
        prompt = "\n".join(msg["content"] for msg in messages)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=client.generate_text(prompt, model=mname, **kwargs)))],
        )


class _Chat:
    completions = _ChatCompletions()

# Expose the public API expected by openai users
chat = _Chat()