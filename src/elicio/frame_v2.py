from __future__ import annotations

import struct
import zlib
from dataclasses import dataclass
from enum import IntEnum

FRAME_V2_VERSION = 2
FRAME_V2_SPS = 2000
FRAME_V2_GAIN = 12
FRAME_V2_SAMPLE_BYTES = 9
FRAME_V2_FRAG_HDR = 8
FRAME_V2_STREAM_HDR = 16
FRAME_V2_HELLO_LEN = 16
FRAME_V2_BATTERY_LEN = 12
FRAME_V2_CRC_LEN = 4
FRAME_V2_MAX_SAMPLES = 40

# Nominal scale, metadata only (plan v2 §6). Not applied by the decoder.
NOMINAL_SCALE_V = 2.42 / (12 * ((1 << 23) - 1))
NOMINAL_FULL_SCALE_V = 2.42 / 12


class MsgType(IntEnum):
    HELLO = 0x00
    STREAM = 0x01
    BATTERY = 0x02


class Flag:
    INVALID = 0x01
    OVERRUN = 0x02
    STOPPED = 0x04
    RESTART = 0x08
    VBUS = 0x10


class StopReason(IntEnum):
    NONE = 0
    UNDERVOLTAGE = 1
    VBUS = 2
    RESET = 3
    HOST = 4


