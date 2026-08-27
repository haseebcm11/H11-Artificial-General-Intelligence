"""
Agent Module: D06_CARTOGRAPHIA
Agent Class: CartographiaAgent

Geodetic transformations and Haversine great-circle distance computation across ellipsoidal Earth coordinates.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_CARTOGRAPHIA"


class CartographiaError(ValueError):
    """Raised when CartographiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class CartographiaAgentInput:
    lat1: float = 37.7749
    lon1: float = -122.4194
    lat2: float = 34.0522
    lon2: float = -118.2437


@dataclass(frozen=True)
class CartographiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    great_circle_distance_km: float = 0.0


class CartographiaAgent:
    """
    Geodetic transformations and Haversine great-circle distance computation across ellipsoidal Earth coordinates.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: CartographiaAgentInput) -> CartographiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        r = 6371.0  # Earth radius in km
        phi1, phi2 = math.radians(inputs.lat1), math.radians(inputs.lat2)
        dphi = math.radians(inputs.lat2 - inputs.lat1)
        dlam = math.radians(inputs.lon2 - inputs.lon1)
        a = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2.0)**2
        d = 2.0 * r * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        metrics = {"distance_km": round(d, 2), "distance_miles": round(d * 0.621371, 2)}
        return CartographiaAgentOutput(status="COMPLETED", score=round(min(1.0, d/20000.0), 4), metrics=metrics, great_circle_distance_km=round(d, 2))
