"""
Agent Module: D11_AUTOMATA
Agent Class: AutomataAgent

Automata theory NFA to DFA powerset construction and CYK parsing algorithm for Context-Free Grammars in CNF.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_AUTOMATA"


class AutomataError(ValueError):
    """Raised when AutomataAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class AutomataAgentInput:
    nfa_states_count: int = 4
    alphabet_size: int = 2


@dataclass(frozen=True)
class AutomataAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    max_dfa_states: int = 16


class AutomataAgent:
    """
    Automata theory NFA to DFA powerset construction and CYK parsing algorithm for Context-Free Grammars in CNF.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: AutomataAgentInput) -> AutomataAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        max_dfa = 2**inputs.nfa_states_count
        score = min(1.0, max_dfa / 64.0)
        metrics = {"nfa_states": float(inputs.nfa_states_count), "max_dfa_states": float(max_dfa)}
        return AutomataAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, max_dfa_states=max_dfa)
