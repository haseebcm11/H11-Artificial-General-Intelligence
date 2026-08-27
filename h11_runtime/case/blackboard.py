"""Blackboard shared case workspace."""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Set
import uuid

from ..contracts import AgentResult


class Blackboard:
    """03 — Blackboard: The shared concurrent case workspace (v3.0 Section 18-19)."""

    def __init__(self, case_id: str) -> None:
        self.case_id = case_id
        self.facts: Dict[str, Any] = {}
        self.hypotheses: List[Dict[str, Any]] = []
        self.task_state: Dict[str, Any] = {}
        self.active_agents: Set[str] = set()
        self.intermediate_results: Dict[str, Any] = {}
        self.agent_results: Dict[str, AgentResult] = {}
        self.evidence: List[Dict[str, Any]] = []
        self.evidence_chain: List[Dict[str, Any]] = self.evidence
        self.conflicts: List[Dict[str, Any]] = []
        self.plans: List[Dict[str, Any]] = []
        self.goals: List[str] = []
        self.decisions: List[Dict[str, Any]] = []
        self.confidence: Dict[str, float] = {}
        self.confidence_scores: Dict[str, float] = self.confidence
        self.constraints: List[str] = []

    def post_fact(self, key: str, value: Any, source_agent: str = "KERNEL") -> None:
        self.facts[key] = {
            "value": value,
            "source": source_agent,
            "timestamp": time.time(),
        }

    def get_fact(self, key: str) -> Optional[Any]:
        f = self.facts.get(key)
        return f["value"] if f else None

    def post_hypothesis(self, hypothesis: str, proposer: str, confidence: float = 0.5) -> None:
        self.hypotheses.append({
            "hypothesis": hypothesis,
            "proposer": proposer,
            "confidence": confidence,
            "timestamp": time.time(),
        })

    def post_result(self, agent_id: str, result: Any) -> None:
        self.agent_results[agent_id] = result
        self.intermediate_results[agent_id] = getattr(result, "output_data", getattr(result, "data", result))
        self.confidence[agent_id] = getattr(result, "confidence", 1.0)

    def post_evidence(self, claim: str, source: str, confidence: float = 0.95, provenance: str = "") -> None:
        self.evidence.append({
            "claim": claim,
            "source": source,
            "confidence": confidence,
            "provenance": provenance,
            "timestamp": time.time(),
        })

    def register_conflict(self, conflict_type: str, propositions: List[Dict[str, Any]]) -> Dict[str, Any]:
        conf = {
            "conflict_id": f"CONF-{uuid.uuid4().hex[:6].upper()}",
            "type": conflict_type,
            "propositions": propositions,
            "resolved": False,
            "timestamp": time.time(),
        }
        self.conflicts.append(conf)
        return conf

    def post_plan(self, goal: str, steps: List[str]) -> None:
        self.plans.append({
            "goal": goal,
            "steps": steps,
            "timestamp": time.time(),
        })

    def post_decision(self, decision: str, rationale: str, deciding_agent: str = "H11C-CONSENSUS") -> None:
        self.decisions.append({
            "decision": decision,
            "rationale": rationale,
            "deciding_agent": deciding_agent,
            "timestamp": time.time(),
        })
