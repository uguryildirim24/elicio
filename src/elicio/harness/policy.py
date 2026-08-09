"""Command risks and confidence policy."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
from types import MappingProxyType
from typing import Mapping


class RiskLevel(IntEnum):
    NONE = 0
    REVERSIBLE = 1
    DANGEROUS = 2


class DecisionStatus(str, Enum):
    APPROVED = "approved"
    CONFIRMATION_REQUIRED = "confirmation_required"
    IGNORED = "ignored"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class Command:
    name: str
    adapter: str
    risk: RiskLevel

    def to_dict(self) -> dict[str, str | int]:
        return {
            "name": self.name,
            "adapter": self.adapter,
            "risk": int(self.risk),
        }


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    status: DecisionStatus
    reason: str
    command: Command | None = None
    confirmed: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status.value,
            "reason": self.reason,
            "command": self.command.to_dict() if self.command else None,
            "confirmed": self.confirmed,
        }


REST_SYMBOL = "rest"
CONFIRM_SYMBOL = "jaw_clench"
CONFIRM_WINDOW_S = 3.0
CONFIRM_CONFIDENCE_FLOOR = 0.85

CONFIDENCE_FLOORS: Mapping[RiskLevel, float] = MappingProxyType(
    {
        RiskLevel.NONE: 0.60,
        RiskLevel.REVERSIBLE: 0.75,
        RiskLevel.DANGEROUS: 0.85,
    }
)

# The original simulated alphabet is retained. wrist_down is the one
# engineering-slice action that now has a real, harmless local adapter.
DEFAULT_COMMANDS: Mapping[str, Command] = MappingProxyType(
    {
        "wrist_up": Command("scroll up", "console", RiskLevel.NONE),
        "wrist_down": Command(
            "record a local demonstration marker",
            "local_marker",
            RiskLevel.NONE,
        ),
        "index_pinch": Command(
            "accept the AI suggestion",
            "console",
            RiskLevel.REVERSIBLE,
        ),
        "middle_pinch": Command(
            "reject the AI suggestion",
            "console",
            RiskLevel.REVERSIBLE,
        ),
        "fist": Command("run the tests", "console", RiskLevel.DANGEROUS),
        "hand_open": Command("send the message", "console", RiskLevel.DANGEROUS),
    }
)
