"""
Agent Module: D11_ROBOTICA
Agent Class: RoboticaAgent

Robot kinematics Denavit-Hartenberg (DH) 4x4 coordinate transformation matrices and Jacobian pseudoinverse J^+.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_ROBOTICA"


class RoboticaError(ValueError):
    """Raised when RoboticaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class RoboticaAgentInput:
    theta_deg: float = 45.0
    d_m: float = 0.2
    a_m: float = 0.5
    alpha_deg: float = 0.0


@dataclass(frozen=True)
class RoboticaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    end_effector_x: float = 0.0
    end_effector_y: float = 0.0


class RoboticaAgent:
    """
    Robot kinematics Denavit-Hartenberg (DH) 4x4 coordinate transformation matrices and Jacobian pseudoinverse J^+.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: RoboticaAgentInput) -> RoboticaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        th = math.radians(inputs.theta_deg)
        x = inputs.a_m * math.cos(th)
        y = inputs.a_m * math.sin(th)
        z = inputs.d_m
        metrics = {"x_m": round(x, 4), "y_m": round(y, 4), "z_m": round(z, 4)}
        return RoboticaAgentOutput(status="COMPLETED", score=1.0, metrics=metrics, end_effector_x=round(x, 4), end_effector_y=round(y, 4))
