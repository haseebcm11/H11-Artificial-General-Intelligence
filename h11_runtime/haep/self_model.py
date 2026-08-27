"""H11-AGI Enhancement Protocol v3.0 — Self-Model, Capability Graphs, & Gap Engine.

Sections 5, 6, 7, 12, 14, 18, 19: The explicit internal self-representation of H11-AGI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Dict, List, Optional, Set, Tuple

from .protocol import (
    DeficiencyType,
    EmergentCapabilityRecord,
    IntelligenceLevel,
    SolutionType,
    SystemState,
)


@dataclass
class CapabilityNode:
    name: str
    provided_by: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    enhanced_by: List[str] = field(default_factory=list)
    constrained_by: List[str] = field(default_factory=list)
    known_limitations: List[str] = field(default_factory=list)
    performance_score: float = 0.95


class H11SelfModel:
    """Section 5, 6, 7: Explicit live self-model of H11-AGI constitution and capabilities."""

    def __init__(self) -> None:
        self.capability_graph: Dict[str, CapabilityNode] = {}
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.dependency_graph: Dict[str, List[str]] = {}
        self.known_limitations: List[str] = []
        self.emergent_capabilities: List[EmergentCapabilityRecord] = []
        self._init_base_capabilities()

    def _init_base_capabilities(self) -> None:
        self.register_capability(
            name="MULTIDISCIPLINARY_REASONING",
            provided_by=["H11-REASON", "H11-ROUTER", "H11-SYNTHESIS"],
            depends_on=["FORMAL_LOGIC", "KNOWLEDGE_RETRIEVAL", "WORLD_MODEL"],
            known_limitations=["Edge case conflicts between physical & chemical domains"],
        )
        self.register_capability(
            name="NEURAL_INFERENCE_OPTIMAL",
            provided_by=["H11-GPU", "H11-TPU", "H11-PAGED-ATTENTION"],
            depends_on=["HARDWARE_ACCELERATION", "KV_CACHE"],
        )
        self.register_capability(
            name="GOVERNED_ADMISSION",
            provided_by=["H11C-POLICY-ENGINE", "H11C-ACTION-LICENSE", "H11C-AUDIT-CHAIN"],
            depends_on=["ZERO_TRUST", "ALIGN_CONSTRAINTS"],
        )

    def register_capability(
        self,
        name: str,
        provided_by: List[str],
        depends_on: Optional[List[str]] = None,
        known_limitations: Optional[List[str]] = None,
    ) -> None:
        self.capability_graph[name] = CapabilityNode(
            name=name,
            provided_by=provided_by,
            depends_on=depends_on or [],
            known_limitations=known_limitations or [],
        )

    def get_self_summary(self) -> Dict[str, Any]:
        """Answers: What am I? What can I do? Where are my limitations?"""
        return {
            "total_capabilities": len(self.capability_graph),
            "pillars": 3,
            "total_agents": 1000,
            "known_limitations": [l for c in self.capability_graph.values() for l in c.known_limitations],
            "emergent_capabilities_count": len(self.emergent_capabilities),
        }


class CapabilityGapEngine:
    """Section 12: Continuous calculation of Required Capability - Available Capability."""

    def __init__(self, self_model: H11SelfModel) -> None:
        self.self_model = self_model

    def compute_gap(self, required_capabilities: Set[str]) -> Tuple[Set[str], float]:
        available = set(self.self_model.capability_graph.keys())
        gap = required_capabilities - available
        severity = len(gap) / max(len(required_capabilities), 1)
        return gap, severity


class KnowledgeVsArchitectureDecider:
    """Section 14: Determines whether a deficiency is Knowledge, Reasoning, Composition, or Substrate."""

    def decide_deficiency_type(self, target: str, symptom: str, context: Dict[str, Any]) -> Tuple[DeficiencyType, SolutionType, str]:
        if "outdated" in symptom.lower() or "missing_fact" in symptom.lower():
            return DeficiencyType.KNOWLEDGE, SolutionType.LOCAL, "Acquire or repair domain knowledge base"
        elif "logic" in symptom.lower() or "deduction" in symptom.lower() or "reason" in target.lower():
            return DeficiencyType.REASONING, SolutionType.LOCAL, "Cognitive reasoning logic refinement"
        elif "routing" in symptom.lower() or "cascade" in symptom.lower() or "conflict" in symptom.lower():
            return DeficiencyType.COMPOSITION, SolutionType.COMPOSITIONAL, "Routing and specialist composition restructuring"
        else:
            return DeficiencyType.SUBSTRATE, SolutionType.STRUCTURAL, "Substrate architecture and core graph enhancement"


class EmergentCapabilityDetector:
    """Section 18: Detects capabilities emerging from multi-agent interaction."""

    def __init__(self, self_model: H11SelfModel) -> None:
        self.self_model = self_model

    def detect_emergent_capability(
        self,
        specialists: List[str],
        task_class: str,
        observed_behavior: str,
        score: float,
    ) -> Optional[EmergentCapabilityRecord]:
        if len(specialists) >= 2 and score >= 0.95:
            rec = EmergentCapabilityRecord(
                name=f"EMERGENT_{task_class.upper()}",
                originating_specialists=specialists,
                composition_topology="PARALLEL_SYNERGY",
                triggering_task_class=task_class,
                observed_behavior=observed_behavior,
                reliability_score=score,
            )
            self.self_model.emergent_capabilities.append(rec)
            return rec
        return None


class CapabilityAttributionEngine:
    """Section 19: Identifies what actually caused a performance improvement."""

    def attribute_cause(self, candidate_delta: Dict[str, Any]) -> str:
        if candidate_delta.get("routing_changed"):
            return "ROUTING"
        elif candidate_delta.get("code_updated"):
            return "AGENT_IMPLEMENTATION"
        elif candidate_delta.get("knowledge_added"):
            return "KNOWLEDGE_BASE"
        elif candidate_delta.get("composition_reordered"):
            return "COMPOSITION"
        return "MODEL_COGNITION"
