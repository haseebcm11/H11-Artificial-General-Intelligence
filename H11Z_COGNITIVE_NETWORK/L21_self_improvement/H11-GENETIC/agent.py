import json
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H11-GENETIC")

@dataclass
class ConnectionGene:
    in_node: int
    out_node: int
    weight: float
    innovation_number: int
    enabled: bool

@dataclass
class NodeGene:
    node_id: int
    node_type: str  # input, hidden, output

@dataclass
class Genome:
    genome_id: str
    nodes: Dict[int, NodeGene]
    connections: Dict[int, ConnectionGene]

class GeneticOperatorManager:
    """Manages genetic operations like crossover based on NEAT principles."""
    
    def align_and_crossover(self, p1: Genome, p2: Genome, f1: float, f2: float) -> Genome:
        """
        Performs homologous crossover aligning by innovation number.
        """
        child_connections = {}
        child_nodes = {}
        
        # Determine more fit parent
        better_p, worse_p = (p1, p2) if f1 >= f2 else (p2, p1)
        
        # Align connections
        for innov, conn in better_p.connections.items():
            if innov in worse_p.connections:
                # Matching gene - randomly choose
                chosen_conn = conn if np.random.rand() < 0.5 else worse_p.connections[innov]
                child_connections[innov] = ConnectionGene(
                    chosen_conn.in_node, chosen_conn.out_node, chosen_conn.weight, innov,
                    conn.enabled and worse_p.connections[innov].enabled # Disable if either disabled
                )
            else:
                # Disjoint/Excess gene from better parent - inherit
                child_connections[innov] = ConnectionGene(
                    conn.in_node, conn.out_node, conn.weight, innov, conn.enabled
                )
                
        # Inherit all nodes from better parent (needed for the connections)
        for nid, node in better_p.nodes.items():
            child_nodes[nid] = NodeGene(node.node_id, node.node_type)
            
        child_genome = Genome(
            genome_id=f"child_{p1.genome_id}_{p2.genome_id}",
            nodes=child_nodes,
            connections=child_connections
        )
        logger.info(f"Generated child {child_genome.genome_id} with {len(child_connections)} connections")
        return child_genome

import numpy as np

class GeneticAgent:
    def __init__(self):
        self.operator = GeneticOperatorManager()
        
    def process_crossover(self, req: Dict[str, Any]) -> Dict[str, Any]:
        p1_data = req["parent1"]
        p2_data = req["parent2"]
        
        p1 = Genome(
            p1_data["genome_id"], 
            {n["node_id"]: NodeGene(**n) for n in p1_data["nodes"]},
            {c["innovation_number"]: ConnectionGene(**c) for c in p1_data["connections"]}
        )
        p2 = Genome(
            p2_data["genome_id"], 
            {n["node_id"]: NodeGene(**n) for n in p2_data["nodes"]},
            {c["innovation_number"]: ConnectionGene(**c) for c in p2_data["connections"]}
        )
        
        child = self.operator.align_and_crossover(p1, p2, req["fitness1"], req["fitness2"])
        
        return {
            "genome_id": child.genome_id,
            "nodes": [{"node_id": n.node_id, "node_type": n.node_type} for n in child.nodes.values()],
            "connections": [{"in_node": c.in_node, "out_node": c.out_node, "weight": c.weight, "innovation_number": c.innovation_number, "enabled": c.enabled} for c in child.connections.values()]
        }

if __name__ == "__main__":
    logger.info("Genetic Agent Ready")
