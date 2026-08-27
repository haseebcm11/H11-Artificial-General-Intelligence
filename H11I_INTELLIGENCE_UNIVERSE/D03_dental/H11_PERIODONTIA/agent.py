import math
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

AGENT_ID = "H11_PERIODONTIA"

class HPeriodontiaException(Exception):
    """Domain-specific exception for H11_PERIODONTIA."""
    pass

@dataclass
class HPeriodontiaInput:
    decayed_teeth: int
    missing_teeth: int
    filled_teeth: int
    sna_angle_deg: float
    snb_angle_deg: float
    implant_radius_mm: float
    insertion_force_n: float
    friction_coefficient: float
    thread_pitch_mm: float

@dataclass
class HPeriodontiaOutput:
    dmft_index: int
    anb_angle_deg: float
    skeletal_class: str
    insertion_torque_ncm: float
    implant_stability_quotient: float
    dental_summary: str

class HPeriodontiaAgent:
    """
    H11_PERIODONTIA Deep Domain Enhancement.
    
    Computes rigorous dental/orthodontic metrics:
    - DMFT Index (Decayed, Missing, Filled Teeth)
    - Cephalometric Analysis (ANB = SNA - SNB, Skeletal Class I/II/III)
    - Implant Insertion Torque = F * (pitch / (2*pi) + mu * r)
    - ISQ (Implant Stability Quotient) estimation based on torque
    """
    
    def __init__(self):
        self.agent_id = AGENT_ID

    def _compute_dmft(self, d: int, m: int, f: int) -> int:
        if any(x < 0 for x in (d, m, f)):
            raise HPeriodontiaException("Tooth counts cannot be negative.")
        if d + m + f > 32:
            raise HPeriodontiaException("DMFT index cannot exceed 32.")
        return d + m + f

    def _compute_cephalometric(self, sna: float, snb: float) -> tuple[float, str]:
        anb = sna - snb
        if anb > 4:
            sk_class = "Class II (Mandibular retrognathia)"
        elif anb < 0:
            sk_class = "Class III (Mandibular prognathia)"
        else:
            sk_class = "Class I (Normal)"
        return anb, sk_class

    def _compute_implant_torque(self, f: float, r: float, mu: float, pitch: float) -> float:
        # Torque = F * (pitch / (2*pi) + mu * r) -> converted to N-cm (assuming input r in mm -> cm)
        torque_nmm = f * (pitch / (2.0 * math.pi) + mu * r)
        return torque_nmm / 10.0

    def _estimate_isq(self, torque_ncm: float) -> float:
        # Logistic curve mapping torque (0-50 Ncm) to ISQ (40-80)
        base = 40.0
        max_add = 40.0
        k = 0.15
        midpoint = 25.0
        return base + max_add / (1.0 + math.exp(-k * (torque_ncm - midpoint)))

    def process(self, request: HPeriodontiaInput) -> HPeriodontiaOutput:
        try:
            dmft = self._compute_dmft(request.decayed_teeth, request.missing_teeth, request.filled_teeth)
            anb, sk_class = self._compute_cephalometric(request.sna_angle_deg, request.snb_angle_deg)
            torque = self._compute_implant_torque(
                request.insertion_force_n, request.implant_radius_mm,
                request.friction_coefficient, request.thread_pitch_mm
            )
            isq = self._estimate_isq(torque)
            
            return HPeriodontiaOutput(
                dmft_index=dmft,
                anb_angle_deg=round(anb, 2),
                skeletal_class=sk_class,
                insertion_torque_ncm=round(torque, 2),
                implant_stability_quotient=round(isq, 1),
                dental_summary=f"DMFT: {dmft}, ANB: {anb:.1f}, Torque: {torque:.1f} Ncm"
            )
        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            raise HPeriodontiaException(f"Error in mathematical modeling: {str(e)}")
