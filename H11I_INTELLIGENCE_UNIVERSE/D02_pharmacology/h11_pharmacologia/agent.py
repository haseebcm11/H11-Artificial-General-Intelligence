import json
import math
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger("H11-PHARMACOLOGIA")
logger.setLevel(logging.INFO)

class ReceptorType(Enum):
    GPCR = "G-Protein Coupled Receptor"
    ION_CHANNEL = "Ligand-gated Ion Channel"
    KINASE = "Receptor Tyrosine Kinase"
    NUCLEAR = "Nuclear Receptor"

@dataclass
class Ligand:
    id: str
    kd: float
    emax: float
    hill_coefficient: float = 1.0
    is_agonist: bool = True
    antagonist_type: Optional[str] = None # competitive, non-competitive

@dataclass
class PKParameters:
    dose: float # mg
    volume_distribution: float # L
    clearance: float # L/h
    bioavailability: float = 1.0
    ka: float = 1.5 # absorption rate constant

@dataclass
class PDMetrics:
    ec50: float
    receptor_occupancy: float
    fractional_effect: float

class DoseResponseEngine:
    """Computes sigmoidal dose-response curves using the Hill equation."""
    def __init__(self, basal_effect: float = 0.0):
        self.basal_effect = basal_effect

    def compute_response(self, concentration: float, ligand: Ligand, competitor: Optional[Ligand] = None, comp_conc: float = 0.0) -> float:
        """Calculates effect at a given concentration."""
        if concentration < 0:
            return self.basal_effect

        if competitor and not competitor.is_agonist:
            # Shift Kd based on competitor (Schild equation logic)
            if competitor.antagonist_type == "competitive":
                apparent_kd = ligand.kd * (1 + (comp_conc / competitor.kd))
            else:
                apparent_kd = ligand.kd # Simplified for non-competitive, max effect drops instead
        else:
            apparent_kd = ligand.kd

        if competitor and not competitor.is_agonist and competitor.antagonist_type == "non-competitive":
            apparent_emax = ligand.emax / (1 + (comp_conc / competitor.kd))
        else:
            apparent_emax = ligand.emax
            
        effect = self.basal_effect + (apparent_emax * (concentration ** ligand.hill_coefficient)) / \
                 ((apparent_kd ** ligand.hill_coefficient) + (concentration ** ligand.hill_coefficient))
        return effect

    def compute_ec50(self, ligand: Ligand) -> float:
        # In a simple Hill model without constitutive activity, EC50 is approx Kd
        return ligand.kd

class CompartmentalSolver:
    """Simple 1-compartment PK solver for oral/IV administration."""
    
    @staticmethod
    def simulate_1cmt_oral(pk: PKParameters, time_points: List[float]) -> List[float]:
        """C(t) = (F * Dose * ka) / (Vd * (ka - kel)) * (exp(-kel * t) - exp(-ka * t))"""
        kel = pk.clearance / pk.volume_distribution
        concentrations = []
        for t in time_points:
            if pk.ka == kel: # avoid division by zero
                pk.ka += 0.001
            
            c = ((pk.bioavailability * pk.dose * pk.ka) / (pk.volume_distribution * (pk.ka - kel))) * \
                (math.exp(-kel * t) - math.exp(-pk.ka * t))
            concentrations.append(max(0.0, c))
        return concentrations

class PharmacologiaAgent:
    """
    H11-PHARMACOLOGIA Main Agent.
    Manages Pharmacokinetic and Pharmacodynamic simulations.
    """
    def __init__(self, agent_id: str = "H11-PHARMA-001"):
        self.agent_id = agent_id
        self.dose_engine = DoseResponseEngine()
        self.pk_solver = CompartmentalSolver()
        self.state: Dict[str, Any] = {"status": "initialized", "last_simulation": None}

    def process_ligand_data(self, payload: Dict[str, Any]) -> PDMetrics:
        """Processes ligand json payload to PD metrics."""
        ligand_data = payload.get("ligand", {})
        l = Ligand(
            id=ligand_data.get("id", "unknown"),
            kd=ligand_data.get("kd", 1e-6),
            emax=ligand_data.get("emax", 100),
            hill_coefficient=ligand_data.get("hill_coefficient", 1.0),
            is_agonist=ligand_data.get("is_agonist", True)
        )
        ec50 = self.dose_engine.compute_ec50(l)
        
        # Test conc for metric
        test_conc = ec50 * 2
        occupancy = (test_conc) / (test_conc + l.kd) # Simple binding
        effect = self.dose_engine.compute_response(test_conc, l)
        
        return PDMetrics(ec50=ec50, receptor_occupancy=occupancy, fractional_effect=effect)

    def run_pk_pd_simulation(self, payload: Dict[str, Any], time_hours: float = 24.0, resolution: int = 100) -> Dict[str, Any]:
        """Runs a combined PK/PD simulation over a specified time."""
        ligand_data = payload.get("ligand", {})
        l = Ligand(**ligand_data)
        
        pk_data = payload.get("pk_parameters", {})
        pk = PKParameters(**pk_data)
        
        time_points = [i * (time_hours / resolution) for i in range(resolution + 1)]
        concentrations = self.pk_solver.simulate_1cmt_oral(pk, time_points)
        
        effects = []
        for c in concentrations:
            # assume concentration in ng/ml -> convert to molarity if needed, here simplified directly
            effects.append(self.dose_engine.compute_response(c, l))
            
        cmax = max(concentrations)
        tmax = time_points[concentrations.index(cmax)]
        auc = sum(concentrations) * (time_hours / resolution)
        
        result = {
            "cmax": cmax,
            "tmax": tmax,
            "auc": auc,
            "time_course": time_points,
            "pk_profile": concentrations,
            "pd_profile": effects
        }
        self.state["last_simulation"] = result
        return result

    def execute_command(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Interface for external callers."""
        try:
            if action == "analyze_pd":
                metrics = self.process_ligand_data(payload)
                return {"status": "success", "data": metrics.__dict__}
            elif action == "simulate_pkpd":
                sim = self.run_pk_pd_simulation(payload)
                return {"status": "success", "data": sim}
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        except Exception as e:
            logger.error(f"Error during {action}: {str(e)}")
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    agent = PharmacologiaAgent()
    sample_payload = {
        "ligand": {"id": "DrugX", "kd": 0.5, "emax": 100, "hill_coefficient": 1.2, "is_agonist": True},
        "pk_parameters": {"dose": 500, "volume_distribution": 50, "clearance": 5, "bioavailability": 0.8}
    }
    print(agent.execute_command("simulate_pkpd", sample_payload))
