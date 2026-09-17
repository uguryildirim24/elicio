#!/usr/bin/env python3.13
"""Manifest schema 1 validator (plan §10 open item 3).

``schema: 1`` is a JSON object. Required keys and types:

schema (int)
    Must be 1.
hash_rule (str)
    Non-empty. Promises SHA-256 of raw file bytes for every name in
    ``files``. For this generator it also records the STEP timestamp pin
    (2026-09-16T00:00:00Z), STL/3MF mesh (0.02 mm chord, 5 deg), 3MF
    UUID5 ``elicio:cad:v1:<part>``, remaining UUID rewrite, and zip date
    2026-09-16.
commit (str)
    Last git commit that changed a hashed solid under
    ``docs/fab/cad/v1`` (``*.step``, ``*.stl``, ``*.3mf``). It is not
    HEAD of the repository. Artwork in ``views`` does not move it.
    Forty lowercase hex characters, or ``unknown``.
parameters (object)
    Derived parameter set. Values are JSON numbers, strings, or bools.
defaults_used (array of str)
ref_build (bool)
crease_bow (object)
    Keys ``source`` (str), ``requested``, ``computed_from_m1_m2``,
    ``clamped`` (numbers).
chord_gate (object)
    Keys ``total_chord``, ``gate``, ``m1`` (numbers). ``gate`` is
    TOTAL_CHORD + 3.
wire_channel (object)
exceptions (object)
    Keys E1–E5, each with ``feature``, ``size``, ``plan_size``,
    ``minimum``.
fits (array of object)
    Each item: ``pair`` (str), ``type`` (str), ``nominal`` (number).
interference (object)
    ``lid_body_overlap_mm3`` (number),
    ``unintended_nominal_overlap_fail`` (bool).
span (object)
walls (object of numbers)
contact_stack (object)
keepout_clearance (object of numbers)
checks (array of object)
    Each: ``name`` (str), ``passed`` (bool), ``detail`` (str),
    ``numbers`` (object).
notes (object)
files (object)
    Each key is a file name. Each value is ``{sha256, bytes}``.
    ``sha256`` is 64 lowercase hex characters. ``bytes`` is a non-negative
    int. This map is the fifteen solids (five parts × STEP/STL/3MF).
quantities (object of ints)
parts (array of str)
variant_preload_built (object)

Optional keys (WP3 artwork):

views (object)
    ``render_medial.png``, ``render_lateral.png``, ``drawing.pdf``, each
    ``{sha256, bytes}`` with the same hash rule: SHA-256 of raw file
    bytes after date-bearing metadata is pinned to 2026-09-16T00:00:00Z.
views_hash_rule (str)
    States that pin.
views_commit (str)
    Same 40-hex commit as ``commit`` (solids last-change). Artwork regen
    does not move ``commit``. ``unknown`` is allowed only if git is missing.

``placement.svg`` (WP6's board placement drawing) sits beside these files
but is not a view of the solids and is not in ``views``;
``tests/test_placement.py`` checks that it regenerates byte-identical.

The validator fails loudly (SystemExit 2) on the first problem. It does
not repair the file.

Usage::

    .venv/bin/python scripts/cad/manifest.py docs/fab/cad/v1/manifest.json
    .venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v1/manifest.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = 1
HEX64 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^(unknown|[0-9a-f]{40})$")
REQUIRED = (
    "schema",
    "hash_rule",
    "commit",
    "parameters",
    "defaults_used",
    "ref_build",
    "crease_bow",
    "chord_gate",
    "wire_channel",
    "exceptions",
    "fits",
    "interference",
    "span",
    "walls",
    "contact_stack",
    "keepout_clearance",
    "checks",
    "notes",
    "files",
    "quantities",
    "parts",
    "variant_preload_built",
)
CREASE_BOW_KEYS = ("source", "requested", "computed_from_m1_m2", "clamped")
CHORD_GATE_KEYS = ("total_chord", "gate", "m1")
EXCEPTION_IDS = ("E1", "E2", "E3", "E4", "E5")
EXCEPTION_KEYS = ("feature", "size", "plan_size", "minimum")
CHECK_KEYS = ("name", "passed", "detail", "numbers")
FILE_KEYS = ("sha256", "bytes")
VIEW_FILES = ("render_medial.png", "render_lateral.png", "drawing.pdf")
VIEWS_HASH_RULE = (
    "SHA-256 of raw file bytes. PNG tIME/tEXt/zTXt/iTXt/eXIf rewritten; "
    "Creation Time text and PDF CreationDate/ModDate/ID pinned to "
    "2026-09-16T00:00:00Z. Same pin as the solids hash_rule timestamp."
)


class ManifestError(ValueError):
    """The document is not schema 1."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fail(path: str, message: str) -> None:
    raise ManifestError(f"{path}: {message}")


