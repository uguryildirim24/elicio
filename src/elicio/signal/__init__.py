"""Deterministic, device-neutral signal replay and contraction detection."""

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
    "build_noise_only_recording",
    "build_synthetic_recording",
    "noise_only_recording",
    "replay",
    "synthetic_recording",
]
