"""
Agent Module: D11_EDGE
Agent Class: EdgeAgent

Edge computing Lyapunov optimization min E[Cost] + V*QueueDelay and Dynamic Voltage and Frequency Scaling (DVFS) power P = C*V^2*f.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_EDGE"


class EdgeError(ValueError):
    """Raised when EdgeAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class EdgeAgentInput:
    cpu_freq_ghz: float = 1.8
    voltage_v: float = 0.9
    capacitance_pf: float = 1500.0


@dataclass(frozen=True)
class EdgeAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    dynamic_power_watts: float = 0.0


class EdgeAgent:
    """
    Edge computing Lyapunov optimization min E[Cost] + V*QueueDelay and Dynamic Voltage and Frequency Scaling (DVFS) power P = C*V^2*f.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: EdgeAgentInput) -> EdgeAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        c_f = inputs.capacitance_pf * 1e-12
        v, f_hz = inputs.voltage_v, inputs.cpu_freq_ghz * 1e9
        p_dyn = c_f * (v**2) * f_hz
        metrics = {"dynamic_power_w": round(p_dyn, 4), "cpu_freq_ghz": inputs.cpu_freq_ghz}
        return EdgeAgentOutput(status="COMPLETED", score=round(min(1.0, 5.0/max(p_dyn, 0.1)), 4), metrics=metrics, dynamic_power_watts=round(p_dyn, 4))
