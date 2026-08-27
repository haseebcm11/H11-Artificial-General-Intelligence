import json
import math
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("H11_CRYSTALLOGRAPHIA")

class CrystalSystem(Enum):
    CUBIC = "Cubic"
    TETRAGONAL = "Tetragonal"
    ORTHORHOMBIC = "Orthorhombic"
    HEXAGONAL = "Hexagonal"
    TRIGONAL = "Trigonal"
    MONOCLINIC = "Monoclinic"
    TRICLINIC = "Triclinic"

@dataclass
class Lattice:
    a: float # Angstroms
    b: float
    c: float
    alpha: float # Degrees
    beta: float
    gamma: float
    
    @property
    def volume(self) -> float:
        # v = abc * sqrt(1 - cos^2 a - cos^2 b - cos^2 g + 2 cos a cos b cos g)
        rad_a = math.radians(self.alpha)
        rad_b = math.radians(self.beta)
        rad_g = math.radians(self.gamma)
        
        ca, cb, cg = math.cos(rad_a), math.cos(rad_b), math.cos(rad_g)
        term = 1 - ca**2 - cb**2 - cg**2 + 2*ca*cb*cg
        if term <= 0: return 0.0
        return self.a * self.b * self.c * math.sqrt(term)
        
    def determine_system(self) -> CrystalSystem:
        tol = 1e-3
        a_eq_b = math.isclose(self.a, self.b, rel_tol=tol)
        b_eq_c = math.isclose(self.b, self.c, rel_tol=tol)
        
        al_90 = math.isclose(self.alpha, 90.0, rel_tol=tol)
        be_90 = math.isclose(self.beta, 90.0, rel_tol=tol)
        ga_90 = math.isclose(self.gamma, 90.0, rel_tol=tol)
        ga_120 = math.isclose(self.gamma, 120.0, rel_tol=tol)
        
        if a_eq_b and b_eq_c and al_90 and be_90 and ga_90:
            return CrystalSystem.CUBIC
        if a_eq_b and not b_eq_c and al_90 and be_90 and ga_90:
            return CrystalSystem.TETRAGONAL
        if not a_eq_b and not b_eq_c and al_90 and be_90 and ga_90:
            return CrystalSystem.ORTHORHOMBIC
        if a_eq_b and not b_eq_c and al_90 and be_90 and ga_120:
            return CrystalSystem.HEXAGONAL
        if not a_eq_b and not b_eq_c and al_90 and ga_90 and not be_90:
            return CrystalSystem.MONOCLINIC
            
        return CrystalSystem.TRICLINIC

class CrystallographiaAgent:
    """Agent for Solid State Chemistry and Crystallography."""
    
    def __init__(self, name: str = "H11-CRYSTALLOGRAPHIA"):
        self.name = name

    def analyze(self, request: Dict[str, Any]) -> Dict[str, Any]:
        comp = request.get("material_composition", "Unknown")
        lat_dict = request.get("lattice_parameters", {})
        atype = request.get("analysis_type", "symmetry")
        
        lattice = Lattice(
            a=lat_dict.get("a", 5.0),
            b=lat_dict.get("b", 5.0),
            c=lat_dict.get("c", 5.0),
            alpha=lat_dict.get("alpha", 90.0),
            beta=lat_dict.get("beta", 90.0),
            gamma=lat_dict.get("gamma", 90.0)
        )
        
        sys = lattice.determine_system()
        
        res = {
            "agent": self.name,
            "composition": comp,
            "crystal_system": sys.value,
            "lattice_volume_A3": round(lattice.volume, 4)
        }
        
        if atype == "symmetry":
            res["space_group"] = "Fm-3m" if sys == CrystalSystem.CUBIC else "P1" # Dummy
        elif atype == "xrd":
            res["xrd_peaks_2theta"] = [25.4, 31.2, 45.8, 52.1] # Dummy pattern
        elif atype == "electronic":
            res["band_gap_eV"] = 1.1 if "Si" in comp else 0.0 # Dummy logic
            res["is_metal"] = res["band_gap_eV"] == 0.0
        elif atype == "mechanical":
            res["bulk_modulus_GPa"] = 150.0
            res["shear_modulus_GPa"] = 80.0
            
        return res

if __name__ == "__main__":
    agent = CrystallographiaAgent()
    req = {
        "material_composition": "NaCl",
        "lattice_parameters": {
            "a": 5.64, "b": 5.64, "c": 5.64,
            "alpha": 90.0, "beta": 90.0, "gamma": 90.0
        },
        "analysis_type": "symmetry"
    }
    print(json.dumps(agent.analyze(req), indent=2))
