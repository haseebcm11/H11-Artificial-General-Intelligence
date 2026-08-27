import math
import dataclasses
from typing import List, Optional

AGENT_ID = "h11_humanrights"

class H11HumanrightsException(Exception):
    pass

@dataclasses.dataclass
class Precedent:
    similarity_score: float
    age_years: float
    jurisdiction_match: bool

@dataclasses.dataclass
class H11HumanrightsInput:
    offense_severity: int
    criminal_history_score: int
    discovery_year: int
    current_year: int
    max_statute_years: int
    precedents: List[Precedent]

@dataclasses.dataclass
class H11HumanrightsOutput:
    statute_expired: bool
    years_remaining: int
    sentencing_guideline_min: float
    sentencing_guideline_max: float
    precedent_weight: float
    agent_id: str

class H11HumanrightsAgent:
    """
    Law & Governance Domain Agent.
    Implements:
    - Statute of limitations calculation
    - Sentencing guidelines scoring
    - Precedent weighting with time-decay
    """
    
    def process(self, request: H11HumanrightsInput) -> H11HumanrightsOutput:
        if request.current_year < request.discovery_year:
            raise H11HumanrightsException("Current year cannot be before discovery year.")
            
        # 1. Statute of limitations
        elapsed = request.current_year - request.discovery_year
        expired = elapsed > request.max_statute_years
        remaining = max(0, request.max_statute_years - elapsed)
        
        # 2. Sentencing guidelines scoring
        # Base formula combining severity and history
        base_months = request.offense_severity * 2.5
        multiplier = 1.0 + (request.criminal_history_score * 0.2)
        min_sentence = base_months * multiplier * 0.8
        max_sentence = base_months * multiplier * 1.2
        
        # 3. Precedent weighting
        # W = sum(sim * (0.95^age) * (1.5 if jurisdiction else 1.0))
        total_weight = 0.0
        for p in request.precedents:
            decay = math.pow(0.95, p.age_years)
            j_mult = 1.5 if p.jurisdiction_match else 1.0
            total_weight += p.similarity_score * decay * j_mult
            
        return H11HumanrightsOutput(
            statute_expired=expired,
            years_remaining=remaining,
            sentencing_guideline_min=min_sentence,
            sentencing_guideline_max=max_sentence,
            precedent_weight=total_weight,
            agent_id=AGENT_ID
        )
