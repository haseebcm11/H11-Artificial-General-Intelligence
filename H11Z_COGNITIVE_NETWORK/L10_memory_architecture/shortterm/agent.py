"""shortterm: Short-term Memory Buffer.

Implements a capacity-bound FIFO queue with time-based degradation tracking.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "shortterm"

class ShortTermError(ValueError): pass

@dataclass
class MemoryChunk:
    id: str
    content: str
    timestamp: float

@dataclass
class ShortTermInput:
    operation: str # 'push' or 'read'
    new_chunk: Optional[MemoryChunk] = None
    capacity: int = 7

@dataclass
class ShortTermOutput:
    agent_id: str
    active_items: int
    oldest_age_s: float
    execution_time_ms: float

class ShortTermAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.queue: List[MemoryChunk] = []

    def process(self, input_data: ShortTermInput) -> ShortTermOutput:
        start_time = time.perf_counter()
        current_time = time.time()
        
        if input_data.operation == "push" and input_data.new_chunk:
            self.queue.append(input_data.new_chunk)
            
            # Enforce capacity
            if len(self.queue) > input_data.capacity:
                self.queue.pop(0) # FIFO eviction
                
        oldest_age = 0.0
        if self.queue:
            oldest_age = current_time - self.queue[0].timestamp

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return ShortTermOutput(
            agent_id=AGENT_ID,
            active_items=len(self.queue),
            oldest_age_s=oldest_age,
            execution_time_ms=elapsed_ms
        )
