# -----------------------------------------------------------------------------
# nexoia/clients/deepseek_client.py
# -----------------------------------------------------------------------------
"""Concrete client for the DeepSeek API."""

from __future__ import annotations

from typing import Any

import httpx

from ..exceptions import APIError
from .base import BaseLLMClient, ModelInfo

_DEEPSEEK_DEFAULT_ENDPOINT = "https://api.deepseek.com/v1"


class DeepSeekClient(BaseLLMClient):
    """Client to interact with DeepSeek LLM endpoints using httpx."""

    PROVIDER_SLUG = "deepseek"
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
        self._client = httpx.Client(
            timeout=self.timeout,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

    def close(self) -> None:
        if getattr(self, "_client", None) is not None:
            self._client.close()

    # ------------------------------- LLM methods ----------------------------

    def generate_text(
        self,
        prompt: str,
        *,
        model: str = "deepseek-chat",
        max_tokens: int = 50,
        **kwargs: Any,
    ) -> str:  # type: ignore[override]
        payload: dict[str, Any] = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            **kwargs,
        }

        url = f"{self.endpoint}/chat/completions"

        try:
            response = self._client.post(url, json=payload)

            # Prefer raise_for_status() when available (real httpx.Response),
            # but keep compatibility with minimal fakes in tests.
            rf = getattr(response, "raise_for_status", None)
            if callable(rf):
                try:
                    rf()
                except httpx.HTTPStatusError as exc:
                    raise APIError(
                        provider="deepseek",
                        status=exc.response.status_code,
                        body=exc.response.text,
                    ) from exc
            else:
                if response.status_code != 200:
                    raise APIError(
                        provider="deepseek",
                        status=response.status_code,
                        body=response.text,
                    )

            data = response.json()

        except httpx.HTTPError as exc:
            # Transport-level error (DNS, timeout, connection reset, etc.)
            raise APIError(
                provider="deepseek",
                status=0,
                body=str(exc),
            ) from exc
        except ValueError as exc:
            # JSON decode error
            raise APIError(
                provider="deepseek",
                status=getattr(response, "status_code", 0),
                body=getattr(response, "text", "")[:1000],
            ) from exc

        return self._extract_text_from_response(data)

    def _extract_text_from_response(self, data: dict[str, Any]) -> str:
        """
        Defensive extraction for OpenAI-like responses:
          {"choices":[{"message":{"content":"..."}}]}
        """
        try:
            choices = data.get("choices")
            if not isinstance(choices, list) or not choices:
                return ""

            first = choices[0]
            if not isinstance(first, dict):
                return ""

            message = first.get("message")
            if isinstance(message, dict):
                content: str | None = message.get("content")
                if isinstance(content, str):
                    return content or ""

                # Future-proof: tool_calls without content
                tool_calls = message.get("tool_calls")
                if tool_calls:
                    return ""

                return ""

            # Fallback: sometimes text may appear at choice level
            text = first.get("text")
            if isinstance(text, str):
                return text or ""

            return ""
        except Exception:
            return ""

    def get_model_info(self) -> ModelInfo:  # type: ignore[override]
        return ModelInfo(
            name="deepseek-llm",
            version="1.0",
            description="DeepSeek chat completions (OpenAI-compatible response shape)",
            provider="deepseek",
        )
