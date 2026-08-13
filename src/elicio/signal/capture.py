"""Capture live one-channel sample streams into replayable recordings.

This module bridges a real sensor stream (a serial device, a file, or
stdin) into the same ``Recording`` form the synthetic fixtures use, so a
captured personal session replays deterministically through
``ContractionDetector`` and the harness. It also provides a small
trailing-envelope meter for terminal biofeedback while training a
muscle channel.

Standard library only, like the rest of the signal package. Timestamps
are synthesized from the declared sample rate, not read from the wall
clock, so a saved capture replays identically every time. The capture
wall-clock time belongs in the saved file's ``meta`` block, not in the
signal itself.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Iterator
import json
import math
import os
from pathlib import Path
import tempfile
from typing import Mapping

from .replay import DEFAULT_SAMPLE_RATE_HZ, Recording

RECORDING_SCHEMA_VERSION = 1
RECORDING_KIND = "elicio_recording"


def parse_sample_line(line: str) -> float | None:
    """Parse one stream line into a raw sample value.

    A stream carries one ASCII number per line. Blank lines and lines
    starting with ``#`` are annotations and return ``None``. Anything
    else that does not parse as a finite number raises ``ValueError``,
    so a mis-wired stream fails loudly instead of producing garbage.
    """

    text = line.strip()
    if not text or text.startswith("#"):
        return None
    value = float(text)
    if not math.isfinite(value):
        raise ValueError(f"sample must be finite, got {text!r}")
    return value


def _validate_transform(offset: float, gain: float) -> tuple[float, float]:
    offset = float(offset)
    gain = float(gain)
    if not math.isfinite(offset):
        raise ValueError("offset must be a finite number")
    if not math.isfinite(gain) or gain <= 0.0:
        raise ValueError("gain must be a positive finite number")
    return offset, gain


def collect_samples(
    lines: Iterable[str],
    *,
    offset: float = 0.0,
    gain: float = 1.0,
    max_samples: int | None = None,
) -> list[float]:
    """Read lines and return transformed samples ``(raw - offset) * gain``.

    ``offset`` recenters an ADC stream (for example 2048 counts for a
    mid-rail-biased 12-bit converter) and ``gain`` rescales it so a firm
    contraction lands near the detector's working range. Collection
    stops after ``max_samples`` values or at the end of the stream.
    """

    offset, gain = _validate_transform(offset, gain)
    if max_samples is not None:
        if not isinstance(max_samples, int) or isinstance(max_samples, bool):
            raise TypeError("max_samples must be an integer")
        if max_samples <= 0:
            raise ValueError("max_samples must be positive")

    samples: list[float] = []
    for line in lines:
        value = parse_sample_line(line)
        if value is None:
            continue
        samples.append((value - offset) * gain)
        if max_samples is not None and len(samples) >= max_samples:
            break
    return samples


def stream_samples(
    lines: Iterable[str],
    *,
    sample_rate_hz: float = DEFAULT_SAMPLE_RATE_HZ,
    start_timestamp: float = 0.0,
    offset: float = 0.0,
    gain: float = 1.0,
) -> Iterator[tuple[float, float]]:
    """Yield ``(timestamp, sample)`` pairs from a live line stream.

    Timestamps are synthesized from the declared sample rate so the
    stream matches what ``replay`` produces for a saved recording.
    """

    sample_rate_hz = float(sample_rate_hz)
    if not math.isfinite(sample_rate_hz) or sample_rate_hz <= 0.0:
        raise ValueError("sample_rate_hz must be a positive finite number")
    start_timestamp = float(start_timestamp)
    if not math.isfinite(start_timestamp) or start_timestamp < 0.0:
        raise ValueError("start_timestamp must be a finite, non-negative number")
    offset, gain = _validate_transform(offset, gain)

    index = 0
    for line in lines:
        value = parse_sample_line(line)
        if value is None:
            continue
        yield start_timestamp + index / sample_rate_hz, (value - offset) * gain
        index += 1


def save_recording(
    recording: Recording,
    path: Path,
    *,
    meta: Mapping[str, object] | None = None,
) -> Path:
    """Atomically write one recording as a JSON file and return its path.

    The signal itself stays deterministic; free-form provenance (capture
    wall-clock time, electrode site, notes) belongs in ``meta``. The raw
    samples in the file are the permanent source record for a capture.
    """

    if not isinstance(recording, Recording):
        raise TypeError("recording must be a Recording")
    path = Path(path)
    payload = {
        "schema_version": RECORDING_SCHEMA_VERSION,
        "kind": RECORDING_KIND,
        "sample_rate_hz": recording.sample_rate_hz,
        "start_timestamp": recording.start_timestamp,
        "samples": list(recording.samples),
        "meta": dict(meta) if meta else {},
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)
    return path


def load_recording(path: Path) -> Recording:
    """Load a recording saved by ``save_recording``.

    Structural problems raise ``ValueError``; sample validation is
    delegated to the ``Recording`` constructor.
    """

    path = Path(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path} does not contain a recording object")
    if payload.get("kind") != RECORDING_KIND:
        raise ValueError(f"{path} is not an {RECORDING_KIND} file")
    if payload.get("schema_version") != RECORDING_SCHEMA_VERSION:
        raise ValueError(
            f"{path} has unsupported schema_version "
            f"{payload.get('schema_version')!r}"
        )
    samples = payload.get("samples")
    if not isinstance(samples, list):
        raise ValueError(f"{path} has no samples list")
    return Recording(
        tuple(samples),
        sample_rate_hz=payload.get("sample_rate_hz", DEFAULT_SAMPLE_RATE_HZ),
        start_timestamp=payload.get("start_timestamp", 0.0),
    )


def load_recording_meta(path: Path) -> dict[str, object]:
    """Return the free-form ``meta`` block of a saved recording."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("kind") != RECORDING_KIND:
        raise ValueError(f"{path} is not an {RECORDING_KIND} file")
    meta = payload.get("meta", {})
    return dict(meta) if isinstance(meta, dict) else {}


