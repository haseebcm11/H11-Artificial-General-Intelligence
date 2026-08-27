import json
import logging
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
import math

logger = logging.getLogger(__name__)

class ControlMode(Enum):
    POSITION = auto()
    VELOCITY = auto()
    TORQUE = auto()
    IMPEDANCE = auto()

class ActuatorType(Enum):
    BLDC = auto()
    STEPPER = auto()
    SERVO = auto()
    PNEUMATIC = auto()

@dataclass
class ActuatorLimits:
    max_torque_nm: float
    max_velocity_rads: float
    position_min_rad: float
    position_max_rad: float
    thermal_limit_c: float
    
@dataclass
class PIDGains:
    kp: float
    ki: float
    kd: float
    anti_windup: bool = True
    integrator_max: float = 100.0

@dataclass
class ActuatorState:
    position: float = 0.0
    velocity: float = 0.0
    torque: float = 0.0
    temperature: float = 25.0
    fault_code: int = 0

class PIDController:
    def __init__(self, gains: PIDGains, dt: float):
        self.gains = gains
        self.dt = dt
        self.integral = 0.0
        self.prev_error = 0.0
        
    def compute(self, setpoint: float, measured: float) -> float:
        error = setpoint - measured
        self.integral += error * self.dt
        
        if self.gains.anti_windup:
            self.integral = max(-self.gains.integrator_max, min(self.gains.integrator_max, self.integral))
            
        derivative = (error - self.prev_error) / self.dt if self.dt > 0 else 0.0
        self.prev_error = error
        
        return (self.gains.kp * error) + (self.gains.ki * self.integral) + (self.gains.kd * derivative)

class Actuator:
    def __init__(self, config: Dict[str, Any]):
        self.id = config["id"]
        self.type = ActuatorType[config["type"]]
        self.control_mode = ControlMode[config["control_mode"]]
        
        limits = config["limits"]
        self.limits = ActuatorLimits(
            max_torque_nm=limits["max_torque_nm"],
            max_velocity_rads=limits["max_velocity_rads"],
            position_min_rad=limits.get("position_min_rad", -math.inf),
            position_max_rad=limits.get("position_max_rad", math.inf),
            thermal_limit_c=limits.get("thermal_limit_c", 80.0)
        )
        
        gains = config.get("pid_gains", {"kp": 1.0, "ki": 0.0, "kd": 0.1})
        self.pid = PIDController(
            PIDGains(gains["kp"], gains["ki"], gains["kd"], gains.get("anti_windup", True)),
            dt=0.01  # Assume 100Hz control loop
        )
        
        self.state = ActuatorState()
        self.target = 0.0
        self.enabled = False
        
    def enable(self):
        self.enabled = True
        logger.info(f"Actuator {self.id} enabled.")
        
    def disable(self):
        self.enabled = False
        self.target = 0.0
        logger.info(f"Actuator {self.id} disabled.")
        
    def set_target(self, target: float):
        if self.control_mode == ControlMode.POSITION:
            self.target = max(self.limits.position_min_rad, min(self.limits.position_max_rad, target))
        elif self.control_mode == ControlMode.VELOCITY:
            self.target = max(-self.limits.max_velocity_rads, min(self.limits.max_velocity_rads, target))
        elif self.control_mode == ControlMode.TORQUE:
            self.target = max(-self.limits.max_torque_nm, min(self.limits.max_torque_nm, target))
            
    def update(self) -> ActuatorState:
        if not self.enabled:
            self.state.torque = 0.0
            return self.state
            
        # Check thermal limits
        if self.state.temperature >= self.limits.thermal_limit_c:
            logger.warning(f"Actuator {self.id} exceeded thermal limit! Disabling.")
            self.state.fault_code = 1
            self.disable()
            return self.state
            
        # Simulate control
        if self.control_mode == ControlMode.POSITION:
            command_torque = self.pid.compute(self.target, self.state.position)
        elif self.control_mode == ControlMode.VELOCITY:
            command_torque = self.pid.compute(self.target, self.state.velocity)
        else:
            command_torque = self.target
            
        # Apply torque limits
        command_torque = max(-self.limits.max_torque_nm, min(self.limits.max_torque_nm, command_torque))
        
        # Simulate physics step (highly simplified)
        inertia = 0.01
        damping = 0.1
        acceleration = (command_torque - (self.state.velocity * damping)) / inertia
        
        self.state.velocity += acceleration * self.pid.dt
        
        # Enforce velocity limits
        self.state.velocity = max(-self.limits.max_velocity_rads, min(self.limits.max_velocity_rads, self.state.velocity))
        
        self.state.position += self.state.velocity * self.pid.dt
        self.state.torque = command_torque
        
        # Simulate slight heating
        self.state.temperature += abs(command_torque) * 0.001
        
        return self.state

class ActuatorManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.actuators: Dict[str, Actuator] = {
            act_conf["id"]: Actuator(act_conf) for act_conf in config.get("actuators", [])
        }
        self.emergency_stop = False
        self.last_cmd_time = time.time()
        self.timeout_s = config.get("safety", {}).get("timeout_ms", 100) / 1000.0
        
    def trigger_estop(self):
        self.emergency_stop = True
        for act in self.actuators.values():
            act.disable()
        logger.critical("EMERGENCY STOP TRIGGERED.")
        
    def update_targets(self, targets: Dict[str, float]):
        if self.emergency_stop:
            return
            
        self.last_cmd_time = time.time()
        for act_id, target in targets.items():
            if act_id in self.actuators:
                self.actuators[act_id].set_target(target)
                
    def step(self):
        if not self.emergency_stop and (time.time() - self.last_cmd_time) > self.timeout_s:
            logger.warning("Command timeout! Disabling actuators.")
            for act in self.actuators.values():
                act.disable()
                
        states = {}
        for act_id, act in self.actuators.items():
            states[act_id] = act.update()
        return states

if __name__ == "__main__":
    config = {
        "actuators": [
            {
                "id": "joint_shoulder",
                "type": "BLDC",
                "control_mode": "POSITION",
                "limits": {
                    "max_torque_nm": 50.0,
                    "max_velocity_rads": 3.14,
                    "position_min_rad": -1.5,
                    "position_max_rad": 1.5,
                    "thermal_limit_c": 85.0
                },
                "pid_gains": {"kp": 10.0, "ki": 0.1, "kd": 0.5}
            }
        ],
        "safety": {
            "emergency_stop_enabled": True,
            "timeout_ms": 500
        }
    }
    
    manager = ActuatorManager(config)
    manager.actuators["joint_shoulder"].enable()
    
    manager.update_targets({"joint_shoulder": 1.0})
    
    for i in range(50):
        states = manager.step()
        state = states["joint_shoulder"]
        print(f"Step {i}: Pos={state.position:.3f}, Vel={state.velocity:.3f}, Trq={state.torque:.3f}")
