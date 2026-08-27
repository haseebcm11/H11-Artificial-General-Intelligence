"""H11-DATASTRUCTURA: Domain-specific agent for Computer Science.

D11_computer_science - Universe

Implements Big-O complexity estimation, hash table load factor, B-tree height log_m(n), TCP congestion window limit.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

AGENT_ID = "H11-DATASTRUCTURA"

class DataStructuraError(ValueError):
    """Domain-specific error for H11-DATASTRUCTURA."""
    pass

@dataclass(frozen=True)
class DataStructuraInput:
    elements: Optional[int] = None
    hash_table_size: Optional[int] = None
    hash_table_elements: Optional[int] = None
    btree_order: Optional[int] = None
    btree_nodes: Optional[int] = None
    tcp_mss: Optional[int] = None
    tcp_cwnd_segments: Optional[int] = None

@dataclass(frozen=True)
class DataStructuraOutput:
    agent_id: str
    status: str
    big_o_nlogn: Optional[float] = None
    hash_load_factor: Optional[float] = None
    btree_max_height: Optional[int] = None
    tcp_cwnd_bytes: Optional[int] = None
    execution_time_ms: float

class DataStructuraAgent:
    """Agent for computer science data structure metrics and complexity."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: DataStructuraInput) -> DataStructuraOutput:
        start_time = time.perf_counter()
        
        big_o = None
        load_factor = None
        height = None
        cwnd = None
        
        if input_data.elements is not None:
            n = input_data.elements
            if n > 0:
                big_o = n * math.log2(n)
                
        if input_data.hash_table_size is not None and input_data.hash_table_elements is not None:
            size = input_data.hash_table_size
            if size <= 0:
                raise DataStructuraError("Hash table size must be > 0")
            load_factor = input_data.hash_table_elements / size
            
        if input_data.btree_order is not None and input_data.btree_nodes is not None:
            m = input_data.btree_order
            n = input_data.btree_nodes
            if m < 2:
                raise DataStructuraError("B-tree order must be >= 2")
            if n > 0:
                # Max height of B-tree is log_{m/2}( (n+1)/2 ) but simplified here to log_m(n) as requested
                height = math.ceil(math.log(n, m))
                
        if input_data.tcp_mss is not None and input_data.tcp_cwnd_segments is not None:
            cwnd = input_data.tcp_mss * input_data.tcp_cwnd_segments

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return DataStructuraOutput(
            agent_id=AGENT_ID,
            status="SUCCESS",
            big_o_nlogn=big_o,
            hash_load_factor=load_factor,
            btree_max_height=height,
            tcp_cwnd_bytes=cwnd,
            execution_time_ms=round(elapsed_ms, 4)
        )
