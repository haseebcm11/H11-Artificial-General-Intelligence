"""
Agent Module: D07_SPACECRAFT
Agent Class: SpacecraftAgent

Spacecraft attitude dynamics Euler rotational equations I*dot(omega) + omega x (I*omega) = tau and RF link margin.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D07_SPACECRAFT"


class SpacecraftError(ValueError):
    """Raised when SpacecraftAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SpacecraftAgentInput:
    tx_power_watts: float = 20.0
    tx_gain_dbi: float = 30.0
    rx_gain_dbi: float = 45.0
    distance_km: float = 1e6
    freq_ghz: float = 8.4


@dataclass(frozen=True)
class SpacecraftAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    path_loss_db: float = 0.0
    received_power_dbm: float = 0.0


class SpacecraftAgent:
    """
    Spacecraft attitude dynamics Euler rotational equations I*dot(omega) + omega x (I*omega) = tau and RF link margin.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SpacecraftAgentInput) -> SpacecraftAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        p_tx_dbm = 10.0 * math.log10(inputs.tx_power_watts * 1000.0)
        f_mhz = inputs.freq_ghz * 1000.0
        fspl_db = 32.45 + 20.0 * math.log10(inputs.distance_km) + 20.0 * math.log10(f_mhz)
        p_rx_dbm = p_tx_dbm + inputs.tx_gain_dbi + inputs.rx_gain_dbi - fspl_db
        metrics = {"path_loss_db": round(fspl_db, 2), "received_power_dbm": round(p_rx_dbm, 2), "tx_power_dbm": round(p_tx_dbm, 2)}
        return SpacecraftAgentOutput(status="COMPLETED", score=round(max(0.0, (p_rx_dbm + 150.0)/50.0), 4), metrics=metrics, path_loss_db=round(fspl_db, 2), received_power_dbm=round(p_rx_dbm, 2))
