import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum, auto

AGENT_ID = "H11-INSIGHT"

class InsightStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()
    DEGRADED = auto()
    FAILED = auto()

class InsightError(ValueError):
    pass

@dataclass(frozen=True)
class InsightInput:
    target_id: str = "default_target"
    intensity: float = 1.0
    batch_size: int = 32
    tolerance: float = 1e-4
    parameters: Dict[str, float] = field(default_factory=lambda: {"alpha": 0.5, "beta": 0.9, "scale": 1.0})
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class InsightOutput:
    agent_id: str
    status: str
    efficiency_score: float
    computed_value: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class InsightAgent:
    """Analytical engine for H11-INSIGHT. Implements Aha moment / Gestalt clustering 
    via energy barrier crossing in Hopfield-like attractor networks."""
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "last_score": 1.0, "status": InsightStatus.IDLE.name}

    def process(self, input_data: Optional[InsightInput] = None) -> InsightOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = InsightInput()

        alpha = float(input_data.parameters.get("alpha", 0.5))
        intensity = float(input_data.intensity)
        
        # Gestalt shift: simulated energy barrier crossing
        # Energy E = - sum(w_ij s_i s_j), insight happens when E drops below a threshold
        initial_energy = 100.0 * alpha
        barrier = 10.0
        
        # Probability of crossing barrier (Arrhenius equation analog)
        temperature = max(0.1, intensity * 5.0)
        prob_insight = math.exp(-barrier / temperature)
        
        # If insight occurs, new energy is lower
        final_energy = initial_energy * (1.0 - prob_insight)
        energy_drop = initial_energy - final_energy
        
        efficiency = min(1.0, prob_insight * (energy_drop / initial_energy) if initial_energy > 0 else 0)

        status = InsightStatus.OPTIMAL.name if efficiency > 0.8 else InsightStatus.ACTIVE.name
        self.state["evaluations_count"] = self.state.get("evaluations_count", 0) + 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        
        return InsightOutput(
            agent_id=AGENT_ID,
            status=status,
            efficiency_score=efficiency,
            computed_value=energy_drop,
            execution_time_ms=elapsed_ms,
            metrics={"prob_insight": prob_insight, "initial_energy": initial_energy, "final_energy": final_energy},
            diagnostics=["Gestalt clustering energy calculation complete."]
        )
