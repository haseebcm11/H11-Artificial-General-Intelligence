"""
Agent Module: D08_OPTICA
Agent Class: OpticaAgent

Geometric and physical optics: Snell's Law n1*sin(th1) = n2*sin(th2) and Gaussian beam Rayleigh range z_R = pi*w0^2 / lambda.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D08_OPTICA"


class OpticaError(ValueError):
    """Raised when OpticaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class OpticaAgentInput:
    n1: float = 1.0
    n2: float = 1.5
    theta1_deg: float = 45.0
    waist_radius_um: float = 10.0
    wavelength_nm: float = 632.8


@dataclass(frozen=True)
class OpticaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    refraction_angle_deg: float = 0.0
    rayleigh_range_mm: float = 0.0


class OpticaAgent:
    """
    Geometric and physical optics: Snell's Law n1*sin(th1) = n2*sin(th2) and Gaussian beam Rayleigh range z_R = pi*w0^2 / lambda.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: OpticaAgentInput) -> OpticaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        n1, n2, th1 = inputs.n1, inputs.n2, math.radians(inputs.theta1_deg)
        sin_th2 = (n1 * math.sin(th1)) / n2
        th2_deg = math.degrees(math.asin(max(-1.0, min(1.0, sin_th2)))) if abs(sin_th2) <= 1.0 else 90.0
        w0_m = inputs.waist_radius_um * 1e-6
        lam_m = inputs.wavelength_nm * 1e-9
        zr_mm = (math.pi * (w0_m**2) / lam_m) * 1000.0
        metrics = {"theta2_deg": round(th2_deg, 2), "rayleigh_range_mm": round(zr_mm, 2)}
        return OpticaAgentOutput(status="COMPLETED", score=round(min(1.0, zr_mm/10.0), 4), metrics=metrics, refraction_angle_deg=round(th2_deg, 2), rayleigh_range_mm=round(zr_mm, 2))
