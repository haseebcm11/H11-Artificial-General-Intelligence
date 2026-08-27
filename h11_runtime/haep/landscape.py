"""H11-AGI Enhancement Protocol v4.0 — Capability Landscape & Discovery Engine.

Sections 9, 10, 11, 13, 14: Mapping capabilities, exploring the UNKNOWN state,
capability decomposition, and dependency origin tracing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Dict, List, Optional, Set, Tuple

from .protocol import CapabilityStatus


@dataclass
class DecomposedCapability:
    """Section 13: 7-component Capability Decomposition."""
    prerequisite: str = "VALIDATED_INPUT"
    perception: str = "MULTIMODAL_INGEST"
    memory: str = "EPISODIC_RECALL"
    reasoning: str = "FORMAL_DEDUCTION"
    planning: str = "TOPOLOGICAL_GRAPH"
    execution: str = "PARALLEL_DISPATCH"
    verification: str = "SCHEMA_ASSERT"


@dataclass
class LandscapeCapability:
    """Section 9: Detailed landscape profile for each capability."""
    capability_id: str
    description: str
    providers: List[str]
    dependencies: List[str] = field(default_factory=list)
    performance: float = 0.95
    reliability: float = 0.98
    status: CapabilityStatus = CapabilityStatus.KNOWN_STRONG
    decomposition: DecomposedCapability = field(default_factory=DecomposedCapability)
    failure_modes: List[str] = field(default_factory=list)
    last_evaluated: float = field(default_factory=time.time)


class CapabilityLandscape:
    """Section 9: Continuous live landscape of all 1,000-agent capabilities."""

    def __init__(self) -> None:
        self.capabilities: Dict[str, LandscapeCapability] = {}
        self._init_landscape()

    def _init_landscape(self) -> None:
        self.register_capability(
            cap_id="QUANTUM_SIMULATION",
            desc="High-fidelity Hamiltonian quantum state simulation",
            providers=["H11_QUANTUM", "H11_PHYSICA"],
            dependencies=["FORMAL_CALCULUS"],
            status=CapabilityStatus.KNOWN_STRONG,
        )
        self.register_capability(
            cap_id="PHOTONIC_COMPUTATION",
            desc="Sub-nanosecond optical waveguide routing",
            providers=["H11_PHOTONIC"],
            status=CapabilityStatus.KNOWN_STRONG,
        )
        self.register_capability(
            cap_id="EXOTIC_PROPULSION",
            desc="Alcubierre warp metric energy constraint calculation",
            providers=[],
            status=CapabilityStatus.UNKNOWN,
        )

    def register_capability(
        self,
        cap_id: str,
        desc: str,
        providers: List[str],
        dependencies: Optional[List[str]] = None,
        status: CapabilityStatus = CapabilityStatus.KNOWN_STRONG,
    ) -> LandscapeCapability:
        cap = LandscapeCapability(
            capability_id=cap_id,
            description=desc,
            providers=providers,
            dependencies=dependencies or [],
            status=status,
        )
        self.capabilities[cap_id] = cap
        return cap

    def trace_dependency_origin(self, cap_id: str) -> List[str]:
        """Section 14: Trace downstream failure to its root dependency origin."""
        if cap_id not in self.capabilities:
            return []
        visited = []
        stack = list(self.capabilities[cap_id].dependencies)
        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.append(curr)
                if curr in self.capabilities:
                    stack.extend(self.capabilities[curr].dependencies)
        return visited

    def discover_latent_capability(
        self,
        target_name: str,
        composing_agents: List[str],
        test_score: float,
    ) -> Tuple[bool, LandscapeCapability]:
        """Section 11: Capability Discovery via composite specialist interaction."""
        status = CapabilityStatus.EMERGENT if test_score >= 0.95 else CapabilityStatus.KNOWN_WEAK
        cap = self.register_capability(
            cap_id=target_name,
            desc=f"Discovered capability composed from {', '.join(composing_agents)}",
            providers=composing_agents,
            status=status,
        )
        return test_score >= 0.95, cap
