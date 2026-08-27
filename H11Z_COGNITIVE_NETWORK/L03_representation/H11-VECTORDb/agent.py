"""
H11-VECTORDb: Autoencoder Reconstruction Loss.
Evaluates Mean Squared Error (MSE) and binary cross-entropy reconstruction.
"""
from dataclasses import dataclass
from typing import List
import math

AGENT_ID = "H11-VECTORDb"

@dataclass
class VectorDbInput:
    original: List[List[float]]
    reconstructed: List[List[float]]
    loss_type: str = "mse"

@dataclass
class VectorDbOutput:
    loss: float
    per_sample_loss: List[float]

class H11VectorDbAgent:
    def process(self, data: VectorDbInput) -> VectorDbOutput:
        N = len(data.original)
        if N != len(data.reconstructed):
            raise ValueError("Mismatched dimensions")
        D = len(data.original[0])
        
        per_sample = []
        total_loss = 0.0
        
        for i in range(N):
            sample_loss = 0.0
            if data.loss_type == "mse":
                sample_loss = sum((data.original[i][j] - data.reconstructed[i][j])**2 for j in range(D)) / D
            elif data.loss_type == "bce":
                for j in range(D):
                    x = data.original[i][j]
                    y = data.reconstructed[i][j]
                    y = max(min(y, 1 - 1e-7), 1e-7)
                    sample_loss -= (x * math.log(y) + (1 - x) * math.log(1 - y))
                sample_loss /= D
            else:
                raise ValueError("Unknown loss type")
                
            per_sample.append(sample_loss)
            total_loss += sample_loss
            
        return VectorDbOutput(
            loss=total_loss / N,
            per_sample_loss=per_sample
        )
