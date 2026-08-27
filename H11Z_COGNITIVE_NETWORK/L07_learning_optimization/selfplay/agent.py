import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-SELFPLAY"

@dataclass
class SelfplayInput:
    agent_1_rating: float
    agent_2_rating: float
    match_outcome: float # 1.0 for agent 1 win, 0.5 draw, 0.0 for agent 2 win
    k_factor: float = 32.0
    scale_factor: float = 400.0

@dataclass
class SelfplayOutput:
    new_agent_1_rating: float
    new_agent_2_rating: float
    expected_score_1: float

class SelfplayException(Exception):
    pass

class SelfplayAgent:
    """
    Implements Elo Rating System for Self-Play in the H11 Cognitive Substrate.
    Features:
    - Expected score calculation
    - K-factor scaling
    - Zero-sum rating updates
    """
    def __init__(self):
        self.match_count = 0

    def process(self, input_data: SelfplayInput) -> SelfplayOutput:
        if input_data.match_outcome < 0.0 or input_data.match_outcome > 1.0:
            raise SelfplayException("Match outcome must be in [0.0, 1.0].")
            
        self.match_count += 1
        
        r1 = input_data.agent_1_rating
        r2 = input_data.agent_2_rating
        
        # Expected score: E_A = 1 / (1 + 10^((R_B - R_A) / 400))
        power = (r2 - r1) / input_data.scale_factor
        e1 = 1.0 / (1.0 + math.pow(10.0, power))
        e2 = 1.0 - e1
        
        s1 = input_data.match_outcome
        s2 = 1.0 - s1
        
        k = input_data.k_factor
        
        # Updates
        new_r1 = r1 + k * (s1 - e1)
        new_r2 = r2 + k * (s2 - e2)
        
        return SelfplayOutput(
            new_agent_1_rating=new_r1,
            new_agent_2_rating=new_r2,
            expected_score_1=e1
        )
