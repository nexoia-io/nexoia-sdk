from __future__ import annotations

from typing import Any

from google import genai

from .base import BaseLLMClient, ModelInfo
from ..types import LLMResponse, TokenUsage

class GeminiClient(BaseLLMClient):
    """
    Google Gemini client using the official google-genai SDK.
    """

    ENV_API_KEY = "GEMINI_API_KEY"
    PROVIDER_SLUG = "gemini"

    def _init_http(self) -> None:
        # The SDK manages endpoints internally.
        self._client = genai.Client(api_key=self.api_key)

    def generate(self, prompt: str, *, model: str = "gemini-2.5-flash", **kwargs: Any,) -> LLMResponse:
        response = self._client.models.generate_content(
            model=model,
            contents=prompt,
            **kwargs,
        )

        text = getattr(response, "text", "") or ""

        usage = None
        usage_meta = getattr(response, "usage_metadata", None)
        if usage_meta is not None:
            usage = TokenUsage(
                input_tokens=getattr(usage_meta, "prompt_token_count", None),
                output_tokens=getattr(usage_meta, "candidates_token_count", None),
                total_tokens=getattr(usage_meta, "total_token_count", None),
                raw={
                    "prompt_token_count": getattr(usage_meta, "prompt_token_count", None),
                    "candidates_token_count": getattr(usage_meta, "candidates_token_count", None),
                    "total_token_count": getattr(usage_meta, "total_token_count", None),
                },
            )

        return LLMResponse(
            text=text,
            provider="gemini",
            model=model,
            usage=usage,
            finish_reason=None,
            response_id=getattr(response, "response_id", None),
            created=None,
            content_blocks=tuple(),
            tool_calls=tuple(),
            raw=response,
        )

    def get_model_info(self) -> ModelInfo:
        """
        Declarative provider metadata.
        """
        return ModelInfo(
            name="google-gemini",
            version="v1",
            description="Google Gemini text-generation models via official SDK",
            provider="gemini",
        )
