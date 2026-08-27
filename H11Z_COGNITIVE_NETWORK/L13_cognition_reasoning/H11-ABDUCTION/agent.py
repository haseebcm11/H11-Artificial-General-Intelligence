import itertools
import logging
from typing import List, Dict, Any, Set
from dataclasses import dataclass, field
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H11-ABDUCTION")

@dataclass
class CausalLink:
    cause: str
    effect: str
    probability: float = 1.0

@dataclass
class Explanation:
    hypotheses: Set[str]
    score: float
    coverage: Set[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "hypotheses": list(self.hypotheses),
            "score": self.score,
            "coverage": list(self.coverage)
        }

class AbductiveReasoner:
    """
    Implements a Set-Covering based abductive reasoning engine with probabilistic scoring.
    """
    def __init__(self, links: List[CausalLink], priors: Dict[str, float] = None):
        self.links = links
        self.priors = priors or {}
        
        # Build indexes
        self.cause_to_effects: Dict[str, Set[str]] = {}
        self.effect_to_causes: Dict[str, Set[str]] = {}
        
        for link in links:
            self.cause_to_effects.setdefault(link.cause, set()).add(link.effect)
            self.effect_to_causes.setdefault(link.effect, set()).add(link.cause)
            
    def _get_prior(self, cause: str) -> float:
        return self.priors.get(cause, 0.1) # Default prior

    def _score_explanation(self, hypotheses: Set[str], observations: Set[str]) -> float:
        # Score based on Bayesian approximation: P(H) * P(O|H)
        # We assume independence for simplicity.
        prior_score = 1.0
        for h in hypotheses:
            prior_score *= self._get_prior(h)
            
        # Parsimony penalty: prefer fewer hypotheses
        parsimony_penalty = 1.0 / (len(hypotheses) + 1)
        
        return prior_score * parsimony_penalty

    def explain(self, observations: List[str], max_results: int = 5) -> List[Explanation]:
        obs_set = set(observations)
        valid_causes = set()
        
        # 1. Identify all potential causes for the observations
        for obs in obs_set:
            causes = self.effect_to_causes.get(obs, set())
            valid_causes.update(causes)
            
        if not valid_causes:
            logger.warning("No known causes for the given observations.")
            return []

        valid_causes_list = list(valid_causes)
        explanations = []
        
        # 2. Set covering algorithm (brute force for small state spaces)
        # Find combinations of causes that cover all observations
        # We start from size 1 up to max allowed
        max_depth = min(len(valid_causes_list), len(obs_set) + 1)
        
        for r in range(1, max_depth + 1):
            for combo in itertools.combinations(valid_causes_list, r):
                combo_set = set(combo)
                
                # Check coverage
                covered = set()
                for h in combo_set:
                    covered.update(self.cause_to_effects.get(h, set()))
                
                # We only want to explain the given observations.
                intersection = covered.intersection(obs_set)
                if intersection == obs_set:
                    # Found a valid cover
                    score = self._score_explanation(combo_set, obs_set)
                    explanations.append(Explanation(
                        hypotheses=combo_set,
                        score=score,
                        coverage=intersection
                    ))
                    
        # 3. Sort by score and parsimony
        explanations.sort(key=lambda e: (-e.score, len(e.hypotheses)))
        
        # Return top N
        return explanations[:max_results]

def run_abduction_agent(input_data: Dict[str, Any]) -> Dict[str, Any]:
    obs = input_data.get("observations", [])
    raw_links = input_data.get("causal_network", [])
    priors = input_data.get("priors", {})
    
    links = [CausalLink(cause=l["cause"], effect=l["effect"], probability=l.get("probability", 1.0)) for l in raw_links]
    
    reasoner = AbductiveReasoner(links, priors)
    explanations = reasoner.explain(obs)
    
    return {
        "best_explanations": [e.to_dict() for e in explanations]
    }

if __name__ == "__main__":
    sample_input = {
        "observations": ["cough", "fever"],
        "causal_network": [
            {"cause": "flu", "effect": "cough", "probability": 0.8},
            {"cause": "flu", "effect": "fever", "probability": 0.9},
            {"cause": "cold", "effect": "cough", "probability": 0.6},
            {"cause": "malaria", "effect": "fever", "probability": 0.9}
        ],
        "priors": {
            "flu": 0.1,
            "cold": 0.3,
            "malaria": 0.01
        }
    }
    result = run_abduction_agent(sample_input)
    print(json.dumps(result, indent=2))
