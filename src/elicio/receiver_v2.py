"""Receive frame v2 streams on the Mac and write pipeline sessions.

The on-disk session is consumed by ``load_receiver_session``, which
returns ``elicio.pipeline.load.Recording`` (the pipeline standard form).
Codes stay int32 in the npz; the loader exposes them as float32 without
applying the nominal scale.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Protocol

import numpy as np

from elicio.frame_v2 import (
    FRAME_V2_GAIN,
    FRAME_V2_MAX_SAMPLES,
    FRAME_V2_SAMPLE_BYTES,
    FRAME_V2_SPS,
    BatteryFrame,
    DecodeError,
    Flag,
    HelloFrame,
    MsgType,
    Reassembler,
    StopReason,
    StreamFrame,
    StreamMeta,
    fragment,
    pack_battery,
    pack_hello,
    pack_stream,
)
from elicio.pipeline.load import Recording

NUS_SERVICE = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
NUS_RX = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
NUS_TX = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

LOADER_NAME = "elicio.receiver_v2.load_receiver_session"
PIPELINE_RECORDING = "elicio.pipeline.load.Recording"
SESSION_FORMAT = "elicio_receiver_v2"
SAMPLES_NAME = "samples.npz"
SIDECAR_NAME = "sidecar.json"
META_NAME = "meta.json"
DROPOUT_INTERVALS = 200
RAIL_CODE = (1 << 23) - 1
RESTART_EXCLUDE = 200

GPIO_MACRO = {
    "AFE SCLK": "ELICIO_PIN_ADS_SCLK",
    "AFE MOSI": "ELICIO_PIN_ADS_MOSI",
    "AFE MISO": "ELICIO_PIN_ADS_MISO",
    "AFE CS": "ELICIO_PIN_ADS_CS",
    "AFE DRDY": "ELICIO_PIN_ADS_DRDY",
    "AFE START": "ELICIO_PIN_ADS_START",
    "AFE PWDN/RESET": "ELICIO_PIN_ADS_PWDN",
    "VBUS_DET": "ELICIO_PIN_VBUS_DET",
    "CHG_MON": "ELICIO_PIN_CHG_MON",
    "VBAT_SENSE": "ELICIO_PIN_VBAT_SENSE",
    "BAT_MEAS_EN (Q5 DNP, unused)": "ELICIO_PIN_BAT_MEAS_EN",
    "LED_EN": "ELICIO_PIN_LED_EN",
    "nRESET": "ELICIO_PIN_NRESET",
}

SAME_CRITERION = ("3.5", "3.6", "3.7", "3.8", "3.9", "3.10")

# receive-check exit codes (docs/fab/receiver-v2.md, "Exit codes").
EXIT_OK = 0
EXIT_SAME_CRITERION_FAILED = 1
EXIT_NOT_A_SESSION = 2
EXIT_DROPOUT_3_4 = 3

FRAME_CASES = (
    "normal",
    "wrap",
    "fragment",
    "reorder",
    "loss",
    "overrun",
    "partial",
    "reconnect",
    "bad_crc",
    "version_mismatch",
)


class PacketSource(Protocol):
    def iter_packets(self) -> Iterator[bytes]:
        ...


class ListSource:
    def __init__(self, packets: list[bytes]) -> None:
        self._packets = packets

    def iter_packets(self) -> Iterator[bytes]:
        yield from self._packets


def ads24_to_int32(raw: bytes) -> int:
    value = (raw[0] << 16) | (raw[1] << 8) | raw[2]
    if value & 0x800000:
        value -= 0x1000000
    return value


def int32_to_ads24(value: int) -> bytes:
    unsigned = value & 0xFFFFFF
    return bytes([(unsigned >> 16) & 0xFF, (unsigned >> 8) & 0xFF, unsigned & 0xFF])


def pack_ads_sample(status: int, ch1: int, ch2: int) -> bytes:
    return int32_to_ads24(status) + int32_to_ads24(ch1) + int32_to_ads24(ch2)


def parse_board_v2_gpio(text: str) -> dict[str, int]:
    start = text.find("## 9. G4 / firmware GPIO map")
    if start < 0:
        raise ValueError("board-v2.md has no §9 GPIO map")
    rest = text[start:]
    end = rest.find("\n## 10.")
    section = rest if end < 0 else rest[:end]
    pins: dict[str, int] = {}
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 3 or cells[0] in {"Function", "---"}:
            continue
        match = re.search(r"P(\d)\.(\d+)", cells[2])
        if match is None:
            continue
        pins[cells[0]] = int(match.group(1)) * 32 + int(match.group(2))
    return pins


def parse_board_pins_h(text: str) -> dict[str, int]:
    found: dict[str, int] = {}
    for match in re.finditer(
        r"#define\s+(ELICIO_PIN_[A-Z0-9_]+)\s+(\d+)\s*/\*\s*P(\d)\.(\d+)",
        text,
    ):
        name = match.group(1)
        value = int(match.group(2))
        gpio = int(match.group(3)) * 32 + int(match.group(4))
        if value != gpio:
            raise ValueError(f"{name} value {value} is not P{match.group(3)}.{match.group(4)}")
        found[name] = value
    return found


def assert_pin_map_matches(board_md: str, pins_h: str) -> None:
    from_md = parse_board_v2_gpio(board_md)
    from_h = parse_board_pins_h(pins_h)
    for function, macro in GPIO_MACRO.items():
        if function not in from_md:
            raise AssertionError(f"board-v2.md §9 missing {function}")
        if macro not in from_h:
            raise AssertionError(f"{macro} missing from board_pins.h")
        if from_md[function] != from_h[macro]:
            raise AssertionError(
                f"{function}: board-v2.md {from_md[function]} vs {macro} {from_h[macro]}"
            )
    if not re.search(r"#define\s+ELICIO_PIN_LED_STREAM\s+ELICIO_PIN_LED_EN", pins_h):
        raise AssertionError("LED_STREAM must alias LED_EN")
    if not re.search(r"#define\s+ELICIO_PIN_RECOVERY\s+ELICIO_PIN_NRESET", pins_h):
        raise AssertionError("RECOVERY must alias NRESET")


@dataclass
class SessionEvent:
    kind: str
    detail: dict[str, int | str]


@dataclass
class ReceiverSession:
    codes: list[list[int]] = field(default_factory=list)
    status: list[int] = field(default_factory=list)
    acq_index: list[int] = field(default_factory=list)
    flags: list[int] = field(default_factory=list)
    stop_reason: list[int] = field(default_factory=list)
    events: list[SessionEvent] = field(default_factory=list)
    batteries: list[dict[str, int]] = field(default_factory=list)
    decode_errors: list[str] = field(default_factory=list)
    wrap_count: int = 0
    overrun_count: int = 0
    transport_loss_count: int = 0
    reconnect_count: int = 0
    mtu: int = 20
    session_id: int = 0
    subject: str = "bench"
    session_name: str = "s2"
    gain: int = FRAME_V2_GAIN


class Receiver:
    def __init__(self, subject: str = "bench", session_name: str = "s2") -> None:
        self.reassembler = Reassembler()
        self.state = ReceiverSession(subject=subject, session_name=session_name)

    def feed(self, packet: bytes) -> None:
        try:
            items = self.reassembler.push(packet)
        except DecodeError as exc:
            self.state.decode_errors.append(exc.code)
            self.state.events.append(SessionEvent(exc.code, {}))
            return
        for item in items:
            if isinstance(item, StreamFrame):
                self._on_stream(item)
            elif isinstance(item, HelloFrame):
                self.state.session_id = item.session_id
                self.state.mtu = item.nus_payload
                self.state.gain = item.gain
            elif isinstance(item, BatteryFrame):
                self.state.batteries.append(
                    {
                        "seq": item.msg_seq,
                        "millivolts": item.millivolts,
                        "flags": item.flags,
                        "stop_reason": item.stop_reason,
                    }
                )
            elif isinstance(item, tuple):
                self._on_extra(item)

    def ingest(self, source: PacketSource) -> ReceiverSession:
        for packet in source.iter_packets():
            self.feed(packet)
        return self.state

    def _on_extra(self, extra: tuple) -> None:
        kind = extra[0]
        if kind == "transport_loss":
            expected, got = int(extra[1]), int(extra[2])
            lost = (got - expected) & 0xFFFF
            self.state.transport_loss_count += lost
            self.state.events.append(
                SessionEvent("transport_loss", {"expected": expected, "got": got, "lost": lost})
            )
        elif kind == "overrun":
            self.state.overrun_count += 1
            self.state.events.append(SessionEvent("overrun", {"acq_index": int(extra[1])}))
        elif kind == "wrap":
            self.state.wrap_count += 1
            self.state.events.append(SessionEvent("wrap", {"acq_index": int(extra[1])}))
        elif kind == "reconnect":
            self.state.reconnect_count += 1
            self.state.events.append(SessionEvent("reconnect", {"session_id": int(extra[1])}))

    def _on_stream(self, frame: StreamFrame) -> None:
        meta = frame.meta
        self.state.session_id = meta.session_id
        self.state.gain = meta.gain
        if meta.flags & Flag.VBUS:
            self.state.events.append(SessionEvent("vbus", {"stop_reason": meta.stop_reason}))
        if meta.stop_reason == StopReason.UNDERVOLTAGE:
            self.state.events.append(
                SessionEvent("undervoltage", {"stop_reason": meta.stop_reason})
            )
        if meta.sample_count == 0:
            return
        raw = frame.samples
        base = self.reassembler.extended_acq_index(meta.session_id, meta.acq_index)
        for i in range(meta.sample_count):
            chunk = raw[i * FRAME_V2_SAMPLE_BYTES : (i + 1) * FRAME_V2_SAMPLE_BYTES]
            status = ads24_to_int32(chunk[0:3])
            ch1 = ads24_to_int32(chunk[3:6])
            ch2 = ads24_to_int32(chunk[6:9])
            self.state.codes.append([ch1, ch2])
            self.state.status.append(status)
            self.state.acq_index.append(base + i)
            self.state.flags.append(meta.flags)
            self.state.stop_reason.append(meta.stop_reason)


def write_session(state: ReceiverSession, out_dir: Path) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    n = len(state.codes)
    codes = np.asarray(state.codes, dtype=np.int32).reshape(n, 2) if n else np.zeros((0, 2), np.int32)
    np.savez_compressed(
        out_dir / SAMPLES_NAME,
        codes=codes,
        status=np.asarray(state.status, dtype=np.int32),
        acq_index=np.asarray(state.acq_index, dtype=np.int64),
        flags=np.asarray(state.flags, dtype=np.uint8),
        stop_reason=np.asarray(state.stop_reason, dtype=np.uint8),
        labels=np.zeros(n, dtype=np.int32),
        sample_rate=np.float64(FRAME_V2_SPS),
        subject=np.array(state.subject),
        session=np.array(state.session_name),
        channel_names=np.array(["ADS_CH1", "ADS_CH2"]),
        gain=np.int32(state.gain),
    )
    sidecar = {
        "overrun_count": state.overrun_count,
        "transport_loss_count": state.transport_loss_count,
        "reconnect_count": state.reconnect_count,
        "wrap_count": state.wrap_count,
        "decode_errors": list(state.decode_errors),
        "events": [{"kind": e.kind, **e.detail} for e in state.events],
        "batteries": state.batteries,
        "same_criterion": {key: "not_scored" for key in SAME_CRITERION},
    }
    (out_dir / SIDECAR_NAME).write_text(json.dumps(sidecar, indent=2) + "\n", encoding="utf-8")
    meta = {
        "format": SESSION_FORMAT,
        "loader": LOADER_NAME,
        "pipeline_recording": PIPELINE_RECORDING,
        "sample_rate": FRAME_V2_SPS,
        "mtu": state.mtu,
        "session_id": state.session_id,
        "gain": state.gain,
        "sample_count": n,
    }
    (out_dir / META_NAME).write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return out_dir


def load_receiver_session(session_dir: Path) -> Recording:
    """Load a receive session as ``elicio.pipeline.load.Recording``."""
    session_dir = Path(session_dir)
    data = np.load(session_dir / SAMPLES_NAME, allow_pickle=False)
    codes = np.asarray(data["codes"], dtype=np.int32)
    labels = np.asarray(data["labels"], dtype=np.int32)
    names = [str(name) for name in np.asarray(data["channel_names"]).tolist()]
    extra = {
        "codes_int32": codes,
        "status": np.asarray(data["status"], dtype=np.int32),
        "acq_index": np.asarray(data["acq_index"], dtype=np.int64),
        "flags": np.asarray(data["flags"], dtype=np.uint8),
        "loader": LOADER_NAME,
    }
    return Recording(
        signal=codes.astype(np.float32),
        labels=labels,
        sample_rate=float(np.asarray(data["sample_rate"])),
        channel_names=names,
        subject=str(np.asarray(data["subject"])),
        session=str(np.asarray(data["session"])),
        extra=extra,
    )


def _dropout_stretches(
    acq: np.ndarray, codes: np.ndarray, flags: np.ndarray
) -> list[dict[str, int]]:
    n = int(codes.shape[0])
    unique: list[dict[str, int]] = []
    if n == 0:
        return unique

    def skipped(index: int) -> bool:
        if int(flags[index]) & Flag.INVALID:
            return True
        return False

    # Montage §8: the first 200 conversions after each RESTART flag are not
    # scored. Review r6: one window per RESTART; the old single
    # ``restart_until`` also skipped every sample before the last restart.
    restarts = [int(acq[index]) for index in range(n) if int(flags[index]) & Flag.RESTART]

    def settling(index: int) -> bool:
        a = int(acq[index])
        return any(r <= a < r + RESTART_EXCLUDE for r in restarts)

    for channel in (0, 1):
        i = 0
        while i < n:
            if skipped(i) or settling(i):
                i += 1
                continue
            code = int(codes[i, channel])
            run = 1
            last_acq = int(acq[i])
            j = i + 1
            while j < n:
                if skipped(j) or settling(j):
                    break
                if int(codes[j, channel]) != code:
                    break
                if int(acq[j]) != last_acq + 1:
                    break
                last_acq = int(acq[j])
                run += 1
                j += 1
            # "More than 200 sample intervals": a run of k equal samples
            # spans k - 1 intervals.
            if run - 1 > DROPOUT_INTERVALS:
                unique.append(
                    {
                        "channel": channel,
                        "start_acq": int(acq[i]),
                        "length": run,
                        "kind": 1 if abs(code) >= RAIL_CODE else 0,
                    }
                )
                i = j
            else:
                i += 1
    return unique


def check_session(session_dir: Path) -> dict[str, object]:
    session_dir = Path(session_dir)
    recording = load_receiver_session(session_dir)
    sidecar = json.loads((session_dir / SIDECAR_NAME).read_text(encoding="utf-8"))
    acq = recording.extra["acq_index"]
    codes = recording.extra["codes_int32"]
    flags = recording.extra["flags"]
    n = int(recording.signal.shape[0])
    duration_s = 0.0
    if n:
        duration_s = (int(acq[-1]) - int(acq[0]) + 1) / FRAME_V2_SPS
    dropouts = _dropout_stretches(acq, codes, flags)
    same = sidecar.get("same_criterion", {key: "not_scored" for key in SAME_CRITERION})
    same_fail = [
        key
        for key, value in same.items()
        if key in SAME_CRITERION and value not in {"not_scored", "pass"}
    ]
    # Montage §8 table: only 3.5–3.10 are marked "same criterion"; they fail
    # only when scored. Line 3.4 is marked "revised" (its dropout half keeps
    # the original rail/flat rule), so a dropout is reported with its own
    # exit code, not as a same-criterion failure (review r6; whether a 3.4
    # dropout stops S2 is decision 76 in tasks/reviews/code-r6.md).
    ok = len(dropouts) == 0 and not same_fail
    if same_fail:
        exit_code = EXIT_SAME_CRITERION_FAILED
    elif dropouts:
        exit_code = EXIT_DROPOUT_3_4
    else:
        exit_code = EXIT_OK
    return {
        "sample_count": n,
        "duration_s": duration_s,
        "wraps": sidecar.get("wrap_count", 0),
        "overruns": sidecar.get("overrun_count", 0),
        "losses": sidecar.get("transport_loss_count", 0),
        "dropout_stretches": len(dropouts),
        "dropouts": dropouts,
        "same_criterion": same,
        "same_criterion_failed": same_fail,
        "ok": ok,
        "exit_code": exit_code,
        "loader": LOADER_NAME,
    }


def load_fixture_packets(path: Path) -> list[bytes]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return [bytes.fromhex(item) for item in payload["packets_hex"]]


def dump_fixture_packets(path: Path, packets: list[bytes]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {"packets_hex": [packet.hex() for packet in packets]}
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")


def _sample_bytes(count: int, seed: int = 1) -> bytes:
    out = bytearray()
    for i in range(count):
        out += pack_ads_sample(0xC00000 + i, seed * 17 + i, seed * 31 + i)
    return bytes(out)


def _meta(count: int, acq: int, seq: int, flags: int = 0) -> StreamMeta:
    return StreamMeta(
        session_id=7,
        frame_seq=seq,
        acq_index=acq & 0xFFFF,
        sample_count=count,
        flags=flags,
        stop_reason=StopReason.NONE,
    )


def case_packets(name: str) -> list[bytes]:
    if name == "normal":
        logical = pack_stream(_meta(4, 10, 3), _sample_bytes(4))
        return fragment(MsgType.STREAM, 7, 3, logical, 244)
    if name == "wrap":
        first = pack_stream(_meta(2, 65534, 9), _sample_bytes(2, 2))
        second = pack_stream(_meta(2, 1, 10), _sample_bytes(2, 2))
        return fragment(MsgType.STREAM, 7, 9, first, 244) + fragment(
            MsgType.STREAM, 7, 10, second, 244
        )
    if name == "fragment":
        logical = pack_stream(_meta(3, 20, 4), _sample_bytes(3, 3))
        return fragment(MsgType.STREAM, 7, 4, logical, 20)
    if name == "reorder":
        logical = pack_stream(_meta(3, 30, 5), _sample_bytes(3, 4))
        return list(reversed(fragment(MsgType.STREAM, 7, 5, logical, 20)))
    if name == "loss":
        first = pack_stream(_meta(1, 0, 1), _sample_bytes(1, 5))
        third = pack_stream(_meta(1, 2, 3), _sample_bytes(1, 5))
        return fragment(MsgType.STREAM, 7, 1, first, 244) + fragment(
            MsgType.STREAM, 7, 3, third, 244
        )
    if name == "overrun":
        logical = pack_stream(_meta(1, 40, 6, Flag.OVERRUN), _sample_bytes(1, 6))
        return fragment(MsgType.STREAM, 7, 6, logical, 244)
    if name == "partial":
        logical = pack_stream(_meta(3, 50, 8), _sample_bytes(3, 7))
        return [fragment(MsgType.STREAM, 7, 8, logical, 20)[0]]
    if name == "reconnect":
        hello = pack_hello(
            HelloFrame(
                session_id=9,
                epoch_id=9,
                acq_index=12,
                nus_payload=244,
                flags=0,
                stop_reason=StopReason.RESET,
            )
        )
        return fragment(MsgType.HELLO, 9, 0, hello, 244)
    if name == "bad_crc":
        logical = bytearray(pack_stream(_meta(1, 60, 11), _sample_bytes(1, 8)))
        logical[-1] ^= 0xFF
        return fragment(MsgType.STREAM, 7, 11, bytes(logical), 244)
    if name == "version_mismatch":
        return [bytes([1, MsgType.STREAM, 7, 0, 1, 0, 0, 1]) + b"x"]
    if name == "dropout":
        n = DROPOUT_INTERVALS + 5
        sample = pack_ads_sample(0xC00000, RAIL_CODE, RAIL_CODE)
        packets: list[bytes] = []
        acq = 0
        seq = 1
        left = n
        while left:
            count = min(FRAME_V2_MAX_SAMPLES, left)
            logical = pack_stream(_meta(count, acq, seq), sample * count)
            packets.extend(fragment(MsgType.STREAM, 7, seq, logical, 244))
            acq += count
            seq += 1
            left -= count
        return packets
    if name == "undervoltage":
        logical = pack_stream(
            StreamMeta(
                session_id=7,
                frame_seq=1,
                acq_index=0,
                sample_count=0,
                flags=Flag.STOPPED | Flag.INVALID,
                stop_reason=StopReason.UNDERVOLTAGE,
            ),
            b"",
        )
        return fragment(MsgType.STREAM, 7, 1, logical, 244)
    if name == "vbus":
        logical = pack_stream(
            StreamMeta(
                session_id=7,
                frame_seq=1,
                acq_index=0,
                sample_count=0,
                flags=Flag.VBUS | Flag.STOPPED | Flag.INVALID,
                stop_reason=StopReason.VBUS,
            ),
            b"",
        )
        return fragment(MsgType.STREAM, 7, 1, logical, 244)
    raise KeyError(name)


def live_fake_packets() -> list[bytes]:
    packets: list[bytes] = []
    hello = pack_hello(
        HelloFrame(
            session_id=7,
            epoch_id=7,
            acq_index=0,
            nus_payload=20,
            flags=0,
            stop_reason=StopReason.RESET,
        )
    )
    packets.extend(fragment(MsgType.HELLO, 7, 0, hello, 20))
    first = pack_stream(_meta(3, 0, 1), _sample_bytes(3, 9))
    packets.extend(fragment(MsgType.STREAM, 7, 1, first, 20))
    third = pack_stream(_meta(3, 6, 3), _sample_bytes(3, 10))
    packets.extend(reversed(fragment(MsgType.STREAM, 7, 3, third, 20)))
    reconnect = pack_hello(
        HelloFrame(
            session_id=7,
            epoch_id=7,
            acq_index=9,
            nus_payload=20,
            flags=0,
            stop_reason=StopReason.NONE,
        )
    )
    packets.extend(fragment(MsgType.HELLO, 7, 0, reconnect, 20))
    after = pack_stream(_meta(2, 9, 1, Flag.OVERRUN | Flag.RESTART), _sample_bytes(2, 11))
    packets.extend(fragment(MsgType.STREAM, 7, 1, after, 20))
    battery = pack_battery(BatteryFrame(7, 0, 3710, 0, StopReason.NONE, 0))
    packets.extend(fragment(MsgType.BATTERY, 7, 0, battery, 20))
    return packets


def receive_packets(
    packets: list[bytes], out_dir: Path, subject: str, session_name: str
) -> Path:
    receiver = Receiver(subject=subject, session_name=session_name)
    receiver.ingest(ListSource(packets))
    return write_session(receiver.state, out_dir)


def run_receive(args: object) -> int:
    out = Path(getattr(args, "out"))
    subject = str(getattr(args, "subject"))
    session_name = str(getattr(args, "session") or "s2")
    if getattr(args, "simulate", None) is not None:
        packets = load_fixture_packets(Path(args.simulate))
        receive_packets(packets, out, subject, session_name)
        print(json.dumps({"out": str(out.resolve()), "mode": "simulate"}, indent=2, sort_keys=True))
        return 0
    if getattr(args, "simulate_live", False):
        receive_packets(live_fake_packets(), out, subject, session_name)
        print(
            json.dumps(
                {"out": str(out.resolve()), "mode": "simulate-live"}, indent=2, sort_keys=True
            )
        )
        return 0
    device = getattr(args, "device", None)
    if not device:
        raise AssertionError("receive needs --device, --simulate, or --simulate-live")
    return _run_bleak(str(device), out, subject, session_name, getattr(args, "seconds", None))


def _run_bleak(
    device: str,
    out: Path,
    subject: str,
    session_name: str,
    seconds: float | None,
) -> int:
    try:
        from bleak import BleakClient, BleakScanner
    except ImportError:
        print(
            json.dumps(
                {"error": "bleak is not installed", "install": "pip install 'elicio[ble]'"},
                indent=2,
            )
        )
        return 2

    receiver = Receiver(subject=subject, session_name=session_name)

    async def _go() -> None:
        target: object = device
        looks_like_address = device.count(":") >= 5
        if not looks_like_address:
            found = None
            for info in await BleakScanner.discover():
                if info.name == device or str(info.address).lower() == device.lower():
                    found = info
                    break
            if found is None:
                raise RuntimeError(f"no BLE device named {device}")
            target = found
        async with BleakClient(target) as client:
            receiver.state.mtu = int(getattr(client, "mtu_size", 23) or 23) - 3

            def _on_notify(_handle: object, data: bytearray) -> None:
                receiver.feed(bytes(data))

            await client.start_notify(NUS_TX, _on_notify)
            if seconds is None:
                while client.is_connected:
                    await asyncio.sleep(0.2)
            else:
                await asyncio.sleep(seconds)
            with contextlib.suppress(Exception):
                await client.stop_notify(NUS_TX)

    try:
        asyncio.run(_go())
    except RuntimeError as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return 2
    write_session(receiver.state, out)
    print(json.dumps({"out": str(out.resolve()), "mode": "ble", "device": device}, indent=2))
    return 0


def run_receive_check(session_dir: Path) -> int:
    session_dir = Path(session_dir)
    missing = [
        name
        for name in (SAMPLES_NAME, SIDECAR_NAME, META_NAME)
        if not (session_dir / name).is_file()
    ]
    if missing:
        print(json.dumps({"error": "not a session", "missing": missing}, indent=2))
        return EXIT_NOT_A_SESSION
    summary = check_session(session_dir)
    print(json.dumps(summary, indent=2, sort_keys=True, default=str))
    return int(summary["exit_code"])

