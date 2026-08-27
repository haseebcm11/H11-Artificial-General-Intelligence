"""forget: Memory eviction and decay management.

Implements Least Recently Used (LRU) eviction and cache capacity bounds.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "forget"

class ForgetError(ValueError): pass

@dataclass
class MemoryItem:
    key: str
    last_accessed: float
    access_count: int = 1

@dataclass
class ForgetInput:
    accessed_keys: List[str]
    capacity: int = 1000

@dataclass
class ForgetOutput:
    agent_id: str
    evicted_keys: List[str]
    current_size: int
    execution_time_ms: float

class ForgetAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        # Simple OrderedDict simulation for LRU
        self.cache_meta: Dict[str, MemoryItem] = {}

    def process(self, input_data: ForgetInput) -> ForgetOutput:
        start_time = time.perf_counter()
        
        current_time = time.time()
        
        # Update access times
        for key in input_data.accessed_keys:
            if key in self.cache_meta:
                self.cache_meta[key].last_accessed = current_time
                self.cache_meta[key].access_count += 1
            else:
                self.cache_meta[key] = MemoryItem(key=key, last_accessed=current_time)
                
        evicted = []
        # Check capacity and evict LRU
        if len(self.cache_meta) > input_data.capacity:
            # Sort by last_accessed ascending (oldest first)
            sorted_items = sorted(self.cache_meta.values(), key=lambda x: x.last_accessed)
            num_to_evict = len(self.cache_meta) - input_data.capacity
            
            for item in sorted_items[:num_to_evict]:
                evicted.append(item.key)
                del self.cache_meta[item.key]

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return ForgetOutput(
            agent_id=AGENT_ID,
            evicted_keys=evicted,
            current_size=len(self.cache_meta),
            execution_time_ms=elapsed_ms
        )
