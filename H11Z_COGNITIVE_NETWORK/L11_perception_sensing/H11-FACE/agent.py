"""H11-FACE: Face representation projection.

Implements Eigenfaces principal component projection.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-FACE"

class FaceError(ValueError): pass

@dataclass
class FaceInput:
    face_vector: List[float]
    mean_face: List[float]
    eigenvectors: List[List[float]] # K x N

@dataclass
class FaceOutput:
    agent_id: str
    projected_weights: List[float]
    reconstruction_error: float
    execution_time_ms: float

class FaceAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: FaceInput) -> FaceOutput:
        start_time = time.perf_counter()
        
        if len(input_data.face_vector) != len(input_data.mean_face):
            raise FaceError("Face and mean face dimension mismatch")
            
        # Zero-mean center the face
        phi = [f - m for f, m in zip(input_data.face_vector, input_data.mean_face)]
        
        # Project onto eigenvectors: w_k = U_k^T * phi
        weights = []
        for ev in input_data.eigenvectors:
            w = sum(x * e for x, e in zip(phi, ev))
            weights.append(w)
            
        # Calculate reconstruction
        reconstructed = [0.0] * len(phi)
        for i, ev in enumerate(input_data.eigenvectors):
            w = weights[i]
            for j in range(len(phi)):
                reconstructed[j] += w * ev[j]
                
        # Error
        error_sq = sum((p - r)**2 for p, r in zip(phi, reconstructed))

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return FaceOutput(
            agent_id=AGENT_ID,
            projected_weights=weights,
            reconstruction_error=math.sqrt(error_sq),
            execution_time_ms=elapsed_ms
        )
