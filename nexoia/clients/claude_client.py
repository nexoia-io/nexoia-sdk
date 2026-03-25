# -----------------------------------------------------------------------------
# nexoia/clients/claude_client.py
# -----------------------------------------------------------------------------
"""Cliente para la API de Claude (Anthropic) compatible con BaseLLMClient."""

from __future__ import annotations

from typing import Any

import httpx

from ..exceptions import APIError
from .base import BaseLLMClient, ModelInfo

_ANTHROPIC_DEFAULT_ENDPOINT = "https://api.anthropic.com"


class ClaudeClient(BaseLLMClient):
    """Client para la API de Claude usando httpx."""

    # Provider slug should match config keys / registry keys (stable, vendor-level)
    PROVIDER_SLUG = "anthropic"
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

    def _init_http(self) -> None:  # noqa: D401
        self._client = httpx.Client(
            timeout=self.timeout,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )

    def close(self) -> None:
        if getattr(self, "_client", None) is not None:
            self._client.close()

    def generate_text(
        self,
        prompt: str,
        *,
        model: str = "claude-sonnet-4-6",
        max_tokens: int = 512,
        **kwargs: Any,
    ) -> str:  # type: ignore[override]
        payload: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
            **kwargs,
        }

        url = f"{self.endpoint}/v1/messages"

        try:
            response = self._client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as exc:
            # HTTP error with response body
            raise APIError(
                provider="anthropic",
                status=exc.response.status_code,
                body=exc.response.text,
            ) from exc
        except httpx.HTTPError as exc:
            # Network / transport error (no status code)
            raise APIError(
                provider="anthropic",
                status=0,
                body=str(exc),
            ) from exc
        except ValueError as exc:
            # JSON decode error
            raise APIError(
                provider="anthropic",
                status=getattr(response, "status_code", 0),
                body=getattr(response, "text", "")[:1000],
            ) from exc

        return self._extract_text_from_response(data)

    def _extract_text_from_response(self, data: dict[str, Any]) -> str:
        """
        Anthropic Messages API:
          "content": [{"type":"text","text":"..."}, {"type":"tool_use",...}, ...]

        We concatenate all text blocks and ignore non-text blocks for now.
        """
        content = data.get("content", [])
        if not isinstance(content, list) or not content:
            return ""

        texts: list[str] = []
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text":
                t = block.get("text")
                if isinstance(t, str) and t:
                    texts.append(t)

        return "\n".join(texts).strip()

    def get_model_info(self) -> ModelInfo:  # type: ignore[override]
        return ModelInfo(
            name="claude",
            version="1.0",
            description="Anthropic Claude via Messages API",
            provider="anthropic",
        )
