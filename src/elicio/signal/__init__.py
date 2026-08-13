"""Deterministic, device-neutral signal replay, capture, and detection."""

from .capture import (
    TrailingEnvelope,
    collect_samples,
    load_recording,
    load_recording_meta,
    parse_sample_line,
    render_meter,
    save_recording,
    stream_samples,
)
from .detector import ContractionDetector
from .replay import (
    DEFAULT_SAMPLE_RATE_HZ,
    Recording,
    ReplaySource,
    build_noise_only_recording,
    build_synthetic_recording,
    noise_only_recording,
    replay,
    synthetic_recording,
)

__all__ = [
    "ContractionDetector",
    "DEFAULT_SAMPLE_RATE_HZ",
    "Recording",
    "ReplaySource",
    "TrailingEnvelope",
    "build_noise_only_recording",
    "build_synthetic_recording",
    "collect_samples",
    "load_recording",
    "load_recording_meta",
    "noise_only_recording",
    "parse_sample_line",
    "render_meter",
    "replay",
    "save_recording",
    "stream_samples",
    "synthetic_recording",
]
