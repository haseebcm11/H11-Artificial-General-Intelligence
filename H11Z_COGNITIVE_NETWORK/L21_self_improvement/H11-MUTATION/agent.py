import json
import logging
import numpy as np
from typing import Dict, Any, Tuple
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H11-MUTATION")

@dataclass
class MutationPolicy:
    weight_mutation_rate: float
    weight_mutation_power: float
    add_node_rate: float
    add_conn_rate: float

class GlobalInnovationDB:
    """Tracks innovations to ensure identical mutations get the same innovation number."""
    def __init__(self):
        self.current_innov = 0
        self.current_node = 0
        self.mutations = {} # (in, out) -> innov

    def get_innovation(self, in_node: int, out_node: int) -> int:
        key = (in_node, out_node)
        if key not in self.mutations:
            self.current_innov += 1
            self.mutations[key] = self.current_innov
        return self.mutations[key]

    def get_new_node_id(self) -> int:
        self.current_node += 1
        return self.current_node

class MutationEngine:
    def __init__(self, db: GlobalInnovationDB):
        self.db = db

    def mutate_weights(self, genome: Dict[str, Any], policy: MutationPolicy):
        for conn in genome.get("connections", []):
            if np.random.rand() < policy.weight_mutation_rate:
                # Either perturb or assign new
                if np.random.rand() < 0.9:
                    conn["weight"] += np.random.normal(0, policy.weight_mutation_power)
                else:
                    conn["weight"] = np.random.normal(0, 1.0)
        logger.debug(f"Mutated weights for {genome['genome_id']}")

    def mutate_add_connection(self, genome: Dict[str, Any], policy: MutationPolicy):
        if np.random.rand() >= policy.add_conn_rate:
            return
            
        nodes = [n["node_id"] for n in genome["nodes"]]
        if not nodes: return
        
        in_node = np.random.choice(nodes)
        out_node = np.random.choice(nodes)
        
        # Check if exists
        exists = any((c["in_node"] == in_node and c["out_node"] == out_node) for c in genome["connections"])
        if not exists:
            innov = self.db.get_innovation(in_node, out_node)
            genome["connections"].append({
                "in_node": int(in_node),
                "out_node": int(out_node),
                "weight": float(np.random.normal(0, 1)),
                "innovation_number": innov,
                "enabled": True
            })
            logger.info(f"Added connection {in_node}->{out_node} to {genome['genome_id']}")

    def mutate_add_node(self, genome: Dict[str, Any], policy: MutationPolicy):
        if np.random.rand() >= policy.add_node_rate:
            return
            
        conns = [c for c in genome["connections"] if c["enabled"]]
        if not conns: return
        
        # Choose connection to split
        conn = np.random.choice(conns)
        conn["enabled"] = False # Disable old connection
        
        new_node_id = self.db.get_new_node_id()
        genome["nodes"].append({"node_id": new_node_id, "type": "hidden"})
        
        # Add two new connections
        # Into new node: weight 1.0 to minimize initial behavioral disruption
        innov1 = self.db.get_innovation(conn["in_node"], new_node_id)
        genome["connections"].append({
            "in_node": conn["in_node"], "out_node": new_node_id, 
            "weight": 1.0, "innovation_number": innov1, "enabled": True
        })
        
        # Out of new node: old weight
        innov2 = self.db.get_innovation(new_node_id, conn["out_node"])
        genome["connections"].append({
            "in_node": new_node_id, "out_node": conn["out_node"], 
            "weight": conn["weight"], "innovation_number": innov2, "enabled": True
        })
        logger.info(f"Added node {new_node_id} to {genome['genome_id']}")

class MutationAgent:
    def __init__(self):
        self.db = GlobalInnovationDB()
        self.engine = MutationEngine(self.db)
        
    def mutate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        genome = request["genome"].copy()
        pol = MutationPolicy(**request.get("policy", {}))
        
        self.engine.mutate_weights(genome, pol)
        self.engine.mutate_add_connection(genome, pol)
        self.engine.mutate_add_node(genome, pol)
        
        return genome

if __name__ == "__main__":
    logger.info("Mutation Agent Initialized")
