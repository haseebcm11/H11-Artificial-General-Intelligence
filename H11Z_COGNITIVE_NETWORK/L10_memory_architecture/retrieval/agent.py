"""retrieval: Memory retrieval and associative search.

Implements Maximum Inner Product Search (MIPS) and Cosine Similarity for dense vectors.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "retrieval"

class RetrievalError(ValueError): pass

@dataclass
class VectorRecord:
    id: str
    vector: List[float]
    norm: float = 0.0
    
    def __post_init__(self):
        self.norm = math.sqrt(sum(x*x for x in self.vector))

@dataclass
class RetrievalInput:
    query: List[float]
    top_k: int = 5
    method: str = "cosine" # or 'mips'
    threshold: float = 0.0

@dataclass
class RetrievalOutput:
    agent_id: str
    results: List[Dict[str, Any]]
    execution_time_ms: float

class RetrievalAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.database: List[VectorRecord] = []

    def insert(self, doc_id: str, vec: List[float]):
        self.database.append(VectorRecord(id=doc_id, vector=vec))

    def process(self, input_data: RetrievalInput) -> RetrievalOutput:
        start_time = time.perf_counter()
        
        q_norm = math.sqrt(sum(x*x for x in input_data.query))
        if q_norm == 0.0:
            raise RetrievalError("Query vector cannot have zero norm")
            
        scores = []
        for record in self.database:
            dot_product = sum(q*v for q, v in zip(input_data.query, record.vector))
            
            if input_data.method == "mips":
                score = dot_product
            elif input_data.method == "cosine":
                if record.norm == 0.0:
                    score = 0.0
                else:
                    score = dot_product / (q_norm * record.norm)
            else:
                raise RetrievalError(f"Unknown method {input_data.method}")
                
            if score >= input_data.threshold:
                scores.append({"id": record.id, "score": score})
                
        # Sort descending by score
        scores.sort(key=lambda x: x["score"], reverse=True)
        top_results = scores[:input_data.top_k]

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return RetrievalOutput(
            agent_id=AGENT_ID,
            results=top_results,
            execution_time_ms=elapsed_ms
        )
