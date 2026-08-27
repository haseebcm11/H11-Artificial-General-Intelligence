"""compression_mem: Memory compression via Principal Component Analysis.

Implements Power Iteration for finding the top principal component.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "compression_mem"

class CompressionError(ValueError): pass

@dataclass
class CompressionInput:
    data_matrix: List[List[float]]
    iterations: int = 50

@dataclass
class CompressionOutput:
    agent_id: str
    principal_vector: List[float]
    eigenvalue: float
    execution_time_ms: float

class CompressionAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: CompressionInput) -> CompressionOutput:
        start_time = time.perf_counter()
        
        matrix = input_data.data_matrix
        if not matrix or not matrix[0]:
            raise CompressionError("Empty data matrix")
            
        rows = len(matrix)
        cols = len(matrix[0])
        
        # Compute covariance matrix (assumed zero-mean for speed)
        cov = [[0.0]*cols for _ in range(cols)]
        for i in range(cols):
            for j in range(cols):
                s = sum(matrix[r][i] * matrix[r][j] for r in range(rows))
                cov[i][j] = s / rows
                
        # Power iteration
        b_k = [1.0] * cols
        eigenvalue = 0.0
        
        for _ in range(input_data.iterations):
            b_k1 = [0.0] * cols
            for i in range(cols):
                b_k1[i] = sum(cov[i][j] * b_k[j] for j in range(cols))
                
            norm = math.sqrt(sum(x*x for x in b_k1))
            if norm == 0:
                break
            b_k = [x / norm for x in b_k1]
            
        # Compute eigenvalue (Rayleigh quotient)
        num = 0.0
        for i in range(cols):
            row_sum = sum(cov[i][j] * b_k[j] for j in range(cols))
            num += b_k[i] * row_sum
        eigenvalue = num

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return CompressionOutput(
            agent_id=AGENT_ID,
            principal_vector=b_k,
            eigenvalue=eigenvalue,
            execution_time_ms=elapsed_ms
        )
