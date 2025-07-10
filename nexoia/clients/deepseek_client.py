
# -----------------------------------------------------------------------------
# nexoia/clients/deepseek_client.py
# -----------------------------------------------------------------------------
"""Concrete client for the DeepSeek API."""

from __future__ import annotations

import json
from typing import Any

import httpx

from .base import BaseLLMClient, ModelInfo
from ..exceptions import APIError

_DEEPSEEK_DEFAULT_ENDPOINT = "https://api.deepseek.com/v1"


class DeepSeekClient(BaseLLMClient):
    """Client to interact with DeepSeek LLM endpoints using httpx."""

    ENV_API_KEY = "DEEPSEEK_API_KEY"

    def __init__(
        self,
        api_key: str | None = None,
        *,
        endpoint: str = _DEEPSEEK_DEFAULT_ENDPOINT,
        timeout: float | int = 10,
    ):
        self.endpoint = endpoint.rstrip("/")
        super().__init__(api_key, timeout=timeout)

    # ---------------------------- HTTP initialisation -----------------------

    def _init_http(self) -> None:  # noqa: D401
        self._client = httpx.Client(timeout=self.timeout, headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    # ------------------------------- LLM methods ----------------------------

    def generate_text(self, prompt: str, *, max_tokens: int = 50, **kwargs: Any) -> str:  # type: ignore[override]
        payload = {"prompt": prompt, "max_tokens": max_tokens, **kwargs}
        url = f"{self.endpoint}/generate"
        response = self._client.post(url, json=payload)

        if response.status_code != 200:
            raise APIError(provider="deepseek", status=response.status_code, body=response.text)

        data = response.json()
        return data.get("generated_text", "")

    def get_model_info(self) -> ModelInfo:  # type: ignore[override]
        return ModelInfo(
            name="deepseek-llm",
            version="1.0",
            description="DeepSeek text‑generation model (simulated)",
            provider="deepseek",
        )

