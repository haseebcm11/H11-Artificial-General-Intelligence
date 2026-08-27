import re
import time
from typing import List, Dict, Callable, Any
from dataclasses import dataclass
from enum import Enum

class ActionStatus(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    FLAG = "FLAG"

@dataclass
class OperationRequest:
    op_id: str
    payload_text: str
    risk_level: float
    source_module: str

@dataclass
class GuardrailResult:
    status: ActionStatus
    triggered_filters: List[str]
    latency_ms: float

class AbstractFilter:
    def __init__(self, name: str):
        self.name = name
        
    def evaluate(self, op: OperationRequest) -> bool:
        """Returns True if the operation VIOLATES the filter."""
        raise NotImplementedError

class RegexFilter(AbstractFilter):
    def __init__(self, name: str, pattern: str):
        super().__init__(name)
        self.pattern = re.compile(pattern, re.IGNORECASE)
        
    def evaluate(self, op: OperationRequest) -> bool:
        return bool(self.pattern.search(op.payload_text))

class RiskThresholdFilter(AbstractFilter):
    def __init__(self, name: str, max_risk: float):
        super().__init__(name)
        self.max_risk = max_risk
        
    def evaluate(self, op: OperationRequest) -> bool:
        return op.risk_level > self.max_risk

class H11GuardrailSystem:
    def __init__(self):
        self.filters: List[AbstractFilter] = []
        self.circuit_breakers_tripped: set[str] = set()
        self.filter_stats: Dict[str, Dict[str, Any]] = {}
        
    def add_filter(self, f: AbstractFilter):
        self.filters.append(f)
        self.filter_stats[f.name] = {"hits": 0, "last_triggered": 0.0}
        
    def check_operation(self, op: OperationRequest) -> GuardrailResult:
        start_time = time.time()
        triggered = []
        
        # Fast path check: if a breaker is already tripped for this source, deny immediately
        if op.source_module in self.circuit_breakers_tripped:
            return GuardrailResult(ActionStatus.DENY, ["CIRCUIT_BREAKER_ACTIVE"], (time.time() - start_time) * 1000)
            
        for f in self.filters:
            if f.evaluate(op):
                triggered.append(f.name)
                self.filter_stats[f.name]["hits"] += 1
                self.filter_stats[f.name]["last_triggered"] = time.time()
                
        status = ActionStatus.ALLOW
        if triggered:
            status = ActionStatus.DENY
            # Trip breaker if multiple filters trigger or it's a high risk op
            if len(triggered) > 1 or op.risk_level > 0.9:
                self._trip_breaker(op.source_module)
                
        latency = (time.time() - start_time) * 1000
        return GuardrailResult(status, triggered, latency)
        
    def _trip_breaker(self, module_name: str):
        self.circuit_breakers_tripped.add(module_name)
        
    def reset_breaker(self, module_name: str):
        if module_name in self.circuit_breakers_tripped:
            self.circuit_breakers_tripped.remove(module_name)