class DecodeError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def crc32(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def samples_for_nus(nus_payload: int) -> int:
    if nus_payload <= FRAME_V2_FRAG_HDR:
        return 0
    data = nus_payload - FRAME_V2_FRAG_HDR
    if data < FRAME_V2_STREAM_HDR + FRAME_V2_CRC_LEN:
        return 1
    n = (data - FRAME_V2_STREAM_HDR - FRAME_V2_CRC_LEN) // FRAME_V2_SAMPLE_BYTES
    if n > FRAME_V2_MAX_SAMPLES:
        n = FRAME_V2_MAX_SAMPLES
    return 1 if n == 0 else n


def _check_crc(body_and_crc: bytes) -> bytes:
    if len(body_and_crc) < FRAME_V2_CRC_LEN:
        raise DecodeError("partial_frame", "frame shorter than a CRC")
    body = body_and_crc[:-FRAME_V2_CRC_LEN]
    (got,) = struct.unpack_from("<I", body_and_crc, len(body))
    if crc32(body) != got:
        raise DecodeError("bad_crc", "CRC32 mismatch")
    return body


@dataclass(frozen=True, slots=True)
class StreamMeta:
    session_id: int
    frame_seq: int
    acq_index: int
    sample_count: int
    flags: int
    stop_reason: int
    gain: int = FRAME_V2_GAIN
    rate_id: int = 0
    vref_id: int = 0
    sample_bytes: int = FRAME_V2_SAMPLE_BYTES

    @property
    def payload_bytes(self) -> int:
        return self.sample_count * self.sample_bytes


@dataclass(frozen=True, slots=True)
class StreamFrame:
    meta: StreamMeta
    samples: bytes


@dataclass(frozen=True, slots=True)
class HelloFrame:
    session_id: int
    epoch_id: int
    acq_index: int
    nus_payload: int
    flags: int
    stop_reason: int
    gain: int = FRAME_V2_GAIN
    rate_id: int = 0
    vref_id: int = 0
    sample_bytes: int = FRAME_V2_SAMPLE_BYTES
    reserved: int = 0


@dataclass(frozen=True, slots=True)
class BatteryFrame:
    session_id: int
    msg_seq: int
    millivolts: int
    flags: int
    stop_reason: int
    reserved: int = 0


def pack_stream(meta: StreamMeta, samples: bytes) -> bytes:
    if meta.sample_count > FRAME_V2_MAX_SAMPLES:
        raise ValueError("sample_count exceeds FRAME_V2_MAX_SAMPLES")
    if meta.sample_bytes != FRAME_V2_SAMPLE_BYTES:
        raise ValueError("sample_bytes must be 9")
    if len(samples) != meta.payload_bytes:
        raise ValueError("samples length must equal sample_count * 9")
    header = struct.pack(
        "<HHHHBBBBBBH",
        meta.session_id,
        meta.frame_seq,
        meta.acq_index,
        meta.sample_count,
        meta.flags,
        meta.stop_reason,
        meta.gain,
        meta.rate_id,
        meta.vref_id,
        meta.sample_bytes,
        meta.payload_bytes,
    )
    body = header + samples
    return body + struct.pack("<I", crc32(body))


def pack_hello(frame: HelloFrame) -> bytes:
    body = struct.pack(
        "<HHHHBBBBBBH",
        frame.session_id,
        frame.epoch_id,
        frame.acq_index,
        frame.nus_payload,
        frame.flags,
        frame.stop_reason,
        frame.gain,
        frame.rate_id,
        frame.vref_id,
        frame.sample_bytes,
        frame.reserved,
    )
    return body + struct.pack("<I", crc32(body))


def pack_battery(frame: BatteryFrame) -> bytes:
    body = struct.pack(
        "<HHHBBI",
        frame.session_id,
        frame.msg_seq,
        frame.millivolts,
        frame.flags,
        frame.stop_reason,
        frame.reserved,
    )
    return body + struct.pack("<I", crc32(body))


def fragment(
    msg_type: int,
    session_id: int,
    frame_seq: int,
    logical: bytes,
    nus_payload: int,
) -> list[bytes]:
    if nus_payload <= FRAME_V2_FRAG_HDR:
        raise ValueError("NUS payload too small for a fragment header")
    chunk = nus_payload - FRAME_V2_FRAG_HDR
    if not logical:
        slices = [b""]
    else:
        slices = [logical[i : i + chunk] for i in range(0, len(logical), chunk)]
    count = len(slices)
    packets = []
    for index, piece in enumerate(slices):
        header = struct.pack(
            "<BBHHBB",
            FRAME_V2_VERSION,
            msg_type,
            session_id,
            frame_seq,
            index,
            count,
        )
        packets.append(header + piece)
    return packets


def unpack_stream(logical: bytes) -> StreamFrame:
    body = _check_crc(logical)
    if len(body) < FRAME_V2_STREAM_HDR:
        raise DecodeError("partial_frame", "stream header truncated")
    fields = struct.unpack_from("<HHHHBBBBBBH", body, 0)
    meta = StreamMeta(
        session_id=fields[0],
        frame_seq=fields[1],
        acq_index=fields[2],
        sample_count=fields[3],
        flags=fields[4],
        stop_reason=fields[5],
        gain=fields[6],
        rate_id=fields[7],
        vref_id=fields[8],
        sample_bytes=fields[9],
    )
    if fields[10] != meta.payload_bytes:
        raise DecodeError("partial_frame", "payload_bytes does not match sample_count")
    samples = body[FRAME_V2_STREAM_HDR:]
    if len(samples) != meta.payload_bytes:
        raise DecodeError("partial_frame", "sample payload truncated")
    return StreamFrame(meta=meta, samples=samples)


def unpack_hello(logical: bytes) -> HelloFrame:
    body = _check_crc(logical)
    if len(body) != FRAME_V2_HELLO_LEN:
        raise DecodeError("partial_frame", "hello length")
    fields = struct.unpack("<HHHHBBBBBBH", body)
    return HelloFrame(*fields)


def unpack_battery(logical: bytes) -> BatteryFrame:
    body = _check_crc(logical)
    if len(body) != FRAME_V2_BATTERY_LEN:
        raise DecodeError("partial_frame", "battery length")
    fields = struct.unpack("<HHHBBI", body)
    return BatteryFrame(*fields)


UNPACKERS = {
    MsgType.STREAM: unpack_stream,
    MsgType.HELLO: unpack_hello,
    MsgType.BATTERY: unpack_battery,
}


@dataclass
class Reassembler:
    """Reassemble NUS packets. Partial frames are rejected, never emitted."""

    def __init__(self) -> None:
        self._pending: dict[tuple[int, int, int], dict] = {}
        self._last_seq: dict[tuple[int, int], int | None] = {}
        self._acq_ext: dict[int, int] = {}
        self._last_acq: dict[int, int | None] = {}

    def reset_session(self, session_id: int) -> None:
        drop = [key for key in self._pending if key[0] == session_id]
        for key in drop:
            del self._pending[key]
        self._last_seq = {k: v for k, v in self._last_seq.items() if k[0] != session_id}
        self._acq_ext.pop(session_id, None)
        self._last_acq.pop(session_id, None)

    def push(self, packet: bytes) -> list[object]:
        if len(packet) < FRAME_V2_FRAG_HDR:
            raise DecodeError("partial_frame", "fragment header truncated")
        version, msg_type, session_id, frame_seq, frag_index, frag_count = struct.unpack_from(
            "<BBHHBB", packet, 0
        )
        if version != FRAME_V2_VERSION:
            raise DecodeError("version_mismatch", f"version {version} is not 2")
        if frag_count == 0 or frag_index >= frag_count:
            raise DecodeError("partial_frame", "fragment index or count")
        payload = packet[FRAME_V2_FRAG_HDR:]
        key = (session_id, msg_type, frame_seq)
        slot = self._pending.get(key)
        if slot is None:
            slot = {"count": frag_count, "parts": {}}
            self._pending[key] = slot
        elif slot["count"] != frag_count:
            del self._pending[key]
            raise DecodeError("partial_frame", "fragment count changed")
        slot["parts"][frag_index] = payload
        if len(slot["parts"]) < frag_count:
            return []
        logical = b"".join(slot["parts"][i] for i in range(frag_count))
        del self._pending[key]
        unpacker = UNPACKERS.get(msg_type)
        if unpacker is None:
            raise DecodeError("version_mismatch", f"unknown message type {msg_type}")
        message = unpacker(logical)
        extras: list[object] = []
        seq_key = (session_id, msg_type)
        last = self._last_seq.get(seq_key)
        if last is not None:
            expected = (last + 1) & 0xFFFF
            if frame_seq != expected:
                extras.append(("transport_loss", expected, frame_seq))
        self._last_seq[seq_key] = frame_seq
        if isinstance(message, StreamFrame):
            wrap = self._note_acq(session_id, message.meta.acq_index)
            if wrap:
                extras.append(("wrap", message.meta.acq_index))
            if message.meta.flags & Flag.OVERRUN:
                extras.append(("overrun", message.meta.acq_index))
        if isinstance(message, HelloFrame):
            self.reset_session(session_id)
            self._last_seq[seq_key] = frame_seq
            extras.append(("reconnect", session_id))
        return [message, *extras]

    def _note_acq(self, session_id: int, acq_index: int) -> bool:
        last = self._last_acq.get(session_id)
        self._last_acq[session_id] = acq_index
        if last is None:
            self._acq_ext[session_id] = 0
            return False
        if acq_index < last:
            self._acq_ext[session_id] = self._acq_ext.get(session_id, 0) + 1
            return True
        return False

    def extended_acq_index(self, session_id: int, acq_index: int) -> int:
        return (self._acq_ext.get(session_id, 0) << 16) | acq_index
