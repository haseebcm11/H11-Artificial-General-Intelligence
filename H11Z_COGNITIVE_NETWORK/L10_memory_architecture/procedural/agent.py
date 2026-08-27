"""procedural: Procedural Memory and Reinforcement Learning.

Implements Q-Learning Temporal Difference (TD) updates.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "procedural"

class ProceduralError(ValueError): pass

@dataclass
class ProceduralInput:
    state: str
    action: str
    reward: float
    next_state: str
    available_actions: List[str]
    alpha: float = 0.1
    gamma: float = 0.9

@dataclass
class ProceduralOutput:
    agent_id: str
    td_error: float
    updated_q_value: float
    execution_time_ms: float

class ProceduralAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.q_table: Dict[str, Dict[str, float]] = {}

    def _get_q(self, s: str, a: str) -> float:
        if s not in self.q_table:
            self.q_table[s] = {}
        return self.q_table[s].get(a, 0.0)

    def process(self, input_data: ProceduralInput) -> ProceduralOutput:
        start_time = time.perf_counter()
        
        s = input_data.state
        a = input_data.action
        r = input_data.reward
        s_next = input_data.next_state
        
        current_q = self._get_q(s, a)
        
        # Max Q over next state
        max_next_q = max([self._get_q(s_next, n_a) for n_a in input_data.available_actions], default=0.0)
        
        # TD Target and Error
        target = r + input_data.gamma * max_next_q
        td_error = target - current_q
        
        # Update
        new_q = current_q + input_data.alpha * td_error
        
        if s not in self.q_table:
            self.q_table[s] = {}
        self.q_table[s][a] = new_q

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return ProceduralOutput(
            agent_id=AGENT_ID,
            td_error=td_error,
            updated_q_value=new_q,
            execution_time_ms=elapsed_ms
        )
