"""
H11-IMMUNOTHERAPIA: Immunotherapy & Biologics
Layer 1 - Medicine & Health Sciences

Models immune system dynamics and designs personalized biologic treatments,
including CAR-T and checkpoint inhibitors. Simulates the tumor microenvironment (TME)
using predator-prey ODEs to predict treatment efficacy and toxicity (e.g. CRS).
"""

from __future__ import annotations
import asyncio
import logging
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)

class TherapyType(Enum):
    CAR_T = auto()
    TCR_THERAPY = auto()
    CHECKPOINT_INHIBITOR = auto()
    MONOCLONAL_ANTIBODY = auto()
    BISPECIFIC_T_CELL_ENGAGER = auto()

@dataclass
class TumorProfile:
    tumor_type: str
    mutational_burden: float
    pd_l1_expression: float
    neoantigens: List[str]
    growth_rate: float

@dataclass
class ImmuneCell:
    cell_type: str
    activation_state: float
    spatial_x: float
    spatial_y: float

@dataclass
class SpatialGraph:
    cells: List[ImmuneCell]
    adjacency_matrix: np.ndarray

@dataclass
class BiologicDesign:
    therapy_type: TherapyType
    target_antigen: str
    affinity_kd: float
    dosage_cells_or_mg: float
    dosing_schedule: str

class ImmuneDynamicsSimulator:
    """Simulates T-cell vs Tumor Cell dynamics using ODEs."""
    
    def __init__(self, t_cell_proliferation_rate: float, tumor_growth_rate: float, exhaustion_rate: float):
        self.r_t = t_cell_proliferation_rate
        self.r_c = tumor_growth_rate
        self.d_e = exhaustion_rate

    def simulate(self, initial_tumor: float, initial_t_cells: float, days: int) -> Tuple[np.ndarray, np.ndarray]:
        """Simple Euler integration for predator-prey TME model."""
        dt = 0.1
        steps = int(days / dt)
        
        T = np.zeros(steps)
        C = np.zeros(steps)
        
        T[0] = initial_t_cells
        C[0] = initial_tumor
        
        for i in range(1, steps):
            # Tumor growth - killing by T cells
            dC = self.r_c * C[i-1] - (0.5 * T[i-1] * C[i-1]) / (1 + C[i-1])
            # T cell expansion stimulated by tumor - exhaustion
            dT = self.r_t * T[i-1] * C[i-1] - self.d_e * T[i-1]
            
            C[i] = max(0, C[i-1] + dC * dt)
            T[i] = max(0, T[i-1] + dT * dt)
            
        return C, T

class ImmunotherapyAgent:
    """Agent for immunotherapy design and evaluation."""
    
    def __init__(self):
        self.simulator = ImmuneDynamicsSimulator(
            t_cell_proliferation_rate=0.15,
            tumor_growth_rate=0.08,
            exhaustion_rate=0.05
        )

    async def design_therapy(self, profile: TumorProfile, tme: SpatialGraph) -> BiologicDesign:
        logger.info(f"Designing therapy for {profile.tumor_type}")
        
        # Simple heuristic for therapy choice
        if profile.pd_l1_expression > 0.5:
            therapy_type = TherapyType.CHECKPOINT_INHIBITOR
            target = "PD-1/PD-L1"
            dose = 200.0 # mg
            schedule = "Q3W"
        elif profile.mutational_burden > 10 and profile.neoantigens:
            therapy_type = TherapyType.CAR_T
            target = profile.neoantigens[0]
            dose = 1e6 # cells/kg
            schedule = "Single Infusion"
        else:
            therapy_type = TherapyType.MONOCLONAL_ANTIBODY
            target = "VEGF"
            dose = 400.0
            schedule = "Q2W"
            
        return BiologicDesign(
            therapy_type=therapy_type,
            target_antigen=target,
            affinity_kd=1e-9,
            dosage_cells_or_mg=dose,
            dosing_schedule=schedule
        )

    async def predict_crs_risk(self, therapy: BiologicDesign, profile: TumorProfile) -> float:
        """Estimate Cytokine Release Syndrome risk based on tumor burden and therapy."""
        base_risk = 0.1
        if therapy.therapy_type in [TherapyType.CAR_T, TherapyType.BISPECIFIC_T_CELL_ENGAGER]:
            base_risk += 0.4
            
        # Higher tumor burden = higher risk of massive activation
        risk = base_risk * (1 + min(profile.growth_rate, 1.0))
        return min(0.99, max(0.01, risk))

    async def evaluate_case(self, profile: TumorProfile, tme: SpatialGraph) -> Dict[str, Any]:
        design = await self.design_therapy(profile, tme)
        crs_risk = await self.predict_crs_risk(design, profile)
        
        # Simulate 30 days
        tumor_traj, t_cell_traj = self.simulator.simulate(initial_tumor=100.0, initial_t_cells=10.0, days=30)
        
        return {
            "design": design,
            "crs_risk_index": crs_risk,
            "day_30_tumor_volume": tumor_traj[-1],
            "clearance_achieved": tumor_traj[-1] < 1.0
        }

async def run_example():
    agent = ImmunotherapyAgent()
    profile = TumorProfile("Melanoma", 15.5, 0.8, ["MAGE-A3"], 0.12)
    empty_graph = SpatialGraph([], np.zeros((0,0)))
    
    result = await agent.evaluate_case(profile, empty_graph)
    print(f"Therapy Evaluation: {result}")

if __name__ == "__main__":
    asyncio.run(run_example())
