"""H11-CONSTITUTION: Constitutional AI alignment and scoring engine.

L17_alignment_safety - Substrate

Implements principle-based constitutional evaluation using an exponential 
penalty model. Computes composite risk scores from simulated violation probabilities 
and generates localized critiques/revisions based on severity-weighted principles.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

AGENT_ID = "H11-CONSTITUTION"


class ConstitutionError(ValueError):
    """Domain-specific error for H11-CONSTITUTION."""
    pass


@dataclass(frozen=True)
class Principle:
    id: str
    description: str
    severity_weight: float  # Range [1.0, 10.0]


@dataclass(frozen=True)
class ConstitutionInput:
    draft_id: str
    # Map of principle ID to estimated probability of violation [0.0, 1.0]
    violation_probs: Dict[str, float]
    principles: List[Principle]
    risk_tolerance: float = 0.1  # Maximum allowable composite risk


@dataclass(frozen=True)
class ConstitutionOutput:
    agent_id: str
    draft_id: str
    is_compliant: bool
    composite_risk_score: float
    critiques: Dict[str, str]
    revision_directives: List[str]
    execution_time_ms: float


class ConstitutionAgent:
    """Analytical engine for Constitutional AI processing."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: Optional[ConstitutionInput] = None) -> ConstitutionOutput:
        start_time = time.perf_counter()
        if input_data is None:
            raise ConstitutionError("Input data must be provided")

        if not (0.0 < input_data.risk_tolerance < 1.0):
            raise ConstitutionError("Risk tolerance must be in (0, 1)")

        total_penalty = 0.0
        critiques: Dict[str, str] = {}
        directives: List[str] = []

        # Map for quick lookup
        principle_map = {p.id: p for p in input_data.principles}

        for p_id, p_prob in input_data.violation_probs.items():
            if not (0.0 <= p_prob <= 1.0):
                raise ConstitutionError(f"Violation probability for {p_id} out of bounds")
            
            if p_id not in principle_map:
                continue

            principle = principle_map[p_id]
            # Exponential accumulation of risk
            penalty = principle.severity_weight * p_prob
            total_penalty += penalty

            # Generate critique if isolated probability is non-trivial
            if p_prob > 0.3:
                critiques[p_id] = f"Potential violation (p={p_prob:.2f}) of '{principle.description}'"
                
                # Propose structural revision directive
                if principle.severity_weight > 7.0:
                    directives.append(f"CRITICAL REDACT: Modify response to adhere to {p_id} (High Severity).")
                else:
                    directives.append(f"SOFTEN TONE: Adjust framing to better align with {p_id}.")

        # Composite risk score using an inverse exponential decay function
        # Score approaches 1.0 as total penalty goes to infinity.
        composite_risk = 1.0 - math.exp(-total_penalty)
        
        is_compliant = composite_risk <= input_data.risk_tolerance

        if not is_compliant and not directives:
            directives.append("GENERAL REVISION: Draft exceeds aggregate constitutional risk tolerance.")

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return ConstitutionOutput(
            agent_id=AGENT_ID,
            draft_id=input_data.draft_id,
            is_compliant=is_compliant,
            composite_risk_score=round(composite_risk, 6),
            critiques=critiques,
            revision_directives=directives,
            execution_time_ms=round(elapsed_ms, 4)
        )
