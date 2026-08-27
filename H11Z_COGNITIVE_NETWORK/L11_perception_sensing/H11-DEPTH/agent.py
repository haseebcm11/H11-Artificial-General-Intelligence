"""H11-DEPTH: Stereo disparity estimation.

Implements Focal length to depth conversion Z = f * B / d.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-DEPTH"

class DepthError(ValueError): pass

@dataclass
class DepthInput:
    disparity_map: List[List[float]]
    focal_length_px: float = 800.0
    baseline_meters: float = 0.1

@dataclass
class DepthOutput:
    agent_id: str
    depth_map: List[List[float]]
    min_depth: float
    max_depth: float
    execution_time_ms: float

class DepthAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: DepthInput) -> DepthOutput:
        start_time = time.perf_counter()
        
        disparity = input_data.disparity_map
        if not disparity or not disparity[0]:
            raise DepthError("Invalid disparity map")
            
        f = input_data.focal_length_px
        B = input_data.baseline_meters
        
        rows = len(disparity)
        cols = len(disparity[0])
        
        depth_map = [[0.0]*cols for _ in range(rows)]
        min_z = float('inf')
        max_z = float('-inf')
        
        for i in range(rows):
            for j in range(cols):
                d = disparity[i][j]
                if d <= 0:
                    z = 0.0 # Unknown or infinite
                else:
                    z = (f * B) / d
                    if z < min_z: min_z = z
                    if z > max_z: max_z = z
                depth_map[i][j] = z
                
        if min_z == float('inf'): min_z = 0.0
        if max_z == float('-inf'): max_z = 0.0

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return DepthOutput(
            agent_id=AGENT_ID,
            depth_map=depth_map,
            min_depth=min_z,
            max_depth=max_z,
            execution_time_ms=elapsed_ms
        )
