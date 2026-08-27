import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum, auto

AGENT_ID = "H11-PERSONA"

class PersonaStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()
    DEGRADED = auto()
    FAILED = auto()

class PersonaError(ValueError):
    pass

@dataclass(frozen=True)
class PersonaInput:
    target_id: str = "default_target"
    intensity: float = 1.0
    batch_size: int = 32
    tolerance: float = 1e-4
    parameters: Dict[str, float] = field(default_factory=lambda: {"alpha": 0.5, "beta": 0.9, "scale": 1.0})
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class PersonaOutput:
    agent_id: str
    status: str
    efficiency_score: float
    computed_value: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class PersonaAgent:
    """Analytical engine for H11-PERSONA. Implements Latent Dirichlet Allocation (LDA)
    topic distribution Dirichlet priors math."""
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "status": PersonaStatus.IDLE.name}

    def process(self, input_data: Optional[PersonaInput] = None) -> PersonaOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = PersonaInput()

        alpha = float(input_data.parameters.get("alpha", 0.5)) # Dirichlet hyperparameter for topic distribution
        intensity = float(input_data.intensity)
        num_topics = 3
        
        # Simulate drawing a topic distribution theta ~ Dir(alpha)
        # Using intensity to bias the distribution
        unnormalized = [alpha + (intensity * (i+1)) for i in range(num_topics)]
        sum_unnormalized = sum(unnormalized)
        theta = [x / sum_unnormalized for x in unnormalized]
        
        # Dirichlet PDF evaluation (ignoring normalizing Beta function constant for speed)
        # pdf propto prod(theta_i ^ (alpha - 1))
        log_pdf_unnorm = 0.0
        for t in theta:
            if t > 0:
                log_pdf_unnorm += (alpha - 1.0) * math.log(t)
                
        # Efficiency based on how sharply defined the persona is (low entropy)
        entropy = -sum(t * math.log2(t) for t in theta if t > 0)
        max_entropy = math.log2(num_topics)
        efficiency = 1.0 - (entropy / max_entropy)

        status = PersonaStatus.OPTIMAL.name if efficiency > 0.8 else PersonaStatus.ACTIVE.name
        self.state["evaluations_count"] = self.state.get("evaluations_count", 0) + 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        
        return PersonaOutput(
            agent_id=AGENT_ID,
            status=status,
            efficiency_score=efficiency,
            computed_value=entropy,
            execution_time_ms=elapsed_ms,
            metrics={"theta_0": theta[0], "theta_1": theta[1], "log_pdf_unnorm": log_pdf_unnorm},
            diagnostics=["Latent Dirichlet Allocation topic distribution computed."]
        )
