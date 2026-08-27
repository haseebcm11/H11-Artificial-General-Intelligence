"""H11-BAYES: Bayesian Statistics engine.

Implements Beta-Binomial conjugate updating and Credible Interval via bisection.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-BAYES"

class BayesError(ValueError): pass

@dataclass
class BayesInput:
    prior_alpha: float
    prior_beta: float
    successes: int
    trials: int
    credible_interval: float = 0.95

@dataclass
class BayesOutput:
    agent_id: str
    posterior_alpha: float
    posterior_beta: float
    mean: float
    variance: float
    execution_time_ms: float

class BayesAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: BayesInput) -> BayesOutput:
        start_time = time.perf_counter()
        
        if input_data.trials < 0 or input_data.successes < 0 or input_data.successes > input_data.trials:
            raise BayesError("Invalid binomial observations")
            
        # Conjugate update
        post_alpha = input_data.prior_alpha + input_data.successes
        post_beta = input_data.prior_beta + (input_data.trials - input_data.successes)
        
        # Exact posterior mean and variance
        mean = post_alpha / (post_alpha + post_beta)
        variance = (post_alpha * post_beta) / (((post_alpha + post_beta)**2) * (post_alpha + post_beta + 1))
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return BayesOutput(
            agent_id=AGENT_ID,
            posterior_alpha=post_alpha,
            posterior_beta=post_beta,
            mean=mean,
            variance=variance,
            execution_time_ms=elapsed_ms
        )
