"""
H11-GYNAECOLOGIA: Gynecology & women's health
Layer 1 - Medicine & Health Sciences

Models the Hypothalamic-Pituitary-Ovarian (HPO) axis dynamics, endometrial 
proliferation, and common pathologies such as PCOS and Endometriosis.
"""

from __future__ import annotations
import math
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Protocol, Sequence, Tuple

logger = logging.getLogger(__name__)

class MenstrualPhase(Enum):
    MENSTRUAL = auto()
    EARLY_FOLLICULAR = auto()
    LATE_FOLLICULAR = auto()
    OVULATORY = auto()
    LUTEAL = auto()
    ANOVULATORY = auto()

@dataclass
class EndocrineProfile:
    fsh_iu_l: float
    lh_iu_l: float
    estradiol_pg_ml: float
    progesterone_ng_ml: float
    testosterone_ng_dl: float
    amanti_mullerian_ng_ml: float
    day_of_cycle: int

@dataclass
class CycleTracking:
    cycle_lengths_days: List[int]
    bleeding_duration_days: float
    pain_score_1_to_10: int
    spotting: bool

class HPOAxisSimulator:
    """Simulates the hormonal feedback loops of the menstrual cycle."""
    
    def estimate_phase(self, profile: EndocrineProfile) -> MenstrualPhase:
        """Heuristic classifier for cycle phase based on point-in-time hormones."""
        if profile.progesterone_ng_ml > 3.0:
            return MenstrualPhase.LUTEAL
            
        if profile.lh_iu_l > 25.0 and profile.estradiol_pg_ml > 200.0:
            return MenstrualPhase.OVULATORY
            
        if profile.estradiol_pg_ml > 100.0:
            return MenstrualPhase.LATE_FOLLICULAR
            
        if profile.day_of_cycle <= 5:
            return MenstrualPhase.MENSTRUAL
            
        return MenstrualPhase.EARLY_FOLLICULAR

    def calculate_ovulation_probability(self, profile: EndocrineProfile) -> float:
        """Estimate likelihood of ovulation within next 48 hours."""
        # E2 triggers LH surge. LH > 25 indicates imminent ovulation.
        if profile.lh_iu_l > 25.0:
            return 0.95
        
        # Approaching surge
        if profile.estradiol_pg_ml > 200.0:
            return 0.60 + min(0.3, profile.lh_iu_l / 100.0)
            
        return 0.05

class PathologyEvaluator:
    """Evaluates risk profiles for common gynecologic conditions."""
    
    def assess_pcos_risk(self, profile: EndocrineProfile, tracking: CycleTracking) -> float:
        """Rotterdam criteria inspired algorithmic risk."""
        risk_score = 0.0
        
        # Oligo/Anovulation
        avg_cycle = sum(tracking.cycle_lengths_days) / len(tracking.cycle_lengths_days) if tracking.cycle_lengths_days else 28
        if avg_cycle > 35:
            risk_score += 0.4
            
        # Clinical/Biochemical Hyperandrogenism
        if profile.testosterone_ng_dl > 50.0:
            risk_score += 0.4
            
        # PCO morphology (proxied by AMH here)
        if profile.amanti_mullerian_ng_ml > 4.5:
            risk_score += 0.3
            
        return min(1.0, risk_score)
        
    def assess_endometriosis_risk(self, tracking: CycleTracking) -> float:
        """Risk based on dysmenorrhea and bleeding patterns."""
        risk = 0.0
        if tracking.pain_score_1_to_10 >= 7:
            risk += 0.5
        if tracking.spotting:
            risk += 0.2
        if tracking.bleeding_duration_days > 7:
            risk += 0.2
            
        return min(1.0, risk)

class H11GynaecologiaAgent:
    def __init__(self):
        self.hpo = HPOAxisSimulator()
        self.pathology = PathologyEvaluator()

    async def analyze_endocrine_status(self, profile: EndocrineProfile) -> Dict[str, Any]:
        """Analyze current hormonal state."""
        logger.info(f"Analyzing hormone profile on cycle day {profile.day_of_cycle}")
        
        phase = self.hpo.estimate_phase(profile)
        ovulation_prob = self.hpo.calculate_ovulation_probability(profile)
        
        # LH/FSH ratio often elevated in PCOS
        lh_fsh_ratio = profile.lh_iu_l / (profile.fsh_iu_l + 1e-5)
        
        return {
            "current_phase": phase.name,
            "ovulation_probability": ovulation_prob,
            "lh_fsh_ratio": lh_fsh_ratio,
            "is_ratio_abnormal": lh_fsh_ratio > 2.0
        }

    async def evaluate_pathologies(self, profile: EndocrineProfile, tracking: CycleTracking) -> Dict[str, float]:
        """Generate a differential diagnosis risk vector."""
        pcos_risk = self.pathology.assess_pcos_risk(profile, tracking)
        endo_risk = self.pathology.assess_endometriosis_risk(tracking)
        
        return {
            "PCOS_Probability": pcos_risk,
            "Endometriosis_Probability": endo_risk,
            "Ovarian_Reserve_Score": min(1.0, profile.amanti_mullerian_ng_ml / 3.0)
        }

    async def predict_next_menses(self, tracking: CycleTracking, current_day: int) -> int:
        """Forecast the start of the next cycle."""
        if not tracking.cycle_lengths_days:
            return max(0, 28 - current_day)
            
        avg_cycle = sum(tracking.cycle_lengths_days[-3:]) / min(3, len(tracking.cycle_lengths_days))
        return max(0, int(avg_cycle) - current_day)
