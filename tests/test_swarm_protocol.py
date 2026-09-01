import unittest

from swarm_protocol import Packet, ProtocolError, RevenueEvent
from swarm_protocol.protocol import PACKET_SIZE


class PacketTests(unittest.TestCase):
    def test_round_trip(self):
        original = Packet(
            event=RevenueEvent.PROFITABLE,
            sequence=42,
            value=18.75,
            flags=3,
            timestamp_ns=123456789,
        )
        payload = original.encode()
        self.assertEqual(len(payload), PACKET_SIZE)
        self.assertEqual(Packet.decode(payload), original)

    def test_crc_rejects_corruption(self):
        payload = bytearray(Packet(RevenueEvent.HF_LOW, 1, 0.98, timestamp_ns=1).encode())
        payload[10] ^= 0x01
        with self.assertRaises(ProtocolError):
            Packet.decode(bytes(payload))

    def test_unknown_event_is_rejected(self):
        payload = bytearray(Packet(RevenueEvent.READY, 7, timestamp_ns=1).encode())
        payload[5:7] = (65535).to_bytes(2, "big")

        import zlib
        crc = zlib.crc32(payload[:-4]) & 0xFFFFFFFF
        payload[-4:] = crc.to_bytes(4, "big")

        with self.assertRaises(ProtocolError):
            Packet.decode(bytes(payload))


if __name__ == "__main__":
    unittest.main()
