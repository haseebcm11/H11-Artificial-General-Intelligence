"""H11-CRYPTOANALYSIS: Domain-specific agent for Cybersecurity.

D12_cybersecurity - Universe

Implements Shannon entropy H=-sum(p*log2(p)), RSA modular arithmetic, Diffie-Hellman key exchange.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-CRYPTOANALYSIS"

class CryptoAnalysisError(ValueError):
    """Domain-specific error for H11-CRYPTOANALYSIS."""
    pass

@dataclass(frozen=True)
class RsaParams:
    message: int
    e: int
    n: int

@dataclass(frozen=True)
class DiffieHellmanParams:
    g: int
    p: int
    private_key: int
    other_public_key: Optional[int] = None

@dataclass(frozen=True)
class CryptoAnalysisInput:
    probabilities: Optional[List[float]] = None
    rsa: Optional[RsaParams] = None
    dh: Optional[DiffieHellmanParams] = None

@dataclass(frozen=True)
class CryptoAnalysisOutput:
    agent_id: str
    status: str
    shannon_entropy: Optional[float] = None
    rsa_ciphertext: Optional[int] = None
    dh_public_key: Optional[int] = None
    dh_shared_secret: Optional[int] = None
    execution_time_ms: float

class CryptoAnalysisAgent:
    """Agent for cryptographic analysis and cybersecurity fundamentals."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: CryptoAnalysisInput) -> CryptoAnalysisOutput:
        start_time = time.perf_counter()
        
        entropy = None
        rsa_c = None
        dh_pub = None
        dh_sec = None
        
        if input_data.probabilities is not None:
            probs = input_data.probabilities
            if not all(0 <= p <= 1 for p in probs):
                raise CryptoAnalysisError("Probabilities must be between 0 and 1")
            total = sum(probs)
            if not math.isclose(total, 1.0, rel_tol=1e-5):
                raise CryptoAnalysisError("Probabilities must sum to 1")
            
            entropy = -sum(p * math.log2(p) for p in probs if p > 0)
            
        if input_data.rsa is not None:
            # RSA Modular Exponentiation: C = M^e mod n
            rsa_c = pow(input_data.rsa.message, input_data.rsa.e, input_data.rsa.n)
            
        if input_data.dh is not None:
            dh = input_data.dh
            # DH Public Key: g^a mod p
            dh_pub = pow(dh.g, dh.private_key, dh.p)
            
            if dh.other_public_key is not None:
                # DH Shared Secret: B^a mod p
                dh_sec = pow(dh.other_public_key, dh.private_key, dh.p)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return CryptoAnalysisOutput(
            agent_id=AGENT_ID,
            status="SUCCESS",
            shannon_entropy=entropy,
            rsa_ciphertext=rsa_c,
            dh_public_key=dh_pub,
            dh_shared_secret=dh_sec,
            execution_time_ms=round(elapsed_ms, 4)
        )
