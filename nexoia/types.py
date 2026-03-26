from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class TokenUsage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    raw: dict[str, Any] | None = None


@dataclass(slots=True, frozen=True)
class LLMResponse:
    text: str
    provider: str
    model: str

    usage: TokenUsage | None = None
    finish_reason: str | None = None
    response_id: str | None = None
    created: int | None = None

    content_blocks: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    tool_calls: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    raw: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return self.text