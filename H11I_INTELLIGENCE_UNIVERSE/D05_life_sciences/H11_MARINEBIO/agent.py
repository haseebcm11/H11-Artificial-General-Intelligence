import json
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any, Tuple
import math

class MarineZone(Enum):
    EPIPELAGIC = "Epipelagic"
    MESOPELAGIC = "Mesopelagic"
    BATHYPELAGIC = "Bathypelagic"
    ABYSSOPELAGIC = "Abyssopelagic"
    BENTHIC = "Benthic"

@dataclass
class OceanConditions:
    temperature_c: float
    salinity_psu: float
    dissolved_oxygen_mgl: float
    ph_level: float
    depth_m: float

@dataclass
class MarineSpecies:
    name: str
    trophic_level: float
    preferred_zone: MarineZone
    temperature_tolerance: Tuple[float, float]
    biomass_mt: float

@dataclass
class CoralReef:
    reef_id: str
    location_lat: float
    location_lon: float
    cover_percentage: float
    symbiont_density: float
    dhw_accumulated: float  # Degree Heating Weeks

class MarineBioProtocol:
    def initialize(self, config: Dict[str, Any]) -> None: ...
    def process(self, input_data: Any) -> Any: ...
    def calculate_bleaching_risk(self, reef: CoralReef, current_sst: float, max_monthly_mean: float) -> float: ...
    def simulate_trophic_transfer(self, producer: MarineSpecies, consumer: MarineSpecies, efficiency: float) -> float: ...

class MarineBioAgent(MarineBioProtocol):
    def __init__(self):
        self.species_db: Dict[str, MarineSpecies] = {}
        self.reefs: Dict[str, CoralReef] = {}
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        self.config = config
        
        phytoplankton = MarineSpecies(
            name="Diatoms",
            trophic_level=1.0,
            preferred_zone=MarineZone.EPIPELAGIC,
            temperature_tolerance=(5.0, 25.0),
            biomass_mt=1e9
        )
        self.species_db[phytoplankton.name] = phytoplankton
        
        reef1 = CoralReef(
            reef_id="GBR_001",
            location_lat=-18.28,
            location_lon=147.69,
            cover_percentage=65.0,
            symbiont_density=1e6,
            dhw_accumulated=0.0
        )
        self.reefs[reef1.reef_id] = reef1

    def assess_habitat_suitability(self, species: MarineSpecies, conditions: OceanConditions) -> float:
        score = 1.0
        
        # Temperature check
        t_min, t_max = species.temperature_tolerance
        if conditions.temperature_c < t_min or conditions.temperature_c > t_max:
            score -= 0.5
            
        # pH check (Ocean acidification effect)
        if conditions.ph_level < 7.8:
            score -= 0.3
            
        # Oxygen check
        if conditions.dissolved_oxygen_mgl < 2.0: # Hypoxia
            score -= 0.8
            
        return max(0.0, score)

    def calculate_bleaching_risk(self, reef: CoralReef, current_sst: float, max_monthly_mean: float) -> float:
        # HotSpot calculation
        hotspot = max(0.0, current_sst - max_monthly_mean)
        
        # If hotspot > threshold (usually 1C), accumulate DHW
        threshold = self.config.get("bleaching_threshold_c", 1.0)
        if hotspot >= threshold:
            reef.dhw_accumulated += hotspot / 7.0 # roughly adding weekly anomaly
            
        risk = 0.0
        if reef.dhw_accumulated >= 4.0:
            risk = 0.5 # Significant bleaching likely
        if reef.dhw_accumulated >= 8.0:
            risk = 0.9 # Severe bleaching and mortality likely
            
        return risk

    def simulate_trophic_transfer(self, producer: MarineSpecies, consumer: MarineSpecies, efficiency: float = 0.1) -> float:
        """
        Simulate biomass transfer up the food web.
        Usually ~10% ecological efficiency.
        """
        if consumer.trophic_level <= producer.trophic_level:
            return 0.0
            
        transferrable_biomass = producer.biomass_mt * 0.1 # Max 10% can be eaten without collapse
        biomass_gained = transferrable_biomass * efficiency
        
        producer.biomass_mt -= transferrable_biomass
        consumer.biomass_mt += biomass_gained
        
        return biomass_gained

    def calculate_carbon_export(self, phytoplankton_biomass: float, depth: float) -> float:
        """
        Biological pump model (Martin curve).
        Flux at depth z = Flux_100 * (z / 100)^-b
        """
        if depth <= 100:
            return phytoplankton_biomass * 0.1 # roughly 10% sinks
            
        flux_100 = phytoplankton_biomass * 0.1
        b = 0.858 # standard Martin curve parameter
        flux_z = flux_100 * math.pow((depth / 100.0), -b)
        return flux_z

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action")
        
        if action == "bleaching_risk":
            reef_id = input_data.get("reef_id")
            sst = input_data.get("current_sst", 28.0)
            mmm = input_data.get("max_monthly_mean", 27.0)
            
            reef = self.reefs.get(reef_id)
            if reef:
                risk = self.calculate_bleaching_risk(reef, sst, mmm)
                return {"reef_id": reef_id, "dhw": reef.dhw_accumulated, "bleaching_risk": risk}
            return {"error": "Reef not found"}
            
        elif action == "carbon_export":
            biomass = input_data.get("biomass_mt", 1000.0)
            depth = input_data.get("depth_m", 500.0)
            flux = self.calculate_carbon_export(biomass, depth)
            return {"depth_m": depth, "carbon_flux_mt": flux}

        return {"error": "Unknown action"}
