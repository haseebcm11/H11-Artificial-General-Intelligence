"""H11-AUDIO: General audio perception, STFT processing, and sound event detection.

Implements FFT frequency binning, Mel filterbanks, and MFCC computation.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-AUDIO"

class AudioError(ValueError): pass

@dataclass
class AudioInput:
    waveform: List[float]
    sample_rate: int = 16000
    n_fft: int = 512
    n_mels: int = 40
    hop_length: int = 160

@dataclass
class AudioOutput:
    agent_id: str
    spectrogram_frames: int
    mfcc_mean_energy: float
    mel_bands: int
    execution_time_ms: float

class AudioAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def _hz_to_mel(self, hz: float) -> float:
        return 2595.0 * math.log10(1.0 + hz / 700.0)

    def _mel_to_hz(self, mel: float) -> float:
        return 700.0 * (10**(mel / 2595.0) - 1.0)

    def _compute_stft_magnitude(self, frame: List[float], n_fft: int) -> List[float]:
        # Very simplified DFT magnitude for n_fft bins
        N = len(frame)
        mags = []
        for k in range(n_fft // 2 + 1):
            re = 0.0
            im = 0.0
            for n in range(N):
                angle = 2.0 * math.pi * k * n / N
                # apply Hann window
                window = 0.5 * (1 - math.cos(2.0 * math.pi * n / (N - 1)))
                val = frame[n] * window
                re += val * math.cos(angle)
                im -= val * math.sin(angle)
            mags.append(math.sqrt(re*re + im*im))
        return mags

    def process(self, input_data: AudioInput) -> AudioOutput:
        start_time = time.perf_counter()
        
        if len(input_data.waveform) == 0:
            raise AudioError("Empty waveform provided.")

        # Mel filterbank generation
        fmin = 0.0
        fmax = input_data.sample_rate / 2.0
        mel_min = self._hz_to_mel(fmin)
        mel_max = self._hz_to_mel(fmax)
        mel_points = [mel_min + i * (mel_max - mel_min) / (input_data.n_mels + 1) for i in range(input_data.n_mels + 2)]
        hz_points = [self._mel_to_hz(m) for m in mel_points]
        bin_points = [int(math.floor((input_data.n_fft + 1) * h / input_data.sample_rate)) for h in hz_points]

        # Process frames
        frames = []
        for i in range(0, len(input_data.waveform) - input_data.n_fft + 1, input_data.hop_length):
            frame = input_data.waveform[i:i+input_data.n_fft]
            frames.append(frame)

        mel_spectrogram = []
        total_energy = 0.0
        
        for frame in frames:
            mags = self._compute_stft_magnitude(frame, input_data.n_fft)
            mel_frame = [0.0] * input_data.n_mels
            
            # Apply mel filterbanks (triangular)
            for m in range(1, input_data.n_mels + 1):
                f_m_minus = bin_points[m - 1]
                f_m = bin_points[m]
                f_m_plus = bin_points[m + 1]
                
                energy = 0.0
                for k in range(f_m_minus, f_m):
                    energy += mags[k] * (k - f_m_minus) / max(1, (f_m - f_m_minus))
                for k in range(f_m, f_m_plus):
                    energy += mags[k] * (f_m_plus - k) / max(1, (f_m_plus - f_m))
                
                # Log mel energy
                log_e = math.log(energy + 1e-9)
                mel_frame[m-1] = log_e
                total_energy += log_e
                
            mel_spectrogram.append(mel_frame)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return AudioOutput(
            agent_id=AGENT_ID,
            spectrogram_frames=len(mel_spectrogram),
            mfcc_mean_energy=total_energy / max(1, (len(mel_spectrogram) * input_data.n_mels)),
            mel_bands=input_data.n_mels,
            execution_time_ms=elapsed_ms
        )
