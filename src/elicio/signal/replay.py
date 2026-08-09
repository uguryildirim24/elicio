"""Small deterministic recordings and a one-channel replay source.

The recordings are generated with only the Python standard library. They are
software fixtures for exercising the signal path, not sensor or hardware data.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
import math
import random


DEFAULT_SAMPLE_RATE_HZ = 100.0
DEFAULT_SYNTHETIC_SEED = 20260808


@dataclass(frozen=True, slots=True)
class Recording:
    """A finite, one-channel sequence of scalar samples."""

    samples: tuple[float, ...]
    sample_rate_hz: float = DEFAULT_SAMPLE_RATE_HZ
    start_timestamp: float = 0.0

    def __post_init__(self) -> None:
        values = tuple(float(sample) for sample in self.samples)
        if not values:
            raise ValueError("samples must contain at least one value")
        if not all(math.isfinite(sample) for sample in values):
            raise ValueError("samples must contain only finite values")

        sample_rate_hz = float(self.sample_rate_hz)
        if not math.isfinite(sample_rate_hz) or sample_rate_hz <= 0.0:
            raise ValueError("sample_rate_hz must be a positive finite number")

        start_timestamp = float(self.start_timestamp)
        if not math.isfinite(start_timestamp) or start_timestamp < 0.0:
            raise ValueError("start_timestamp must be a finite, non-negative number")

        object.__setattr__(self, "samples", values)
        object.__setattr__(self, "sample_rate_hz", sample_rate_hz)
        object.__setattr__(self, "start_timestamp", start_timestamp)

    @property
    def duration_seconds(self) -> float:
        """Return the elapsed sample time, excluding the final sample interval."""

        return (len(self.samples) - 1) / self.sample_rate_hz


class ReplaySource:
    """Replay one recording as ``(timestamp, sample)`` pairs."""

    def __init__(self, recording: Recording) -> None:
        if not isinstance(recording, Recording):
            raise TypeError("recording must be a Recording")
        self.recording = recording

    def __iter__(self) -> Iterator[tuple[float, float]]:
        return replay(self.recording)

    def replay(self) -> Iterator[tuple[float, float]]:
        """Return a fresh iterator, so a source can be replayed repeatedly."""

        return replay(self.recording)


def replay(recording: Recording) -> Iterator[tuple[float, float]]:
    """Yield deterministic timestamps and samples from ``recording``."""

    if not isinstance(recording, Recording):
        raise TypeError("recording must be a Recording")
    for index, sample in enumerate(recording.samples):
        yield recording.start_timestamp + index / recording.sample_rate_hz, sample


def build_synthetic_recording(
    *,
    sample_rate_hz: float = DEFAULT_SAMPLE_RATE_HZ,
    seed: int = DEFAULT_SYNTHETIC_SEED,
) -> Recording:
    """Build rest noise, one clear burst, and a final rest interval.

    The fixture has one second of rest, 0.6 seconds of elevated signal, and
    1.6 seconds of rest at the default sample rate. A local seeded generator
    keeps every replay independent of process-global random state.
    """

    sample_rate_hz = float(sample_rate_hz)
    if not math.isfinite(sample_rate_hz) or sample_rate_hz <= 0.0:
        raise ValueError("sample_rate_hz must be a positive finite number")
    rng = random.Random(seed)
    rest_before = int(round(sample_rate_hz * 1.0))
    burst_samples = int(round(sample_rate_hz * 0.6))
    rest_after = int(round(sample_rate_hz * 1.6))
    values: list[float] = []

    for _ in range(rest_before):
        values.append(rng.uniform(-0.025, 0.025))
    for index in range(burst_samples):
        phase = index / sample_rate_hz
        carrier = 0.75 + 0.08 * math.sin(2.0 * math.pi * 5.0 * phase)
        values.append(carrier + rng.uniform(-0.025, 0.025))
    for _ in range(rest_after):
        values.append(rng.uniform(-0.025, 0.025))

    return Recording(tuple(values), sample_rate_hz=sample_rate_hz)


def build_noise_only_recording(
    *,
    duration_seconds: float = 3.2,
    sample_rate_hz: float = DEFAULT_SAMPLE_RATE_HZ,
    seed: int = DEFAULT_SYNTHETIC_SEED,
    amplitude: float = 0.025,
) -> Recording:
    """Build a deterministic recording containing rest-level noise only."""

    duration_seconds = float(duration_seconds)
    sample_rate_hz = float(sample_rate_hz)
    amplitude = float(amplitude)
    if not math.isfinite(duration_seconds) or duration_seconds <= 0.0:
        raise ValueError("duration_seconds must be a positive finite number")
    if not math.isfinite(sample_rate_hz) or sample_rate_hz <= 0.0:
        raise ValueError("sample_rate_hz must be a positive finite number")
    if not math.isfinite(amplitude) or amplitude < 0.0:
        raise ValueError("amplitude must be a finite, non-negative number")

    sample_count = max(1, int(round(duration_seconds * sample_rate_hz)))
    rng = random.Random(seed)
    values = tuple(rng.uniform(-amplitude, amplitude) for _ in range(sample_count))
    return Recording(values, sample_rate_hz=sample_rate_hz)


# Short names keep call sites readable while the build_* names remain explicit.
synthetic_recording = build_synthetic_recording
noise_only_recording = build_noise_only_recording
