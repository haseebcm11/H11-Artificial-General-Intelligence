import time
import random
import logging
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H11-RETRY")

class ErrorCategory(Enum):
    TRANSIENT = auto()      # E.g. timeout, 5xx server error, temporary network partition
    PERMANENT = auto()      # E.g. 400 Bad Request, unauthorized, invalid payload
    RATE_LIMIT = auto()     # E.g. 429 Too Many Requests

class CircuitState(Enum):
    CLOSED = auto()         # Healthy, normal operation
    OPEN = auto()           # Failing, requests are fast-failed
    HALF_OPEN = auto()      # Probation, testing if healthy

@dataclass
class RetryPolicy:
    max_attempts: int = 3
    base_delay_ms: float = 1000.0
    max_delay_ms: float = 30000.0
    exponential_base: float = 2.0
    jitter_factor: float = 0.2

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout_ms: float = 60000.0
    half_open_success_required: int = 3

@dataclass
class OperationState:
    operation_id: str
    service_name: str
    attempts: int = 0
    start_time: float = field(default_factory=time.time)
    payload: Any = None
    last_error: Optional[str] = None

class DeadLetterQueue:
    def __init__(self):
        self.queue: List[OperationState] = []
        
    def enqueue(self, state: OperationState, reason: str):
        logger.error(f"[DLQ] Operation {state.operation_id} dead-lettered. Reason: {reason}")
        self.queue.append(state)
        
    def list_items(self) -> List[OperationState]:
        return self.queue

