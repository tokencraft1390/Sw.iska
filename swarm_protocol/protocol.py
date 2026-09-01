from __future__ import annotations

from dataclasses import dataclass
import struct
import time
import zlib

from .vocabulary import RevenueEvent

MAGIC = b"SWL1"
VERSION = 1
_PACKET_NO_CRC = struct.Struct("!4sBHB I Q d")
_PACKET = struct.Struct("!4sBHB I Q d I")
PACKET_SIZE = _PACKET.size


class ProtocolError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class Packet:
    event: RevenueEvent
    sequence: int
    value: float = 0.0
    flags: int = 0
    timestamp_ns: int = 0

    def encode(self) -> bytes:
        ts = self.timestamp_ns or time.time_ns()
        if not 0 <= self.flags <= 0xFF:
            raise ProtocolError("flags must fit uint8")
        if not 0 <= self.sequence <= 0xFFFFFFFF:
            raise ProtocolError("sequence must fit uint32")

        body = _PACKET_NO_CRC.pack(
            MAGIC,
            VERSION,
            int(self.event),
            self.flags,
            self.sequence,
            ts,
            float(self.value),
        )
        crc = zlib.crc32(body) & 0xFFFFFFFF
        return body + struct.pack("!I", crc)

    @classmethod
    def decode(cls, payload: bytes) -> "Packet":
        if len(payload) != PACKET_SIZE:
            raise ProtocolError(f"invalid packet length: {len(payload)} != {PACKET_SIZE}")

        magic, version, event_id, flags, sequence, ts, value, expected_crc = _PACKET.unpack(payload)
        if magic != MAGIC:
            raise ProtocolError("bad magic")
        if version != VERSION:
            raise ProtocolError(f"unsupported version: {version}")

        actual_crc = zlib.crc32(payload[:-4]) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise ProtocolError("CRC mismatch")

        try:
            event = RevenueEvent(event_id)
        except ValueError as exc:
            raise ProtocolError(f"unknown event id: {event_id}") from exc

        return cls(event=event, sequence=sequence, value=value, flags=flags, timestamp_ns=ts)
