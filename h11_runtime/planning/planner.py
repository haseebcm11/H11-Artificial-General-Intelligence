"""Planner & Autonomous Replanner Engine for H11-AGI (v3.0 Section 10)."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from ..graph.execution_graph import ExecutionGraph, ExecutionNode
from ..graph.types import EdgeType
from ..neural_clustering.neural_cluster_engine import NeuralAgentClusterEngine, NeuralRoutingDecision

logger = logging.getLogger(__name__)


@dataclass
class SubGoal:
    subgoal_id: str
    description: str
    required_capabilities: List[str]
    assigned_specialists: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    completed: bool = False


@dataclass
class CognitivePlan:
    plan_id: str
    primary_goal: str
    subgoals: List[SubGoal] = field(default_factory=list)
    activated_agents: List[str] = field(default_factory=list)
    iteration: int = 1
    max_iterations: int = 3
    is_replanned: bool = False
    replan_rationale: Optional[str] = None
    primary_cluster_id: str = ""
    cluster_affinity: float = 0.0
    routing_probabilities: Dict[str, float] = field(default_factory=dict)


class CognitivePlanner:
    """10 — CognitivePlanner: Autonomous goal decomposition, specialist graph assembly, and replanning."""

    def __init__(self, cluster_engine: Optional[NeuralAgentClusterEngine] = None) -> None:
        self.cluster_engine = cluster_engine

    def create_plan(
        self,
        goal: str,
        retrieved_evidence: Optional[List[Dict[str, Any]]] = None,
        domain_hint: Optional[str] = None,
    ) -> CognitivePlan:
        """Decomposes primary goal into structured subgoals and constructs initial cognitive plan."""
        # 1. MoE Neural Routing
        activated_specialists = []
        primary_cluster_id = domain_hint or ""
        cluster_affinity = 0.0
        routing_probabilities: Dict[str, float] = {}
        if self.cluster_engine:
            routing = self.cluster_engine.route_query(
                query=goal,
                retrieved_evidence=retrieved_evidence or [],
                top_k_agents=6,
            )
            activated_specialists = routing.selected_agent_ids
            primary_cluster_id = routing.primary_cluster_id
            cluster_affinity = routing.cluster_affinity
            routing_probabilities = routing.agent_routing_probabilities
        else:
            activated_specialists = ["H11-REASON", "H11-ANALYTICA", "H11-SYNTHESIS"]

        # 2. Decompose Goal into Subgoals
        subgoals = [
            SubGoal(
                subgoal_id="SG-1-EVIDENCE",
                description=f"Collect domain evidence and facts for: {goal[:60]}",
                required_capabilities=["SEARCH", "EVIDENCE_RETRIEVAL"],
                assigned_specialists=activated_specialists[:2],
            ),
            SubGoal(
                subgoal_id="SG-2-SPECIALIST-REASONING",
                description="Execute specialist domain mathematical and causal analysis",
                required_capabilities=["DOMAIN_ANALYSIS", "REASONING"],
                assigned_specialists=activated_specialists[2:4] or activated_specialists[:2],
                dependencies=["SG-1-EVIDENCE"],
            ),
            SubGoal(
                subgoal_id="SG-3-DELIBERATION-SYNTHESIS",
                description="Synthesize specialist findings and resolve contradictions",
                required_capabilities=["SYNTHESIS", "DELIBERATION"],
                assigned_specialists=activated_specialists[4:] or ["H11-REASON"],
                dependencies=["SG-2-SPECIALIST-REASONING"],
            ),
        ]

        plan = CognitivePlan(
            plan_id=f"PLAN-{abs(hash(goal)) % 1000000:06d}",
            primary_goal=goal,
            subgoals=subgoals,
            activated_agents=activated_specialists,
            primary_cluster_id=primary_cluster_id,
            cluster_affinity=cluster_affinity,
            routing_probabilities=routing_probabilities,
        )
        return plan

    def build_execution_graph(self, plan: CognitivePlan, case_id: str = "") -> ExecutionGraph:
        """Constructs an executable ExecutionGraph from a CognitivePlan."""
        graph = ExecutionGraph(case_id=case_id, graph_id=f"GRAPH-{plan.plan_id}")
        prev_stage_node_ids: List[str] = []

        for sg in plan.subgoals:
            current_stage_node_ids = []
            for ag_id in sg.assigned_specialists:
                # Disambiguate node_id by subgoal
                nid = f"NODE-{sg.subgoal_id}-{ag_id.replace(':', '_').replace('/', '_')}"
                node = graph.add_node(
                    agent_id=ag_id,
                    node_id=nid,
                    canonical_id=ag_id,
                    capability=",".join(sg.required_capabilities),
                )
                current_stage_node_ids.append(node.node_id)
                for prev_nid in prev_stage_node_ids:
                    if prev_nid != node.node_id:
                        graph.add_edge(prev_nid, node.node_id, edge_type=EdgeType.DATA)

            if current_stage_node_ids:
                prev_stage_node_ids = current_stage_node_ids

        return graph

    def replan(
        self,
        current_plan: CognitivePlan,
        rejection_reasons: List[str],
        replan_actions: List[str],
    ) -> Optional[CognitivePlan]:
        """Modifies existing plan by injecting additional specialists, expanding evidence, and iterating."""
        if current_plan.iteration >= current_plan.max_iterations:
            logger.warning(f"Maximum replanning iterations ({current_plan.max_iterations}) reached.")
            return None

        new_iteration = current_plan.iteration + 1
        logger.info(f"Replanning iteration {new_iteration} triggered: {', '.join(rejection_reasons)}")

        # Add arbiter and deep verification specialists
        additional_specialists = ["H11-REASON", "H11-ARBITER", "H11-VERIFICA", "H11-LOGICA"]
        updated_agents = list(set(current_plan.activated_agents + additional_specialists))

        new_subgoals = list(current_plan.subgoals)
        new_subgoals.append(
            SubGoal(
                subgoal_id=f"SG-REPLAN-{new_iteration}",
                description=f"Resolve verification rejections: {'; '.join(rejection_reasons)}",
                required_capabilities=["ARBITRATION", "DEEP_VERIFICATION"],
                assigned_specialists=additional_specialists,
                dependencies=[sg.subgoal_id for sg in current_plan.subgoals],
            )
        )

        replanned = CognitivePlan(
            plan_id=f"{current_plan.plan_id}-R{new_iteration}",
            primary_goal=current_plan.primary_goal,
            subgoals=new_subgoals,
            activated_agents=updated_agents,
            iteration=new_iteration,
            max_iterations=current_plan.max_iterations,
            is_replanned=True,
            replan_rationale="; ".join(rejection_reasons),
            primary_cluster_id=current_plan.primary_cluster_id,
            cluster_affinity=current_plan.cluster_affinity,
            routing_probabilities=dict(current_plan.routing_probabilities),
        )
        return replanned
