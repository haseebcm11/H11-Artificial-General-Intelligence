from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Set, Optional
import math

class ReactionType(Enum):
    MASS_ACTION = auto()
    MICHAELIS_MENTEN = auto()
    ALLOSTERIC = auto()

@dataclass
class Metabolite:
    id: str
    name: str
    molecular_weight: float
    initial_concentration: float = 0.0

@dataclass
class Enzyme:
    id: str
    name: str
    k_cat: float
    k_m: float
    concentration: float = 1.0

@dataclass
class Reaction:
    id: str
    type: ReactionType
    substrates: Dict[str, float]  # metabolite_id -> stoichiometry
    products: Dict[str, float]    # metabolite_id -> stoichiometry
    rate_constant: float
    enzyme_id: Optional[str] = None
    reversible: bool = False
    reverse_rate_constant: float = 0.0

@dataclass
class NetworkState:
    concentrations: Dict[str, float] = field(default_factory=dict)
    fluxes: Dict[str, float] = field(default_factory=dict)
    time: float = 0.0

class MolecularisAgent:
    """
    H11-MOLECULARIS: Biochemical reaction and metabolic pathway simulator.
    """
    def __init__(self):
        self.metabolites: Dict[str, Metabolite] = {}
        self.enzymes: Dict[str, Enzyme] = {}
        self.reactions: Dict[str, Reaction] = {}
        self.state = NetworkState()
        
    def add_metabolite(self, metabolite: Metabolite) -> None:
        self.metabolites[metabolite.id] = metabolite
        self.state.concentrations[metabolite.id] = metabolite.initial_concentration
        
    def add_enzyme(self, enzyme: Enzyme) -> None:
        self.enzymes[enzyme.id] = enzyme
        
    def add_reaction(self, reaction: Reaction) -> None:
        self.reactions[reaction.id] = reaction
        self.state.fluxes[reaction.id] = 0.0
        
    def calculate_rate(self, reaction: Reaction) -> float:
        """Calculate the instantaneous reaction rate based on current concentrations."""
        rate = 0.0
        
        if reaction.type == ReactionType.MASS_ACTION:
            # Forward rate
            fwd = reaction.rate_constant
            for sub_id, stoich in reaction.substrates.items():
                conc = self.state.concentrations.get(sub_id, 0.0)
                fwd *= (conc ** stoich)
                
            # Reverse rate
            rev = 0.0
            if reaction.reversible:
                rev = reaction.reverse_rate_constant
                for prod_id, stoich in reaction.products.items():
                    conc = self.state.concentrations.get(prod_id, 0.0)
                    rev *= (conc ** stoich)
                    
            rate = fwd - rev
            
        elif reaction.type == ReactionType.MICHAELIS_MENTEN:
            if not reaction.enzyme_id or reaction.enzyme_id not in self.enzymes:
                return 0.0
            
            enzyme = self.enzymes[reaction.enzyme_id]
            # Assuming single substrate for simplified MM
            sub_id = list(reaction.substrates.keys())[0]
            s = self.state.concentrations.get(sub_id, 0.0)
            
            v_max = enzyme.k_cat * enzyme.concentration
            rate = (v_max * s) / (enzyme.k_m + s)
            
        return rate

    def step(self, dt: float) -> None:
        """Integrate the network forward by dt using Euler method."""
        rates = {}
        for r_id, rxn in self.reactions.items():
            rates[r_id] = self.calculate_rate(rxn)
            
        # Update concentrations based on stoichiometries
        delta_c = {m_id: 0.0 for m_id in self.metabolites}
        
        for r_id, rxn in self.reactions.items():
            flux = rates[r_id]
            self.state.fluxes[r_id] = flux
            
            # Consume substrates
            for sub_id, stoich in rxn.substrates.items():
                delta_c[sub_id] -= stoich * flux
                
            # Produce products
            for prod_id, stoich in rxn.products.items():
                delta_c[prod_id] += stoich * flux
                
        # Apply deltas
        for m_id, delta in delta_c.items():
            new_conc = self.state.concentrations[m_id] + (delta * dt)
            # Prevent negative concentrations
            self.state.concentrations[m_id] = max(0.0, new_conc)
            
        self.state.time += dt
        
    def check_mass_balance(self) -> float:
        """Validate mass conservation across the network."""
        total_mass = 0.0
        for m_id, conc in self.state.concentrations.items():
            total_mass += conc * self.metabolites[m_id].molecular_weight
        return total_mass

    def get_steady_state_approximation(self, max_steps: int = 10000, tol: float = 1e-6) -> bool:
        """Run simulation until fluxes stabilize or max steps reached."""
        dt = 0.01
        for step in range(max_steps):
            old_concentrations = self.state.concentrations.copy()
            self.step(dt)
            
            max_diff = max(abs(self.state.concentrations[m] - old_concentrations[m]) 
                           for m in self.metabolites)
            
            if max_diff < tol:
                return True
        return False

    def report(self) -> Dict[str, float]:
        """Return a snapshot of current concentrations and major fluxes."""
        return {
            "time": self.state.time,
            "concentrations": self.state.concentrations.copy(),
            "fluxes": self.state.fluxes.copy(),
            "total_mass": self.check_mass_balance()
        }
