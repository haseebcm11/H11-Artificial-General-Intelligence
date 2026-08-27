import json
import logging
from typing import Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H11-COUNTERFACTUAL")

@dataclass
class SCMNode:
    name: str
    equation: Callable[[Dict[str, float], float], float]
    noise_val: float = 0.0

class StructuralCausalModel:
    def __init__(self):
        self.nodes: Dict[str, SCMNode] = {}
        self.topo_order: list[str] = []

    def add_node(self, name: str, equation: Callable, depends_on: list[str]):
        self.nodes[name] = SCMNode(name, equation)
        # Assuming simplified topological order handling for demo
        self.topo_order.append(name)

    def evaluate(self, state: Dict[str, float]) -> Dict[str, float]:
        result = dict(state)
        for node_name in self.topo_order:
            if node_name not in result: # Not intervened
                node = self.nodes[node_name]
                result[node_name] = node.equation(result, node.noise_val)
        return result

class CounterfactualEngine:
    def __init__(self, scm: StructuralCausalModel):
        self.scm = scm

    def abduct(self, factual_state: Dict[str, float]) -> Dict[str, float]:
        """
        Step 1: Abduction. Infer exogenous noise terms (U) given factual state.
        In this simplified linear/deterministic SCM, we invert the equations to find U.
        For demonstration, we assume U is already computed or is 0.
        """
        inferred_noise = {}
        for name, node in self.scm.nodes.items():
            inferred_noise[name] = 0.0 # Placeholder for actual inverse function
        return inferred_noise

    def action(self, intervention: Dict[str, float]) -> Dict[str, float]:
        """
        Step 2: Action. Apply do-operator.
        """
        return intervention.copy()

    def predict(self, intervened_state: Dict[str, float], noise: Dict[str, float]) -> Dict[str, float]:
        """
        Step 3: Prediction. Evaluate SCM with new state and abducted noise.
        """
        for name, n in self.scm.nodes.items():
            n.noise_val = noise.get(name, 0.0)
        return self.scm.evaluate(intervened_state)

    def evaluate_counterfactual(self, factual_state: Dict[str, float], intervention: Dict[str, float]) -> Dict[str, float]:
        noise = self.abduct(factual_state)
        intervened_state = self.action(intervention)
        return self.predict(intervened_state, noise)

class CounterfactualAgent:
    def __init__(self):
        self.scm = StructuralCausalModel()
        # Setup a simple SCM: 
        # Education = U_E
        # Income = 2 * Education + U_I
        self.scm.add_node("Education", lambda s, u: s.get("Education", u), [])
        self.scm.add_node("Income", lambda s, u: 2.0 * s.get("Education", 0) + u, ["Education"])
        self.engine = CounterfactualEngine(self.scm)

    def process_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        action = payload.get("action")
        if action == "evaluate_counterfactual":
            factual = payload.get("factual_state", {})
            interv = payload.get("intervention", {})
            target = payload.get("target")
            
            result = self.engine.evaluate_counterfactual(factual, interv)
            
            return {
                "factual_state": factual,
                "intervention": interv,
                "counterfactual_result": result,
                "target_value": result.get(target)
            }
        return {"error": "Unknown action"}

if __name__ == "__main__":
    agent = CounterfactualAgent()
    req = {
        "action": "evaluate_counterfactual",
        "factual_state": {"Education": 12, "Income": 24},
        "intervention": {"Education": 16},
        "target": "Income"
    }
    print(json.dumps(agent.process_request(req), indent=2))
