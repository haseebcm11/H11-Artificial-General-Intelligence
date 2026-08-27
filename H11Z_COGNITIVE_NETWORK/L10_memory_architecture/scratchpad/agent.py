"""scratchpad: Spatial matrix manipulation buffer.

Implements 2D Affine transformations (Scale, Rotate, Translate).
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "scratchpad"

class ScratchpadError(ValueError): pass

@dataclass
class ScratchpadInput:
    points: List[List[float]] # List of [x, y]
    translation: List[float] = field(default_factory=lambda: [0.0, 0.0])
    rotation_deg: float = 0.0
    scale: List[float] = field(default_factory=lambda: [1.0, 1.0])

@dataclass
class ScratchpadOutput:
    agent_id: str
    transformed_points: List[List[float]]
    execution_time_ms: float

class ScratchpadAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: ScratchpadInput) -> ScratchpadOutput:
        start_time = time.perf_counter()
        
        rad = math.radians(input_data.rotation_deg)
        cos_t = math.cos(rad)
        sin_t = math.sin(rad)
        
        tx = input_data.translation[0]
        ty = input_data.translation[1]
        
        sx = input_data.scale[0]
        sy = input_data.scale[1]
        
        # Transformation matrix (homogeneous)
        # [ sx*cos_t  -sy*sin_t   tx ]
        # [ sx*sin_t   sy*cos_t   ty ]
        # [ 0          0          1  ]
        
        transformed = []
        for p in input_data.points:
            x, y = p[0], p[1]
            
            # Scale
            x_s = x * sx
            y_s = y * sy
            
            # Rotate
            x_r = x_s * cos_t - y_s * sin_t
            y_r = x_s * sin_t + y_s * cos_t
            
            # Translate
            x_t = x_r + tx
            y_t = y_r + ty
            
            transformed.append([x_t, y_t])

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return ScratchpadOutput(
            agent_id=AGENT_ID,
            transformed_points=transformed,
            execution_time_ms=elapsed_ms
        )
