import math
from dataclasses import dataclass
from typing import List, Dict

AGENT_ID = "H11-CACHE-INF"

@dataclass
class CacheInput:
    query_embedding: List[float]
    cache_keys: Dict[str, List[float]]
    threshold: float

@dataclass
class CacheOutput:
    hit_id: str
    max_similarity: float

class CacheException(Exception):
    pass

class H11CacheInfAgent:
    """
    Semantic caching using Cosine Similarity.
    sim = (A dot B) / (||A|| ||B||)
    """
    def process(self, input_data: CacheInput) -> CacheOutput:
        q = input_data.query_embedding
        q_norm = math.sqrt(sum(x*x for x in q))
        if q_norm == 0:
            raise CacheException("Zero query embedding vector")
            
        best_id = ""
        best_sim = -1.0
        
        for cid, k_vec in input_data.cache_keys.items():
            k_norm = math.sqrt(sum(x*x for x in k_vec))
            if k_norm == 0:
                continue
                
            dot = sum(x*y for x, y in zip(q, k_vec))
            sim = dot / (q_norm * k_norm)
            
            if sim > best_sim:
                best_sim = sim
                best_id = cid
                
        if best_sim >= input_data.threshold:
            return CacheOutput(hit_id=best_id, max_similarity=best_sim)
            
        return CacheOutput(hit_id="", max_similarity=best_sim)
