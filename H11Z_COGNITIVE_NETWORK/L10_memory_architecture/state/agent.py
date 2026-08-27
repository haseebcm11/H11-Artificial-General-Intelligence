"""state: Cognitive State machine modeling.

Implements Markov Decision Process (MDP) State Transition Matrix multiplication.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "state"

class StateError(ValueError): pass

@dataclass
class StateInput:
    current_distribution: List[float]
    transition_matrix: List[List[float]] # P(s' | s)

@dataclass
class StateOutput:
    agent_id: str
    next_distribution: List[float]
    entropy: float
    execution_time_ms: float

class StateAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: StateInput) -> StateOutput:
        start_time = time.perf_counter()
        
        curr = input_data.current_distribution
        trans = input_data.transition_matrix
        
        if len(curr) != len(trans):
            raise StateError("Vector/Matrix dimension mismatch")
            
        dim = len(curr)
        next_dist = [0.0] * dim
        
        # P(s') = sum_s P(s' | s) * P(s)
        # Note trans[s][s']
        for s in range(dim):
            for s_prime in range(dim):
                next_dist[s_prime] += curr[s] * trans[s][s_prime]
                
        # Calculate Shannon entropy
        import math
        entropy = 0.0
        for p in next_dist:
            if p > 0:
                entropy -= p * math.log2(p)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return StateOutput(
            agent_id=AGENT_ID,
            next_distribution=next_dist,
            entropy=entropy,
            execution_time_ms=elapsed_ms
        )
