"""
Agent Module: L11_SENSOR
Agent Class: SensorAgent

Multi-modal sensor telemetry fusion with 1D Kalman filter state estimation and covariance propagation P = F P F^T + Q.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L11_SENSOR"


class SensorError(ValueError):
    """Raised when SensorAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SensorAgentInput:
    measurements: list[float] = field(default_factory=lambda: [10.2, 10.5, 9.8, 10.1, 11.0, 9.9])
    process_variance: float = 0.05
    measurement_variance: float = 0.5


@dataclass(frozen=True)
class SensorAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    filtered_states: list[float] = field(default_factory=list)


class SensorAgent:
    """
    Multi-modal sensor telemetry fusion with 1D Kalman filter state estimation and covariance propagation P = F P F^T + Q.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SensorAgentInput) -> SensorAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        meas = inputs.measurements if inputs.measurements else [1.0, 1.1, 0.9]
        q, r = inputs.process_variance, inputs.measurement_variance
        x_est, p_est = meas[0], 1.0
        filtered = []
        for z in meas:
            p_pred = p_est + q
            k_gain = p_pred / (p_pred + r)
            x_est = x_est + k_gain * (z - x_est)
            p_est = (1.0 - k_gain) * p_pred
            filtered.append(round(x_est, 4))
        residual_var = sum((z - x)**2 for z, x in zip(meas, filtered)) / len(meas)
        score = min(1.0, 1.0 / (1.0 + residual_var))
        metrics = {"final_estimate": round(x_est, 4), "final_covariance": round(p_est, 4), "residual_variance": round(residual_var, 4)}
        return SensorAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, filtered_states=filtered)
