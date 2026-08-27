import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum, auto

AGENT_ID = "H11-LOCALIZATION"

class LocalizationStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()
    DEGRADED = auto()
    FAILED = auto()

class LocalizationError(ValueError):
    pass

@dataclass(frozen=True)
class LocalizationInput:
    target_id: str = "default_target"
    intensity: float = 1.0
    batch_size: int = 32
    tolerance: float = 1e-4
    parameters: Dict[str, float] = field(default_factory=lambda: {"alpha": 0.5, "beta": 0.9, "scale": 1.0})
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class LocalizationOutput:
    agent_id: str
    status: str
    efficiency_score: float
    computed_value: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class LocalizationAgent:
    """Analytical engine for H11-LOCALIZATION. Implements Bounding Box IoU 
    (Intersection over Union) and Non-Maximum Suppression (NMS)."""
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "status": LocalizationStatus.IDLE.name}

    def process(self, input_data: Optional[LocalizationInput] = None) -> LocalizationOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = LocalizationInput()

        intensity = float(input_data.intensity)
        iou_threshold = float(input_data.parameters.get("alpha", 0.5))
        
        # Simulate two bounding boxes [x1, y1, x2, y2]
        # Box A
        ax1, ay1, ax2, ay2 = 0.0, 0.0, 10.0, 10.0
        # Box B (overlapping based on intensity)
        offset = 5.0 * (1.0 - min(1.0, intensity))
        bx1, by1, bx2, by2 = offset, offset, 10.0 + offset, 10.0 + offset
        
        # Compute Intersection
        ix1 = max(ax1, bx1)
        iy1 = max(ay1, by1)
        ix2 = min(ax2, bx2)
        iy2 = min(ay2, by2)
        
        inter_area = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
        
        # Compute Union
        box_a_area = (ax2 - ax1) * (ay2 - ay1)
        box_b_area = (bx2 - bx1) * (by2 - by1)
        union_area = box_a_area + box_b_area - inter_area
        
        iou = inter_area / max(1e-5, union_area)
        
        # NMS suppression check
        suppressed = 1.0 if iou > iou_threshold else 0.0
        
        efficiency = iou # High IoU means good localization overlap

        status = LocalizationStatus.OPTIMAL.name if efficiency > 0.8 else LocalizationStatus.ACTIVE.name
        self.state["evaluations_count"] = self.state.get("evaluations_count", 0) + 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        
        return LocalizationOutput(
            agent_id=AGENT_ID,
            status=status,
            efficiency_score=efficiency,
            computed_value=iou,
            execution_time_ms=elapsed_ms,
            metrics={"inter_area": inter_area, "union_area": union_area, "suppressed": suppressed},
            diagnostics=["Bounding Box IoU and NMS evaluated."]
        )
