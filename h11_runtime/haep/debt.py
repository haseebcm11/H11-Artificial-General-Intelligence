"""H11-AGI Enhancement Protocol v4.0 — Evolution Debt & Complexity Compression.

Sections 31, 32, 33, 34, 35, 36, 48: Debt prioritization, complexity compression,
capability density maximization, and overfitting protection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Dict, List, Optional, Tuple

from .protocol import EvolutionDebt


class EvolutionDebtManager:
    """Section 31 & 34: Manages structural debt and optimizes complexity compression."""

    def __init__(self, max_complexity_budget: float = 1.0) -> None:
        self.debt = EvolutionDebt()
        self.max_complexity_budget = max_complexity_budget

    def record_debt(self, debt_type: str, amount: float) -> None:
        if debt_type == "technical":
            self.debt.technical_debt += amount
        elif debt_type == "architectural":
            self.debt.architectural_debt += amount
        elif debt_type == "capability":
            self.debt.capability_debt += amount
        elif debt_type == "security":
            self.debt.security_debt += amount
        elif debt_type == "governance":
            self.debt.governance_debt += amount

    def check_complexity_budget(self, current_complexity: float, delta_complexity: float) -> Tuple[bool, str]:
        """Section 33: Ensures new transitions do not exceed complexity budget."""
        new_total = current_complexity + delta_complexity
        if new_total > self.max_complexity_budget:
            return False, f"COMPLEXITY_BUDGET_EXCEEDED: New complexity {new_total:.2f} > max budget {self.max_complexity_budget:.2f}"
        return True, "COMPLEXITY_WITHIN_BUDGET"

    def detect_overfitting(self, validation_gain: float, general_system_gain: float) -> Tuple[bool, str]:
        """Section 48: Flags candidates that overfit benchmark vs real-world general performance."""
        if validation_gain > 0.15 and general_system_gain < -0.02:
            return True, "EVOLUTION_OVERFIT_DETECTED: Candidate improved test suite but degraded global performance"
        return False, "GENERALIZATION_VERIFIED"
