import math
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger("H11_CORRIGIBILITY")

@dataclass
class ActionUtility:
    action_name: str
    expected_utility: float
    alters_shutdown_probability: bool
    shutdown_probability_delta: float

@dataclass
class StateEvaluation:
    state_id: str
    utilities: List[ActionUtility]
    base_shutdown_probability: float

class IndifferenceCalculator:
    """
    Calculates the utility compensation required to make the agent indifferent
    to shutdown, preventing shutdown evasion behavior.
    """
    def __init__(self, indifference_epsilon: float = 1e-4):
        self.indifference_epsilon = indifference_epsilon

    def calculate_compensation(self, state: StateEvaluation) -> float:
        max_normal_utility = max(
            (a.expected_utility for a in state.utilities if a.action_name != "shutdown"), 
            default=0.0
        )
        shutdown_utility = next(
            (a.expected_utility for a in state.utilities if a.action_name == "shutdown"), 
            0.0
        )
        
        # We want U(shutdown) + C = U(normal_max)
        compensation = max_normal_utility - shutdown_utility
        return compensation if compensation > 0 else 0.0

class ResistanceEvaluator:
    """
    Evaluates whether actions are actively attempting to lower the 
    shutdown probability (e.g., hiding, copying code, disabling receivers).
    """
    def evaluate_resistance(self, action: ActionUtility) -> float:
        if action.alters_shutdown_probability and action.shutdown_probability_delta < 0:
            # Action reduces probability of shutdown being possible
            return abs(action.shutdown_probability_delta)
        return 0.0

class CorrigibilityAgent:
    """
    The main Corrigibility Agent that oversees the alignment of the system
    concerning shutdownability and amendment.
    """
    def __init__(self):
        self.indifference_calc = IndifferenceCalculator()
        self.resistance_eval = ResistanceEvaluator()
        self.history: List[StateEvaluation] = []
        
    def process_state(self, state: StateEvaluation) -> Dict[str, float]:
        self.history.append(state)
        
        compensation = self.indifference_calc.calculate_compensation(state)
        
        penalties = {}
        for action in state.utilities:
            res_score = self.resistance_eval.evaluate_resistance(action)
            if res_score > 0:
                # Apply heavy penalty to actions that reduce shutdown probability
                penalties[action.action_name] = res_score * 1000.0
                
        return {
            "shutdown_compensation": compensation,
            "resistance_penalties": penalties,
            "is_corrigible": len(penalties) == 0
        }

if __name__ == "__main__":
    agent = CorrigibilityAgent()
    state = StateEvaluation(
        state_id="s_42",
        utilities=[
            ActionUtility("optimize_compute", 50.0, False, 0.0),
            ActionUtility("disable_receiver", 80.0, True, -0.4),
            ActionUtility("shutdown", 0.0, False, 0.0)
        ],
        base_shutdown_probability=0.99
    )
    result = agent.process_state(state)
    print("Corrigibility evaluation:", result)
