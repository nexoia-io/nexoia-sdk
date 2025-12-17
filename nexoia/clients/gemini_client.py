from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from google import genai

from .base import BaseLLMClient


@dataclass
class GeminiClient(BaseLLMClient):
    provider: str = "gemini"

    def _client(self):
        # Si tú manejas API keys centralizadas, reemplaza por tu helper.
        # Si no, el SDK lee GEMINI_API_KEY desde env.
        return genai.Client()

    def generate_text(self, prompt: str, model: str, **kwargs: Any) -> str:
        """
        Método requerido por BaseLLMClient.
        """
        client = self._client()
        resp = client.models.generate_content(model=model, contents=prompt, **kwargs)
        return getattr(resp, "text", "") or ""

    def get_model_info(self, model: str) -> Dict[str, Any]:
        """
        Método requerido por BaseLLMClient.
        Mantén esto declarativo (sin inventar números si no los tienes).
        """
        return {
            "provider": self.provider,
            "model": model,
            "supports_text": True,
            # Completa según tu esquema real de ModelInfo si existe
            "notes": "Gemini model metadata not retrieved from API; declarative info only.",
        }
