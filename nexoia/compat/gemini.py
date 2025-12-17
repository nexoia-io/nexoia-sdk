# nexoia/compat/gemini.py
from ..registry import register_provider  # ajusta al nombre real
from ..clients.gemini_client import GeminiClient

register_provider(
    name="gemini",
    client_cls=GeminiClient,
    # si tu registry guarda metadata:
    env_key="GEMINI_API_KEY",
    default_base_url=None,
)
