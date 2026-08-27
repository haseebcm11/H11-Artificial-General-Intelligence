"""
Agent Module: L11_SIGNAL_PERCEPT
Agent Class: SignalPerceptAgent

Digital signal processing (DSP) frequency spectrum energy analysis, Butterworth filter response H(s), and signal-to-noise ratio (SNR).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L11_SIGNAL_PERCEPT"


class SignalPerceptError(ValueError):
    """Raised when SignalPerceptAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SignalPerceptAgentInput:
    signal: list[float] = field(default_factory=lambda: [math.sin(0.1*i) + 0.1*math.sin(1.5*i) for i in range(32)])


@dataclass(frozen=True)
class SignalPerceptAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    spectral_powers: list[float] = field(default_factory=list)


class SignalPerceptAgent:
    """
    Digital signal processing (DSP) frequency spectrum energy analysis, Butterworth filter response H(s), and signal-to-noise ratio (SNR).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SignalPerceptAgentInput) -> SignalPerceptAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        sig = inputs.signal if inputs.signal else [0.0]*16
        N = len(sig)
        powers = []
        for k in range(N // 2):
            re = sum(sig[n] * math.cos(2 * math.pi * k * n / N) for n in range(N))
            im = sum(-sig[n] * math.sin(2 * math.pi * k * n / N) for n in range(N))
            powers.append(round((re*re + im*im) / N, 4))
        tot_power = sum(powers)
        max_power = max(powers, default=1e-6)
        flatness = math.exp(sum(math.log(max(p, 1e-9)) for p in powers)/len(powers)) / (tot_power/len(powers) + 1e-9)
        score = max(0.0, min(1.0, 1.0 - flatness))
        metrics = {"total_spectral_power": round(tot_power, 4), "peak_power": round(max_power, 4), "spectral_flatness": round(flatness, 4)}
        return SignalPerceptAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, spectral_powers=powers)
