import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-AUTOGRAD"

@dataclass
class AutogradInput:
    computation_tape: typing.List[str]
    target_node: str
    intermediate_values: typing.Dict[str, float] = field(default_factory=dict)
    node_derivatives: typing.Dict[str, typing.Dict[str, float]] = field(default_factory=dict)

@dataclass
class AutogradOutput:
    adjoints: typing.Dict[str, float]
    jacobian_matrix: typing.List[typing.List[float]]
    computational_cost: float

class AutogradException(Exception):
    pass

class AutogradAgent:
    """
    Implements reverse-mode automatic differentiation algorithm for the H11 Cognitive Substrate.
    Features:
    - Tape-based AD
    - Jacobian-vector product estimation
    - Graph traversal
    """
    def __init__(self):
        self.gradient_cache = {}

    def _traverse_backward(self, tape: typing.List[str], target: str, derivatives: typing.Dict[str, typing.Dict[str, float]]) -> typing.Dict[str, float]:
        adjoints = {node: 0.0 for node in tape}
        adjoints[target] = 1.0 # Seed the target with 1.0
        
        # Reverse topological sort is assumed by the order of the tape
        for node in reversed(tape):
            if node in derivatives:
                for child, d_child_d_node in derivatives[node].items():
                    adjoints[child] += adjoints[node] * d_child_d_node
                    
        return adjoints

    def process(self, input_data: AutogradInput) -> AutogradOutput:
        if not input_data.computation_tape:
            raise AutogradException("Computation tape is empty.")
            
        adjoints = self._traverse_backward(
            input_data.computation_tape, 
            input_data.target_node, 
            input_data.node_derivatives
        )
        
        # Build Jacobian assuming each tape node is a dimension
        jacobian = []
        for node in input_data.computation_tape:
            row = []
            for other_node in input_data.computation_tape:
                # Approximate or exact depending on derivatives provided
                val = input_data.node_derivatives.get(node, {}).get(other_node, 0.0)
                row.append(val)
            jacobian.append(row)
            
        cost = len(input_data.computation_tape) * 2.5 # Arbitrary FLOP estimate
        
        return AutogradOutput(
            adjoints=adjoints, 
            jacobian_matrix=jacobian,
            computational_cost=cost
        )
