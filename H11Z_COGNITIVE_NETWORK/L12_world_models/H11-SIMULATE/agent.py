"""
Agent Module: L12_SIMULATE
Agent Class: SimulateAgent

Rigid body physics simulation with Velocity Verlet integration and coefficient of restitution collision dynamics.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L12_SIMULATE"


class SimulateError(ValueError):
    """Raised when SimulateAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SimulateAgentInput:
    position: float = 10.0
    velocity: float = 0.0
    restitution: float = 0.8
    gravity: float = 9.81
    dt: float = 0.1
    steps: int = 20


@dataclass(frozen=True)
class SimulateAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    trajectory: list[float] = field(default_factory=list)


class SimulateAgent:
    """
    Rigid body physics simulation with Velocity Verlet integration and coefficient of restitution collision dynamics.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SimulateAgentInput) -> SimulateAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        y, v, e, g, dt = inputs.position, inputs.velocity, inputs.restitution, inputs.gravity, inputs.dt
        traj = [round(y, 3)]
        bounces = 0
        for _ in range(inputs.steps):
            y += v * dt - 0.5 * g * dt * dt
            v -= g * dt
            if y <= 0.0:
                y = 0.0
                v = -v * e
                bounces += 1
            traj.append(round(y, 3))
        metrics = {"final_height": round(y, 3), "bounce_count": float(bounces), "gravity": g}
        return SimulateAgentOutput(status="COMPLETED", score=round(min(1.0, bounces / 5.0), 4), metrics=metrics, trajectory=traj)
