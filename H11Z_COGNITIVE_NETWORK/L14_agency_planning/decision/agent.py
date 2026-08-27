import math
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Callable
from enum import Enum

class RiskProfile(Enum):
    AVERSE = 1
    NEUTRAL = 2
    SEEKING = 3

@dataclass
class Criteria:
    name: str
    weight: float
    is_benefit: bool # True if higher is better (profit), False if lower is better (cost)

@dataclass
class Alternative:
    name: str
    attributes: Dict[str, float]

class MCDAEngine:
    """
    Multi-Criteria Decision Analysis using TOPSIS 
    (Technique for Order of Preference by Similarity to Ideal Solution)
    """
    def __init__(self, criteria: List[Criteria]):
        self.criteria = criteria
        self.criteria_dict = {c.name: c for c in criteria}

    def topsis(self, alternatives: List[Alternative]) -> List[Tuple[str, float]]:
        if not alternatives or not self.criteria:
            return []

        # 1. Create evaluation matrix
        m = len(alternatives)
        n = len(self.criteria)
        matrix = np.zeros((m, n))
        
        for i, alt in enumerate(alternatives):
            for j, crit in enumerate(self.criteria):
                matrix[i, j] = alt.attributes.get(crit.name, 0.0)

        # 2. Normalize the matrix
        sq_sum = np.sqrt(np.sum(matrix**2, axis=0))
        # Handle zero division for identical vectors
        sq_sum[sq_sum == 0] = 1.0
        norm_matrix = matrix / sq_sum

        # 3. Apply criteria weights
        weights = np.array([c.weight for c in self.criteria])
        weighted_matrix = norm_matrix * weights

        # 4. Determine ideal and negative-ideal solutions
        ideal_solution = np.zeros(n)
        anti_ideal_solution = np.zeros(n)

        for j, crit in enumerate(self.criteria):
            if crit.is_benefit:
                ideal_solution[j] = np.max(weighted_matrix[:, j])
                anti_ideal_solution[j] = np.min(weighted_matrix[:, j])
            else:
                ideal_solution[j] = np.min(weighted_matrix[:, j])
                anti_ideal_solution[j] = np.max(weighted_matrix[:, j])

        # 5. Calculate separation measures (Euclidean distance)
        dist_to_ideal = np.sqrt(np.sum((weighted_matrix - ideal_solution)**2, axis=1))
        dist_to_anti_ideal = np.sqrt(np.sum((weighted_matrix - anti_ideal_solution)**2, axis=1))

        # 6. Calculate relative closeness to ideal solution
        denominator = dist_to_ideal + dist_to_anti_ideal
        # Prevent division by zero if all alternatives are identical
        denominator[denominator == 0] = 1e-9
        closeness = dist_to_anti_ideal / denominator

        # Rank alternatives by descending closeness
        ranked = sorted(zip([a.name for a in alternatives], closeness), key=lambda x: x[1], reverse=True)
        return ranked


@dataclass
class State:
    id: str
    is_terminal: bool = False

@dataclass
class Action:
    id: str

class MDPEngine:
    """
    Sequential Decision Making under uncertainty using Markov Decision Processes (MDP).
    Solved via Value Iteration algorithm.
    """
    def __init__(self, states: List[State], actions: List[Action], gamma: float = 0.9):
        self.states = {s.id: s for s in states}
        self.actions = {a.id: a for a in actions}
        self.gamma = gamma
        self.transitions: Dict[str, Dict[str, List[Tuple[str, float]]]] = {} 
        self.rewards: Dict[str, Dict[str, float]] = {} 
        self.V: Dict[str, float] = {s.id: 0.0 for s in states}
        self.policy: Dict[str, str] = {}

    def set_transition(self, state_id: str, action_id: str, next_state_probs: List[Tuple[str, float]]):
        if state_id not in self.transitions:
            self.transitions[state_id] = {}
        # Ensure probabilities sum to 1
        total_prob = sum(p for _, p in next_state_probs)
        if total_prob == 0:
            return
        normalized_probs = [(s, p/total_prob) for s, p in next_state_probs]
        self.transitions[state_id][action_id] = normalized_probs

    def set_reward(self, state_id: str, action_id: str, reward: float):
        if state_id not in self.rewards:
            self.rewards[state_id] = {}
        self.rewards[state_id][action_id] = reward

    def value_iteration(self, epsilon: float = 1e-6, max_iter: int = 1000):
        for _ in range(max_iter):
            delta = 0.0
            new_V = self.V.copy()
            for state_id, state in self.states.items():
                if state.is_terminal:
                    continue
                
                max_v = float('-inf')
                best_a = None
                
                actions_available = self.transitions.get(state_id, {})
                if not actions_available:
                    continue
                    
                for action_id, transitions in actions_available.items():
                    # Calculate Expected Value from Bellman Optimality Equation
                    q_value = self.rewards.get(state_id, {}).get(action_id, 0.0)
                    for next_s, prob in transitions:
                        q_value += prob * self.gamma * self.V[next_s]
                        
                    if q_value > max_v:
                        max_v = q_value
                        best_a = action_id
                        
                if best_a is not None:
                    new_V[state_id] = max_v
                    self.policy[state_id] = best_a
                    delta = max(delta, abs(max_v - self.V[state_id]))
                    
            self.V = new_V
            if delta < epsilon:
                break

    def get_optimal_policy(self) -> Dict[str, str]:
        return self.policy

    def get_value_function(self) -> Dict[str, float]:
        return self.V


