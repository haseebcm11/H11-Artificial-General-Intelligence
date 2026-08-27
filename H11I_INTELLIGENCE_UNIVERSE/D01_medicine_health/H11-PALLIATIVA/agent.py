import math
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

AGENT_ID = "H11-PALLIATIVA"

class HPalliativaException(Exception):
    """Domain-specific exception for H11-PALLIATIVA."""
    pass

@dataclass
class HPalliativaInput:
    weight_kg: float
    height_m: float
    age_years: int
    serum_creatinine_mg_dl: float
    is_female: bool
    gcs_motor: int
    gcs_verbal: int
    gcs_eye: int
    temperature_c: float
    mean_arterial_pressure: float
    heart_rate: int
    respiratory_rate: int
    oxygenation_pao2: float

@dataclass
class HPalliativaOutput:
    bmi: float
    bmi_category: str
    gfr_ml_min: float
    gcs_total: int
    apache_ii_score: int
    mortality_risk_percent: float
    clinical_summary: str

class HPalliativaAgent:
    """
    H11-PALLIATIVA Deep Domain Enhancement.
    
    Computes rigorous clinical metrics:
    - BMI (kg/m^2)
    - Cockcroft-Gault GFR = ((140 - age) * weight) / (72 * SCr) * (0.85 if female)
    - Glasgow Coma Scale (GCS) = Motor + Verbal + Eye
    - APACHE II Scoring System (simplified physiological variables)
    """
    
    def __init__(self):
        self.agent_id = AGENT_ID

    def _compute_bmi(self, weight: float, height: float) -> tuple[float, str]:
        if height <= 0:
            raise HPalliativaException("Height must be positive.")
        bmi = weight / (height ** 2)
        if bmi < 18.5: cat = "Underweight"
        elif bmi < 25: cat = "Normal"
        elif bmi < 30: cat = "Overweight"
        else: cat = "Obese"
        return bmi, cat

    def _compute_gfr(self, age: int, weight: float, scr: float, is_female: bool) -> float:
        if scr <= 0:
            raise HPalliativaException("Serum creatinine must be positive.")
        gfr = ((140 - age) * weight) / (72.0 * scr)
        if is_female:
            gfr *= 0.85
        return gfr

    def _compute_gcs(self, motor: int, verbal: int, eye: int) -> int:
        if not (1 <= motor <= 6 and 1 <= verbal <= 5 and 1 <= eye <= 4):
            raise HPalliativaException("GCS components out of range.")
        return motor + verbal + eye

    def _compute_apache_ii(self, temp: float, map_: float, hr: int, rr: int, pao2: float) -> int:
        score = 0
        # Temperature
        if temp >= 41 or temp <= 29.9: score += 4
        elif 39 <= temp <= 40.9 or 30 <= temp <= 31.9: score += 3
        elif 38.5 <= temp <= 38.9 or 32 <= temp <= 33.9: score += 1
        elif 34 <= temp <= 35.9: score += 2
        # MAP
        if map_ >= 160 or map_ <= 49: score += 4
        elif 130 <= map_ <= 159 or 50 <= map_ <= 69: score += 2
        elif 110 <= map_ <= 129: score += 1
        elif 70 <= map_ <= 109: score += 0
        # HR
        if hr >= 180 or hr <= 39: score += 4
        elif 140 <= hr <= 179 or 40 <= hr <= 54: score += 3
        elif 110 <= hr <= 139 or 55 <= hr <= 69: score += 2
        # RR
        if rr >= 50 or rr <= 5: score += 4
        elif 35 <= rr <= 49: score += 3
        elif 25 <= rr <= 34 or 10 <= rr <= 11: score += 1
        elif 6 <= rr <= 9: score += 2
        # Oxygenation
        if pao2 > 500: score += 4
        elif 350 < pao2 <= 500: score += 3
        elif 200 < pao2 <= 350: score += 2
        return score

    def process(self, request: HPalliativaInput) -> HPalliativaOutput:
        try:
            bmi, bmi_cat = self._compute_bmi(request.weight_kg, request.height_m)
            gfr = self._compute_gfr(request.age_years, request.weight_kg, request.serum_creatinine_mg_dl, request.is_female)
            gcs = self._compute_gcs(request.gcs_motor, request.gcs_verbal, request.gcs_eye)
            apache_score = self._compute_apache_ii(
                request.temperature_c, request.mean_arterial_pressure,
                request.heart_rate, request.respiratory_rate, request.oxygenation_pao2
            )
            
            mortality_risk = 1.0 / (1.0 + math.exp(-(-3.517 + (apache_score * 0.146))))
            
            return HPalliativaOutput(
                bmi=round(bmi, 2),
                bmi_category=bmi_cat,
                gfr_ml_min=round(gfr, 2),
                gcs_total=gcs,
                apache_ii_score=apache_score,
                mortality_risk_percent=round(mortality_risk * 100, 2),
                clinical_summary=f"GCS: {gcs}, GFR: {gfr:.1f}, APACHE II: {apache_score}"
            )
        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            raise HPalliativaException(f"Error in mathematical modeling: {str(e)}")
