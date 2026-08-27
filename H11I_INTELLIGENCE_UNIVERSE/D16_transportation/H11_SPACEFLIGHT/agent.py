import math
import dataclasses
from typing import List, Optional, Dict

AGENT_ID = "H11_SPACEFLIGHT"

class H11SpaceflightException(Exception):
    pass

@dataclasses.dataclass
class H11SpaceflightInput:
    mass_kg: float
    velocity_mps: float
    drag_coefficient: float
    frontal_area_sqm: float
    air_density: float = 1.225
    orbit_radius_m: Optional[float] = None
    battery_capacity_kwh: Optional[float] = None
    efficiency_kwh_per_km: Optional[float] = None

@dataclasses.dataclass
class H11SpaceflightOutput:
    drag_force_n: float
    kinetic_energy_j: float
    orbital_velocity_mps: Optional[float]
    max_range_km: Optional[float]
    bernoulli_lift_n: float
    agent_id: str

class H11SpaceflightAgent:
    """
    Transportation Domain Agent computing aerodynamics and orbital mechanics.
    Implements:
    - Drag force: F = 0.5 * Cd * rho * A * v^2
    - Orbital velocity: v = sqrt(G*M / r)
    - EV Range = Battery / Efficiency
    - Bernoulli Lift approximation.
    """
    
    G_CONSTANT = 6.67430e-11
    EARTH_MASS = 5.972e24

    def process(self, request: H11SpaceflightInput) -> H11SpaceflightOutput:
        if request.mass_kg <= 0 or request.velocity_mps < 0:
            raise H11SpaceflightException("Invalid physical parameters.")
            
        # 1. Aerodynamic Drag
        # F = 0.5 * Cd * rho * A * v^2
        drag_force = 0.5 * request.drag_coefficient * request.air_density * request.frontal_area_sqm * (request.velocity_mps ** 2)
        
        # 2. Kinetic Energy
        kinetic_energy = 0.5 * request.mass_kg * (request.velocity_mps ** 2)
        
        # 3. Orbital Velocity (if applicable)
        orbital_v = None
        if request.orbit_radius_m and request.orbit_radius_m > 6371000:
            orbital_v = math.sqrt(self.G_CONSTANT * self.EARTH_MASS / request.orbit_radius_m)
            
        # 4. EV Range Equation
        max_range = None
        if request.battery_capacity_kwh and request.efficiency_kwh_per_km:
            if request.efficiency_kwh_per_km > 0:
                max_range = request.battery_capacity_kwh / request.efficiency_kwh_per_km
                
        # 5. Bernoulli Lift approximation
        # Assuming pressure differential creates lift
        lift_coefficient = request.drag_coefficient * 0.8 # heuristic
        bernoulli_lift = 0.5 * lift_coefficient * request.air_density * request.frontal_area_sqm * (request.velocity_mps ** 2)
        
        return H11SpaceflightOutput(
            drag_force_n=drag_force,
            kinetic_energy_j=kinetic_energy,
            orbital_velocity_mps=orbital_v,
            max_range_km=max_range,
            bernoulli_lift_n=bernoulli_lift,
            agent_id=AGENT_ID
        )
