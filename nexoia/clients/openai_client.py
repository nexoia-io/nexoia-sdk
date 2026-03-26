# -----------------------------------------------------------------------------
# nexoia/clients/openai_client.py
# -----------------------------------------------------------------------------
"""Wrapper around the official openai SDK to comply with BaseLLMClient."""

from __future__ import annotations

from typing import Any

try:
    from openai import OpenAI  # official SDK (\u2265 1.23)
except ModuleNotFoundError as exc:  # pragma: no cover
    raise RuntimeError("openai package is required to use OpenAIClient") from exc

from ..types import LLMResponse, TokenUsage
from .base import BaseLLMClient, ModelInfo


class OpenAIClient(BaseLLMClient):
    """Thin wrapper delegating to :pypi:`openai` while matching BaseLLMClient."""

    PROVIDER_SLUG = "openai"
    ENV_API_KEY = "OPENAI_API_KEY"

    def _init_http(self) -> None:  # noqa: D401
        # openai SDK creates its own client internally; just cache an instance
        self._client = OpenAI(api_key=self.api_key, timeout=self.timeout)

    # ------------------------------- LLM methods ----------------------------

    def generate(self, prompt: str, *, model: str = "gpt-3.5-turbo", **kwargs: Any,) -> LLMResponse:
        resp = self._client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )

        choice0 = resp.choices[0] if getattr(resp, "choices", None) else None
        message = getattr(choice0, "message", None)

        text = getattr(message, "content", "") or ""
        finish_reason = getattr(choice0, "finish_reason", None)

        usage_obj = getattr(resp, "usage", None)
        usage = None
        if usage_obj is not None:
            usage = TokenUsage(
                input_tokens=getattr(usage_obj, "prompt_tokens", None),
                output_tokens=getattr(usage_obj, "completion_tokens", None),
                total_tokens=getattr(usage_obj, "total_tokens", None),
            )

        tool_calls: list[dict[str, Any]] = []
        if message is not None and getattr(message, "tool_calls", None):
            for tc in message.tool_calls:
                fn = getattr(tc, "function", None)
                tool_calls.append(
                    {
                        "id": getattr(tc, "id", None),
                        "type": getattr(tc, "type", None),
                        "function": {
                            "name": getattr(fn, "name", None),
                            "arguments": getattr(fn, "arguments", None),
                        },
                    }
                )

        return LLMResponse(
            text=text,
            provider="openai",
            model=getattr(resp, "model", model),
            usage=usage,
            finish_reason=finish_reason,
            response_id=getattr(resp, "id", None),
            created=getattr(resp, "created", None),
            tool_calls=tuple(tool_calls),
            raw=resp,
        )

    def get_model_info(self) -> ModelInfo:  # type: ignore[override]
        return ModelInfo(
            name="openai",
            version="1.0",
            description="OpenAI chat completions",
            provider="openai",
        )

    def _extract_text_from_response(self, response) -> str:
        try:
            choices = getattr(response, "choices", None)
            if not choices:
                return ""

            message = getattr(choices[0], "message", None)
            if not message:
                return ""

            # Normal text
            if message.content:
                return message.content

            # Tool calls (future-proof)
            if hasattr(message, "tool_calls") and message.tool_calls:
                return ""

            return ""

        except Exception:
            return ""
