"""Deterministic simulated decoder events from milestone 0."""

from __future__ import annotations

from collections.abc import Iterable

from .events import GestureEvent


DEMO_SCRIPT: tuple[tuple[str, float, float], ...] = (
    ("wrist_down", 0.92, 0.0),
    ("wrist_down", 0.55, 0.6),
    ("index_pinch", 0.88, 1.2),
    ("fist", 0.91, 2.0),
    ("jaw_clench", 0.90, 3.1),
    ("hand_open", 0.93, 5.0),
    ("wrist_up", 0.90, 5.5),
    ("jaw_clench", 0.88, 9.0),
    ("rest", 0.99, 9.5),
)

REAL_ACTION_DEMO: tuple[tuple[str, float, float], ...] = (
    ("wrist_down", 0.92, 0.0),
)


def events_from_script(
    script: Iterable[tuple[str, float, float]],
    *,
    start_timestamp: float,
) -> list[GestureEvent]:
    return [
        GestureEvent(symbol, confidence, start_timestamp + offset)
        for symbol, confidence, offset in script
    ]
