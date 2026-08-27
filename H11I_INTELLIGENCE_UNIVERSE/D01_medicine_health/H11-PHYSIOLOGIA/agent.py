"""
H11-PHYSIOLOGIA: Physiology & Organ Systems
Layer 1 - Medicine & Health Sciences

Simulates dynamic human physiology using compartmental models and feedback loops.
"""

from __future__ import annotations
import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Protocol, Tuple

logger = logging.getLogger(__name__)

class ParameterType(Enum):
    HEMODYNAMIC = auto()
    RESPIRATORY = auto()
    METABOLIC = auto()
    ENDOCRINE = auto()
    RENAL = auto()

@dataclass
class PhysiologicalParameter:
    name: str
    param_type: ParameterType
    value: float
    baseline: float
    unit: str
    lower_bound: float
    upper_bound: float
    critical_lower: float
    critical_upper: float

    def is_critical(self) -> bool:
        return self.value <= self.critical_lower or self.value >= self.critical_upper

@dataclass
class StressorEvent:
    name: str
    magnitude: float
    target_param: str
    duration_secs: float
    time_applied: float = 0.0

class FeedbackLoop(Protocol):
    def apply(self, state: Dict[str, PhysiologicalParameter], dt: float) -> None:
        ...

class BaroreceptorReflex:
    def __init__(self, sensitivity: float = 0.5):
        self.sensitivity = sensitivity
        
    def apply(self, state: Dict[str, PhysiologicalParameter], dt: float) -> None:
        map_param = state.get("MeanArterialPressure")
        hr_param = state.get("HeartRate")
        
        if map_param and hr_param:
            error = map_param.baseline - map_param.value
            hr_adjustment = error * self.sensitivity * dt
            hr_param.value += hr_adjustment
            # Limits
            hr_param.value = max(hr_param.lower_bound, min(hr_param.value, hr_param.upper_bound))

class RAASSystem:
    def __init__(self, activation_rate: float = 0.05):
        self.activation_rate = activation_rate

    def apply(self, state: Dict[str, PhysiologicalParameter], dt: float) -> None:
        bp = state.get("MeanArterialPressure")
        ang2 = state.get("AngiotensinII")
        
        if bp and ang2:
            if bp.value < bp.baseline:
                ang2.value += self.activation_rate * dt
            else:
                ang2.value -= (self.activation_rate / 2) * dt
            ang2.value = max(ang2.lower_bound, min(ang2.value, ang2.upper_bound))

class PhysiologyEngine:
    def __init__(self):
        self.parameters: Dict[str, PhysiologicalParameter] = {}
        self.feedbacks: List[FeedbackLoop] = []
        self.time: float = 0.0

    def add_parameter(self, param: PhysiologicalParameter) -> None:
        self.parameters[param.name] = param

    def add_feedback(self, loop: FeedbackLoop) -> None:
        self.feedbacks.append(loop)

    def apply_stressor(self, stressor: StressorEvent) -> None:
        logger.warning(f"Applying stressor: {stressor.name}")
        param = self.parameters.get(stressor.target_param)
        if param:
            param.value += stressor.magnitude

    def step(self, dt: float) -> None:
        """Advances the simulation by dt seconds."""
        # 1. Apply feedback loops
        for fb in self.feedbacks:
            fb.apply(self.parameters, dt)
        
        # 2. Baseline reversion (simple natural homeostasis)
        for p in self.parameters.values():
            if p.name != "AngiotensinII": # Exceptions managed by specific loops
                reversion = (p.baseline - p.value) * 0.01 * dt
                p.value += reversion
        
        self.time += dt

    def get_state(self) -> Dict[str, float]:
        return {name: p.value for name, p in self.parameters.items()}

class PhysiologyAgent:
    """Agent interface for physiological simulation."""
    def __init__(self):
        self.engine = PhysiologyEngine()

    async def initialize(self) -> None:
        logger.info("Initializing H11-PHYSIOLOGIA baseline state...")
        self.engine.add_parameter(PhysiologicalParameter(
            "MeanArterialPressure", ParameterType.HEMODYNAMIC, 90.0, 90.0, "mmHg", 60.0, 120.0, 40.0, 150.0
        ))
        self.engine.add_parameter(PhysiologicalParameter(
            "HeartRate", ParameterType.HEMODYNAMIC, 75.0, 75.0, "bpm", 40.0, 180.0, 30.0, 220.0
        ))
        self.engine.add_parameter(PhysiologicalParameter(
            "AngiotensinII", ParameterType.ENDOCRINE, 10.0, 10.0, "pg/mL", 0.0, 100.0, 0.0, 200.0
        ))
        
        self.engine.add_feedback(BaroreceptorReflex())
        self.engine.add_feedback(RAASSystem())

    async def simulate_duration(self, duration: float, dt: float = 1.0) -> Dict[str, Any]:
        """Runs the simulation forward in time."""
        steps = int(duration / dt)
        for _ in range(steps):
            self.engine.step(dt)
        return {
            "time_elapsed": duration,
            "final_state": self.engine.get_state()
        }

    async def trigger_event(self, event: StressorEvent) -> None:
        """Injects an acute event like hemorrhage or drug dose."""
        self.engine.apply_stressor(event)

    EFFECT_STRESSORS = {
        "anemia": ("MeanArterialPressure", -12.0),
        "fever": ("HeartRate", 18.0),
        "portal_hypertension": ("MeanArterialPressure", -8.0),
        "malabsorption": ("MeanArterialPressure", -5.0),
    }

    async def apply_systemic_effects(self, effects: List[str]) -> Dict[str, float]:
        """Map parasitology systemic effects onto hemodynamic/endocrine stressors."""
        for effect in effects:
            mapping = self.EFFECT_STRESSORS.get(effect)
            if not mapping:
                continue
            target, magnitude = mapping
            await self.trigger_event(StressorEvent(effect, magnitude, target, 0.0))
        return self.engine.get_state()

async def main():
    agent = PhysiologyAgent()
    await agent.initialize()
    
    # Hemorrhage simulation
    hemorrhage = StressorEvent("Severe Hemorrhage", -30.0, "MeanArterialPressure", 0.0)
    await agent.trigger_event(hemorrhage)
    
    print("Post-hemorrhage state:", agent.engine.get_state())
    res = await agent.simulate_duration(60.0) # 1 minute
    print("State after 60s compensation:", res)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
