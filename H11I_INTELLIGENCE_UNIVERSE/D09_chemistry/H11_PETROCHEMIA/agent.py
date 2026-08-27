import json
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum, auto

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("H11_PETROCHEMIA")

class RefineryProcess(Enum):
    DISTILLATION = "distillation"
    FCC = "fcc" # Fluid Catalytic Cracking
    REFORMING = "reforming"
    HYDROCRACKING = "hydrocracking"

@dataclass
class Feedstock:
    name: str
    api_gravity: float
    sulfur_wt_pct: float
    nitrogen_ppm: float = 0.0
    
    @property
    def specific_gravity(self) -> float:
        return 141.5 / (self.api_gravity + 131.5)

@dataclass
class ProductYields:
    fuel_gas: float # wt%
    lpg: float
    gasoline: float
    diesel: float
    heavy_oil: float
    coke: float

class ProcessSimulator:
    def __init__(self, process: RefineryProcess):
        self.process = process

    def simulate(self, feed: Feedstock, temp: float, press: float) -> ProductYields:
        # Dummy correlations based on process type and feed API
        base_conversion = min(0.95, (temp / 500.0) * (press / 10.0)**0.1)
        
        if self.process == RefineryProcess.FCC:
            conversion = base_conversion * (feed.api_gravity / 30.0) # higher api, easier to crack
            return ProductYields(
                fuel_gas=5.0,
                lpg=15.0 * conversion,
                gasoline=50.0 * conversion,
                diesel=20.0 * (1-conversion),
                heavy_oil=5.0 * (1-conversion),
                coke=5.0
            )
        elif self.process == RefineryProcess.REFORMING:
            return ProductYields(
                fuel_gas=10.0,
                lpg=5.0,
                gasoline=85.0, # High octane reformate
                diesel=0.0,
                heavy_oil=0.0,
                coke=0.0
            )
        else: # Generic Distillation
            return ProductYields(
                fuel_gas=2.0,
                lpg=3.0,
                gasoline=25.0,
                diesel=30.0,
                heavy_oil=40.0,
                coke=0.0
            )

class PetrochemiaAgent:
    """Agent for Petrochemical and Refinery process simulation."""
    
    def __init__(self, name: str = "H11-PETROCHEMIA"):
        self.name = name

    def evaluate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        p_type_str = request.get("process_type", "fcc")
        feed_dict = request.get("feedstock", {})
        temp = request.get("operating_temp_C", 520.0)
        press = request.get("operating_press_bar", 2.0)
        
        feed = Feedstock(
            name=feed_dict.get("name", "Generic VGO"),
            api_gravity=feed_dict.get("api_gravity", 25.0),
            sulfur_wt_pct=feed_dict.get("sulfur_wt_pct", 1.5)
        )
        
        try:
            p_type = RefineryProcess(p_type_str.lower())
        except ValueError:
            logger.warning(f"Unknown process {p_type_str}, defaulting to FCC.")
            p_type = RefineryProcess.FCC
            
        simulator = ProcessSimulator(p_type)
        yields = simulator.simulate(feed, temp, press)
        
        # Normalize yields
        total = yields.fuel_gas + yields.lpg + yields.gasoline + yields.diesel + yields.heavy_oil + yields.coke
        
        return {
            "agent": self.name,
            "feedstock_properties": {
                "specific_gravity": round(feed.specific_gravity, 4),
                "api_gravity": feed.api_gravity
            },
            "process": p_type.value,
            "conditions": {
                "temperature_C": temp,
                "pressure_bar": press
            },
            "normalized_yields_wt_pct": {
                "fuel_gas": round(yields.fuel_gas / total * 100, 2),
                "lpg": round(yields.lpg / total * 100, 2),
                "gasoline": round(yields.gasoline / total * 100, 2),
                "diesel": round(yields.diesel / total * 100, 2),
                "heavy_oil": round(yields.heavy_oil / total * 100, 2),
                "coke": round(yields.coke / total * 100, 2)
            }
        }

if __name__ == "__main__":
    agent = PetrochemiaAgent()
    req = {
        "process_type": "fcc",
        "feedstock": {
            "name": "Heavy Vacuum Gas Oil",
            "api_gravity": 22.5,
            "sulfur_wt_pct": 2.1
        },
        "operating_temp_C": 540,
        "operating_press_bar": 2.5
    }
    print(json.dumps(agent.evaluate(req), indent=2))
