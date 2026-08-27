import json
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import defaultdict

class NodeType(Enum):
    ENTITY = "entity"      # e.g., a dataset, a model
    ACTIVITY = "activity"  # e.g., a preprocessing script, a training run
    AGENT = "agent"        # e.g., a specific H11 module or user

@dataclass
class ProvNode:
    id: str
    node_type: NodeType
    attributes: Dict[str, str] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class ProvEdge:
    source_id: str
    target_id: str
    relation: str  # e.g., "wasGeneratedBy", "used", "wasAssociatedWith"

@dataclass
class ProvEvent:
    activity_id: str
    activity_name: str
    inputs: List[str]
    outputs: List[str]
    agent_id: str
    params: Dict[str, str]

class ProvenanceTrackerAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.nodes: Dict[str, ProvNode] = {}
        # adjacency list: node_id -> list of outgoing edges
        self.edges: Dict[str, List[ProvEdge]] = defaultdict(list)
        # reverse adjacency list for fast upstream traversal
        self.reverse_edges: Dict[str, List[ProvEdge]] = defaultdict(list)
        
    def _add_node(self, node: ProvNode):
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            
    def _add_edge(self, edge: ProvEdge):
        self.edges[edge.source_id].append(edge)
        self.reverse_edges[edge.target_id].append(edge)

    def ingest_event(self, event: ProvEvent):
        """Processes a provenance event and updates the DAG."""
        # 1. Add Activity
        act_node = ProvNode(
            id=event.activity_id,
            node_type=NodeType.ACTIVITY,
            attributes={"name": event.activity_name, "params": json.dumps(event.params)}
        )
        self._add_node(act_node)
        
        # 2. Add Agent and associate
        agent_node = ProvNode(id=event.agent_id, node_type=NodeType.AGENT)
        self._add_node(agent_node)
        self._add_edge(ProvEdge(event.activity_id, event.agent_id, "wasAssociatedWith"))
        
        # 3. Add Inputs and link (Activity 'used' Input)
        for in_id in event.inputs:
            in_node = ProvNode(id=in_id, node_type=NodeType.ENTITY)
            self._add_node(in_node)
            self._add_edge(ProvEdge(event.activity_id, in_id, "used"))
            
        # 4. Add Outputs and link (Output 'wasGeneratedBy' Activity)
        for out_id in event.outputs:
            out_node = ProvNode(id=out_id, node_type=NodeType.ENTITY)
            self._add_node(out_node)
            self._add_edge(ProvEdge(out_id, event.activity_id, "wasGeneratedBy"))

    def trace_upstream(self, entity_id: str, depth: int = 100) -> Dict:
        """Traverses backwards to find all origins of an entity."""
        if entity_id not in self.nodes:
            return {"error": "Entity not found"}
            
        visited: Set[str] = set()
        queue: List[Tuple[str, int]] = [(entity_id, 0)]
        subgraph = {"nodes": [], "edges": []}
        
        while queue:
            current_id, current_depth = queue.pop(0)
            if current_id in visited or current_depth > depth:
                continue
                
            visited.add(current_id)
            node = self.nodes[current_id]
            subgraph["nodes"].append({"id": node.id, "type": node.node_type.value, "attrs": node.attributes})
            
            for edge in self.edges.get(current_id, []):
                if edge.target_id not in visited:
                    subgraph["edges"].append({"source": edge.source_id, "target": edge.target_id, "relation": edge.relation})
                    queue.append((edge.target_id, current_depth + 1))
                    
        return subgraph

    def generate_compliance_report(self, entity_id: str) -> str:
        """Generates a human-readable text report of the lineage."""
        graph = self.trace_upstream(entity_id)
        if "error" in graph:
            return f"Report generation failed: {graph['error']}"
            
        lines = [f"Provenance Report for: {entity_id}", "="*40]
        for node in graph["nodes"]:
            if node["type"] == "activity":
                lines.append(f"Activity: {node['id']} - {node['attrs'].get('name', 'Unknown')}")
                lines.append(f"  Parameters: {node['attrs'].get('params', '{}')}")
        
        return "\n".join(lines)
