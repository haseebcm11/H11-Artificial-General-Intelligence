"""
H11-ALLERGOLOGIA: Allergology & hypersensitivity
Layer 1 - Medicine & Health Sciences

This module implements the cognitive and analytical substrate for evaluating 
allergic reactions, profiling hypersensitivity, and computing immunotherapy 
trajectories. It utilizes a stateful Bayesian inference system combined with 
PK/PD modeling for desensitization protocols.
"""

from __future__ import annotations
import asyncio
import logging
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Protocol, Sequence, Tuple, Set

logger = logging.getLogger(__name__)

class HypersensitivityType(Enum):
    TYPE_I_IMMEDIATE = auto()
    TYPE_II_CYTOTOXIC = auto()
    TYPE_III_IMMUNE_COMPLEX = auto()
    TYPE_IV_DELAYED = auto()
    MIXED_PATTERN = auto()

class AllergenRoute(Enum):
    INHALATION = auto()
    INGESTION = auto()
    INJECTION = auto()
    CONTACT = auto()

@dataclass
class AllergenExposure:
    allergen_id: str
    route: AllergenRoute
    dose_micrograms: float
    timestamp_sec: float
    duration_sec: float

@dataclass
class AtopyProfile:
    patient_id: str
    family_history_score: float
    baseline_ige_iu_ml: float
    known_sensitizations: Dict[str, float]  # Allergen ID -> specific IgE
    eos_count: float

@dataclass
class ReactionRisk:
    probability: float
    severity_index: float
    biphasic_risk: float
    contributing_factors: List[str]

@dataclass
class ImmunotherapyPhase:
    phase_name: str
    target_dose_mcg: float
    interval_days: int
    duration_weeks: int

@dataclass
class DesensitizationProtocol:
    allergen_id: str
    phases: List[ImmunotherapyPhase]
    expected_igg4_ratio_shift: float
    success_probability: float

class AllergyStateStore(Protocol):
    async def fetch_cross_reactivity_matrix(self) -> Dict[Tuple[str, str], float]: ...
    async def update_patient_state(self, patient_id: str, state: Dict[str, Any]) -> None: ...

class ImmuneSystemSimulator:
    """Simulates Th1/Th2 shifts and mast cell degranulation dynamics."""
    
    def __init__(self, base_reactivity: float):
        self.base_reactivity = base_reactivity
        self._degranulation_threshold = 100.0

    def compute_degranulation(self, ige_level: float, exposure_dose: float) -> float:
        """Calculate mast cell degranulation percentage based on receptor occupancy."""
        occupancy = (ige_level * exposure_dose) / (ige_level + exposure_dose + 1.0)
        return min(100.0, (occupancy / self._degranulation_threshold) * 100.0)
        
    def simulate_immunotherapy_shift(self, current_ige: float, doses: List[float]) -> Tuple[float, float]:
        """Simulate the shift in IgE and IgG4 levels over a series of doses."""
        ige_decay_factor = 0.98
        igg4_growth_factor = 1.05
        
        simulated_ige = current_ige
        simulated_igg4 = 1.0
        
        for dose in doses:
            simulated_ige *= ige_decay_factor
            simulated_igg4 += dose * igg4_growth_factor * 0.01
            
        return simulated_ige, simulated_igg4

class H11AllergologiaAgent:
    def __init__(self, state_store: AllergyStateStore):
        self.state_store = state_store
        self.simulator = ImmuneSystemSimulator(base_reactivity=1.2)
        self._active_alerts: Set[str] = set()

    async def initialize(self) -> None:
        """Initialize the agent and load cross-reactivity matrices."""
        logger.info("Initializing H11-ALLERGOLOGIA agent")
        self.cross_matrix = await self.state_store.fetch_cross_reactivity_matrix()
        logger.info(f"Loaded {len(self.cross_matrix)} cross-reactivity edges.")

    async def evaluate_anaphylaxis_risk(
        self, profile: AtopyProfile, recent_exposures: List[AllergenExposure]
    ) -> ReactionRisk:
        """
        Evaluate the real-time risk of severe hypersensitivity.
        Uses recent exposure data and baseline specific IgE levels.
        """
        max_degranulation = 0.0
        factors = []
        
        for exp in recent_exposures:
            s_ige = profile.known_sensitizations.get(exp.allergen_id, 0.0)
            
            # Check for cross-reactivities if specific IgE is missing
            if s_ige == 0.0:
                for known_alg, k_ige in profile.known_sensitizations.items():
                    cr_score = self.cross_matrix.get((known_alg, exp.allergen_id), 0.0)
                    if cr_score > 0.5:
                        s_ige = max(s_ige, k_ige * cr_score)
                        factors.append(f"Cross-reaction: {known_alg} -> {exp.allergen_id}")
            
            if s_ige > 0:
                deg = self.simulator.compute_degranulation(s_ige, exp.dose_micrograms)
                if deg > max_degranulation:
                    max_degranulation = deg
                factors.append(f"Direct exposure to {exp.allergen_id}")
                
        prob = min(1.0, max_degranulation / 100.0)
        sev_index = prob * (profile.baseline_ige_iu_ml / 100.0)
        biphasic = 0.2 if sev_index > 0.8 else 0.05
        
        return ReactionRisk(
            probability=prob,
            severity_index=sev_index,
            biphasic_risk=biphasic,
            contributing_factors=factors
        )

    async def generate_immunotherapy_protocol(
        self, profile: AtopyProfile, target_allergen: str
    ) -> DesensitizationProtocol:
        """
        Generate a customized desensitization plan.
        """
        baseline_ige = profile.known_sensitizations.get(target_allergen, 0.0)
        if baseline_ige < 0.35:
            # Below standard sensitization threshold
            return DesensitizationProtocol(
                allergen_id=target_allergen,
                phases=[],
                expected_igg4_ratio_shift=0.0,
                success_probability=0.0
            )
            
        build_up = ImmunotherapyPhase("Build-Up", target_dose_mcg=10.0, interval_days=7, duration_weeks=16)
        maintenance = ImmunotherapyPhase("Maintenance", target_dose_mcg=100.0, interval_days=28, duration_weeks=156)
        
        doses = [0.1 * (1.5**i) for i in range(16)] + [100.0] * 36
        end_ige, end_igg4 = self.simulator.simulate_immunotherapy_shift(baseline_ige, doses)
        
        ratio_shift = end_igg4 / (end_ige + 1e-5)
        success_prob = 0.85 if ratio_shift > 10.0 else 0.45
        
        return DesensitizationProtocol(
            allergen_id=target_allergen,
            phases=[build_up, maintenance],
            expected_igg4_ratio_shift=ratio_shift,
            success_probability=success_prob
        )

    async def monitor_patient_status(self, profile: AtopyProfile) -> Dict[str, Any]:
        """Background task entry point for continuous monitoring."""
        status = {
            "is_stable": True,
            "recommended_actions": []
        }
        
        if profile.eos_count > 500:
            status["is_stable"] = False
            status["recommended_actions"].append("Evaluate for eosinophilic complications")
            
        return status

    def clear_alerts(self) -> None:
        self._active_alerts.clear()
