# -----------------------------------------------------------------------------
# nexoia/clients/claude_client.py
# -----------------------------------------------------------------------------
"""Cliente para la API de Claude (Anthropic) compatible con BaseLLMClient."""

from __future__ import annotations

from typing import Any

import httpx

from .base import BaseLLMClient, ModelInfo
from ..exceptions import APIError

_ANTHROPIC_DEFAULT_ENDPOINT = "https://api.anthropic.com"


class ClaudeClient(BaseLLMClient):
    """Client para la API de Claude usando httpx."""

    # Nombre estándar de la variable de entorno de Anthropic
    ENV_API_KEY = "ANTHROPIC_API_KEY"

    def __init__(
        self,
        api_key: str | None = None,
        *,
        endpoint: str = _ANTHROPIC_DEFAULT_ENDPOINT,
        timeout: float | int = 10,
    ):
        self.endpoint = endpoint.rstrip("/")
        super().__init__(api_key, timeout=timeout)

    # ---------------------------- HTTP init ---------------------------------
    def _init_http(self) -> None:  # noqa: D401
        # Cliente HTTP persistente
        self._client = httpx.Client(
            timeout=self.timeout,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )

    # ----------------------------- LLM methods ------------------------------
    def generate_text(
        self,
        prompt: str,
        *,
        model: str = "claude-sonnet-4-5",
        max_tokens: int = 512,
        **kwargs: Any,
    ) -> str:  # type: ignore[override]
        """Genera texto usando el endpoint /v1/messages de Anthropic."""
        payload: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "user", "content": prompt},
            ],
            **kwargs,
        }

        url = f"{self.endpoint}/v1/messages"
        response = self._client.post(url, json=payload)

        if response.status_code != 200:
            raise APIError(
                provider="claude",
                status=response.status_code,
                body=response.text,
            )

        data = response.json()

        # Respuesta típica de Claude:
        # {
        #   "id": "...",
        #   "type": "message",
        #   "role": "assistant",
        #   "content": [{"type": "text", "text": "..."}],
        #   ...
        # }
        content = data.get("content", [])
        if not content:
            return ""

        # Tomamos el primer bloque de texto
        first = content[0]
        if isinstance(first, dict) and first.get("type") == "text":
            return first.get("text", "")

        # Fallback genérico
        return str(first)

    def get_model_info(self) -> ModelInfo:  # type: ignore[override]
        return ModelInfo(
            name="claude",
            version="1.0",
            description="Anthropic Claude via Messages API",
            provider="anthropic",
        )
