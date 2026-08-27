"""longterm: Long-term Storage and Vector Quantization.

Implements K-Means centroid assignment for latent space quantization.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "longterm"

class LongtermError(ValueError): pass

@dataclass
class LongtermInput:
    vector: List[float]
    centroids: List[List[float]]

@dataclass
class LongtermOutput:
    agent_id: str
    assigned_cluster: int
    quantization_error: float
    execution_time_ms: float

class LongtermAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: LongtermInput) -> LongtermOutput:
        start_time = time.perf_counter()
        
        if not input_data.centroids or not input_data.vector:
            raise LongtermError("Vectors and centroids required")
            
        best_cluster = -1
        min_dist = float('inf')
        
        for idx, centroid in enumerate(input_data.centroids):
            dist_sq = sum((v - c)**2 for v, c in zip(input_data.vector, centroid))
            if dist_sq < min_dist:
                min_dist = dist_sq
                best_cluster = idx

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return LongtermOutput(
            agent_id=AGENT_ID,
            assigned_cluster=best_cluster,
            quantization_error=math.sqrt(min_dist),
            execution_time_ms=elapsed_ms
        )
