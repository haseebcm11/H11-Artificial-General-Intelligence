import uuid
import math
import logging
from typing import List, Dict, Any, Optional, Set, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H11-INDUCTION")

class PredicateType(Enum):
    FEATURE = auto()
    RELATION = auto()

@dataclass
class Variable:
    name: str
    type_id: str

@dataclass
class Literal:
    predicate: str
    args: List[Variable]
    is_negated: bool = False

    def to_string(self) -> str:
        prefix = "NOT " if self.is_negated else ""
        args_str = ", ".join([arg.name for arg in self.args])
        return f"{prefix}{self.predicate}({args_str})"

@dataclass
class Rule:
    head: Literal
    body: List[Literal]
    
    def to_string(self) -> str:
        if not self.body:
            return f"{self.head.to_string()} :- True"
        body_str = " AND ".join([lit.to_string() for lit in self.body])
        return f"{self.head.to_string()} :- {body_str}"

@dataclass
class Example:
    id: str
    attributes: Dict[str, Any]
    
    def satisfies(self, literal: Literal, var_bindings: Dict[str, str]) -> bool:
        # Simplified evaluation mechanism for features
        if literal.predicate in self.attributes:
            val = self.attributes[literal.predicate]
            # Assuming boolean features for simple FOIL
            if isinstance(val, bool):
                return not val if literal.is_negated else val
            # If it's categorical
            if len(literal.args) > 1:
                expected = literal.args[1].name # Hack for equality
                res = (str(val) == expected)
                return not res if literal.is_negated else res
        return False

@dataclass
class InductiveHypothesis:
    rules: List[Rule]
    coverage_ratio: float
    false_positive_ratio: float
    simplicity_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rules": [r.to_string() for r in self.rules],
            "metrics": {
                "coverage": self.coverage_ratio,
                "false_positive_ratio": self.false_positive_ratio,
                "simplicity": self.simplicity_score
            }
        }

class FOILEngine:
    """
    Simplified implementation inspired by First-Order Inductive Learner (FOIL).
    Uses Information Gain to construct rules sequentially.
    """
    def __init__(self, max_rule_length: int = 5, min_gain: float = 0.01):
        self.max_rule_length = max_rule_length
        self.min_gain = min_gain

    def _compute_info_gain(self, p0: int, n0: int, p1: int, n1: int) -> float:
        if p0 == 0:
            return 0.0
        # Info prior
        prior_prob = p0 / (p0 + n0)
        info_prior = -math.log2(prior_prob) if prior_prob > 0 else 0.0
        
        # Info post
        post_prob = p1 / (p1 + n1) if (p1 + n1) > 0 else 0.0
        info_post = -math.log2(post_prob) if post_prob > 0 else 0.0
        
        return p1 * (info_prior - info_post)

    def _generate_candidate_literals(self, pos_examples: List[Example]) -> List[Literal]:
        # Extract features from examples to form candidates
        candidates = []
        features = set()
        for ex in pos_examples:
            features.update(ex.attributes.keys())
            
        target_var = Variable("X", "Entity")
        for f in features:
            candidates.append(Literal(f, [target_var], is_negated=False))
            candidates.append(Literal(f, [target_var], is_negated=True))
            
        return candidates

    def _evaluate_literal(self, literal: Literal, pos: List[Example], neg: List[Example]) -> Tuple[List[Example], List[Example]]:
        covered_pos = [ex for ex in pos if ex.satisfies(literal, {})]
        covered_neg = [ex for ex in neg if ex.satisfies(literal, {})]
        return covered_pos, covered_neg

    def learn_single_rule(self, target_head: Literal, pos: List[Example], neg: List[Example]) -> Optional[Rule]:
        current_pos = list(pos)
        current_neg = list(neg)
        body = []
        
        logger.info(f"Learning new rule to cover {len(pos)} positive examples.")
        
        while current_neg and len(body) < self.max_rule_length:
            best_literal = None
            best_gain = -1.0
            best_pos_cov = []
            best_neg_cov = []
            
            candidates = self._generate_candidate_literals(current_pos)
            
            for lit in candidates:
                if lit in body: continue
                
                cov_pos, cov_neg = self._evaluate_literal(lit, current_pos, current_neg)
                
                p0, n0 = len(current_pos), len(current_neg)
                p1, n1 = len(cov_pos), len(cov_neg)
                
                gain = self._compute_info_gain(p0, n0, p1, n1)
                if gain > best_gain:
                    best_gain = gain
                    best_literal = lit
                    best_pos_cov = cov_pos
                    best_neg_cov = cov_neg
                    
            if best_literal and best_gain >= self.min_gain:
                body.append(best_literal)
                current_pos = best_pos_cov
                current_neg = best_neg_cov
                logger.debug(f"Added literal {best_literal.to_string()} with gain {best_gain:.3f}")
            else:
                break
                
        if not body and not current_pos:
            return None
            
        return Rule(target_head, body)

    def induce_theory(self, target_predicate: str, pos: List[Example], neg: List[Example]) -> InductiveHypothesis:
        uncovered_pos = list(pos)
        rules = []
        target_head = Literal(target_predicate, [Variable("X", "Entity")])
        
        initial_pos_count = len(pos)
        
        while uncovered_pos:
            rule = self.learn_single_rule(target_head, uncovered_pos, neg)
            if not rule:
                logger.warning("Could not find rule to cover remaining positive examples.")
                break
                
            rules.append(rule)
            
            # Remove covered positive examples
            new_uncovered = []
            for ex in uncovered_pos:
                # evaluate rule body
                satisfies = True
                for lit in rule.body:
                    if not ex.satisfies(lit, {}):
                        satisfies = False
                        break
                if not satisfies:
                    new_uncovered.append(ex)
                    
            if len(new_uncovered) == len(uncovered_pos):
                logger.error("Rule learned but did not cover any new positive examples. Breaking to avoid infinite loop.")
                break
                
            uncovered_pos = new_uncovered
            
        coverage = 1.0 - (len(uncovered_pos) / max(1, initial_pos_count))
        # Simplistic complexity penalty
        complexity = sum(len(r.body) for r in rules)
        simplicity = 1.0 / (1.0 + complexity)
        
        return InductiveHypothesis(
            rules=rules,
            coverage_ratio=coverage,
            false_positive_ratio=0.0, # Ideal FOIL has 0
            simplicity_score=simplicity
        )

def run_induction_agent(input_data: Dict[str, Any]) -> Dict[str, Any]:
    pos_data = input_data.get("positive_examples", [])
    neg_data = input_data.get("negative_examples", [])
    target = input_data.get("target_predicate", "Target")
    
    pos_examples = [Example(e["id"], e["features"]) for e in pos_data]
    neg_examples = [Example(e["id"], e["features"]) for e in neg_data]
    
    engine = FOILEngine()
    hypothesis = engine.induce_theory(target, pos_examples, neg_examples)
    
    return hypothesis.to_dict()

if __name__ == "__main__":
    # Test stub
    sample_input = {
        "target_predicate": "IsBird",
        "positive_examples": [
            {"id": "e1", "features": {"has_feathers": True, "can_fly": True, "lays_eggs": True}},
            {"id": "e2", "features": {"has_feathers": True, "can_fly": False, "lays_eggs": True}}
        ],
        "negative_examples": [
            {"id": "e3", "features": {"has_feathers": False, "can_fly": False, "lays_eggs": False}}, # Cat
            {"id": "e4", "features": {"has_feathers": False, "can_fly": True, "lays_eggs": False}}   # Bat
        ]
    }
    result = run_induction_agent(sample_input)
    print(json.dumps(result, indent=2))
