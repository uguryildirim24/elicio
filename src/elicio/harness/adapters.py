"""Explicit action adapters used after a policy decision."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import tempfile
from typing import Mapping, Protocol

from .events import GestureEvent
from .policy import Command


@dataclass(frozen=True, slots=True)
class ActionResult:
    success: bool
    adapter: str
    details: Mapping[str, object] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "status": "completed" if self.success else "failed",
            "success": self.success,
            "adapter": self.adapter,
            "details": dict(self.details),
            "error": self.error,
        }


class ActionAdapter(Protocol):
    name: str

    def execute(self, command: Command, event: GestureEvent) -> ActionResult:
        ...


class AdapterRouter:
    """Routes only to adapters that were explicitly registered."""

    def __init__(self, adapters: Mapping[str, ActionAdapter]) -> None:
        self._adapters = dict(adapters)

    def execute(self, command: Command, event: GestureEvent) -> ActionResult:
        adapter = self._adapters.get(command.adapter)
        if adapter is None:
            return ActionResult(
                success=False,
                adapter=command.adapter,
                error=f"adapter {command.adapter!r} is not registered",
            )
        try:
            return adapter.execute(command, event)
        except Exception as exc:
            return ActionResult(
                success=False,
                adapter=adapter.name,
                error=f"{type(exc).__name__}: {exc}",
            )


class ConsoleAdapter:
    """Retains the remaining milestone-0 actions as explicit simulations."""

    name = "console"

    def execute(self, command: Command, event: GestureEvent) -> ActionResult:
        print(f"[simulated] {command.name}")
        return ActionResult(
            success=True,
            adapter=self.name,
            details={"simulated": True, "command": command.name},
        )


class LocalMarkerAdapter:
    """Atomically writes one fixed marker file.

    The event cannot choose the path or arbitrary content. The caller must
    configure the path when constructing the adapter.
    """

    name = "local_marker"

    def __init__(self, marker_path: Path) -> None:
        self.marker_path = Path(marker_path)

    def execute(self, command: Command, event: GestureEvent) -> ActionResult:
        self.marker_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 1,
            "action": command.name,
            "event": event.to_dict(),
        }
        encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"

        descriptor, temporary_name = tempfile.mkstemp(
            dir=self.marker_path.parent,
            prefix=f".{self.marker_path.name}.",
            suffix=".tmp",
        )
        temporary_path = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_path, self.marker_path)
        finally:
            temporary_path.unlink(missing_ok=True)

        return ActionResult(
            success=True,
            adapter=self.name,
            details={"path": str(self.marker_path.resolve()), "bytes_written": len(encoded)},
        )
