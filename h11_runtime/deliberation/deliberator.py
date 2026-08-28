"""Deliberation Layer: Cross-Agent Agreement, Disagreement, Contradiction Detection, and Synthesis."""
from __future__ import annotations

import collections
import difflib
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from ..contracts.agent_result import AgentResult

logger = logging.getLogger(__name__)


@dataclass
class SynthesisCandidate:
    """Consolidated deliberation output synthesized across multiple specialist agents."""
    consensus_claims: List[str] = field(default_factory=list)
    disputed_claims: List[Dict[str, Any]] = field(default_factory=list)
    contradictions: List[Dict[str, Any]] = field(default_factory=list)
    weighed_evidence: List[Dict[str, Any]] = field(default_factory=list)
    unsupported_claims: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    synthesized_output: Dict[str, Any] = field(default_factory=dict)
    overall_confidence: float = 0.90
    uncertainty_score: float = 0.10
    needs_additional_specialists: bool = False
    recommended_specialists: List[str] = field(default_factory=list)
    deliberation_summary: str = ""


class Deliberator:
    """08 — Deliberator: Cross-agent deliberation, contradiction resolution, and evidence weighing (v3.0 Section 8)."""

    def __init__(self, agreement_threshold: float = 0.65, contradiction_threshold: float = 0.35) -> None:
        self.agreement_threshold = agreement_threshold
        self.contradiction_threshold = contradiction_threshold

    def deliberate(self, agent_results: List[AgentResult], query_context: str = "") -> SynthesisCandidate:
        """Processes specialist outputs through cross-agent deliberation."""
        if not agent_results:
            return SynthesisCandidate(
                overall_confidence=0.0,
                uncertainty_score=1.0,
                deliberation_summary="No specialist results provided for deliberation.",
            )

        all_claims: List[Tuple[str, str, float]] = []  # (agent_id, claim_text, confidence)
        all_evidence: List[Dict[str, Any]] = []
        all_assumptions: List[str] = []
        all_actions: List[str] = []
        total_conf = 0.0
        success_count = 0

        for res in agent_results:
            if res.success:
                success_count += 1
                total_conf += res.confidence
                for claim in res.claims:
                    all_claims.append((res.agent_id, claim, res.confidence))
                all_evidence.extend(res.evidence)
                all_assumptions.extend(res.assumptions)
                all_actions.extend(res.proposed_actions)

        avg_conf = (total_conf / success_count) if success_count > 0 else 0.5
        consensus_claims: List[str] = []
        disputed_claims: List[Dict[str, Any]] = []
        contradictions: List[Dict[str, Any]] = []
        unsupported_claims: List[str] = []

        # 1. Cluster and Compare Claims
        seen_claims: Set[str] = set()
        for i, (ag1, claim1, c1) in enumerate(all_claims):
            if claim1 in seen_claims:
                continue
            seen_claims.add(claim1)

            supporting_agents = [ag1]
            opposing_agents = []

            for j, (ag2, claim2, c2) in enumerate(all_claims):
                if i == j:
                    continue
                similarity = difflib.SequenceMatcher(None, claim1.lower(), claim2.lower()).ratio()
                if similarity >= self.agreement_threshold:
                    if ag2 not in supporting_agents:
                        supporting_agents.append(ag2)
                elif self._is_contradiction(claim1, claim2):
                    opposing_agents.append((ag2, claim2))

            if opposing_agents:
                contradictions.append({
                    "primary_claim": claim1,
                    "primary_agent": ag1,
                    "opposing": [{"agent": a, "claim": c} for a, c in opposing_agents],
                })
            elif len(supporting_agents) >= 2 or len(agent_results) == 1:
                consensus_claims.append(claim1)
            else:
                disputed_claims.append({
                    "claim": claim1,
                    "agent": ag1,
                    "confidence": c1,
                })

        # 2. Evidence Support Evaluation
        evidence_sources = {str(e.get("url") or e.get("source") or "") for e in all_evidence}
        for claim in consensus_claims + [d["claim"] for d in disputed_claims]:
            words = set(claim.lower().split())
            supported = any(
                len(words.intersection(set(str(e.get("title") or e.get("snippet") or "").lower().split()))) >= 2
                for e in all_evidence
            )
            if not supported and len(all_evidence) > 0:
                unsupported_claims.append(claim)

        # 3. Formulate Synthesized Output
        synthesized_data: Dict[str, Any] = {
            "query": query_context,
            "participating_agents": [r.agent_id for r in agent_results],
            "total_agents_deliberated": len(agent_results),
            "consensus_count": len(consensus_claims),
            "contradiction_count": len(contradictions),
            "primary_action": all_actions[0] if all_actions else "REASON",
            "findings": consensus_claims or [r.agent_id for r in agent_results],
        }

        # 4. Uncertainty & Replanning Signals
        uncertainty = 1.0 - avg_conf
        if contradictions:
            uncertainty = min(1.0, uncertainty + 0.25 * len(contradictions))
        if unsupported_claims:
            uncertainty = min(1.0, uncertainty + 0.15)

        needs_replan = len(contradictions) > 0 or uncertainty > 0.45
        recommended_specialists = []
        if contradictions:
            recommended_specialists.extend(["H11-REASON", "H11-VERIFICA", "H11-ARBITER"])

        summary = (
            f"Deliberated across {len(agent_results)} specialists. "
            f"Consensus claims: {len(consensus_claims)}, Contradictions: {len(contradictions)}, "
            f"Uncertainty: {uncertainty:.2f}."
        )

        return SynthesisCandidate(
            consensus_claims=consensus_claims,
            disputed_claims=disputed_claims,
            contradictions=contradictions,
            weighed_evidence=all_evidence,
            unsupported_claims=unsupported_claims,
            assumptions=all_assumptions,
            synthesized_output=synthesized_data,
            overall_confidence=max(0.1, 1.0 - uncertainty),
            uncertainty_score=uncertainty,
            needs_additional_specialists=needs_replan,
            recommended_specialists=recommended_specialists,
            deliberation_summary=summary,
        )

    def _is_contradiction(self, claim1: str, claim2: str) -> bool:
        """Simple negation and opposite detection between two assertions."""
        c1 = claim1.lower()
        c2 = claim2.lower()
        negations = ["not", "no", "never", "cannot", "inhibits", "blocks", "decreases", "fails"]
        has_neg1 = any(f" {n} " in f" {c1} " for n in negations)
        has_neg2 = any(f" {n} " in f" {c2} " for n in negations)
        if has_neg1 != has_neg2:
            sim = difflib.SequenceMatcher(None, c1, c2).ratio()
            if sim > 0.5:
                return True
        return False
