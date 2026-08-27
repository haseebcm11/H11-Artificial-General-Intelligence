"""H11-PHYSICS-ENGINE: Semi-implicit Euler integration of point masses.

Provides rigorous forward kinematics simulation computing v += a*dt and x += v*dt.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-PHYSICS-ENGINE"

class PhysicsEngineError(ValueError): pass

@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        
    def __mul__(self, scalar: float) -> Vector3:
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

@dataclass
class Body:
    id: str
    position: Vector3
    velocity: Vector3
    force: Vector3
    mass: float

@dataclass
class PhysicsEngineInput:
    bodies: List[Body]
    dt: float
    gravity: Vector3 = field(default_factory=lambda: Vector3(0.0, -9.81, 0.0))
    drag_coeff: float = 0.1

@dataclass
class PhysicsEngineOutput:
    agent_id: str
    bodies_simulated: int
    total_kinetic_energy: float
    execution_time_ms: float

class PhysicsEngineAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: PhysicsEngineInput) -> PhysicsEngineOutput:
        start_time = time.perf_counter()
        
        if input_data.dt <= 0:
            raise PhysicsEngineError("dt must be strictly positive")

        total_ke = 0.0
        
        # Semi-implicit Euler Integration
        # 1. Update velocities based on forces
        # 2. Update positions based on new velocities
        for body in input_data.bodies:
            m = body.mass if body.mass > 0 else 1.0
            
            # F = m*g + applied_force - drag*v
            drag = body.velocity * input_data.drag_coeff
            total_force = Vector3(
                (m * input_data.gravity.x) + body.force.x - drag.x,
                (m * input_data.gravity.y) + body.force.y - drag.y,
                (m * input_data.gravity.z) + body.force.z - drag.z
            )
            
            acceleration = total_force * (1.0 / m)
            
            # v += a * dt
            body.velocity = body.velocity + (acceleration * input_data.dt)
            
            # x += v * dt
            body.position = body.position + (body.velocity * input_data.dt)
            
            # KE = 0.5 * m * v^2
            v_sq = (body.velocity.x**2 + body.velocity.y**2 + body.velocity.z**2)
            total_ke += 0.5 * m * v_sq

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return PhysicsEngineOutput(
            agent_id=AGENT_ID,
            bodies_simulated=len(input_data.bodies),
            total_kinetic_energy=total_ke,
            execution_time_ms=elapsed_ms
        )
