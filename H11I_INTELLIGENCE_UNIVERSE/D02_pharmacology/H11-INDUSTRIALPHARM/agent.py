import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class UnitOperationType(Enum):
    MILLING = "milling"
    BLENDING = "blending"
    GRANULATION = "granulation"
    COMPRESSION = "compression"
    COATING = "coating"

@dataclass
class CriticalProcessParameter:
    name: str
    target_value: float
    lower_limit: float
    upper_limit: float
    unit: str

@dataclass
class CriticalQualityAttribute:
    name: str
    target_value: float
    specification_limit: float
    unit: str

@dataclass
class UnitOperation:
    op_type: UnitOperationType
    cpps: List[CriticalProcessParameter]
    cqas: List[CriticalQualityAttribute]
    
    def validate_process(self, measured_cpps: Dict[str, float]) -> bool:
        """Check if measured parameters fall within validated CPP ranges."""
        for cpp in self.cpps:
            if cpp.name in measured_cpps:
                val = measured_cpps[cpp.name]
                if val < cpp.lower_limit or val > cpp.upper_limit:
                    return False
        return True

class QualityByDesignEngine:
    """Manages QbD risk assessments and control strategies."""
    def __init__(self):
        self.risk_matrix = {}
        
    def assess_risk(self, cpp: CriticalProcessParameter, cqa: CriticalQualityAttribute, impact_score: int) -> str:
        """Simple FMEA style risk assessment linking CPP to CQA."""
        # impact_score: 1-10
        variance = (cpp.upper_limit - cpp.lower_limit) / cpp.target_value
        risk_score = impact_score * variance * 100
        
        if risk_score > 50:
            return "HIGH"
        elif risk_score > 20:
            return "MEDIUM"
        return "LOW"

class IndustrialPharmacyAgent:
    """Agent for pharmaceutical manufacturing and scale-up."""
    
    def __init__(self, gmp_version: str = "ICH Q7"):
        self.gmp_version = gmp_version
        self.operations: Dict[str, UnitOperation] = {}
        self.qbd_engine = QualityByDesignEngine()
        
    def define_unit_operation(self, name: str, op_type: UnitOperationType, cpps: List[CriticalProcessParameter], cqas: List[CriticalQualityAttribute]) -> None:
        """Define a manufacturing unit operation."""
        self.operations[name] = UnitOperation(op_type=op_type, cpps=cpps, cqas=cqas)
        
    def evaluate_batch_record(self, batch_id: str, op_data: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Evaluate electronic batch record against established operations."""
        results = {"batch_id": batch_id, "deviations": [], "status": "APPROVED"}
        
        for op_name, measured_cpps in op_data.items():
            if op_name not in self.operations:
                results["deviations"].append(f"Unknown operation: {op_name}")
                results["status"] = "REJECTED"
                continue
                
            op = self.operations[op_name]
            is_valid = op.validate_process(measured_cpps)
            
            if not is_valid:
                results["deviations"].append(f"OOS (Out of Spec) in {op_name}")
                results["status"] = "REJECTED"
                
        return results

    def scale_up_compression(self, lab_scale_rpm: float, lab_scale_diameter: float, production_diameter: float) -> float:
        """Basic kinematic scale-up calculation for a tablet press (constant dwell time approx)."""
        # production_rpm = lab_scale_rpm * (lab_scale_diameter / production_diameter)
        if production_diameter == 0:
            return 0.0
        return lab_scale_rpm * (lab_scale_diameter / production_diameter)

if __name__ == "__main__":
    agent = IndustrialPharmacyAgent()
    cpp1 = CriticalProcessParameter("compression_force", 15.0, 10.0, 20.0, "kN")
    cpp2 = CriticalProcessParameter("turret_speed", 30.0, 25.0, 35.0, "rpm")
    cqa1 = CriticalQualityAttribute("tablet_hardness", 100.0, 10.0, "N")
    
    agent.define_unit_operation("Tableting", UnitOperationType.COMPRESSION, [cpp1, cpp2], [cqa1])
    
    batch_data = {
        "Tableting": {
            "compression_force": 16.5,
            "turret_speed": 32.0
        }
    }
    
    result = agent.evaluate_batch_record("BATCH-001", batch_data)
    print(f"Batch Review: {result}")
    
    prod_rpm = agent.scale_up_compression(30.0, 0.5, 1.5)
    print(f"Scaled up turret speed: {prod_rpm:.1f} rpm")