class TrailingEnvelope:
    """Trailing mean of absolute sample values.

    Matches the envelope the detector computes internally, so the meter
    a person trains against shows the same quantity the detector
    thresholds.
    """

    def __init__(self, window: int = 8) -> None:
        if not isinstance(window, int) or isinstance(window, bool):
            raise TypeError("window must be an integer")
        if window <= 0:
            raise ValueError("window must be positive")
        self.window = window
        self._values: deque[float] = deque(maxlen=window)
        self._total = 0.0

    def update(self, sample: float) -> float:
        sample = float(sample)
        if not math.isfinite(sample):
            raise ValueError("sample must be finite")
        magnitude = abs(sample)
        if len(self._values) == self.window:
            self._total -= self._values[0]
        self._values.append(magnitude)
        self._total += magnitude
        return self._total / len(self._values)


def render_meter(
    envelope: float,
    threshold: float,
    *,
    width: int = 40,
    peak: float = 1.0,
) -> str:
    """Render one text meter line with a threshold marker.

    ``peak`` is the envelope value that fills the whole bar. The
    threshold marker shows where the detector's onset threshold sits, so
    a person can see how far a contraction is from registering.
    """

    envelope = float(envelope)
    threshold = float(threshold)
    if not math.isfinite(envelope) or envelope < 0.0:
        raise ValueError("envelope must be a finite, non-negative number")
    if not math.isfinite(threshold) or threshold < 0.0:
        raise ValueError("threshold must be a finite, non-negative number")
    if not isinstance(width, int) or isinstance(width, bool):
        raise TypeError("width must be an integer")
    if width <= 0:
        raise ValueError("width must be positive")
    peak = float(peak)
    if not math.isfinite(peak) or peak <= 0.0:
        raise ValueError("peak must be a positive finite number")

    filled = min(1.0, envelope / peak)
    cells = int(round(filled * width))
    bar = ["#" if index < cells else "-" for index in range(width)]
    marker = min(width - 1, int(round(min(1.0, threshold / peak) * width)))
    bar[marker] = "|"
    return f"[{''.join(bar)}] env={envelope:.3f} thr={threshold:.2f}"
