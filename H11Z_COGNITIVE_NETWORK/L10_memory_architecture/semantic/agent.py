"""semantic: Semantic network and Knowledge graph processing.

Implements graph node distance and activation spreading.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "semantic"

class SemanticError(ValueError): pass

@dataclass
class SemanticInput:
    source_node: str
    target_node: str
    max_depth: int = 3

@dataclass
class SemanticOutput:
    agent_id: str
    distance: int
    activation_strength: float
    execution_time_ms: float

class SemanticAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        # Simple adjacency list for knowledge graph
        self.graph = {
            "animal": ["cat", "dog", "bird"],
            "cat": ["feline", "animal", "pet"],
            "dog": ["canine", "animal", "pet"],
            "pet": ["cat", "dog"],
            "bird": ["animal", "flying"]
        }

    def process(self, input_data: SemanticInput) -> SemanticOutput:
        start_time = time.perf_counter()
        
        # BFS for shortest path
        queue = [(input_data.source_node, 0)]
        visited = set([input_data.source_node])
        
        found_dist = -1
        while queue:
            current, dist = queue.pop(0)
            if current == input_data.target_node:
                found_dist = dist
                break
                
            if dist < input_data.max_depth:
                neighbors = self.graph.get(current, [])
                for n in neighbors:
                    if n not in visited:
                        visited.add(n)
                        queue.append((n, dist + 1))
                        
        strength = 0.0
        if found_dist != -1:
            # Exponential decay based on semantic distance
            strength = 1.0 / (2 ** found_dist)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return SemanticOutput(
            agent_id=AGENT_ID,
            distance=found_dist,
            activation_strength=strength,
            execution_time_ms=elapsed_ms
        )
