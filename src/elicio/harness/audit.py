"""Append-only JSONL audit sinks."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Mapping, Protocol


class AuditSink(Protocol):
    def record(self, entry: Mapping[str, object]) -> None:
        ...


class JsonlAuditLog:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def record(self, entry: Mapping[str, object]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(dict(entry), separators=(",", ":"), sort_keys=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            handle.flush()
            os.fsync(handle.fileno())


class MemoryAuditLog:
    def __init__(self) -> None:
        self.entries: list[dict[str, object]] = []

    def record(self, entry: Mapping[str, object]) -> None:
        self.entries.append(dict(entry))
