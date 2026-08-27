"""episodic: Autobiographical memory for temporal context binding and experience replay.

Implements Recurrent Spatiotemporal Binding (RSB) and episodic decay exp(-t/tau).
Event boundaries are triggered via prediction error EWMA thresholds.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-EPISODIC"

class EpisodicError(ValueError): pass

@dataclass
class StateFrame:
    timestamp: float
    state_vector: List[float]
    prediction_error: float

@dataclass
class Episode:
    id: int
    start_time: float
    end_time: float
    frames: List[StateFrame]
    summary_vector: List[float]
    strength: float = 1.0

@dataclass
class EpisodicInput:
    state_vector: List[float]
    prediction_error: float
    timestamp: float
    tau: float = 100.0
    threshold: float = 0.5
    ewma_alpha: float = 0.2

@dataclass
class EpisodicOutput:
    agent_id: str
    boundary_detected: bool
    current_episode_frames: int
    ewma_error: float
    decayed_episodes_count: int
    active_strength: float
    execution_time_ms: float

class EpisodicAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.episodes: List[Episode] = []
        self.current_frames: List[StateFrame] = []
        self.ewma_error: float = 0.0
        self.episode_counter: int = 0
        self.current_start: float = 0.0

    def process(self, input_data: EpisodicInput) -> EpisodicOutput:
        start_time = time.perf_counter()
        
        # 1. Update EWMA prediction error
        if not self.current_frames:
            self.ewma_error = input_data.prediction_error
            self.current_start = input_data.timestamp
        else:
            self.ewma_error = (input_data.ewma_alpha * input_data.prediction_error) + \
                              ((1.0 - input_data.ewma_alpha) * self.ewma_error)

        # 2. Store current frame
        frame = StateFrame(input_data.timestamp, input_data.state_vector, input_data.prediction_error)
        self.current_frames.append(frame)

        boundary_detected = False
        
        # 3. Check for event boundary
        if self.ewma_error > input_data.threshold and len(self.current_frames) > 1:
            boundary_detected = True
            # Package episode
            summary = [sum(x)/len(self.current_frames) for x in zip(*[f.state_vector for f in self.current_frames])]
            ep = Episode(
                id=self.episode_counter,
                start_time=self.current_start,
                end_time=input_data.timestamp,
                frames=list(self.current_frames),
                summary_vector=summary
            )
            self.episodes.append(ep)
            self.episode_counter += 1
            self.current_frames.clear()
            self.ewma_error = 0.0 # reset

        # 4. Apply episodic decay exp(-t/tau)
        current_time = input_data.timestamp
        decayed_count = 0
        active_strength = 0.0
        for ep in self.episodes:
            dt = current_time - ep.end_time
            if dt > 0:
                ep.strength = math.exp(-dt / input_data.tau)
            if ep.strength < 0.01:
                decayed_count += 1
            active_strength += ep.strength

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return EpisodicOutput(
            agent_id=AGENT_ID,
            boundary_detected=boundary_detected,
            current_episode_frames=len(self.current_frames),
            ewma_error=self.ewma_error,
            decayed_episodes_count=decayed_count,
            active_strength=active_strength,
            execution_time_ms=elapsed_ms
        )

    def retrieve(self, cue_vector: List[float]) -> Optional[Episode]:
        # Simple cosine similarity retrieval
        best_ep = None
        best_score = -1.0
        for ep in self.episodes:
            dot = sum(a*b for a, b in zip(ep.summary_vector, cue_vector))
            norm_a = math.sqrt(sum(a*a for a in ep.summary_vector))
            norm_b = math.sqrt(sum(b*b for b in cue_vector))
            if norm_a == 0 or norm_b == 0:
                continue
            sim = dot / (norm_a * norm_b) * ep.strength # modulated by decay
            if sim > best_score:
                best_score = sim
                best_ep = ep
        return best_ep
