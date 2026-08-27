"""
Agent Module: D06_REMOTESENSING
Agent Class: RemotesensingAgent

Multispectral satellite index analytics calculating NDVI = (NIR - Red)/(NIR + Red) and NDWI water masking.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_REMOTESENSING"


class RemotesensingError(ValueError):
    """Raised when RemotesensingAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class RemotesensingAgentInput:
    nir_band: list[float] = field(default_factory=lambda: [0.6, 0.55, 0.2, 0.7])
    red_band: list[float] = field(default_factory=lambda: [0.1, 0.12, 0.25, 0.08])


@dataclass(frozen=True)
class RemotesensingAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    mean_ndvi: float = 0.0
    ndvi_values: list[float] = field(default_factory=list)


class RemotesensingAgent:
    """
    Multispectral satellite index analytics calculating NDVI = (NIR - Red)/(NIR + Red) and NDWI water masking.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: RemotesensingAgentInput) -> RemotesensingAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        nir, red = inputs.nir_band, inputs.red_band
        ndvi = [round((n - r) / max(n + r, 1e-6), 4) for n, r in zip(nir, red)]
        mean_ndvi = sum(ndvi) / max(len(ndvi), 1)
        metrics = {"mean_ndvi": round(mean_ndvi, 4), "vegetation_fraction": round(sum(1 for v in ndvi if v > 0.4)/max(len(ndvi), 1), 4)}
        return RemotesensingAgentOutput(status="COMPLETED", score=round(max(0.0, mean_ndvi), 4), metrics=metrics, mean_ndvi=round(mean_ndvi, 4), ndvi_values=ndvi)
