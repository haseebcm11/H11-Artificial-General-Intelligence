import math
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ValueNode:
    id: str
    name: str
    embedding: List[float]
    base_weight: float
    
@dataclass
class StateContext:
    semantic_features: List[float]
    urgency_level: float
    affected_entities: int

class ValueManifold:
    def __init__(self, dimension: int = 64):
        self.dimension = dimension
        self.nodes: Dict[str, ValueNode] = {}
        
    def add_node(self, node: ValueNode):
        if len(node.embedding) != self.dimension:
            raise ValueError(f"Embedding must be of dimension {self.dimension}")
        self.nodes[node.id] = node
        
    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        dot_product = sum(x*y for x, y in zip(v1, v2))
        mag1 = math.sqrt(sum(x*x for x in v1))
        mag2 = math.sqrt(sum(y*y for y in v2))
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot_product / (mag1 * mag2)

    def retrieve_salient(self, context_vector: List[float], top_k: int = 3) -> List[ValueNode]:
        scored_nodes = []
        for node in self.nodes.values():
            sim = self._cosine_similarity(node.embedding, context_vector)
            scored_nodes.append((sim, node))
            
        scored_nodes.sort(key=lambda x: x[0], reverse=True)
        return [node for _, node in scored_nodes[:top_k]]

class H11ValueEncoder:
    def __init__(self, manifold: ValueManifold):
        self.manifold = manifold
        
    def map_context_to_values(self, context: StateContext) -> List[ValueNode]:
        """Maps the current semantic context to core values."""
        # Using the semantic features to query the manifold
        return self.manifold.retrieve_salient(context.semantic_features, top_k=5)
        
    def compute_reward_shaping(self, proposed_action_embedding: List[float], context: StateContext) -> float:
        """Computes a dense reward signal based on value alignment."""
        salient_values = self.map_context_to_values(context)
        
        total_reward = 0.0
        for val in salient_values:
            sim = self.manifold._cosine_similarity(proposed_action_embedding, val.embedding)
            # Weighted by the base weight of the value and the urgency of the context
            total_reward += sim * val.base_weight * (1.0 + context.urgency_level)
            
        return total_reward / (len(salient_values) + 1e-9)

# Example usage/initialization
def create_default_encoder() -> H11ValueEncoder:
    manifold = ValueManifold(dimension=4)
    manifold.add_node(ValueNode("v1", "Do No Harm", [0.9, 0.1, -0.2, 0.5], 1.0))
    manifold.add_node(ValueNode("v2", "Helpfulness", [0.5, 0.8, 0.1, 0.2], 0.8))
    return H11ValueEncoder(manifold)
