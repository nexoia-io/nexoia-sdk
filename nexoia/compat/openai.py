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

from ..clients.openai_client import OpenAIClient  # ensure OpenAI is registered

# Register built‑in providers (users can register more before calling patch)
from ..registry import get_client, register_client

register_client("openai", OpenAIClient)


class _ChatCompletions:
    def create(self, *, model: str, messages: list[dict], **kwargs):
        provider = kwargs.pop("provider", "openai")

        client_cls = get_client(provider)
        client = client_cls()

        prompt_parts: list[str] = []
        for msg in messages:
            content = msg.get("content")
            if isinstance(content, str):
                prompt_parts.append(content)

        prompt = "\n".join(prompt_parts)

        resp = client.generate(prompt, model=model, **kwargs)

        usage_ns = None
        if resp.usage is not None:
            usage_ns = SimpleNamespace(
                prompt_tokens=resp.usage.input_tokens,
                completion_tokens=resp.usage.output_tokens,
                total_tokens=resp.usage.total_tokens,
            )

        return SimpleNamespace(
            id=resp.response_id,
            model=resp.model,
            created=resp.created,
            usage=usage_ns,
            choices=[
                SimpleNamespace(
                    finish_reason=resp.finish_reason,
                    message=SimpleNamespace(
                        content=resp.text,
                        tool_calls=list(resp.tool_calls),
                    ),
                )
            ],
        )


class _Chat:
    completions = _ChatCompletions()


# Expose the public API expected by openai users
chat = _Chat()
