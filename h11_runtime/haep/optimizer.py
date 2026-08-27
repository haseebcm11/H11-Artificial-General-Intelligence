"""H11-AGI Enhancement Protocol v5.0 — Self-Optimization Engine (H11-OPT).

Sections 9, 14, 15, 21, 25, 26, 27, 28, 29, 30, 59, 60, 96: Central H11-OPT optimizer,
bottleneck detection & migration, marginal intelligence gain (MIG), elasticity, and compilation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Dict, List, Optional, Set, Tuple

from .protocol import (
    OptimizationDomain,
    OptimizationRegime,
    SystemState,
)


@dataclass
class BottleneckRecord:
    bottleneck_id: str
    target_capability: str
    weakest_component: str
    limiting_factor: str  # COMPUTE, MEMORY, ROUTING, REASONING, KNOWLEDGE
    severity: float = 0.85
    upstream_origin: Optional[str] = None
    is_resolved: bool = False


@dataclass
class CompiledIntelligencePathway:
    pathway_id: str
    pattern_signature: str
    specialists: List[str]
    speedup_factor: float = 3.5
    usage_count: int = 1
    created_at: float = field(default_factory=time.time)


class SelfOptimizer:
    """Section 9: Central H11-OPT Self-Optimization Controller."""

    def __init__(self) -> None:
        self.active_bottlenecks: Dict[str, BottleneckRecord] = {}
        self.compiled_pathways: Dict[str, CompiledIntelligencePathway] = {}
        self.cached_capabilities: Dict[str, List[str]] = {}

    def detect_bottleneck(
        self,
        capability: str,
        dependency_graph: Dict[str, List[str]],
        component_latencies: Dict[str, float],
    ) -> BottleneckRecord:
        """Section 27 & 28: Identifies limiting bottleneck and traces upstream propagation."""
        # Find highest latency component in the capability's dependency chain
        deps = dependency_graph.get(capability, list(component_latencies.keys()))
        weakest = max(deps, key=lambda c: component_latencies.get(c, 0.0))
        rec = BottleneckRecord(
            bottleneck_id=f"BN-{len(self.active_bottlenecks) + 1}",
            target_capability=capability,
            weakest_component=weakest,
            limiting_factor="REASONING_LATENCY" if "reason" in weakest.lower() else "ROUTING_HOP",
            severity=component_latencies.get(weakest, 0.8),
            upstream_origin=deps[0] if deps else None,
        )
        self.active_bottlenecks[rec.bottleneck_id] = rec
        return rec

    def compute_mig(self, delta_capability: float, delta_resources: float) -> float:
        """Section 25: Marginal Intelligence Gain (MIG) = delta_capability / delta_resources."""
        res = max(delta_resources, 0.01)
        return round(delta_capability / res, 4)

    def is_intelligence_saturated(self, mig_history: List[float], threshold: float = 0.05) -> bool:
        """Section 26: Detects compute saturation when MIG drops below threshold."""
        if len(mig_history) < 2:
            return False
        return mig_history[-1] < threshold

    def escalate_regime(self, current_regime: OptimizationRegime, failure_count: int) -> OptimizationRegime:
        """Section 15: Optimization Escalation: LOCAL -> COMPOSITION -> STRUCTURAL -> ARCHITECTURAL -> META."""
        if failure_count >= 2 and current_regime < OptimizationRegime.REGIME_5_META:
            return OptimizationRegime(current_regime.value + 1)
        return current_regime

    def compile_intelligence_pathway(
        self,
        signature: str,
        specialists: List[str],
    ) -> CompiledIntelligencePathway:
        """Section 59: Transforms repeated dynamic multi-agent interaction into a compiled pathway."""
        path = CompiledIntelligencePathway(
            pathway_id=f"COMP-{len(self.compiled_pathways) + 1}",
            pattern_signature=signature,
            specialists=specialists,
            speedup_factor=3.8,
        )
        self.compiled_pathways[signature] = path
        return path

    def should_acquire_information(self, uncertainty: float, risk: float) -> bool:
        """Section 96: Determines if Information Acquisition is preferred over immediate transformation."""
        return uncertainty > 0.4 and risk > 0.3
