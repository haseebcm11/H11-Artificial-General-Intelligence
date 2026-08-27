import json
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any, Set
import math
import random

class ThreatLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

@dataclass
class HabitatPatch:
    patch_id: str
    area_km2: float
    quality: float  # 0.0 to 1.0
    cost_to_protect: float
    is_protected: bool
    species_present: List[str]

@dataclass
class Edge:
    patch_a: str
    patch_b: str
    distance_km: float
    resistance: float

@dataclass
class LandscapeNetwork:
    patches: Dict[str, HabitatPatch]
    corridors: List[Edge]

class ConservationBioProtocol:
    def initialize(self, config: Dict[str, Any]) -> None: ...
    def process(self, input_data: Any) -> Any: ...
    def simulate_metapopulation(self, landscape: LandscapeNetwork, species: str, steps: int) -> float: ...
    def optimize_reserve_design(self, landscape: LandscapeNetwork, budget: float) -> List[str]: ...

class ConservationBioAgent(ConservationBioProtocol):
    def __init__(self):
        self.landscapes: Dict[str, LandscapeNetwork] = {}
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        self.config = config
        
        # Setup a sample landscape
        p1 = HabitatPatch("P1", 100.0, 0.9, 50000.0, False, ["Tiger", "Leopard"])
        p2 = HabitatPatch("P2", 50.0, 0.6, 20000.0, False, ["Leopard"])
        p3 = HabitatPatch("P3", 200.0, 0.8, 120000.0, False, ["Tiger"])
        
        edges = [
            Edge("P1", "P2", 10.0, 1.5),
            Edge("P2", "P3", 25.0, 3.0)
        ]
        
        self.landscapes["default"] = LandscapeNetwork(
            patches={"P1": p1, "P2": p2, "P3": p3},
            corridors=edges
        )

    def calculate_patch_isolation(self, patch_id: str, landscape: LandscapeNetwork) -> float:
        isolation = 0.0
        for edge in landscape.corridors:
            if edge.patch_a == patch_id or edge.patch_b == patch_id:
                isolation += math.exp(-edge.distance_km * edge.resistance)
        return 1.0 / (isolation + 0.001)

    def simulate_metapopulation(self, landscape: LandscapeNetwork, species: str, steps: int = 10) -> float:
        """
        Levins-style metapopulation model tracking patch occupancy.
        dp/dt = c*p*(1-p) - e*p
        """
        # Initial occupancy
        occupancy = {pid: (species in p.species_present) for pid, p in landscape.patches.items()}
        
        base_colonization_rate = 0.2
        base_extinction_rate = 0.1
        
        for _ in range(steps):
            new_occupancy = occupancy.copy()
            for pid, p in landscape.patches.items():
                if occupancy[pid]:
                    # Extinction phase
                    ext_risk = base_extinction_rate / (p.area_km2 * p.quality)
                    if not p.is_protected:
                        ext_risk *= 1.5
                    if random.random() < ext_risk:
                        new_occupancy[pid] = False
                else:
                    # Colonization phase
                    # Chance to be colonized from connected occupied patches
                    col_pressure = 0.0
                    for edge in landscape.corridors:
                        neighbor = None
                        if edge.patch_a == pid: neighbor = edge.patch_b
                        elif edge.patch_b == pid: neighbor = edge.patch_a
                        
                        if neighbor and occupancy[neighbor]:
                            col_pressure += base_colonization_rate * math.exp(-edge.distance_km * edge.resistance)
                    
                    if random.random() < col_pressure:
                        new_occupancy[pid] = True
            
            occupancy = new_occupancy
            
        occupied_count = sum(1 for v in occupancy.values() if v)
        return occupied_count / len(landscape.patches) if landscape.patches else 0.0

    def optimize_reserve_design(self, landscape: LandscapeNetwork, budget: float) -> List[str]:
        """
        Greedy algorithm for spatial conservation prioritization (simplified Marxan).
        Maximizes species representation and area/quality per cost.
        """
        unprotected = [p for p in landscape.patches.values() if not p.is_protected]
        selected = []
        spent = 0.0
        
        # Keep picking the best cost-benefit patch until budget exhausted
        while unprotected and spent < budget:
            best_patch = None
            best_score = -1.0
            
            for p in unprotected:
                if spent + p.cost_to_protect > budget:
                    continue
                    
                # Benefit: Area * Quality + uniqueness of species
                benefit = (p.area_km2 * p.quality) + (len(p.species_present) * 100.0)
                score = benefit / p.cost_to_protect
                
                if score > best_score:
                    best_score = score
                    best_patch = p
                    
            if best_patch:
                selected.append(best_patch.patch_id)
                spent += best_patch.cost_to_protect
                unprotected.remove(best_patch)
            else:
                break
                
        return selected

    def triage_species(self, species_risks: Dict[str, float], costs: Dict[str, float], budget: float) -> List[str]:
        """
        Weitzman approach to conservation triage (simplified).
        """
        items = []
        for sp, risk in species_risks.items():
            c = costs.get(sp, 10000.0)
            # prioritize high risk, low cost
            score = risk / c
            items.append((score, sp, c))
            
        items.sort(reverse=True, key=lambda x: x[0])
        
        funded = []
        spent = 0.0
        for score, sp, c in items:
            if spent + c <= budget:
                funded.append(sp)
                spent += c
                
        return funded

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action")
        landscape = self.landscapes.get(input_data.get("landscape_id", "default"))
        
        if not landscape:
            return {"error": "Landscape not found"}
            
        if action == "optimize":
            budget = input_data.get("budget", 100000.0)
            selected = self.optimize_reserve_design(landscape, budget)
            return {"selected_patches": selected, "budget_used": sum(landscape.patches[p].cost_to_protect for p in selected)}
            
        elif action == "metapopulation":
            species = input_data.get("species", "Tiger")
            steps = input_data.get("steps", 20)
            occ_prob = self.simulate_metapopulation(landscape, species, steps)
            return {"species": species, "final_occupancy_fraction": occ_prob}

        return {"error": "Unknown action"}
