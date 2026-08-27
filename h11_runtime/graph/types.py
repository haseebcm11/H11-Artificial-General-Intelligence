"""Graph edge types."""
from enum import Enum


class EdgeType(str, Enum):
    """The four edge types of H11-AGI execution and composition."""
    DATA = "DATA"              # A output -> B input (typed payload)
    DEPENDENCY = "DEPENDENCY"  # B requires A
    CONTROL = "CONTROL"        # A complete -> permit B
    GOVERNANCE = "GOVERNANCE"  # policy -> execution restriction
