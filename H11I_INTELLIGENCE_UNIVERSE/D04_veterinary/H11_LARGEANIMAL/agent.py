import math
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

AGENT_ID = "H11_LARGEANIMAL"

class HLargeanimalException(Exception):
    """Domain-specific exception for H11_LARGEANIMAL."""
    pass

@dataclass
class HLargeanimalInput:
    animal_mass_kg: float
    reference_mass_kg: float
    reference_dose_mg: float
    allometric_exponent: float
    rib_fat_thickness_mm: float
    basic_r0: float
    vaccine_efficacy: float
    metabolic_rate_constant: float

@dataclass
class HLargeanimalOutput:
    scaled_dose_mg: float
    body_condition_score: float
    herd_immunity_threshold: float
    critical_vaccination_coverage: float
    basal_metabolic_rate_kcal: float
    veterinary_summary: str

class HLargeanimalAgent:
    """
    H11_LARGEANIMAL Deep Domain Enhancement.
    
    Computes rigorous veterinary/animal science metrics:
    - Allometric Drug Scaling: Dose_animal = Dose_ref * (Mass_animal / Mass_ref)^b
    - Body Condition Scoring (BCS) mapped from rib fat thickness
    - Herd Immunity Threshold = 1 - 1/R0
    - Critical Vaccination Coverage = HIT / Vaccine_Efficacy
    - Kleiber's Law BMR = a * M^0.75
    """
    
    def __init__(self):
        self.agent_id = AGENT_ID

    def _allometric_scaling(self, m_animal: float, m_ref: float, dose_ref: float, exponent: float) -> float:
        if m_animal <= 0 or m_ref <= 0:
            raise HLargeanimalException("Mass must be positive.")
        return dose_ref * ((m_animal / m_ref) ** exponent)

    def _compute_bcs(self, fat_mm: float) -> float:
        # Linear map for standard 1-9 scale based on mm of fat (simplified model)
        bcs = 1.0 + (fat_mm / 3.0)
        return max(1.0, min(9.0, bcs))

    def _herd_immunity(self, r0: float, efficacy: float) -> tuple[float, float]:
        if r0 <= 1.0:
            return 0.0, 0.0
        hit = 1.0 - (1.0 / r0)
        vc = hit / efficacy if efficacy > 0 else float('inf')
        return hit, min(1.0, vc)

    def _compute_bmr(self, mass: float, constant: float = 70.0) -> float:
        # Kleiber's law BMR ~ 70 * M^0.75
        return constant * (mass ** 0.75)

    def process(self, request: HLargeanimalInput) -> HLargeanimalOutput:
        try:
            dose = self._allometric_scaling(
                request.animal_mass_kg, request.reference_mass_kg,
                request.reference_dose_mg, request.allometric_exponent
            )
            bcs = self._compute_bcs(request.rib_fat_thickness_mm)
            hit, vc = self._herd_immunity(request.basic_r0, request.vaccine_efficacy)
            bmr = self._compute_bmr(request.animal_mass_kg, request.metabolic_rate_constant)
            
            return HLargeanimalOutput(
                scaled_dose_mg=round(dose, 2),
                body_condition_score=round(bcs, 1),
                herd_immunity_threshold=round(hit, 4),
                critical_vaccination_coverage=round(vc, 4),
                basal_metabolic_rate_kcal=round(bmr, 2),
                veterinary_summary=f"Dose: {dose:.1f}mg, BCS: {bcs:.1f}, Vc: {vc*100:.1f}%"
            )
        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            raise HLargeanimalException(f"Error in mathematical modeling: {str(e)}")
