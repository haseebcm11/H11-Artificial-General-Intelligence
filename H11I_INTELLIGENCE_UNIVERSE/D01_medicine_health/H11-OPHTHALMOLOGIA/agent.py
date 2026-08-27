"""
H11-OPHTHALMOLOGIA: Ophthalmology & vision
Layer 1 - Medicine & Health Sciences

Advanced computation module for the visual system, utilizing Zernike polynomial
ray-tracing for optical systems and structural-functional models for retinal 
neuropathies like glaucoma and AMD.
"""

from __future__ import annotations
import math
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Protocol, Sequence, Tuple

logger = logging.getLogger(__name__)

class PathologyFocus(Enum):
    GLAUCOMA = auto()
    MACULAR_DEGENERATION = auto()
    DIABETIC_RETINOPATHY = auto()
    CATARACT = auto()
    CORNEAL_ECTASIA = auto()

@dataclass
class ZernikeCoefficients:
    pupil_diameter_mm: float
    coefficients: Dict[int, float]  # OSA standard indices to microns
    
    def get_defocus(self) -> float:
        return self.coefficients.get(4, 0.0)
        
    def get_astigmatism(self) -> Tuple[float, float]:
        return (self.coefficients.get(3, 0.0), self.coefficients.get(5, 0.0))

@dataclass
class OCTDataCube:
    resolution_x: int
    resolution_y: int
    resolution_z: int
    voxel_size_um: Tuple[float, float, float]
    rnfl_thickness_map: List[List[float]]
    macular_volume_mm3: float
    fluid_pockets: int

@dataclass
class LensPrescription:
    sphere: float
    cylinder: float
    axis: int
    add_power: float
    visual_acuity_expected: str

@dataclass
class VisualField:
    mean_deviation: float
    pattern_standard_deviation: float
    test_reliability: float
    points_db: List[float]

class OcularBiomechanics(Protocol):
    def get_corneal_hysteresis(self) -> float: ...
    def update_iop(self, pressure_mmhg: float) -> None: ...

class OpticalRayTracer:
    """Simulates retinal image quality based on wavefront aberrations."""
    
    def __init__(self, ref_wavelength_nm: float = 555.0):
        self.wavelength = ref_wavelength_nm
        
    def calculate_strehl_ratio(self, zernike: ZernikeCoefficients) -> float:
        """Estimate Strehl ratio using Marechal approximation for small aberrations."""
        variance = sum(c**2 for idx, c in zernike.coefficients.items() if idx > 2)
        rms_error = math.sqrt(variance)
        if rms_error == 0:
            return 1.0
        # Phase variance
        phase_variance = (2 * math.pi * rms_error / (self.wavelength / 1000.0)) ** 2
        strehl = math.exp(-phase_variance)
        return max(0.0, min(1.0, strehl))

    def compute_sphero_cylindrical_refraction(self, zernike: ZernikeCoefficients) -> LensPrescription:
        """Convert Zernike defocus and astigmatism to clinical prescription."""
        r_pupil = zernike.pupil_diameter_mm / 2.0
        
        c20 = zernike.get_defocus()
        c22, c2_2 = zernike.get_astigmatism()
        
        # Dioptric conversion factor
        conversion = (-4.0 * math.sqrt(3)) / (r_pupil ** 2)
        
        sphere = conversion * c20
        cyl_c = conversion * math.sqrt(c22**2 + c2_2**2)
        
        if c22 == 0:
            axis = 90.0 if c2_2 > 0 else 0.0
        else:
            axis = (math.degrees(math.atan2(c2_2, c22)) / 2.0)
            
        if axis < 0:
            axis += 180.0
            
        return LensPrescription(
            sphere=round(sphere * 4) / 4.0,
            cylinder=round(cyl_c * 4) / 4.0,
            axis=int(round(axis)),
            add_power=0.0,
            visual_acuity_expected="20/20"
        )

class H11OphthalmologiaAgent:
    def __init__(self, biomechanics: OcularBiomechanics):
        self.biomechanics = biomechanics
        self.ray_tracer = OpticalRayTracer()
        self.history_length = 50

    async def evaluate_refractive_state(self, wavefront: ZernikeCoefficients) -> LensPrescription:
        """Process wavefront data to generate an optical prescription."""
        logger.info(f"Evaluating refractive state for pupil {wavefront.pupil_diameter_mm}mm")
        prescription = self.ray_tracer.compute_sphero_cylindrical_refraction(wavefront)
        
        strehl = self.ray_tracer.calculate_strehl_ratio(wavefront)
        if strehl < 0.2:
            prescription.visual_acuity_expected = "20/40 or worse"
        elif strehl < 0.8:
            prescription.visual_acuity_expected = "20/25"
            
        return prescription

    async def analyze_glaucoma_risk(self, oct_data: OCTDataCube, vf: VisualField, iop_history: List[float]) -> Dict[str, float]:
        """Combine structural (OCT) and functional (VF) metrics with biomechanics."""
        # 1. Structural integrity
        avg_rnfl = sum(sum(row) for row in oct_data.rnfl_thickness_map) / (len(oct_data.rnfl_thickness_map) * len(oct_data.rnfl_thickness_map[0]))
        structural_score = max(0.0, (avg_rnfl - 50.0) / 50.0)
        
        # 2. Functional integrity
        functional_score = max(0.0, (30.0 + vf.mean_deviation) / 30.0)
        
        # 3. Stress factors
        peak_iop = max(iop_history) if iop_history else 15.0
        hysteresis = self.biomechanics.get_corneal_hysteresis()
        
        biomechanical_vulnerability = (peak_iop / 21.0) * (10.0 / (hysteresis + 1e-5))
        
        progression_risk = (1.0 - structural_score) * 0.4 + (1.0 - functional_score) * 0.4 + (biomechanical_vulnerability - 1.0) * 0.2
        
        return {
            "progression_risk_index": max(0.0, min(1.0, progression_risk)),
            "structural_score": structural_score,
            "functional_score": functional_score,
            "estimated_rnfl_loss_rate_um_yr": progression_risk * 2.5
        }

    async def simulate_macular_degeneration(self, oct_data: OCTDataCube, years: int) -> float:
        """Predict the growth of geographic atrophy or neovascularization over time."""
        current_volume = oct_data.macular_volume_mm3
        fluid_factor = 1.0 + (oct_data.fluid_pockets * 0.05)
        
        # Basic exponential decay model for healthy tissue volume
        decay_rate = 0.02 * fluid_factor
        projected_volume = current_volume * math.exp(-decay_rate * years)
        
        return projected_volume
