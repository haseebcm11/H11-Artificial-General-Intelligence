import json
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any, Protocol
import math

class ConservationStatus(Enum):
    LEAST_CONCERN = "LC"
    NEAR_THREATENED = "NT"
    VULNERABLE = "VU"
    ENDANGERED = "EN"
    CRITICALLY_ENDANGERED = "CR"
    EXTINCT = "EX"

class DietType(Enum):
    CARNIVORE = "Carnivore"
    HERBIVORE = "Herbivore"
    OMNIVORE = "Omnivore"
    INSECTIVORE = "Insectivore"

@dataclass
class MammalTrait:
    body_mass_kg: float
    gestation_period_days: int
    litter_size: float
    metabolic_rate_w: float

@dataclass
class MammalSpecies:
    scientific_name: str
    common_name: str
    family: str
    order: str
    diet: DietType
    traits: MammalTrait
    status: ConservationStatus
    habitat_range_km2: float
    population_estimate: Optional[int] = None

@dataclass
class PopulationSimulationInput:
    species: MammalSpecies
    years: int
    carrying_capacity: int
    growth_rate: float
    environmental_stress: float

@dataclass
class PopulationSimulationOutput:
    final_population: int
    yearly_trajectory: List[int]
    extinction_probability: float
    warnings: List[str] = field(default_factory=list)

class MammalogiaProtocol(Protocol):
    def initialize(self, config: Dict[str, Any]) -> None: ...
    def process(self, input_data: Any) -> Any: ...
    def calculate_basal_metabolic_rate(self, species: MammalSpecies) -> float: ...
    def simulate_population(self, params: PopulationSimulationInput) -> PopulationSimulationOutput: ...

class MammalogiaAgent:
    def __init__(self):
        self.taxonomic_db: Dict[str, MammalSpecies] = {}
        self.simulations_run: int = 0
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        self.config = config
        # Pre-load some foundational taxa
        tiger = MammalSpecies(
            scientific_name="Panthera tigris",
            common_name="Tiger",
            family="Felidae",
            order="Carnivora",
            diet=DietType.CARNIVORE,
            traits=MammalTrait(body_mass_kg=200.0, gestation_period_days=103, litter_size=3.0, metabolic_rate_w=0.0),
            status=ConservationStatus.ENDANGERED,
            habitat_range_km2=1000000.0,
            population_estimate=3900
        )
        tiger.traits.metabolic_rate_w = self.calculate_basal_metabolic_rate(tiger)
        self.register_species(tiger)

    def register_species(self, species: MammalSpecies) -> None:
        self.taxonomic_db[species.scientific_name] = species

    def calculate_basal_metabolic_rate(self, species: MammalSpecies) -> float:
        # Kleiber's law: BMR = 73.3 * M^0.74 (in kcal/day), we convert to Watts roughly
        # 1 kcal/day = 0.0484 Watts
        mass = species.traits.body_mass_kg
        bmr_kcal = 73.3 * (mass ** 0.74)
        return bmr_kcal * 0.0484

    def assess_extinction_risk(self, species: MammalSpecies) -> float:
        risk = 0.0
        if species.population_estimate and species.population_estimate < 1000:
            risk += 0.5
        if species.status in [ConservationStatus.ENDANGERED, ConservationStatus.CRITICALLY_ENDANGERED]:
            risk += 0.3
        if species.habitat_range_km2 < 10000:
            risk += 0.2
        return min(risk, 1.0)

    def simulate_population(self, params: PopulationSimulationInput) -> PopulationSimulationOutput:
        trajectory = []
        current_pop = params.species.population_estimate or 100
        K = params.carrying_capacity
        r = params.growth_rate
        stress = params.environmental_stress
        
        trajectory.append(int(current_pop))
        warnings = []
        
        for year in range(params.years):
            # Logistic growth with environmental stochasticity (stress)
            stochastic_factor = 1.0 - (stress * (hash(str(year)) % 100) / 100.0)
            dn = r * current_pop * (1 - current_pop / K) * stochastic_factor
            current_pop += dn
            
            if current_pop < 2:
                current_pop = 0
                warnings.append(f"Extinction event occurred at year {year}.")
                break
                
            trajectory.append(int(current_pop))
            
        extinction_prob = 1.0 if current_pop == 0 else (1.0 / current_pop if current_pop < 100 else 0.0)
        self.simulations_run += 1
        
        return PopulationSimulationOutput(
            final_population=int(current_pop),
            yearly_trajectory=trajectory,
            extinction_probability=extinction_prob,
            warnings=warnings
        )

    def get_species_by_diet(self, diet: DietType) -> List[MammalSpecies]:
        return [sp for sp in self.taxonomic_db.values() if sp.diet == diet]

    def allometric_scaling_analysis(self, species_list: List[MammalSpecies]) -> Dict[str, float]:
        if not species_list:
            return {}
        avg_mass = sum(sp.traits.body_mass_kg for sp in species_list) / len(species_list)
        avg_bmr = sum(sp.traits.metabolic_rate_w for sp in species_list) / len(species_list)
        return {"average_mass_kg": avg_mass, "average_bmr_w": avg_bmr}

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action")
        if action == "simulate":
            sp_name = input_data.get("species")
            sp = self.taxonomic_db.get(sp_name)
            if not sp:
                return {"error": "Species not found"}
            
            params = PopulationSimulationInput(
                species=sp,
                years=input_data.get("years", 50),
                carrying_capacity=input_data.get("carrying_capacity", 10000),
                growth_rate=input_data.get("growth_rate", 0.05),
                environmental_stress=input_data.get("stress", 0.1)
            )
            result = self.simulate_population(params)
            return {
                "final_population": result.final_population,
                "extinction_prob": result.extinction_probability,
                "trajectory": result.yearly_trajectory
            }
        
        return {"error": "Unknown action"}
