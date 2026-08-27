"""H11-MONTECARLO: Markov Chain Monte Carlo Engine.

Implements Metropolis-Hastings for sampling from an unnormalized target distribution.
"""
from __future__ import annotations
import math
import random
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

AGENT_ID = "H11-MONTECARLO"

class MonteCarloError(ValueError): pass

@dataclass
class MonteCarloInput:
    iterations: int = 1000
    burn_in: int = 200
    initial_state: float = 0.0
    step_size: float = 0.5

@dataclass
class MonteCarloOutput:
    agent_id: str
    mean: float
    variance: float
    acceptance_rate: float
    execution_time_ms: float

class MonteCarloAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def _target_pdf(self, x: float) -> float:
        # Example target: Standard Normal N(0,1) unnormalized
        return math.exp(-0.5 * x * x)

    def process(self, input_data: MonteCarloInput) -> MonteCarloOutput:
        start_time = time.perf_counter()
        
        current_x = input_data.initial_state
        samples = []
        accepted = 0
        
        for i in range(input_data.iterations):
            # Propose new state
            proposal_x = current_x + random.uniform(-input_data.step_size, input_data.step_size)
            
            # Acceptance ratio
            p_current = self._target_pdf(current_x)
            p_proposal = self._target_pdf(proposal_x)
            
            if p_current == 0:
                alpha = 1.0
            else:
                alpha = min(1.0, p_proposal / p_current)
                
            if random.random() < alpha:
                current_x = proposal_x
                accepted += 1
                
            if i >= input_data.burn_in:
                samples.append(current_x)
                
        n_samples = len(samples)
        if n_samples == 0:
            raise MonteCarloError("Zero samples after burn-in")
            
        mean = sum(samples) / n_samples
        variance = sum((x - mean)**2 for x in samples) / max(1, n_samples - 1)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return MonteCarloOutput(
            agent_id=AGENT_ID,
            mean=mean,
            variance=variance,
            acceptance_rate=accepted / input_data.iterations,
            execution_time_ms=elapsed_ms
        )
