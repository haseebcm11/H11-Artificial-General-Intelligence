"""
Agent Module: L12_DYNAMICS
Agent Class: DynamicsAgent

Forward dynamics state transition model with Runge-Kutta 4th order (RK4) ODE integration and kinetic energy conservation.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L12_DYNAMICS"


class DynamicsError(ValueError):
    """Raised when DynamicsAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class DynamicsAgentInput:
    state: list[float] = field(default_factory=lambda: [1.0, 0.0])
    dt: float = 0.05
    omega_sq: float = 4.0


@dataclass(frozen=True)
class DynamicsAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    next_state: list[float] = field(default_factory=list)


class DynamicsAgent:
    """
    Forward dynamics state transition model with Runge-Kutta 4th order (RK4) ODE integration and kinetic energy conservation.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: DynamicsAgentInput) -> DynamicsAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        x = inputs.state[0] if len(inputs.state) > 0 else 1.0
        v = inputs.state[1] if len(inputs.state) > 1 else 0.0
        dt, w2 = inputs.dt, inputs.omega_sq
        def deriv(x_curr, v_curr): return v_curr, -w2 * x_curr
        k1_x, k1_v = deriv(x, v)
        k2_x, k2_v = deriv(x + 0.5*dt*k1_x, v + 0.5*dt*k1_v)
        k3_x, k3_v = deriv(x + 0.5*dt*k2_x, v + 0.5*dt*k2_v)
        k4_x, k4_v = deriv(x + dt*k3_x, v + dt*k3_v)
        x_next = x + (dt/6.0)*(k1_x + 2*k2_x + 2*k3_x + k4_x)
        v_next = v + (dt/6.0)*(k1_v + 2*k2_v + 2*k3_v + k4_v)
        e_init = 0.5*v**2 + 0.5*w2*x**2
        e_final = 0.5*v_next**2 + 0.5*w2*x_next**2
        e_error = abs(e_final - e_init) / max(e_init, 1e-6)
        score = max(0.0, 1.0 - min(1.0, e_error))
        metrics = {"initial_energy": round(e_init, 4), "final_energy": round(e_final, 4), "energy_error": round(e_error, 6)}
        return DynamicsAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, next_state=[round(x_next, 4), round(v_next, 4)])
