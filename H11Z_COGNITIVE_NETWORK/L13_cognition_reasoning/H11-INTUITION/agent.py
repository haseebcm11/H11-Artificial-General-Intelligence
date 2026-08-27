import logging
import re
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H11-INTUITION")

@dataclass
class IntuitionResult:
    heuristic_estimate: float
    intuition_summary: str
    confidence: float
    requires_system2: bool

class PatternMatcher:
    def __init__(self):
        # Simulated cache of common patterns
        self.known_patterns = {
            "NP_HARD": {"regex": r"(traveling salesperson|knapsack|clique)", "estimate": 0.1, "sys2": True},
            "LINEAR": {"regex": r"(sort|search|filter)", "estimate": 0.9, "sys2": False},
            "DANGER": {"regex": r"(delete all|drop table|format)", "estimate": 0.0, "sys2": True}
        }
        
    def match(self, state: str) -> Optional[Dict[str, Any]]:
        state_lower = state.lower()
        for key, pattern in self.known_patterns.items():
            if re.search(pattern["regex"], state_lower):
                logger.info(f"Matched pattern {key}")
                return pattern
        return None

class HeuristicEngine:
    def __init__(self, domain: str = "general"):
        self.domain = domain
        self.matcher = PatternMatcher()

    def generate_intuition(self, problem_state: str) -> IntuitionResult:
        logger.info(f"Generating System 1 intuition for domain: {self.domain}")
        
        # 1. Pattern Matching
        match = self.matcher.match(problem_state)
        
        if match:
            return IntuitionResult(
                heuristic_estimate=match["estimate"],
                intuition_summary="Pattern recognized. Applying cached heuristic.",
                confidence=0.85,
                requires_system2=match["sys2"]
            )
            
        # 2. Fallback Heuristics
        # Length proxy: shorter problems might seem simpler but could be deceptive.
        word_count = len(problem_state.split())
        if word_count > 100:
            est = 0.3
            summary = "Problem is lengthy and complex; requires careful deliberation."
            req_sys2 = True
            conf = 0.7
        else:
            est = 0.6
            summary = "Problem seems manageable, standard heuristic applied."
            req_sys2 = False
            conf = 0.5
            
        return IntuitionResult(
            heuristic_estimate=est,
            intuition_summary=summary,
            confidence=conf,
            requires_system2=req_sys2
        )

def run_intuition(input_data: Dict) -> Dict:
    state = input_data.get("problem_state", "")
    domain = input_data.get("domain", "general")
    
    engine = HeuristicEngine(domain=domain)
    res = engine.generate_intuition(state)
    
    return {
        "heuristic_estimate": res.heuristic_estimate,
        "intuition_summary": res.intuition_summary,
        "confidence": res.confidence,
        "requires_system2": res.requires_system2
    }

if __name__ == "__main__":
    test_input = {
        "problem_state": "Find the optimal route for the traveling salesperson across 50 cities.",
        "domain": "algorithm"
    }
    print(run_intuition(test_input))
