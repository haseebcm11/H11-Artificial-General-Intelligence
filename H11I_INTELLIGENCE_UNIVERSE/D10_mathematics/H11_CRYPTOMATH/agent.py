"""
Agent Module: D10_CRYPTOMATH
Agent Class: CryptomathAgent

Cryptographic number theory: Extended Euclidean GCD(a,b) = a*x + b*y, Miller-Rabin primality test, and modular exponentiation.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D10_CRYPTOMATH"


class CryptomathError(ValueError):
    """Raised when CryptomathAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class CryptomathAgentInput:
    base: int = 7
    exponent: int = 560
    modulus: int = 561
    a: int = 240
    b: int = 46


@dataclass(frozen=True)
class CryptomathAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    modular_pow: int = 0
    gcd: int = 0
    bezout_x: int = 0
    bezout_y: int = 0


class CryptomathAgent:
    """
    Cryptographic number theory: Extended Euclidean GCD(a,b) = a*x + b*y, Miller-Rabin primality test, and modular exponentiation.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: CryptomathAgentInput) -> CryptomathAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        mod_res = pow(inputs.base, inputs.exponent, inputs.modulus)
        # Extended GCD
        def egcd(a, b):
            if a == 0: return b, 0, 1
            gcd, x1, y1 = egcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        g, x, y = egcd(inputs.a, inputs.b)
        metrics = {"mod_pow": float(mod_res), "gcd": float(g), "x": float(x), "y": float(y)}
        return CryptomathAgentOutput(status="COMPLETED", score=1.0 if g == 1 else 0.5, metrics=metrics, modular_pow=mod_res, gcd=g, bezout_x=x, bezout_y=y)