class UtilityEvaluator:
    """
    Transforms objective values into Subjective Expected Utilities based on risk profiles.
    """
    def __init__(self, profile: RiskProfile):
        self.profile = profile
        
    def transform(self, value: float) -> float:
        if self.profile == RiskProfile.NEUTRAL:
            return value
        elif self.profile == RiskProfile.AVERSE:
            # Concave utility function for gains, convex for losses
            return math.log(max(1e-9, value + 1.0)) if value >= 0 else -((-value)**1.2)
        elif self.profile == RiskProfile.SEEKING:
            # Convex utility function for gains, concave for losses
            return value**1.2 if value >= 0 else -math.log(max(1e-9, -value + 1.0))
        return value


class H11DecisionAgent:
    """
    Main H11 Substrate facade for coordinating different decision paradigms.
    """
    def __init__(self):
        self.mcda_history: List[List[Tuple[str, float]]] = []
        
    def run_mcda(self, criteria: List[Criteria], alternatives: List[Alternative]) -> List[Tuple[str, float]]:
        engine = MCDAEngine(criteria)
        result = engine.topsis(alternatives)
        self.mcda_history.append(result)
        return result
        
    def solve_mdp(self, states: List[State], actions: List[Action], 
                transitions: Dict[str, Dict[str, List[Tuple[str, float]]]], 
                rewards: Dict[str, Dict[str, float]], 
                gamma: float = 0.9) -> Tuple[Dict[str, str], Dict[str, float]]:
        
        engine = MDPEngine(states, actions, gamma)
        for s_id, a_dict in transitions.items():
            for a_id, probs in a_dict.items():
                engine.set_transition(s_id, a_id, probs)
                
        for s_id, a_dict in rewards.items():
            for a_id, rew in a_dict.items():
                engine.set_reward(s_id, a_id, rew)
                
        engine.value_iteration()
        return engine.get_optimal_policy(), engine.get_value_function()

    def evaluate_lottery(self, outcomes: List[Tuple[float, float]], profile: RiskProfile) -> float:
        """
        Evaluates Expected Utility of a lottery.
        outcomes are (value, probability) pairs.
        """
        evaluator = UtilityEvaluator(profile)
        expected_utility = 0.0
        for value, prob in outcomes:
            expected_utility += prob * evaluator.transform(value)
        return expected_utility

if __name__ == "__main__":
    # Example Usage for Validation
    agent = H11DecisionAgent()
    
    # 1. MCDA Example
    crits = [Criteria("cost", 0.5, False), Criteria("benefit", 0.5, True)]
    alts = [
        Alternative("Option A", {"cost": 100, "benefit": 50}), 
        Alternative("Option B", {"cost": 80, "benefit": 40}),
        Alternative("Option C", {"cost": 120, "benefit": 70})
    ]
    mcda_rankings = agent.run_mcda(crits, alts)
    print(f"MCDA Rankings: {mcda_rankings}")
    
    # 2. Expected Utility Example
    lottery = [(100, 0.5), (-50, 0.5)] # 50% chance of gaining 100, 50% of losing 50
    eu_neutral = agent.evaluate_lottery(lottery, RiskProfile.NEUTRAL)
    eu_averse = agent.evaluate_lottery(lottery, RiskProfile.AVERSE)
    eu_seeking = agent.evaluate_lottery(lottery, RiskProfile.SEEKING)
    print(f"Lottery Utility -> Neutral: {eu_neutral:.2f}, Averse: {eu_averse:.2f}, Seeking: {eu_seeking:.2f}")
