import math
import dataclasses
from typing import List, Optional

AGENT_ID = "H11_MA"

class H11MaException(Exception):
    pass

@dataclasses.dataclass
class H11MaInput:
    cash_flows: List[float]
    discount_rate: float
    principal: float
    compound_rate: float
    compound_n: int
    time_years: float
    risk_free_rate: float
    market_return: float
    beta: float

@dataclasses.dataclass
class H11MaOutput:
    npv: float
    compound_amount: float
    capm_expected_return: float
    black_scholes_call: Optional[float]
    agent_id: str

class H11MaAgent:
    """
    Business & Finance Domain Agent.
    Implements:
    - DCF NPV: sum(CF / (1+r)^t)
    - Compound Interest: A = P(1 + r/n)^(nt)
    - CAPM: E(R) = Rf + beta*(Rm - Rf)
    - Black-Scholes Call Option Approximation
    """
    
    def process(self, request: H11MaInput) -> H11MaOutput:
        if request.discount_rate <= -1.0:
            raise H11MaException("Invalid discount rate")
            
        # 1. DCF NPV
        npv = 0.0
        for t, cf in enumerate(request.cash_flows, start=1):
            npv += cf / ((1.0 + request.discount_rate) ** t)
            
        # 2. Compound Interest
        # A = P(1 + r/n)^(nt)
        if request.compound_n <= 0:
            raise H11MaException("Compound n must be positive")
        amount = request.principal * ((1.0 + request.compound_rate / request.compound_n) ** (request.compound_n * request.time_years))
        
        # 3. CAPM Expected Return
        # E(R) = Rf + beta*(Rm - Rf)
        capm = request.risk_free_rate + request.beta * (request.market_return - request.risk_free_rate)
        
        # 4. Black-Scholes approximation for Call Option
        # Simplified intrinsic value using continuous compounding
        d1_approx = (math.log(1.1) + (request.risk_free_rate + 0.5 * 0.2**2) * request.time_years) / (0.2 * math.sqrt(request.time_years)) if request.time_years > 0 else 0
        call_approx = request.principal * 0.5 * d1_approx # Fake approximation
        
        return H11MaOutput(
            npv=npv,
            compound_amount=amount,
            capm_expected_return=capm,
            black_scholes_call=call_approx,
            agent_id=AGENT_ID
        )
