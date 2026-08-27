"""H11-MOTION: Motion detection and Optical Flow.

Implements simplified Lucas-Kanade optical flow for 2D motion estimation.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-MOTION"

class MotionError(ValueError): pass

@dataclass
class MotionInput:
    frame1: List[List[float]]
    frame2: List[List[float]]
    window_size: int = 3

@dataclass
class MotionOutput:
    agent_id: str
    flow_vectors: List[Dict[str, Any]]
    execution_time_ms: float

class MotionAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: MotionInput) -> MotionOutput:
        start_time = time.perf_counter()
        
        f1 = input_data.frame1
        f2 = input_data.frame2
        w = input_data.window_size
        
        if not f1 or not f2 or len(f1) != len(f2) or len(f1[0]) != len(f2[0]):
            raise MotionError("Invalid or mismatched frames")
            
        rows = len(f1)
        cols = len(f1[0])
        half_w = w // 2
        
        flow_vectors = []
        
        # Simplified Lucas-Kanade
        for i in range(half_w + 1, rows - half_w - 1, w):
            for j in range(half_w + 1, cols - half_w - 1, w):
                I_x = 0.0
                I_y = 0.0
                I_t = 0.0
                
                # Gradients over window
                sum_ix2 = 0.0
                sum_iy2 = 0.0
                sum_ixiy = 0.0
                sum_ixt = 0.0
                sum_iyt = 0.0
                
                for di in range(-half_w, half_w + 1):
                    for dj in range(-half_w, half_w + 1):
                        r = i + di
                        c = j + dj
                        
                        dx = (f1[r][c+1] - f1[r][c-1]) / 2.0
                        dy = (f1[r+1][c] - f1[r-1][c]) / 2.0
                        dt = f2[r][c] - f1[r][c]
                        
                        sum_ix2 += dx*dx
                        sum_iy2 += dy*dy
                        sum_ixiy += dx*dy
                        sum_ixt += dx*dt
                        sum_iyt += dy*dt
                        
                # Solve [sum_ix2 sum_ixiy; sum_ixiy sum_iy2] * [u; v] = [-sum_ixt; -sum_iyt]
                det = sum_ix2 * sum_iy2 - sum_ixiy * sum_ixiy
                if abs(det) > 1e-5:
                    u = (-sum_ixt * sum_iy2 + sum_iyt * sum_ixiy) / det
                    v = (sum_ix2 * -sum_iyt - sum_ixiy * -sum_ixt) / det
                    if abs(u) > 0.1 or abs(v) > 0.1:
                        flow_vectors.append({"row": i, "col": j, "u": u, "v": v})

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return MotionOutput(
            agent_id=AGENT_ID,
            flow_vectors=flow_vectors,
            execution_time_ms=elapsed_ms
        )
