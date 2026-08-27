import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum, auto

AGENT_ID = "H11-MUSICGEN"

class MusicgenStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()
    DEGRADED = auto()
    FAILED = auto()

class MusicgenError(ValueError):
    pass

@dataclass(frozen=True)
class MusicgenInput:
    target_id: str = "default_target"
    intensity: float = 1.0
    batch_size: int = 32
    tolerance: float = 1e-4
    parameters: Dict[str, float] = field(default_factory=lambda: {"alpha": 0.5, "beta": 0.9, "scale": 1.0})
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class MusicgenOutput:
    agent_id: str
    status: str
    efficiency_score: float
    computed_value: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class MusicgenAgent:
    """Analytical engine for H11-MUSICGEN. Implements MIDI pitch to frequency 
    conversion and harmonic overtone series math."""
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "status": MusicgenStatus.IDLE.name}

    def process(self, input_data: Optional[MusicgenInput] = None) -> MusicgenOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = MusicgenInput()

        intensity = float(input_data.intensity)
        
        # MIDI note 69 is A4 (440 Hz). We simulate generating a note.
        # Let's say intensity maps to an octave range (48 to 84)
        midi_note = 48 + int(intensity * 36)
        
        # f = 440 * 2^((d-69)/12)
        frequency = 440.0 * math.pow(2.0, (midi_note - 69.0) / 12.0)
        
        # Harmonic overtone energies (1/n^2)
        num_harmonics = 5
        harmonic_energy = 0.0
        for n in range(1, num_harmonics + 1):
            harmonic_energy += 1.0 / (n ** 2)
            
        # Spectral centroid approximation
        spectral_centroid = frequency * (harmonic_energy / sum(1.0/n for n in range(1, num_harmonics + 1)))
        
        # Efficiency based on how well it fits human hearing range (20Hz - 20kHz)
        if 20.0 <= frequency <= 20000.0:
            efficiency = 1.0
        else:
            efficiency = 0.0

        status = MusicgenStatus.OPTIMAL.name if efficiency > 0.8 else MusicgenStatus.ACTIVE.name
        self.state["evaluations_count"] = self.state.get("evaluations_count", 0) + 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        
        return MusicgenOutput(
            agent_id=AGENT_ID,
            status=status,
            efficiency_score=efficiency,
            computed_value=frequency,
            execution_time_ms=elapsed_ms,
            metrics={"midi_note": float(midi_note), "frequency": frequency, "spectral_centroid": spectral_centroid},
            diagnostics=["MIDI frequency and harmonic series computed."]
        )
