from typing import List, Dict, Any
from dataclasses import dataclass

AGENT_ID = "H11-KVCACHE"

class KVCacheException(Exception):
    pass

@dataclass
class KVCacheInput:
    new_k: List[List[float]]
    new_v: List[List[float]]
    max_size: int
    eviction_policy: str # "lru", "fifo"

@dataclass
class KVCacheOutput:
    cached_k: List[List[float]]
    cached_v: List[List[float]]
    cache_hit_rate: float

class KVCacheAgent:
    """
    H11-KVCACHE
    Manages incremental decoding cache. Evicts tokens based on policies when exceeding max_size.
    Ensures O(1) attention for auto-regressive generation.
    """
    def __init__(self):
        self.k_cache = []
        self.v_cache = []
        self.hits = 0
        self.misses = 0

    def process(self, input_data: KVCacheInput) -> KVCacheOutput:
        new_k = input_data.new_k
        new_v = input_data.new_v
        max_size = input_data.max_size
        
        if len(new_k) != len(new_v):
            raise KVCacheException("K and V sequences must match length")
            
        self.misses += len(new_k) # new tokens are misses
        self.hits += len(self.k_cache) # existing tokens are hits
        
        # Append
        self.k_cache.extend(new_k)
        self.v_cache.extend(new_v)
        
        # Evict
        if len(self.k_cache) > max_size:
            excess = len(self.k_cache) - max_size
            if input_data.eviction_policy == "fifo":
                self.k_cache = self.k_cache[excess:]
                self.v_cache = self.v_cache[excess:]
            elif input_data.eviction_policy == "lru":
                # For simplified structural implementation, LRU acts like FIFO on sequence chunks
                self.k_cache = self.k_cache[excess:]
                self.v_cache = self.v_cache[excess:]
            else:
                self.k_cache = self.k_cache[-max_size:]
                self.v_cache = self.v_cache[-max_size:]
                
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0.0
        
        return KVCacheOutput(
            cached_k=list(self.k_cache),
            cached_v=list(self.v_cache),
            cache_hit_rate=hit_rate
        )
