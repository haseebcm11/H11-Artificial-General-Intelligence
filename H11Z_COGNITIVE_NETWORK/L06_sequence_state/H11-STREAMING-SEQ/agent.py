from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-STREAMING-SEQ"

class StreamingEvictionError(Exception):
    """Raised when eviction strategy violates state bounds."""
    pass

@dataclass
class StreamingInput:
    total_tokens: int
    sink_size: int = 4
    window_size: int = 512

@dataclass
class StreamingOutput:
    retained_indices: List[int]
    evicted_count: int

class StreamingAgent:
    """
    StreamingLLM KV eviction policy.
    Retains first 'sink_size' tokens as attention sinks, and recent 'window_size' tokens.
    """
    def process(self, req: StreamingInput) -> StreamingOutput:
        if req.sink_size < 0 or req.window_size < 0:
            raise StreamingEvictionError("Sink and window sizes must be non-negative")
            
        if req.total_tokens <= req.sink_size + req.window_size:
            return StreamingOutput(list(range(req.total_tokens)), 0)
            
        sinks = list(range(req.sink_size))
        window = list(range(req.total_tokens - req.window_size, req.total_tokens))
        
        retained = sinks + window
        evicted = req.total_tokens - len(retained)
        
        return StreamingOutput(
            retained_indices=retained,
            evicted_count=evicted
        )
