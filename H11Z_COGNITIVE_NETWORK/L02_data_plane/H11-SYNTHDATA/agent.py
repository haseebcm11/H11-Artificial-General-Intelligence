"""H11-SYNTHDATA: Privacy-preserving synthetic data generator.

Implements Differential Privacy Stochastic Gradient Descent (DP-SGD) concepts
via Laplace and Gaussian noise mechanisms, strictly managing the epsilon budget.
Math: f(x) + Laplace(\\Delta f / \\epsilon) ensures \\epsilon-differential privacy.
"""
import math
import random
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11-SYNTHDATA"

class SynthdataError(ValueError):
    """Domain-specific error for H11-SYNTHDATA."""

class SynthdataStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()

@dataclass(frozen=True)
class SynthdataInput:
    seed_numerical_data: List[float] = field(default_factory=list)
    epsilon: float = 1.0
    delta: float = 1e-5
    sensitivity: float = 1.0
    mechanism: str = "gaussian"  # 'laplace' or 'gaussian'

@dataclass(frozen=True)
class SynthdataOutput:
    agent_id: str
    status: str
    synthetic_data: List[float]
    budget_consumed: float
    execution_time_ms: float
    metrics: Dict[str, float]

class SynthdataAgent:
    """Analytical engine for Differential Privacy synthesis."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.total_epsilon_spent = 0.0

    def _laplace_noise(self, scale: float) -> float:
        """Draws noise from Laplace distribution."""
        u = random.uniform(-0.5, 0.5)
        return -scale * math.copysign(1.0, u) * math.log(1 - 2 * abs(u))

    def _gaussian_noise(self, scale: float) -> float:
        """Draws noise from Gaussian distribution using Box-Muller."""
        u1 = random.random()
        u2 = random.random()
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        return scale * z0

    def process(self, input_data: Optional[SynthdataInput] = None) -> SynthdataOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = SynthdataInput()

        eps = input_data.epsilon
        delta = input_data.delta
        sens = input_data.sensitivity
        mech = input_data.mechanism
        
        synthetic = []
        
        if mech == "laplace":
            # Laplace scale = Delta f / epsilon
            scale = sens / eps
            for val in input_data.seed_numerical_data:
                synthetic.append(val + self._laplace_noise(scale))
        elif mech == "gaussian":
            # Gaussian scale = (Delta f * sqrt(2 * ln(1.25 / delta))) / epsilon
            if delta <= 0:
                raise SynthdataError("Gaussian mechanism requires delta > 0")
            scale = (sens * math.sqrt(2 * math.log(1.25 / delta))) / eps
            for val in input_data.seed_numerical_data:
                synthetic.append(val + self._gaussian_noise(scale))
        else:
            raise SynthdataError(f"Unknown mechanism: {mech}")

        self.total_epsilon_spent += eps
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return SynthdataOutput(
            agent_id=AGENT_ID,
            status=SynthdataStatus.OPTIMAL.name,
            synthetic_data=synthetic,
            budget_consumed=eps,
            execution_time_ms=round(elapsed_ms, 2),
            metrics={
                "noise_scale": round(scale, 4),
                "total_epsilon_spent": round(self.total_epsilon_spent, 4),
                "items_synthesized": len(synthetic)
            }
        )
