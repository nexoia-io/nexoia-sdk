from __future__ import annotations

from typing import Any

from google import genai

from .base import BaseLLMClient, ModelInfo


class GeminiClient(BaseLLMClient):
    """
    Google Gemini client using the official google-genai SDK.
    """

    ENV_API_KEY = "GEMINI_API_KEY"
    PROVIDER_SLUG = "gemini"

    def _init_http(self) -> None:
        # The SDK manages endpoints internally.
        self._client = genai.Client(api_key=self.api_key)

    def generate_text(self, prompt: str, model: str = "gemini-2.5-flash", **kwargs: Any) -> str:
        """
        Generate text using a Gemini model.
        """
        response = self._client.models.generate_content(
            model=model,
            contents=prompt,
            **kwargs,
        )
        return getattr(response, "text", "") or ""

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
