from __future__ import annotations

import os
import struct
import subprocess
import tempfile
import unittest
from pathlib import Path

from elicio.frame_v2 import (
    FRAME_V2_GAIN,
    FRAME_V2_SAMPLE_BYTES,
    BatteryFrame,
    DecodeError,
    Flag,
    HelloFrame,
    MsgType,
    Reassembler,
    StopReason,
    StreamMeta,
    crc32,
    fragment,
    pack_battery,
    pack_hello,
    pack_stream,
    samples_for_nus,
    unpack_battery,
    unpack_hello,
    unpack_stream,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "frame_v2"
NATIVE_SRC = ROOT / "tests" / "native" / "framer_cli.c"
FIRMWARE_SRC = ROOT / "firmware" / "src"


def _sample(n: int, seed: int = 1) -> bytes:
    out = bytearray()
    for i in range(n):
        status = 0xC00000 + i
        ch1 = seed * 17 + i
        ch2 = seed * 31 + i
        out += bytes([(status >> 16) & 0xFF, (status >> 8) & 0xFF, status & 0xFF])
        out += bytes([(ch1 >> 16) & 0xFF, (ch1 >> 8) & 0xFF, ch1 & 0xFF])
        out += bytes([(ch2 >> 16) & 0xFF, (ch2 >> 8) & 0xFF, ch2 & 0xFF])
    return bytes(out)


def _meta(count: int, acq: int = 0, seq: int = 1, flags: int = 0) -> StreamMeta:
    return StreamMeta(
        session_id=7,
        frame_seq=seq,
        acq_index=acq & 0xFFFF,
        sample_count=count,
        flags=flags,
        stop_reason=StopReason.NONE,
    )


def _write_u16(value: int) -> bytes:
    return struct.pack("<H", value)


def compile_cli() -> Path:
    clang = os.environ.get("CLANG", "clang")
    tmp = Path(tempfile.mkdtemp(prefix="frame_v2_"))
    binary = tmp / "framer_cli"
    cmd = [
        clang,
        "-std=c11",
        "-O0",
        "-I",
        str(FIRMWARE_SRC),
        str(FIRMWARE_SRC / "frame_v2.c"),
        str(FIRMWARE_SRC / "undervoltage.c"),
        str(FIRMWARE_SRC / "ads1292.c"),
        str(NATIVE_SRC),
        "-o",
        str(binary),
    ]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return binary


CLI = compile_cli()


def native(payload: bytes) -> bytes:
    proc = subprocess.run([str(CLI)], input=payload, capture_output=True, check=False)
    if proc.returncode != 0:
        raise AssertionError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout


def native_pack_stream(meta: StreamMeta, samples: bytes) -> bytes:
    blob = (
        bytes([1])
        + _write_u16(meta.session_id)
        + _write_u16(meta.frame_seq)
        + _write_u16(meta.acq_index)
        + _write_u16(meta.sample_count)
        + bytes(
            [
                meta.flags,
                meta.stop_reason,
                meta.gain,
                meta.rate_id,
                meta.vref_id,
                meta.sample_bytes,
            ]
        )
        + _write_u16(meta.payload_bytes)
        + samples
    )
    return native(blob)


def native_fragment(msg: int, session: int, seq: int, nus: int, logical: bytes) -> list[bytes]:
    blob = bytes([4, msg]) + _write_u16(session) + _write_u16(seq) + _write_u16(nus) + logical
    out = native(blob)
    count = out[0]
    pos = 1
    packets = []
    for _ in range(count):
        (length,) = struct.unpack_from("<H", out, pos)
        pos += 2
        packets.append(out[pos : pos + length])
        pos += length
    return packets


def fixture(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


class FrameV2ContractTests(unittest.TestCase):
    def test_normal_round_trip_python_and_c(self) -> None:
        samples = _sample(4)
        meta = _meta(4, acq=10, seq=3)
        logical = pack_stream(meta, samples)
        self.assertEqual(logical, fixture("normal.bin"))
        self.assertEqual(native_pack_stream(meta, samples), logical)
        decoded = unpack_stream(logical)
        self.assertEqual(decoded.meta.acq_index, 10)
        self.assertEqual(decoded.samples, samples)
        self.assertEqual(crc32(logical[:-4]), struct.unpack_from("<I", logical, len(logical) - 4)[0])

    def test_wrap_acq_index(self) -> None:
        samples = _sample(2, seed=2)
        meta = _meta(2, acq=65534, seq=9)
        logical = pack_stream(meta, samples)
        self.assertEqual(logical, fixture("wrap.bin"))
        self.assertEqual(native_pack_stream(meta, samples), logical)
        recv = Reassembler()
        for pkt in fragment(MsgType.STREAM, 7, 9, logical, 244):
            recv.push(pkt)
        next_meta = _meta(2, acq=1, seq=10)
        next_logical = pack_stream(next_meta, samples)
        events = []
        for pkt in fragment(MsgType.STREAM, 7, 10, next_logical, 244):
            events.extend(recv.push(pkt))
        kinds = [e[0] for e in events if isinstance(e, tuple)]
        self.assertIn("wrap", kinds)
        self.assertEqual(recv.extended_acq_index(7, 1), (1 << 16) | 1)

    def test_fragment_small_mtu(self) -> None:
        samples = _sample(3, seed=3)
        meta = _meta(3, acq=20, seq=4)
        logical = pack_stream(meta, samples)
        packets = fragment(MsgType.STREAM, 7, 4, logical, 20)
        self.assertGreater(len(packets), 1)
        self.assertEqual(b"".join(struct.pack("<H", len(p)) + p for p in packets), fixture("fragment.bin"))
        native_packets = native_fragment(MsgType.STREAM, 7, 4, 20, logical)
        self.assertEqual(native_packets, packets)
        recv = Reassembler()
        out = []
        for pkt in packets:
            out.extend(recv.push(pkt))
        frames = [m for m in out if hasattr(m, "samples")]
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].samples, samples)

    def test_reorder_fragments(self) -> None:
        samples = _sample(3, seed=4)
        logical = pack_stream(_meta(3, acq=30, seq=5), samples)
        packets = fragment(MsgType.STREAM, 7, 5, logical, 20)
        self.assertGreater(len(packets), 2)
        recv = Reassembler()
        out = []
        for pkt in reversed(packets):
            out.extend(recv.push(pkt))
        frames = [m for m in out if hasattr(m, "samples")]
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].samples, samples)
        self.assertEqual((FIXTURES / "reorder.bin").read_bytes(), b"".join(reversed(packets)))
        samples = _sample(1, seed=5)
        recv = Reassembler()
        first = pack_stream(_meta(1, acq=0, seq=1), samples)
        third = pack_stream(_meta(1, acq=2, seq=3), samples)
        recv.push(fragment(MsgType.STREAM, 7, 1, first, 244)[0])
        events = recv.push(fragment(MsgType.STREAM, 7, 3, third, 244)[0])
        self.assertIn(("transport_loss", 2, 3), events)
        self.assertEqual((FIXTURES / "loss.bin").read_bytes()[: len(first)], first)

    def test_overrun_flag(self) -> None:
        samples = _sample(1, seed=6)
        logical = pack_stream(_meta(1, acq=40, seq=6, flags=Flag.OVERRUN), samples)
        self.assertEqual(logical, fixture("overrun.bin"))
        recv = Reassembler()
        events = recv.push(fragment(MsgType.STREAM, 7, 6, logical, 244)[0])
        self.assertTrue(any(e == ("overrun", 40) for e in events if isinstance(e, tuple)))

    def test_partial_frame_rejected(self) -> None:
        samples = _sample(3, seed=7)
        logical = pack_stream(_meta(3, acq=50, seq=8), samples)
        packets = fragment(MsgType.STREAM, 7, 8, logical, 20)
        recv = Reassembler()
        self.assertEqual(recv.push(packets[0]), [])
        self.assertEqual((FIXTURES / "partial.bin").read_bytes(), packets[0])
        with self.assertRaises(DecodeError) as ctx:
            recv.push(packets[0][:4])
        self.assertEqual(ctx.exception.code, "partial_frame")

    def test_reconnect_hello_resets_session_seq(self) -> None:
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
        self.assertEqual(hello, fixture("reconnect.bin"))
        native_hello = native(
            bytes([2])
            + _write_u16(9)
            + _write_u16(9)
            + _write_u16(12)
            + _write_u16(244)
            + bytes([0, StopReason.RESET, FRAME_V2_GAIN, 0, 0, FRAME_V2_SAMPLE_BYTES])
            + _write_u16(0)
        )
        self.assertEqual(native_hello, hello)
        recv = Reassembler()
        events = recv.push(fragment(MsgType.HELLO, 9, 0, hello, 244)[0])
        self.assertTrue(any(e == ("reconnect", 9) for e in events if isinstance(e, tuple)))
        decoded = unpack_hello(hello)
        self.assertEqual(decoded.nus_payload, 244)

    def test_bad_crc(self) -> None:
        samples = _sample(1, seed=8)
        logical = bytearray(pack_stream(_meta(1, acq=60, seq=11), samples))
        logical[-1] ^= 0xFF
        bad = bytes(logical)
        self.assertEqual(bad, fixture("bad_crc.bin"))
        with self.assertRaises(DecodeError) as ctx:
            unpack_stream(bad)
        self.assertEqual(ctx.exception.code, "bad_crc")

    def test_version_mismatch(self) -> None:
        packet = bytes([1, MsgType.STREAM, 7, 0, 1, 0, 0, 1]) + b"x"
        self.assertEqual(packet, fixture("version_mismatch.bin"))
        recv = Reassembler()
        with self.assertRaises(DecodeError) as ctx:
            recv.push(packet)
        self.assertEqual(ctx.exception.code, "version_mismatch")

    def test_battery_every_message_round_trips(self) -> None:
        frame = BatteryFrame(7, 2, 3710, Flag.VBUS, StopReason.VBUS, 0)
        logical = pack_battery(frame)
        self.assertEqual(unpack_battery(logical), frame)
        native_logical = native(
            bytes([3])
            + _write_u16(7)
            + _write_u16(2)
            + _write_u16(3710)
            + bytes([Flag.VBUS, StopReason.VBUS, 0, 0, 0, 0])
        )
        self.assertEqual(native_logical, logical)

    def test_undervoltage_machine_in_c(self) -> None:
        # board-v2.md §6: V_STOP 3.00 V, V_START 3.20 V.
        run = native(bytes([5]) + _write_u16(3001) + bytes([0]))
        self.assertEqual(run[0], 0)
        stop = native(bytes([5]) + _write_u16(3000) + bytes([0]))
        self.assertEqual(stop[0], 1)
        self.assertTrue(stop[1] & Flag.STOPPED)
        self.assertEqual(stop[2], StopReason.UNDERVOLTAGE)
        held = native(bytes([5]) + _write_u16(3000) + bytes([0]) + _write_u16(3199) + bytes([0]))
        self.assertEqual(held[3], 1)
        resume = native(bytes([5]) + _write_u16(3000) + bytes([0]) + _write_u16(3200) + bytes([0]))
        self.assertEqual(resume[3], 0)
        self.assertTrue(resume[4] & Flag.RESTART)
        vbus = native(bytes([5]) + _write_u16(4000) + bytes([1]))
        self.assertEqual(vbus[2], StopReason.VBUS)
        self.assertTrue(vbus[1] & Flag.VBUS)

    def test_ads1292_worn_register_set(self) -> None:
        dump = native(bytes([6]))
        count = dump[0]
        regs = {dump[1 + 2 * i]: dump[2 + 2 * i] for i in range(count)}
        self.assertEqual(regs[0x01], 0x04)
        self.assertEqual(regs[0x02], 0xA0)
        self.assertEqual(regs[0x04], 0x60)  # gain 12, normal input
        self.assertEqual(regs[0x05], 0x81)  # unused channel 2 powered down, input short
        self.assertEqual(regs[0x06], 0x23)
        self.assertEqual(regs[0x07], 0x00)
        self.assertEqual(regs[0x09], 0x02)
        self.assertEqual(regs[0x0A], 0x07)  # RESP_FREQ and bit 0 must be 1 (SBAS502C 8.6.1.11)

    def test_samples_for_nus_prefers_one_fragment(self) -> None:
        self.assertEqual(samples_for_nus(20), 1)
        self.assertGreaterEqual(samples_for_nus(244), 20)


if __name__ == "__main__":
    unittest.main()
