import math
from dataclasses import dataclass
from typing import List, Tuple

AGENT_ID = "H11-BEAM"

@dataclass
class BeamState:
    sequence: List[int]
    log_prob: float

@dataclass
class BeamInput:
    current_beams: List[BeamState]
    next_token_log_probs: List[List[float]]
    beam_width: int
    length_penalty_alpha: float

@dataclass
class BeamOutput:
    top_beams: List[BeamState]

class BeamException(Exception):
    pass

class H11BeamAgent:
    """
    Beam search decoding with length penalty.
    Score = sum(log P) / (length ^ alpha)
    """
    def process(self, input_data: BeamInput) -> BeamOutput:
        candidates = []
        
        for i, beam in enumerate(input_data.current_beams):
            probs = input_data.next_token_log_probs[i]
            for token_id, lp in enumerate(probs):
                new_seq = beam.sequence + [token_id]
                new_lp = beam.log_prob + lp
                
                # Length penalty
                score = new_lp / (len(new_seq) ** input_data.length_penalty_alpha)
                candidates.append((score, BeamState(new_seq, new_lp)))
                
        # Sort by score descending
        candidates.sort(key=lambda x: x[0], reverse=True)
        
        top_beams = [c[1] for c in candidates[:input_data.beam_width]]
        return BeamOutput(top_beams=top_beams)
