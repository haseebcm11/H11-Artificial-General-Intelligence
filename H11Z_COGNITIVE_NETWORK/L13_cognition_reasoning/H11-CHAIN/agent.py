import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum, auto

AGENT_ID = "H11-CHAIN"

class ChainStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()
    DEGRADED = auto()
    FAILED = auto()

class ChainError(ValueError):
    pass

@dataclass(frozen=True)
class ChainInput:
    target_id: str = "default_target"
    intensity: float = 1.0
    batch_size: int = 32
    tolerance: float = 1e-4
    parameters: Dict[str, float] = field(default_factory=lambda: {"alpha": 0.5, "beta": 0.9, "scale": 1.0})
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class ChainOutput:
    agent_id: str
    status: str
    efficiency_score: float
    computed_value: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

@dataclass
class ChainNode:
    id: int
    content: float
    parent: Optional['ChainNode'] = None
    children: List['ChainNode'] = field(default_factory=list)
    utility: float = 0.0

class ChainAgent:
    """Analytical engine for H11-CHAIN. Implements rigorous chain-of-thought 
    probability decay and utility backpropagation."""
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "last_score": 1.0, "status": ChainStatus.IDLE.name}
        self.nodes: List[ChainNode] = []

    def _build_chain(self, depth: int, branch_factor: int) -> ChainNode:
        root = ChainNode(0, 1.0)
        self.nodes = [root]
        current_level = [root]
        
        for d in range(1, depth + 1):
            next_level = []
            for parent in current_level:
                for b in range(branch_factor):
                    child = ChainNode(len(self.nodes), parent.content * math.exp(-0.1 * d), parent)
                    parent.children.append(child)
                    self.nodes.append(child)
                    next_level.append(child)
            current_level = next_level
        return root

    def _backpropagate_utility(self, node: ChainNode) -> float:
        if not node.children:
            node.utility = node.content * 1.5
            return node.utility
        child_utils = [self._backpropagate_utility(c) for c in node.children]
        node.utility = node.content + 0.9 * max(child_utils)
        return node.utility

    def process(self, input_data: Optional[ChainInput] = None) -> ChainOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = ChainInput()

        alpha = float(input_data.parameters.get("alpha", 0.5))
        intensity = float(input_data.intensity)
        depth = max(1, int(intensity * 5))
        branch_factor = max(1, int(alpha * 4))

        root = self._build_chain(depth, branch_factor)
        optimal_utility = self._backpropagate_utility(root)
        
        # Rigorous math: probability of chain coherence
        coherence = 1.0 - math.exp(-optimal_utility / (depth * branch_factor))
        efficiency = min(1.0, max(0.0, coherence))

        status = ChainStatus.OPTIMAL.name if efficiency > 0.8 else ChainStatus.ACTIVE.name
        self.state["evaluations_count"] = self.state.get("evaluations_count", 0) + 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        
        return ChainOutput(
            agent_id=AGENT_ID,
            status=status,
            efficiency_score=efficiency,
            computed_value=optimal_utility,
            execution_time_ms=elapsed_ms,
            metrics={"depth": float(depth), "branching": float(branch_factor), "coherence": coherence},
            diagnostics=["Chain-of-thought decomposition complete."]
        )
