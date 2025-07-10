# -----------------------------------------------------------------------------
# nexoia/exceptions.py
# -----------------------------------------------------------------------------
from __future__ import annotations


class APIError(RuntimeError):
    """Raised when a provider returns a non‑OK HTTP status."""

    def __init__(self, *, provider: str, status: int, body: str | None = None):
        super().__init__(f"{provider} API error: HTTP {status}\n{body or ''}")
        self.provider = provider
        self.status = status
        self.body = body
