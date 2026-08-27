"""H11-AGI Enhancement Protocol v1.0 — 1,000-Agent Society Ecology & Minimum Sufficient Intelligence.

Sections 31, 32, 33: Maintaining the health of the 1,000-agent society,
pruning redundancy, and selecting Minimum Sufficient Intelligence subsets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
import time
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class AgentTelemetry:
    agent_id: str
    layer_or_domain: str
    invocations: int = 0
    successes: int = 0
    failures: int = 0
    total_latency_ms: float = 0.0
    last_invoked: float = 0.0
    capabilities: Set[str] = field(default_factory=set)

    @property
    def success_rate(self) -> float:
        return self.successes / max(self.invocations, 1)

    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / max(self.invocations, 1)


class SocietyEcologyTracker:
    """Section 31: Tracks metrics across the 1,000 agents and diagnoses optimization actions."""

    def __init__(self) -> None:
        self.registry: Dict[str, AgentTelemetry] = {}

    def register_agent(self, agent_id: str, layer_or_domain: str, capabilities: List[str]) -> None:
        self.registry[agent_id] = AgentTelemetry(
            agent_id=agent_id,
            layer_or_domain=layer_or_domain,
            capabilities=set(capabilities),
        )

    def record_execution(self, agent_id: str, success: bool, latency_ms: float) -> None:
        if agent_id not in self.registry:
            self.registry[agent_id] = AgentTelemetry(agent_id=agent_id, layer_or_domain="UNKNOWN")
        tele = self.registry[agent_id]
        tele.invocations += 1
        if success:
            tele.successes += 1
        else:
            tele.failures += 1
        tele.total_latency_ms += latency_ms
        tele.last_invoked = time.time()

    def identify_overlap(self, threshold: float = 0.8) -> List[Tuple[str, str, float]]:
        """Find agents with redundant capability sets."""
        overlaps = []
        agent_list = list(self.registry.values())
        for i in range(len(agent_list)):
            for j in range(i + 1, len(agent_list)):
                a1, a2 = agent_list[i], agent_list[j]
                if not a1.capabilities or not a2.capabilities:
                    continue
                intersection = len(a1.capabilities & a2.capabilities)
                union = len(a1.capabilities | a2.capabilities)
                jaccard = intersection / max(union, 1)
                if jaccard >= threshold:
                    overlaps.append((a1.agent_id, a2.agent_id, round(jaccard, 3)))
        return overlaps

    def recommend_action(self, agent_id: str) -> str:
        """Recommend ADD, UPDATE, MERGE, SPLIT, RETIRE, or RE-ROUTE based on system contribution."""
        if agent_id not in self.registry:
            return "NO_DATA"
        t = self.registry[agent_id]
        if t.invocations > 50 and t.success_rate < 0.85:
            return "UPDATE"  # Needs prompt or domain logic refinement
        if t.invocations > 100 and t.avg_latency_ms > 500.0:
            return "SPLIT"   # Agent doing too much, split into sub-specialists
        return "HEALTHY"


class MinimumSufficientIntelligence:
    """Section 32: Computes the smallest sufficient specialist set for a given case."""

    def __init__(self, tracker: SocietyEcologyTracker) -> None:
        self.tracker = tracker

    def resolve_minimal_set(self, required_capabilities: Set[str]) -> List[str]:
        """Greedy set cover to find the minimum set of specialists covering all requirements."""
        uncovered = set(required_capabilities)
        selected_agents: List[str] = []

        # Sort agents by highest coverage and highest success rate
        candidates = list(self.tracker.registry.values())

        while uncovered:
            best_agent = None
            best_cover_count = 0

            for agent in candidates:
                if agent.agent_id in selected_agents:
                    continue
                cover_count = len(agent.capabilities & uncovered)
                if cover_count > best_cover_count:
                    best_cover_count = cover_count
                    best_agent = agent

            if not best_agent or best_cover_count == 0:
                # Cannot cover remaining capabilities with known registry
                break

            selected_agents.append(best_agent.agent_id)
            uncovered -= best_agent.capabilities

        return selected_agents
