import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum, auto

AGENT_ID = "H11-RENDER"

class RenderStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()
    DEGRADED = auto()
    FAILED = auto()

class RenderError(ValueError):
    pass

@dataclass(frozen=True)
class RenderInput:
    target_id: str = "default_target"
    intensity: float = 1.0
    batch_size: int = 32
    tolerance: float = 1e-4
    parameters: Dict[str, float] = field(default_factory=lambda: {"alpha": 0.5, "beta": 0.9, "scale": 1.0})
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class RenderOutput:
    agent_id: str
    status: str
    efficiency_score: float
    computed_value: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class RenderAgent:
    """Analytical engine for H11-RENDER. Implements Ray Tracing Lambertian 
    reflectance and Blinn-Phong specular highlighting math."""
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "status": RenderStatus.IDLE.name}

    def _dot(self, v1: List[float], v2: List[float]) -> float:
        return sum(a*b for a, b in zip(v1, v2))

    def _normalize(self, v: List[float]) -> List[float]:
        mag = math.sqrt(sum(a*a for a in v))
        return [a/mag for a in v] if mag > 0 else v

    def process(self, input_data: Optional[RenderInput] = None) -> RenderOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = RenderInput()

        intensity = float(input_data.intensity)
        shininess = float(input_data.parameters.get("scale", 32.0))
        
        # Simulate vectors for a surface point
        normal_vec = self._normalize([0.0, 1.0, 0.0])
        # Light moving based on intensity
        light_vec = self._normalize([math.cos(intensity), math.sin(intensity), 0.5])
        view_vec = self._normalize([0.0, 0.5, 1.0])
        
        # Lambertian Reflectance (Diffuse)
        # I_d = I_l * K_d * max(0, N dot L)
        n_dot_l = max(0.0, self._dot(normal_vec, light_vec))
        diffuse = n_dot_l
        
        # Blinn-Phong (Specular)
        # Halfway vector H = normalize(L + V)
        half_vec = self._normalize([l + v for l, v in zip(light_vec, view_vec)])
        n_dot_h = max(0.0, self._dot(normal_vec, half_vec))
        specular = math.pow(n_dot_h, shininess) if n_dot_l > 0 else 0.0
        
        # Total lighting
        total_light = diffuse + 0.5 * specular
        
        efficiency = min(1.0, total_light)

        status = RenderStatus.OPTIMAL.name if efficiency > 0.8 else RenderStatus.ACTIVE.name
        self.state["evaluations_count"] = self.state.get("evaluations_count", 0) + 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        
        return RenderOutput(
            agent_id=AGENT_ID,
            status=status,
            efficiency_score=efficiency,
            computed_value=total_light,
            execution_time_ms=elapsed_ms,
            metrics={"diffuse": diffuse, "specular": specular, "n_dot_l": n_dot_l},
            diagnostics=["Lambertian and Blinn-Phong reflectance evaluated."]
        )
