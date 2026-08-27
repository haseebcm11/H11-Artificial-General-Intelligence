import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum, auto

AGENT_ID = "motivation"

class MotivationStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()
    DEGRADED = auto()
    FAILED = auto()

class MotivationError(ValueError):
    pass

@dataclass(frozen=True)
class MotivationInput:
    target_id: str = "default_target"
    intensity: float = 1.0
    batch_size: int = 32
    tolerance: float = 1e-4
    parameters: Dict[str, float] = field(default_factory=lambda: {"alpha": 0.5, "beta": 0.9, "scale": 1.0})
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class MotivationOutput:
    agent_id: str
    status: str
    efficiency_score: float
    computed_value: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class MotivationAgent:
    """Analytical engine for Motivation. Implements Hull's Drive-Reduction Theory
    math where behavior potential E = D(Drive) * H(Habit) * V(Stimulus) * K(Incentive)."""
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "status": MotivationStatus.IDLE.name}
        self.start_time = time.time()

    def process(self, input_data: Optional[MotivationInput] = None) -> MotivationOutput:
        start_time_perf = time.perf_counter()
        if input_data is None:
            input_data = MotivationInput()

        # Hullian Drive Theory parameters
        habit_strength_H = float(input_data.parameters.get("alpha", 0.8)) 
        incentive_K = float(input_data.parameters.get("beta", 1.2))
        stimulus_V = float(input_data.intensity)
        
        # Drive grows logarithmically with time since satisfied
        time_elapsed = time.time() - self.start_time
        base_drive = math.log1p(time_elapsed)
        
        # Behavior Potential E = D * H * V * K
        behavior_potential_E = base_drive * habit_strength_H * stimulus_V * incentive_K
        
        # When E exceeds a threshold, an action occurs reducing the drive
        action_triggered = behavior_potential_E > 10.0
        
        if action_triggered:
            # Drive reduction
            self.start_time = time.time() # Reset clock
            drive_after = 0.0
        else:
            drive_after = base_drive

        # Efficiency measures how well the agent translates drive into potential
        efficiency = min(1.0, max(0.0, behavior_potential_E / 20.0))

        status = MotivationStatus.OPTIMAL.name if efficiency > 0.8 else MotivationStatus.ACTIVE.name
        self.state["evaluations_count"] = self.state.get("evaluations_count", 0) + 1

        elapsed_ms = (time.perf_counter() - start_time_perf) * 1000.0
        
        return MotivationOutput(
            agent_id=AGENT_ID,
            status=status,
            efficiency_score=efficiency,
            computed_value=behavior_potential_E,
            execution_time_ms=elapsed_ms,
            metrics={"drive": base_drive, "potential_E": behavior_potential_E, "action_triggered": float(action_triggered)},
            diagnostics=["Hullian Drive-Reduction theory computed."]
        )
