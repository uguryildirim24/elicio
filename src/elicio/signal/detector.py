"""A deterministic contraction detector for one-channel sample streams."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable
import math

from elicio.harness.events import GestureEvent


class ContractionDetector:
    """Detect sustained envelope crossings and emit stable gesture events.

    Each input item is a ``(timestamp, sample)`` pair. The envelope is the
    trailing mean of the absolute sample value over ``envelope_window``
    samples. An event is emitted once a crossing remains above the threshold
    for the configured minimum duration. A refractory interval suppresses
    immediate re-triggers until the active contraction has ended.
    """

    def __init__(
        self,
        *,
        sample_rate_hz: float = 100.0,
        envelope_window: int = 8,
        onset_threshold: float = 0.20,
        min_contraction_duration: float = 0.12,
        refractory_period: float = 0.50,
        confidence_scale: float = 1.0,
    ) -> None:
        sample_rate_hz = float(sample_rate_hz)
        onset_threshold = float(onset_threshold)
        min_contraction_duration = float(min_contraction_duration)
        refractory_period = float(refractory_period)
        confidence_scale = float(confidence_scale)
        if not math.isfinite(sample_rate_hz) or sample_rate_hz <= 0.0:
            raise ValueError("sample_rate_hz must be a positive finite number")
        if not isinstance(envelope_window, int) or isinstance(envelope_window, bool):
            raise TypeError("envelope_window must be an integer")
        if envelope_window <= 0:
            raise ValueError("envelope_window must be positive")
        if not math.isfinite(onset_threshold) or onset_threshold < 0.0:
            raise ValueError("onset_threshold must be a finite, non-negative number")
        if (
            not math.isfinite(min_contraction_duration)
            or min_contraction_duration < 0.0
        ):
            raise ValueError(
                "min_contraction_duration must be a finite, non-negative number"
            )
        if not math.isfinite(refractory_period) or refractory_period < 0.0:
            raise ValueError("refractory_period must be a finite, non-negative number")
        if not math.isfinite(confidence_scale) or confidence_scale <= 0.0:
            raise ValueError("confidence_scale must be a positive finite number")

        self.sample_rate_hz = sample_rate_hz
        self.envelope_window = envelope_window
        self.onset_threshold = onset_threshold
        self.min_contraction_duration = min_contraction_duration
        self.refractory_period = refractory_period
        self.confidence_scale = confidence_scale
        self._window: deque[float] = deque(maxlen=envelope_window)
        self._window_sum = 0.0
        self._above_since: float | None = None
        self._active = False
        self._suppressed = False
        self._refractory_until = 0.0
        self._last_timestamp: float | None = None

    def reset(self) -> None:
        """Clear streaming state before replaying a recording."""

        self._window.clear()
        self._window_sum = 0.0
        self._above_since = None
        self._active = False
        self._suppressed = False
        self._refractory_until = 0.0
        self._last_timestamp = None

    def process_sample(self, timestamp: float, sample: float) -> GestureEvent | None:
        """Consume one pair and return an event only when one is detected."""

        timestamp = float(timestamp)
        sample = float(sample)
        if not math.isfinite(timestamp) or timestamp < 0.0:
            raise ValueError("timestamp must be a finite, non-negative number")
        if not math.isfinite(sample):
            raise ValueError("sample must be finite")
        if self._last_timestamp is not None and timestamp < self._last_timestamp:
            raise ValueError("timestamps must be non-decreasing")
        self._last_timestamp = timestamp

        magnitude = abs(sample)
        if len(self._window) == self.envelope_window:
            self._window_sum -= self._window[0]
        self._window.append(magnitude)
        self._window_sum += magnitude
        envelope = self._window_sum / len(self._window)

        if envelope < self.onset_threshold:
            self._above_since = None
            self._active = False
            self._suppressed = False
            return None

        if self._above_since is None:
            self._above_since = timestamp
            self._suppressed = timestamp < self._refractory_until
        if self._active or self._suppressed:
            return None
        if timestamp - self._above_since < self.min_contraction_duration:
            return None

        self._active = True
        self._refractory_until = timestamp + self.refractory_period
        confidence = min(1.0, max(0.0, envelope / self.confidence_scale))
        return GestureEvent("wrist_down", confidence, self._above_since)

    def detect(
        self, samples: Iterable[tuple[float, float]]
    ) -> list[GestureEvent]:
        """Detect events from a fresh replay, resetting prior stream state."""

        self.reset()
        events: list[GestureEvent] = []
        for timestamp, sample in samples:
            event = self.process_sample(timestamp, sample)
            if event is not None:
                events.append(event)
        return events
