import uuid
import logging
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import graphlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H11-DECOMPOSE")

class DecompositionStrategy(Enum):
    LEAST_TO_MOST = "least_to_most"
    RECURSIVE_DIVIDE = "recursive_divide"
    DEPENDENCY_FIRST = "dependency_first"

@dataclass
class TaskNode:
    id: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    estimated_complexity: float = 1.0
    status: str = "pending"
    metadata: Dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "dependencies": self.dependencies,
            "estimated_complexity": self.estimated_complexity,
            "status": self.status
        }

class TaskGraph:
    def __init__(self):
        self.nodes: Dict[str, TaskNode] = {}
    
    def add_node(self, node: TaskNode):
        self.nodes[node.id] = node
        
    def add_dependency(self, task_id: str, depends_on: str):
        if task_id in self.nodes and depends_on in self.nodes:
            if depends_on not in self.nodes[task_id].dependencies:
                self.nodes[task_id].dependencies.append(depends_on)
        else:
            raise ValueError("Task ID or dependency ID not found in graph.")

    def get_topological_order(self) -> List[str]:
        graph = {}
        for node_id, node in self.nodes.items():
            graph[node_id] = set(node.dependencies)
            
        ts = graphlib.TopologicalSorter(graph)
        try:
            order = list(ts.static_order())
            return order
        except graphlib.CycleError as e:
            logger.error(f"Cycle detected in task graph: {e}")
            raise ValueError(f"Task dependency cycle detected: {e}")

class DecompositionEngine:
    def __init__(self, strategy: DecompositionStrategy = DecompositionStrategy.LEAST_TO_MOST):
        self.strategy = strategy
        self.graph = TaskGraph()
        
    def decompose(self, goal: str, max_depth: int = 3) -> TaskGraph:
        logger.info(f"Decomposing goal: {goal} using strategy: {self.strategy.value}")
        
        # Simulated decomposition logic
        # In a real implementation, this would involve LLM calls or complex heuristic planners.
        if self.strategy == DecompositionStrategy.LEAST_TO_MOST:
            self._least_to_most_decompose(goal, max_depth)
        elif self.strategy == DecompositionStrategy.RECURSIVE_DIVIDE:
            self._recursive_decompose(goal, max_depth, None)
        else:
            self._dependency_first_decompose(goal)
            
        return self.graph

    def _least_to_most_decompose(self, goal: str, depth_limit: int):
        # Generates tasks in increasing order of complexity, chaining dependencies.
        t1 = TaskNode(id=f"T-{uuid.uuid4().hex[:6]}", description="Identify constraints")
        t2 = TaskNode(id=f"T-{uuid.uuid4().hex[:6]}", description="Gather resources", dependencies=[t1.id])
        t3 = TaskNode(id=f"T-{uuid.uuid4().hex[:6]}", description=f"Execute core logic for {goal}", dependencies=[t1.id, t2.id])
        
        self.graph.add_node(t1)
        self.graph.add_node(t2)
        self.graph.add_node(t3)

    def _recursive_decompose(self, goal: str, current_depth: int, parent_id: Optional[str]):
        if current_depth <= 0:
            return
            
        node = TaskNode(id=f"T-{uuid.uuid4().hex[:6]}", description=f"Sub-goal of {goal} at depth {current_depth}")
        if parent_id:
            node.dependencies.append(parent_id)
            
        self.graph.add_node(node)
        
        # Recursive branch 1
        self._recursive_decompose(f"Part A of {goal}", current_depth - 1, node.id)
        # Recursive branch 2
        self._recursive_decompose(f"Part B of {goal}", current_depth - 1, node.id)

    def _dependency_first_decompose(self, goal: str):
        # Identify leaf prerequisites first, then build up
        t_leaf1 = TaskNode(id="req1", description="Prerequisite 1")
        t_leaf2 = TaskNode(id="req2", description="Prerequisite 2")
        t_main = TaskNode(id="main", description=goal, dependencies=["req1", "req2"])
        
        self.graph.add_node(t_leaf1)
        self.graph.add_node(t_leaf2)
        self.graph.add_node(t_main)

def run_decompose(goal: str, strategy: str = "least_to_most") -> Dict:
    strat_enum = DecompositionStrategy(strategy)
    engine = DecompositionEngine(strategy=strat_enum)
    graph = engine.decompose(goal)
    
    try:
        order = graph.get_topological_order()
        is_dag = True
    except ValueError:
        order = []
        is_dag = False
        
    tasks_data = [node.to_dict() for node in graph.nodes.values()]
    
    return {
        "tasks": tasks_data,
        "execution_order": order,
        "is_dag": is_dag
    }

if __name__ == "__main__":
    result = run_decompose("Build a distributed key-value store", "least_to_most")
    print(result)
