"""Base abstract client for Large Language Model providers.

Every concrete provider (OpenAI, DeepSeek, etc.) must inherit from
:class:`BaseLLMClient` and implement :py:meth:`generate_text` and
:py:meth:`get_model_info`.

This base class also handles common concerns such as:

* API-key retrieval (from argument, environment variable or YAML config)
* Default timeout configuration for HTTP requests
* Basic representation helpers
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping

from ..config import get_api_key


@dataclass(slots=True, frozen=True)
class ModelInfo:
    """Container for model metadata returned by each client."""

    name: str
    version: str
    description: str
    provider: str


class BaseLLMClient(ABC):
    """Abstract base class to unify the public surface of all LLM providers."""

    #: Environment variable expected by default.  Concrete subclasses SHOULD
    #: override this to match their own conventional variable name.
    ENV_API_KEY: str | None = None

    def __init__(self, api_key: str | None = None, *, timeout: float | int = 10):
        self.api_key: str = (
            api_key
            or get_api_key(self.__class__.__name__.lower())
            or (os.getenv(self.ENV_API_KEY) if self.ENV_API_KEY else None)
        )
        if not self.api_key:
            raise ValueError(
                f"API key not provided and not found in config for {self.__class__.__name__}."
            )

        self.timeout: float = float(timeout)
        self._init_http()  # allow subclasses to prepare HTTP client

    # ------------------------------------------------------------------
    # Public interface expected by downstream code (sync only for v0.1)
    # ------------------------------------------------------------------

    @abstractmethod
    def generate_text(self, prompt: str, **kwargs: Any) -> str:
        """Generate a text completion for *prompt*.

        Subclasses must make the appropriate HTTP call and return the resulting
        string or raise :class:`nexoia.exceptions.APIError`.
        """

    @abstractmethod
    def get_model_info(self) -> ModelInfo:
        """Return metadata describing the underlying model implementation."""

    # ------------------------------------------------------------------
    # Optional extension points
    # ------------------------------------------------------------------

    def _init_http(self) -> None:  # noqa: D401 (imperative mood)
        """Hook for subclasses to initialise persistent HTTP clients."""
        # By default we do nothing; subclasses can override and create an
        # httpx.AsyncClient or similar.
        return

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover
        meta = self.get_model_info()
        return (
            f"<{self.__class__.__name__} {meta.name} v{meta.version} timeout={self.timeout}s>"
        )

