"""H11_CLEANSER: Anomaly Detection and Data Imputation.

Implements Median Absolute Deviation (MAD) for robust outlier detection
and z-score based clipping, followed by mean/median imputation.
Math: MAD = median(|x_i - median(X)|). Robust Z-score = 0.6745 * (x_i - median) / MAD.
"""
import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_CLEANSER"

class CleanserError(ValueError):
    """Domain-specific error for H11_CLEANSER."""

class CleanserStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()

@dataclass(frozen=True)
class CleanserInput:
    features: List[Optional[float]] = field(default_factory=list)
    robust_z_threshold: float = 3.5
    imputation_strategy: str = "median" # 'median' or 'mean'

@dataclass(frozen=True)
class CleanserOutput:
    agent_id: str
    status: str
    cleaned_features: List[float]
    imputed_indices: List[int]
    anomaly_indices: List[int]
    execution_time_ms: float
    diagnostics: Dict[str, float]

class CleanserAgent:
    """Analytical engine for robust anomaly detection and imputation."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def _median(self, data: List[float]) -> float:
        if not data: return 0.0
        s = sorted(data)
        n = len(s)
        if n % 2 == 1:
            return s[n // 2]
        return 0.5 * (s[n // 2 - 1] + s[n // 2])

    def _mean(self, data: List[float]) -> float:
        if not data: return 0.0
        return sum(data) / len(data)

    def process(self, input_data: Optional[CleanserInput] = None) -> CleanserOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = CleanserInput()

        raw = input_data.features
        n = len(raw)
        
        # 1. Separate valid from missing
        valid_vals = [x for x in raw if x is not None]
        if not valid_vals:
            raise CleanserError("No valid data to compute statistics.")

        # 2. Compute statistics
        med = self._median(valid_vals)
        mean_val = self._mean(valid_vals)
        mad = self._median([abs(x - med) for x in valid_vals])
        
        # 3. Detect anomalies using Robust Z-Score
        # Constant 0.6745 scales MAD to standard deviation for normal distribution
        anomalies = []
        imputed = []
        clean = []
        
        replacement = med if input_data.imputation_strategy == "median" else mean_val
        
        for i, val in enumerate(raw):
            if val is None:
                clean.append(replacement)
                imputed.append(i)
                continue
                
            if mad == 0:
                robust_z = 0.0
            else:
                robust_z = 0.6745 * abs(val - med) / mad
                
            if robust_z > input_data.robust_z_threshold:
                anomalies.append(i)
                # Clip or impute anomaly. Here we impute.
                clean.append(replacement)
                imputed.append(i)
            else:
                clean.append(val)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return CleanserOutput(
            agent_id=AGENT_ID,
            status=CleanserStatus.OPTIMAL.name,
            cleaned_features=clean,
            imputed_indices=imputed,
            anomaly_indices=anomalies,
            execution_time_ms=round(elapsed_ms, 2),
            diagnostics={
                "median": round(med, 4),
                "mad": round(mad, 4),
                "imputation_ratio": len(imputed) / n if n > 0 else 0
            }
        )
