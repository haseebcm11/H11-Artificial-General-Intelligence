import math
from dataclasses import dataclass

AGENT_ID = "H11-QUANTUM"

@dataclass
class QuantumInput:
    t1_time_us: float
    t2_time_us: float
    gate_time_ns: float
    num_gates: int
    base_gate_fidelity: float

@dataclass
class QuantumOutput:
    decoherence_fidelity_limit: float
    operational_fidelity: float
    total_circuit_fidelity: float

class QuantumException(Exception):
    pass

class QuantumAgent:
    """
    Computes qubit fidelity including T1 (relaxation) and T2 (dephasing) decay factors.
    Formula: F_decoherence = exp(-t/T1) * exp(-(t/T2)^2) or similar approximations.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: QuantumInput) -> QuantumOutput:
        if input_data.t1_time_us <= 0 or input_data.t2_time_us <= 0:
            raise QuantumException("T1 and T2 must be positive.")
            
        total_time_ns = input_data.num_gates * input_data.gate_time_ns
        total_time_us = total_time_ns / 1000.0
        
        # Simple exponential decay for T1 and T2
        # Fidelity drop due to relaxation (T1) and dephasing (T2)
        # Using typical exponential decay for depolarization
        f_t1 = math.exp(-total_time_us / input_data.t1_time_us)
        f_t2 = math.exp(-total_time_us / input_data.t2_time_us)
        
        decoherence_fidelity = f_t1 * f_t2
        
        # Operational fidelity assumes independent errors per gate
        # F_op = (F_gate) ^ N
        operational_fidelity = math.pow(input_data.base_gate_fidelity, input_data.num_gates)
        
        total_fidelity = decoherence_fidelity * operational_fidelity
        
        return QuantumOutput(
            decoherence_fidelity_limit=decoherence_fidelity,
            operational_fidelity=operational_fidelity,
            total_circuit_fidelity=total_fidelity
        )
