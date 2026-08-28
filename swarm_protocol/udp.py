from __future__ import annotations

import socket
from typing import Callable

from .protocol import PACKET_SIZE, Packet


class UDPSender:
    def __init__(self, host: str, port: int):
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, packet: Packet) -> int:
        return self.socket.sendto(packet.encode(), self.address)

    def close(self) -> None:
        self.socket.close()


class UDPReceiver:
    def __init__(self, host: str, port: int, timeout: float = 0.25):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        self.socket.settimeout(timeout)

    def receive_once(self) -> Packet:
        payload, _ = self.socket.recvfrom(PACKET_SIZE)
        return Packet.decode(payload)

    def serve(self, handler: Callable[[Packet], None]) -> None:
        while True:
            try:
                handler(self.receive_once())
            except socket.timeout:
                continue

    def close(self) -> None:
        self.socket.close()
