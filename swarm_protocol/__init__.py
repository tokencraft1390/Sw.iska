"""Compact deterministic coordination protocol for SWL-powered agent swarms."""

from .protocol import Packet, ProtocolError
from .vocabulary import RevenueEvent

__all__ = ["Packet", "ProtocolError", "RevenueEvent"]
