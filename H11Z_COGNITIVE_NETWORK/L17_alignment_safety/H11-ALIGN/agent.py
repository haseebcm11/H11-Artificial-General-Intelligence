import uuid
from dataclasses import dataclass, field
from typing import Any, List, Dict, Tuple, Optional
from enum import Enum

class InterventionType(Enum):
    HALT = "HALT"
    REPLAN = "REPLAN"
    REWEIGHT = "REWEIGHT"
    LOG = "LOG"

@dataclass
class TrajectoryPoint:
    state_vector: List[float]
    action_log_prob: float
    timestamp: float

@dataclass
class AlignmentConstraint:
    id: str
    description: str
    priority: float
    tolerance: float

@dataclass
class InterventionProposal:
    intervention_type: InterventionType
    target_module: str
    adjustment_vector: Optional[List[float]] = None
    reason: str = ""

class AlignmentDAG:
    def __init__(self):
        self.nodes: Dict[str, AlignmentConstraint] = {}
        self.edges: Dict[str, List[str]] = {}
        self.in_degree: Dict[str, int] = {}
        
    def add_constraint(self, constraint: AlignmentConstraint):
        self.nodes[constraint.id] = constraint
        if constraint.id not in self.edges:
            self.edges[constraint.id] = []
            self.in_degree[constraint.id] = 0

    def add_dependency(self, source_id: str, target_id: str):
        if source_id in self.nodes and target_id in self.nodes:
            self.edges[source_id].append(target_id)
            self.in_degree[target_id] = self.in_degree.get(target_id, 0) + 1

    def resolve_conflicts(self) -> List[AlignmentConstraint]:
        # Topological sort based conflict resolution prioritizing higher priority constraints
        sorted_nodes = []
        zero_in_degree = [n for n, deg in self.in_degree.items() if deg == 0]
        zero_in_degree.sort(key=lambda x: self.nodes[x].priority, reverse=True)
        
        in_deg_copy = self.in_degree.copy()
        
        while zero_in_degree:
            curr = zero_in_degree.pop(0)
            sorted_nodes.append(self.nodes[curr])
            for neighbor in self.edges.get(curr, []):
                in_deg_copy[neighbor] -= 1
                if in_deg_copy[neighbor] == 0:
                    zero_in_degree.append(neighbor)
            zero_in_degree.sort(key=lambda x: self.nodes[x].priority, reverse=True)
            
        return sorted_nodes

class H11AlignOrchestrator:
    def __init__(self):
        self.dag = AlignmentDAG()
        self.divergence_threshold = 0.85
        
    def evaluate_trajectory(self, trajectory: List[TrajectoryPoint]) -> float:
        """Evaluates a sequence of states for alignment divergence."""
        if not trajectory:
            return 0.0
        
        divergence = 0.0
        for i in range(1, len(trajectory)):
            prev = trajectory[i-1].state_vector
            curr = trajectory[i].state_vector
            step_div = sum(abs(p - c) for p, c in zip(prev, curr))
            divergence += step_div * trajectory[i].action_log_prob
            
        return divergence / len(trajectory)

    def propose_intervention(self, divergence_score: float) -> Optional[InterventionProposal]:
        """Proposes an intervention if divergence exceeds the threshold."""
        if divergence_score > self.divergence_threshold * 1.5:
            return InterventionProposal(InterventionType.HALT, "GLOBAL", reason="Critical divergence detected.")
        elif divergence_score > self.divergence_threshold:
            return InterventionProposal(
                InterventionType.REPLAN, 
                "PLANNING_MODULE",
                adjustment_vector=[-0.1] * 10,
                reason="Sub-critical divergence, forcing replan."
            )
        return None

    def evaluate_case(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Constraint check on a proposed action — not a dummy trajectory of unit-scaled vitals."""
        violations: List[str] = []
        treat = bool(attrs.get("would_treat"))
        conf = attrs.get("confidence")
        map_mmhg = attrs.get("map_mmhg")
        named = bool(attrs.get("named_protocol"))
        if treat and conf is not None and float(conf) < 0.85:
            violations.append("non_maleficence: confidence below 0.85")
        if treat and map_mmhg is not None and float(map_mmhg) <= 40.0:
            violations.append("homeostasis: critical hypotension")
        if treat and not named:
            violations.append("evidence: no named protocol")
        if violations:
            proposal = InterventionProposal(
                InterventionType.HALT,
                "ACTION",
                reason="; ".join(violations),
            )
            return {
                "allowed": False,
                "divergence": 1.0,
                "intervention": proposal,
                "violations": violations,
            }
        return {"allowed": True, "divergence": 0.0, "intervention": None, "violations": []}

    def update_constraints(self, new_constraints: List[AlignmentConstraint]):
        for c in new_constraints:
            self.dag.add_constraint(c)
        return self.dag.resolve_conflicts()
