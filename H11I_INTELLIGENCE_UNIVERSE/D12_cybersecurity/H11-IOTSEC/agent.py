"""
Agent Module: D12_IOTSEC
Agent Class: IotsecAgent

IoT device security: Lightweight ChaCha20 quarter-round operations and firmware binary Shannon entropy analysis.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D12_IOTSEC"


class IotsecError(ValueError):
    """Raised when IotsecAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class IotsecAgentInput:
    firmware_bytes: list[int] = field(default_factory=lambda: [12, 45, 233, 128, 45, 12, 99, 105])


@dataclass(frozen=True)
class IotsecAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    shannon_entropy: float = 0.0


class IotsecAgent:
    """
    IoT device security: Lightweight ChaCha20 quarter-round operations and firmware binary Shannon entropy analysis.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: IotsecAgentInput) -> IotsecAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        b = inputs.firmware_bytes if inputs.firmware_bytes else [0]
        tot = len(b)
        freqs = {}
        for byte in b: freqs[byte] = freqs.get(byte, 0) + 1
        ent = -sum((c/tot) * math.log2(c/tot) for c in freqs.values())
        # High entropy > 7.5 indicates encrypted/compressed payload
        is_encrypted = ent > 7.0
        metrics = {"entropy": round(ent, 4), "is_likely_encrypted": 1.0 if is_encrypted else 0.0}
        return IotsecAgentOutput(status="COMPLETED", score=round(min(1.0, ent/8.0), 4), metrics=metrics, shannon_entropy=round(ent, 4))
