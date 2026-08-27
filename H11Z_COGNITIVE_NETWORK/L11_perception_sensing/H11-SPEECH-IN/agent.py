"""
Agent Module: L11_SPEECH_IN
Agent Class: SpeechInAgent

Acoustic audio frontend processing with pre-emphasis filter y[n] = x[n] - alpha*x[n-1], Hamming windowing, and energy Voice Activity Detection (VAD).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L11_SPEECH_IN"


class SpeechInError(ValueError):
    """Raised when SpeechInAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SpeechInAgentInput:
    audio_samples: list[float] = field(default_factory=lambda: [0.05*i for i in range(16)])
    pre_emphasis: float = 0.97
    energy_threshold: float = 0.01


@dataclass(frozen=True)
class SpeechInAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    emphasized_signal: list[float] = field(default_factory=list)


class SpeechInAgent:
    """
    Acoustic audio frontend processing with pre-emphasis filter y[n] = x[n] - alpha*x[n-1], Hamming windowing, and energy Voice Activity Detection (VAD).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SpeechInAgentInput) -> SpeechInAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        x = inputs.audio_samples if inputs.audio_samples else [0.0]*10
        alpha = inputs.pre_emphasis
        y = [x[0]] + [x[i] - alpha * x[i-1] for i in range(1, len(x))]
        windowed = [y[i] * (0.54 - 0.46 * math.cos(2 * math.pi * i / max(len(y)-1, 1))) for i in range(len(y))]
        energy = sum(s*s for s in windowed) / max(len(windowed), 1)
        vad = 1.0 if energy >= inputs.energy_threshold else 0.0
        score = round(min(1.0, energy * 10.0), 4)
        metrics = {"frame_energy": round(energy, 6), "vad_active": vad, "pre_emphasis_factor": alpha}
        return SpeechInAgentOutput(status="COMPLETED", score=score, metrics=metrics, emphasized_signal=[round(v, 4) for v in y])
