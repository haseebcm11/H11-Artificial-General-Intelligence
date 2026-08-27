"""H11-VISION: Visual edge detection and processing.

Implements Sobel operators for discrete 2D spatial gradient convolution.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-VISION"

class VisionError(ValueError): pass

@dataclass
class VisionInput:
    image: List[List[float]] # 2D array of grayscale intensities [0, 1]
    threshold: float = 0.5

@dataclass
class VisionOutput:
    agent_id: str
    edge_map: List[List[float]]
    edge_pixel_count: int
    execution_time_ms: float

class VisionAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: VisionInput) -> VisionOutput:
        start_time = time.perf_counter()
        
        img = input_data.image
        if not img or not img[0]:
            raise VisionError("Invalid image dimensions")
            
        rows = len(img)
        cols = len(img[0])
        
        # Sobel kernels
        Gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        Gy = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
        
        edge_map = [[0.0 for _ in range(cols)] for _ in range(rows)]
        edge_count = 0
        
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                px = 0.0
                py = 0.0
                # 3x3 convolution
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        val = img[i+di][j+dj]
                        px += val * Gx[di+1][dj+1]
                        py += val * Gy[di+1][dj+1]
                        
                magnitude = math.sqrt(px*px + py*py)
                if magnitude >= input_data.threshold:
                    edge_map[i][j] = magnitude
                    edge_count += 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return VisionOutput(
            agent_id=AGENT_ID,
            edge_map=edge_map,
            edge_pixel_count=edge_count,
            execution_time_ms=elapsed_ms
        )
