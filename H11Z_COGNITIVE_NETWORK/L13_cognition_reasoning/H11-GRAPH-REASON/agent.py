import json
import logging
from typing import List, Dict, Any, Set, Optional
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H11-GRAPH-REASON")

@dataclass
class GoTNode:
    id: str
    content: str
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    is_merged: bool = False
    status: str = "pending" # pending, active, completed

class ThoughtGraph:
    def __init__(self):
        self.nodes: Dict[str, GoTNode] = {}
        
    def add_node(self, node: GoTNode):
        self.nodes[node.id] = node
        for dep in node.dependencies:
            if dep in self.nodes:
                self.nodes[dep].dependents.append(node.id)

    def get_ready_nodes(self) -> List[GoTNode]:
        ready = []
        for node in self.nodes.values():
            if node.status == "pending":
                # Check if all deps are completed
                if all(self.nodes[d].status == "completed" for d in node.dependencies):
                    ready.append(node)
        return ready

class MergeOperator:
    def merge(self, sources: List[GoTNode]) -> str:
        """Simulates merging multiple thoughts into one coherent synthesis."""
        contents = [n.content for n in sources]
        return f"Merged Insight: [{ ' | '.join(contents) }]"

class H11GraphReasonAgent:
    """Agent orchestrating Graph of Thoughts reasoning."""
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.merger = MergeOperator()

    def _build_topology(self, task: str) -> ThoughtGraph:
        """Builds a predefined graph topology for demonstration."""
        graph = ThoughtGraph()
        
        # Root
        root = GoTNode("n0", f"Initial analysis of: {task}")
        graph.add_node(root)
        
        # Parallel branches
        branch1 = GoTNode("n1", "Perspective A analysis", dependencies=["n0"])
        branch2 = GoTNode("n2", "Perspective B analysis", dependencies=["n0"])
        graph.add_node(branch1)
        graph.add_node(branch2)
        
        # Merge node
        merge1 = GoTNode("n3", "Synthesize A and B", dependencies=["n1", "n2"], is_merged=True)
        graph.add_node(merge1)
        
        # Final refinement
        final = GoTNode("n4", "Final Refinement", dependencies=["n3"])
        graph.add_node(final)
        
        return graph

    def process(self, request_payload: str) -> str:
        try:
            req = json.loads(request_payload)
            task = req.get("task", "")
            enable_merging = req.get("enable_merging", True)
            
            logger.info(f"[{self.agent_id}] Initializing GoT for task: {task}")
            graph = self._build_topology(task)
            
            # Execute DAG
            completed_order = []
            
            while True:
                ready_nodes = graph.get_ready_nodes()
                if not ready_nodes:
                    break
                    
                for node in ready_nodes:
                    node.status = "active"
                    # Simulate processing
                    if node.is_merged and enable_merging:
                        deps = [graph.nodes[d] for d in node.dependencies]
                        node.content = self.merger.merge(deps)
                    else:
                        node.content += " (Processed)"
                        
                    node.status = "completed"
                    completed_order.append(node.id)
            
            final_node = graph.nodes.get("n4")
            result_content = final_node.content if final_node else "No conclusion"
            
            return json.dumps({
                "final_thought": result_content,
                "execution_trace": completed_order,
                "nodes_processed": len(completed_order),
                "graph_topology_type": "Diamond DAG"
            })

        except Exception as e:
            logger.error(f"Graph reasoning failed: {e}")
            return json.dumps({"error": str(e)})

if __name__ == "__main__":
    agent = H11GraphReasonAgent("GRAPH_01")
    print(agent.process(json.dumps({
        "task": "Design a hybrid vehicle powertrain",
        "enable_merging": True
    })))
