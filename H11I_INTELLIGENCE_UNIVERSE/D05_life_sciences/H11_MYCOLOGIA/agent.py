import json
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any, Tuple
import math
import random

class FungalRole(Enum):
    SAPROTROPHIC = "Saprotrophic"
    MYCORRHIZAL = "Mycorrhizal"
    PATHOGENIC = "Pathogenic"
    ENDOPHYTIC = "Endophytic"

@dataclass
class EnzymeProfile:
    cellulase: float
    ligninase: float
    protease: float
    chitinase: float

@dataclass
class FungalSpecies:
    name: str
    phylum: str
    role: FungalRole
    enzymes: EnzymeProfile
    growth_rate_mm_per_day: float
    optimal_temp_c: float
    optimal_ph: float

@dataclass
class SpatialNode:
    x: float
    y: float
    nutrient_concentration: float
    is_colonized: bool
    biomass: float

@dataclass
class MycelialNetwork:
    network_id: str
    species: FungalSpecies
    nodes: List[SpatialNode]
    edges: List[Tuple[int, int]]
    total_biomass: float

class MycologiaProtocol:
    def initialize(self, config: Dict[str, Any]) -> None: ...
    def process(self, input_data: Any) -> Any: ...
    def simulate_growth(self, network: MycelialNetwork, days: int) -> MycelialNetwork: ...
    def calculate_decay_rate(self, species: FungalSpecies, substrate_type: str) -> float: ...

class MycologiaAgent(MycologiaProtocol):
    def __init__(self):
        self.networks: Dict[str, MycelialNetwork] = {}
        self.species_db: Dict[str, FungalSpecies] = {}
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        self.config = config
        
        # Load sample species
        amanita = FungalSpecies(
            name="Amanita muscaria",
            phylum="Basidiomycota",
            role=FungalRole.MYCORRHIZAL,
            enzymes=EnzymeProfile(cellulase=0.2, ligninase=0.1, protease=0.8, chitinase=0.1),
            growth_rate_mm_per_day=2.5,
            optimal_temp_c=18.0,
            optimal_ph=5.5
        )
        self.species_db[amanita.name] = amanita

    def calculate_decay_rate(self, species: FungalSpecies, substrate_type: str) -> float:
        # Simple Michaelis-Menten inspired decay heuristic
        if substrate_type == "wood":
            return (species.enzymes.ligninase * 0.7) + (species.enzymes.cellulase * 0.3)
        elif substrate_type == "leaf_litter":
            return (species.enzymes.cellulase * 0.8) + (species.enzymes.protease * 0.2)
        elif substrate_type == "insect":
            return species.enzymes.chitinase * 0.9
        return 0.1

    def create_network(self, species_name: str, origin_x: float, origin_y: float) -> Optional[str]:
        sp = self.species_db.get(species_name)
        if not sp:
            return None
        
        nid = f"net_{len(self.networks) + 1}"
        origin_node = SpatialNode(x=origin_x, y=origin_y, nutrient_concentration=100.0, is_colonized=True, biomass=1.0)
        net = MycelialNetwork(
            network_id=nid,
            species=sp,
            nodes=[origin_node],
            edges=[],
            total_biomass=1.0
        )
        self.networks[nid] = net
        return nid

    def simulate_growth(self, network: MycelialNetwork, days: int) -> MycelialNetwork:
        # Spatially explicit growth model (simplified)
        growth_rate = network.species.growth_rate_mm_per_day
        
        for day in range(days):
            new_nodes = []
            new_edges = []
            current_nodes_len = len(network.nodes)
            
            for i, node in enumerate(network.nodes):
                if node.is_colonized and node.biomass > 0.5:
                    # Attempt to branch out
                    if random.random() < 0.3: # Branching probability
                        angle = random.uniform(0, 2 * math.pi)
                        dist = growth_rate
                        nx = node.x + math.cos(angle) * dist
                        ny = node.y + math.sin(angle) * dist
                        
                        # Cost of building new biomass
                        node.biomass -= 0.2
                        network.total_biomass += 0.8
                        
                        new_node = SpatialNode(x=nx, y=ny, nutrient_concentration=random.uniform(10, 50), is_colonized=True, biomass=1.0)
                        new_nodes.append(new_node)
                        new_edges.append((i, current_nodes_len + len(new_nodes) - 1))
            
            network.nodes.extend(new_nodes)
            network.edges.extend(new_edges)
            
        return network

    def calculate_symbiotic_exchange(self, network_id: str, plant_carbon_flux: float) -> float:
        net = self.networks.get(network_id)
        if not net or net.species.role != FungalRole.MYCORRHIZAL:
            return 0.0
        
        # Fungi provide Phosphorus/Nitrogen for Carbon
        phosphorus_provided = net.total_biomass * 0.05
        carbon_received = plant_carbon_flux * 0.2
        net.total_biomass += carbon_received * 0.1
        return phosphorus_provided

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action")
        if action == "grow_network":
            nid = input_data.get("network_id")
            days = input_data.get("days", 10)
            net = self.networks.get(nid)
            if net:
                self.simulate_growth(net, days)
                return {"network_id": nid, "nodes_count": len(net.nodes), "biomass": net.total_biomass}
            return {"error": "Network not found"}
            
        elif action == "evaluate_decay":
            sp_name = input_data.get("species")
            substrate = input_data.get("substrate")
            sp = self.species_db.get(sp_name)
            if sp:
                rate = self.calculate_decay_rate(sp, substrate)
                return {"species": sp_name, "substrate": substrate, "decay_rate": rate}
            return {"error": "Species not found"}

        return {"error": "Unknown action"}
