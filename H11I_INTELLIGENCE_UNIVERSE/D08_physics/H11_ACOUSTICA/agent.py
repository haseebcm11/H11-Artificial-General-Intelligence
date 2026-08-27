"""
Agent Module: D08_ACOUSTICA
Agent Class: AcousticaAgent

Acoustic impedance Z = rho*c, Sound Pressure Level SPL = 20*log10(p_rms/p_0), and Doppler frequency shift.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D08_ACOUSTICA"


class AcousticaError(ValueError):
    """Raised when AcousticaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class AcousticaAgentInput:
    pressure_pa: float = 2.0
    density_kg_m3: float = 1.225
    sound_speed_m_s: float = 343.0
    source_velocity_m_s: float = 30.0
    freq_hz: float = 1000.0


@dataclass(frozen=True)
class AcousticaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    spl_db: float = 0.0
    doppler_freq_hz: float = 0.0


class AcousticaAgent:
    """
    Acoustic impedance Z = rho*c, Sound Pressure Level SPL = 20*log10(p_rms/p_0), and Doppler frequency shift.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: AcousticaAgentInput) -> AcousticaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        p, rho, c, vs, f = inputs.pressure_pa, inputs.density_kg_m3, inputs.sound_speed_m_s, inputs.source_velocity_m_s, inputs.freq_hz
        p0 = 20e-6  # reference pressure 20 microPa
        spl = 20.0 * math.log10(max(p, 1e-9) / p0)
        z = rho * c
        f_doppler = f * (c / max(c - vs, 1e-6))
        metrics = {"spl_db": round(spl, 2), "acoustic_impedance_rayls": round(z, 1), "doppler_freq_hz": round(f_doppler, 2)}
        return AcousticaAgentOutput(status="COMPLETED", score=round(min(1.0, spl/120.0), 4), metrics=metrics, spl_db=round(spl, 2), doppler_freq_hz=round(f_doppler, 2))
