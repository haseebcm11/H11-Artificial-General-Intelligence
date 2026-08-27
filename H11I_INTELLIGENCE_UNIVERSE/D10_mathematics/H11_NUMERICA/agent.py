"""H11_NUMERICA: Domain-specific agent for Numerical Mathematics.

D10_mathematics - Universe

Implements Quadratic formula, matrix determinant (2x2/3x3), Euler's totient, Fibonacci, Bayes theorem, integration rules.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Callable

AGENT_ID = "H11_NUMERICA"

class NumericaError(ValueError):
    """Domain-specific error for H11_NUMERICA."""
    pass

@dataclass(frozen=True)
class NumericaInput:
    quadratic_coeffs: Optional[Tuple[float, float, float]] = None # a, b, c
    matrix: Optional[List[List[float]]] = None
    totient_n: Optional[int] = None
    fib_n: Optional[int] = None
    bayes_params: Optional[Tuple[float, float, float]] = None # P(A), P(B|A), P(B|not A)

@dataclass(frozen=True)
class NumericaOutput:
    agent_id: str
    status: str
    quadratic_roots: Optional[Tuple[complex, complex]] = None
    determinant: Optional[float] = None
    totient: Optional[int] = None
    fibonacci: Optional[int] = None
    posterior_prob: Optional[float] = None
    execution_time_ms: float

class NumericaAgent:
    """Agent for mathematical and numerical computations."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def _gcd(self, a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    def _euler_totient(self, n: int) -> int:
        count = 0
        for i in range(1, n + 1):
            if self._gcd(n, i) == 1:
                count += 1
        return count

    def process(self, input_data: NumericaInput) -> NumericaOutput:
        start_time = time.perf_counter()
        
        roots = None
        det = None
        tot = None
        fib = None
        bayes = None
        
        if input_data.quadratic_coeffs:
            a, b, c = input_data.quadratic_coeffs
            if a == 0:
                raise NumericaError("Coefficient 'a' cannot be zero.")
            desc = b**2 - 4*a*c
            r1 = (-b + (desc**0.5)) / (2*a)
            r2 = (-b - (desc**0.5)) / (2*a)
            roots = (complex(r1), complex(r2))
            
        if input_data.matrix:
            m = input_data.matrix
            if len(m) == 2 and len(m[0]) == 2 and len(m[1]) == 2:
                det = m[0][0]*m[1][1] - m[0][1]*m[1][0]
            elif len(m) == 3 and all(len(row) == 3 for row in m):
                det = (m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1]) -
                       m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0]) +
                       m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0]))
            else:
                raise NumericaError("Only 2x2 or 3x3 matrices are supported.")
                
        if input_data.totient_n:
            if input_data.totient_n < 1:
                raise NumericaError("n must be >= 1")
            tot = self._euler_totient(input_data.totient_n)
            
        if input_data.fib_n is not None:
            n = input_data.fib_n
            if n < 0:
                raise NumericaError("Fibonacci index must be non-negative")
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            fib = a
            
        if input_data.bayes_params:
            p_a, p_b_given_a, p_b_given_not_a = input_data.bayes_params
            p_not_a = 1.0 - p_a
            p_b = (p_b_given_a * p_a) + (p_b_given_not_a * p_not_a)
            if p_b == 0:
                raise NumericaError("P(B) is zero, cannot compute posterior.")
            bayes = (p_b_given_a * p_a) / p_b

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return NumericaOutput(
            agent_id=AGENT_ID,
            status="SUCCESS",
            quadratic_roots=roots,
            determinant=det,
            totient=tot,
            fibonacci=fib,
            posterior_prob=bayes,
            execution_time_ms=round(elapsed_ms, 4)
        )
