"""The stable decoder-to-harness event contract."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True, slots=True)
class GestureEvent:
    """One decoder decision: (symbol, confidence, timestamp)."""

    symbol: str
    confidence: float
    timestamp: float

    def __post_init__(self) -> None:
        if not isinstance(self.symbol, str) or not self.symbol.strip():
            raise ValueError("symbol must be a non-empty string")
        if self.symbol != self.symbol.strip():
            raise ValueError("symbol must not have leading or trailing whitespace")

        confidence = float(self.confidence)
        if not math.isfinite(confidence) or not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be a finite number from 0.0 to 1.0")

        timestamp = float(self.timestamp)
        if not math.isfinite(timestamp) or timestamp < 0.0:
            raise ValueError("timestamp must be a finite, non-negative number")

        object.__setattr__(self, "confidence", confidence)
        object.__setattr__(self, "timestamp", timestamp)

    def as_tuple(self) -> tuple[str, float, float]:
        return self.symbol, self.confidence, self.timestamp

    def to_dict(self) -> dict[str, str | float]:
        return {
            "symbol": self.symbol,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
        }