class CircuitBreaker:
    def __init__(self, name: str, config: CircuitBreakerConfig):
        self.name = name
        self.config = config
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.successes_in_half_open = 0
        self.last_failure_time = 0.0

    def record_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.successes_in_half_open += 1
            if self.successes_in_half_open >= self.config.half_open_success_required:
                logger.info(f"[CircuitBreaker] {self.name} recovered. State -> CLOSED")
                self.state = CircuitState.CLOSED
                self.failures = 0
                self.successes_in_half_open = 0
        elif self.state == CircuitState.CLOSED:
            self.failures = 0 # Reset on success

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.CLOSED and self.failures >= self.config.failure_threshold:
            logger.warning(f"[CircuitBreaker] {self.name} threshold exceeded. State -> OPEN")
            self.state = CircuitState.OPEN

        elif self.state == CircuitState.HALF_OPEN:
            logger.warning(f"[CircuitBreaker] {self.name} failed during probation. State -> OPEN")
            self.state = CircuitState.OPEN
            self.successes_in_half_open = 0

    def allow_request(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
            
        if self.state == CircuitState.OPEN:
            now = time.time()
            if (now - self.last_failure_time) * 1000 >= self.config.recovery_timeout_ms:
                logger.info(f"[CircuitBreaker] {self.name} timeout elapsed. State -> HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self.successes_in_half_open = 0
                return True # Allow a probe
            return False
            
        if self.state == CircuitState.HALF_OPEN:
            # Allow limited requests to probe
            # For simplicity, we allow all in this prototype until success threshold or failure
            return True

class RetryRecoveryAgent:
    def __init__(self):
        self.retry_policies: Dict[str, RetryPolicy] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.active_operations: Dict[str, OperationState] = {}
        self.dlq = DeadLetterQueue()
        self.fallback_registry: Dict[str, Callable[[Any], Any]] = {}
        self.compensation_registry: Dict[str, Callable[[Any], bool]] = {}

    def configure_service(self, service_name: str, retry_policy: RetryPolicy, cb_config: CircuitBreakerConfig):
        self.retry_policies[service_name] = retry_policy
        self.circuit_breakers[service_name] = CircuitBreaker(service_name, cb_config)

    def register_fallback(self, service_name: str, fallback_func: Callable[[Any], Any]):
        self.fallback_registry[service_name] = fallback_func

    def register_compensation(self, service_name: str, comp_func: Callable[[Any], bool]):
        self.compensation_registry[service_name] = comp_func

    def _classify_error(self, error_type: str) -> ErrorCategory:
        error_type = error_type.upper()
        if error_type in ["TIMEOUT", "NETWORK", "INTERNAL", "UNAVAILABLE"]:
            return ErrorCategory.TRANSIENT
        elif error_type == "RATE_LIMIT":
            return ErrorCategory.RATE_LIMIT
        else:
            return ErrorCategory.PERMANENT

    def _calculate_backoff(self, policy: RetryPolicy, attempt: int) -> float:
        delay = policy.base_delay_ms * (policy.exponential_base ** attempt)
        delay = min(delay, policy.max_delay_ms)
        jitter = delay * policy.jitter_factor * random.uniform(-1, 1)
        return delay + jitter

    def evaluate_operation(self, op_id: str, service: str, payload: Any) -> Dict[str, Any]:
        """Called BEFORE attempting an operation to check circuit breakers."""
        if service not in self.circuit_breakers:
            self.configure_service(service, RetryPolicy(), CircuitBreakerConfig())
            
        cb = self.circuit_breakers[service]
        
        if not cb.allow_request():
            if service in self.fallback_registry:
                return {
                    "action": "FALLBACK",
                    "circuit_state": cb.state.name,
                    "fallback_payload": self.fallback_registry[service](payload)
                }
            return {
                "action": "ABORT",
                "circuit_state": cb.state.name,
                "reason": "Circuit breaker OPEN, no fallback."
            }
            
        # Register new op if not exists
        if op_id not in self.active_operations:
            self.active_operations[op_id] = OperationState(operation_id=op_id, service_name=service, payload=payload)
            
        return {"action": "PROCEED", "circuit_state": cb.state.name}

    def report_success(self, op_id: str):
        if op_id in self.active_operations:
            service = self.active_operations[op_id].service_name
            if service in self.circuit_breakers:
                self.circuit_breakers[service].record_success()
            del self.active_operations[op_id]

    def report_failure(self, op_id: str, error_type: str, error_message: str) -> Dict[str, Any]:
        """Called AFTER an operation fails to determine recovery strategy."""
        if op_id not in self.active_operations:
            return {"action": "ABORT", "reason": "Unknown operation ID"}
            
        op_state = self.active_operations[op_id]
        service = op_state.service_name
        op_state.last_error = error_message
        
        cb = self.circuit_breakers.get(service)
        if cb:
            cb.record_failure()
            
        category = self._classify_error(error_type)
        policy = self.retry_policies.get(service, RetryPolicy())
        
        # Immediate abort for permanent errors
        if category == ErrorCategory.PERMANENT:
            if service in self.compensation_registry:
                success = self.compensation_registry[service](op_state.payload)
                logger.info(f"Compensation action executed for {op_id}: success={success}")
                self.dlq.enqueue(op_state, "Permanent Error")
                del self.active_operations[op_id]
                return {"action": "COMPENSATE", "circuit_state": cb.state.name if cb else "UNKNOWN", "dlq_enqueued": True}
            
            self.dlq.enqueue(op_state, f"Permanent error: {error_message}")
            del self.active_operations[op_id]
            return {"action": "ABORT", "dlq_enqueued": True, "circuit_state": cb.state.name if cb else "UNKNOWN"}
            
        # Check retry limits
        op_state.attempts += 1
        if op_state.attempts > policy.max_attempts:
            if service in self.fallback_registry:
                del self.active_operations[op_id]
                return {
                    "action": "FALLBACK",
                    "fallback_payload": self.fallback_registry[service](op_state.payload),
                    "circuit_state": cb.state.name if cb else "UNKNOWN"
                }
            self.dlq.enqueue(op_state, "Retry exhausted")
            del self.active_operations[op_id]
            return {"action": "ABORT", "dlq_enqueued": True, "circuit_state": cb.state.name if cb else "UNKNOWN"}
            
        # Calculate backoff for retry
        delay_ms = self._calculate_backoff(policy, op_state.attempts)
        if category == ErrorCategory.RATE_LIMIT:
            delay_ms *= 2.0 # Penalty for rate limits
            
        return {
            "action": "RETRY",
            "delay_ms": delay_ms,
            "circuit_state": cb.state.name if cb else "UNKNOWN",
            "dlq_enqueued": False
        }

if __name__ == "__main__":
    # Example usage
    agent = RetryRecoveryAgent()
    agent.configure_service("db_write", RetryPolicy(max_attempts=3), CircuitBreakerConfig(failure_threshold=2))
    
    agent.register_fallback("db_write", lambda p: {"status": "saved_to_local_cache", "original": p})
    
    # Simulate failures
    for i in range(3):
        eval_res = agent.evaluate_operation("op123", "db_write", {"data": 42})
        if eval_res["action"] == "PROCEED":
            res = agent.report_failure("op123", "TIMEOUT", "Connection timed out")
            print(f"Attempt {i+1} Failure Decision: {res}")
            
    # Should trigger fallback or abort depending on config
    eval_res = agent.evaluate_operation("op999", "db_write", {"data": 99})
    print(f"Subsequent operation eval: {eval_res}")
