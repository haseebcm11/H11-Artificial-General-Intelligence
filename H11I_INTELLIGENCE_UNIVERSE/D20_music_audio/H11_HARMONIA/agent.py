import math
from dataclasses import dataclass
from typing import List, Optional

AGENT_ID = "H11_HARMONIA"

@dataclass
class AudioMetricsInput:
    midi_notes: List[int]
    amplitudes: List[float]
    reference_amplitude: float = 1e-5
    beats: int = 120
    duration_minutes: float = 1.0

@dataclass
class AudioMetricsOutput:
    frequencies_hz: List[float]
    decibels_db: List[float]
    tempo_bpm: float
    octave_ratio: float
    perfect_fifth_ratio: float

class DomainException(Exception):
    pass

class H11HarmoniaAgent:
    """
    Deeply domain-specific Audio & Music agent implementing exact mathematical models
    for acoustics and music theory. Includes MIDI to Hz conversion, Decibel calculation,
    and fundamental frequency ratios.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: AudioMetricsInput) -> AudioMetricsOutput:
        if not input_data.midi_notes:
            raise DomainException("MIDI notes cannot be empty")
            
        # 1. MIDI note to Hz: f = 440 * 2^((n - 69) / 12)
        freqs = [440.0 * (2.0 ** ((n - 69) / 12.0)) for n in input_data.midi_notes]
        
        # 2. dB = 20 * log10(A/A0)
        dbs = []
        for a in input_data.amplitudes:
            if a <= 0:
                dbs.append(0.0)
            else:
                dbs.append(20.0 * math.log10(a / input_data.reference_amplitude))
                
        # 3. Tempo BPM calculation
        if input_data.duration_minutes <= 0:
            raise DomainException("Duration must be positive")
        bpm = input_data.beats / input_data.duration_minutes
        
        # 4. Fundamental frequency ratios
        octave = 2.0 / 1.0
        fifth = 3.0 / 2.0
        
        return AudioMetricsOutput(
            frequencies_hz=freqs,
            decibels_db=dbs,
            tempo_bpm=bpm,
            octave_ratio=octave,
            perfect_fifth_ratio=fifth
        )
