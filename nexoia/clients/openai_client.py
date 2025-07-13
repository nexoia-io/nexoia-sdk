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

from .base import BaseLLMClient, ModelInfo


class OpenAIClient(BaseLLMClient):
    """Thin wrapper delegating to :pypi:`openai` while matching BaseLLMClient."""

    ENV_API_KEY = "OPENAI_API_KEY"

    def _init_http(self) -> None:  # noqa: D401
        # openai SDK creates its own client internally; just cache an instance
        self._client = OpenAI(api_key=self.api_key, timeout=self.timeout)

    # ------------------------------- LLM methods ----------------------------

    def generate_text(self, prompt: str, *, model: str = "gpt-3.5-turbo", **kwargs: Any) -> str:  # type: ignore[override]
        chat = self._client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        return chat.choices[0].message.content  # type: ignore[attr-defined]

    def get_model_info(self) -> ModelInfo:  # type: ignore[override]
        return ModelInfo(
            name="openai",
            version="1.0",
            description="OpenAI chat completions",
            provider="openai",
        )