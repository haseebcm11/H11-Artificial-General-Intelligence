"""
H11-OTOLARYNGOLOGIA: ENT medicine
Layer 1 - Medicine & Health Sciences

Models the auditory transduction pathway, vestibular endolymph dynamics, 
and upper airway aerodynamics. Critical for sensory balance and airway management.
"""

from __future__ import annotations
import math
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Protocol, Sequence, Tuple

logger = logging.getLogger(__name__)

class HearingLossType(Enum):
    NORMAL = auto()
    CONDUCTIVE = auto()
    SENSORINEURAL = auto()
    MIXED = auto()

@dataclass
class AudiogramData:
    frequencies_hz: List[int]
    air_conduction_db: List[float]
    bone_conduction_db: List[float]
    tympanogram_type: str  # A, B, C, Ad, As
    acoustic_reflexes_present: bool

@dataclass
class HearingAssessment:
    loss_type: HearingLossType
    pure_tone_average: float
    air_bone_gap: float
    speech_discrimination_score: float

@dataclass
class VNGTracing:
    head_velocity: List[float]
    eye_velocity: List[float]
    time_series_ms: List[float]
    canal_plane: str

@dataclass
class AirwayMesh:
    min_cross_sectional_area_mm2: float
    pharyngeal_length_mm: float
    compliance_factor: float

class VestibularDynamicsSimulator:
    """Simulates the cupula mechanics in the semicircular canals."""
    
    def __init__(self):
        # Time constants for the torsion pendulum model
        self.T1 = 5.0   # Short time constant (viscous drag / cupular elasticity)
        self.T2 = 0.005 # Long time constant (moment of inertia / viscous drag)
        
    def calculate_vor_gain(self, vng: VNGTracing) -> float:
        """Calculate Vestibulo-Ocular Reflex gain from head and eye velocities."""
        if not vng.head_velocity or not vng.eye_velocity:
            return 0.0
            
        # Simplified peak-to-peak or RMS gain
        head_rms = math.sqrt(sum(v**2 for v in vng.head_velocity) / len(vng.head_velocity))
        eye_rms = math.sqrt(sum(v**2 for v in vng.eye_velocity) / len(vng.eye_velocity))
        
        if head_rms < 1.0:
            return 1.0 # Avoid division by zero for negligible movement
            
        return eye_rms / head_rms

class UpperAirwayCFD:
    """Reduced-order aerodynamic model of the upper airway."""
    
    def estimate_ahi(self, airway: AirwayMesh, bmi: float, age: float) -> float:
        """
        Estimate Apnea-Hypopnea Index using anatomical and demographic factors.
        Uses a modified Starling resistor model concept.
        """
        # Base collapsibility
        p_crit = -10.0 + (airway.min_cross_sectional_area_mm2 * 0.1) - (airway.compliance_factor * 5.0)
        
        # Demographic modifiers
        bmi_factor = max(0.0, (bmi - 25.0) * 0.5)
        age_factor = max(0.0, (age - 40.0) * 0.1)
        
        effective_p_crit = p_crit + bmi_factor + age_factor
        
        # Mapping P_crit to AHI (heuristic mapping)
        if effective_p_crit < -5.0:
            return 2.0  # Normal
        elif effective_p_crit < 0.0:
            return 10.0 + (effective_p_crit + 5.0) * 2.0  # Mild
        else:
            return 20.0 + (effective_p_crit) * 5.0  # Moderate to Severe

class H11OtolaryngologiaAgent:
    def __init__(self):
        self.vestibular_sim = VestibularDynamicsSimulator()
        self.airway_cfd = UpperAirwayCFD()

    async def analyze_hearing(self, data: AudiogramData) -> HearingAssessment:
        """Categorize hearing loss based on audiometric thresholds."""
        logger.info("Analyzing audiogram data")
        
        # Calculate Pure Tone Average (500, 1000, 2000 Hz)
        pta_indices = [i for i, f in enumerate(data.frequencies_hz) if f in (500, 1000, 2000)]
        if pta_indices:
            pta = sum(data.air_conduction_db[i] for i in pta_indices) / len(pta_indices)
        else:
            pta = sum(data.air_conduction_db) / len(data.air_conduction_db)
            
        # Calculate Air-Bone Gap
        ab_gaps = [ac - bc for ac, bc in zip(data.air_conduction_db, data.bone_conduction_db)]
        avg_ab_gap = sum(ab_gaps) / len(ab_gaps)
        
        # Categorize
        is_ac_loss = pta > 25.0
        is_gap_significant = avg_ab_gap >= 10.0
        
        loss_type = HearingLossType.NORMAL
        if is_ac_loss and not is_gap_significant:
            loss_type = HearingLossType.SENSORINEURAL
        elif is_ac_loss and is_gap_significant:
            # Check if bone conduction is normal
            bc_pta = sum(data.bone_conduction_db[i] for i in pta_indices) / len(pta_indices)
            if bc_pta > 25.0:
                loss_type = HearingLossType.MIXED
            else:
                loss_type = HearingLossType.CONDUCTIVE
                
        # Estimate Speech Discrim (heuristic based on loss type and degree)
        sds = 100.0
        if loss_type == HearingLossType.SENSORINEURAL:
            sds = max(0.0, 100.0 - (pta - 25) * 0.8)
            
        return HearingAssessment(
            loss_type=loss_type,
            pure_tone_average=pta,
            air_bone_gap=avg_ab_gap,
            speech_discrimination_score=sds
        )

    async def evaluate_vestibular_function(self, vng: VNGTracing) -> Dict[str, Any]:
        """Assess VOR and detect pathological nystagmus."""
        gain = self.vestibular_sim.calculate_vor_gain(vng)
        
        is_pathological = gain < 0.8 or gain > 1.2
        
        return {
            "vor_gain": gain,
            "canal": vng.canal_plane,
            "status": "Pathological" if is_pathological else "Normal",
            "recommended_rehab": is_pathological
        }

    async def predict_osa_risk(self, airway: AirwayMesh, bmi: float, age: float) -> Dict[str, float]:
        """Predict sleep apnea severity."""
        ahi = self.airway_cfd.estimate_ahi(airway, bmi, age)
        return {
            "predicted_ahi": ahi,
            "severity_index": min(1.0, ahi / 60.0)
        }
