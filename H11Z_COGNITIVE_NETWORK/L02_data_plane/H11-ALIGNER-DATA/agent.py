"""H11-ALIGNER-DATA: Multi-modal and cross-lingual data alignment engine.

Implements the Gale-Church algorithm for length-based sentence alignment 
and Dynamic Time Warping (DTW) with Sakoe-Chiba bands for temporal sequences.
Math: Cost function C(l1, l2) = -log(P(match|l1, l2)) based on Gaussian approximation
of length differences.
"""
import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11-ALIGNER-DATA"

class AlignerdataError(ValueError):
    """Domain-specific error for H11-ALIGNER-DATA."""

class AlignerdataStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()

@dataclass(frozen=True)
class SequenceItem:
    length: int
    content: str
    timestamp: float = 0.0

@dataclass(frozen=True)
class AlignerdataInput:
    source_sequence: List[SequenceItem] = field(default_factory=list)
    target_sequence: List[SequenceItem] = field(default_factory=list)
    mean_length_ratio: float = 1.0
    variance_length: float = 6.8
    dtw_band_radius: int = 10

@dataclass(frozen=True)
class AlignerdataOutput:
    agent_id: str
    status: str
    gale_church_cost: float
    aligned_pairs: List[Tuple[int, int]]
    dtw_distance: float
    execution_time_ms: float
    diagnostics: Dict[str, float]

class AlignerdataAgent:
    """Analytical engine for Gale-Church and DTW alignment."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.c = 1.0  # length ratio constant

    def _prob_match(self, l1: int, l2: int, var: float) -> float:
        """Computes the probability of a match given sequence lengths."""
        if l1 == 0 and l2 == 0:
            return 1.0
        delta = (l1 - l2 * self.c) / math.sqrt(l1 * var) if l1 > 0 else float('inf')
        # Normal distribution CDF approximation
        prob = 2 * (1.0 - self._norm_cdf(abs(delta)))
        return max(prob, 1e-10) # avoid log(0)

    def _norm_cdf(self, x: float) -> float:
        """Approximation of the standard normal CDF."""
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))

    def _gale_church(self, src: List[SequenceItem], tgt: List[SequenceItem], var: float) -> Tuple[float, List[Tuple[int, int]]]:
        """Dynamic programming for length-based alignment."""
        n, m = len(src), len(tgt)
        if n == 0 or m == 0:
            return 0.0, []

        cost_matrix = [[float('inf')] * (m + 1) for _ in range(n + 1)]
        cost_matrix[0][0] = 0.0
        backtrack = [[(0, 0)] * (m + 1) for _ in range(n + 1)]

        transitions = [(1, 1), (1, 0), (0, 1), (2, 1), (1, 2), (2, 2)]

        for i in range(n + 1):
            for j in range(m + 1):
                if i == 0 and j == 0:
                    continue
                
                best_cost = float('inf')
                best_step = (0, 0)
                
                for di, dj in transitions:
                    if i - di >= 0 and j - dj >= 0:
                        l1 = sum(src[x].length for x in range(i - di, i))
                        l2 = sum(tgt[y].length for y in range(j - dj, j))
                        
                        transition_cost = -math.log(self._prob_match(l1, l2, var))
                        prev_cost = cost_matrix[i - di][j - dj]
                        
                        total_cost = prev_cost + transition_cost
                        if total_cost < best_cost:
                            best_cost = total_cost
                            best_step = (di, dj)
                            
                cost_matrix[i][j] = best_cost
                backtrack[i][j] = best_step

        # Backtracking
        path = []
        curr_i, curr_j = n, m
        while curr_i > 0 or curr_j > 0:
            di, dj = backtrack[curr_i][curr_j]
            if di == 0 and dj == 0:
                break
            path.append((curr_i - di, curr_j - dj))
            curr_i -= di
            curr_j -= dj
            
        path.reverse()
        return cost_matrix[n][m], path

    def _fast_dtw(self, src: List[SequenceItem], tgt: List[SequenceItem], r: int) -> float:
        """Fast Dynamic Time Warping with Sakoe-Chiba band."""
        n, m = len(src), len(tgt)
        if n == 0 or m == 0: return 0.0
        
        dtw = [[float('inf')] * (m + 1) for _ in range(n + 1)]
        dtw[0][0] = 0.0
        
        for i in range(1, n + 1):
            start = max(1, i - r)
            end = min(m, i + r)
            for j in range(start, end + 1):
                cost = abs(src[i-1].timestamp - tgt[j-1].timestamp)
                dtw[i][j] = cost + min(dtw[i-1][j], dtw[i][j-1], dtw[i-1][j-1])
                
        return dtw[n][m]

    def process(self, input_data: Optional[AlignerdataInput] = None) -> AlignerdataOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = AlignerdataInput()

        self.c = input_data.mean_length_ratio

        gc_cost, pairs = self._gale_church(
            input_data.source_sequence, 
            input_data.target_sequence, 
            input_data.variance_length
        )
        
        dtw_dist = self._fast_dtw(
            input_data.source_sequence,
            input_data.target_sequence,
            input_data.dtw_band_radius
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return AlignerdataOutput(
            agent_id=AGENT_ID,
            status=AlignerdataStatus.OPTIMAL.name,
            gale_church_cost=round(gc_cost, 4),
            aligned_pairs=pairs,
            dtw_distance=round(dtw_dist, 4),
            execution_time_ms=round(elapsed_ms, 2),
            diagnostics={"pairs_aligned": len(pairs), "avg_cost": gc_cost / max(1, len(pairs))}
        )
