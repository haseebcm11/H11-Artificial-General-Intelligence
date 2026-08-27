"""consolidate: Memory consolidation and sleep phase processing.

Implements exponential activation thresholding for short-to-long term transfer.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "consolidate"

class ConsolidateError(ValueError): pass

@dataclass
class ConsolidateInput:
    memory_traces: List[Dict[str, float]] # dict of memory_id -> activation_strength
    threshold_base: float = 0.6
    sleep_depth: float = 0.8

@dataclass
class ConsolidateOutput:
    agent_id: str
    consolidated_ids: List[str]
    pruned_ids: List[str]
    execution_time_ms: float

class ConsolidateAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: ConsolidateInput) -> ConsolidateOutput:
        start_time = time.perf_counter()
        
        dynamic_threshold = input_data.threshold_base * math.exp(-input_data.sleep_depth)
        
        consolidated = []
        pruned = []
        
        for m_id, strength in input_data.memory_traces.items():
            # Apply non-linear synaptic scaling
            scaled_strength = strength ** (1.0 / max(0.1, input_data.sleep_depth))
            
            if scaled_strength >= dynamic_threshold:
                consolidated.append(m_id)
            else:
                pruned.append(m_id)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return ConsolidateOutput(
            agent_id=AGENT_ID,
            consolidated_ids=consolidated,
            pruned_ids=pruned,
            execution_time_ms=elapsed_ms
        )
