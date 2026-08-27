"""Reflexion Search Loop, Tree-of-Thought Planning & Epistemic Uncertainty.

Implements:
- Tree-of-Thought (ToT) multi-branch search query planning.
- Uncertainty Quantification:
  * Epistemic Uncertainty (knowledge deficit / missing evidence)
  * Aleatoric Uncertainty (inherent statistical ambiguity)
- Reflexion Loop: Dynamically identifies missing evidence gaps and generates
  recursive follow-up queries to resolve premises autonomously.
"""
from __future__ import annotations

import logging
import math
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class SearchThoughtNode:
    """A thought branch in the Tree-of-Thought search decomposition."""
    thought_id: str
    sub_goal: str
    query_string: str
    expected_evidence_type: str
    parent_id: Optional[str] = None
    children: List[SearchThoughtNode] = field(default_factory=list)
    confidence: float = 1.0


@dataclass
class UncertaintyEstimate:
    """Decomposed uncertainty estimation of retrieved evidence."""
    total_uncertainty: float     # [0.0, 1.0]
    epistemic_uncertainty: float # [0.0, 1.0] (reduces with more search)
    aleatoric_uncertainty: float # [0.0, 1.0] (inherent noise)
    has_information_gap: bool
    missing_premises: List[str] = field(default_factory=list)


@dataclass
class ReflexionCycleResult:
    """Outcome of a self-reflecting search iteration."""
    iteration: int
    resolved: bool
    uncertainty: UncertaintyEstimate
    generated_followup_queries: List[str]
    synthesized_notes: str


class ReflexionSearchLoop:
    """Executes Tree-of-Thought query expansion and recursive gap-resolving reflexion."""

    def __init__(self, max_reflexion_depth: int = 3, epistemic_threshold: float = 0.35) -> None:
        self.max_depth = max_reflexion_depth
        self.epistemic_threshold = epistemic_threshold

    def plan_tree_of_thoughts(self, goal_prompt: str) -> SearchThoughtNode:
        """Decomposes a complex prompt into a Tree-of-Thought hierarchy of search sub-goals."""
        root = SearchThoughtNode(
            thought_id="T0",
            sub_goal="Primary Goal Evaluation",
            query_string=goal_prompt,
            expected_evidence_type="OVERVIEW",
        )

        # Heuristic branch decomposition
        # Branch 1: Foundational mechanism & definitions
        b1 = SearchThoughtNode(
            thought_id="T1",
            sub_goal="Fundamental Mechanisms & Principles",
            query_string=f"Mechanism and definition of {goal_prompt}",
            expected_evidence_type="MECHANISM",
            parent_id="T0",
        )

        # Branch 2: State-of-the-art clinical/empirical benchmarks
        b2 = SearchThoughtNode(
            thought_id="T2",
            sub_goal="Empirical Benchmarks & Efficacy",
            query_string=f"Clinical efficacy benchmarks for {goal_prompt}",
            expected_evidence_type="EMPIRICAL",
            parent_id="T0",
        )

        # Branch 3: Contraindications and edge cases
        b3 = SearchThoughtNode(
            thought_id="T3",
            sub_goal="Safety, Contraindications & Limits",
            query_string=f"Safety limits contraindications {goal_prompt}",
            expected_evidence_type="SAFETY",
            parent_id="T0",
        )

        root.children = [b1, b2, b3]
        return root

    def estimate_uncertainty(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> UncertaintyEstimate:
        """Quantifies epistemic vs aleatoric uncertainty from retrieved document corpus."""
        if not retrieved_docs:
            return UncertaintyEstimate(
                total_uncertainty=1.0,
                epistemic_uncertainty=1.0,
                aleatoric_uncertainty=0.1,
                has_information_gap=True,
                missing_premises=["Zero documents retrieved for the requested query."],
            )

        query_terms = set(re.findall(r"\w+", query.lower())) - {"what", "is", "the", "for", "and", "in", "of"}
        combined_text = " ".join([d.get("title", "") + " " + d.get("snippet", "") for d in retrieved_docs]).lower()

        # Check coverage of key query terms
        missing_terms = [t for t in query_terms if t not in combined_text]
        coverage_ratio = (len(query_terms) - len(missing_terms)) / max(1, len(query_terms))

        # Check document source diversity
        sources = {d.get("source", "web") for d in retrieved_docs}
        source_diversity_factor = min(1.0, len(sources) / 3.0)

        # Epistemic uncertainty is high if query terms are missing or source diversity is low
        epistemic = max(0.0, 1.0 - (coverage_ratio * 0.7 + source_diversity_factor * 0.3))

        # Aleatoric uncertainty (variance in document scores)
        scores = [d.get("score", 0.5) for d in retrieved_docs]
        mean_s = sum(scores) / len(scores) if scores else 0.5
        variance = sum((s - mean_s) ** 2 for s in scores) / max(1, len(scores))
        aleatoric = min(0.5, math.sqrt(variance))

        total_unc = min(1.0, epistemic + aleatoric)
        has_gap = epistemic > self.epistemic_threshold

        missing_premises = []
        if missing_terms:
            missing_premises.append(f"Missing specific evidence addressing: {', '.join(missing_terms)}")
        if len(retrieved_docs) < 3:
            missing_premises.append("Low evidence sample count (fewer than 3 independent sources).")

        return UncertaintyEstimate(
            total_uncertainty=round(total_unc, 3),
            epistemic_uncertainty=round(epistemic, 3),
            aleatoric_uncertainty=round(aleatoric, 3),
            has_information_gap=has_gap,
            missing_premises=missing_premises,
        )

    def reflect_and_generate_followups(self, query: str, uncertainty: UncertaintyEstimate) -> List[str]:
        """Generates targeted follow-up queries to resolve identified information gaps."""
        if not uncertainty.has_information_gap:
            return []

        followups = []
        for premise in uncertainty.missing_premises:
            if "Missing specific evidence addressing:" in premise:
                terms = premise.split(":")[-1].strip()
                followups.append(f"{query} specifically regarding {terms}")
            elif "Low evidence sample count" in premise:
                followups.append(f"{query} systematic review academic literature")

        if not followups:
            followups.append(f"{query} primary research data")

        return followups[:3]
