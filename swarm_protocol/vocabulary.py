from enum import IntEnum


class RevenueEvent(IntEnum):
    """Stable machine-readable event IDs for revenue-oriented agent swarms.

    IDs are append-only. Never renumber an existing value once deployed.
    """

    HEARTBEAT = 1
    READY = 2
    STALE = 3
    ERROR = 4

    BORROWER_SEEN = 100
    HF_LOW = 101
    HF_RECOVERED = 102
    ORACLE_MOVE = 103
    PRICE_DIVERGENCE = 104

    ROUTE_FOUND = 200
    ROUTE_READY = 201
    ROUTE_REJECTED = 202
    SIMULATION_OK = 203
    SIMULATION_FAILED = 204

    PROFITABLE = 300
    UNPROFITABLE = 301
    GAS_HIGH = 302
    GAS_OK = 303
    FLASH_FEE_HIGH = 304
    MEV_RISK_HIGH = 305

    EXECUTION_CANDIDATE = 400
    EXECUTION_BLOCKED = 401
    EXECUTION_APPROVED = 402
    EXECUTION_SENT = 403
    EXECUTION_CONFIRMED = 404
    EXECUTION_REVERTED = 405

    CONSENSUS_PROPOSE = 500
    CONSENSUS_ACCEPT = 501
    CONSENSUS_REJECT = 502
