import math
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

AGENT_ID = "H11-PHARMACOVIGILANTIA"

class HPharmacovigilantiaException(Exception):
    """Domain-specific exception for H11-PHARMACOVIGILANTIA."""
    pass

@dataclass
class HPharmacovigilantiaInput:
    substrate_conc: float
    v_max: float
    k_m: float
    clearance: float
    volume_dist: float
    dose_mg: float
    auc_oral: float
    auc_iv: float
    toxic_dose_td50: float
    effective_dose_ed50: float

@dataclass
class HPharmacovigilantiaOutput:
    michaelis_menten_velocity: float
    elimination_rate_constant: float
    half_life_hours: float
    bioavailability_percent: float
    therapeutic_index: float
    steady_state_conc: float
    pharmacological_summary: str

class HPharmacovigilantiaAgent:
    """
    H11-PHARMACOVIGILANTIA Deep Domain Enhancement.
    
    Computes rigorous pharmacological metrics:
    - Michaelis-Menten Kinetics: V = (Vmax * [S]) / (Km + [S])
    - First-order elimination: ke = Cl / Vd, t1/2 = 0.693 / ke
    - Bioavailability: F = (AUC_oral / AUC_iv) * 100
    - Therapeutic Index = TD50 / ED50
    """
    
    def __init__(self):
        self.agent_id = AGENT_ID

    def _compute_mm_velocity(self, s: float, vmax: float, km: float) -> float:
        if s < 0 or km < 0:
            raise HPharmacovigilantiaException("Concentration and Km must be non-negative.")
        return (vmax * s) / (km + s)

    def _compute_pk_parameters(self, cl: float, vd: float) -> tuple[float, float]:
        if vd <= 0:
            raise HPharmacovigilantiaException("Volume of distribution must be positive.")
        ke = cl / vd
        t_half = 0.693 / ke if ke > 0 else float("inf")
        return ke, t_half

    def _compute_bioavailability(self, auc_oral: float, auc_iv: float) -> float:
        if auc_iv <= 0:
            raise HPharmacovigilantiaException("AUC IV must be positive.")
        return (auc_oral / auc_iv) * 100.0

    def _compute_therapeutic_index(self, td50: float, ed50: float) -> float:
        if ed50 <= 0:
            raise HPharmacovigilantiaException("ED50 must be positive.")
        return td50 / ed50

    def _compute_steady_state(self, dose: float, cl: float, tau: float = 24.0) -> float:
        if cl <= 0:
            raise HPharmacovigilantiaException("Clearance must be positive.")
        return dose / (cl * tau)

    def process(self, request: HPharmacovigilantiaInput) -> HPharmacovigilantiaOutput:
        try:
            v_mm = self._compute_mm_velocity(request.substrate_conc, request.v_max, request.k_m)
            ke, t_half = self._compute_pk_parameters(request.clearance, request.volume_dist)
            bioavail = self._compute_bioavailability(request.auc_oral, request.auc_iv)
            ti = self._compute_therapeutic_index(request.toxic_dose_td50, request.effective_dose_ed50)
            css = self._compute_steady_state(request.dose_mg, request.clearance)
            
            return HPharmacovigilantiaOutput(
                michaelis_menten_velocity=round(v_mm, 4),
                elimination_rate_constant=round(ke, 4),
                half_life_hours=round(t_half, 2),
                bioavailability_percent=round(bioavail, 2),
                therapeutic_index=round(ti, 2),
                steady_state_conc=round(css, 2),
                pharmacological_summary=f"V: {v_mm:.2f}, t1/2: {t_half:.2f}h, TI: {ti:.2f}"
            )
        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            raise HPharmacovigilantiaException(f"Error in mathematical modeling: {str(e)}")
