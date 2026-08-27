"""
H11-BACTERIOLOGIA: Bacteriology & Microbiome
Layer 1 - Medicine & Health Sciences

Simulates bacterial growth, virulence factor expression, and antibiotic resistance.
"""

from __future__ import annotations
import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional
import math
import random

logger = logging.getLogger(__name__)

class GramStain(Enum):
    POSITIVE = auto()
    NEGATIVE = auto()
    ATYPICAL = auto()

@dataclass
class ResistanceGene:
    name: str
    target_antibiotic_class: str
    mechanism: str # e.g., "efflux_pump", "beta_lactamase"

@dataclass
class BacteriumType:
    species_name: str
    gram: GramStain
    doubling_time_mins: float
    max_carrying_capacity: float
    toxins_produced: List[str]
    resistance_genes: List[ResistanceGene] = field(default_factory=list)

@dataclass
class Population:
    bacterium: BacteriumType
    cfu_count: float # Colony forming units
    biofilm_mass: float = 0.0
    in_quorum: bool = False

@dataclass
class MicroEnvironment:
    nutrients: float # 0.0 to 1.0
    oxygen: float # 0.0 to 1.0
    antibiotic_concentration: Dict[str, float] = field(default_factory=dict)

class BacteriologyEngine:
    def __init__(self):
        self.quorum_threshold = 1e6

    def compute_growth(self, pop: Population, env: MicroEnvironment, dt_mins: float) -> float:
        """Calculates population growth using logistic equation with antibiotic modifiers."""
        # Base growth rate based on doubling time
        r = math.log(2) / pop.bacterium.doubling_time_mins
        
        # Modifier based on nutrients
        r *= env.nutrients
        
        # Antibiotic kill rate
        kill_rate = 0.0
        for abx_class, conc in env.antibiotic_concentration.items():
            # Check for resistance
            is_resistant = any(g.target_antibiotic_class == abx_class for g in pop.bacterium.resistance_genes)
            if not is_resistant and conc > 0:
                kill_rate += conc * 0.1 # simplified kill rate parameter
                
        # Biofilm protection
        if pop.biofilm_mass > 0:
            kill_rate *= 0.1 # Biofilm significantly reduces antibiotic efficacy
            
        net_r = r - kill_rate
        
        # Logistic growth step: dN/dt = rN(1 - N/K)
        N = pop.cfu_count
        K = pop.bacterium.max_carrying_capacity
        
        if N <= 0:
            return 0
            
        dN = net_r * N * (1 - N / K) * dt_mins
        return dN

class BacteriologiaAgent:
    """Agent for bacterial and microbiome simulation."""
    def __init__(self):
        self.engine = BacteriologyEngine()
        self.populations: Dict[str, Population] = {}

    async def initialize(self) -> None:
        logger.info("Initializing H11-BACTERIOLOGIA...")
        # Seed normal gut flora
        ecoli = BacteriumType("Escherichia coli", GramStain.NEGATIVE, 20.0, 1e12, ["endotoxin"])
        self.populations["gut_ecoli"] = Population(ecoli, 1e9)

    async def add_pathogen(self, bacterium: BacteriumType, initial_cfu: float, location: str) -> None:
        pop_id = f"{location}_{bacterium.species_name.replace(' ', '_')}"
        self.populations[pop_id] = Population(bacterium, initial_cfu)
        logger.info(f"Pathogen added: {bacterium.species_name} at {location} with CFU {initial_cfu}")

    async def simulate_time(self, env: MicroEnvironment, mins: float, dt: float = 1.0) -> Dict[str, Any]:
        """Runs the bacterial growth simulation forward."""
        steps = int(mins / dt)
        toxin_load = {}
        
        for _ in range(steps):
            for pop_id, pop in self.populations.items():
                delta = self.engine.compute_growth(pop, env, dt)
                pop.cfu_count = max(0.0, pop.cfu_count + delta)
                
                # Quorum sensing check
                if pop.cfu_count > self.engine.quorum_threshold and not pop.in_quorum:
                    pop.in_quorum = True
                    logger.warning(f"{pop.bacterium.species_name} reached quorum sensing threshold!")
                    
                # Biofilm formation
                if pop.in_quorum:
                    pop.biofilm_mass += 0.01 * dt
                    
                # Toxin production
                for toxin in pop.bacterium.toxins_produced:
                    toxin_load[toxin] = toxin_load.get(toxin, 0) + (pop.cfu_count * 1e-9 * dt)

        return {
            "time_simulated_mins": mins,
            "populations": {pid: p.cfu_count for pid, p in self.populations.items()},
            "toxins_released": toxin_load
        }

async def main():
    agent = BacteriologiaAgent()
    await agent.initialize()
    
    staph = BacteriumType("Staphylococcus aureus", GramStain.POSITIVE, 30.0, 1e10, ["alpha_toxin"])
    await agent.add_pathogen(staph, 1e4, "wound")
    
    env = MicroEnvironment(nutrients=0.8, oxygen=0.9, antibiotic_concentration={"penicillin": 0.0})
    
    res = await agent.simulate_time(env, 120.0) # 2 hours
    print("Growth after 2 hours:", res)
    
    # Apply antibiotic
    env.antibiotic_concentration["penicillin"] = 5.0
    res2 = await agent.simulate_time(env, 120.0)
    print("Growth after 2h antibiotic treatment:", res2)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
