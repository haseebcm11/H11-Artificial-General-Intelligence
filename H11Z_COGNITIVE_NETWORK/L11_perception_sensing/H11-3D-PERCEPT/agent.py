"""H11-3D-PERCEPT: 3D Point Cloud transformations.

Implements 3D rotation via Euler angles and projection.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-3D-PERCEPT"

class Percept3DError(ValueError): pass

@dataclass
class Percept3DInput:
    points: List[List[float]] # [x, y, z]
    pitch: float = 0.0 # X-axis rot
    yaw: float = 0.0   # Y-axis rot
    roll: float = 0.0  # Z-axis rot

@dataclass
class Percept3DOutput:
    agent_id: str
    transformed_points: List[List[float]]
    execution_time_ms: float

class Percept3DAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: Percept3DInput) -> Percept3DOutput:
        start_time = time.perf_counter()
        
        rx = math.radians(input_data.pitch)
        ry = math.radians(input_data.yaw)
        rz = math.radians(input_data.roll)
        
        cx, sx = math.cos(rx), math.sin(rx)
        cy, sy = math.cos(ry), math.sin(ry)
        cz, sz = math.cos(rz), math.sin(rz)
        
        # Combined rotation matrix Z * Y * X
        m00 = cy * cz
        m01 = sx * sy * cz - cx * sz
        m02 = cx * sy * cz + sx * sz
        
        m10 = cy * sz
        m11 = sx * sy * sz + cx * cz
        m12 = cx * sy * sz - sx * cz
        
        m20 = -sy
        m21 = sx * cy
        m22 = cx * cy
        
        transformed = []
        for p in input_data.points:
            x, y, z = p[0], p[1], p[2]
            nx = m00*x + m01*y + m02*z
            ny = m10*x + m11*y + m12*z
            nz = m20*x + m21*y + m22*z
            transformed.append([nx, ny, nz])

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return Percept3DOutput(
            agent_id=AGENT_ID,
            transformed_points=transformed,
            execution_time_ms=elapsed_ms
        )
