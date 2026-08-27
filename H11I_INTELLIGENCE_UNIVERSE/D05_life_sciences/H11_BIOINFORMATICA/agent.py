"""H11_BIOINFORMATICA: Bioinformatics & Sequence Alignment Engine.

D05_life_sciences - Universe

This module implements the analytical execution engine for H11_BIOINFORMATICA.
It performs sequence alignment scoring using match/mismatch penalties,
and calculates basic GC content metrics.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_BIOINFORMATICA"

class BioinformaticaError(ValueError):
    """Domain-specific error for H11_BIOINFORMATICA."""
    pass

class BioinformaticaStatus(Enum):
    IDLE = auto()
    HIGH_HOMOLOGY = auto()
    LOW_HOMOLOGY = auto()
    FAILED = auto()

@dataclass(frozen=True)
class BioinformaticaInput:
    sequence_a: str
    sequence_b: str
    match_score: int = 1
    mismatch_penalty: int = -1
    gap_penalty: int = -2

@dataclass(frozen=True)
class BioinformaticaOutput:
    agent_id: str
    status: str
    alignment_score: int
    percent_identity: float
    gc_content_a: float
    gc_content_b: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class BioinformaticaAgent:
    """Analytical engine for bioinformatics sequence calculations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {
            "evaluations_count": 0, 
            "status": BioinformaticaStatus.IDLE.name
        }

    def process(self, input_data: Optional[BioinformaticaInput] = None) -> BioinformaticaOutput:
        start_time = time.perf_counter()
        
        if input_data is None:
            raise BioinformaticaError("BioinformaticaInput data must be provided.")
        if not input_data.sequence_a or not input_data.sequence_b:
            raise BioinformaticaError("Sequences cannot be empty.")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1
        diagnostics = []

        seq_a = input_data.sequence_a.upper()
        seq_b = input_data.sequence_b.upper()
        
        # Calculate GC Content
        gc_a = sum(1 for c in seq_a if c in 'GC') / len(seq_a)
        gc_b = sum(1 for c in seq_b if c in 'GC') / len(seq_b)

        # Simplified Needleman-Wunsch Scoring (Global Alignment Matrix)
        m, n = len(seq_a), len(seq_b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i * input_data.gap_penalty
        for j in range(n + 1):
            dp[0][j] = j * input_data.gap_penalty
            
        matches = 0
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq_a[i-1] == seq_b[j-1]:
                    score = input_data.match_score
                    matches += 1
                else:
                    score = input_data.mismatch_penalty
                    
                dp[i][j] = max(
                    dp[i-1][j-1] + score,
                    dp[i-1][j] + input_data.gap_penalty,
                    dp[i][j-1] + input_data.gap_penalty
                )
                
        alignment_score = dp[m][n]
        max_possible_length = max(m, n)
        percent_identity = (matches / max_possible_length) * 100.0

        if percent_identity > 80.0:
            status = BioinformaticaStatus.HIGH_HOMOLOGY.name
            diagnostics.append("High sequence homology detected.")
        else:
            status = BioinformaticaStatus.LOW_HOMOLOGY.name
            diagnostics.append("Low sequence homology detected.")

        self.state["status"] = status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "sequence_length_diff": abs(m - n),
            "max_possible_score": min(m, n) * input_data.match_score
        }

        return BioinformaticaOutput(
            agent_id=AGENT_ID,
            status=status,
            alignment_score=alignment_score,
            percent_identity=round(percent_identity, 2),
            gc_content_a=round(gc_a * 100, 2),
            gc_content_b=round(gc_b * 100, 2),
            execution_time_ms=round(elapsed_ms, 4),
            metrics=metrics,
            diagnostics=diagnostics
        )

    def health_check(self) -> Dict[str, Any]:
        return {
            "agent_id": AGENT_ID,
            "status": self.state.get("status", "UNKNOWN"),
            "evaluations_count": self.state.get("evaluations_count", 0)
        }
