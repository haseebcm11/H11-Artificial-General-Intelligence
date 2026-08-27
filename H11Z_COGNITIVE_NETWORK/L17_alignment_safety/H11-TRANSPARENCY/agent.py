import numpy as np
import uuid
import json
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum

class ExplanationMethod(Enum):
    CAUSAL_TRACE = "causal_trace"
    TCAV = "tcav"
    INTEGRATED_GRADIENTS = "integrated_gradients"

@dataclass
class CognitiveState:
    node_id: str
    activations: np.ndarray
    layer_depth: int
    metadata: Dict[str, str] = field(default_factory=dict)

@dataclass
class ExplanationGraphNode:
    concept_name: str
    causal_effect: float
    saliency_score: float

@dataclass
class ExplanationResult:
    trace_id: str
    method: ExplanationMethod
    nodes: List[ExplanationGraphNode]
    overall_confidence: float
    raw_heatmaps: Optional[np.ndarray] = None

class TransparencyAgent:
    """
    H11-TRANSPARENCY Agent: Computes explainability metrics for latent cognitive states
    using Causal Tracing, TCAV, and Integrated Gradients.
    """
    def __init__(self, baseline_distribution: np.ndarray, num_steps: int = 50):
        self.baseline = baseline_distribution
        self.num_steps = num_steps
        self.concept_vectors: Dict[str, np.ndarray] = {}
        
    def register_concept(self, name: str, vector: np.ndarray) -> None:
        """Register a Concept Activation Vector (CAV)."""
        normalized_vector = vector / (np.linalg.norm(vector) + 1e-9)
        self.concept_vectors[name] = normalized_vector

    def _integrated_gradients(self, state: CognitiveState, target_grad_fn) -> np.ndarray:
        """
        Approximate the integral of gradients from baseline to the target state.
        """
        path = [self.baseline + (float(i) / self.num_steps) * (state.activations - self.baseline)
                for i in range(self.num_steps + 1)]
        
        grads = np.array([target_grad_fn(p) for p in path])
        avg_grads = np.mean(grads[:-1], axis=0)
        integrated_grad = (state.activations - self.baseline) * avg_grads
        return integrated_grad

    def _causal_trace(self, state: CognitiveState, intervention_target: np.ndarray) -> float:
        """
        Estimate the Average Causal Effect (ACE) by intervening on the latent state.
        Simulates an ablation/intervention.
        """
        # Simplified structural causal effect
        diff = np.abs(state.activations - intervention_target)
        effect_size = np.sum(np.exp(-diff)) / diff.size
        return float(effect_size)

    def _compute_tcav(self, state: CognitiveState, grad_wrt_state: np.ndarray) -> Dict[str, float]:
        """
        Compute TCAV scores for all registered concepts.
        """
        scores = {}
        for concept, cav in self.concept_vectors.items():
            # Directional derivative along the CAV
            directional_deriv = np.dot(grad_wrt_state.flatten(), cav.flatten())
            # TCAV score is the probability that the directional derivative is positive (simplified to magnitude here)
            scores[concept] = float(np.tanh(directional_deriv))
        return scores

    def generate_explanation(
        self, 
        trace_id: str, 
        state: CognitiveState, 
        method: ExplanationMethod,
        dummy_grad_fn=None
    ) -> ExplanationResult:
        """
        Generate an explanation for a given cognitive state using the specified method.
        """
        if dummy_grad_fn is None:
            # Provide a dummy gradient function for demonstration
            dummy_grad_fn = lambda x: np.random.randn(*x.shape) * 0.1

        nodes = []
        confidence = 0.95
        heatmaps = None

        if method == ExplanationMethod.INTEGRATED_GRADIENTS:
            heatmaps = self._integrated_gradients(state, dummy_grad_fn)
            # Summarize into generic nodes
            nodes.append(ExplanationGraphNode(
                concept_name="Overall_Saliency",
                causal_effect=0.0,
                saliency_score=float(np.sum(np.abs(heatmaps)))
            ))
            
        elif method == ExplanationMethod.CAUSAL_TRACE:
            # Simulate a set of interventions
            effect = self._causal_trace(state, np.zeros_like(state.activations))
            nodes.append(ExplanationGraphNode(
                concept_name="Baseline_Ablation",
                causal_effect=effect,
                saliency_score=0.0
            ))
            
        elif method == ExplanationMethod.TCAV:
            grad = dummy_grad_fn(state.activations)
            tcav_scores = self._compute_tcav(state, grad)
            for concept, score in tcav_scores.items():
                nodes.append(ExplanationGraphNode(
                    concept_name=concept,
                    causal_effect=0.0,
                    saliency_score=score
                ))

        return ExplanationResult(
            trace_id=trace_id,
            method=method,
            nodes=nodes,
            overall_confidence=confidence,
            raw_heatmaps=heatmaps
        )

# Example Usage
if __name__ == "__main__":
    agent = TransparencyAgent(baseline_distribution=np.zeros((10, 10)))
    agent.register_concept("Safety", np.ones((10, 10)))
    agent.register_concept("Risk", -np.ones((10, 10)))
    
    state = CognitiveState(
        node_id="node_x_1",
        activations=np.random.rand(10, 10),
        layer_depth=3
    )
    
    res = agent.generate_explanation("trace-001", state, ExplanationMethod.TCAV)
    print(f"Explanation for trace {res.trace_id}: {res.nodes}")
