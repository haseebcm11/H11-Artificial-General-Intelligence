"""H11-QUALITY: Multi-dimensional quality scoring and SLA enforcement gate.

Implements Kolmogorov-Smirnov (KS) test and 1D Wasserstein metric 
(Earth Mover's Distance) for distribution drift detection.
Math: W_1(u, v) = integral_{-inf}^{inf} |U(x) - V(x)| dx where U,V are CDFs.
"""
import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11-QUALITY"

class QualityError(ValueError):
    """Domain-specific error for H11-QUALITY."""

class QualityStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()

@dataclass(frozen=True)
class QualityInput:
    baseline_distribution: List[float] = field(default_factory=list)
    incoming_distribution: List[float] = field(default_factory=list)
    ks_threshold: float = 0.05
    wasserstein_threshold: float = 0.1

@dataclass(frozen=True)
class QualityOutput:
    agent_id: str
    status: str
    ks_statistic: float
    wasserstein_distance: float
    is_drifted: bool
    execution_time_ms: float
    diagnostics: Dict[str, float]

class QualityAgent:
    """Analytical engine for Statistical drift detection."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def _ecdf(self, data: List[float]) -> List[Tuple[float, float]]:
        """Computes Empirical Cumulative Distribution Function."""
        n = len(data)
        if n == 0: return []
        sorted_data = sorted(data)
        result = []
        for i, val in enumerate(sorted_data):
            result.append((val, (i + 1) / n))
        return result

    def _ks_2samp(self, data1: List[float], data2: List[float]) -> float:
        """Computes 2-sample Kolmogorov-Smirnov statistic."""
        n1, n2 = len(data1), len(data2)
        if n1 == 0 or n2 == 0: return 1.0
        
        data1_sorted = sorted(data1)
        data2_sorted = sorted(data2)
        
        data_all = sorted(set(data1_sorted + data2_sorted))
        d_max = 0.0
        i, j = 0, 0
        
        for val in data_all:
            while i < n1 and data1_sorted[i] <= val: i += 1
            while j < n2 and data2_sorted[j] <= val: j += 1
            
            cdf1 = i / n1
            cdf2 = j / n2
            d_max = max(d_max, abs(cdf1 - cdf2))
            
        return d_max

    def _wasserstein_1d(self, u_values: List[float], v_values: List[float]) -> float:
        """Computes 1D Wasserstein distance between two distributions."""
        n = len(u_values)
        m = len(v_values)
        if n == 0 or m == 0: return float('inf')
        
        u_sorted = sorted(u_values)
        v_sorted = sorted(v_values)
        
        # Merge sort unique values
        all_values = sorted(set(u_sorted + v_sorted))
        u_cdf = 0.0
        v_cdf = 0.0
        i, j = 0, 0
        
        distance = 0.0
        prev_val = all_values[0]
        
        for val in all_values:
            # Integrate absolute difference of CDFs
            delta = val - prev_val
            distance += abs(u_cdf - v_cdf) * delta
            
            while i < n and u_sorted[i] <= val:
                u_cdf += 1.0 / n
                i += 1
            while j < m and v_sorted[j] <= val:
                v_cdf += 1.0 / m
                j += 1
                
            prev_val = val
            
        return distance

    def process(self, input_data: Optional[QualityInput] = None) -> QualityOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = QualityInput()

        base = input_data.baseline_distribution
        inc = input_data.incoming_distribution

        ks_stat = self._ks_2samp(base, inc)
        w_dist = self._wasserstein_1d(base, inc)
        
        drifted = (ks_stat > input_data.ks_threshold) or (w_dist > input_data.wasserstein_threshold)
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return QualityOutput(
            agent_id=AGENT_ID,
            status=QualityStatus.OPTIMAL.name,
            ks_statistic=round(ks_stat, 6),
            wasserstein_distance=round(w_dist, 6),
            is_drifted=drifted,
            execution_time_ms=round(elapsed_ms, 2),
            diagnostics={
                "n_baseline": len(base),
                "n_incoming": len(inc)
            }
        )
