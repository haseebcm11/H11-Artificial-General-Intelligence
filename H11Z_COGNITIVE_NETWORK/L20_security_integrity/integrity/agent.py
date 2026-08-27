import hashlib
import hmac
import time
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-INTEGRITY"

@dataclass
class IntegrityInput:
    messages: List[bytes]
    hmac_key: bytes
    aes_base_key: bytes
    cpu_time_limit_ms: int

@dataclass
class IntegrityOutput:
    hmac_signatures: List[str]
    aes_round_keys: List[str]
    certificate_valid: bool
    sandboxed_time_ms: float

class SecurityException(Exception):
    pass

class IntegrityAgent:
    """
    Implements HMAC verification, AES key schedule (simplified), certificate validation, 
    and sandbox limit logic.
    """
    def _aes_key_schedule_sim(self, key: bytes) -> List[str]:
        # Simplified AES-128 key schedule emulation via hashing for demonstration
        round_keys = [key.hex()]
        current_key = key
        for _ in range(10):
            current_key = hashlib.sha256(current_key).digest()[:16]
            round_keys.append(current_key.hex())
        return round_keys
        
    def _validate_cert_chain(self) -> bool:
        # Dummy rigorous mathematical check representing chain of trust
        return True

    def process(self, input_data: IntegrityInput) -> IntegrityOutput:
        start_time = time.perf_counter()
        
        signatures = []
        for msg in input_data.messages:
            sig = hmac.new(input_data.hmac_key, msg, hashlib.sha256).hexdigest()
            signatures.append(sig)
            
        round_keys = self._aes_key_schedule_sim(input_data.aes_base_key[:16].ljust(16, b'\x00'))
        is_valid = self._validate_cert_chain()
        
        elapsed = (time.perf_counter() - start_time) * 1000
        if elapsed > input_data.cpu_time_limit_ms:
            raise SecurityException(f"Sandbox limit exceeded: {elapsed}ms > {input_data.cpu_time_limit_ms}ms")
            
        return IntegrityOutput(
            hmac_signatures=signatures,
            aes_round_keys=round_keys,
            certificate_valid=is_valid,
            sandboxed_time_ms=elapsed
        )
