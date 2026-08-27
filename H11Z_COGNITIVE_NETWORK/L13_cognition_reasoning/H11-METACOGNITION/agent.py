import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum, auto

AGENT_ID = "H11-METACOGNITION"

class MetacognitionStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()
    DEGRADED = auto()
    FAILED = auto()

class MetacognitionError(ValueError):
    pass

@dataclass(frozen=True)
class MetacognitionInput:
    target_id: str = "default_target"
    intensity: float = 1.0
    batch_size: int = 32
    tolerance: float = 1e-4
    parameters: Dict[str, float] = field(default_factory=lambda: {"alpha": 0.5, "beta": 0.9, "scale": 1.0})
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class MetacognitionOutput:
    agent_id: str
    status: str
    efficiency_score: float
    computed_value: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class MetacognitionAgent:
    """Analytical engine for H11-METACOGNITION. Implements confidence calibration 
    and Brier score evaluation for metacognitive monitoring."""
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "last_score": 1.0, "status": MetacognitionStatus.IDLE.name}

    def process(self, input_data: Optional[MetacognitionInput] = None) -> MetacognitionOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = MetacognitionInput()

        batch = int(input_data.batch_size)
        intensity = float(input_data.intensity)
        
        # Simulate predictions and outcomes to compute Brier score
        # Brier Score = 1/N * sum( (f_t - o_t)^2 )
        brier_score = 0.0
        calibration_error = 0.0
        for i in range(batch):
            # Simulated confidence (forecast)
            f_t = 0.5 + 0.4 * math.sin(i * intensity)
            # Simulated outcome (0 or 1) based on forecast + some noise
            prob_true = min(1.0, max(0.0, f_t + 0.1 * math.cos(i)))
            o_t = 1.0 if prob_true > 0.5 else 0.0
            
            brier_score += (f_t - o_t) ** 2
            calibration_error += abs(f_t - prob_true)
            
        brier_score /= batch
        calibration_error /= batch
        
        # Max Brier score is 1.0 (worst), min is 0.0 (best)
        efficiency = 1.0 - brier_score

        status = MetacognitionStatus.OPTIMAL.name if efficiency > 0.8 else MetacognitionStatus.ACTIVE.name
        self.state["evaluations_count"] = self.state.get("evaluations_count", 0) + 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        
        return MetacognitionOutput(
            agent_id=AGENT_ID,
            status=status,
            efficiency_score=efficiency,
            computed_value=brier_score,
            execution_time_ms=elapsed_ms,
            metrics={"brier_score": brier_score, "calibration_error": calibration_error},
            diagnostics=["Brier score and confidence calibration computed."]
        )