def _require_keys(obj: Any, keys: tuple[str, ...], path: str) -> None:
    if not isinstance(obj, dict):
        _fail(path, f"must be an object, got {type(obj).__name__}")
    missing = [key for key in keys if key not in obj]
    if missing:
        _fail(path, f"missing key {missing[0]!r}")


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check_file_meta(meta: Any, path: str) -> None:
    _require_keys(meta, FILE_KEYS, path)
    sha = meta["sha256"]
    if not isinstance(sha, str) or not HEX64.match(sha):
        _fail(f"{path}.sha256", "must be 64 lowercase hex characters")
    size = meta["bytes"]
    if not isinstance(size, int) or isinstance(size, bool) or size < 0:
        _fail(f"{path}.bytes", "must be a non-negative int")


def validate(payload: Any, *, path: str = "manifest") -> None:
    """Raise ManifestError if payload is not a schema-1 manifest."""
    _require_keys(payload, REQUIRED, path)
    if payload["schema"] != SCHEMA:
        _fail(f"{path}.schema", f"must be {SCHEMA}, got {payload['schema']!r}")
    if not isinstance(payload["hash_rule"], str) or not payload["hash_rule"].strip():
        _fail(f"{path}.hash_rule", "must be a non-empty string")
    if not isinstance(payload["commit"], str) or not COMMIT.match(payload["commit"]):
        _fail(f"{path}.commit", "must be 40 hex characters or 'unknown'")
    if not isinstance(payload["parameters"], dict):
        _fail(f"{path}.parameters", "must be an object")
    if not isinstance(payload["defaults_used"], list) or not all(
        isinstance(item, str) for item in payload["defaults_used"]
    ):
        _fail(f"{path}.defaults_used", "must be an array of strings")
    if not isinstance(payload["ref_build"], bool):
        _fail(f"{path}.ref_build", "must be a bool")
    _require_keys(payload["crease_bow"], CREASE_BOW_KEYS, f"{path}.crease_bow")
    if not isinstance(payload["crease_bow"]["source"], str):
        _fail(f"{path}.crease_bow.source", "must be a string")
    for key in ("requested", "computed_from_m1_m2", "clamped"):
        if not _is_number(payload["crease_bow"][key]):
            _fail(f"{path}.crease_bow.{key}", "must be a number")
    _require_keys(payload["chord_gate"], CHORD_GATE_KEYS, f"{path}.chord_gate")
    for key in CHORD_GATE_KEYS:
        if not _is_number(payload["chord_gate"][key]):
            _fail(f"{path}.chord_gate.{key}", "must be a number")
    if not isinstance(payload["wire_channel"], dict):
        _fail(f"{path}.wire_channel", "must be an object")
    exceptions = payload["exceptions"]
    _require_keys(exceptions, EXCEPTION_IDS, f"{path}.exceptions")
    for eid in EXCEPTION_IDS:
        block = exceptions[eid]
        _require_keys(block, EXCEPTION_KEYS, f"{path}.exceptions.{eid}")
        if not isinstance(block["feature"], str):
            _fail(f"{path}.exceptions.{eid}.feature", "must be a string")
    if not isinstance(payload["fits"], list):
        _fail(f"{path}.fits", "must be an array")
    for i, row in enumerate(payload["fits"]):
        _require_keys(row, ("pair", "type", "nominal"), f"{path}.fits[{i}]")
        if not _is_number(row["nominal"]):
            _fail(f"{path}.fits[{i}].nominal", "must be a number")
    interference = payload["interference"]
    _require_keys(
        interference,
        ("lid_body_overlap_mm3", "unintended_nominal_overlap_fail"),
        f"{path}.interference",
    )
    if not _is_number(interference["lid_body_overlap_mm3"]):
        _fail(f"{path}.interference.lid_body_overlap_mm3", "must be a number")
    if not isinstance(interference["unintended_nominal_overlap_fail"], bool):
        _fail(
            f"{path}.interference.unintended_nominal_overlap_fail",
            "must be a bool",
        )
    if not isinstance(payload["span"], dict):
        _fail(f"{path}.span", "must be an object")
    if not isinstance(payload["walls"], dict) or not all(
        _is_number(v) for v in payload["walls"].values()
    ):
        _fail(f"{path}.walls", "must be an object of numbers")
    if not isinstance(payload["contact_stack"], dict):
        _fail(f"{path}.contact_stack", "must be an object")
    if not isinstance(payload["keepout_clearance"], dict):
        _fail(f"{path}.keepout_clearance", "must be an object")
    if not isinstance(payload["checks"], list):
        _fail(f"{path}.checks", "must be an array")
    for i, row in enumerate(payload["checks"]):
        _require_keys(row, CHECK_KEYS, f"{path}.checks[{i}]")
        if not isinstance(row["passed"], bool):
            _fail(f"{path}.checks[{i}].passed", "must be a bool")
    if not isinstance(payload["notes"], dict):
        _fail(f"{path}.notes", "must be an object")
    files = payload["files"]
    if not isinstance(files, dict) or not files:
        _fail(f"{path}.files", "must be a non-empty object")
    for name, meta in files.items():
        if not isinstance(name, str) or "/" in name or "\\" in name:
            _fail(f"{path}.files", f"bad file name {name!r}")
        _check_file_meta(meta, f"{path}.files.{name}")
    if not isinstance(payload["quantities"], dict):
        _fail(f"{path}.quantities", "must be an object")
    if not isinstance(payload["parts"], list) or not all(
        isinstance(item, str) for item in payload["parts"]
    ):
        _fail(f"{path}.parts", "must be an array of strings")
    if not isinstance(payload["variant_preload_built"], dict):
        _fail(f"{path}.variant_preload_built", "must be an object")
    if "views" in payload:
        _validate_views(payload, path)


