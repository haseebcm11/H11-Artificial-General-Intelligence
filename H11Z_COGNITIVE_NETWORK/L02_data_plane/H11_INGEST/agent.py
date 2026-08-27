"""H11_INGEST: Multi-source raw data ingestion with backpressure.

Implements Token Bucket algorithm with Additive Increase Multiplicative Decrease 
(AIMD) flow control for dynamic backpressure handling.
Math: tokens = min(capacity, tokens + rate * dt)
"""
import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_INGEST"

class IngestError(ValueError):
    """Domain-specific error for H11_INGEST."""

class IngestStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()
    THROTTLED = auto()

@dataclass(frozen=True)
class IngestInput:
    incoming_payloads: List[int] = field(default_factory=list) # bytes per payload
    time_delta_sec: float = 1.0
    congestion_signal: bool = False

@dataclass(frozen=True)
class IngestOutput:
    agent_id: str
    status: str
    accepted_payloads: int
    dropped_payloads: int
    current_rate: float
    execution_time_ms: float
    diagnostics: Dict[str, float]

class IngestAgent:
    """Analytical engine for Token Bucket and AIMD backpressure."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.capacity = float(self.config.get("bucket_capacity", 1000000.0)) # 1MB
        self.rate = float(self.config.get("initial_rate", 500000.0)) # 500KB/s
        self.tokens = self.capacity
        self.additive_step = 50000.0
        self.multiplicative_factor = 0.5

    def _aimd_adjust(self, congestion: bool):
        """Additive Increase, Multiplicative Decrease."""
        if congestion:
            self.rate = max(1000.0, self.rate * self.multiplicative_factor)
        else:
            self.rate = min(self.capacity * 10, self.rate + self.additive_step)

    def process(self, input_data: Optional[IngestInput] = None) -> IngestOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = IngestInput()

        # Update AIMD rate based on congestion signal
        self._aimd_adjust(input_data.congestion_signal)

        # Replenish tokens
        replenish = self.rate * input_data.time_delta_sec
        self.tokens = min(self.capacity, self.tokens + replenish)

        accepted = 0
        dropped = 0
        
        for payload_size in input_data.incoming_payloads:
            if payload_size <= self.tokens:
                self.tokens -= payload_size
                accepted += 1
            else:
                dropped += 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        
        status = IngestStatus.THROTTLED if input_data.congestion_signal or dropped > 0 else IngestStatus.OPTIMAL

        return IngestOutput(
            agent_id=AGENT_ID,
            status=status.name,
            accepted_payloads=accepted,
            dropped_payloads=dropped,
            current_rate=round(self.rate, 2),
            execution_time_ms=round(elapsed_ms, 2),
            diagnostics={
                "bucket_tokens_remaining": round(self.tokens, 2),
                "aimd_rate": round(self.rate, 2)
            }
        )
