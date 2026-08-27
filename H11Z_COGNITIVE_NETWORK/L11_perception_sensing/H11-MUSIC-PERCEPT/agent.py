"""
H11-MUSIC-PERCEPT: Music Perception
Layer 11 - Perception & Sensing
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum, auto
import numpy as np

class MusicFeature(Enum):
    BEAT = auto()
    TEMPO = auto()
    CHORD = auto()
    INSTRUMENT = auto()
    STRUCTURE = auto()
    ONSET = auto()
    PITCH = auto()

@dataclass
class BeatEvent:
    timestamp: float
    is_downbeat: bool
    confidence: float

@dataclass
class ChordSegment:
    start_time: float
    end_time: float
    root: str
    quality: str  # e.g., "maj", "min", "dim", "aug", "dom7"
    bass: Optional[str]
    confidence: float
    
    @property
    def label(self) -> str:
        base = f"{self.root}:{self.quality}"
        if self.bass and self.bass != self.root:
            base += f"/{self.bass}"
        return base

@dataclass
class NoteEvent:
    start_time: float
    end_time: float
    midi_pitch: int
    velocity: float
    instrument_id: Optional[str] = None

@dataclass
class MusicAnalysisResult:
    tempo_bpm: Optional[float] = None
    beats: List[BeatEvent] = field(default_factory=list)
    chords: List[ChordSegment] = field(default_factory=list)
    notes: List[NoteEvent] = field(default_factory=list)
    instruments: Dict[str, float] = field(default_factory=dict)
    key_signature: Optional[str] = None

class CQTAnalyzer:
    """Handles Constant-Q Transform computations for music analysis."""
    def __init__(self, sample_rate: int = 44100, bins_per_octave: int = 36, n_bins: int = 84):
        self.sr = sample_rate
        self.bins_per_octave = bins_per_octave
        self.n_bins = n_bins
        self.fmin = 32.70  # C1
        
    def compute_cqt(self, audio: np.ndarray) -> np.ndarray:
        # Placeholder for actual DSP/Librosa CQT logic
        # Returns a complex spectrogram representation
        frames = len(audio) // 512
        return np.random.randn(self.n_bins, frames) + 1j * np.random.randn(self.n_bins, frames)
        
    def compute_chromagram(self, cqt_mag: np.ndarray) -> np.ndarray:
        # Fold CQT bins into 12 pitch classes
        frames = cqt_mag.shape[1]
        chroma = np.zeros((12, frames))
        for b in range(self.n_bins):
            pitch_class = b % 12
            chroma[pitch_class, :] += cqt_mag[b, :]
        # Normalize
        norms = np.linalg.norm(chroma, axis=0) + 1e-6
        return chroma / norms

class RhythmProcessor:
    """Beat and tempo tracking using onset detection and dynamic programming."""
    
    def calculate_onset_strength(self, spectrogram: np.ndarray) -> np.ndarray:
        # Spectral flux
        diff = np.diff(spectrogram, axis=1)
        diff[diff < 0] = 0
        return np.sum(diff, axis=0)
        
    def estimate_tempo(self, onset_env: np.ndarray, sr: int, hop_length: int) -> float:
        # Autocorrelation based tempo estimation placeholder
        return 120.0
        
    def track_beats(self, onset_env: np.ndarray, tempo: float) -> List[BeatEvent]:
        # Placeholder for Ellis dynamic programming beat tracking
        beats = []
        hop_duration = 512 / 44100.0
        interval = 60.0 / tempo
        curr_time = 0.5
        while curr_time < (len(onset_env) * hop_duration):
            beats.append(BeatEvent(timestamp=curr_time, is_downbeat=(len(beats) % 4 == 0), confidence=0.85))
            curr_time += interval
        return beats

class HarmonyAnalyzer:
    """HMM-based chord recognition over chromagrams."""
    
    def __init__(self):
        self.chord_templates = self._build_templates()
        
    def _build_templates(self) -> Dict[str, np.ndarray]:
        # 12 major + 12 minor templates
        templates = {}
        roots = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        for i, r in enumerate(roots):
            maj = np.zeros(12); maj[i]=1; maj[(i+4)%12]=1; maj[(i+7)%12]=1
            min_ = np.zeros(12); min_[i]=1; min_[(i+3)%12]=1; min_[(i+7)%12]=1
            templates[f"{r}:maj"] = maj / np.sum(maj)
            templates[f"{r}:min"] = min_ / np.sum(min_)
        return templates

    def recognize_chords(self, chromagram: np.ndarray, times: np.ndarray) -> List[ChordSegment]:
        chords = []
        frames = chromagram.shape[1]
        
        # Greedy template matching placeholder
        template_keys = list(self.chord_templates.keys())
        template_matrix = np.array(list(self.chord_templates.values())) # (24, 12)
        
        # (24, 12) dot (12, frames) -> (24, frames)
        scores = template_matrix @ chromagram
        best_indices = np.argmax(scores, axis=0)
        
        current_chord = None
        start_t = 0.0
        
        for i in range(frames):
            chord_name = template_keys[best_indices[i]]
            t = times[i]
            if current_chord != chord_name:
                if current_chord is not None:
                    root, qual = current_chord.split(':')
                    chords.append(ChordSegment(start_t, t, root, qual, None, 0.9))
                current_chord = chord_name
                start_t = t
                
        if current_chord is not None:
            root, qual = current_chord.split(':')
            chords.append(ChordSegment(start_t, times[-1], root, qual, None, 0.9))
            
        return self._smooth_chords(chords)
        
    def _smooth_chords(self, chords: List[ChordSegment]) -> List[ChordSegment]:
        # Viterbi decoding / median filtering placeholder
        return chords

class MusicPerceptionAgent:
    """
    H11-MUSIC-PERCEPT Agent
    Analyzes audio streams for musical content: rhythm, harmony, melody.
    """
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.cqt_analyzer = CQTAnalyzer(sample_rate=self.sample_rate)
        self.rhythm_processor = RhythmProcessor()
        self.harmony_analyzer = HarmonyAnalyzer()
        
    def process_audio(self, audio_data: np.ndarray, requested_features: List[MusicFeature]) -> MusicAnalysisResult:
        if audio_data.ndim > 1:
            # Downmix to mono
            audio_data = np.mean(audio_data, axis=1)
            
        result = MusicAnalysisResult()
        
        # 1. Feature Extraction
        cqt_complex = self.cqt_analyzer.compute_cqt(audio_data)
        cqt_mag = np.abs(cqt_complex)
        
        time_vector = np.arange(cqt_mag.shape[1]) * (512 / self.sample_rate)
        
        # 2. Rhythm Analysis
        if MusicFeature.BEAT in requested_features or MusicFeature.TEMPO in requested_features:
            onset_env = self.rhythm_processor.calculate_onset_strength(cqt_mag)
            result.tempo_bpm = self.rhythm_processor.estimate_tempo(onset_env, self.sample_rate, 512)
            
            if MusicFeature.BEAT in requested_features:
                result.beats = self.rhythm_processor.track_beats(onset_env, result.tempo_bpm)
                
        # 3. Harmonic Analysis
        if MusicFeature.CHORD in requested_features:
            chroma = self.cqt_analyzer.compute_chromagram(cqt_mag)
            result.chords = self.harmony_analyzer.recognize_chords(chroma, time_vector)
            
        # 4. Instrument ID (Placeholder)
        if MusicFeature.INSTRUMENT in requested_features:
            result.instruments = {"piano": 0.8, "acoustic_guitar": 0.15, "drums": 0.9}
            
        return result

    def get_music_summary(self, result: MusicAnalysisResult) -> str:
        lines = ["Music Perception Summary:"]
        if result.tempo_bpm:
            lines.append(f"- Tempo: {result.tempo_bpm:.1f} BPM")
        if result.chords:
            lines.append(f"- Chord Progression: {' -> '.join(c.label for c in result.chords[:5])} ...")
        if result.instruments:
            lines.append("- Dominant Instruments:")
            for inst, prob in sorted(result.instruments.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"  * {inst}: {prob:.0%}")
        return "\n".join(lines)
