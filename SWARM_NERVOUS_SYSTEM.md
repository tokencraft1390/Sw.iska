# SWL Swarm Nervous System

This layer extracts the useful machine-to-machine coordination idea from SWL without replacing domain execution logic.

## Boundary

SWL is the coordination bus, not the trading brain and not the signer.

```text
Onchain/RPC data
      |
      v
Scout agents
      |
      | 32-byte deterministic packets
      v
SWL swarm protocol
      |
      +--> risk gate
      +--> route scorer
      +--> simulation worker
      +--> oracle watcher
      +--> consensus/ranking
      |
      v
Execution candidate
      |
      v
Existing policy/approval/executor boundary
```

The protocol MUST NOT bypass health-factor validation, profitability gates, transaction simulation, policy approval, signing controls, or chain-specific execution rules.

## Why this exists

Revenue swarms frequently exchange tiny state transitions that do not require natural-language messages. Examples:

- `HF_LOW`
- `ORACLE_MOVE`
- `ROUTE_READY`
- `SIMULATION_OK`
- `PROFITABLE`
- `GAS_HIGH`
- `MEV_RISK_HIGH`
- `EXECUTION_CANDIDATE`
- `EXECUTION_BLOCKED`

Each event has a stable integer ID in `swarm_protocol/vocabulary.py`.

## Wire format

`swarm_protocol.protocol.Packet` is a fixed 32-byte network-order packet:

| Field | Bytes |
|---|---:|
| Magic (`SWL1`) | 4 |
| Version | 1 |
| Event ID | 2 |
| Flags | 1 |
| Sequence | 4 |
| Timestamp ns | 8 |
| Numeric value | 8 |
| CRC32 | 4 |
| Total | 32 |

The `value` field carries the event's primary numeric observation, for example health factor, expected net profit USD, gas cost USD, price divergence bps, or risk score. Rich evidence remains in the originating service or evidence store and can be referenced by higher-level systems.

## Example

```python
from swarm_protocol import Packet, RevenueEvent

packet = Packet(
    event=RevenueEvent.PROFITABLE,
    sequence=1842,
    value=23.71,
)
payload = packet.encode()
assert len(payload) == 32
```

UDP transport is available in `swarm_protocol/udp.py`. Production deployments can replace UDP with NATS, Redis Streams, Kafka, WebSocket, QUIC, or another transport while keeping the event vocabulary and packet semantics stable.

## Revenue swarm mapping

Recommended mapping for the liquidation/arbitrage stack:

1. Borrower scout emits `BORROWER_SEEN` and `HF_LOW`.
2. Oracle watcher emits `ORACLE_MOVE` or `PRICE_DIVERGENCE`.
3. Route builder emits `ROUTE_FOUND` / `ROUTE_READY`.
4. Simulator emits `SIMULATION_OK` / `SIMULATION_FAILED`.
5. Economics scorer emits `PROFITABLE`, `UNPROFITABLE`, `GAS_HIGH`, `FLASH_FEE_HIGH`, or `MEV_RISK_HIGH`.
6. Coordinator ranks only candidates with fresh required evidence.
7. Qualified candidates become `EXECUTION_CANDIDATE`.
8. Existing policy and signing boundaries decide `EXECUTION_APPROVED` or `EXECUTION_BLOCKED`.
9. Executor reports `EXECUTION_SENT`, `EXECUTION_CONFIRMED`, or `EXECUTION_REVERTED`.

## Safety invariants

- Event IDs are append-only after deployment.
- CRC failure means discard, never guess.
- Unknown versions and event IDs fail closed.
- Sequence numbers should be monotonic per producer.
- Consumers should enforce freshness independently from packet transport.
- `PROFITABLE` is evidence, not authorization.
- `EXECUTION_CANDIDATE` is not a signature instruction.
- Private keys and credentials never enter SWL packets.
- Signing remains isolated behind the existing execution policy gate.

## Next production hardening

- producer identity/authentication (HMAC or signatures)
- replay window and per-producer monotonic sequence enforcement
- evidence ID/hash field or side-channel correlation ID
- transport benchmarks against JSON and current agent messaging
- NATS/Redis adapter
- Aave scout adapter
- oracle watcher adapter
- profitability scorer adapter
- soak test at 100, 500, and 1,000 agents