def _validate_views(payload: dict[str, Any], path: str) -> None:
    views = payload["views"]
    if not isinstance(views, dict):
        _fail(f"{path}.views", "must be an object")
    missing = [name for name in VIEW_FILES if name not in views]
    if missing:
        _fail(f"{path}.views", f"missing key {missing[0]!r}")
    extra = sorted(set(views) - set(VIEW_FILES))
    if extra:
        _fail(f"{path}.views", f"unknown file {extra[0]!r}")
    for name in VIEW_FILES:
        _check_file_meta(views[name], f"{path}.views.{name}")
    rule = payload.get("views_hash_rule")
    if not isinstance(rule, str) or not rule.strip():
        _fail(f"{path}.views_hash_rule", "must be a non-empty string when views is set")
    commit = payload.get("views_commit")
    if not isinstance(commit, str) or not COMMIT.match(commit):
        _fail(f"{path}.views_commit", "must be 40 hex characters or 'unknown'")


def validate_bytes(
    payload: dict[str, Any], folder: Path, *, path: str = "manifest"
) -> None:
    """Check sha256 and byte counts against files beside the JSON."""
    validate(payload, path=path)
    for map_name in ("files", "views"):
        mapping = payload.get(map_name)
        if not isinstance(mapping, dict):
            continue
        for name, meta in mapping.items():
            dest = folder / name
            if not dest.is_file():
                _fail(f"{path}.{map_name}.{name}", f"file missing: {dest}")
            digest = sha256_file(dest)
            if digest != meta["sha256"]:
                _fail(
                    f"{path}.{map_name}.{name}",
                    f"sha256 mismatch: file {digest} manifest {meta['sha256']}",
                )
            size = dest.stat().st_size
            if size != meta["bytes"]:
                _fail(
                    f"{path}.{map_name}.{name}",
                    f"bytes mismatch: file {size} manifest {meta['bytes']}",
                )


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"{path}: cannot read JSON ({exc})") from exc
    if not isinstance(payload, dict):
        raise ManifestError(f"{path}: top level must be an object")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a schema-1 CAD manifest.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--check-bytes",
        action="store_true",
        help="Also hash the files listed in files and views",
    )
    args = parser.parse_args(argv)
    payload = load_manifest(args.manifest)
    if args.check_bytes:
        validate_bytes(payload, args.manifest.parent, path=str(args.manifest))
    else:
        validate(payload, path=str(args.manifest))
    print(f"{args.manifest}: schema {payload['schema']} ok")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ManifestError as exc:
        print(f"MANIFEST FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
