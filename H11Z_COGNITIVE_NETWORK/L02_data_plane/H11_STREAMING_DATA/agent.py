"""H11_STREAMING_DATA: Real-time event windowing and temporal alignment.

Implements Stateful Tumbling Windows and Event-Time Watermarking.
Math: W_t = max(event_timestamps) - max_out_of_order_tolerance.
"""
import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_STREAMING_DATA"

class StreamingError(ValueError):
    """Domain-specific error for H11_STREAMING_DATA."""

class StreamingStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()

@dataclass(frozen=True)
class StreamEvent:
    event_id: str
    timestamp: float
    value: float

@dataclass(frozen=True)
class StreamingInput:
    events: List[StreamEvent] = field(default_factory=list)
    out_of_order_tolerance: float = 2.0  # seconds
    window_size: float = 5.0 # seconds

@dataclass(frozen=True)
class StreamingOutput:
    agent_id: str
    status: str
    current_watermark: float
    emitted_windows: Dict[int, float] # window_idx -> aggregated value
    late_dropped_events: int
    execution_time_ms: float
    diagnostics: Dict[str, float]

class StreamingdataAgent:
    """Analytical engine for Event-time watermarking and windowing."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.max_seen_time = 0.0
        self.window_state: Dict[int, List[float]] = {}

    def process(self, input_data: Optional[StreamingInput] = None) -> StreamingOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = StreamingInput()

        tol = input_data.out_of_order_tolerance
        w_size = input_data.window_size
        
        dropped = 0
        emitted = {}
        
        # 1. Update max seen time to advance watermark
        for ev in input_data.events:
            if ev.timestamp > self.max_seen_time:
                self.max_seen_time = ev.timestamp
                
        watermark = max(0.0, self.max_seen_time - tol)
        
        # 2. Assign events to windows
        for ev in input_data.events:
            if ev.timestamp < watermark:
                # Late data
                dropped += 1
                continue
                
            w_idx = int(ev.timestamp // w_size)
            if w_idx not in self.window_state:
                self.window_state[w_idx] = []
            self.window_state[w_idx].append(ev.value)
            
        # 3. Emit closed windows (where window end < watermark)
        active_windows = list(self.window_state.keys())
        for w_idx in active_windows:
            w_end = (w_idx + 1) * w_size
            if w_end <= watermark:
                # Close and aggregate (e.g. mean)
                vals = self.window_state.pop(w_idx)
                if vals:
                    emitted[w_idx] = sum(vals) / len(vals)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return StreamingOutput(
            agent_id=AGENT_ID,
            status=StreamingStatus.OPTIMAL.name,
            current_watermark=round(watermark, 4),
            emitted_windows={k: round(v, 4) for k, v in emitted.items()},
            late_dropped_events=dropped,
            execution_time_ms=round(elapsed_ms, 2),
            diagnostics={
                "max_seen_time": round(self.max_seen_time, 4),
                "active_windows_count": len(self.window_state)
            }
        )
